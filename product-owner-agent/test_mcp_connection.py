#!/usr/bin/env python3
"""Test MCP server connection and tool listing."""

import asyncio
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

from claude_agent_sdk import ClaudeSDKClient
from agent.product_owner import ProductOwnerAgent


async def test_mcp_connection():
    """Test if MCP servers are connecting and list their tools."""
    print("=" * 60)
    print("Testing MCP Server Connection")
    print("=" * 60)

    agent = ProductOwnerAgent()
    options = agent._get_agent_options()

    print("\nConfigured MCP servers:")
    for server_name in options.mcp_servers.keys():
        print(f"  - {server_name}")

    print("\nAttempting to connect...")
    print("-" * 60)

    try:
        async with ClaudeSDKClient(options=options) as client:
            print("✅ Client connected successfully!")

            # Try to send a simple query that lists available tools
            query = "List all the Atlassian MCP tools available to you. Don't call any tools, just list their names."

            print(f"\nQuery: {query}\n")
            await client.query(query)

            result = []
            async for message in client.receive_response():
                text = agent._extract_text_from_message(message)
                if text:
                    result.append(text)
                    print(text, end="", flush=True)

            print("\n" + "=" * 60)
            return True

    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_mcp_connection())
    sys.exit(0 if success else 1)
