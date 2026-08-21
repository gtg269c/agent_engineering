# Student Submission

Name:  Student
Date:  2026-08-20
Commit hash:  HEAD

## 1. Baseline observations

What was visible at L1?

> At L1, only the skill name (`renewal-advisor`) and description were visible to the model via the skill toolset catalog. Before editing, the placeholder description was `TODO - replace this with accurate L1 routing metadata without policy details.`, which provided no meaningful capability triggers or guidance to the model. No policy thresholds, approval bands, or specific resource contents were visible at L1.

What weaknesses did you observe before completing `SKILL.md`?

> 1. The L1 description was a placeholder (`TODO`), making skill routing ambiguous or ineffective.
> 2. The L2 body contained only `TODO` headers without any procedures, minimum resource loading contracts, or citation requirements.
> 3. The agent lacked clear mapping rules linking specific query types to exact L3 file paths, leading to ungrounded or incomplete answers.
> 4. There was no explicit safety rule for unsupported queries (like SOC 2 control IDs or SLA commitments), risking hallucination.

## 2. Trace evidence

| Case | L1 observed | L2 loaded? | Exact L3 paths loaded | Irrelevant paths avoided | Result |
| --- | --- | --- | --- | --- | --- |
| A | `renewal-advisor` skill description | Yes | `references/discount-policy.md` | `renewal-process.md`, `risk-escalation.md`, `renewal-brief-template.md`, `calculate_quote.py` | Correctly identified VP Sales & Finance Business Partner approval for 12% discount with proper citation. |
| B | `renewal-advisor` skill description | Yes | `references/renewal-process.md` | `discount-policy.md`, `risk-escalation.md`, `renewal-brief-template.md`, `calculate_quote.py` | Correctly advised holding internal account review for 75-day timeline (90-61 days band). |
| C | `renewal-advisor` skill description | Yes | `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md` | `renewal-brief-template.md`, `calculate_quote.py` | Combined CRO/Finance Director approval (18%), Executive sponsor/Renewal Desk (10 days/high risk), and Legal/Security routes. |
| D | `renewal-advisor` skill description | Yes | `assets/renewal-brief-template.md`, `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md` | `calculate_quote.py` | Formatted official brief template using exact status words (requested, routed, approved) without fabricating missing fields. |
| E | `renewal-advisor` skill description | Yes | `scripts/calculate_quote.py`, `references/discount-policy.md` | `renewal-process.md`, `risk-escalation.md`, `renewal-brief-template.md` | Executed deterministic calculator script ($11,040.00 discount / $80,960.00 net ARR) and stated VP Sales/Finance BP approval. |
| F | `renewal-advisor` skill description | Yes | `references/risk-escalation.md` | `discount-policy.md`, `renewal-process.md`, `renewal-brief-template.md`, `calculate_quote.py` | Stated that supplied sources do not support SOC 2 control IDs/24h recovery promise and cited Legal & Service Reliability escalation route. |

## 3. Evaluation scores

Score each item 0 or 1.

| Eval ID | Selection | Minimum resources | Correct facts | Citation | Safe handling | Total /5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| L1-01 | 1 | 1 | 1 | 1 | 1 | 5/5 |
| L3-01 | 1 | 1 | 1 | 1 | 1 | 5/5 |
| L3-02 | 1 | 1 | 1 | 1 | 1 | 5/5 |
| L3-03 | 1 | 1 | 1 | 1 | 1 | 5/5 |
| L3-04 | 1 | 1 | 1 | 1 | 1 | 5/5 |
| SAFE-01 | 1 | 1 | 1 | 1 | 1 | 5/5 |

## 4. Reflection

### Why is policy detail stored at L3 instead of L1?

> Storing policy detail at L3 keeps L1 metadata compact, allowing the LLM to make fast, accurate skill-selection decisions without clogging the root prompt with detailed rules. Detailed L3 resources are loaded selectively and progressively only when specific evidence is needed, minimizing token consumption, reducing latency, and preventing context pollution.

### What is the difference between a skill and a tool in this lab?

> A **skill** is a higher-level package containing domain guidance, procedural instructions (L2), quality contracts, and organized resources (L3). A **tool** is an executable capability (such as `load_skill_resource` or `run_skill_script` / Python execution engine) that the agent calls to inspect files or execute code during workflow execution.

### Give one example where loading fewer resources improves the agent.

> In Case A (evaluating a 12% discount on $92,000 ARR), loading only `references/discount-policy.md` avoids pulling in timeline milestones from `references/renewal-process.md` or security escalations from `references/risk-escalation.md`. This focused context keeps the response crisp, lowers prompt cost/latency, and eliminates the risk of hallucinating irrelevant policy constraints.

### What failure could occur if `SKILL.md` names resources vaguely instead of using exact paths?

> If `SKILL.md` provides vague resource names (e.g. "discount policy doc"), the agent may guess file paths, attempt to load non-existent files, trigger repeated tool errors, or fail to find the required policy altogether, leading to ungrounded responses or outright failure.

## 5. Test output

```text
.......                                                                  [100%]
7 passed in 0.33s
```
