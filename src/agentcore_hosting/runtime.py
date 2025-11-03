"""HTTP runtime for AWS Bedrock Agentcore toolkit hosting."""
from __future__ import annotations

from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .config import AgentcoreConfig
from .team_lead import TeamLeadAgent


async def handle_turn(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle a single Agentcore invocation event.

    Agentcore invokes the runtime with JSON payloads that include the current
    session state and the latest user input. We wire the Team Lead agent and
    return a dictionary that conforms to the toolkit contract. The structure is
    intentionally explicit so teams integrating with Agentcore can quickly map
    fields to their infrastructure.
    """

    config = AgentcoreConfig.load()

    session_state = event.get("session_state", {})
    user_input = event["input"]

    agent = TeamLeadAgent.build_default()
    response_text = await agent.dispatch(user_input, session_state)

    session_state.setdefault("metadata", {})
    session_state["metadata"].update({
        "aws_region": config.aws_region,
        "agent_id": config.agent_id,
    })

    return {
        "session_state": session_state,
        "response": {
            "message": response_text,
        },
    }


app = FastAPI(title="Team Lead Agentcore Runtime")


@app.get("/health")
async def health() -> Dict[str, str]:
    """Return a simple health response used by Agentcore readiness probes."""

    return {"status": "ok"}


@app.post("/invoke")
async def invoke(request: Request) -> JSONResponse:
    """Primary Agentcore invocation endpoint."""

    payload = await request.json()
    response = await handle_turn(payload)
    return JSONResponse(content=response)


def run() -> None:
    """Run the HTTP server using the configured host and port."""

    config = AgentcoreConfig.load()
    uvicorn.run(
        "agentcore_hosting.runtime:app",
        host=config.host,
        port=config.port,
        reload=False,
    )


def main() -> None:
    """Synchronous entry point for CLI execution."""

    run()


__all__ = ["app", "handle_turn", "health", "invoke", "run", "main"]


if __name__ == "__main__":  # pragma: no cover - manual execution helper
    main()
