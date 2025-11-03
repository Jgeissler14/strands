"""Team Lead agent orchestrating Strands tools under AWS Agentcore."""
from __future__ import annotations

import asyncio
from typing import Any, Dict, Iterable

from .base import ConversationRouter, ToolAgent
from .tools import CompanyDataAgent, ContributionMarginAgent


class TeamLeadAgent(ConversationRouter):
    """Primary agent we expose to users via Agentcore."""

    def __init__(self, *, tools: Iterable[ToolAgent] | None = None) -> None:
        self._tool_registry: Dict[str, ToolAgent] = {}
        if tools:
            for tool in tools:
                self.register_tool(tool)

    def register_tool(self, tool: ToolAgent) -> None:
        self._tool_registry[tool.name] = tool

    async def dispatch(self, user_input: str, session_state: Dict[str, Any]) -> str:
        """Simple dispatcher that selects tools based on lightweight heuristics.

        Agentcore will call this method for every turn in the conversation. The
        implementation uses trivial keyword routing today so that the repo can
        be validated without live LLM calls. When the Strands SDK is available
        you can replace the heuristics with a Strands ``Agent`` instance that
        orchestrates the tools using planning or agent-to-agent communication.
        """

        lowered = user_input.lower()
        if "margin" in lowered or "profit" in lowered:
            tool = self._tool_registry.get("contribution_margin")
            if tool:
                return await tool.invoke(user_input, session_state)
        if "data" in lowered or "policy" in lowered or "company" in lowered:
            tool = self._tool_registry.get("company_data")
            if tool:
                return await tool.invoke(user_input, session_state)

        return self._fallback_response(user_input)

    @staticmethod
    def build_default() -> "TeamLeadAgent":
        """Factory that wires the placeholder tool agents."""

        contribution_agent = ContributionMarginAgent()
        company_data_agent = CompanyDataAgent()

        tools = [
            ToolAgent(
                name=contribution_agent.name,
                description=contribution_agent.description,
                handler=contribution_agent.run,
            ),
            ToolAgent(
                name=company_data_agent.name,
                description=company_data_agent.description,
                handler=company_data_agent.run,
            ),
        ]

        return TeamLeadAgent(tools=tools)

    def _fallback_response(self, prompt: str) -> str:
        return (
            "[Team Lead]\n"
            "I can assist with contribution margin or company data questions. "
            "Please provide additional details so I can route your request to the "
            "appropriate specialist agent.\n"
            f"Prompt received: {prompt}"
        )


async def simulate_chat() -> None:
    agent = TeamLeadAgent.build_default()
    context: Dict[str, Any] = {}

    for prompt in (
        "How is our Q3 contribution margin tracking?",
        "Share any policy updates from the company data team.",
        "Tell me something unrelated.",
    ):
        response = await agent.dispatch(prompt, context)
        print("User:", prompt)
        print("Agent:", response)
        print("---")


if __name__ == "__main__":
    asyncio.run(simulate_chat())
