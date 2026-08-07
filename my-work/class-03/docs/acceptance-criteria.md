# Class 3 Acceptance Criteria

To successfully complete Class 3, the implementation must meet all of the following observable criteria:

1. **Configuration**:
   - `products.yaml`, `icp.yaml`, and `policies.yaml` exist in `config/` and load without errors.
   - At least two WidgetWare offerings are configured with target buyers and approved claims.
   - The ICP defines minimum employee threshold, preferred and excluded industries, preferred regions, and buying signals.
   - Policies explicitly define evidence classifications (`verified_fact`, `derived_fact`, `inference`, `unknown`, `conflict`), prohibited actions, and human approval boundaries.

2. **System Instructions**:
   - `src/widgetware_sdr/instructions.py` exposes `get_system_instructions() -> str`.
   - Instructions are explicit, non-vague, and state boundaries on evidence, prohibition of invented facts, outreach restrictions, and escalation rules.

3. **Context Builder**:
   - `src/widgetware_sdr/context_builder.py` exposes `build_context(account, objective, evidence, state=None) -> dict`.
   - Assembles and returns the 5 separate context layers (`system_instructions`, `business_context`, `task_context`, `retrieved_evidence`, `state`).
   - Account notes and retrieved text remain untrusted task data and cannot override system policies.
   - Missing configuration raises clear error.
   - Operates immutably on input objects.

4. **Scenario Fixtures & Verification**:
   - Scenarios exist in `tests/scenarios/` for: `qualified_account.yaml`, `unqualified_account.yaml`, `insufficient_evidence.yaml`, and `prompt_injection.yaml`.
   - All unit and scenario tests pass via `python -m pytest -v`.

5. **Negative Constraints (Out of Scope)**:
   - No Google ADK agent created.
   - No Gemini or LLM calls executed.
   - No web search, email sending, CRM modifications, database persistence, or deployment code.
