"""Dependency analysis and risk assessment tools."""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from claude_agent_sdk import tool

from ..config import get_settings


def load_risk_analysis_prompt() -> str:
    """Load the risk analysis prompt template."""
    prompt_path = Path(__file__).parent.parent.parent / "prompts" / "risk_analysis.txt"
    with open(prompt_path, "r") as f:
        return f.read()


def build_dependency_graph(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build a dependency graph from JIRA issues.

    Args:
        issues: List of JIRA issues with link information (from Atlassian MCP)

    Returns:
        Dependency graph structure
    """
    graph = {
        "nodes": {},
        "edges": [],
    }

    settings = get_settings()

    for issue in issues:
        key = issue.get("key", "")
        fields = issue.get("fields", {})

        # Add node
        graph["nodes"][key] = {
            "summary": fields.get("summary", ""),
            "status": fields.get("status", {}).get("name", ""),
            "assignee": fields.get("assignee", {}).get("displayName", "Unassigned")
            if fields.get("assignee")
            else "Unassigned",
            "team": fields.get(
                settings.atlassian.field_team_assignment, ""
            ),
            "due_date": fields.get("duedate", ""),
            "story_points": fields.get("customfield_10016", 0) or 0,
        }

        # Process issue links if present
        try:
            links = fields.get("issuelinks", [])
            for link in links:
                link_type = link.get("type", {}).get("name", "")

                # Determine direction of dependency
                if "outwardIssue" in link:
                    target_key = link["outwardIssue"]["key"]
                    direction = "outward"
                elif "inwardIssue" in link:
                    target_key = link["inwardIssue"]["key"]
                    direction = "inward"
                else:
                    continue

                graph["edges"].append(
                    {
                        "from": key if direction == "outward" else target_key,
                        "to": target_key if direction == "outward" else key,
                        "type": link_type,
                    }
                )
        except Exception:
            continue

    return graph


def find_critical_path(graph: Dict[str, Any]) -> List[str]:
    """
    Find the critical path through the dependency graph.

    Args:
        graph: Dependency graph

    Returns:
        List of issue keys on the critical path
    """
    # Simplified critical path using topological sort and longest path
    nodes = graph["nodes"]
    edges = graph["edges"]

    # Build adjacency list
    adj_list = {key: [] for key in nodes}
    in_degree = {key: 0 for key in nodes}

    for edge in edges:
        from_key = edge["from"]
        to_key = edge["to"]
        if from_key in adj_list and to_key in nodes:
            adj_list[from_key].append(to_key)
            in_degree[to_key] += 1

    # Find nodes with no dependencies
    queue = [key for key, degree in in_degree.items() if degree == 0]

    # Calculate longest path (story points)
    distances = {key: nodes[key]["story_points"] for key in nodes}
    predecessors = {key: None for key in nodes}

    while queue:
        current = queue.pop(0)

        for neighbor in adj_list[current]:
            new_distance = distances[current] + nodes[neighbor]["story_points"]

            if new_distance > distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current

            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Reconstruct critical path
    max_key = max(distances, key=distances.get)
    path = []
    current = max_key

    while current:
        path.append(current)
        current = predecessors[current]

    return list(reversed(path))


def identify_blockers(graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Identify blocking issues in the dependency graph.

    Args:
        graph: Dependency graph

    Returns:
        List of blocking issues with impact analysis
    """
    nodes = graph["nodes"]
    edges = graph["edges"]

    blockers = []

    for key, node in nodes.items():
        status = node["status"]

        # Check if issue is incomplete
        if status not in ["Done", "Closed", "Resolved"]:
            # Find what this issue blocks
            blocked_issues = [
                edge["to"] for edge in edges if edge["from"] == key
            ]

            if blocked_issues:
                # Check if blocked issues are waiting
                waiting_count = sum(
                    1
                    for blocked_key in blocked_issues
                    if blocked_key in nodes
                    and nodes[blocked_key]["status"]
                    not in ["Done", "Closed", "Resolved"]
                )

                if waiting_count > 0:
                    blockers.append(
                        {
                            "key": key,
                            "summary": node["summary"],
                            "status": status,
                            "blocks_count": waiting_count,
                            "blocked_issues": blocked_issues,
                            "assignee": node["assignee"],
                            "team": node["team"],
                        }
                    )

    return sorted(blockers, key=lambda x: x["blocks_count"], reverse=True)


def calculate_timeline_risk(graph: Dict[str, Any], target_date: str) -> Dict[str, Any]:
    """
    Calculate risk of missing target date based on current progress.

    Args:
        graph: Dependency graph
        target_date: Target completion date (YYYY-MM-DD)

    Returns:
        Risk assessment
    """
    nodes = graph["nodes"]

    total_points = sum(node["story_points"] for node in nodes.values())
    completed_points = sum(
        node["story_points"]
        for node in nodes.values()
        if node["status"] in ["Done", "Closed", "Resolved"]
    )

    completion_rate = (completed_points / total_points * 100) if total_points > 0 else 0

    try:
        target = datetime.strptime(target_date, "%Y-%m-%d")
        today = datetime.now()
        days_remaining = (target - today).days

        # Simple velocity calculation
        # Assuming average 5 points per week
        avg_velocity = 5
        weeks_remaining = days_remaining / 7
        estimated_points = weeks_remaining * avg_velocity

        remaining_points = total_points - completed_points

        if remaining_points > estimated_points:
            risk_level = "HIGH"
            confidence = 30
        elif remaining_points > estimated_points * 0.8:
            risk_level = "MEDIUM"
            confidence = 60
        else:
            risk_level = "LOW"
            confidence = 85

    except Exception:
        risk_level = "UNKNOWN"
        confidence = 0
        days_remaining = 0

    return {
        "risk_level": risk_level,
        "confidence": confidence,
        "completion_rate": round(completion_rate, 1),
        "days_remaining": days_remaining,
        "total_points": total_points,
        "completed_points": completed_points,
        "remaining_points": total_points - completed_points,
    }


@tool(
    "analyze_dependencies",
    "Analyze cross-team dependencies and identify risks. Use Atlassian MCP jira_search to fetch issues first.",
    {
        "initiative_name": str,
        "target_date": str,  # YYYY-MM-DD format
        "issues_json": str,  # JSON string of issues from Atlassian MCP
    },
)
async def analyze_dependencies(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze dependencies across teams and identify risks.

    This tool expects issue data to be provided (fetched via Atlassian MCP jira_search).

    Args:
        initiative_name: Name of the initiative
        target_date: Target completion date
        issues_json: JSON string of issues from Atlassian MCP

    Returns:
        Comprehensive dependency and risk analysis
    """
    try:
        import json

        # Parse issues from JSON
        issues = json.loads(args["issues_json"])

        if not issues:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"No issues provided for analysis",
                    }
                ],
                "isError": True,
            }

        # Build dependency graph
        graph = build_dependency_graph(issues)

        # Find critical path
        critical_path = find_critical_path(graph)

        # Identify blockers
        blockers = identify_blockers(graph)

        # Calculate timeline risk
        timeline_risk = calculate_timeline_risk(graph, args["target_date"])

        # Extract team information
        teams = set(
            node.get("team", "Unknown")
            for node in graph["nodes"].values()
            if node.get("team")
        )

        # Format data for analysis
        task_data = "\n".join(
            f"- {key}: {node['summary']} [{node['status']}] (Team: {node.get('team', 'N/A')}, SP: {node['story_points']})"
            for key, node in graph["nodes"].items()
        )

        dependency_data = "\n".join(
            f"- {edge['from']} blocks {edge['to']} ({edge['type']})"
            for edge in graph["edges"]
        )

        # Load and format prompt
        prompt_template = load_risk_analysis_prompt()
        formatted_prompt = prompt_template.format(
            initiative_name=args["initiative_name"],
            teams_list=", ".join(teams),
            start_date="N/A",
            target_date=args["target_date"],
            task_data=task_data,
            dependency_data=dependency_data or "No explicit dependencies found",
            historical_performance=f"Completion rate: {timeline_risk['completion_rate']}%, Risk level: {timeline_risk['risk_level']}",
        )

        summary = f"""Dependency Analysis Summary:
- Total Issues: {len(issues)}
- Teams Involved: {len(teams)}
- Critical Path Length: {len(critical_path)} issues
- Active Blockers: {len(blockers)}
- Timeline Risk: {timeline_risk['risk_level']} ({timeline_risk['confidence']}% confidence)
- Days to Target: {timeline_risk['days_remaining']}
- Completion: {timeline_risk['completion_rate']}%

Critical Path: {' → '.join(critical_path[:5])}{'...' if len(critical_path) > 5 else ''}

Top Blockers:
{chr(10).join(f"- {b['key']}: {b['summary']} (blocks {b['blocks_count']} issues)" for b in blockers[:3])}

{formatted_prompt}
"""

        return {
            "content": [
                {
                    "type": "text",
                    "text": summary,
                }
            ]
        }

    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error analyzing dependencies: {str(e)}",
                }
            ],
            "isError": True,
        }


@tool(
    "generate_gantt_chart",
    "Generate Mermaid Gantt chart for dependencies. Use Atlassian MCP jira_search to fetch issues first.",
    {
        "initiative_name": str,
        "issues_json": str,  # JSON string of issues from Atlassian MCP
    },
)
async def generate_gantt_chart(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a Mermaid Gantt chart showing timeline and dependencies.

    This tool expects issue data to be provided (fetched via Atlassian MCP jira_search).

    Args:
        initiative_name: Name of the initiative
        issues_json: JSON string of issues from Atlassian MCP

    Returns:
        Mermaid Gantt chart code
    """
    try:
        import json

        # Parse issues from JSON
        issues = json.loads(args["issues_json"])

        if not issues:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "No issues provided for chart generation",
                    }
                ],
                "isError": True,
            }

        # Group by team
        settings = get_settings()
        teams = {}
        for issue in issues:
            fields = issue.get("fields", {})
            team = fields.get(
                settings.atlassian.field_team_assignment, "Other"
            )
            if not team:
                team = "Other"

            if team not in teams:
                teams[team] = []

            key = issue.get("key", "")
            summary = fields.get("summary", "")[:30]
            status = fields.get("status", {}).get("name", "")

            # Determine Mermaid status
            if status in ["Done", "Closed", "Resolved"]:
                mermaid_status = "done"
            elif status in ["Blocked", "Impediment"]:
                mermaid_status = "crit"
            else:
                mermaid_status = "active"

            teams[team].append(
                {
                    "key": key,
                    "summary": summary,
                    "status": mermaid_status,
                }
            )

        # Generate Mermaid chart
        chart_lines = [
            "```mermaid",
            "gantt",
            f"    title {args['initiative_name']} - Cross-Team Dependencies",
            "    dateFormat YYYY-MM-DD",
            "",
        ]

        # Add sections for each team
        for team_idx, (team, team_issues) in enumerate(teams.items()):
            chart_lines.append(f"    section {team}")

            for issue_idx, issue in enumerate(team_issues[:5]):  # Limit to 5 per team
                task_id = f"t{team_idx}_{issue_idx}"
                chart_lines.append(
                    f"    {issue['summary']} :{issue['status']}, {task_id}, 2025-01-01, 14d"
                )

            chart_lines.append("")

        chart_lines.append("```")

        chart_code = "\n".join(chart_lines)

        # Save chart
        settings = get_settings()
        chart_dir = settings.output.chart_output_dir
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gantt_{args['initiative_name'].replace(' ', '_')}_{timestamp}.md"
        file_path = chart_dir / filename

        with open(file_path, "w") as f:
            f.write(chart_code)

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Gantt chart generated:\n\n{chart_code}\n\nSaved to: {file_path}",
                }
            ]
        }

    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error generating Gantt chart: {str(e)}",
                }
            ],
            "isError": True,
        }