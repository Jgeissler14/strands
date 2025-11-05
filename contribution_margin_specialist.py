from strands import Agent, tool
from strands_tools import retrieve, http_request

@tool
def contribution_margin_specialist(query: str) -> str:
    """
    Assess the contribution margin based on the given query.

    Args:
        query: A query for the contribution margin assessment.

    Returns:
        The results of the contribution margin assessment.
    """
    try:
        agent = Agent(
            system_prompt="""You are a specialized agent for assessing the contribution margin.""",
            tools=[retrieve, http_request],
        )
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in contribution_margin_specialist: {str(e)}"
