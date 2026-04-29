# Task 013: Schema And Policy Validation

## Goal

Strengthen validation for PAPF records before expanding the benchmark.

## Create or update

- `src/papf/policy/validators.py`
- `src/papf/intent/validators.py` if needed
- `tests/test_policy_validation.py`

## Requirements

- Validate unique ids for rules, capabilities, data objects, and calls.
- Validate consent labels and decision labels.
- Detect policies that allow dangerous unrelated data without confirmation.
- Detect rules that reference unavailable environment objects.
- Preserve fail-closed behavior.

## Verification

- Add negative tests for malformed policies and ambiguous scopes.
