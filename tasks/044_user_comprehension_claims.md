# Task 044: Revise User-Comprehension Claims

Status: planned.

## Goal

Remove or weaken unsupported claims that PAPF is already user-comprehensible.

## Create or update

- `paper/papf_final.md`
- `paper/papf_draft.md`
- `docs/paper_plan.md`
- `docs/user_study_protocol.md`

## Requirements

- Search for terms such as "users understand", "user-comprehensible", "intuitive", "clear to users", and "easy to understand".
- Replace unsupported claims with careful language:
  - "PAPF is designed to support user comprehension."
  - "We evaluate whether users can understand and act on PAPF-style prompts."
  - "User comprehension remains an empirical question."
- Preserve claims that are explicitly framed as goals, hypotheses, or planned evaluation items.
- Do not introduce user-study statistics unless actual participant data exists.

## Verification

- Grep results show no unsupported comprehension claims remain.
- Abstract, introduction, discussion, and conclusion use evidence-bounded phrasing.
- Any user-comprehension claim has either a citation, a study result, or explicit design-goal language.
