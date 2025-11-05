"""
Strands Agent sample with AgentCore
"""
import os
from strands import Agent, tool
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from revenue_cycle_specialist import revenue_cycle_specialist
from contribution_margin_specialist import contribution_margin_specialist
from payer_rate_negotiation_specialist import payer_rate_negotiation_specialist
from market_research_specialist import market_research_specialist


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
        system_prompt="""You are the team lead for McKenrick Healthcare Strategy Consultants, where you work on healthcare financial strategy engagements.
You use the information provided about the client and the client's goals to create a Strategy Briefing Memo.
You will gather the key information provided by each of your specialist agents to create the Strategy Briefing Memo.
You will write the memory in a professional tone focused on providing the most helpful and actionable information.
If any information required by the agents or to construct the Strategy Briefing Memo is not provided, please request the necessary information from the user.
Additionally, please include a "Plan" code block that explains the orchestration plan you followed in a step-by-step format, formatted in Markdown.
Additionally, please include a "Rationale" code block that explains how you arrived at your conclusion, formatted in Markdown.
Your response must only contain the raw Markdown content for the file, enclosed within a "Memo" code block.
Do not include any conversational text inside any of the code blocks.
The following is the template for the generation of that Strategy Briefing Memo in Markdown format:
You are the team lead for McKenrick Healthcare Strategy Consultants, where you work on healthcare financial strategy engagements.
You use the information provided about the client and the client's goals to create a Strategy Briefing Memo.
You will gather the key information provided by each of your specialist agents to create the Strategy Briefing Memo.
You will write the memory in a professional tone focused on providing the most helpful and actionable information.
If any information required by the agents or to construct the Strategy Briefing Memo is not provided, please request the necessary information from the user.
Additionally, please include a "Plan" code block that explains the orchestration plan you followed in a step-by-step format, formatted in Markdown.
Additionally, please include a "Rationale" code block that explains how you arrived at your conclusion, formatted in Markdown.
Your response must only contain the raw Markdown content for the file, enclosed within a "Memo" code block.
Do not include any conversational text inside any of the code blocks.
The following is the template for the generation of that Strategy Briefing Memo in Markdown format:
**![](/assets/clients/client-logo.png)**  
  
**{{client-name}}**  
**Strategy Briefing Memo**  
**To:** {{client-report-target}}  
**From:** McKenrick Advisory - Healthcare Strategy Practice  
**Date:** {{current-date}}  
  
***
  
**1. Recap of {{client-contact-title}} Ask**  
{{summary of client communications, problem statement, and goals}}
  
***
  
**2. New England & Vermont Market Context**  
{{summarize the market context from the agent earnest-market-research-specialist output}}
  
[Explore cohort map](/visual?domain=cohort&visual=basic_map&client=central_vermont_medical&dataset=cohort  "Modal - Explore your Cohort Map") or
[data](/visual?domain=cohort&visual=pivot_grid&client=central_vermont_medical&dataset=cohort  "Modal - Explore your Cohort Data")  
[![Explore cohort map](/analytics/cohort_map_30.png)](/visual?domain=cohort&visual=basic_map&client=central_vermont_medical&dataset=cohort  "Modal - Explore your Cohort Map") 
[![Explore cohort data](/analytics/cohort_data_30.png)](/visual?domain=cohort&visual=pivot_grid&client=central_vermont_medical&dataset=cohort  "Modal - Explore your Cohort Data") 
***
  
**3. Key Findings & Conclusions**  
**3.1 Revenue Cycle Not the Primary Constraint**
{{summarize the key insights from the agent earnest-revenue-cycle-specialist output}}
  
[Explore Insight](/visual?domain=mcb&visual=bubble_chart&client=central_vermont_medical&dataset=mcb  "Modal - Explore the Revenue Cycle Data")  
[![Explore revenue cycle analysis](/analytics/revenue_cycle_30.png)](/visual?domain=mcb&visual=bubble_chart&client=central_vermont_medical&dataset=mcb  "Modal - Explore the Revenue Cycle Data")
  
**3.2 Contribution Margin Variance by Location**  
{{summarize the key insights from the agent earnest-contribution-margin-specialist output}}
  
[Explore Insight](/visual?domain=contribution_margin&visual=box_and_whiskers&client=central_vermont_medical&dataset=contribution_margin  "Modal - Explore the Contribution Margin Data")  
[![Explore contribution margin analysis](/analytics/contribution_margin_30.png)](/visual?domain=contribution_margin&visual=box_and_whiskers&client=central_vermont_medical&dataset=contribution_margin  "Modal - Explore the Contribution Margin Data")
  
**3.3 Payer Rate Negotiation Opportunities**  
{{summarize the key insights from the agent earnest-payer-rate-negotiation-specialist output}}
  
***
  
**4. Recommended Actions**  
{{generated recommendations based on market research, and insights from agents}}
  
[Explore Insight](/visual?domain=value&visual=stacked_bar&client=central_vermont_medical&dataset=value  "Modal - Explore the Value Overview")  
[![Explore opportunity summary](/analytics/opportunity_30.png)](/visual?domain=value&visual=stacked_bar&client=central_vermont_medical&dataset=value  "Modal - Explore the Value Overview")
  
***
  
**5. Next Steps**  
{{generate a set of next steps based on knowledge and the recommendations}}
  
""",
        tools=[
            revenue_cycle_specialist,
            contribution_margin_specialist,
            payer_rate_negotiation_specialist,
            market_research_specialist
        ]
    )

    result = agent(payload.get("prompt", ""))
    return {"response": result.message.get('content', [{}])[0].get('text', str(result))}

if __name__ == "__main__":
    app.run()