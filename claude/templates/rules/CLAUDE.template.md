# CLAUDE.md Template

<!--
################################################################################
# CLAUDE.md TEMPLATE - SETUP INSTRUCTIONS
################################################################################

This template helps you create a comprehensive CLAUDE.md file for your project.
CLAUDE.md provides context and guidance to Claude Code when working with your codebase.

## Quick Setup (2 minutes):
1. Copy this template to your project root as CLAUDE.md
2. Replace all placeholders in square brackets [LIKE_THIS] with your values
3. Delete sections that don't apply to your project
4. Add any project-specific rules or patterns

## Automatic Setup:
Use this prompt in Claude Code for automatic customization:

"Please analyze my codebase and create a customized CLAUDE.md file by:
1. Detecting my technology stack and project structure
2. Identifying key commands and workflows
3. Finding coding patterns and conventions
4. Replacing all placeholders in the template
5. Adding project-specific guidelines"

################################################################################
-->

# CLAUDE.md

This file provides comprehensive guidance to Claude Code when working with code in this repository.

## 🎯 Project Overview

**Project**: [PROJECT_NAME]
**Description**: [Brief description of what your project does]
**Primary Goal**: [Main objective or value proposition]
**Domain**: [Business domain - e.g., e-commerce, healthcare, fintech, etc.]

## 🏗️ Architecture & Structure

### Repository Type
<!-- Choose one and delete others -->
- [ ] Monorepo with multiple packages
- [ ] Single application
- [ ] Library/Package
- [ ] Microservices

### Project Structure
```
[PROJECT_ROOT]/
├── [MAIN_APP_DIR]/          # [Description - e.g., Main application code]
├── [API_DIR]/               # [Description - e.g., API endpoints]
├── [COMPONENTS_DIR]/        # [Description - e.g., Shared components]
├── [TESTS_DIR]/             # [Description - e.g., Test files]
├── [DOCS_DIR]/              # [Description - e.g., Documentation]
└── [CONFIG_DIR]/            # [Description - e.g., Configuration files]
```

### Key Directories
- **[PRIMARY_SOURCE_DIR]**: Main source code location
- **[BUILD_OUTPUT_DIR]**: Build artifacts location
- **[DEPENDENCIES_DIR]**: Dependencies location (node_modules, vendor, etc.)

## 🛠️ Technology Stack

### Core Technologies
- **Language**: [LANGUAGE] [VERSION] <!-- e.g., TypeScript 5.0, Python 3.11 -->
- **Framework**: [FRAMEWORK] [VERSION] <!-- e.g., Next.js 14, Django 4.2 -->
- **Runtime**: [RUNTIME] [VERSION] <!-- e.g., Node.js 20, Python 3.11 -->
- **Package Manager**: [PACKAGE_MANAGER] <!-- npm, yarn, pnpm, pip, poetry -->

### Frontend (if applicable)
- **UI Framework**: [UI_FRAMEWORK] <!-- React, Vue, Angular, etc. -->
- **Styling**: [STYLING_SOLUTION] <!-- Tailwind CSS, styled-components, CSS Modules -->
- **State Management**: [STATE_MANAGEMENT] <!-- Redux, Zustand, Context API -->
- **Build Tool**: [BUILD_TOOL] <!-- Vite, Webpack, Turbopack -->

### Backend (if applicable)
- **API Type**: [API_TYPE] <!-- REST, GraphQL, gRPC -->
- **Database**: [DATABASE] <!-- PostgreSQL, MongoDB, MySQL -->
- **ORM/ODM**: [ORM] <!-- Prisma, TypeORM, Mongoose, SQLAlchemy -->
- **Authentication**: [AUTH_SOLUTION] <!-- JWT, OAuth, Session-based -->

### Infrastructure
- **Deployment Platform**: [DEPLOYMENT_PLATFORM] <!-- Vercel, AWS, GCP, Heroku -->
- **CI/CD**: [CI_CD_PLATFORM] <!-- GitHub Actions, GitLab CI, Jenkins -->
- **Container**: [CONTAINER_SOLUTION] <!-- Docker, Kubernetes -->
- **Monitoring**: [MONITORING_SOLUTION] <!-- DataDog, New Relic, CloudWatch -->

## 📋 Essential Commands

### Development Workflow
```bash
# Start development server
[PACKAGE_MANAGER] [DEV_COMMAND]              # e.g., npm run dev

# Start specific service (if monorepo)
[PACKAGE_MANAGER] [WORKSPACE_COMMAND]        # e.g., pnpm --filter web dev

# Build for production
[PACKAGE_MANAGER] [BUILD_COMMAND]            # e.g., npm run build

# Run in production mode
[PACKAGE_MANAGER] [START_COMMAND]            # e.g., npm start
```

### Testing
```bash
# Run all tests
[PACKAGE_MANAGER] [TEST_COMMAND]             # e.g., npm test

# Run tests with coverage
[PACKAGE_MANAGER] [COVERAGE_COMMAND]         # e.g., npm run test:coverage

# Run specific test file
[PACKAGE_MANAGER] [TEST_FILE_COMMAND]        # e.g., npm test -- path/to/test

# Run e2e tests
[PACKAGE_MANAGER] [E2E_COMMAND]              # e.g., npm run test:e2e
```

### Code Quality
```bash
# Lint code
[PACKAGE_MANAGER] [LINT_COMMAND]             # e.g., npm run lint

# Format code
[PACKAGE_MANAGER] [FORMAT_COMMAND]           # e.g., npm run format

# Type checking (if applicable)
[PACKAGE_MANAGER] [TYPECHECK_COMMAND]        # e.g., npm run typecheck

# Run all checks
[PACKAGE_MANAGER] [CHECK_ALL_COMMAND]        # e.g., npm run check
```

### Database Operations (if applicable)
```bash
# Run migrations
[DATABASE_MIGRATION_COMMAND]                 # e.g., npm run db:migrate

# Generate types/schema
[DATABASE_TYPEGEN_COMMAND]                   # e.g., npm run db:typegen

# Seed database
[DATABASE_SEED_COMMAND]                      # e.g., npm run db:seed

# Reset database
[DATABASE_RESET_COMMAND]                     # e.g., npm run db:reset
```

### Deployment
```bash
# Deploy to production
[DEPLOY_COMMAND]                             # e.g., npm run deploy

# Deploy to staging
[DEPLOY_STAGING_COMMAND]                     # e.g., npm run deploy:staging

# Preview deployment
[DEPLOY_PREVIEW_COMMAND]                     # e.g., npm run deploy:preview
```

## 💻 Code Style & Conventions

### General Principles
- **Code Philosophy**: [Clean Code, DRY, SOLID, etc.]
- **Design Patterns**: [MVC, MVVM, Repository, etc.]
- **Error Handling**: [Approach to error handling]
- **Comments**: [When and how to comment code]

### Naming Conventions
- **Files**: [camelCase, kebab-case, PascalCase]
- **Components/Classes**: [PascalCase, etc.]
- **Functions/Methods**: [camelCase, snake_case]
- **Variables**: [camelCase, snake_case]
- **Constants**: [UPPER_SNAKE_CASE, etc.]
- **Database Tables**: [snake_case, plural/singular]

### File Organization
```
[FEATURE_DIR]/
├── index.[EXT]              # Public API/exports
├── [FEATURE].[EXT]          # Main implementation
├── [FEATURE].test.[EXT]     # Tests
├── [FEATURE].types.[EXT]    # Type definitions
└── [FEATURE].utils.[EXT]    # Utility functions
```

### Import Order
1. External dependencies
2. Internal aliases/absolute imports
3. Relative imports
4. Type imports (if TypeScript)

### Specific Patterns
```[LANGUAGE]
// Example of preferred patterns in your codebase
// Replace with actual examples from your project

// ✅ Preferred pattern
[GOOD_PATTERN_EXAMPLE]

// ❌ Avoid this pattern
[BAD_PATTERN_EXAMPLE]
```

## 🔌 API & Data Patterns

### API Structure
```
[API_BASE_PATH]/
├── [ENDPOINT_GROUP]/
│   ├── route.[EXT]          # Route handler
│   ├── validation.[EXT]     # Input validation
│   └── service.[EXT]        # Business logic
```

### Request/Response Format
```[LANGUAGE]
// Standard API response structure
{
  "success": boolean,
  "data": T | null,
  "error": {
    "code": string,
    "message": string
  } | null,
  "meta": {
    "timestamp": string,
    "version": string
  }
}
```

### Data Models
```[LANGUAGE]
// Example data model structure
interface [MODEL_NAME] {
  id: string;
  [FIELD_1]: [TYPE];
  [FIELD_2]: [TYPE];
  createdAt: Date;
  updatedAt: Date;
}
```

### Authentication Pattern
- **Method**: [JWT, Session, OAuth]
- **Token Location**: [Header, Cookie, LocalStorage]
- **Refresh Strategy**: [How tokens are refreshed]
- **Permission Model**: [RBAC, ABAC, etc.]

## 🧪 Testing Guidelines

### Test Structure
- **Unit Tests**: [UNIT_TEST_PATTERN]
- **Integration Tests**: [INTEGRATION_TEST_PATTERN]
- **E2E Tests**: [E2E_TEST_PATTERN]

### Coverage Requirements
- **Minimum Coverage**: [COVERAGE_PERCENT]%
- **Critical Paths**: Must have 100% coverage
- **New Code**: Must include tests

### Mock Patterns
```[LANGUAGE]
// Standard mock setup
[MOCK_EXAMPLE]
```

## 🔒 Security Considerations

### Authentication & Authorization
- **Auth Provider**: [AUTH_PROVIDER]
- **Session Management**: [SESSION_STRATEGY]
- **Password Policy**: [PASSWORD_REQUIREMENTS]
- **MFA**: [ENABLED/DISABLED]

### Data Protection
- **Encryption at Rest**: [ENCRYPTION_METHOD]
- **Encryption in Transit**: [TLS_VERSION]
- **PII Handling**: [PII_STRATEGY]
- **Secrets Management**: [SECRETS_SOLUTION]

### Security Headers
- CSP: [CONTENT_SECURITY_POLICY]
- CORS: [CORS_POLICY]
- Rate Limiting: [RATE_LIMIT_STRATEGY]

## ⚡ Performance Guidelines

### Optimization Targets
- **Page Load Time**: < [TARGET_MS]ms
- **API Response Time**: < [TARGET_MS]ms
- **Bundle Size**: < [TARGET_KB]KB

### Caching Strategy
- **Client Cache**: [CLIENT_CACHE_STRATEGY]
- **Server Cache**: [SERVER_CACHE_STRATEGY]
- **Database Cache**: [DB_CACHE_STRATEGY]

### Database Optimization
- **Query Optimization**: [QUERY_GUIDELINES]
- **Indexing Strategy**: [INDEX_STRATEGY]
- **Connection Pooling**: [POOL_SETTINGS]

## ⚠️ Critical Rules & Warnings

### NEVER DO
- ❌ [CRITICAL_RULE_1] <!-- e.g., Never commit secrets -->
- ❌ [CRITICAL_RULE_2] <!-- e.g., Never bypass authentication -->
- ❌ [CRITICAL_RULE_3] <!-- e.g., Never use raw SQL queries -->

### ALWAYS DO
- ✅ [CRITICAL_RULE_1] <!-- e.g., Always validate input -->
- ✅ [CRITICAL_RULE_2] <!-- e.g., Always handle errors -->
- ✅ [CRITICAL_RULE_3] <!-- e.g., Always write tests -->

### Project-Specific Rules
<!-- Add your specific business logic rules here -->
- [BUSINESS_RULE_1]
- [BUSINESS_RULE_2]
- [BUSINESS_RULE_3]

## 🤖 Claude Code Integration

### Available Agents
Located in `.claude/agents/`:
- `[AGENT_NAME]` - [Agent purpose]
- `[AGENT_NAME]` - [Agent purpose]

### Available Commands
Located in `.claude/commands/`:
- `[COMMAND_NAME]` - [Command purpose]
- `[COMMAND_NAME]` - [Command purpose]

### Workflow Patterns
1. **Feature Development**: Use `start-task` command → Implementation → `api-test` → `security` audit
2. **Bug Fixes**: Use `debugger` agent → Fix → Test → Review
3. **Performance Issues**: Use `database-optimizer` → Profile → Optimize

## 📚 Resources & Documentation

### Internal Documentation
- Architecture Docs: [DOCS_LOCATION]
- API Documentation: [API_DOCS_LOCATION]
- Style Guide: [STYLE_GUIDE_LOCATION]

### External Resources
- Framework Docs: [FRAMEWORK_DOCS_URL]
- Library Docs: [LIBRARY_DOCS_URL]
- Design System: [DESIGN_SYSTEM_URL]

## 🚀 Quick Reference

### Most Used Commands
```bash
# Development
[PACKAGE_MANAGER] [DEV_COMMAND]

# Testing
[PACKAGE_MANAGER] [TEST_COMMAND]

# Build
[PACKAGE_MANAGER] [BUILD_COMMAND]

# Deploy
[DEPLOY_COMMAND]
```

### Key File Locations
- Environment Variables: [ENV_FILE_LOCATION]
- Configuration: [CONFIG_FILE_LOCATION]
- Database Schema: [SCHEMA_LOCATION]
- API Routes: [ROUTES_LOCATION]

### Important Contacts
- Tech Lead: [TECH_LEAD_CONTACT]
- DevOps: [DEVOPS_CONTACT]
- Security: [SECURITY_CONTACT]

---

## 📝 Template Customization Checklist

After replacing placeholders, ensure you have:
- [ ] Replaced all [PLACEHOLDER] values
- [ ] Removed sections that don't apply
- [ ] Added project-specific patterns and examples
- [ ] Included critical business rules
- [ ] Added team-specific conventions
- [ ] Verified all commands work
- [ ] Added links to documentation
- [ ] Included security considerations
- [ ] Added performance targets

---

*Last Updated: [DATE]*
*Maintained by: [TEAM_NAME]*