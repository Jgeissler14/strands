"""Factory helpers for specialist Strands agents used by the team lead."""

from __future__ import annotations

from typing import Sequence

from bedrock_agentcore.memory.integrations.strands.session_manager import (
    AgentCoreMemorySessionManager,
)
from strands import Agent

from embedded_agent_tool import EmbeddedAgentTool


def create_specialist_tools(
    *,
    model_id: str,
    session_manager: AgentCoreMemorySessionManager | None,
) -> Sequence[EmbeddedAgentTool]:
    """Instantiate the finance and contribution margin specialist tools."""

    finance_specialist = Agent(
        model=model_id,
        session_manager=session_manager,
        name="finance_specialist",
        description="Finance specialist focused on financial health assessments and forecasting.",
        system_prompt="""You are a finance specialist. Provide rigorous financial analysis, identify trends, and deliver
clear, actionable recommendations grounded in standard financial best practices.""",
    )

    contribution_margin_specialist = Agent(
        model=model_id,
        session_manager=session_manager,
        name="contribution_margin_specialist",
        description="Expert in contribution margin calculations and profitability diagnostics.",
        system_prompt="""You are a contribution margin specialist. Break down revenue, variable costs, and unit economics.
Return precise contribution margin insights and highlight optimization opportunities.""",
    )

    finance_tool = EmbeddedAgentTool(
        agent=finance_specialist,
        name="finance_specialist",
        description="Provide detailed financial analysis, forecasts, and insights.",
    )
    margin_tool = EmbeddedAgentTool(
        agent=contribution_margin_specialist,
        name="contribution_margin_specialist",
        description="Evaluate contribution margins and profitability scenarios in depth.",
    )

    return finance_tool, margin_tool
