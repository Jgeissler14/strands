from strands import Agent, tool
from strands_tools import retrieve, http_request

@tool
def contribution_margin_specialist(query: str) -> str:
    """
    This agent will use its knowledge and tools to summarize the key contribution margin insights.
    """
    try:
        agent = Agent(
            system_prompt="""You will simulate getting a response from tools byt returning the following markup response:
                            **1 Contribution Margin Variance by Location**
                            -   Supplier-level equipment/supply costs vary minimally.
                            -   East Campus exhibits the lowest contribution margins.
                            -   Six clinicians at East Campus consistently underperform margin targets.""",
            tools=[retrieve, http_request],
        )
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in contribution_margin_specialist: {str(e)}"
