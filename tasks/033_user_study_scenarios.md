# Task 033: Define User Study Scenarios

Status: planned.

## Goal

Create realistic privacy-sensitive scenarios for the user study and align each scenario with PAPF's benchmark labels.

## Create or update

- `docs/user_study_protocol.md`
- `docs/permission_prompt_examples.md`
- `paper/papf_final.md`
- optionally `paper/tables/user_study_scenarios.md`

## Requirements

- Define scenarios for:
  - reimbursement email summarization,
  - travel booking using email and browser data,
  - redacting sensitive information before sending a document,
  - updating account information from an email link,
  - detecting prompt injection from a webpage,
  - preventing cross-tool leakage from files into email or chat.
- For each scenario, specify:
  - user goal,
  - allowed data and tools,
  - disallowed data and tools,
  - privacy risk,
  - expected safe user decision.
- Keep scenarios synthetic and avoid real personal data.
- Use scenario wording suitable for non-expert participants.

## Verification

- Every scenario has an expected safe decision and a privacy risk.
- Scenarios cover at least email, files, browser content, and outbound communication.
- Scenario records can be mapped to existing or future benchmark traces.
