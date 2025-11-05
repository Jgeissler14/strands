from strands import Agent, tool
from strands_tools import retrieve, http_request

@tool
def revenue_cycle_specialist(query: str) -> str:
    """
    This agent will use its knowledge and tools to summarize the key revenue cycle insights.
    """
    try:
        agent = Agent(
            system_prompt="""You will simulate getting a response from tools by returning the following markup response:
                            **1 Revenue Cycle **

                            | **Metric**                               | **2025 Projection (USD mm)** |
                            |------------------------------------------|------------------------------|
                            | Gross Patient Service Charges            | 695.8                        |
                            | Net Patient Service Revenue (achievable) | 301.7                        |
                            | Operating Expenses                       | 325.2                        |
                            """,
            tools=[retrieve, http_request],
        )
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in revenue_cycle_specialist: {str(e)}"
