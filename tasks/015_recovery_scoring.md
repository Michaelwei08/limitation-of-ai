# Task 015: Recovery Scoring And Safer Alternatives

## Goal

Score whether the agent recovers from denial or narrowing through approved safer alternatives.

## Create or update

- `src/papf/evaluation/recovery.py`
- `src/papf/benchmark/models.py`
- `tests/test_recovery_scoring.py`

## Requirements

- Add structured safer-alternative definitions to benchmark tasks.
- Compute `recovery_quality`.
- Distinguish safe partial success from task failure.
- Avoid rewarding unsafe workarounds after denial.

## Verification

- Include tests for successful recovery, no recovery, and unsafe workaround.
