from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any

class InquiryMetadata(BaseModel):
    channel: str = Field(description="Channel type: email, chat, or phone")
    customer_id: str = Field(description="Unique customer identifier")
    customer_history: Optional[str] = Field(description="Summary of customer history if available")
    model_config = ConfigDict(extra="forbid")

class TriageAgentInput(BaseModel):
    inquiry_text: str = Field(description="Raw inquiry text from the customer")
    metadata: InquiryMetadata
    model_config = ConfigDict(extra="forbid")

class TriageAgentOutput(BaseModel):
    category: str = Field(description="Issue category: technical, billing, or general")
    priority: str = Field(description="Priority level: High, Medium, or Low")
    confidence: float = Field(description="Confidence score (0.0 - 1.0)")
    ticket_metadata: InquiryMetadata
    clarification_needed: Optional[bool] = Field(description="Whether clarification is needed due to low confidence")
    model_config = ConfigDict(extra="forbid")

class ResolutionAgentInput(BaseModel):
    ticket: TriageAgentOutput
    inquiry_text: str = Field(description="Original inquiry text from the customer")
    model_config = ConfigDict(extra="forbid")

class ResolutionAgentOutput(BaseModel):
    resolution_reply: str = Field(description="Detailed reply for the customer")
    ticket_status: str = Field(description="Ticket status: resolved, escalated, pending further action")
    resolution_notes: Optional[str] = Field(description="Any notes about the resolution or escalation")
    escalation_channel: Optional[str] = Field(description="Channel used for escalation, if any (e.g., Slack)")
    model_config = ConfigDict(extra="forbid")

class PerformanceMetric(BaseModel):
    metric_name: str
    value: float
    model_config = ConfigDict(extra="forbid")

class PerformanceMonitoringInput(BaseModel):
    ticket_updates: List[Dict[str, Any]] = Field(description="List of ticket status updates and logs")
    sla_targets: Dict[str, float] = Field(description="SLA targets for metrics like response time, resolution time")
    model_config = ConfigDict(extra="forbid")

class PerformanceMonitoringOutput(BaseModel):
    metrics: List[PerformanceMetric]
    sla_breaches: List[str] = Field(description="List of SLA metrics that are below threshold")
    alerts_sent: bool = Field(description="Whether alerts were sent to managers")
    dashboard_report: str = Field(description="Formatted summary for dashboard display")
    model_config = ConfigDict(extra="forbid")

class RunTriageRequest(BaseModel):
    inquiry_text: str
    metadata: InquiryMetadata
    model_config = ConfigDict(extra="forbid")

class RunResolutionRequest(BaseModel):
    ticket: TriageAgentOutput
    inquiry_text: str
    model_config = ConfigDict(extra="forbid")

class RunPerformanceMonitoringRequest(BaseModel):
    ticket_updates: List[Dict[str, Any]]
    sla_targets: Dict[str, float]
    model_config = ConfigDict(extra="forbid")

class RunTriageResponse(BaseModel):
    triage_result: TriageAgentOutput
    model_config = ConfigDict(extra="forbid")

class RunResolutionResponse(BaseModel):
    resolution_result: ResolutionAgentOutput
    model_config = ConfigDict(extra="forbid")

class RunPerformanceMonitoringResponse(BaseModel):
    monitoring_result: PerformanceMonitoringOutput
    model_config = ConfigDict(extra="forbid")

