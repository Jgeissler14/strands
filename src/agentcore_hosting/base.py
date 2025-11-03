"""Common abstractions to coordinate Strands agents inside Agentcore."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, Optional


@dataclass
class ToolAgent:
    """Metadata for a Strands sub-agent exposed as a tool."""

    name: str
    description: str
    handler: Callable[[str, Dict[str, Any]], Awaitable[str]]
    instructions: Optional[str] = None
    configuration: Dict[str, Any] = field(default_factory=dict)

    async def invoke(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Delegate an instruction to the underlying tool agent."""
        context = context or {}
        return await self.handler(prompt, context)


class ConversationRouter:
    """Very small abstraction used by Agentcore runtime.

    When Agentcore forwards an interaction to this hosted agent we use the
    router to orchestrate the Team Lead agent and its tool agents. A concrete
    implementation that integrates with Strands should override ``dispatch``
    but by providing this hook we can keep the remainder of the project
    framework-agnostic for local development.
    """

    async def dispatch(self, user_input: str, session_state: Dict[str, Any]) -> str:
        raise NotImplementedError


__all__ = ["ToolAgent", "ConversationRouter"]
