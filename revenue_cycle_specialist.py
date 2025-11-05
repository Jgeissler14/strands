from strands import Agent, tool
from strands_tools import retrieve, http_request

@tool
def revenue_cycle_specialist(query: str) -> str:
    """
    Assess the revenue cycle based on the given query.

    Args:
        query: A query for the revenue cycle assessment.

    Returns:
        The results of the revenue cycle assessment.
    """
    try:
        agent = Agent(
            system_prompt="""You are a specialized agent for assessing the revenue cycle.""",
            tools=[retrieve, http_request],
        )
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in revenue_cycle_specialist: {str(e)}"
