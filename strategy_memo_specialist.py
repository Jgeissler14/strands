from strands import Agent, tool
from strands_tools import retrieve, http_request

@tool
def strategy_memo_specialist(query: str) -> str:
    """
    Create a strategy memo with findings based on the given query.

    Args:
        query: A query to create the strategy memo.

    Returns:
        The created strategy memo.
    """
    try:
        agent = Agent(
            system_prompt="""You are a specialized agent for creating strategy memos with findings.""",
            tools=[retrieve, http_request],
        )
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in strategy_memo_specialist: {str(e)}"
