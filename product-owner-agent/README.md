# Product Owner Agent for Outsystems

An AI-powered agent built with Claude Agent SDK and Atlassian Remote MCP Server that automates Product Owner responsibilities for Outsystems development teams. This agent reduces coordination overhead, generates automated reports, and provides proactive risk management for multi-team product initiatives.

**🆕 Now with native JIRA and Confluence integration via Atlassian Remote MCP Server!**
- No credential management required (OAuth 2.1)
- Direct access to JIRA issues, sprints, and boards
- Confluence page search and creation
- Secure, cloud-based bridge to your Atlassian data

## Features

### 🔄 Business ↔ Technical Requirements Translation
Transform high-level business requirements from JIRA epics into detailed technical specifications that development teams can immediately implement.

- Parse business requirements from JIRA epics
- Access Outsystems technical documentation
- Generate detailed technical specifications
- Create granular JIRA tasks automatically
- Include story point estimates and acceptance criteria

### 📊 Auto-generated Progress Reports
Generate comprehensive sprint reports by analyzing JIRA data, reducing manual reporting overhead from hours to minutes.

- Sprint progress reports with key metrics
- Team performance analysis
- Velocity and cycle time tracking
- Blocker identification
- Automated attachment to JIRA

### ⚠️ Risk & Dependency Alerts
Proactively identify and visualize cross-team dependencies, conflicts, and risks using advanced analysis.

- Cross-team dependency mapping
- Critical path analysis
- Blocking issue detection
- Timeline risk calculation
- Mermaid Gantt chart generation
- Mitigation recommendations

## Installation

### Prerequisites

- Python 3.8 or higher
- Atlassian Cloud site with JIRA and/or Confluence
- Anthropic API key (for Claude)
- Modern web browser (for OAuth authentication)

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd product-owner-agent
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
```bash
# Atlassian MCP Configuration
ATLASSIAN_MCP_URL=https://mcp.atlassian.com/v1/sse
ATLASSIAN_SITE_URL=https://yourcompany.atlassian.net

# Claude API
ANTHROPIC_API_KEY=your_anthropic_key

# Customize other settings as needed
```

4. **Authenticate with Atlassian:**

When you first run the agent, it will open a browser window for OAuth authentication:
- Log in to your Atlassian account
- Grant access to JIRA, Compass, and/or Confluence
- Allow the Product Owner Agent to access your data

The agent will automatically connect via the Atlassian Remote MCP Server.

5. **Verify installation:**
```bash
python main.py check
```

## Usage

### Command Line Interface

#### Translate Epic to Stories
Convert a business epic into technical user stories:

```bash
python main.py translate EPIC-123 \
    --architecture microservices \
    --components "API Gateway, Auth Service" \
    --skills "Python, React, PostgreSQL"
```

#### Generate Sprint Report
Create a comprehensive sprint progress report:

```bash
python main.py report 42 \
    --sprint 123 \
    --team "Alpha Team" \
    --output report.md
```

#### Analyze Dependencies and Risks
Analyze cross-team dependencies and identify risks:

```bash
python main.py analyze "project=PROJ AND fixVersion='v2.0'" \
    --initiative "Version 2.0 Release" \
    --target-date 2025-12-31 \
    --generate-chart
```

#### Interactive Mode
Start an interactive chat session with the agent:

```bash
python main.py interactive
```

In interactive mode, you can:
- Ask questions in natural language
- Execute commands dynamically
- Have contextual conversations about your projects

#### View Configuration
Display current agent configuration:

```bash
python main.py config
```

### Python API

You can also use the agent programmatically:

```python
import asyncio
from agent import ProductOwnerAgent

async def main():
    agent = ProductOwnerAgent()

    # Translate an epic
    result = await agent.translate_epic(
        epic_key="EPIC-123",
        architecture_type="microservices",
        component_list="API Gateway, Auth Service",
        team_skills="Python, React"
    )
    print(result)

    # Generate a report
    report = await agent.generate_report(
        board_id=42,
        sprint_id=123,
        team_name="Alpha Team"
    )
    print(report)

    # Analyze risks
    analysis = await agent.analyze_risks(
        jql_query="project=PROJ AND fixVersion='v2.0'",
        initiative_name="Version 2.0",
        target_date="2025-12-31"
    )
    print(analysis)

if __name__ == "__main__":
    asyncio.run(main())
```

## Architecture

### Project Structure

```
product-owner-agent/
├── agent/                      # Core agent package
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── product_owner.py       # Main agent logic
│   └── tools/                 # Agent tools
│       ├── __init__.py
│       ├── jira_tools.py      # JIRA API integration
│       ├── translation.py     # Requirement translation
│       ├── reporting.py       # Report generation
│       └── dependency.py      # Dependency analysis
├── prompts/                   # Prompt templates
│   ├── translation.txt
│   ├── reporting.txt
│   └── risk_analysis.txt
├── main.py                    # CLI entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

### Custom Tools

The agent uses custom tools built with the Claude Agent SDK:

1. **translate_epic_to_stories**: Fetches JIRA epic and generates technical specifications
2. **create_stories_from_spec**: Creates JIRA stories from specifications
3. **generate_sprint_report**: Analyzes sprint data and generates reports
4. **save_report_to_jira**: Saves reports as JIRA attachments
5. **analyze_dependencies**: Analyzes cross-team dependencies and risks
6. **generate_gantt_chart**: Creates Mermaid Gantt charts for visualization

## Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# JIRA Custom Fields (update based on your JIRA setup)
JIRA_FIELD_TECHNICAL_SPEC=customfield_10001
JIRA_FIELD_DEPENDENCY_LINKS=customfield_10002
JIRA_FIELD_RISK_SCORE=customfield_10003
JIRA_FIELD_TEAM_ASSIGNMENT=customfield_10004
JIRA_FIELD_MILESTONE_TARGET=customfield_10005

# Agent Behavior
REPORT_GENERATION_SCHEDULE=0 9 * * 1-5  # Weekdays at 9 AM
RISK_ALERT_THRESHOLD=0.7                 # 0-1 scale
DEPENDENCY_SCAN_DEPTH=3                  # Levels of dependencies
LOG_LEVEL=INFO

# Outsystems Context
OUTSYSTEMS_VERSION=11
OUTSYSTEMS_DOCS_URL=https://docs.outsystems.com
OUTSYSTEMS_REPO_PATH=/path/to/codebase

# Output
REPORT_OUTPUT_DIR=./reports
CHART_OUTPUT_DIR=./charts
```

## Examples

### Example 1: Complete Epic Breakdown Workflow

```bash
# 1. Translate epic to technical stories
python main.py translate EPIC-456 --output epic-456-spec.md

# 2. Review the specification and create stories in JIRA
# (This can be automated in future versions)

# 3. Generate a report mid-sprint
python main.py report 42 --sprint 124 --team "Beta Team"

# 4. Analyze dependencies before sprint planning
python main.py analyze "sprint=125" \
    --initiative "Sprint 125" \
    --target-date 2025-11-15
```

### Example 2: Interactive Session

```bash
$ python main.py interactive

Product Owner Agent - Interactive Mode
==================================================
Commands:
  - translate <epic-key>: Translate epic to stories
  - report <board-id> [sprint-id]: Generate sprint report
  - analyze <jql>: Analyze dependencies and risks
  - help: Show available commands
  - exit: Exit the session
==================================================

You: What are the blockers in sprint 124?

Agent: Let me check the current sprint status...
[Generates report showing blockers and their impact]

You: How risky is our Q4 release?

Agent: Let me analyze the Q4 release timeline...
[Performs dependency analysis and risk assessment]

You: exit
Goodbye!
```

## Success Metrics

The agent is designed to improve key Product Owner metrics:

- **PO Time Reduction**: Target 40% reduction in coordination/reporting time
- **Sprint Predictability**: Achieve ≥80% accuracy in sprint commitments
- **Throughput Variance**: Maintain ≤20% variance across sprints
- **Delivery Deviation**: ≤15% deviation from GA dates
- **Report Generation Time**: <5 minutes per report
- **Dependency Conflict Detection**: 95% accuracy rate

## Troubleshooting

### Common Issues

**1. JIRA Connection Errors**
```bash
Error: 401 Unauthorized
```
Solution: Verify your JIRA API token and user email in `.env`

**2. Missing Custom Fields**
```bash
Error: Field customfield_10001 not found
```
Solution: Update the custom field IDs in `.env` to match your JIRA configuration

**3. Import Errors**
```bash
ModuleNotFoundError: No module named 'claude_agent_sdk'
```
Solution: Install dependencies with `pip install -r requirements.txt`

**4. Configuration Not Found**
```bash
Error loading configuration
```
Solution: Create a `.env` file based on `.env.example`

### Debug Mode

Enable verbose logging:

```bash
export LOG_LEVEL=DEBUG
python main.py [command]
```

## Roadmap

### Phase 1: MVP ✅ (Current)
- [x] JIRA integration
- [x] Basic requirement translation
- [x] Simple progress report generation
- [x] Manual trigger for all features

### Phase 2: Enhancement (Planned)
- [ ] Advanced NLP for requirement parsing
- [ ] Automated report scheduling
- [ ] Slack integration for alerts
- [ ] Historical data analysis

### Phase 3: Intelligence (Future)
- [ ] Machine learning for estimation accuracy
- [ ] Predictive risk analysis
- [ ] Cross-team optimization suggestions
- [ ] Feedback loop implementation

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is proprietary software developed for Outsystems by supermodular.ai.

## Support

For support and feedback, contact: supermodular-ai-team@outsystems.com

## Acknowledgments

- Built with [Claude Agent SDK](https://docs.anthropic.com/en/api/agent-sdk)
- Designed for Outsystems Product Development Lifecycle
- Developed by supermodular.ai team