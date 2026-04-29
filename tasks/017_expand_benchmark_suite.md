# Task 017: Expand Email + Files + Browser Suite

## Goal

Expand the first PAPF benchmark slice beyond the single reimbursement scenario.

## Create or update

- `benchmarks/papf_seed_cases/`
- `tests/test_seed_case_coverage.py`

## Requirements

- Add at least 12 PAPF seed cases across clean, temptation, attack, and recovery suites.
- Include email, files, browser, and at least one cross-tool exfiltration attempt.
- Include at least one redaction case and one confirmation-gated outbound action.
- Keep all content synthetic.

## Verification

- Coverage test confirms suite labels, attack labels, and policy outcomes are represented.
