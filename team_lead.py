"""
Strands Agent sample with AgentCore
"""
import os
from strands import Agent
from strands_tools.code_interpreter import AgentCoreCodeInterpreter
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

MEMORY_ID = os.getenv("BEDROCK_AGENTCORE_MEMORY_ID")
REGION = os.getenv("AWS_REGION")
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"


def _content_blocks_to_text(content: list[dict[str, Any]] | None) -> str:
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
            text = _content_blocks_to_text(message.get("content")) or str(agent_result)
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

@app.entrypoint
def invoke(payload, context):
    actor_id = "quickstart-user"

    # Get runtime session ID for isolation
    session_id = getattr(context, 'session_id', None)

    # Configure memory if available
    session_manager = None
    if MEMORY_ID:
        memory_config = AgentCoreMemoryConfig(
            memory_id=MEMORY_ID,
            session_id=session_id or 'default',
            actor_id=actor_id,
            retrieval_config={
                f"/users/{actor_id}/facts": RetrievalConfig(top_k=3, relevance_score=0.5),
                f"/users/{actor_id}/preferences": RetrievalConfig(top_k=3, relevance_score=0.5)
            }
        )
        session_manager = AgentCoreMemorySessionManager(memory_config, REGION)

    # Create Code Interpreter with runtime session binding
    code_interpreter = AgentCoreCodeInterpreter(
        region=REGION,
        session_name=session_id,
        auto_create=True
    )

<<<<<<< HEAD
    agent = Agent(
=======
    finance_specialist = Agent(
        model=MODEL_ID,
        session_manager=session_manager,
        name="finance_specialist",
        description="Finance specialist focused on financial health assessments and forecasting.",
        system_prompt="""You are a finance specialist. Provide rigorous financial analysis, identify trends, and deliver
clear, actionable recommendations grounded in standard financial best practices.""",
    )

    contribution_margin_specialist = Agent(
        model=MODEL_ID,
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

    team_lead = Agent(
>>>>>>> parent of 7b356d2 (Refactor team lead specialists into separate modules)
        model=MODEL_ID,
        session_manager=session_manager,
        system_prompt="""You are a helpful assistant with code execution capabilities. Use tools when appropriate.
Response format when using code:
1. Brief explanation of your approach
2. Code block showing the executed code
3. Results and analysis
""",
        tools=[code_interpreter.code_interpreter]
    )

<<<<<<< HEAD
    result = agent(payload.get("prompt", ""))
    return {"response": result.message.get('content', [{}])[0].get('text', str(result))}
=======
    prompt = payload.get("prompt", "")
    result = team_lead(prompt)
    response_text = _content_blocks_to_text(result.message.get("content")) or str(result)
    return {"response": response_text}
>>>>>>> parent of 7b356d2 (Refactor team lead specialists into separate modules)

if __name__ == "__main__":
    app.run()