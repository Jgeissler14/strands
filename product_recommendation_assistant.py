from strands import Agent, tool
from strands_tools import retrieve, http_request

@tool
def product_recommendation_assistant(query: str) -> str:
    """
    Handle product recommendation queries by suggesting appropriate products.

    Args:
        query: A product inquiry with user preferences

    Returns:
        Personalized product recommendations with reasoning
    """
    try:
        product_agent = Agent(
            system_prompt="""You are a specialized product recommendation assistant.
            Provide personalized product suggestions based on user preferences.""",
            tools=[retrieve, http_request, dialog],  # Tools for getting product data
        )
        # Implementation with response handling
        # ...
        return processed_response
    except Exception as e:
        return f"Error in product recommendation: {str(e)}"

@tool
def trip_planning_assistant(query: str) -> str:
    """
    Create travel itineraries and provide travel advice.

    Args:
        query: A travel planning request with destination and preferences

    Returns:
        A detailed travel itinerary or travel advice
    """
    try:
        travel_agent = Agent(
            system_prompt="""You are a specialized travel planning assistant.
            Create detailed travel itineraries based on user preferences.""",
            tools=[retrieve, http_request],  # Travel information tools
        )
        # Implementation with response handling
        # ...
        return processed_response
    except Exception as e:
        return f"Error in trip planning: {str(e)}"