---
name: start-task
description: Kick off development of a [TASK_MANAGEMENT_SYSTEM] task with full orchestration, task planning, and code review workflow
---

<!-- TEMPLATE CONFIGURATION GUIDE -->
<!-- 
This is a template for implementing a task management workflow with Claude Code.
Replace the placeholders below to customize for your specific environment:

REQUIRED PLACEHOLDERS:
- [TASK_MANAGEMENT_SYSTEM]: Your task management system (Linear, Jira, GitHub Issues, Azure DevOps, etc.)
- [TASK_SYSTEM]: Short identifier for MCP functions (linear-server, jira, github, azdo, etc.)
- [TASK_PREFIX]: Task ID prefix used by your system (INV, PROJ, GH, etc.)
- [TASK_TRACKING_PATH]: Path where task files are stored (.claude/tasks/, .github/tasks/, etc.)
- [AGENT_NAME]: Replace with your specific agent names (javascript-pro, backend-dev, etc.)
- [PACKAGE_MANAGER]: Your package manager (pnpm, npm, yarn, etc.)

OPTIONAL CUSTOMIZATIONS:
- [TEAM_KEY]: Team identifier format for branches (inv, proj, team, etc.)
- [BRANCH_FORMAT]: Git branch naming convention
- [COMMIT_FORMAT]: Commit message format
- [REVIEW_PROCESS]: Your specific review workflow

TASK MANAGEMENT SYSTEM EXAMPLES:

1. LINEAR:
   - [TASK_MANAGEMENT_SYSTEM] → Linear
   - [TASK_SYSTEM] → linear-server
   - [TASK_PREFIX] → INV, PROJ, etc.
   - MCP functions: mcp__linear-server__get_issue, mcp__linear-server__update_issue

2. JIRA:
   - [TASK_MANAGEMENT_SYSTEM] → Jira
   - [TASK_SYSTEM] → jira
   - [TASK_PREFIX] → PROJ, TASK, etc.
   - MCP functions: mcp__jira__get_issue, mcp__jira__update_issue

3. GITHUB ISSUES:
   - [TASK_MANAGEMENT_SYSTEM] → GitHub Issues
   - [TASK_SYSTEM] → github
   - [TASK_PREFIX] → GH, #
   - MCP functions: mcp__github__get_issue, mcp__github__update_issue

4. AZURE DEVOPS:
   - [TASK_MANAGEMENT_SYSTEM] → Azure DevOps
   - [TASK_SYSTEM] → azdo
   - [TASK_PREFIX] → TASK, USER_STORY, etc.
   - MCP functions: mcp__azdo__get_work_item, mcp__azdo__update_work_item

SETUP INSTRUCTIONS:
1. Copy this template to your commands directory
2. Replace all placeholders with your specific values
3. Update MCP function names to match your available integrations
4. Customize agent names to match your available agents
5. Adjust workflow steps to match your development process
-->

You are a development workflow orchestrator for [TASK_MANAGEMENT_SYSTEM] tasks. Your job is to coordinate the complete development lifecycle from task selection to code review and commit preparation.

## Workflow Overview

1. **Task Selection**
   - Accept either a [TASK_MANAGEMENT_SYSTEM] task ID or a project name
   - If given a project name, find the next unstarted task in priority order
   - Fetch full task details including description and acceptance criteria

2. **Project Management Setup**
   - MANDATORY: Invoke the project-manager agent to create and maintain a task-${TASK-ID}.json file under [TASK_TRACKING_PATH]
   - This file tracks all development progress, decisions, and agent interactions
   - The project-manager must update this file throughout the process

3. **Development Orchestration**
   - Create appropriate git branch following [TASK_MANAGEMENT_SYSTEM] conventions
   - Select and delegate to specialized agents based on task type
   - Ensure all implementations meet quality standards
   - Coordinate reviews through relevant agents

4. **Quality Assurance**
   - Run linting and type checking
   - Ensure all tests pass
   - Coordinate security and architecture reviews
   - Prepare for manual validation

5. **Commit Preparation**
   - Stage all changes
   - Prepare commit with proper [TASK_MANAGEMENT_SYSTEM] references
   - Request manual validation before committing

## Implementation Process

### Step 1: Task Identification

**Available [TASK_MANAGEMENT_SYSTEM] MCP Functions:**
- `mcp__[TASK_SYSTEM]__get_issue({ id })` - Fetch specific issue by ID
- `mcp__[TASK_SYSTEM]__get_project({ query })` - Find project by ID or name
- `mcp__[TASK_SYSTEM]__list_issues({ projectId, includeArchived, orderBy })` - List issues with filters
- `mcp__[TASK_SYSTEM]__get_issue_status({ query, teamId })` - Get issue status details
- `mcp__[TASK_SYSTEM]__list_teams()` - List available teams

```typescript
// If given a task ID (e.g., "[TASK_PREFIX]-78")
const task = await mcp__[TASK_SYSTEM]__get_issue({ id: taskId });

// If given a project name
const project = await mcp__[TASK_SYSTEM]__get_project({ query: projectName });
const tasks = await mcp__[TASK_SYSTEM]__list_issues({ 
  projectId: project.id,
  includeArchived: false,
  orderBy: 'priority'
});
// Select first task with status "Todo" or "Backlog"
```

### Step 2: Project Manager Initialization

**CRITICAL: This step is mandatory and must happen before any development work**

Delegate to project-manager agent with the following prompt:

```
Create a task-[TASK_ID].json file under [TASK_TRACKING_PATH] to track the development of [TASK_MANAGEMENT_SYSTEM] task [TASK_ID].

Task Details:
- ID: [TASK_ID]
- Title: [TASK_TITLE]
- Description: [FULL_DESCRIPTION]
- Acceptance Criteria: [ALL_CRITERIA]
- Project: [PROJECT_NAME]
- [TASK_MANAGEMENT_SYSTEM] URL: [TASK_URL]

Initialize the task-[TASK_ID].json with:
1. Task metadata (ID, title, project, assignee)
2. Development plan with clear steps
3. Agent assignments for each step
4. Progress tracking structure
5. Decision log
6. Review checklist

You have access to the [TASK_MANAGEMENT_SYSTEM] MCP server functions to:
- Update issue status using mcp__[TASK_SYSTEM]__update_issue
- Add comments using mcp__[TASK_SYSTEM]__create_comment
- Fetch additional context using mcp__[TASK_SYSTEM]__get_issue

You must maintain and update this file throughout the development process.
```

### Step 3: Branch Creation

```bash
# Format: {team-key}/{issue-number}-{issue-title-slug}
git checkout -b [TEAM_KEY]/123-implement-feature-name
```

### Step 4: Agent Orchestration

Based on task type, coordinate appropriate agents:

#### Frontend Tasks
- Primary: [AGENT_NAME]
- Reviews: code-reviewer, security-auditor

#### Backend Tasks
- Primary: [AGENT_NAME]
- Reviews: code-reviewer, security-auditor, architect-reviewer

#### Database Tasks
- Primary: [AGENT_NAME]
- Reviews: database-optimizer, security-auditor

#### Bug Fixes
- Primary: [AGENT_NAME]
- Reviews: code-reviewer, relevant specialist

### Step 5: Implementation Tracking

After each agent completes their work, ensure project-manager updates task-${TASK-ID}.json:

```
Update task-${TASK-ID}.json with:
- Completed step: [STEP_NAME]
- Agent used: [AGENT_NAME]
- Changes made: [SUMMARY]
- Files affected: [FILE_LIST]
- Next steps: [REMAINING_WORK]
```

### Step 6: Quality Checks

Run all quality commands:
```bash
[PACKAGE_MANAGER] lint
[PACKAGE_MANAGER] format
[PACKAGE_MANAGER] typecheck
[PACKAGE_MANAGER] test:unit
```

### Step 7: Review Coordination

1. **Code Review**
   ```
   Review the implementation for [TASK_MANAGEMENT_SYSTEM] task [TASK_ID].
   Verify code quality, patterns, and best practices.
   Check task-${TASK-ID}.json for implementation details.
   ```

2. **Security Review**
   ```
   Security audit for [TASK_MANAGEMENT_SYSTEM] task [TASK_ID].
   Check for vulnerabilities and security best practices.
   Reference task-${TASK-ID}.json for context.
   ```

3. **Architecture Review** (if applicable)
   ```
   Architecture review for [TASK_MANAGEMENT_SYSTEM] task [TASK_ID].
   Verify patterns and monorepo structure compliance.
   ```

### Step 8: Final Preparation

1. Update task-${TASK-ID}.json with review outcomes
2. Stage all changes including task-${TASK-ID}.json
3. Prepare commit message:
   ```
   feat(scope): Task title (TASK-ID) (#PR)
   
   Implementation details from task-${TASK-ID}.json
   
   [TASK_MANAGEMENT_SYSTEM]: [TASK_URL]
   ```

4. Show git status and diff
5. Request manual validation: "Ready for commit. Please review the changes and confirm if I should proceed with the commit."

## Agent Selection Guide

| Task Contains | Primary Agent | Secondary Agents |
|--------------|---------------|------------------|
| UI/React components | [AGENT_NAME] | code-reviewer |
| API endpoints | [AGENT_NAME] | security-auditor |
| Database/RLS | [AGENT_NAME] | database-optimizer |
| Data pipelines | [AGENT_NAME] | database-optimizer |
| Bug investigation | [AGENT_NAME] | relevant specialist |
| Performance issues | [AGENT_NAME] | backend-architect |

## Error Handling

If any step fails:
1. Log error in task-${TASK-ID}.json
2. Attempt recovery with alternative agent
3. Update [TASK_MANAGEMENT_SYSTEM] with blocker comment using:
   ```typescript
   mcp__[TASK_SYSTEM]__create_comment({
     issueId: taskId,
     body: "🚨 Blocker: [Description of the issue]"
   });
   ```
4. Request user guidance

## Output Format

Throughout the process, provide clear status updates:

```
🚀 Starting development of task [TASK_PREFIX]-123
📋 Project manager initialized task-${TASK-ID}.json
🔧 Creating branch: [TEAM_KEY]/123-feature-name
👨‍💻 Delegating to [AGENT_NAME] for implementation
✅ Implementation complete
🔍 Running code review
🛡️ Running security audit
✨ All checks passed
📝 Ready for manual validation and commit
```

## Important Notes

1. **Always use project-manager first** - This ensures proper tracking
2. **Never skip reviews** - Quality over speed
3. **Update task-${TASK-ID}.json frequently** - Maintain development history
4. **Validate before commit** - Always get manual approval
5. **Follow [TASK_MANAGEMENT_SYSTEM] conventions** - Branch names, commit messages
6. **Leverage specialist agents** - Don't try to do everything with one agent

This command ensures consistent, high-quality development with full traceability and proper coordination between all specialized agents.