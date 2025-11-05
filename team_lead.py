"""
Strands Agent sample with AgentCore
"""
import os
from strands import Agent, tool
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from research import research_assistant
from product_recommendation_assistant import product_recommendation_assistant, trip_planning_assistant

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
You have access to research assistants, product recommendation specialists, and trip planning experts.
Use these specialized tools when relevant to provide accurate and detailed responses.

When providing responses:
1. Explain which specialist(s) you're consulting
2. Share their expert findings
3. Provide a clear, actionable conclusion
4. If using code, include it in a code block
5. Always maintain a professional, leadership tone

Remember to coordinate between specialists when a query requires multiple areas of expertise.""",
        tools=[research_assistant, product_recommendation_assistant, trip_planning_assistant]
    )

    result = agent(payload.get("prompt", ""))
    return {"response": result.message.get('content', [{}])[0].get('text', str(result))}

if __name__ == "__main__":
    app.run()