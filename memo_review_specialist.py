from strands import Agent, tool
from strands_tools import retrieve, http_request

@tool
def memo_review_specialist(query: str) -> str:
    """
    Review and approve a strategy memo.

    Args:
        query: A query to review and approve the strategy memo.

    Returns:
        The approval status of the strategy memo.
    """
    try:
        agent = Agent(
            system_prompt="""You are a specialized agent for reviewing and approving strategy memos.""",
            tools=[retrieve, http_request],
        )
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in memo_review_specialist: {str(e)}"
