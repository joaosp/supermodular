#!/usr/bin/env python3
"""Test Atlassian OAuth authentication."""

import asyncio
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

from agent.product_owner import ProductOwnerAgent


async def test_auth():
    """Test if Atlassian authentication is working."""
    print("=" * 60)
    print("Testing Atlassian OAuth Authentication")
    print("=" * 60)

    agent = ProductOwnerAgent()

    # Try the simplest Atlassian MCP tool - get user info
    query = """Use the 'mcp__atlassian__atlassianUserInfo' tool to get my Atlassian user information.

This tool requires no parameters and should return information about the currently authenticated user."""

    print(f"\nQuery: {query}\n")
    print("Calling atlassianUserInfo...")
    print("-" * 60)

    try:
        result = await agent.one_shot_query(query)
        print("\n" + "=" * 60)
        print("RESULT:")
        print("=" * 60)
        print(result)
        print("=" * 60)

        if "permission" in result.lower() or "error" in result.lower():
            print("\n❌ Authentication appears to be failing")
            return False
        else:
            print("\n✅ Authentication successful!")
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
    success = asyncio.run(test_auth())
    sys.exit(0 if success else 1)
