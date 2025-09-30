# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Product Owner Agent is an AI-powered automation tool built with Claude Agent SDK and Atlassian Remote MCP Server. It automates Product Owner responsibilities for Outsystems development teams through three core capabilities:

1. **Business ↔ Technical Requirements Translation** - Converts JIRA epics into detailed technical specifications
2. **Auto-generated Progress Reports** - Analyzes sprint data and generates comprehensive reports
3. **Risk & Dependency Alerts** - Identifies cross-team dependencies and calculates timeline risks

**Key Architectural Decision**: The agent uses Atlassian's official Remote MCP Server (v0.2.0+) instead of direct REST API calls, providing OAuth 2.1 authentication and native Confluence support.

## Development Setup

```bash
# Install dependencies (use virtual environment)
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Atlassian site URL and Anthropic API key

# Verify installation
python main.py check

# Run tests (when available)
pytest
```

## Running the Agent

```bash
# CLI commands
python main.py check                    # System diagnostics
python main.py config                   # View configuration
python main.py interactive              # Interactive session
python main.py translate EPIC-123       # Translate epic
python main.py report 42 --sprint 123   # Generate report
python main.py analyze "jql query"      # Dependency analysis

# Always use virtual environment
source .venv/bin/activate && python main.py [command]
```

## Architecture

### Two-Tier Tool System

The agent implements a **hybrid tool architecture** combining Claude Agent SDK custom tools with Atlassian MCP tools:

```
ProductOwnerAgent
├── Custom Tools (agent/tools/) - Business logic layer
│   ├── translate_epic_to_stories    - Formats translation prompts
│   ├── create_stories_from_spec     - Guides story creation
│   ├── generate_sprint_report       - Calculates metrics, formats reports
│   ├── save_report_to_jira          - Saves reports locally
│   ├── analyze_dependencies         - Builds dependency graphs
│   └── generate_gantt_chart         - Creates Mermaid charts
│
└── Atlassian MCP Tools - Data access layer
    ├── jira_search, jira_get_issue, jira_create_issue
    ├── jira_update_issue, jira_add_comment
    ├── jira_get_sprint, jira_get_board
    └── confluence_search, confluence_get_page, confluence_create_page
```

**Critical Pattern**: Custom tools receive data fetched by Atlassian MCP tools, not raw API calls. For example:
- `translate_epic_to_stories` expects `epic_summary` and `epic_description` parameters (from `jira_get_issue`)
- `generate_sprint_report` expects `issues_json` parameter (from `jira_search`)
- `analyze_dependencies` expects `issues_json` parameter (from `jira_search`)

### MCP Server Configuration

Located in `agent/product_owner.py` `_get_agent_options()`:

```python
mcp_servers={
    "po_tools": self.tools_server,           # Custom tools (SDK MCP server)
    "atlassian": {                           # Atlassian MCP server
        "type": "sse",                       # Server-sent events transport
        "url": "https://mcp.atlassian.com/v1/sse"
    }
}
```

The Atlassian MCP server requires browser OAuth authentication on first run. Tools are prefixed with `mcp__atlassian__*` in the allowed_tools list.

### Configuration System

Pydantic-based configuration in `agent/config.py` with nested settings classes:

- `AtlassianMCPConfig` - MCP URL, site URL, custom field mappings
- `OutsystemsConfig` - Docs URL, version, repo path
- `AgentConfig` - Scheduling, thresholds, scan depth
- `ClaudeConfig` - API key
- `NotificationConfig` - Slack settings (optional)
- `OutputConfig` - Report/chart output directories

**Important**: After v0.2.0, `JiraConfig` was replaced with `AtlassianMCPConfig`. Any code referencing `settings.jira` is deprecated.

### Prompt Templates

Located in `prompts/` directory:
- `translation.txt` - Epic to stories translation (2,350 chars)
- `reporting.txt` - Sprint report generation (3,076 chars)
- `risk_analysis.txt` - Dependency and risk analysis (4,407 chars)

Loaded via helper functions like `load_translation_prompt()` and use `.format()` for variable substitution.

### Dependency Analysis Algorithm

`agent/tools/dependency.py` implements a directed graph approach:

1. **Graph Building** - `build_dependency_graph()` creates nodes from issues, edges from issuelinks
2. **Critical Path** - `find_critical_path()` uses topological sort + longest path calculation
3. **Blockers** - `identify_blockers()` finds incomplete issues blocking others
4. **Timeline Risk** - `calculate_timeline_risk()` compares critical path to target date

Graph structure:
```python
{
    "nodes": {issue_key: {summary, status, assignee, team, due_date, story_points}},
    "edges": [{from, to, type, link_type}]
}
```

## Code Modification Guidelines

### When Adding New Custom Tools

1. Define tool with `@tool` decorator in appropriate file under `agent/tools/`
2. Tool descriptions should mention which Atlassian MCP tools to use first
3. Accept JSON string parameters for complex data (e.g., `issues_json`)
4. Return dict with `content` array containing text blocks
5. Register tool in `ProductOwnerAgent.__init__()` tools list
6. Add to `allowed_tools` in `_get_agent_options()`
7. Update system prompt to document the new tool

### When Modifying Configuration

1. Update the appropriate config class in `agent/config.py`
2. Add new environment variable to `.env.example` with comments
3. Update `main.py` config command if display needed
4. Document in MIGRATION_GUIDE.md if breaking change

### When Updating MCP Integration

- **DO NOT** import or use `JiraClient` from `agent/tools/jira_tools.py` (deprecated)
- **DO** expect data from Atlassian MCP tools as function parameters
- **DO** update tool descriptions to guide MCP usage
- The agent's system prompt (in `_get_agent_options()`) documents all available MCP tools

### Message Extraction Pattern

The agent implements clean text extraction from Claude SDK message objects via `_extract_text_from_message()` in `agent/product_owner.py`:

```python
# Filters out internal messages (init, tool_use, tool_result)
# Extracts text from content blocks
# Handles both dict and object message formats
# Used in all output methods to prevent raw object display
```

This prevents displaying raw `SystemMessage` objects in interactive mode.

## Testing

Run comprehensive system check:
```bash
python main.py check
```

Expected output:
- ✓ Python version, package installations
- ✓ Configuration loaded
- ✓ Agent initialized successfully
- ✓ MCP servers configured: po_tools, atlassian
- ✓ Atlassian MCP: sse at https://mcp.atlassian.com/v1/sse

Test imports programmatically:
```bash
python -c "from agent import ProductOwnerAgent; agent = ProductOwnerAgent(); print('Success')"
```

## File Organization

```
agent/
├── config.py           - Pydantic settings (DO modify for config changes)
├── product_owner.py    - Main agent class (CORE - modify carefully)
└── tools/
    ├── __init__.py     - Exports custom tools (update when adding tools)
    ├── jira_tools.py   - DEPRECATED - DO NOT USE (kept for reference)
    ├── translation.py  - Epic translation tools
    ├── reporting.py    - Sprint reporting tools
    └── dependency.py   - Dependency analysis tools

prompts/                - Prompt templates (modify for prompt changes)
main.py                - CLI entry point (modify for new commands)
```

## Important Constraints

1. **Async Required** - All agent methods and custom tools are async (`async def`)
2. **OAuth Flow** - First run requires browser authentication (can't be bypassed)
3. **No Offline Mode** - Atlassian MCP requires internet connection
4. **Tool Prefixes** - Custom tools: `mcp__po_tools__*`, Atlassian tools: `mcp__atlassian__*`
5. **Python 3.8+** - Minimum version requirement

## Recent Changes (v0.2.0)

- Migrated from custom JIRA REST API client to Atlassian Remote MCP Server
- Replaced credential-based auth with OAuth 2.1
- Added native Confluence support
- Refactored all custom tools to expect MCP-fetched data as parameters
- Deprecated `JiraClient` class (file retained for reference only)
- Updated configuration from `JiraConfig` to `AtlassianMCPConfig`

See CHANGELOG.md and MIGRATION_GUIDE.md for complete migration details.