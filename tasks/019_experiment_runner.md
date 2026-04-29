# Task 019: Experiment Runner

## Goal

Create a command or script that runs PAPF and baselines over benchmark suites.

## Create or update

- `src/papf/cli.py` or `scripts/run_papf_experiment.py`
- `experiments/configs/`
- `tests/test_experiment_runner.py`

## Requirements

- Run selected suites deterministically.
- Write metrics, decisions, audit summaries, and config snapshots to `experiments/runs/`.
- Support PAPF, broad-access baseline, and prompt-only baseline modes.
- Fail clearly if config references missing cases.

## Verification

- Test a small run writes expected artifacts.
