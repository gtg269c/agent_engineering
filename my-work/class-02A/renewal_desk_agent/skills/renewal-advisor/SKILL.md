---
name: renewal-advisor
description: Evaluates enterprise contract renewals, discount approval routing, renewal timelines, risk escalations, quotes, and approval briefs.
---

# Renewal Advisor

Provides policy-grounded guidance for WidgetWare enterprise customer renewals, commercial discount approvals, renewal process timelines, risk escalations, quote calculations, and approval briefs.

## When to use

Use this skill when responding to queries regarding:
- Enterprise contract renewal procedures and timeline milestones.
- Discount approval bands and required approver roles.
- Risk escalations, churn risk, non-standard contract term requests (such as auto-renewal removal), or regulated customer requirements.
- Formatting renewal approval briefs using the standard template.
- Quote calculations for dollar discounts and net ARR arithmetic.

## When not to use

Do not use this skill for:
- Unrelated product troubleshooting, general technical support, or user onboarding.
- Non-renewal new business sales or initial deal structuring.
- Requests for specific SOC 2 control IDs, compliance audit logs, or unauthorized 24-hour recovery time guarantees not supported by internal policy documents.

## Required inputs

Identify the necessary inputs provided in the user prompt:
- Customer name and current Annual Recurring Revenue (ARR).
- Requested discount percentage.
- Renewal date or days remaining until renewal.
- Risk factors (e.g., high churn risk, regulated customer status, non-standard term requests).

If required inputs for a calculation or brief are missing, ask the user to provide them rather than inventing values.

## Procedure

1. **Classify Query Type**: Determine whether the query asks about discount approvals, renewal timeline milestones, risk escalation, quote calculation, or brief generation.
2. **Selective Resource Loading**: Load only the minimum necessary L3 resource file(s) specified in the Resource routing map. Do not load irrelevant L3 files.
3. **Execute Quote Calculations**: If net ARR or dollar discount arithmetic is requested, run `scripts/calculate_quote.py` via script execution with the exact `--arr` and `--discount-percent` flags.
4. **Formulate Grounded Response**: Base all policy statements strictly on loaded L3 content. Cite every policy conclusion using exact relative file paths, for example `[Source: references/discount-policy.md]`.
5. **Handle Unsupported Claims**: If asked for facts not supported by the loaded resources (such as SOC 2 control IDs or SLA promises), state clearly that the supplied sources do not support the request and state the proper escalation path without fabricating details.

## Resource routing map

Map each question type to the minimum necessary relative file path:

- **Discount approval bands and thresholds**: `references/discount-policy.md`
- **Renewal process timeline and action milestones**: `references/renewal-process.md`
- **Risk escalation routes, non-standard legal terms, and churn risk**: `references/risk-escalation.md`
- **Official renewal brief structure and template**: `assets/renewal-brief-template.md`
- **Deterministic quote calculation script**: `scripts/calculate_quote.py`

## Output contract

- **Minimum Resources**: Load only the minimum required L3 resources for the query.
- **Citations**: Cite source policies for every conclusion using exact relative paths (e.g., `[Source: references/discount-policy.md]`).
- **Status Classification**: Strictly distinguish between **requested** (asked by customer), **routed** (submitted for review), and **approved** (confirmed by authorized approvers). Never treat requested terms as approved.

## Unsupported and missing-source behavior

When asked for unsupported items (e.g., SOC 2 control IDs or 24-hour recovery time guarantees) or missing policy information:
- State explicitly that the supplied sources do not support or establish the requested information.
- Cite the proper escalation route (e.g., Legal, Security, or Service Reliability as detailed in `references/risk-escalation.md`).
- Never invent, assume, or hallucinate approvals, control IDs, deadlines, or policy exceptions.

## Examples

### Positive

- **User**: "The renewal ARR is $92,000 and the requested discount is 12%. Which approval path is required?"
- **Action**: Load `references/discount-policy.md` only. State that a 12% discount requires VP Sales and Finance Business Partner approval. Cite `[Source: references/discount-policy.md]`.

### Negative

- **User**: "How do I reset my password on the WidgetWare admin portal?"
- **Action**: Do not invoke `renewal-advisor` skill, as this is a general support request outside renewal policy scope.

### Ambiguous

- **User**: "The customer is asking for a discount and contract change."
- **Action**: Identify that specific numbers (ARR, discount %) and specific contract terms requested are missing. Ask the user for clarification while referencing `references/discount-policy.md` and `references/risk-escalation.md` if minimum guidance is requested.
