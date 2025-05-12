from agents import Agent, function_tool, ModelSettings
from models.schemas import ResolutionAgentInput

@function_tool
def search_knowledge_base(query: str) -> dict:
    """
    Simulates searching the knowledge base (e.g., Confluence) for a solution.
    Args:
        query: The inquiry or ticket content to search for.
    Returns:
        Dictionary with a 'result' field containing the found information or empty if not found.
    """
    # In a real implementation, this would query an external KB system.
    if "password reset" in query.lower():
        return {"result": "To reset your password, click 'Forgot Password' on the login page."}
    return {"result": "No relevant knowledge base article found."}

knowledge_base_tool_agent = Agent(
    name="knowledge_base_tool_agent",
    instructions="You are the Knowledge Base Tool. Search the knowledge base for relevant solutions to the provided inquiry.",
    tools=[search_knowledge_base],
    model_settings=ModelSettings(tool_choice="required"),
)
