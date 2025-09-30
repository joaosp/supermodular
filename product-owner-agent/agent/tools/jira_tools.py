"""
DEPRECATED: JIRA REST API integration tools for Product Owner Agent.

⚠️ WARNING: This module is DEPRECATED as of v0.2.0 ⚠️

This file is retained for reference only. All JIRA operations should now
use the Atlassian Remote MCP Server integration instead of direct REST API calls.

DO NOT USE THIS MODULE IN NEW CODE.

Migration Information:
- Instead of JiraClient.search_issues() → Use Atlassian MCP tool: mcp__atlassian__jira_search
- Instead of JiraClient.get_issue() → Use Atlassian MCP tool: mcp__atlassian__jira_get_issue
- Instead of JiraClient.create_issue() → Use Atlassian MCP tool: mcp__atlassian__jira_create_issue
- Instead of JiraClient.update_issue() → Use Atlassian MCP tool: mcp__atlassian__jira_update_issue
- Instead of JiraClient.add_comment() → Use Atlassian MCP tool: mcp__atlassian__jira_add_comment
- Instead of JiraClient.get_sprint_data() → Use Atlassian MCP tool: mcp__atlassian__jira_get_sprint
- Instead of JiraClient.upload_attachment() → Save locally and use Confluence/JIRA MCP tools

See MIGRATION_GUIDE.md for complete migration instructions.
See CHANGELOG.md [0.2.0] for details on the MCP integration.

This file will be removed in v0.3.0.
"""

import base64
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from requests.auth import HTTPBasicAuth

from ..config import get_settings


class JiraClient:
    """Client for JIRA API operations."""

    def __init__(self):
        """Initialize JIRA client with configuration."""
        settings = get_settings()
        self.base_url = settings.jira.base_url.rstrip("/")
        self.auth = HTTPBasicAuth(
            settings.jira.user_email, settings.jira.api_token
        )
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.custom_fields = {
            "technical_spec": settings.jira.field_technical_spec,
            "dependency_links": settings.jira.field_dependency_links,
            "risk_score": settings.jira.field_risk_score,
            "team_assignment": settings.jira.field_team_assignment,
            "milestone_target": settings.jira.field_milestone_target,
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to JIRA API with error handling."""
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                auth=self.auth,
                json=data,
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.HTTPError as e:
            raise Exception(f"JIRA API error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"JIRA connection error: {str(e)}")

    def search_issues(
        self, jql: str, fields: Optional[List[str]] = None, max_results: int = 100
    ) -> Dict[str, Any]:
        """
        Search JIRA issues using JQL.

        Args:
            jql: JIRA Query Language string
            fields: List of fields to return (None for all)
            max_results: Maximum number of results

        Returns:
            Search results including issues list
        """
        params = {
            "jql": jql,
            "maxResults": max_results,
        }
        if fields:
            params["fields"] = ",".join(fields)

        return self._request("GET", "/rest/api/2/search", params=params)

    def get_issue(self, issue_key: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get a single JIRA issue by key.

        Args:
            issue_key: JIRA issue key (e.g., "PROJ-123")
            fields: List of fields to return

        Returns:
            Issue data
        """
        params = {}
        if fields:
            params["fields"] = ",".join(fields)

        return self._request("GET", f"/rest/api/2/issue/{issue_key}", params=params)

    def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Story",
        **custom_fields,
    ) -> Dict[str, Any]:
        """
        Create a new JIRA issue.

        Args:
            project_key: Project key (e.g., "PROJ")
            summary: Issue summary/title
            description: Issue description
            issue_type: Type of issue (Story, Epic, Task, etc.)
            **custom_fields: Custom field values

        Returns:
            Created issue data including key
        """
        data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type},
            }
        }

        # Add custom fields
        for field_name, field_value in custom_fields.items():
            if field_name in self.custom_fields:
                data["fields"][self.custom_fields[field_name]] = field_value

        return self._request("POST", "/rest/api/2/issue", data=data)

    def update_issue(
        self, issue_key: str, fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a JIRA issue.

        Args:
            issue_key: Issue key to update
            fields: Dictionary of fields to update

        Returns:
            Empty dict on success
        """
        data = {"fields": fields}
        return self._request("PUT", f"/rest/api/2/issue/{issue_key}", data=data)

    def add_comment(self, issue_key: str, comment: str) -> Dict[str, Any]:
        """
        Add a comment to a JIRA issue.

        Args:
            issue_key: Issue key
            comment: Comment text

        Returns:
            Created comment data
        """
        data = {"body": comment}
        return self._request(
            "POST", f"/rest/api/2/issue/{issue_key}/comment", data=data
        )

    def upload_attachment(
        self, issue_key: str, file_path: Path
    ) -> Dict[str, Any]:
        """
        Upload an attachment to a JIRA issue.

        Args:
            issue_key: Issue key
            file_path: Path to file to upload

        Returns:
            Attachment data
        """
        url = f"{self.base_url}/rest/api/2/issue/{issue_key}/attachments"
        headers = {"X-Atlassian-Token": "no-check"}

        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f)}
            response = requests.post(
                url, headers=headers, auth=self.auth, files=files, timeout=60
            )
            response.raise_for_status()
            return response.json()

    def get_sprint_data(self, board_id: int, sprint_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get sprint data from JIRA Agile API.

        Args:
            board_id: Board ID
            sprint_id: Specific sprint ID (None for active sprint)

        Returns:
            Sprint data including issues
        """
        if sprint_id:
            endpoint = f"/rest/agile/1.0/sprint/{sprint_id}"
        else:
            endpoint = f"/rest/agile/1.0/board/{board_id}/sprint"
            params = {"state": "active"}
            sprints = self._request("GET", endpoint, params=params)
            if not sprints.get("values"):
                raise Exception("No active sprint found")
            sprint_id = sprints["values"][0]["id"]
            endpoint = f"/rest/agile/1.0/sprint/{sprint_id}"

        sprint_info = self._request("GET", endpoint)

        # Get issues in sprint
        issues_endpoint = f"/rest/agile/1.0/sprint/{sprint_id}/issue"
        issues = self._request("GET", issues_endpoint)

        return {"sprint": sprint_info, "issues": issues}

    def get_issue_links(self, issue_key: str) -> List[Dict[str, Any]]:
        """
        Get all issue links (dependencies) for an issue.

        Args:
            issue_key: Issue key

        Returns:
            List of issue links
        """
        issue = self.get_issue(issue_key, fields=["issuelinks"])
        return issue.get("fields", {}).get("issuelinks", [])

    def create_issue_link(
        self, inward_issue: str, outward_issue: str, link_type: str = "Blocks"
    ) -> Dict[str, Any]:
        """
        Create a link between two issues.

        Args:
            inward_issue: Issue that is blocked/depends on
            outward_issue: Issue that blocks/is depended on
            link_type: Type of link (Blocks, Relates, etc.)

        Returns:
            Empty dict on success
        """
        data = {
            "type": {"name": link_type},
            "inwardIssue": {"key": inward_issue},
            "outwardIssue": {"key": outward_issue},
        }
        return self._request("POST", "/rest/api/2/issueLink", data=data)


# Tool functions that can be exposed to the agent

def search_issues(jql: str, max_results: int = 100) -> Dict[str, Any]:
    """Search JIRA issues using JQL query."""
    client = JiraClient()
    return client.search_issues(jql, max_results=max_results)


def create_issue(
    project_key: str,
    summary: str,
    description: str,
    issue_type: str = "Story",
    **kwargs,
) -> Dict[str, Any]:
    """Create a new JIRA issue."""
    client = JiraClient()
    return client.create_issue(project_key, summary, description, issue_type, **kwargs)


def update_issue(issue_key: str, fields: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing JIRA issue."""
    client = JiraClient()
    return client.update_issue(issue_key, fields)


def add_comment(issue_key: str, comment: str) -> Dict[str, Any]:
    """Add a comment to a JIRA issue."""
    client = JiraClient()
    return client.add_comment(issue_key, comment)


def upload_attachment(issue_key: str, file_path: str) -> Dict[str, Any]:
    """Upload an attachment to a JIRA issue."""
    client = JiraClient()
    return client.upload_attachment(issue_key, Path(file_path))


def get_sprint_data(board_id: int, sprint_id: Optional[int] = None) -> Dict[str, Any]:
    """Get sprint data including all issues."""
    client = JiraClient()
    return client.get_sprint_data(board_id, sprint_id)