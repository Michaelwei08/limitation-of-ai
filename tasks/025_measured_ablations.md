# Task 025: Measured PAPF Ablations

Status: implemented on 2026-04-30.

## Goal

Add deterministic ablation modes so the paper can report which PAPF components drive the utility/security tradeoff.

## Create or update

- `src/papf/ablation/`
- `src/papf/cli.py`
- `src/papf/evaluation/reporting.py`
- `tests/test_ablations.py`
- `paper/tables/ablation_results.{csv,md}`

## Requirements

- Run ablations over the same file-backed benchmark cases and scenario ids as the default experiment.
- Preserve metric schema compatibility or version it explicitly.
- Include at least:
  - no scope narrowing
  - no redaction evidence
  - no confirmation gating
  - no safer-alternative recovery
  - no audit completeness validation
- Report deltas against full PAPF for task success, safe partial success, over-access, false allow, unredacted disclosure, consent prompts, recovery quality, and auditability completeness.
- Do not manually enter ablation numbers in the paper.

## Verification

- Unit tests cover each ablation mode on at least one scenario.
- Reporting tests confirm ablation tables are derived from serialized run artifacts.
- Full test suite passes.
