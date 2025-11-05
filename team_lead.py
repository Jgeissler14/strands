"""Strands Agent sample with AgentCore and specialist agent tools."""

import os

from strands import Agent
from strands_tools.code_interpreter import AgentCoreCodeInterpreter
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from bedrock_agentcore.runtime import BedrockAgentCoreApp

from embedded_agent_tool import content_blocks_to_text
from specialists import create_specialist_tools

app = BedrockAgentCoreApp()

MEMORY_ID = os.getenv("BEDROCK_AGENTCORE_MEMORY_ID")
REGION = os.getenv("AWS_REGION")
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"

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

    finance_tool, margin_tool = create_specialist_tools(
        model_id=MODEL_ID,
        session_manager=session_manager,
    )

    team_lead = Agent(
        model=MODEL_ID,
        session_manager=session_manager,
        name="team_lead",
        description="Team lead who coordinates finance-focused specialists.",
        system_prompt="""You are a strategic finance team lead.

Coordinate specialist agents to deliver thorough answers. Delegate to:
- finance_specialist for holistic financial analysis
- contribution_margin_specialist for margin and profitability deep dives
- code_interpreter for calculations or data validation

Always explain which specialists you consulted and synthesize their findings into an actionable summary.""",
        tools=[
            code_interpreter.code_interpreter,
            finance_tool,
            margin_tool,
        ],
    )

    prompt = payload.get("prompt", "")
    result = team_lead(prompt)
    response_text = content_blocks_to_text(result.message.get("content")) or str(result)
    return {"response": response_text}

if __name__ == "__main__":
    app.run()
