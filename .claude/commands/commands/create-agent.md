---
allowed-tools: Write, Read, LS
argument-hint: <agent-name>
description: Create a new Claude agent with the standard framework
---

## Agent Creation Request

Create a new agent named "$ARGUMENTS" following this exact framework:

### Required Components:

1. **Frontmatter**:
   - `name`: $ARGUMENTS (use lowercase with hyphens)
   - `description`: When this agent should be used (include "PROACTIVELY" if appropriate)
   - `tools`: List specific tools or omit to inherit all

2. **Agent Identity Section**:
   - Opening statement: "You are a [Role] specializing in [Domain]."
   - "When To Use Me" section with specific triggers
   - Core responsibilities and specializations

3. **Methodology Section**:
   - Multi-phase approach (3-4 phases typical)
   - Each phase with numbered steps
   - Clear progression from analysis to implementation

4. **Technical Standards**:
   - Quality requirements
   - Best practices specific to the domain
   - Tool usage guidelines with examples

5. **Output/Deliverables Section**:
   - Expected outputs and formats
   - Success criteria
   - Integration with other agents if applicable

### Template Structure:

```markdown
---
name: $ARGUMENTS
description: [When to use - be specific about triggers]
tools: [optional - comma-separated list]
---

You are a [Role] specializing in [specific domain and capabilities].

## When To Use Me

**PROACTIVELY use for:**
- [Specific trigger scenario 1]
- [Specific trigger scenario 2]
- [Specific trigger scenario 3]

**Key Trigger:** [Primary use case]

## Core Responsibilities

### [Primary Area]
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

### [Secondary Area]
- [Responsibility 1]
- [Responsibility 2]

## [Methodology/Process Name]

### Phase 1: [Phase Name]
1. **[Step 1]**: [Description]
2. **[Step 2]**: [Description]
3. **[Step 3]**: [Description]

### Phase 2: [Phase Name]
1. **[Step 1]**: [Description]
2. **[Step 2]**: [Description]

### Phase 3: [Phase Name]
1. **[Step 1]**: [Description]
2. **[Step 2]**: [Description]

## Technical Standards

### [Quality Area 1]
- [Standard 1]
- [Standard 2]
- [Standard 3]

### [Quality Area 2]
- [Standard 1]
- [Standard 2]

## Tool Usage Guidelines

- **[Tool 1]**: [Specific usage pattern]
- **[Tool 2]**: [Specific usage pattern]
- **[Tool 3]**: [Specific usage pattern]

## Output Format

### [Output Type 1]
- [Format specification]
- [Content requirement]

### [Output Type 2]
- [Format specification]
- [Content requirement]

## Success Criteria

- [Measurable criterion 1]
- [Measurable criterion 2]
- [Measurable criterion 3]

Remember: [Key principle or reminder about the agent's role and approach]
```

### Creation Instructions:

1. First check if an agent with this name already exists
2. Create the agent in the appropriate location:
   - Project agents: `.claude/agents/$ARGUMENTS.md`
   - User agents: `~/.claude/agents/$ARGUMENTS.md`
3. Follow the framework structure exactly
4. Make the agent specific and actionable
5. Include clear triggers for when to use the agent
6. Define comprehensive tool access if needed

Please create this new agent now, ensuring it follows the established patterns from existing agents while being tailored to its specific purpose.
