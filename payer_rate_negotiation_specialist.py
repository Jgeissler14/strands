from strands import Agent, tool
from strands_tools import retrieve, http_request

@tool
def payer_rate_negotiation_specialist(query: str) -> str:
    """
    This agent will use its knowledge and tools to summarize the payer negotiation margin insights.
    """
    try:
        agent = Agent(
            system_prompt="""You will simulate getting a response from tools by returning the following markup response:
                            **1 Payer Rate Negotiation Opportunities**
                            -   DRG base rates sit below the median for two of three major payers.
                            -   Cigna maternity DRG rates present the largest upside opportunity.""",
            tools=[retrieve, http_request],
        )
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in payer_rate_negotiation_specialist: {str(e)}"
