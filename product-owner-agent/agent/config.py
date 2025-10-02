"""Configuration management for Product Owner Agent."""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AtlassianMCPConfig(BaseSettings):
    """Atlassian MCP Server configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    mcp_url: str = Field(
        "https://mcp.atlassian.com/v1/sse",
        alias="ATLASSIAN_MCP_URL"
    )
    site_url: str = Field(..., alias="ATLASSIAN_SITE_URL")

    # Custom fields (optional - for advanced usage)
    field_technical_spec: str = Field(
        "customfield_10001", alias="JIRA_FIELD_TECHNICAL_SPEC"
    )
    field_dependency_links: str = Field(
        "customfield_10002", alias="JIRA_FIELD_DEPENDENCY_LINKS"
    )
    field_risk_score: str = Field(
        "customfield_10003", alias="JIRA_FIELD_RISK_SCORE"
    )
    field_team_assignment: str = Field(
        "customfield_10004", alias="JIRA_FIELD_TEAM_ASSIGNMENT"
    )
    field_milestone_target: str = Field(
        "customfield_10005", alias="JIRA_FIELD_MILESTONE_TARGET"
    )


class OutsystemsConfig(BaseSettings):
    """Outsystems-specific configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    docs_url: str = Field(
        "https://docs.outsystems.com", alias="OUTSYSTEMS_DOCS_URL"
    )
    repo_path: Optional[str] = Field(None, alias="OUTSYSTEMS_REPO_PATH")
    version: str = Field("11", alias="OUTSYSTEMS_VERSION")


class VectorDBConfig(BaseSettings):
    """Vector database configuration for enhanced context."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    connection: Optional[str] = Field(None, alias="VECTOR_DB_CONNECTION")
    enabled: bool = Field(False, alias="VECTOR_DB_ENABLED")


class AgentConfig(BaseSettings):
    """Agent behavior configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    report_generation_schedule: str = Field(
        "0 9 * * 1-5", alias="REPORT_GENERATION_SCHEDULE"
    )
    risk_alert_threshold: float = Field(0.7, alias="RISK_ALERT_THRESHOLD")
    dependency_scan_depth: int = Field(3, alias="DEPENDENCY_SCAN_DEPTH")
    log_level: str = Field("INFO", alias="LOG_LEVEL")


class ClaudeConfig(BaseSettings):
    """Claude API configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    api_key: Optional[str] = Field(
        None,
        alias="ANTHROPIC_API_KEY",
        description="Anthropic API key. If not set, the SDK will use Claude Code CLI as fallback."
    )


class NotificationConfig(BaseSettings):
    """Notification settings for alerts."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    slack_webhook_url: Optional[str] = Field(None, alias="SLACK_WEBHOOK_URL")
    slack_enabled: bool = Field(False, alias="SLACK_ENABLED")


class OutputConfig(BaseSettings):
    """Output directories configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    report_output_dir: Path = Field(
        Path("./reports"), alias="REPORT_OUTPUT_DIR"
    )
    chart_output_dir: Path = Field(
        Path("./charts"), alias="CHART_OUTPUT_DIR"
    )


class Settings(BaseSettings):
    """Main settings class combining all configurations."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    atlassian: AtlassianMCPConfig = Field(default_factory=AtlassianMCPConfig)
    outsystems: OutsystemsConfig = Field(default_factory=OutsystemsConfig)
    vector_db: VectorDBConfig = Field(default_factory=VectorDBConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    claude: ClaudeConfig = Field(default_factory=ClaudeConfig)
    notifications: NotificationConfig = Field(default_factory=NotificationConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)

    def __init__(self, **kwargs):
        """Initialize settings and create output directories."""
        super().__init__(**kwargs)
        self._create_output_dirs()

    def _create_output_dirs(self):
        """Create output directories if they don't exist."""
        self.output.report_output_dir.mkdir(parents=True, exist_ok=True)
        self.output.chart_output_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """Reload settings from environment."""
    global _settings
    _settings = Settings()
    return _settings