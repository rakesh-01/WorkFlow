from agents import Agent, ModelSettings, function_tool
from models.schemas import PerformanceMonitoringInput, PerformanceMonitoringOutput, PerformanceMetric
from typing import List, Dict, Any
import random

@function_tool
def collect_ticket_metrics(ticket_updates: List[Dict[str, Any]], sla_targets: Dict[str, float]) -> dict:
    """
    Simulates collecting and analyzing ticket metrics for SLA adherence.
    Returns metrics and SLA breaches.
    """
    metrics = [
        {"metric_name": "avg_resolution_time", "value": random.uniform(1.0, 8.0)},
        {"metric_name": "customer_satisfaction", "value": random.uniform(80, 100)},
        {"metric_name": "sla_compliance", "value": random.uniform(0.7, 1.0)},
    ]
    sla_breaches = []
    alerts_sent = False
    dashboard_report = ""
    for metric in metrics:
        name = metric["metric_name"]
        value = metric["value"]
        if name in sla_targets and value < sla_targets[name]:
            sla_breaches.append(name)
            alerts_sent = True
    dashboard_report = f"Metrics: {metrics}, SLA Breaches: {sla_breaches}"
    return {
        "metrics": metrics,
        "sla_breaches": sla_breaches,
        "alerts_sent": alerts_sent,
        "dashboard_report": dashboard_report
    }

performance_monitoring_agent = Agent(
    name="performance_monitoring_agent",
    instructions="""
You are the Performance Monitoring Agent. Automatically collect and analyze data from the ticketing system and communication tools to track SLA adherence and performance metrics. Alert managers via Slack or dashboard notifications if KPIs fall below target thresholds. Maintain historical performance logs for trend analysis.
""",
    input_type=PerformanceMonitoringInput,
    output_type=PerformanceMonitoringOutput,
    tools=[collect_ticket_metrics],
    model_settings=ModelSettings(tool_choice="required"),
)
