# Task 028: Reframe Paper as HCI/Privacy Contribution

Status: implemented on 2026-05-14 for the first HCI/privacy front-matter pass.

## Goal

Revise the paper's primary contribution so PAPF is positioned as an HCI/privacy paper about user-understandable task-scoped consent for personal AI agents.

## Create or update

- `paper/papf_final.md`
- `docs/paper_outline.md`
- `docs/paper_plan.md`

## Requirements

- Rewrite the abstract, introduction, and contribution list around permission UX, consent burden, and privacy-preserving user choice.
- Emphasize PAPF as a permission and consent framework for personal AI agents rather than primarily as a systems/security benchmark.
- State the central claim carefully: consumer AI agents need externally enforced, task-scoped authority boundaries that users can understand and act on.
- Keep enforcement outside the LLM as a non-negotiable design invariant.
- Avoid claims that PAPF is deployment-ready, standardized, or empirically proven usable before a user study exists.

## Verification

- The abstract and introduction lead with HCI/privacy motivation before benchmark details.
- The contribution list includes architecture, prompt/consent design, and planned or measured privacy-usability evaluation.
- Unsupported claims about user comprehension are removed or explicitly framed as design goals.

## Implementation notes

- `paper/papf_final.md` now uses an HCI/privacy-oriented title, abstract, introduction, and contribution list.
- User comprehension is framed as a planned empirical question, not a current finding.
- Prototype trace results are described as secondary feasibility evidence.
