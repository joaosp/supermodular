#!/usr/bin/env python3
"""
Test script for Product Owner Agent.
Tests core functionality with Atlassian MCP Server integration.
"""

import sys
from pathlib import Path

# Test imports
print("Testing imports...")
try:
    from agent import ProductOwnerAgent, get_settings
    from agent.config import Settings
    from agent.tools import translation, reporting, dependency
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test configuration
print("\nTesting configuration...")
try:
    settings = get_settings()
    print(f"✓ Configuration loaded")
    print(f"  - Atlassian MCP URL: {settings.atlassian.mcp_url}")
    print(f"  - Atlassian Site URL: {settings.atlassian.site_url}")
    print(f"  - Outsystems Version: {settings.outsystems.version}")
    print(f"  - Reports dir: {settings.output.report_output_dir}")
except Exception as e:
    print(f"✗ Configuration error: {e}")
    sys.exit(1)

# Test output directories creation
print("\nTesting output directories...")
try:
    assert settings.output.report_output_dir.exists()
    assert settings.output.chart_output_dir.exists()
    print("✓ Output directories created")
except AssertionError:
    print("✗ Output directories not created")
    sys.exit(1)

# Test prompt loading
print("\nTesting prompt templates...")
try:
    from agent.tools.translation import load_translation_prompt
    from agent.tools.reporting import load_reporting_prompt
    from agent.tools.dependency import load_risk_analysis_prompt

    trans_prompt = load_translation_prompt()
    report_prompt = load_reporting_prompt()
    risk_prompt = load_risk_analysis_prompt()

    assert len(trans_prompt) > 100
    assert len(report_prompt) > 100
    assert len(risk_prompt) > 100

    print("✓ All prompt templates loaded successfully")
    print(f"  - Translation prompt: {len(trans_prompt)} chars")
    print(f"  - Reporting prompt: {len(report_prompt)} chars")
    print(f"  - Risk analysis prompt: {len(risk_prompt)} chars")
except Exception as e:
    print(f"✗ Prompt loading error: {e}")
    sys.exit(1)

# Test agent initialization
print("\nTesting agent initialization...")
try:
    agent = ProductOwnerAgent()
    print("✓ Agent initialized successfully")
    print(f"  - Tools server created: {agent.tools_server is not None}")

    # Check MCP configuration
    options = agent._get_agent_options()
    print(f"  - MCP servers configured: {', '.join(options.mcp_servers.keys())}")

    atlassian_config = options.mcp_servers.get("atlassian", {})
    print(f"  - Atlassian MCP type: {atlassian_config.get('type', 'N/A')}")
    print(f"  - Atlassian MCP URL: {atlassian_config.get('url', 'N/A')}")

    # Count Atlassian MCP tools
    atlassian_tools = [t for t in options.allowed_tools if 'atlassian' in t]
    print(f"  - Atlassian MCP tools available: {len(atlassian_tools)}")
except Exception as e:
    print(f"✗ Agent initialization error: {e}")
    sys.exit(1)

# Test dependency graph functions
print("\nTesting dependency analysis functions...")
try:
    from agent.tools.dependency import build_dependency_graph, find_critical_path

    # Mock data
    test_issues = [
        {
            "key": "TEST-1",
            "fields": {
                "summary": "Test Issue 1",
                "status": {"name": "Done"},
                "assignee": {"displayName": "Test User"},
                "customfield_10016": 5
            }
        }
    ]

    graph = build_dependency_graph(test_issues)
    assert "nodes" in graph
    assert "edges" in graph
    assert "TEST-1" in graph["nodes"]

    print("✓ Dependency analysis functions working")
    print(f"  - Nodes: {len(graph['nodes'])}")
    print(f"  - Edges: {len(graph['edges'])}")
except Exception as e:
    print(f"✗ Dependency analysis error: {e}")
    sys.exit(1)

# Test metrics calculation
print("\nTesting sprint metrics calculation...")
try:
    from agent.tools.reporting import calculate_sprint_metrics

    test_issues = [
        {
            "key": "TEST-1",
            "fields": {
                "summary": "Completed Story",
                "status": {"name": "Done"},
                "customfield_10016": 5
            }
        },
        {
            "key": "TEST-2",
            "fields": {
                "summary": "In Progress Story",
                "status": {"name": "In Progress"},
                "customfield_10016": 3
            }
        }
    ]

    metrics = calculate_sprint_metrics(test_issues)
    assert metrics["total_issues"] == 2
    assert metrics["velocity"] == 5
    assert len(metrics["completed"]) == 1
    assert len(metrics["in_progress"]) == 1

    print("✓ Metrics calculation working")
    print(f"  - Total issues: {metrics['total_issues']}")
    print(f"  - Velocity: {metrics['velocity']}")
    print(f"  - Completion rate: {metrics['completion_rate']}%")
except Exception as e:
    print(f"✗ Metrics calculation error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✓ All tests passed successfully!")
print("="*60)
print("\nThe Product Owner Agent is ready to use.")
print("\n⚠️  Important Notes:")
print("  - First run requires browser authentication for Atlassian MCP")
print("  - JIRA and Confluence access via OAuth 2.1")
print("  - No API tokens needed - credentials managed by Atlassian MCP Server")