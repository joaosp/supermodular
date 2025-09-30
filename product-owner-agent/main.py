#!/usr/bin/env python3
"""
Product Owner Agent CLI

A command-line interface for the Product Owner Agent that automates
Product Owner responsibilities for Outsystems development teams.
"""

import asyncio
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from agent import ProductOwnerAgent, get_settings

console = Console()


def print_banner():
    """Print application banner."""
    banner = """
╔═══════════════════════════════════════════════════════╗
║         Product Owner Agent for Outsystems            ║
║                                                       ║
║  Automate requirements translation, reporting,        ║
║  and risk analysis for your development teams         ║
╚═══════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    Product Owner Agent CLI.

    Automate Product Owner responsibilities including requirement translation,
    sprint reporting, and dependency analysis.
    """
    pass


@cli.command()
@click.argument("epic_key")
@click.option(
    "--architecture",
    "-a",
    default="microservices",
    help="System architecture type",
)
@click.option(
    "--components",
    "-c",
    default="",
    help="Comma-separated list of existing components",
)
@click.option(
    "--skills",
    "-s",
    default="",
    help="Comma-separated list of team skills",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file for translation results",
)
def translate(epic_key, architecture, components, skills, output):
    """
    Translate a business epic into technical user stories.

    EPIC_KEY: JIRA epic key (e.g., EPIC-123)

    Example:
        po-agent translate EPIC-123 --architecture microservices
    """
    console.print(
        f"\n[bold]Translating epic {epic_key}...[/bold]", style="cyan"
    )

    async def run():
        agent = ProductOwnerAgent()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing epic...", total=None)

            result = await agent.translate_epic(
                epic_key, architecture, components, skills
            )

            progress.update(task, completed=True)

        console.print("\n[bold green]✓ Translation completed![/bold green]")
        console.print(Panel(result, title="Translation Result", border_style="green"))

        if output:
            output_path = Path(output)
            output_path.write_text(result)
            console.print(f"\n[dim]Saved to: {output_path}[/dim]")

    asyncio.run(run())


@cli.command()
@click.argument("board_id", type=int)
@click.option(
    "--sprint",
    "-s",
    type=int,
    default=0,
    help="Sprint ID (0 for active sprint)",
)
@click.option("--team", "-t", default="Team", help="Team name")
@click.option(
    "--save-to-jira",
    "-j",
    help="JIRA issue key to attach report to",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file for report",
)
def report(board_id, sprint, team, save_to_jira, output):
    """
    Generate a sprint progress report.

    BOARD_ID: JIRA board ID

    Example:
        po-agent report 42 --sprint 123 --team "Alpha Team"
    """
    console.print(
        f"\n[bold]Generating report for board {board_id}...[/bold]",
        style="cyan",
    )

    async def run():
        agent = ProductOwnerAgent()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing sprint data...", total=None)

            result = await agent.generate_report(board_id, sprint, team)

            progress.update(task, completed=True)

        console.print("\n[bold green]✓ Report generated![/bold green]")
        console.print(Panel(result, title="Sprint Report", border_style="green"))

        if output:
            output_path = Path(output)
            output_path.write_text(result)
            console.print(f"\n[dim]Saved to: {output_path}[/dim]")

        if save_to_jira:
            console.print(f"\n[dim]Attaching report to {save_to_jira}...[/dim]")
            # TODO: Implement JIRA attachment

    asyncio.run(run())


@cli.command()
@click.argument("jql_query")
@click.option(
    "--initiative",
    "-i",
    required=True,
    help="Initiative name",
)
@click.option(
    "--target-date",
    "-d",
    required=True,
    help="Target completion date (YYYY-MM-DD)",
)
@click.option(
    "--generate-chart",
    "-c",
    is_flag=True,
    help="Generate Gantt chart",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file for analysis",
)
def analyze(jql_query, initiative, target_date, generate_chart, output):
    """
    Analyze dependencies and risks for an initiative.

    JQL_QUERY: JIRA Query Language string to fetch issues

    Example:
        po-agent analyze "project=PROJ AND fixVersion='v2.0'" -i "Version 2.0" -d 2025-12-31
    """
    console.print(
        f"\n[bold]Analyzing initiative: {initiative}...[/bold]",
        style="cyan",
    )

    async def run():
        agent = ProductOwnerAgent()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing dependencies...", total=None)

            result = await agent.analyze_risks(jql_query, initiative, target_date)

            progress.update(task, completed=True)

        console.print("\n[bold green]✓ Analysis completed![/bold green]")
        console.print(
            Panel(result, title="Risk Analysis", border_style="green")
        )

        if output:
            output_path = Path(output)
            output_path.write_text(result)
            console.print(f"\n[dim]Saved to: {output_path}[/dim]")

    asyncio.run(run())


@cli.command()
def interactive():
    """
    Start an interactive session with the agent.

    Launch an interactive chat session where you can have a conversation
    with the Product Owner Agent and execute commands dynamically.

    Example:
        po-agent interactive
    """
    print_banner()

    async def run():
        agent = ProductOwnerAgent()
        await agent.interactive_session()

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        console.print("\n[yellow]Session interrupted[/yellow]")
        sys.exit(0)


@cli.command()
def config():
    """
    Show current configuration.

    Display the current agent configuration including JIRA connection,
    Outsystems settings, and agent parameters.

    Example:
        po-agent config
    """
    try:
        settings = get_settings()

        config_info = f"""
[bold]Atlassian MCP Configuration:[/bold]
  MCP URL: {settings.atlassian.mcp_url}
  Site URL: {settings.atlassian.site_url}

[bold]Outsystems Configuration:[/bold]
  Docs URL: {settings.outsystems.docs_url}
  Version: {settings.outsystems.version}
  Repo Path: {settings.outsystems.repo_path or 'Not configured'}

[bold]Agent Settings:[/bold]
  Report Schedule: {settings.agent.report_generation_schedule}
  Risk Threshold: {settings.agent.risk_alert_threshold}
  Dependency Depth: {settings.agent.dependency_scan_depth}
  Log Level: {settings.agent.log_level}

[bold]Output Directories:[/bold]
  Reports: {settings.output.report_output_dir}
  Charts: {settings.output.chart_output_dir}

[bold]Notifications:[/bold]
  Slack: {'Enabled' if settings.notifications.slack_enabled else 'Disabled'}
"""

        console.print(Panel(config_info, title="Agent Configuration", border_style="blue"))

    except Exception as e:
        console.print(f"[red]Error loading configuration: {str(e)}[/red]")
        console.print(
            "\n[yellow]Tip:[/yellow] Make sure you have a .env file with required settings."
        )
        sys.exit(1)


@cli.command()
def check():
    """
    Check system requirements and connectivity.

    Verify that all required dependencies are installed and that
    the agent can connect to JIRA and other services.

    Example:
        po-agent check
    """
    console.print("\n[bold]Checking system requirements...[/bold]\n")

    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        console.print("✓ Python version:", f"{python_version.major}.{python_version.minor}", style="green")
    else:
        console.print("✗ Python version too old (need 3.8+)", style="red")
        return

    # Check required packages
    required_packages = [
        "claude_agent_sdk",
        "requests",
        "click",
        "rich",
        "pydantic",
        "dotenv",
    ]

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            console.print(f"✓ {package} installed", style="green")
        except ImportError:
            console.print(f"✗ {package} not installed", style="red")

    # Check configuration
    try:
        settings = get_settings()
        console.print("✓ Configuration loaded", style="green")

        # Test Agent initialization
        console.print("\n[dim]Testing Agent initialization...[/dim]")
        from agent import ProductOwnerAgent
        agent = ProductOwnerAgent()
        console.print("✓ Agent initialized successfully", style="green")

        # Check MCP servers
        options = agent._get_agent_options()
        console.print(f"✓ MCP servers configured: {', '.join(options.mcp_servers.keys())}", style="green")

        atlassian_config = options.mcp_servers.get("atlassian", {})
        console.print(f"✓ Atlassian MCP: {atlassian_config.get('type', 'N/A')} at {atlassian_config.get('url', 'N/A')}", style="green")

        console.print("\n[yellow]Note:[/yellow] First run will require browser authentication for Atlassian MCP")

    except Exception as e:
        console.print(f"✗ Configuration error: {str(e)}", style="red")
        console.print("\n[yellow]Create a .env file based on .env.example[/yellow]")

    console.print("\n[bold green]System check completed![/bold green]")


if __name__ == "__main__":
    cli()