"""Utilities for wrapping Strands agents so they can be invoked as tools."""

from __future__ import annotations

from typing import Any, Iterable

from strands import Agent
from strands.types._events import ToolResultEvent
from strands.types.tools import AgentTool, ToolGenerator, ToolResult, ToolUse


def content_blocks_to_text(content: Iterable[dict[str, Any]] | None) -> str:
    """Flatten Strands content blocks into a plain-text response."""

    if not content:
        return ""

    texts: list[str] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        if isinstance(block.get("text"), str):
            texts.append(block["text"])
        elif block.get("type") == "text" and isinstance(block.get("text"), str):
            texts.append(block["text"])

    return "\n".join(texts).strip()


class EmbeddedAgentTool(AgentTool):
    """Wrap a Strands Agent instance so it can be invoked as a tool."""

    def __init__(self, *, agent: Agent, name: str, description: str) -> None:
        super().__init__()
        self._agent = agent
        self._name = name
        self._tool_spec = {
            "name": name,
            "description": description,
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "request": {
                            "type": "string",
                            "description": "Primary question or task for the specialist to solve.",
                        },
                        "context": {
                            "type": "string",
                            "description": "Optional additional context or supporting data for the request.",
                        },
                    },
                    "required": ["request"],
                }
            },
        }

    @property
    def tool_name(self) -> str:
        return self._name

    @property
    def tool_spec(self) -> dict[str, Any]:
        return self._tool_spec

    @property
    def tool_type(self) -> str:
        return "agent"

    async def stream(
        self, tool_use: ToolUse, invocation_state: dict[str, Any], **kwargs: Any
    ) -> ToolGenerator:
        input_payload = tool_use.get("input", {}) if isinstance(tool_use, dict) else {}
        request = input_payload.get("request") if isinstance(input_payload, dict) else None
        context = input_payload.get("context") if isinstance(input_payload, dict) else None

        if not isinstance(request, str) or not request.strip():
            error_result: ToolResult = {
                "toolUseId": tool_use.get("toolUseId", ""),
                "status": "error",
                "content": [
                    {
                        "text": "The 'request' field is required and must be a non-empty string.",
                    }
                ],
            }
            yield ToolResultEvent(error_result)
            return

        prompt_parts = [request.strip()]
        if isinstance(context, str) and context.strip():
            prompt_parts.append(f"Context: {context.strip()}")
        prompt = "\n\n".join(prompt_parts)

        try:
            agent_result = await self._agent.invoke_async(prompt, invocation_state=invocation_state)
            message = agent_result.message or {}
            text = content_blocks_to_text(message.get("content")) or str(agent_result)
            success_result: ToolResult = {
                "toolUseId": tool_use.get("toolUseId", ""),
                "status": "success",
                "content": [{"text": text}],
            }
            yield ToolResultEvent(success_result)
        except Exception as exc:  # pragma: no cover - defensive
            failure_result: ToolResult = {
                "toolUseId": tool_use.get("toolUseId", ""),
                "status": "error",
                "content": [
                    {
                        "text": f"{self._name} was unable to complete the request: {exc}",
                    }
                ],
            }
            yield ToolResultEvent(failure_result)
