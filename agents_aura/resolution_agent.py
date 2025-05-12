from agents import Agent, ModelSettings
from models.schemas import ResolutionAgentInput, ResolutionAgentOutput
from agents_aura.knowledge_base_tool import knowledge_base_tool_agent

resolution_agent = Agent(
    name="resolution_agent",
    instructions="""
You are the Resolution Agent responsible for resolving customer inquiries. Utilize the knowledge base to provide accurate responses, update ticket statuses, and escalate issues to specialized teams if needed. ALWAYS use the knowledge_base_tool to find information before responding. Communicate clearly with the customer and ensure SLAs are met. If no resolution is found, escalate to a specialist team and notify via Slack.
""",
    input_type=ResolutionAgentInput,
    output_type=ResolutionAgentOutput,
    tools=[knowledge_base_tool_agent.as_tool(
        tool_name="search_knowledge_base",
        tool_description="Search the knowledge base for relevant solutions."
    )],
    model_settings=ModelSettings(tool_choice="required"),
)
