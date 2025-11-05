"""
Strands Agent sample with AgentCore
"""
import os
from strands import Agent, tool
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from cohort_specialist import cohort_specialist
from revenue_cycle_specialist import revenue_cycle_specialist
from contribution_margin_specialist import contribution_margin_specialist
from payer_rate_negotiation_specialist import payer_rate_negotiation_specialist
from strategy_memo_specialist import strategy_memo_specialist
from memo_review_specialist import memo_review_specialist


app = BedrockAgentCoreApp()

MEMORY_ID = os.getenv("BEDROCK_AGENTCORE_MEMORY_ID")
REGION = os.getenv("AWS_REGION")
MODEL_ID = "amazon.nova-lite-v1:0"

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


    agent = Agent(
        model=MODEL_ID,
        session_manager=session_manager,
        system_prompt="""You are a team lead assistant who coordinates with specialized agents to provide comprehensive information.
You have access to the following specialized agents:
- cohort_specialist: Creates a client cohort for analysis.
- revenue_cycle_specialist: Assesses the revenue cycle.
- contribution_margin_specialist: Assesses the contribution margin.
- payer_rate_negotiation_specialist: Assesses payer rate negotiations.
- strategy_memo_specialist: Creates a strategy memo with findings.
- memo_review_specialist: Reviews and approves a strategy memo.

Use these specialized tools when relevant to provide accurate and detailed responses.

When providing responses:
1. Explain which specialist(s) you're consulting
2. Share their expert findings
3. Provide a clear, actionable conclusion
4. If using code, include it in a code block
5. Always maintain a professional, leadership tone

Remember to coordinate between specialists when a query requires multiple areas of expertise.""",
        tools=[
            cohort_specialist,
            revenue_cycle_specialist,
            contribution_margin_specialist,
            payer_rate_negotiation_specialist,
            strategy_memo_specialist,
            memo_review_specialist
        ]
    )

    result = agent(payload.get("prompt", ""))
    return {"response": result.message.get('content', [{}])[0].get('text', str(result))}

if __name__ == "__main__":
    app.run()