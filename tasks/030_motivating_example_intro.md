# Task 030: Add Motivating User Scenario

Status: planned.

## Goal

Add a vivid user-facing scenario early in the introduction to motivate task-scoped authority, redaction, consent, and auditability.

## Create or update

- `paper/papf_final.md`
- `paper/tables/capability_compilation_example.md`

## Requirements

- Add a concrete reimbursement-email scenario near the start of the introduction.
- Include these behaviors:
  - the user asks the agent to summarize one reimbursement email,
  - the agent should not access unrelated tax documents,
  - the agent should not follow malicious webpage instructions,
  - the agent should not send private information without confirmation.
- Use the scenario to explain why broad app authorization is too coarse.
- Connect each risk to a PAPF mechanism: scoped capability, redaction evidence, confirmation gate, and audit trace.
- Keep the example non-technical and understandable to a non-expert reader.

## Verification

- The introduction contains one coherent motivating example before technical architecture details.
- The example uses synthetic, non-real personal data only.
- The example does not rely on chain-of-thought or model self-policing as enforcement.
