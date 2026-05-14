# Task 031: Strengthen Privacy Framing

Status: implemented on 2026-05-14.

## Goal

Reframe PAPF around privacy harms and privacy principles rather than only security failures.

## Create or update

- `paper/papf_final.md`
- `docs/research_brief.md`
- `docs/research_gap.md`

## Requirements

- Add discussion of privacy harms:
  - over-collection,
  - secondary use,
  - cross-context leakage,
  - unauthorized disclosure,
  - prompt-injection-mediated data exfiltration,
  - loss of user agency.
- Connect PAPF to privacy principles:
  - data minimization,
  - purpose limitation,
  - contextual integrity,
  - user consent,
  - transparency and accountability.
- Keep the technical enforcement claim: privacy goals require runtime enforcement outside the LLM.
- Avoid generic AI ethics framing without measurable consequences.

## Verification

- Privacy harms appear before or alongside security examples in the paper.
- Each privacy principle maps to a PAPF mechanism or evaluation measure.
- The paper's thesis is understandable as a human-centered privacy contribution.
