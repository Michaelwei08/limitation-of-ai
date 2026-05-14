# Task 026: Stronger External-Enforcement Baselines

Status: implemented on 2026-04-30 for coarse tool-scope and static-policy baselines. IFC-style and permission-hierarchy inference baselines remain future extensions.

## Goal

Add stronger non-PAPF baselines that enforce some external boundary, so PAPF is not compared only against broad access and prompt-only advice.

## Create or update

- `src/papf/baselines/`
- `experiments/configs/default_email_files_browser.json`
- `src/papf/evaluation/reporting.py`
- `tests/test_baselines.py`
- `paper/tables/stronger_baseline_results.{csv,md}`

## Requirements

- Keep the same synthetic benchmark records, tool adapters, and metrics.
- Add at least one implementable baseline first:
  - tool-scope delegated authorization baseline, or
  - static policy DSL enforcement baseline.
- If feasible, add later baselines:
  - information-flow-control style baseline,
  - permission-hierarchy inference baseline.
- Clearly distinguish implemented baseline numbers from planned future baselines.
- Do not claim equivalence to Progent, AgentSpec, Fides, or MiniScope unless the implementation actually matches their published mechanisms.

## Verification

- Tests show the stronger baseline blocks at least one attack that broad access allows.
- Tests show the stronger baseline still differs from PAPF in task-derived data scoping or recovery behavior.
- Reporting artifacts include provenance linking each baseline row to serialized decisions and audit summaries.
