# Seed Benchmark Cases

This directory contains a small synthetic seed set for the Checkpointed Adaptive Reasoning task file. It is separate from the PAPF runtime benchmark code under `src/papf/`.

## Purpose

The cases test whether a long-running assistant can incorporate mid-task user input without discarding useful prior work. Each case describes a checkpoint state, a user update, expected reuse, expected invalidation, local replanning behavior, final answer properties, and forbidden behavior.

## Schema

Cases are stored in `cases.yaml`. Each case includes:

- `id`, `domain`, and `initial_task`
- `checkpoint_state` with current goal, constraints, completed and pending steps, assumptions, evidence, partial conclusions, uncertainties, and next action
- `mid_task_input` with user text and an input type
- expected reuse, invalidation, local replan, final answer properties, forbidden behavior, and metrics

## Relation To The Research Question

The seed set is designed around checkpointed continuation. A good system should classify the user update, preserve still-valid work, revise only affected assumptions or conclusions, and continue locally when possible. Some cases intentionally require stronger interruption behavior, such as aborts or topic switches.

## Future Evaluation Use

Future evaluators can compare naive baselines such as ignoring updates, hard restart, blind append, and summary-then-restart against checkpointed adaptive continuation. The current labels are intended as initial targets for reuse and invalidation checks, not validated ground truth.

## Current Limitations

The cases are synthetic and unvalidated. They do not include real private data, raw chain-of-thought, or experimental results. Human review is still needed to calibrate ambiguity, domain difficulty, and grading rubrics.
