# 🚀 Claude Code Agent Templates - Complete Beginner's Guide

## 📖 Table of Contents
- [What Are Claude Code Agents?](#what-are-claude-code-agents)
- [Why Use Agent Templates?](#why-use-agent-templates)
- [Quick Start (5 Minutes)](#quick-start-5-minutes)
- [Available Agent Templates](#available-agent-templates)
- [Manual Setup Guide](#manual-setup-guide)
- [Automatic Setup with Claude Code](#automatic-setup-with-claude-code)
- [The Magic Prompt](#the-magic-prompt)
- [Examples for Different Projects](#examples-for-different-projects)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

## 🤔 What Are Claude Code Agents?

Think of Claude Code agents as **specialized AI assistants** that are experts in specific areas of software development. Instead of having one AI that knows a little about everything, you can have:
- A **JavaScript Pro** that writes perfect TypeScript code
- A **Security Auditor** that finds vulnerabilities 
- A **Database Admin** that optimizes your queries
- A **Product Manager** that creates user stories
- And many more!

Each agent has been given specific instructions, context about your project, and expertise in their domain. It's like having a team of expert developers available 24/7!

## 💡 Why Use Agent Templates?

These templates are **pre-built agent personalities** that you can customize for your project. Benefits include:
- ✅ **Save Hours**: Don't write agent instructions from scratch
- ✅ **Best Practices Built-In**: Each template includes industry best practices
- ✅ **Consistent Quality**: All agents follow proven patterns
- ✅ **Easy Customization**: Just fill in placeholders with your project details
- ✅ **Team Collaboration**: Share agents across your team

## ⚡ Quick Start (5 Minutes)

### Step 1: Create Your Agents Folder
```bash
# Navigate to your project root
cd /path/to/your/project

# Create the Claude agents directory
mkdir -p .claude/agents
```

### Step 2: Copy a Template
```bash
# Example: Copy the JavaScript Pro template
cp /path/to/templates/javascript-pro.md .claude/agents/javascript-pro.md
```

### Step 3: Use the Magic Prompt
Copy this prompt and paste it into Claude Code to automatically customize all templates for your project:

```
Please explore my codebase and automatically customize all Claude Code agent templates in .claude/agents/ by:
1. Analyzing my project structure, tech stack, and dependencies
2. Identifying the correct values for all placeholders
3. Replacing placeholders with my project-specific values
4. Keeping all best practices intact

Start by examining package.json, requirements.txt, or other dependency files, then look at the codebase structure.
```

That's it! Claude Code will customize all agents for your project automatically! 🎉

## 📚 Available Agent Templates

| Agent | Purpose | Best For |
|-------|---------|----------|
| **api-documenter** | Creates API documentation | REST APIs, GraphQL, SDK docs |
| **architect-review** | Reviews system architecture | Large refactors, new features |
| **backend-architect** | Designs backend systems | APIs, microservices, databases |
| **code-reviewer** | Reviews code quality | PRs, code improvements |
| **codebase-explorer** | Analyzes codebases | Onboarding, understanding legacy code |
| **data-engineer** | Builds data pipelines | ETL, analytics, data processing |
| **data-scientist** | Analyzes data & creates insights | Reports, ML models, analytics |
| **database-admin** | Manages databases | Schema design, migrations, optimization |
| **database-optimizer** | Optimizes queries | Performance issues, slow queries |
| **debugger** | Fixes bugs | Error investigation, troubleshooting |
| **javascript-pro** | JavaScript/TypeScript expert | React, Node.js, frontend/backend |
| **product-manager** | Product planning | User stories, feature specs |
| **project-manager** | Project coordination | Task management, sprints |
| **scrum-master** | Agile processes | Sprint planning, retrospectives |
| **security-auditor** | Security reviews | Vulnerability assessment, compliance |

## 🛠️ Manual Setup Guide

If you prefer to customize templates manually, here's how:

### Understanding Placeholders

Templates use placeholders in square brackets that you need to replace:

| Placeholder | What to Replace It With | Example |
|------------|------------------------|---------|
| `[PROJECT_NAME]` | Your project/company name | "MyApp", "Acme Corp" |
| `[PRIMARY_FRAMEWORK]` | Main framework | "Next.js 14", "Django", "Express" |
| `[DATABASE_SYSTEM]` | Your database | "PostgreSQL", "MongoDB", "MySQL" |
| `[LANGUAGE]` | Programming language | "TypeScript", "Python", "Java" |
| `[PACKAGE_MANAGER]` | Package manager | "npm", "yarn", "pnpm", "pip" |
| `[API_ROUTES_PATH]` | API directory | "app/api", "src/routes", "api/" |
| `[AUTH_SYSTEM]` | Authentication | "Auth0", "Supabase Auth", "JWT" |
| `[DOMAIN_CONTEXT]` | Your business domain | "e-commerce", "SaaS", "healthcare" |

### Step-by-Step Manual Customization

1. **Open a template file** in your favorite editor
2. **Read the placeholder documentation** at the top of each file
3. **Find and replace** each placeholder with your values
4. **Save the file** in `.claude/agents/` directory
5. **Test the agent** by asking Claude Code to use it

### Example: Customizing for a Next.js E-commerce App

Before:
```markdown
You are a specialized {PROJECT_NAME} {PRIMARY_FRAMEWORK} expert...
```

After:
```markdown
You are a specialized ShopifyClone Next.js 14 expert...
```

## 🤖 Automatic Setup with Claude Code

### The Magic Prompt

This is the ultimate prompt to set up all agents automatically. Copy and paste into Claude Code:

```
I need you to set up Claude Code agents for my project. Please:

1. First, explore my codebase to understand:
   - Project structure and architecture
   - Technology stack (check package.json, requirements.txt, go.mod, etc.)
   - Database system (check for database configs, migrations, schemas)
   - Authentication method (check auth implementations)
   - Business domain (analyze models, routes, and features)
   - API structure and patterns
   - Testing framework
   - CI/CD setup

2. Then, for each template in .claude/agents/, replace these placeholders:
   - [PROJECT_NAME] with my actual project name
   - [PRIMARY_FRAMEWORK] with my main framework
   - [DATABASE_SYSTEM] with my database
   - [LANGUAGE] with my programming language
   - [PACKAGE_MANAGER] with my package manager
   - [API_ROUTES_PATH] with my API path structure
   - [AUTH_SYSTEM] with my auth implementation
   - [DOMAIN_CONTEXT] with my business domain
   - All other placeholders with appropriate values

3. Create a SETUP_SUMMARY.md file listing all the values you used

Please start by exploring the codebase now.
```

### Advanced Automatic Setup Prompts

#### For Monorepo Projects:
```
Explore my monorepo and set up Claude Code agents for each package/app. 
Check the root package.json/lerna.json/nx.json to understand the structure, 
then customize agents for the main application considering all shared packages.
```

#### For Microservices:
```
Analyze my microservices architecture and create specialized agents for each service.
Look for docker-compose.yml, kubernetes configs, or service directories to understand
the service boundaries and customize agents accordingly.
```

#### For Legacy Codebases:
```
This is a legacy codebase that needs modernization. Set up agents that understand
both the current state and our target architecture. Check for TODO comments,
deprecated patterns, and technical debt markers to inform the agent context.
```

## 📝 Examples for Different Projects

### Example 1: React + Node.js SaaS Application

```bash
# Your project structure:
my-saas-app/
├── frontend/          # React 18 + TypeScript
├── backend/           # Node.js + Express
├── database/          # PostgreSQL
└── .claude/agents/    # Your agents go here
```

**Prompt for this setup:**
```
Set up agents for my full-stack SaaS app:
- Frontend: React 18 with TypeScript and Tailwind CSS
- Backend: Node.js with Express and Prisma ORM  
- Database: PostgreSQL with Redis for caching
- Auth: Auth0 for authentication
Focus on multi-tenant architecture patterns.
```

### Example 2: Python Data Pipeline

```bash
# Your project structure:
data-processor/
├── pipelines/         # Apache Airflow DAGs
├── transformers/      # Data transformation scripts
├── models/           # ML models
└── .claude/agents/   # Your agents go here
```

**Prompt for this setup:**
```
Configure agents for my data pipeline project:
- Python 3.11 with pandas and numpy
- Apache Airflow for orchestration
- PostgreSQL for data warehouse
- Scikit-learn for ML models
Focus on ETL best practices and data quality.
```

### Example 3: Mobile App with Backend

```bash
# Your project structure:
mobile-app/
├── app/              # React Native
├── api/              # FastAPI backend
├── infrastructure/   # Terraform configs
└── .claude/agents/   # Your agents go here
```

**Prompt for this setup:**
```
Set up agents for my mobile application:
- React Native with Expo for the mobile app
- FastAPI for the backend API
- PostgreSQL with SQLAlchemy
- AWS deployment with Terraform
Include mobile-specific patterns and API versioning.
```

## ✨ Best Practices

### 1. Start Small
- Begin with 2-3 agents most relevant to your current work
- Add more agents as you need them
- Don't overwhelm yourself with all 15 agents at once

### 2. Customize Gradually
- Start with the automatic setup
- Fine-tune specific agents based on your experience
- Add project-specific rules and patterns over time

### 3. Team Collaboration
- Share your `.claude/agents` folder via version control
- Document any custom modifications
- Create team-specific agents for your workflows

### 4. Agent Selection
- Use the right agent for the task
- Combine agents for complex tasks
- Let agents delegate to each other

### 5. Keep Agents Updated
- Update agents when your tech stack changes
- Add new patterns as you discover them
- Remove outdated rules and practices

## 🔧 Troubleshooting

### Problem: "Agent not found"
**Solution:** Make sure the agent file is in `.claude/agents/` directory and has the `.md` extension.

### Problem: "Placeholders still visible"
**Solution:** You missed some placeholders. Search for `[` in the file to find remaining placeholders.

### Problem: "Agent gives generic advice"
**Solution:** Your placeholders might be too vague. Be specific about your tech stack and requirements.

### Problem: "Agent doesn't understand my project"
**Solution:** Add more context to the agent file, including:
- Project-specific patterns
- Custom conventions
- Business logic rules
- Team preferences

### Problem: "Too many agents to manage"
**Solution:** Start with essential agents only:
1. `javascript-pro` (or your language expert)
2. `code-reviewer`
3. `debugger`
Add others as needed.

## ❓ FAQ

### Q: Can I create my own custom agents?
**A:** Absolutely! Use the templates as a starting point and create new agents for your specific needs.

### Q: How do I use an agent?
**A:** Just ask Claude Code to act as that agent. For example: "As the security-auditor, review my API endpoints."

### Q: Can agents work together?
**A:** Yes! Agents can delegate tasks to each other. The project-manager agent, for example, can coordinate other agents.

### Q: Should I commit agents to version control?
**A:** Yes! Treat them as part of your development environment configuration.

### Q: How often should I update agents?
**A:** Update them when:
- Your tech stack changes
- You establish new patterns
- You find better practices
- Team conventions evolve

### Q: Can I use agents in production?
**A:** Agents are development tools. They help you write code but don't run in production.

### Q: What if I don't have all the information for placeholders?
**A:** Fill in what you know and leave TODO comments for the rest. You can update them later.

### Q: Can I share agents between projects?
**A:** Yes! Create a shared repository of customized agents for your organization.

## 🚀 Next Steps

1. **Copy the templates** to your project
2. **Run the magic prompt** to customize them automatically
3. **Start using agents** in your daily development
4. **Customize further** based on your needs
5. **Share with your team** for consistent development practices

## 💬 Getting Help

- **Claude Code Documentation**: Ask Claude Code: "How do I use agents?"
- **Template Issues**: Check the placeholder documentation in each template
- **Best Practices**: Ask your specialized agents for domain-specific advice
- **Community**: Share your customized agents and learn from others

---

## 🎯 Quick Reference Card

Save this for quick access:

```bash
# Set up agents (copy and run)
mkdir -p .claude/agents
cd .claude/agents

# The Magic Prompt (copy and paste into Claude Code)
"Please explore my codebase and automatically customize all Claude Code agent templates in .claude/agents/ by analyzing my project and replacing all placeholders with correct values."

# Use an agent
"As the javascript-pro agent, refactor this component"
"As the security-auditor, review my authentication"
"As the database-optimizer, improve this query"
```

---

*Happy coding with your new AI team! 🎉*