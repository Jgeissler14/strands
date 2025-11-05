from strands import Agent, tool
from strands_tools import retrieve, http_request

@tool
def market_research_specialist(query: str) -> str:
    """
    This agent will use its knowledge and internet research to create a summary of the market for the client in the current engagement.
    """
    try:
        agent = Agent(
            system_prompt="""You will simulate getting a response from tools by returning the following markup response:
                            **1. New England & Vermont Market Context**
                            -   Rising labor and supply costs outstrip reimbursement growth across New England.
                            -   Provider and payer consolidation has increased negotiation leverage for large systems.
                            -   Vermont’s high Medicare/Medicaid mix compresses margins vs. commercial-heavy peers.
                            -   Value-based payment pilots demand upfront investment but reward quality.""",
            tools=[retrieve, http_request],
        )
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in market_research_specialist: {str(e)}"
