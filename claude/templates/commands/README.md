# 🎯 Claude Code Command Templates - Complete Guide

## 📖 Table of Contents
- [What Are Claude Code Commands?](#what-are-claude-code-commands)
- [Why Use Command Templates?](#why-use-command-templates)
- [Quick Start (3 Minutes)](#quick-start-3-minutes)
- [Available Command Templates](#available-command-templates)
- [The Magic Prompt](#the-magic-prompt)
- [Manual Customization Guide](#manual-customization-guide)
- [Examples by Project Type](#examples-by-project-type)
- [Command Usage Guide](#command-usage-guide)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

## 🤔 What Are Claude Code Commands?

Claude Code commands are **pre-built automation workflows** that help you perform complex development tasks with a single request. Think of them as:
- 🔧 **Power tools** for common development tasks
- 🤖 **Intelligent scripts** that adapt to your codebase
- 📋 **Best practice workflows** codified and automated
- 🎭 **Specialized personas** Claude can adopt for specific tasks

Instead of manually performing repetitive tasks or explaining complex workflows step-by-step, you can invoke a command and Claude Code handles the entire process intelligently.

## 💡 Why Use Command Templates?

Command templates provide:
- ⚡ **Instant Automation**: Complex workflows ready in minutes
- 🎯 **Consistency**: Same high-quality process every time
- 📚 **Best Practices**: Industry standards built-in
- 🔄 **Reusability**: Customize once, use forever
- 👥 **Team Alignment**: Share workflows across your team

## ⚡ Quick Start (3 Minutes)

### Step 1: Create Commands Directory
```bash
# Navigate to your project root
cd /path/to/your/project

# Create the Claude commands directory
mkdir -p .claude/commands
```

### Step 2: Copy Templates
```bash
# Copy the templates you need
cp /path/to/templates/api-test.md .claude/commands/
cp /path/to/templates/security.md .claude/commands/
# ... copy any others you need
```

### Step 3: Use the Magic Prompt
Copy and paste this into Claude Code to automatically customize all templates:

```
Please explore my codebase and automatically customize all Claude Code command templates in .claude/commands/ by:
1. Analyzing my project structure, technology stack, and dependencies
2. Identifying the correct values for all placeholders in square brackets
3. Replacing all placeholders with my project-specific values
4. Removing any sections that don't apply to my stack

Start by examining package.json, requirements.txt, pom.xml, or other dependency files.
```

That's it! Your commands are ready to use! 🎉

## 📚 Available Command Templates

### 🧪 api-test.md - API Test Coverage Automation
**Purpose**: Automatically generate comprehensive test suites for API endpoints with >90% coverage

**Use Cases**:
- Generate tests for new API endpoints
- Increase test coverage for existing APIs
- Create mock patterns for external services
- Set up test harnesses for complex integrations

**Example Usage**:
```
Please run the api-test command to generate tests for all API endpoints in the /api directory
```

### 🔄 reset-branch.md - Git Branch Reset Tool
**Purpose**: Safely reset current branch to default branch state with confirmations

**Use Cases**:
- Start fresh after experiments gone wrong
- Clean up messy commit history
- Synchronize with latest main/master
- Recovery from merge conflicts

**Example Usage**:
```
Execute the reset-branch command - I need to start over on this feature
```

### 🛡️ security.md - Comprehensive Security Audit
**Purpose**: Perform expert-level security analysis of your entire application

**Use Cases**:
- Pre-deployment security review
- Compliance audits (GDPR, SOC2, etc.)
- Vulnerability assessment
- Third-party dependency analysis
- Authentication/authorization review

**Example Usage**:
```
Run the security audit command and create a report of all findings
```

### 📋 start-task.md - Task Management Workflow
**Purpose**: Orchestrate complete development workflow from task selection to code review

**Use Cases**:
- Start development on a new feature
- Coordinate multiple agents for complex tasks
- Maintain task tracking and progress
- Automate branch creation and commits

**Example Usage**:
```
Use the start-task command to begin work on ticket PROJ-123
```

## 🪄 The Magic Prompt

This prompt automatically customizes ALL templates for your project. Copy and paste exactly:

```
I need you to customize the Claude Code command templates in .claude/commands/ for my project.

Please:
1. First, explore my codebase to understand:
   - Technology stack (check package.json, requirements.txt, go.mod, pom.xml, etc.)
   - Project structure and architecture
   - Testing framework and patterns
   - Task management system (if any)
   - Deployment platform
   - Authentication method
   - Database system

2. Then for each template file in .claude/commands/:
   - Replace ALL placeholders in square brackets with appropriate values
   - Remove sections that don't apply to my stack
   - Add any project-specific patterns you find

3. Provide a summary of all replacements made

Here are common placeholders to replace:
- [PROJECT_NAME] - My project/company name
- [FRAMEWORK] - Main framework (Next.js, Django, Express, etc.)
- [TEST_FRAMEWORK] - Testing framework (Jest, Pytest, etc.)
- [PACKAGE_MANAGER] - npm, yarn, pnpm, pip, etc.
- [DATABASE_SERVICE] - PostgreSQL, MongoDB, MySQL, etc.
- [AUTH_PROVIDER] - Auth0, Firebase, Supabase, etc.
- [DEPLOYMENT_PLATFORM] - Vercel, AWS, Heroku, etc.
- [TASK_MANAGEMENT_SYSTEM] - Jira, Linear, GitHub Issues, etc.
- [DEFAULT_BRANCH] - main, master, develop, etc.

Start exploring now and customize all templates.
```

## 🛠️ Manual Customization Guide

If you prefer to customize manually, here's what to replace in each template:

### Common Placeholders Across All Templates

| Placeholder | Description | Examples |
|------------|-------------|----------|
| `[PROJECT_NAME]` | Your project/company name | "MyApp", "Acme Corp" |
| `[FRAMEWORK]` | Main application framework | "Next.js 14", "Django 4.2", "Express" |
| `[PACKAGE_MANAGER]` | Package management tool | "npm", "yarn", "pnpm", "pip" |
| `[TEST_PATH]` | Test files directory | "__tests__", "tests/", "spec/" |

### Template-Specific Placeholders

#### api-test.md
- `[TEST_FRAMEWORK]` - "Jest", "Pytest", "Mocha", "Vitest"
- `[DATABASE_CLIENT]` - Your database client import path
- `[AUTH_HANDLER]` - Your authentication handler path
- `[TABLE_NAME]` - Replace with actual table names

#### reset-branch.md
- `[DEFAULT_BRANCH]` - "main", "master", "develop"

#### security.md
- `[BACKEND_SERVICE]` - "Supabase", "Firebase", "Custom API"
- `[AUTH_PROVIDER]` - "Auth0", "AWS Cognito", "Okta"
- `[DEPLOYMENT_PLATFORM]` - "Vercel", "AWS", "Google Cloud"
- `[MIDDLEWARE_FILE]` - "middleware.ts", "auth.py", "server.js"

#### start-task.md
- `[TASK_MANAGEMENT_SYSTEM]` - "Linear", "Jira", "GitHub"
- `[TASK_PREFIX]` - "PROJ", "TASK", "ISSUE"
- `[TASK_TRACKING_PATH]` - ".claude/tasks/", "docs/tasks/"
- `[TEAM_KEY]` - Your team's abbreviation

## 📝 Examples by Project Type

### Example 1: React + Node.js SaaS

```markdown
# For api-test.md
[PROJECT_NAME] → "SaaSPlatform"
[FRAMEWORK] → "Express.js"
[TEST_FRAMEWORK] → "Jest"
[DATABASE_CLIENT] → "@/lib/prisma"
[AUTH_HANDLER] → "@/middleware/auth"

# For security.md
[BACKEND_SERVICE] → "PostgreSQL with Prisma"
[AUTH_PROVIDER] → "Auth0"
[DEPLOYMENT_PLATFORM] → "AWS ECS"
```

### Example 2: Python Django Application

```markdown
# For api-test.md
[PROJECT_NAME] → "DjangoApp"
[FRAMEWORK] → "Django 4.2"
[TEST_FRAMEWORK] → "Pytest"
[PACKAGE_MANAGER] → "pip"
[TEST_PATH] → "tests/"

# For security.md
[BACKEND_SERVICE] → "PostgreSQL"
[AUTH_PROVIDER] → "Django Auth"
[DEPLOYMENT_PLATFORM] → "Heroku"
```

### Example 3: Next.js E-commerce

```markdown
# For start-task.md
[TASK_MANAGEMENT_SYSTEM] → "Linear"
[TASK_PREFIX] → "SHOP"
[TEAM_KEY] → "shop"
[PACKAGE_MANAGER] → "pnpm"
```

## 📖 Command Usage Guide

### How to Invoke Commands

Once customized, you can invoke commands in several ways:

#### Direct Invocation
```
Run the api-test command for the /api/users endpoint
```

#### With Parameters
```
Execute the start-task command for ticket PROJ-123
```

#### Batch Operations
```
Run the security audit on the authentication module only
```

### Command Chaining

Commands can work together:
```
1. Start with the start-task command for PROJ-456
2. After implementation, run api-test to ensure coverage
3. Then run security audit on the new code
4. Finally, prepare the commit
```

### Command Customization

You can override defaults:
```
Run api-test but target 95% coverage instead of 90%
```

## ✨ Best Practices

### 1. Start with Core Commands
Begin with these essential commands:
- `api-test` - Maintain quality
- `security` - Ensure safety
- `start-task` - Manage workflow

### 2. Customize Incrementally
- Start with automatic customization
- Fine-tune based on your needs
- Add project-specific sections

### 3. Version Control
- Commit customized commands to git
- Track changes over time
- Share with your team

### 4. Regular Updates
- Update commands when stack changes
- Add new patterns as discovered
- Remove outdated sections

### 5. Team Alignment
- Review commands in team meetings
- Ensure everyone understands workflow
- Document any special customizations

## 🔧 Troubleshooting

### Issue: "Command not found"
**Solution**: Ensure the command file is in `.claude/commands/` and has `.md` extension.

### Issue: "Placeholders still visible"
**Solution**: Run the magic prompt again or manually search for `[` brackets.

### Issue: "Command doesn't fit my workflow"
**Solution**: Commands are starting points - customize them to match your exact needs.

### Issue: "Tests are failing"
**Solution**: Ensure your mock patterns match your actual implementation.

### Issue: "Security audit too broad"
**Solution**: Comment out sections that don't apply to your stack.

## ❓ FAQ

### Q: Can I create my own commands?
**A:** Absolutely! Use these templates as inspiration for your own automated workflows.

### Q: How do commands differ from agents?
**A:** Commands are specific workflows/tasks, while agents are specialized personas. Commands often use multiple agents.

### Q: Can I modify commands after customization?
**A:** Yes! Treat them as living documents that evolve with your project.

### Q: Do commands work with all languages?
**A:** These templates are language-agnostic once customized for your stack.

### Q: How often should I run security audits?
**A:** Before major releases, after significant changes, or on a regular schedule (monthly/quarterly).

### Q: Can commands call other commands?
**A:** Yes! Commands can reference and trigger other commands for complex workflows.

### Q: Should I customize all commands at once?
**A:** No, start with the ones you need immediately and add others as required.

## 🚀 Next Steps

1. **Copy the templates** you need
2. **Run the magic prompt** for instant customization
3. **Test a command** to see it in action
4. **Fine-tune** based on your experience
5. **Share** with your team

## 🎯 Quick Command Reference

Save this for easy access:

```bash
# Setup
mkdir -p .claude/commands
cd .claude/commands

# Copy templates (adjust path as needed)
cp /path/to/templates/*.md .

# The Magic Prompt (paste into Claude Code)
"Please explore my codebase and automatically customize all Claude Code command templates in .claude/commands/"

# Use commands
"Run the api-test command"
"Execute security audit"
"Start task PROJ-123"
"Reset this branch"
```

## 💬 Getting Help

- **Command Issues**: Check the template documentation at the top of each file
- **Customization Help**: Use the magic prompt for automatic setup
- **Workflow Questions**: Commands can be modified to match any workflow
- **Best Practices**: Ask Claude Code for recommendations specific to your stack

---

## 📋 Command Capabilities Summary

| Command | Purpose | Time Saved | Complexity |
|---------|---------|------------|------------|
| **api-test** | Generate comprehensive API tests | 2-4 hours per endpoint | High |
| **reset-branch** | Safe branch reset with confirmations | 5-10 minutes | Low |
| **security** | Full security audit | 1-2 days | Very High |
| **start-task** | Complete task workflow | 30-60 minutes | High |

---

*Transform your development workflow with intelligent automation! 🚀*

*Commands are your automation Swiss Army knife - use them wisely and customize freely!*