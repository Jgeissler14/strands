"""Configuration helpers for Team Lead Agentcore hosting."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class AgentcoreConfig:
    """Runtime configuration for the hosted Agentcore agent."""

    aws_region: str
    agent_id: str
    host: str = "0.0.0.0"
    port: int = 8080
    strands_workspace_id: Optional[str] = None
    strands_api_key: Optional[str] = None
    contribution_margin_agent_id: Optional[str] = None
    company_data_agent_id: Optional[str] = None

    @classmethod
    def load(cls, env_file: Path | None = None) -> "AgentcoreConfig":
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        def _require(name: str) -> str:
            import os

            value = os.getenv(name)
            if not value:
                raise RuntimeError(f"Missing required environment variable: {name}")
            return value

        import os

        return cls(
            aws_region=_require("AWS_REGION"),
            agent_id=_require("AGENTCORE_AGENT_ID"),
            host=os.getenv("AGENTCORE_HOST", "0.0.0.0"),
            port=int(os.getenv("AGENTCORE_PORT", "8080")),
            strands_workspace_id=os.getenv("STRANDS_WORKSPACE_ID"),
            strands_api_key=os.getenv("STRANDS_API_KEY"),
            contribution_margin_agent_id=os.getenv("CONTRIBUTION_MARGIN_AGENT_ID"),
            company_data_agent_id=os.getenv("COMPANY_DATA_AGENT_ID"),
        )


__all__ = ["AgentcoreConfig"]
