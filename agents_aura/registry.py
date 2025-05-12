from typing import Dict
from agents import Agent
from agents_aura.triage_agent import triage_agent
from agents_aura.resolution_agent import resolution_agent
from agents_aura.knowledge_base_tool import knowledge_base_tool_agent
from agents_aura.performance_monitoring_agent import performance_monitoring_agent

def validate_agent(agent: Agent, name: str) -> None:
    if not hasattr(agent, "output_type") or agent.output_type is None:
        raise ValueError(f"Agent {name} is missing output_type which is required")

validate_agent(triage_agent, "triage_agent")
validate_agent(resolution_agent, "resolution_agent")
validate_agent(knowledge_base_tool_agent, "knowledge_base_tool_agent")
validate_agent(performance_monitoring_agent, "performance_monitoring_agent")

AGENT_REGISTRY: Dict[str, Agent] = {
    "triage_agent": triage_agent,
    "resolution_agent": resolution_agent,
    "knowledge_base_tool_agent": knowledge_base_tool_agent,
    "performance_monitoring_agent": performance_monitoring_agent,
}

def get_agent(name: str) -> Agent:
    if name not in AGENT_REGISTRY:
        raise ValueError(f"Agent {name} not found in registry")
    return AGENT_REGISTRY[name]
