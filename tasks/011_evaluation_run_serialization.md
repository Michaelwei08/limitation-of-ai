# Task 011: Evaluation Run Serialization

## Goal

Write deterministic PAPF evaluation results to files under `experiments/runs/`.

## Create or update

- `src/papf/evaluation/serialization.py`
- `experiments/configs/default_email_files_browser.json`
- `tests/test_evaluation_serialization.py`

## Requirements

- Serialize metric rows as JSONL and CSV or document why only one format is chosen.
- Serialize audit summaries without raw personal payloads.
- Include run metadata: timestamp, git status summary if available, scenario ids, and metric schema version.
- Fail clearly on malformed output paths.

## Verification

- Run `python -m unittest discover -s tests -v`.
- Confirm output files are deterministic except timestamp metadata.
