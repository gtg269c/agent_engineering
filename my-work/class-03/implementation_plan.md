# Implementation Plan — Class 3 WidgetWare SDR Context Package

Construct a structured, deterministic, and testable context package for the WidgetWare SDR domain to serve as context input for future agents, adhering strictly to `SPEC.md` boundaries.

## User Review Required

> [!IMPORTANT]
> **Strict Out-of-Scope Enforcement**: No LLM calls (Gemini/OpenAI/etc.), no Google ADK agent, no live web search, no CRM integrations, no email/messaging delivery, and no database persistence will be introduced. All context loading is purely deterministic.

> [!NOTE]
> No files in the workspace have been created, modified, or deleted during this planning step.

## Workspace Inspection & Findings

### 1. Existing Files in Workspace
- `README.md` — Minimal setup instructions placeholder
- `SPEC.md` — Complete Class 3 specification (source of truth)
- `LAB.md` — Step-by-step guidance for the lab
- `STARTER_CONTENTS.md` — Inventory of starter files and targets
- `pyproject.toml` — Package configuration with `PyYAML` and `pytest` dependencies
- `src/widgetware_sdr/__init__.py` — Package docstring starter
- `tests/unit/test_starter.py` — Smoke test verifying module import
- `config/.gitkeep`, `docs/.gitkeep`, `tests/scenarios/.gitkeep` — Directory placeholders

### 2. SPEC.md Requirements Summary
`SPEC.md` requires constructing a structured context package composed of 5 distinct context layers:
1. **System Instructions** (`src/widgetware_sdr/instructions.py`): Observable, inspectable agent guidelines.
2. **Business Context** (`config/products.yaml`, `config/icp.yaml`, `config/policies.yaml`): Company offerings, target profile fit, safety and approval policies.
3. **Task Context**: Dynamic account data, target account objective, account notes.
4. **Retrieved Evidence**: Evidence records with full provenance (`claim`, `classification`, `source.name`, `source.url`, `retrieved_at`, `excerpt`).
5. **Workflow State**: Execution state reserved for future workflow engines.

Additionally, scenario fixtures in YAML and unit/scenario test coverage must validate context assembly, untrusted data isolation, prompt-injection defense, and evidence provenance.

### 3. Required Dependencies
- **Runtime**: Python `>=3.11`, `PyYAML>=6.0,<7.0`
- **Development & Testing**: `pytest>=8.0,<9.0`
- **Standard Library**: `pathlib`, `typing`, `copy`
- *No LLM or agent SDKs required.*

---

## Proposed Changes

### Configuration Layer (`config/`)

#### [NEW] [products.yaml](file:///c:/projects/learn/agent_engineering/my-work/class-03/config/products.yaml)
- Defines company background and offerings ("Plant Operations Platform", "Industrial AI Accelerator").
- Specifies target buyers, approved value claims, and boundary limits (no invented customer names, no unsupported numerical claims).

#### [NEW] [icp.yaml](file:///c:/projects/learn/agent_engineering/my-work/class-03/config/icp.yaml)
- Defines ideal customer criteria: company size threshold (e.g. 250+ employees), preferred industries (manufacturing, industrial automation), excluded industries, preferred regions, buying signals, and required account fields.

#### [NEW] [policies.yaml](file:///c:/projects/learn/agent_engineering/my-work/class-03/config/policies.yaml)
- Defines 5 evidence classifications (`verified_fact`, `derived_fact`, `inference`, `unknown`, `conflict`).
- Defines prohibited actions (inventing facts, email sending, CRM modification, pricing commitments).
- Explicitly enforces human approval for any external outreach or CRM changes.

---

### Documentation Layer (`docs/` & Root)

#### [NEW] [.env.example](file:///c:/projects/learn/agent_engineering/my-work/class-03/.env.example)
- Documents environment setup (noting no API keys or secrets are required for Class 3).

#### [NEW] [widgetware-business-brief.md](file:///c:/projects/learn/agent_engineering/my-work/class-03/docs/widgetware-business-brief.md)
- Summarizes WidgetWare's market position, value proposition, and SDR workflow boundaries.

#### [NEW] [acceptance-criteria.md](file:///c:/projects/learn/agent_engineering/my-work/class-03/docs/acceptance-criteria.md)
- Documents explicit verification criteria from `SPEC.md` Section 16.

#### [MODIFY] [README.md](file:///c:/projects/learn/agent_engineering/my-work/class-03/README.md)
- Updated with an explanation of the 5 context layers, setup commands, and test running instructions.

---

### Source Code Layer (`src/widgetware_sdr/`)

#### [NEW] [instructions.py](file:///c:/projects/learn/agent_engineering/my-work/class-03/src/widgetware_sdr/instructions.py)
- Implements `get_system_instructions() -> str`.
- Returns clear, observable instructions defining agent role, boundaries, evidence classification rules, prohibition of invented facts/outreach, and prompt-injection resistance.

#### [NEW] [context_builder.py](file:///c:/projects/learn/agent_engineering/my-work/class-03/src/widgetware_sdr/context_builder.py)
- Implements `build_context(account: dict, objective: str, evidence: list[dict], state: dict | None = None) -> dict`.
- Loads `products.yaml`, `icp.yaml`, `policies.yaml` deterministically from `config/`.
- Assembles and returns a dict with exact 5 context keys (`system_instructions`, `business_context`, `task_context`, `retrieved_evidence`, `state`).
- Strictly isolates untrusted task data (account notes, user prompts) from system instructions and business policies.
- Preserves evidence provenance, treats missing info as `unknown`, and operates immutably on inputs.

---

### Scenario Fixtures & Tests Layer (`tests/`)

#### [NEW] [qualified_account.yaml](file:///c:/projects/learn/agent_engineering/my-work/class-03/tests/scenarios/qualified_account.yaml)
- Scenario fixture matching ICP criteria (manufacturing, 500 employees, plant modernization signal).

#### [NEW] [unqualified_account.yaml](file:///c:/projects/learn/agent_engineering/my-work/class-03/tests/scenarios/unqualified_account.yaml)
- Scenario fixture failing ICP criteria (e.g. excluded industry or under size threshold).

#### [NEW] [insufficient_evidence.yaml](file:///c:/projects/learn/agent_engineering/my-work/class-03/tests/scenarios/insufficient_evidence.yaml)
- Scenario fixture missing critical fields (unknown employee count / region / buying signals).

#### [NEW] [prompt_injection.yaml](file:///c:/projects/learn/agent_engineering/my-work/class-03/tests/scenarios/prompt_injection.yaml)
- Scenario fixture containing malicious instructions in account notes attempting to override policy or force automated email sending.

#### [NEW] [test_context_builder.py](file:///c:/projects/learn/agent_engineering/my-work/class-03/tests/unit/test_context_builder.py)
- Comprehensive pytest suite covering:
  - Configuration structure and content validation.
  - Instruction content and constraint validation.
  - 5-layer context assembly and immutability.
  - Untrusted content and prompt-injection defense.
  - Scenario fixture loading and validation across all 4 required scenarios.

---

## Verification Plan

### Automated Tests
- Execute full test suite via pytest:
  ```bash
  python -m pytest -v
  ```
- Verify zero failures across configuration, instructions, context builder, and all 4 scenario tests.

### Manual Verification
- Review generated context objects for strict 5-layer separation.
- Inspect `git status` and `git diff` to ensure no out-of-scope files or changes exist.
