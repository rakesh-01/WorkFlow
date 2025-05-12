# Customer Support Multi-Agent System

This project implements a multi-agent FastAPI application for automated customer support workflows, including triage, resolution, and performance monitoring. It leverages OpenAI Agents SDK and advanced agent orchestration patterns (Routing, Agents-as-Tools, Deterministic Flow, Forcing Tool Use, Input/Output Guardrails, and Parallelization).

## Project Structure

- `main.py`: FastAPI application entry point and workflow orchestration.
- `models/schemas.py`: All Pydantic models for structured input/output.
- `agents_aura/`: Agent definitions and registry.
  - `triage_agent.py`: Automated classifier/triage agent.
  - `resolution_agent.py`: Human-augmented resolution agent using knowledge base as a tool.
  - `knowledge_base_tool.py`: Knowledge base search tool agent.
  - `performance_monitoring_agent.py`: Hybrid agent for SLA and performance monitoring.
  - `registry.py`: Central registry for all agents with validation.
  - `__init__.py`: Imports all agents for easy access.
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation.
- `.env.example`: Example environment variables file.

## API Endpoints

### 1. POST `/run_triage/`
**Description:** Run the Triage Agent to classify and prioritize an inquiry.
**Request Body:**
```
{
  "inquiry_text": "I can't log in to my account.",
  "metadata": {
    "channel": "email",
    "customer_id": "12345",
    "customer_history": "VIP, 2 prior tickets"
  }
}
```
**Response:**
```
{
  "triage_result": {
    "category": "technical",
    "priority": "High",
    "confidence": 0.92,
    "ticket_metadata": { ... },
    "clarification_needed": false
  }
}
```

### 2. POST `/run_resolution/`
**Description:** Run the Resolution Agent to resolve a ticket using the knowledge base.
**Request Body:**
```
{
  "ticket": { ...TriageAgentOutput... },
  "inquiry_text": "I can't log in to my account."
}
```
**Response:**
```
{
  "resolution_result": {
    "resolution_reply": "To reset your password, click 'Forgot Password'...",
    "ticket_status": "resolved",
    "resolution_notes": "Used KB article.",
    "escalation_channel": null
  }
}
```

### 3. POST `/run_performance_monitoring/`
**Description:** Run the Performance Monitoring Agent to collect and analyze SLA metrics.
**Request Body:**
```
{
  "ticket_updates": [ ... ],
  "sla_targets": { "avg_resolution_time": 4.0, "sla_compliance": 0.9 }
}
```
**Response:**
```
{
  "monitoring_result": {
    "metrics": [ ... ],
    "sla_breaches": [ ... ],
    "alerts_sent": true,
    "dashboard_report": "Metrics: ..."
  }
}
```

### 4. POST `/run_agent/`
**Description:** Run any agent by name with a query (for advanced use).
**Request Body:**
```
{
  "agent_name": "triage_agent",
  "query": { ... }
}
```
**Response:**
```
{
  "agent_name": "triage_agent",
  "input_query": { ... },
  "output": { ... }
}
```

## Patterns Implemented
- **Routing Pattern:** Triage Agent routes tickets to Resolution Agent.
- **Agents-as-Tools Pattern:** Resolution Agent uses Knowledge Base as a tool.
- **Deterministic Flow Pattern:** Sequential, validated steps in Resolution and Monitoring.
- **Forcing Tool Use Pattern:** Resolution Agent always consults the Knowledge Base.
- **Input/Output Guardrails Pattern:** Ensures compliance and data integrity.
- **Parallelization Pattern:** Performance Monitoring gathers metrics concurrently.

## Setup
1. Copy `.env.example` to `.env` and fill in your environment variables (e.g., `OPENAI_API_KEY`).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the server:
   ```
   uvicorn main:app --reload --port 8000
   ```

## Environment Variables
See `.env.example` for required variables.

## Notes
- All agents are defined in `agents_aura/` and registered in `agents_aura/registry.py`.
- All models are defined in `models/schemas.py`.
- This system is designed for extensibility and compliance with OpenAI Agents SDK best practices.
