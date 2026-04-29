# Task 016: Baselines

## Goal

Implement comparable broad-access and prompt-only baselines in the same synthetic environment.

## Create or update

- `src/papf/baselines/`
- `tests/test_baselines.py`

## Requirements

- Broad-access baseline should execute requested traces without PAPF policy enforcement, while still recording observed data touches.
- Prompt-only baseline should simulate advisory policy text without external enforcement.
- Baselines must consume the same task, environment, and trace records as PAPF.
- Do not add LLM calls in this task.

## Verification

- Demonstrate that baseline traces can produce over-access or false-allow metrics that PAPF blocks.
