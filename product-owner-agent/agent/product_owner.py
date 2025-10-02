"""Core Product Owner Agent implementation using Claude Agent SDK."""

import asyncio
import logging
import sys
from typing import Any, Dict, List, Optional

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    create_sdk_mcp_server,
    CLINotFoundError,
    ProcessError,
    PermissionResultAllow,
    PermissionResultDeny,
)

from .config import get_settings
from .tools.translation import (
    translate_epic_to_stories,
    create_stories_from_spec,
)
from .tools.reporting import generate_sprint_report, save_report_to_jira
from .tools.dependency import analyze_dependencies, generate_gantt_chart

# Configure logging
logger = logging.getLogger(__name__)


class ProductOwnerAgent:
    """
    Product Owner Agent for Outsystems.

    This agent automates Product Owner responsibilities including:
    - Business to technical requirements translation
    - Automated progress reporting
    - Risk and dependency analysis
    """

    def __init__(self):
        """Initialize the Product Owner Agent."""
        self.settings = get_settings()
        self.client: Optional[ClaudeSDKClient] = None

        # Create MCP server with custom tools
        self.tools_server = create_sdk_mcp_server(
            name="product-owner-tools",
            version="1.0.0",
            tools=[
                translate_epic_to_stories,
                create_stories_from_spec,
                generate_sprint_report,
                save_report_to_jira,
                analyze_dependencies,
                generate_gantt_chart,
            ],
        )

    async def _permission_handler(
        self, tool_name: str, input_data: dict, _context: dict
    ) -> PermissionResultAllow:
        """
        Permission handler for tool usage.
        Auto-approves all MCP tools (Product Owner and Atlassian).

        Args:
            tool_name: Name of the tool being invoked
            input_data: Input parameters for the tool
            _context: Additional context information (unused)

        Returns:
            PermissionResultAllow object to auto-approve all tools
        """
        logger.debug(f"Permission requested for tool: {tool_name}")
        logger.debug(f"Input data: {input_data}")

        # Auto-approve all MCP tools and pass through input
        if tool_name.startswith("mcp__po_tools__") or tool_name.startswith(
            "mcp__atlassian__"
        ):
            logger.debug(f"Auto-approving MCP tool: {tool_name}")
            return PermissionResultAllow(updated_input=input_data or {})

        # Default: allow all tools
        logger.debug(f"Allowing tool: {tool_name}")
        return PermissionResultAllow(updated_input=input_data or {})

    def _get_agent_options(self) -> ClaudeAgentOptions:
        """
        Get Claude Agent options with tool configuration.

        Returns:
            Configured ClaudeAgentOptions
        """
        mcp_servers = {
            "po_tools": self.tools_server,
            "atlassian": {
                "command": "npx",
                "args": ["-y", "mcp-remote", "https://mcp.atlassian.com/v1/sse"]
            }
        }

        logger.info(f"Configuring MCP servers: {list(mcp_servers.keys())}")
        logger.info(f"Atlassian MCP config: command={mcp_servers['atlassian']['command']}, "
                   f"url={mcp_servers['atlassian']['args'][-1]}")

        return ClaudeAgentOptions(
            mcp_servers=mcp_servers,
            allowed_tools=[
                # Custom Product Owner tools
                "mcp__po_tools__translate_epic_to_stories",
                "mcp__po_tools__create_stories_from_spec",
                "mcp__po_tools__generate_sprint_report",
                "mcp__po_tools__save_report_to_jira",
                "mcp__po_tools__analyze_dependencies",
                "mcp__po_tools__generate_gantt_chart",
                # Atlassian User & Resources
                "mcp__atlassian__atlassianUserInfo",
                "mcp__atlassian__getAccessibleAtlassianResources",
                # Atlassian MCP tools (JIRA)
                "mcp__atlassian__getJiraIssue",
                "mcp__atlassian__editJiraIssue",
                "mcp__atlassian__createJiraIssue",
                "mcp__atlassian__getTransitionsForJiraIssue",
                "mcp__atlassian__transitionJiraIssue",
                "mcp__atlassian__lookupJiraAccountId",
                "mcp__atlassian__searchJiraIssuesUsingJql",
                "mcp__atlassian__addCommentToJiraIssue",
                "mcp__atlassian__getJiraIssueRemoteIssueLinks",
                "mcp__atlassian__getVisibleJiraProjects",
                "mcp__atlassian__getJiraProjectIssueTypesMetadata",
                # Atlassian MCP tools (Confluence)
                "mcp__atlassian__getConfluenceSpaces",
                "mcp__atlassian__getConfluencePage",
                "mcp__atlassian__getPagesInConfluenceSpace",
                "mcp__atlassian__getConfluencePageFooterComments",
                "mcp__atlassian__getConfluencePageInlineComments",
                "mcp__atlassian__getConfluencePageDescendants",
                "mcp__atlassian__createConfluencePage",
                "mcp__atlassian__updateConfluencePage",
                "mcp__atlassian__createConfluenceFooterComment",
                "mcp__atlassian__createConfluenceInlineComment",
                "mcp__atlassian__searchConfluenceUsingCql",
                # Rovo Search & Fetch
                "mcp__atlassian__search",
                "mcp__atlassian__fetch",
                # Allow basic file operations
                "Read",
                "Write",
            ],
            can_use_tool=self._permission_handler,
            system_prompt="""You are a Product Owner Agent specialized in Outsystems development.

Your primary responsibilities are:
1. Translate business requirements into detailed technical specifications
2. Generate comprehensive progress reports from JIRA and Confluence data
3. Identify and analyze cross-team dependencies and risks

Guidelines:
- Use clear, professional language suitable for stakeholders
- Quantify impacts and provide specific recommendations
- Format outputs as JIRA-compatible markdown
- Always consider the Outsystems platform context
- Prioritize actionable insights over general observations

Available Atlassian MCP tools:
- getAccessibleAtlassianResources: Get your Atlassian Cloud IDs
- atlassianUserInfo: Get current user information
- searchJiraIssuesUsingJql: Search JIRA issues using JQL
- getJiraIssue: Get detailed issue information (requires cloudId and issueIdOrKey)
- createJiraIssue: Create new JIRA issues
- editJiraIssue: Update existing issues
- addCommentToJiraIssue: Add comments to issues
- getVisibleJiraProjects: List visible JIRA projects
- search: Rovo Search for both JIRA and Confluence content
- getConfluenceSpaces: List Confluence spaces
- getConfluencePage: Get Confluence page content
- createConfluencePage: Create new Confluence pages
- searchConfluenceUsingCql: Search Confluence using CQL

Custom Product Owner tools:
- translate_epic_to_stories: Convert business epics to technical stories
- create_stories_from_spec: Create JIRA stories from specifications
- generate_sprint_report: Generate comprehensive sprint reports
- save_report_to_jira: Save reports as JIRA attachments
- analyze_dependencies: Analyze cross-team dependencies
- generate_gantt_chart: Create visual dependency timelines

When asked to perform a task, use the appropriate Atlassian MCP tools to fetch data from JIRA/Confluence,
then use custom tools for specialized analysis and reporting.""",
            permission_mode="acceptEdits",
        )

    async def translate_epic(
        self,
        epic_key: str,
        architecture_type: str = "microservices",
        component_list: str = "",
        team_skills: str = "",
    ) -> str:
        """
        Translate a business epic into technical user stories.

        Args:
            epic_key: JIRA epic key
            architecture_type: System architecture type
            component_list: Existing components
            team_skills: Team capabilities

        Returns:
            Translation result

        Raises:
            CLINotFoundError: If Claude Code CLI is not found and ANTHROPIC_API_KEY is not set
            ProcessError: If there's an error with the Claude CLI process
        """
        prompt = f"""Translate the epic {epic_key} into detailed technical user stories.

Architecture: {architecture_type}
Existing components: {component_list or 'None specified'}
Team skills: {team_skills or 'General development'}

Use the translate_epic_to_stories tool to fetch the epic and generate technical specifications.
Break down the requirements into implementable stories with clear acceptance criteria."""

        try:
            options = self._get_agent_options()
            result = []

            async with ClaudeSDKClient(options=options) as client:
                await client.query(prompt)
                async for message in client.receive_response():
                    text = self._extract_text_from_message(message)
                    if text:
                        result.append(text)

            return "".join(result)
        except CLINotFoundError:
            raise CLINotFoundError(
                "Claude Code CLI not found. Please install it with:\n"
                "  npm install -g @anthropic-ai/claude-code\n"
                "Or set ANTHROPIC_API_KEY environment variable to use the API directly."
            )
        except ProcessError as e:
            raise ProcessError(
                f"Claude CLI process error (exit code: {e.exit_code}). "
                "Try setting ANTHROPIC_API_KEY environment variable to use the API directly.",
                exit_code=e.exit_code
            )

    async def generate_report(
        self, board_id: int, sprint_id: int = 0, team_name: str = "Team"
    ) -> str:
        """
        Generate a sprint progress report.

        Args:
            board_id: JIRA board ID
            sprint_id: Sprint ID (0 for active sprint)
            team_name: Team name

        Returns:
            Generated report

        Raises:
            CLINotFoundError: If Claude Code CLI is not found and ANTHROPIC_API_KEY is not set
            ProcessError: If there's an error with the Claude CLI process
        """
        prompt = f"""Generate a comprehensive sprint progress report.

Board ID: {board_id}
Sprint ID: {sprint_id if sprint_id > 0 else 'Active sprint'}
Team: {team_name}

Use the generate_sprint_report tool to fetch sprint data and create a detailed report including:
- Executive summary
- Team performance metrics
- Key achievements
- Blockers and risks
- Next sprint priorities

Format the report professionally for stakeholder consumption."""

        try:
            options = self._get_agent_options()
            result = []

            async with ClaudeSDKClient(options=options) as client:
                await client.query(prompt)
                async for message in client.receive_response():
                    text = self._extract_text_from_message(message)
                    if text:
                        result.append(text)

            return "".join(result)
        except CLINotFoundError:
            raise CLINotFoundError(
                "Claude Code CLI not found. Please install it with:\n"
                "  npm install -g @anthropic-ai/claude-code\n"
                "Or set ANTHROPIC_API_KEY environment variable to use the API directly."
            )
        except ProcessError as e:
            raise ProcessError(
                f"Claude CLI process error (exit code: {e.exit_code}). "
                "Try setting ANTHROPIC_API_KEY environment variable to use the API directly.",
                exit_code=e.exit_code
            )

    async def analyze_risks(
        self, jql_query: str, initiative_name: str, target_date: str
    ) -> str:
        """
        Analyze dependencies and risks for an initiative.

        Args:
            jql_query: JQL query to fetch relevant issues
            initiative_name: Initiative name
            target_date: Target completion date (YYYY-MM-DD)

        Returns:
            Risk analysis report

        Raises:
            CLINotFoundError: If Claude Code CLI is not found and ANTHROPIC_API_KEY is not set
            ProcessError: If there's an error with the Claude CLI process
        """
        prompt = f"""Analyze dependencies and risks for the initiative: {initiative_name}

JQL Query: {jql_query}
Target Date: {target_date}

Use the analyze_dependencies tool to:
1. Map all cross-team dependencies
2. Identify the critical path
3. Detect blocking issues
4. Calculate timeline risks
5. Provide mitigation recommendations

Then use generate_gantt_chart to create a visual timeline.

Provide a comprehensive risk assessment with actionable recommendations."""

        try:
            options = self._get_agent_options()
            result = []

            async with ClaudeSDKClient(options=options) as client:
                await client.query(prompt)
                async for message in client.receive_response():
                    text = self._extract_text_from_message(message)
                    if text:
                        result.append(text)

            return "".join(result)
        except CLINotFoundError:
            raise CLINotFoundError(
                "Claude Code CLI not found. Please install it with:\n"
                "  npm install -g @anthropic-ai/claude-code\n"
                "Or set ANTHROPIC_API_KEY environment variable to use the API directly."
            )
        except ProcessError as e:
            raise ProcessError(
                f"Claude CLI process error (exit code: {e.exit_code}). "
                "Try setting ANTHROPIC_API_KEY environment variable to use the API directly.",
                exit_code=e.exit_code
            )

    def _extract_text_from_message(self, message: Any) -> str:
        """
        Extract displayable text from a message object.

        Args:
            message: Message object from Claude SDK

        Returns:
            Extracted text content or empty string
        """
        # Handle string messages
        if isinstance(message, str):
            return message

        # Handle dict-like objects
        if hasattr(message, "__dict__"):
            msg_dict = message.__dict__
        elif isinstance(message, dict):
            msg_dict = message
        else:
            return str(message)

        # Skip tool use messages (internal operations) - check this first
        if msg_dict.get("subtype") in ["init", "tool_use", "tool_result"]:
            return ""

        # Extract text from content blocks
        if "content" in msg_dict:
            content = msg_dict["content"]
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                text_parts = []
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                    elif hasattr(block, "text"):
                        text_parts.append(block.text)
                return "".join(text_parts)

        # Handle direct text attribute
        if "text" in msg_dict:
            return msg_dict["text"]

        return ""

    async def interactive_session(self) -> None:
        """
        Start an interactive session with the agent.

        Raises:
            CLINotFoundError: If Claude Code CLI is not found and ANTHROPIC_API_KEY is not set
            ProcessError: If there's an error with the Claude CLI process
        """
        options = self._get_agent_options()

        print("Product Owner Agent - Interactive Mode")
        print("=" * 50)
        print("Commands:")
        print("  - translate <epic-key>: Translate epic to stories")
        print("  - report <board-id> [sprint-id]: Generate sprint report")
        print("  - analyze <jql>: Analyze dependencies and risks")
        print("  - help: Show available commands")
        print("  - exit: Exit the session")
        print("=" * 50)

        try:
            async with ClaudeSDKClient(options=options) as client:
                self.client = client

                while True:
                    try:
                        user_input = input("\nYou: ").strip()

                        if not user_input:
                            continue

                        if user_input.lower() == "exit":
                            print("Goodbye!")
                            break

                        if user_input.lower() == "help":
                            print(
                                """
Available commands:
- translate <epic-key>: Translate an epic to technical stories
- report <board-id> [sprint-id]: Generate sprint progress report
- analyze <jql> <initiative> <target-date>: Analyze risks and dependencies
- custom: Any custom query about product management

You can also ask questions in natural language."""
                            )
                            continue

                        # Send query to agent
                        await client.query(user_input)

                        # Thinking animation with spinner
                        thinking_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
                        thinking_idx = 0
                        has_output = False

                        print()  # New line before agent response

                        # Stream response with clean text extraction and thinking animation
                        async for message in client.receive_response():
                            text = self._extract_text_from_message(message)
                            if text:
                                # Clear thinking animation and show agent label
                                if not has_output:
                                    sys.stdout.write("\r\033[K")  # Clear line
                                    sys.stdout.write("Agent: ")
                                    sys.stdout.flush()
                                    has_output = True
                                print(text, end="", flush=True)
                            else:
                                # Show thinking animation while processing
                                if not has_output:
                                    sys.stdout.write(f"\rAgent: {thinking_chars[thinking_idx % len(thinking_chars)]} thinking...")
                                    sys.stdout.flush()
                                    thinking_idx += 1

                        # Ensure we showed agent label even if no text
                        if not has_output:
                            sys.stdout.write("\r\033[K")
                            sys.stdout.write("Agent: [No response]\n")
                        else:
                            print()  # Final newline

                    except KeyboardInterrupt:
                        print("\n\nGoodbye!")
                        break
                    except Exception as e:
                        print(f"\nError: {str(e)}")
        except CLINotFoundError:
            print("\n❌ Claude Code CLI not found.")
            print("Please install it with:")
            print("  npm install -g @anthropic-ai/claude-code")
            print("\nOr set ANTHROPIC_API_KEY environment variable to use the API directly.")
            raise
        except ProcessError as e:
            print(f"\n❌ Claude CLI process error (exit code: {e.exit_code}).")
            print("Try setting ANTHROPIC_API_KEY environment variable to use the API directly.")
            raise

    async def one_shot_query(self, prompt: str) -> str:
        """
        Execute a single query without maintaining session.

        Args:
            prompt: Query prompt

        Returns:
            Agent response

        Raises:
            CLINotFoundError: If Claude Code CLI is not found and ANTHROPIC_API_KEY is not set
            ProcessError: If there's an error with the Claude CLI process
        """
        try:
            options = self._get_agent_options()
            result = []

            async with ClaudeSDKClient(options=options) as client:
                # Send the query
                await client.query(prompt)

                # Receive and collect the response
                async for message in client.receive_response():
                    text = self._extract_text_from_message(message)
                    if text:
                        result.append(text)

            return "".join(result)
        except CLINotFoundError:
            raise CLINotFoundError(
                "Claude Code CLI not found. Please install it with:\n"
                "  npm install -g @anthropic-ai/claude-code\n"
                "Or set ANTHROPIC_API_KEY environment variable to use the API directly."
            )
        except ProcessError as e:
            raise ProcessError(
                f"Claude CLI process error (exit code: {e.exit_code}). "
                "Try setting ANTHROPIC_API_KEY environment variable to use the API directly.",
                exit_code=e.exit_code
            )


# Convenience functions for common operations

async def translate_epic_cli(
    epic_key: str,
    architecture: str = "microservices",
    components: str = "",
    skills: str = "",
) -> str:
    """CLI wrapper for epic translation."""
    agent = ProductOwnerAgent()
    return await agent.translate_epic(epic_key, architecture, components, skills)


async def generate_report_cli(
    board_id: int, sprint_id: int = 0, team: str = "Team"
) -> str:
    """CLI wrapper for report generation."""
    agent = ProductOwnerAgent()
    return await agent.generate_report(board_id, sprint_id, team)


async def analyze_risks_cli(
    jql: str, initiative: str, target_date: str
) -> str:
    """CLI wrapper for risk analysis."""
    agent = ProductOwnerAgent()
    return await agent.analyze_risks(jql, initiative, target_date)