# Task 020: Results Tables And Figures

## Goal

Generate paper-ready tables and figures from experiment artifacts.

## Create or update

- `src/papf/evaluation/reporting.py`
- `paper/figures/`
- `paper/tables/`
- `tests/test_reporting.py`

## Requirements

- Generate main metrics table.
- Generate baseline comparison table.
- Generate failure-case summary table.
- Include provenance from run ids to source artifacts.
- Do not invent or manually enter experimental numbers.

## Verification

- Tests confirm reports are derived from run artifacts only.
