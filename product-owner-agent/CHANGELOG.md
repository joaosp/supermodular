# Changelog

## [0.2.0] - 2025-09-30

### Added
- **Atlassian Remote MCP Server Integration** - Native JIRA and Confluence integration
  - Replaced custom JIRA REST API client with official Atlassian MCP Server
  - OAuth 2.1 authentication (no credential management required)
  - Direct access to JIRA issues, sprints, boards via MCP tools
  - Confluence page search, creation, and updates via MCP tools
  - Secure cloud-based bridge at `https://mcp.atlassian.com/v1/sse`

### Changed
- **Configuration** - Updated from `JiraConfig` to `AtlassianMCPConfig`
  - Removed: `JIRA_BASE_URL`, `JIRA_API_TOKEN`, `JIRA_USER_EMAIL`
  - Added: `ATLASSIAN_MCP_URL`, `ATLASSIAN_SITE_URL`
  - Custom field mappings retained for advanced usage

- **Agent Initialization** - Added Atlassian MCP server connection
  - Uses `TransportType.SSE` for server-sent events
  - Enabled Atlassian MCP tools in allowed_tools list
  - Updated system prompt to reference MCP tools

- **Custom Tools** - Refactored to leverage Atlassian MCP
  - `translate_epic_to_stories`: Now expects epic data from MCP `jira_get_issue`
  - `generate_sprint_report`: Now expects sprint data from MCP `jira_get_sprint` and `jira_search`
  - `analyze_dependencies`: Now expects issue data from MCP `jira_search`
  - `save_report_to_jira`: Provides instructions for MCP-based upload
  - `create_stories_from_spec`: Provides instructions for MCP `jira_create_issue`

- **Authentication Flow** - Browser-based OAuth instead of API tokens
  - First run opens browser for Atlassian login
  - User grants access to products (JIRA, Confluence, Compass)
  - Credentials managed securely by MCP server

### Deprecated
- **JiraClient** - Custom REST API client no longer used
  - File `agent/tools/jira_tools.py` retained for reference
  - All operations now via Atlassian MCP tools

### Documentation
- Updated README with OAuth setup instructions
- Updated .env.example with Atlassian MCP configuration
- Added MCP integration details to system prompts

### Benefits
- ✅ No credential management required
- ✅ Native Confluence support added
- ✅ Respects Atlassian user permissions
- ✅ Real-time data streaming via SSE
- ✅ Rate limits managed by Atlassian

### Breaking Changes
- Existing `.env` JIRA configuration is incompatible
- Users must update to Atlassian MCP configuration
- First run requires browser authentication
- No offline mode (requires internet connection)

---

## [0.1.1] - 2025-09-30

### Added
- **Thinking Animation** - Added animated spinner while agent is processing
  - Displays rotating spinner (⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏) with "thinking..." message
  - Automatically clears when agent starts responding
  - Provides visual feedback during API calls and tool execution
  - Smooth transition from animation to response text

### Fixed
- **Interactive Mode UI Cleanup** - Fixed issue where full message objects were displayed instead of clean text
  - Added `_extract_text_from_message()` helper method to parse Claude SDK message objects
  - Extracts only displayable text content from messages
  - Filters out internal tool use/result messages
  - Handles multiple message formats (strings, dicts, objects with `__dict__`)
  - Applied to all output methods: `interactive_session()`, `translate_epic()`, `generate_report()`, `analyze_risks()`, `one_shot_query()`

### Changed
- Message streaming now displays clean, formatted text instead of raw objects
- Result aggregation changed from `"\n".join()` to `"".join()` for smoother text flow
- Interactive mode now shows visual feedback during agent processing

### Technical Details

**Problem:**
```python
# Before - displayed raw objects
Agent: SystemMessage(subtype='init', data={'type': 'system', 'subtype': 'init', ...})
```

**Solution:**
```python
# After - displays clean text only
Agent: Hello! I'm your Product Owner Agent...
```

**Implementation:**
- Checks message subtype to filter internal messages (init, tool_use, tool_result)
- Extracts text from content blocks (handles both dict and object formats)
- Supports TextBlock arrays and direct text attributes
- Maintains streaming output for real-time feedback

### Testing
- Created `test_message_extraction.py` with 7 test cases
- All tests passing ✓
- Verified with multiple message formats

---

## [0.1.0] - 2025-09-30

### Added
- **Initial Release** - Complete Product Owner Agent implementation
- Business ↔ Technical Requirements Translation
- Auto-generated Progress Reports
- Risk & Dependency Alerts
- Full CLI with Rich UI
- JIRA integration with custom tools
- Interactive and command-line modes
- Comprehensive documentation

### Features
- 6 custom tools using Claude Agent SDK `@tool` decorator
- Pydantic-based configuration management
- Dependency graph analysis with critical path detection
- Sprint metrics calculation (velocity, completion rate, cycle time)
- Mermaid Gantt chart generation
- Professional CLI with colors, panels, and progress indicators

### Documentation
- Complete README.md with usage examples
- TEST_RESULTS.md with comprehensive test coverage
- Prompt templates for all three core capabilities
- .env.example for easy configuration