# Task 027: Create New HCI/Privacy Paper Outline

Status: implemented on 2026-05-14.

## Goal

Create a new outline for the HCI/privacy version of the PAPF paper.

## Create or update

- `docs/paper_outline.md`
- `docs/paper_plan.md`
- optionally `paper/papf_hci_outline.md`

## Requirements

- Use the target structure:
  1. Introduction
  2. Motivating Example
  3. Background and Privacy Risks
  4. PAPF Design Goals
  5. PAPF Architecture
  6. Permission Prompt Design
  7. Prototype Implementation
  8. User Study
  9. Prototype Trace Evaluation
  10. Results
  11. Discussion
  12. Limitations
  13. Related Work
  14. Conclusion
- For each section, define the paragraph-level message and evidence needed.
- Identify which sections require user-study results before final submission.
- Preserve the external-enforcement invariant throughout the outline.

## Verification

- The outline prioritizes HCI/privacy evaluation before prototype trace evaluation.
- Every section has a clear purpose and evidence source.
- The outline distinguishes implemented evidence from planned empirical work.

## Implementation notes

- `docs/paper_outline.md` now uses the 14-section HCI/privacy structure.
- `docs/paper_plan.md` now records HCI/privacy framing and the corrected revision order.
- `paper/papf_hci_outline.md` provides a compact section plan and claim-evidence guardrails.
