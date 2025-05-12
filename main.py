from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import uvicorn
import asyncio
import json
import traceback
from typing import Any

from models.schemas import (
    TriageAgentInput, TriageAgentOutput, RunTriageRequest, RunTriageResponse,
    ResolutionAgentInput, ResolutionAgentOutput, RunResolutionRequest, RunResolutionResponse,
    PerformanceMonitoringInput, PerformanceMonitoringOutput, RunPerformanceMonitoringRequest, RunPerformanceMonitoringResponse
)
from agents import Runner
from agents_aura.registry import AGENT_REGISTRY

app = FastAPI(
    title="Customer Support Multi-Agent System",
    description="Automated triage, resolution, and performance monitoring for customer support workflows.",
    version="1.0.0"
)

@app.post("/run_triage/", response_model=RunTriageResponse)
async def run_triage(request: RunTriageRequest):
    try:
        triage_agent = AGENT_REGISTRY["triage_agent"]
        triage_input = TriageAgentInput(inquiry_text=request.inquiry_text, metadata=request.metadata)
        result = await Runner.run(triage_agent, triage_input)
        try:
            triage_output = result.final_output_as(TriageAgentOutput)
        except Exception as e:
            print(f"TriageAgentOutput parsing error: {e}")
            if isinstance(result.final_output, dict):
                triage_output = TriageAgentOutput(**result.final_output)
            else:
                triage_output = TriageAgentOutput(
                    category="general", priority="Low", confidence=0.5, ticket_metadata=request.metadata, clarification_needed=True
                )
        return RunTriageResponse(triage_result=triage_output)
    except Exception as e:
        print(f"Error in run_triage: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Triage error: {str(e)}")

@app.post("/run_resolution/", response_model=RunResolutionResponse)
async def run_resolution(request: RunResolutionRequest):
    try:
        resolution_agent = AGENT_REGISTRY["resolution_agent"]
        resolution_input = ResolutionAgentInput(ticket=request.ticket, inquiry_text=request.inquiry_text)
        result = await Runner.run(resolution_agent, resolution_input)
        try:
            resolution_output = result.final_output_as(ResolutionAgentOutput)
        except Exception as e:
            print(f"ResolutionAgentOutput parsing error: {e}")
            if isinstance(result.final_output, dict):
                resolution_output = ResolutionAgentOutput(**result.final_output)
            else:
                resolution_output = ResolutionAgentOutput(
                    resolution_reply="Unable to resolve at this time.",
                    ticket_status="pending further action",
                    resolution_notes="Parsing error.",
                    escalation_channel=None
                )
        return RunResolutionResponse(resolution_result=resolution_output)
    except Exception as e:
        print(f"Error in run_resolution: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Resolution error: {str(e)}")

@app.post("/run_performance_monitoring/", response_model=RunPerformanceMonitoringResponse)
async def run_performance_monitoring(request: RunPerformanceMonitoringRequest):
    try:
        performance_agent = AGENT_REGISTRY["performance_monitoring_agent"]
        monitoring_input = PerformanceMonitoringInput(ticket_updates=request.ticket_updates, sla_targets=request.sla_targets)
        result = await Runner.run(performance_agent, monitoring_input)
        try:
            monitoring_output = result.final_output_as(PerformanceMonitoringOutput)
        except Exception as e:
            print(f"PerformanceMonitoringOutput parsing error: {e}")
            if isinstance(result.final_output, dict):
                monitoring_output = PerformanceMonitoringOutput(**result.final_output)
            else:
                monitoring_output = PerformanceMonitoringOutput(
                    metrics=[], sla_breaches=["unknown"], alerts_sent=False, dashboard_report="Parsing error."
                )
        return RunPerformanceMonitoringResponse(monitoring_result=monitoring_output)
    except Exception as e:
        print(f"Error in run_performance_monitoring: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Performance monitoring error: {str(e)}")

@app.post("/run_agent/")
async def run_agent(agent_name: str, query: Any):
    agent = AGENT_REGISTRY.get(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found.")
    try:
        result = await Runner.run(agent, query)
        return {"agent_name": agent_name, "input_query": query, "output": result.final_output}
    except Exception as e:
        print(f"Error running agent {agent_name}: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

if __name__ == "__main__":
    print("Starting FastAPI server. For development, run with: uvicorn main:app --reload --port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
