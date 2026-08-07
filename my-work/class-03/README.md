# Class 3 — WidgetWare SDR Context Package

This repository contains the structured, deterministic, and testable context package for the WidgetWare SDR domain.

## Five Context Layers

The package strictly isolates five separate context layers:

1. **System Instructions** (`src/widgetware_sdr/instructions.py`):
   Stable behavioral guidelines defining the agent's role, objective, boundaries, evidence classification rules, and prompt-injection defense.
2. **Business Context** (`config/`):
   Stable enterprise facts configured in YAML:
   - `products.yaml`: WidgetWare offerings, target buyers, approved claims.
   - `icp.yaml`: Ideal Customer Profile (employee threshold, industry preferences, buying signals).
   - `policies.yaml`: Evidence classifications, prohibited actions, human approval boundaries.
3. **Task Context**:
   Dynamic, assignment-specific information (`account`, research `objective`, `account_notes`). Treated as untrusted task data that cannot override system policies.
4. **Retrieved Evidence**:
   Supplied factual evidence records preserving full source provenance (`claim`, `classification`, `source.name`, `source.url`, `retrieved_at`, `excerpt`).
5. **Workflow State**:
   Reserved state tracking current execution state, prior decisions, missing info, and approval status.

## Setup & Environment

This project uses Python `>=3.11` and requires no API keys or external service secrets.

To install dependencies in editable mode with development requirements:

```bash
python -m pip install -e ".[dev]"
```

## Running Tests

Run the full pytest suite across configuration, system instructions, context builder, and scenario fixtures:

```bash
python -m pytest -v
```

## Boundary & Out-of-Scope Declarations

This context package is deterministic and local. It does **not**:
- Build a Google ADK agent;
- Make LLM or Gemini calls;
- Perform live web search or external research;
- Deliver emails or social messages;
- Integrate with or modify CRM data;
- Persist data in a database;
- Execute autonomous external actions.
