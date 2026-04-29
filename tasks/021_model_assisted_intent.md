# Task 021: Model-Assisted Intent Proposal

## Goal

Add an optional model-assisted intent proposal layer that remains non-authoritative.

## Create or update

- `src/papf/intent/proposer.py`
- `docs/model_assisted_boundaries.md`
- `tests/test_intent_proposer_contract.py`

## Requirements

- Keep the security-critical path deterministic.
- Treat model output only as a candidate `TaskIntent`.
- Validate schema before capability compilation.
- No model call is required for this task; use an interface and deterministic fake proposer.

## Verification

- Tests prove invalid proposals cannot mint capabilities.
