# Task 004: PAPF System Design Plan

## Goal

Refine the PAPF system design into a modular implementation plan.

This task should create an architecture plan, not code.

## Read first

- `AGENTS.md`
- `CONTINUITY.md`
- `docs/system_design.md`
- `docs/benchmark_spec.md`
- `docs/benchmark_schema_plan.md` if it exists
- `docs/research_gap.md` if it exists

## Create or update

- Update `docs/system_design.md`
- Create `docs/implementation_plan.md`
- Update `CONTINUITY.md` only if the project state materially changes

## System premise

PAPF should not let the LLM be the final authority for permission enforcement.

The system may allow the LLM to propose:

- task intent
- candidate capabilities
- user-facing explanations
- recovery suggestions

But final enforcement should be outside the LLM through explicit policies and runtime checks.

## Required architecture layers

Refine these layers:

1. Task intent analysis
2. Capability compiler
3. Runtime policy enforcement point
4. Risk-adaptive consent
5. Audit and traceability
6. Evaluation harness

## `docs/implementation_plan.md` format

Include:

1. Minimal viable prototype
2. Main modules
3. Data structures needed
4. Interfaces between modules
5. What should be rule-based first
6. What may later use an LLM
7. Testing strategy
8. Risks and failure modes
9. Milestones

## Suggested module boundaries

Use these as planning targets:

- `src/papf/intent/`
- `src/papf/capabilities/`
- `src/papf/policy/`
- `src/papf/enforcement/`
- `src/papf/audit/`
- `src/papf/benchmark/`
- `src/papf/evaluation/`

Do not create implementation code yet unless necessary for placeholders.

## Requirements

- No production integrations.
- No real personal data.
- No credentials.
- No hidden LLM-based permission override.
- No code files unless placeholder files are necessary.
- Keep the plan implementable by future Codex tasks.

## Final output

Report:

1. Architecture clarified
2. Proposed modules
3. First implementation milestone
4. Main risks
5. Whether `CONTINUITY.md` was updated