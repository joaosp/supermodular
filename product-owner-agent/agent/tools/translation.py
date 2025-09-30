"""Business to technical requirement translation tools."""

from pathlib import Path
from typing import Any, Dict, List

from claude_agent_sdk import tool

from ..config import get_settings


def load_translation_prompt() -> str:
    """Load the translation prompt template."""
    prompt_path = Path(__file__).parent.parent.parent / "prompts" / "translation.txt"
    with open(prompt_path, "r") as f:
        return f.read()


@tool(
    "translate_epic_to_stories",
    "Translate a business epic into technical user stories. Use Atlassian MCP jira_get_issue to fetch the epic first.",
    {
        "epic_key": str,
        "epic_summary": str,
        "epic_description": str,
        "architecture_type": str,
        "component_list": str,
        "team_skills": str,
    },
)
async def translate_epic_to_stories(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translate a JIRA epic from business requirements to technical stories.

    This tool expects epic data to be provided (fetched via Atlassian MCP jira_get_issue),
    analyzes the business requirements, and generates detailed technical specifications
    that can be broken down into implementable user stories.

    Args:
        epic_key: JIRA epic key (e.g., "EPIC-123")
        epic_summary: Epic summary from JIRA
        epic_description: Epic description from JIRA
        architecture_type: System architecture (e.g., "microservices", "monolithic")
        component_list: Comma-separated list of existing components
        team_skills: Comma-separated list of team capabilities

    Returns:
        Dictionary containing translation prompt and guidance
    """
    try:
        # Get Outsystems version from config
        settings = get_settings()
        version = settings.outsystems.version

        business_requirement = f"{args['epic_summary']}\n\n{args['epic_description']}"

        # Format the prompt
        prompt_template = load_translation_prompt()
        formatted_prompt = prompt_template.format(
            business_requirement=business_requirement,
            version=version,
            architecture_type=args["architecture_type"],
            component_list=args["component_list"],
            team_skills=args["team_skills"],
        )

        # Return the formatted prompt for the agent to process
        # The actual translation will be done by the Claude agent
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Epic '{args['epic_key']}' ready to translate.\n\n{formatted_prompt}",
                }
            ]
        }

    except Exception as e:
        return {
            "content": [
                {"type": "text", "text": f"Error translating epic: {str(e)}"}
            ],
            "isError": True,
        }




@tool(
    "create_stories_from_spec",
    "Guide for creating JIRA stories from technical specifications. Use Atlassian MCP jira_create_issue for each story.",
    {
        "epic_key": str,
        "project_key": str,
        "stories_json": str,  # JSON string of stories list
    },
)
async def create_stories_from_spec(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Provide guidance for creating JIRA user stories from a technical specification.

    NOTE: This tool provides instructions. Actual story creation should be done using
    Atlassian MCP jira_create_issue tool for each story.

    Args:
        epic_key: Parent epic key to link stories to
        project_key: JIRA project key
        stories_json: JSON string containing list of stories

    Returns:
        Instructions for creating stories via Atlassian MCP
    """
    try:
        import json

        stories = json.loads(args["stories_json"])

        if not isinstance(stories, list):
            raise ValueError("stories_json must be a JSON array")

        instructions = f"""Ready to create {len(stories)} stories in project {args['project_key']}.

For each story, use the Atlassian MCP jira_create_issue tool with:
- project: {args['project_key']}
- issuetype: Story
- parent: {args['epic_key']} (epic link)
- summary: [story title]
- description: [story description]

Stories to create:
"""
        for i, story in enumerate(stories, 1):
            instructions += f"\n{i}. {story.get('title', 'Untitled')}"

        return {
            "content": [
                {
                    "type": "text",
                    "text": instructions,
                }
            ]
        }

    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error processing stories: {str(e)}",
                }
            ],
            "isError": True,
        }