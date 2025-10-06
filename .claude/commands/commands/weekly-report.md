# Weekly Progress Report Generator

Generate comprehensive weekly progress reports and create Linear tasks automatically.

## Usage

```
/weekly-report [next-steps-description]
```

**Examples:**
```
# For agent development work:
/weekly-report "Complete Linear MCP integration and implement automated sprint reporting"

# For template/infrastructure work:
/weekly-report "Begin development of Data Engineer Agent with database optimization tools"
```

## Report Meta-Structure

**Target Audience**: Product owners, stakeholders, executives
**Format**: Executive summary (150-200 words total)
**Focus**: Business value and impact, not technical implementation

The weekly report follows this business-oriented structure:

### 1. Executive Summary 📋
- 2-3 sentence overview of the week's primary achievement
- Focus on capabilities delivered and business value
- Avoid technical jargon; use plain language

### 2. This Week's Impact 🎯
- 3-5 bullet points of concrete outcomes
- Emphasize user-facing capabilities, not code changes
- Use business language: "Enabled X", "Reduced Y by Z%", "Automated W"
- Quantify impact: time savings, efficiency gains, features unlocked

### 3. Progress Metrics 📊
- 2-4 high-level quantified outcomes
- Examples: "3 new automation capabilities", "60% faster development cycle"
- Avoid technical metrics (lines of code, file counts)
- Focus on deliverables that stakeholders understand

### 4. Next Week's Focus 🔜
- 1-3 forward-looking priorities (from command argument)
- Brief, outcome-oriented statements
- What value will be delivered next

**Note**: Technical details (commits, file changes, architecture) remain in git history and are not included in the executive summary.

## Git Analysis Commands

Use these git commands to extract weekly progress data:

### Commit Summary
```bash
# Get all commits from the last 7 days with stats
git log --since="1 week ago" --pretty=format:"%h - %s (%ar)" --stat

# Get just the commit messages for quick scanning
git log --since="1 week ago" --oneline
```

### Feature Analysis
```bash
# Find feature additions
git log --since="1 week ago" --pretty=format:"- %s" --grep="feat:"

# Find bug fixes
git log --since="1 week ago" --pretty=format:"- %s" --grep="fix:"

# Find documentation updates
git log --since="1 week ago" --pretty=format:"- %s" --grep="docs:"
```

### File Changes
```bash
# Get file change statistics
git diff --stat HEAD~$(git rev-list --count HEAD --since="1 week ago")

# List all files modified this week
git diff --name-only HEAD~$(git rev-list --count HEAD --since="1 week ago")

# Count lines added/removed
git log --since="1 week ago" --numstat --pretty=format:"" | awk '{added+=$1; removed+=$2} END {print "Lines added:", added, "Lines removed:", removed}'
```

### File Type Analysis
```bash
# Python files created/modified (agent code, tools, tests)
git diff --name-only HEAD~$(git rev-list --count HEAD --since="1 week ago") | grep -E "\.py$" | wc -l

# Documentation files (README, CHANGELOG, guides)
git diff --name-only HEAD~$(git rev-list --count HEAD --since="1 week ago") | grep -E "\.md$" | wc -l

# Configuration files (MCP, environment, requirements)
git diff --name-only HEAD~$(git rev-list --count HEAD --since="1 week ago") | grep -E "\.(json|yml|yaml|txt|env)$" | wc -l
```

## Linear MCP Commands

### Get Current Week Number
```bash
# Calculate week number from current date
echo "Week $(date +%V)"
```

### Check Previous Week's Task
```bash
# List recent issues to find last week's task
mcp__linear-server__list_issues --limit 10 --assignee "me" --orderBy "updatedAt"
```

### Create This Week's Task
```javascript
// Use this pattern to create the weekly task
mcp__linear-server__create_issue {
  "title": "Week [NUMBER] - [PRIMARY_ACHIEVEMENT]",
  "description": "[GENERATED_REPORT_MARKDOWN]",
  "team": "Supermodular",
  "project": "[AGENT_NAME or Infrastructure]",  // e.g., "Product Owner Agent" or "Claude Code Templates"
  "assignee": "me"
}
```

## Implementation Steps

When running this command:

1. **Calculate Week Number**: `date +%V`

2. **Gather Git Data**:
   - Run commit analysis commands above
   - Count files created/modified by type
   - Calculate lines added/removed
   - Identify major features from commit messages

3. **Transform Technical Data to Business Language**:
   - **Executive Summary**:
     - Identify primary achievement from commit messages
     - Express in business terms (capabilities, outcomes, value)
     - Keep to 2-3 sentences maximum

   - **This Week's Impact**:
     - Convert technical changes to user-facing capabilities
     - Use action verbs: "Enabled", "Automated", "Reduced", "Improved"
     - Quantify business impact (time savings, efficiency, features)
     - Limit to 3-5 most impactful items

   - **Progress Metrics**:
     - Transform technical stats into business outcomes
     - Examples: "15 templates" NOT "8,400 lines of code"
     - Focus on deliverable count and efficiency gains
     - Limit to 2-4 key metrics

   - **Next Week's Focus**:
     - Use command argument
     - Express as outcome-oriented priority
     - 1-3 items maximum

4. **Create Linear Task**:
   - Title: "Week {week_number} - {primary_achievement_in_business_terms}"
   - Description: Business-focused executive summary (150-200 words)
   - Assign to current user
   - Set team to "Supermodular"
   - Set project based on work scope

5. **Output**: Show Linear task URL and concise summary

**Writing Guidelines**:
- Avoid: "Implemented", "Refactored", "Added code for", "Created module"
- Prefer: "Enabled", "Automated", "Reduced time by", "Delivered capability to"
- Avoid: Lines of code, file counts, technical architecture details
- Prefer: Features delivered, time saved, capabilities unlocked, efficiency gains

## Example Output Formats

### Example A: Agent Development Week

```markdown
## Executive Summary 📋
Integrated the Product Owner Agent with JIRA and Confluence, enabling automated project tracking and documentation. Teams can now automate sprint reporting and requirement translation without manual data entry.

## This Week's Impact 🎯
- **Automated JIRA Access**: Enabled direct integration with JIRA issues, sprints, and boards
- **Confluence Integration**: Added capability to search and create documentation automatically
- **Simplified Authentication**: Removed manual credential management, reducing setup time by 80%
- **Enhanced Capabilities**: Agent can now access both project tracking and documentation systems

## Progress Metrics 📊
- **Integration Scope**: JIRA + Confluence fully connected
- **Setup Time**: Reduced from 30 minutes to 5 minutes
- **Manual Work Eliminated**: Sprint reporting now fully automated

## Next Week's Focus 🔜
Complete Linear integration and implement automated sprint reporting capabilities
```

### Example B: Templates & Infrastructure Week

```markdown
## Executive Summary 📋
Developed a comprehensive library of 15 reusable AI agent templates covering backend development, data engineering, security, and project management. These templates accelerate future agent development by 60% and ensure consistent quality standards.

## This Week's Impact 🎯
- **Accelerated Development**: Created 15 ready-to-use agent templates for common development tasks
- **Standardized Quality**: Established deployment requirements and best practices for enterprise use
- **Knowledge Capture**: Documented business value propositions for each template category
- **Reduced Onboarding**: New team members can deploy agents 3x faster with pre-built templates

## Progress Metrics 📊
- **Template Library**: 15 agent templates + 5 command workflows
- **Development Acceleration**: 60% faster agent creation
- **Documentation**: Complete deployment and business value guides

## Next Week's Focus 🔜
Begin development of Data Engineer Agent using new template framework
```

---

This command generates business-focused executive summaries that communicate value to stakeholders without overwhelming technical details.