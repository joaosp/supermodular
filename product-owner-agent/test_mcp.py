#!/usr/bin/env python3
"""Test script to debug Atlassian MCP integration."""

import asyncio
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

from agent.product_owner import ProductOwnerAgent


async def test_jira_query():
    """Test fetching a JIRA issue."""
    print("=" * 60)
    print("Testing Atlassian MCP Integration")
    print("=" * 60)

    agent = ProductOwnerAgent()

    # Step 1: Get the cloud ID
    print("\n[Step 1] Getting Atlassian Cloud ID...")
    print("-" * 60)

    query1 = """Use the Atlassian MCP tool 'getAccessibleAtlassianResources' to get my Atlassian Cloud ID.
This tool doesn't require any parameters.
Please extract and show me the cloudId (UUID format) from the response."""

    try:
        result1 = await agent.one_shot_query(query1)
        print("\nCloud ID Query Result:")
        print(result1)
        print("-" * 60)
    except Exception as e:
        print(f"\n❌ Failed to get Cloud ID: {e}")
        import traceback
        traceback.print_exc()
        print("-" * 60)

    # Step 2: Fetch SDDEMO-3 with the correct cloud ID
    print("\n[Step 2] Fetching JIRA issue SDDEMO-3...")
    print("-" * 60)

    query2 = """Fetch JIRA issue SDDEMO-3.

Steps:
1. First use getAccessibleAtlassianResources to get the cloudId (it will be a UUID)
2. Then use getJiraIssue with that cloudId and issueIdOrKey='SDDEMO-3'
3. Show me the issue's summary, description, status, assignee, and any other important details"""

    print(f"\nQuery: Fetch SDDEMO-3 using correct cloudId\n")
    print("Sending query to agent...")
    print("-" * 60)

    try:
        result2 = await agent.one_shot_query(query2)
        print("\n" + "=" * 60)
        print("RESULT:")
        print("=" * 60)
        print(result2)
        print("=" * 60)
        return True
    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR:")
        print("=" * 60)
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = asyncio.run(test_jira_query())
    sys.exit(0 if success else 1)
