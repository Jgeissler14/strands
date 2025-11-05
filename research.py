from strands import Agent, tool
from strands_tools import retrieve, http_request

# Define a specialized system prompt
RESEARCH_ASSISTANT_PROMPT = """
You are a specialized research assistant. Focus only on providing
factual, well-sourced information in response to research questions.
Always cite your sources when possible.
"""

@tool
def research_assistant(query: str) -> str:
    """
    Process and respond to research-related queries.

    Args:
        query: A research question requiring factual information

    Returns:
        A detailed research answer with citations
    """
    try:
        # Strands Agents SDK makes it easy to create a specialized agent
        research_agent = Agent(
            system_prompt=RESEARCH_ASSISTANT_PROMPT,
            tools=[retrieve, http_request]  # Research-specific tools
        )

        # Call the agent and return its response
        response = research_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"