# Task 012: PAPF Benchmark Loader

## Goal

Move from hard-coded fixture construction to file-backed PAPF benchmark cases.

## Create or update

- `benchmarks/papf_seed_cases/`
- `src/papf/benchmark/loader.py`
- `tests/test_benchmark_loader.py`

## Requirements

- Load task, environment, policy, and trace scenario records from YAML or JSON.
- Validate foreign-key-like references between tasks, data objects, policy rules, and traces.
- Keep synthetic data only.
- Preserve existing hard-coded fixture as a smoke-test fixture until loader coverage is complete.

## Verification

- Loader rejects missing data refs and invalid enum labels with clear errors.
