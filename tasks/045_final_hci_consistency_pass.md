# Task 045: Final HCI/Privacy Consistency Pass

Status: planned.

## Goal

Run a final consistency pass so every major paper claim aligns with the HCI/privacy framing and available evidence.

## Create or update

- `paper/papf_final.md`
- `docs/paper_plan.md`
- `CONTINUITY.md`

## Requirements

- Search the paper for unsupported terms:
  - "users understand",
  - "user-comprehensible",
  - "intuitive",
  - "clear to users",
  - "usable",
  - "trustworthy",
  - "privacy-preserving".
- Revise each unsupported phrase to either cite user-study results or reframe it as a design goal, hypothesis, or planned evaluation.
- Check the abstract, introduction, results, discussion, limitations, related work, and conclusion for consistent HCI/privacy positioning.
- Ensure the prototype trace evaluation is not presented as user-comprehension evidence.
- Update PDF export after final paper edits if requested.

## Verification

- Grep output for unsupported user-comprehension claims is reviewed and addressed.
- Claim-evidence map is updated for the HCI/privacy paper.
- Citation-like keys in the final paper all exist in `references.bib`.
- `CONTINUITY.md` records the final paper state and any skipped checks.
