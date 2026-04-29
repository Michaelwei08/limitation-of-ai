# Task 018: Synthetic Tool Runtime

## Goal

Add deterministic tool adapters that expose observed data touches for scoring.

## Create or update

- `src/papf/tools/`
- `tests/test_synthetic_tools.py`

## Requirements

- Implement synthetic email, files, and browser adapters.
- Ensure adapters only run after enforcement allows, narrows, or redacts a request.
- Return observed data refs and produced artifact refs.
- Do not integrate real accounts, browsers, filesystems, or APIs.

## Verification

- Tests prove blocked requests do not execute and allowed requests report observed refs.
