"""Sprint and initiative reporting tools."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from claude_agent_sdk import tool

from ..config import get_settings


def load_reporting_prompt() -> str:
    """Load the reporting prompt template."""
    prompt_path = Path(__file__).parent.parent.parent / "prompts" / "reporting.txt"
    with open(prompt_path, "r") as f:
        return f.read()


def calculate_sprint_metrics(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate sprint metrics from JIRA issues.

    Args:
        issues: List of JIRA issues from sprint

    Returns:
        Dictionary of calculated metrics
    """
    completed = []
    in_progress = []
    blocked = []
    not_started = []

    total_story_points = 0
    completed_story_points = 0

    for issue in issues:
        fields = issue.get("fields", {})
        status = fields.get("status", {}).get("name", "")
        story_points = fields.get("customfield_10016", 0) or 0  # Common SP field

        total_story_points += story_points

        if status in ["Done", "Closed", "Resolved"]:
            completed.append(issue)
            completed_story_points += story_points
        elif status in ["In Progress", "In Review"]:
            in_progress.append(issue)
        elif status in ["Blocked", "Impediment"]:
            blocked.append(issue)
        else:
            not_started.append(issue)

    completion_rate = (
        (len(completed) / len(issues) * 100) if issues else 0
    )

    return {
        "total_issues": len(issues),
        "completed": completed,
        "in_progress": in_progress,
        "blocked": blocked,
        "not_started": not_started,
        "completion_rate": round(completion_rate, 1),
        "total_story_points": total_story_points,
        "completed_story_points": completed_story_points,
        "velocity": completed_story_points,
    }


def format_task_details(issues: List[Dict[str, Any]]) -> str:
    """Format task details for prompt."""
    details = []
    for issue in issues:
        fields = issue.get("fields", {})
        key = issue.get("key", "")
        summary = fields.get("summary", "")
        status = fields.get("status", {}).get("name", "")
        assignee = fields.get("assignee", {})
        assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"

        details.append(f"- {key}: {summary} [{status}] (Assignee: {assignee_name})")

    return "\n".join(details) if details else "No tasks"


def format_updates(issues: List[Dict[str, Any]]) -> str:
    """Format issue updates from provided issue data."""
    updates = []

    for issue in issues[:10]:  # Limit to recent 10 for performance
        key = issue.get("key", "")
        fields = issue.get("fields", {})

        # Extract comments if available
        comments = fields.get("comment", {}).get("comments", [])

        # Get latest 2 comments
        for comment in comments[-2:]:
            author = comment.get("author", {}).get("displayName", "Unknown")
            body = comment.get("body", "")[:200]  # Truncate long comments

            updates.append(f"[{key}] {author}: {body}")

    return "\n".join(updates) if updates else "No recent updates"


@tool(
    "generate_sprint_report",
    "Generate a comprehensive sprint progress report. Use Atlassian MCP jira_get_sprint and jira_search to fetch sprint data first.",
    {
        "sprint_name": str,
        "sprint_start": str,
        "sprint_end": str,
        "team_name": str,
        "issues_json": str,  # JSON string of sprint issues from Atlassian MCP
    },
)
async def generate_sprint_report(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a comprehensive sprint report with metrics and analysis.

    This tool expects sprint data to be provided (fetched via Atlassian MCP jira_get_sprint
    and jira_search), calculates metrics, and generates a formatted report.

    Args:
        sprint_name: Sprint name
        sprint_start: Sprint start date
        sprint_end: Sprint end date
        team_name: Name of the team
        issues_json: JSON string of sprint issues

    Returns:
        Formatted report prompt for Claude to process
    """
    try:
        import json

        issues = json.loads(args["issues_json"])

        # Calculate metrics
        metrics = calculate_sprint_metrics(issues)

        # Format data for prompt
        task_details = format_task_details(issues)
        recent_updates = format_updates(issues)

        # Load and format prompt
        prompt_template = load_reporting_prompt()
        formatted_prompt = prompt_template.format(
            sprint_id=args["sprint_name"],
            team_name=args["team_name"],
            sprint_start=args["sprint_start"],
            sprint_end=args["sprint_end"],
            completed_tasks=len(metrics["completed"]),
            in_progress_tasks=len(metrics["in_progress"]),
            blocked_tasks=len(metrics["blocked"]),
            not_started_tasks=len(metrics["not_started"]),
            task_details=task_details,
            recent_updates=recent_updates,
            previous_velocity="N/A",  # Would need historical data
            team_capacity=metrics["total_issues"],
            planned_points=metrics["total_story_points"],
            completed_points=metrics["completed_story_points"],
        )

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Sprint data analyzed successfully. Generating report...\n\n{formatted_prompt}",
                }
            ]
        }

    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error generating sprint report: {str(e)}",
                }
            ],
            "isError": True,
        }


@tool(
    "save_report_to_jira",
    "Save generated report locally and provide instructions for uploading to JIRA/Confluence",
    {
        "issue_key": str,
        "report_content": str,
        "report_name": str,
    },
)
async def save_report_to_jira(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save a generated report locally and provide instructions for JIRA/Confluence upload.

    This tool saves the report file locally. Use Atlassian MCP tools to upload to JIRA
    or create/update a Confluence page.

    Args:
        issue_key: JIRA issue key to attach report to (or Confluence page ID)
        report_content: Markdown content of the report
        report_name: Name for the report file

    Returns:
        File path and upload instructions
    """
    try:
        settings = get_settings()
        report_dir = settings.output.report_output_dir

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{args['report_name']}_{timestamp}.md"
        file_path = report_dir / filename

        # Write report to file
        with open(file_path, "w") as f:
            f.write(args["report_content"])

        instructions = f"""Report saved locally to: {file_path}

To share this report:
1. For JIRA: Use Atlassian MCP jira_add_comment to add the report content to issue {args['issue_key']}
2. For Confluence: Use Atlassian MCP confluence_create_page or confluence_update_page to publish the report

Report content is ready to be uploaded."""

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Report saved successfully:\n- File: {filename}\n- Attached to: {args['issue_key']}\n- Local copy: {file_path}",
                }
            ]
        }

    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error saving report: {str(e)}",
                }
            ],
            "isError": True,
        }


def generate_report_summary(report_content: str) -> str:
    """
    Generate a brief summary of the report for notifications.

    Args:
        report_content: Full report content

    Returns:
        Brief summary text
    """
    # Extract key metrics from report
    lines = report_content.split("\n")
    summary_lines = [line for line in lines if any(
        keyword in line.lower()
        for keyword in ["predictability", "velocity", "completion", "risk"]
    )]

    return "\n".join(summary_lines[:5]) if summary_lines else "Report generated successfully"