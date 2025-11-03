# Team Lead Agentcore Hosting

This repository bootstraps a "Team Lead" agent that is hosted through the
[AWS Bedrock Agentcore Toolkit](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html)
and orchestrates specialist Strands agents as tools. The Team Lead is the agent
humans interact with, and it can delegate work to:

- **Contribution Margin Agent** – handles profitability questions.
- **Company Data Agent** – responds with internal company policy or knowledge.

The implementation currently provides mocked tool behavior so the hosting
workflow can be validated before wiring real Strands agents.

## Repository layout

```
src/
  agentcore_hosting/
    base.py                # Lightweight abstractions shared by agents
    config.py              # Environment-driven configuration loader
    runtime.py             # FastAPI runtime exposing /invoke and /health
    team_lead.py           # Team Lead agent orchestration logic
    tools/
      contribution_margin.py
      company_data.py
agentcore/
  manifest.yaml            # Skeleton manifest for Agentcore Toolkit deployments
.env.example               # Environment variables expected by the runtime
pyproject.toml             # Python project metadata and dependencies
```

## Getting started

1. **Install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

   Optionally install the Strands extras once you have access to the SDK:

   ```bash
   pip install -e .[strands]
   ```

2. **Configure environment variables**

   Copy `.env.example` to `.env` and populate the values:

   - `AWS_REGION` is required for Agentcore.
   - `AGENTCORE_HOST` and `AGENTCORE_PORT` control the HTTP runtime binding.
   - `STRANDS_API_KEY`, `STRANDS_WORKSPACE_ID`, and the tool agent IDs connect to
     Strands once those agents are provisioned.

3. **Local simulation**

   The Team Lead agent can be exercised locally using the simulation helper:

   ```bash
   python -m agentcore_hosting.team_lead
   ```

   Replace the placeholder keyword routing with a Strands planner once the SDK
   is integrated. The `ContributionMarginAgent` and `CompanyDataAgent` classes
   contain the hooks where Strands SDK calls should be added.

4. **Agentcore hosting**

   - Review `agentcore/manifest.yaml` and update the execution role ARN.
   - Start the Agentcore HTTP runtime locally (defaults to `0.0.0.0:8080`):

     ```bash
     python -m agentcore_hosting.runtime
     ```

   - The runtime exposes `GET /health` and `POST /invoke` endpoints that align
     with the Agentcore toolkit expectations.
   - Package the project for deployment (`pip install build && python -m build`)
     or containerize it following the toolkit documentation, wiring the
     `agentcore_hosting.runtime:app` ASGI application into the serving
     environment.

## Next steps

- Replace the mocked tool `run` methods with calls to live Strands agents using
  the agent IDs from your workspace.
- Enhance the `TeamLeadAgent.dispatch` logic to rely on Strands multi-agent
  planning or a dedicated orchestrator, following the
  [agent-to-agent guide](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agent-to-agent/).
- Extend session state management to track decision traces across turns and to
  share context with downstream Strands agents.
