# Migration Guide: Atlassian Remote MCP Server Integration

This guide will help you migrate from the previous version (0.1.x) with custom JIRA API integration to version 0.2.0 with Atlassian Remote MCP Server.

## What Changed?

### Before (v0.1.x)
- Custom JIRA REST API client
- Required API tokens and credentials in `.env`
- Manual credential management
- JIRA-only support

### After (v0.2.0)
- Official Atlassian Remote MCP Server
- OAuth 2.1 authentication (browser-based)
- Automatic credential management
- JIRA + Confluence support

## Migration Steps

### 1. Update Dependencies

```bash
# Ensure you have the latest requirements
pip install -r requirements.txt --upgrade
```

### 2. Update Environment Configuration

**Old `.env` format (DEPRECATED):**
```bash
JIRA_BASE_URL=https://yourcompany.atlassian.net
JIRA_API_TOKEN=your_api_token
JIRA_USER_EMAIL=your.email@company.com
```

**New `.env` format:**
```bash
ATLASSIAN_MCP_URL=https://mcp.atlassian.com/v1/sse
ATLASSIAN_SITE_URL=https://yourcompany.atlassian.net
```

**What to do:**
1. Open your `.env` file
2. Remove `JIRA_BASE_URL`, `JIRA_API_TOKEN`, `JIRA_USER_EMAIL`
3. Add `ATLASSIAN_MCP_URL` and `ATLASSIAN_SITE_URL`
4. Keep your `ANTHROPIC_API_KEY` and other settings

### 3. First Run Authentication

The first time you run the agent after migration:

```bash
python main.py interactive
```

**What will happen:**
1. A browser window will open automatically
2. You'll be redirected to Atlassian login
3. Log in with your Atlassian account
4. Grant access to JIRA, Confluence, and Compass
5. The browser will close, and the agent will connect

**Important:**
- Disable pop-up blockers for this process
- Make sure you have access to the Atlassian products you need
- This authentication is one-time only

### 4. Verify Migration

Check that everything works:

```bash
python main.py check
```

Expected output should show:
- ✓ Atlassian MCP connection established
- ✓ JIRA access verified
- ✓ Confluence access verified (if applicable)
- ✓ Claude API connected

## Tool Usage Changes

The agent now uses Atlassian MCP tools internally. Here's how the workflow changes:

### Epic Translation

**Before:**
```python
# Agent internally called JiraClient.get_issue()
```

**After:**
```python
# Agent uses: mcp__atlassian__jira_get_issue
# Then passes data to translate_epic_to_stories
```

**User experience:** No change! The commands remain the same:
```bash
python main.py translate EPIC-123 --architecture microservices
```

### Sprint Reporting

**Before:**
```python
# Agent internally called JiraClient.get_sprint_data()
```

**After:**
```python
# Agent uses: mcp__atlassian__jira_get_sprint
#            mcp__atlassian__jira_search
# Then passes data to generate_sprint_report
```

**User experience:** No change! The commands remain the same:
```bash
python main.py report 42 --sprint 123 --team "Alpha Team"
```

### Dependency Analysis

**Before:**
```python
# Agent internally called JiraClient.search_issues()
```

**After:**
```python
# Agent uses: mcp__atlassian__jira_search
# Then passes data to analyze_dependencies
```

**User experience:** No change! The commands remain the same:
```bash
python main.py analyze "project = PROJ" "Initiative" "2025-12-31"
```

## New Capabilities

### Confluence Integration

You can now ask the agent to:
- Search Confluence pages
- Create documentation pages
- Update existing pages
- Link JIRA issues to Confluence

**Example queries in interactive mode:**
```
You: Search Confluence for "Q3 Planning"
You: Create a Confluence page with the sprint report
You: Link JIRA issue PROJ-123 to the architecture page
```

### Natural Language Queries

The agent can now:
- "Summarize the Confluence page 'Product Roadmap'"
- "Create a JIRA issue for the bug described in the API documentation"
- "Find all tasks assigned to me"

## Troubleshooting

### Browser Authentication Fails

**Problem:** Browser doesn't open or authentication hangs

**Solutions:**
1. Disable pop-up blockers
2. Make sure you're logged in to Atlassian in your default browser
3. Try a different browser (set as default temporarily)
4. Check internet connection

### "No Access" Errors

**Problem:** Agent says it can't access JIRA/Confluence

**Solutions:**
1. Verify you granted access during OAuth flow
2. Check that your Atlassian account has permissions
3. Try disconnecting and re-authenticating
4. Verify `ATLASSIAN_SITE_URL` is correct

### Rate Limiting

**Problem:** "Rate limit exceeded" messages

**Solutions:**
- Rate limits depend on your Atlassian plan
- Standard plans have lower limits than Premium/Enterprise
- Spread out requests or upgrade your plan
- Contact Atlassian support for limit increases

## Rollback (If Needed)

If you need to rollback to v0.1.x:

```bash
# 1. Checkout previous version
git checkout v0.1.1

# 2. Restore old .env format
# Add back JIRA_BASE_URL, JIRA_API_TOKEN, JIRA_USER_EMAIL

# 3. Reinstall dependencies
pip install -r requirements.txt

# 4. Run the agent
python main.py interactive
```

**Note:** We recommend staying on v0.2.0 for better security and features.

## Benefits of Migration

✅ **Security**
- No API tokens to manage
- OAuth 2.1 authentication
- Credentials never stored locally

✅ **Features**
- Native Confluence support
- Respects Atlassian permissions
- Real-time data streaming

✅ **Reliability**
- Official Atlassian integration
- Better rate limit handling
- Automatic updates from Atlassian

## Support

If you encounter issues during migration:

1. Check this guide's troubleshooting section
2. Review CHANGELOG.md for detailed changes
3. Check Atlassian MCP Server docs: https://support.atlassian.com/atlassian-rovo-mcp-server/
4. Open an issue on GitHub

## Next Steps

After successful migration:

1. Try the interactive mode: `python main.py interactive`
2. Test epic translation with a real epic
3. Generate a sprint report
4. Explore Confluence integration
5. Update your team's documentation with new capabilities

Happy migrating! 🚀