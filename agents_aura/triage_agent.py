from agents import Agent, ModelSettings
from models.schemas import TriageAgentInput, TriageAgentOutput

triage_agent = Agent(
    name="triage_agent",
    instructions="""
You are the Triage Agent. Use NLP to analyze the inquiry text, identify the issue category (technical, billing, general), assign a priority level based on pre-defined rules and customer history, then route the ticket to the appropriate queue. If your confidence level is below 80% for any attribute, request clarification before proceeding. Always output a structured JSON object with: category, priority, confidence (0.0-1.0), and ticket metadata. If confidence is below 0.8, set clarification_needed to true.
""",
    input_type=TriageAgentInput,
    output_type=TriageAgentOutput,
)
