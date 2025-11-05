from strands import Agent, tool
from strands_tools import retrieve, http_request

@tool
def cohort_specialist(query: str) -> str:
    """
    Create a client cohort for analysis based on the given criteria.

    Args:
        query: A query describing the criteria for the client cohort.

    Returns:
        A confirmation that the cohort has been created or an error message.
    """
    try:
        agent = Agent(
            system_prompt="""You are a specialized agent for creating client cohorts for analysis.""",
            tools=[retrieve, http_request],
        )
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in cohort_specialist: {str(e)}"
