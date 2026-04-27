# Task 002: Research Gap and Positioning

## Goal

Use the existing project docs and the seed related-work map to clarify the PAPF research gap and possible paper positioning.

This task should produce a research planning document, not a final paper section.

## Read first

- `AGENTS.md`
- `CONTINUITY.md`
- `docs/research_brief.md`
- `docs/related_work.md`
- `docs/lit_matrix.md` if it exists
- `docs/benchmark_spec.md`
- `docs/system_design.md`

## Create or update

- Create `docs/research_gap.md`
- Update `docs/research_brief.md` if needed
- Update `CONTINUITY.md` only if the project state materially changes

## Main question

Clarify why PAPF may be a distinct research contribution.

The likely gap is:

Existing work studies prompt injection, tool-using agent safety, privacy leakage, permissions, or usability, but does not fully combine:

1. task-scoped least-privilege capability compilation,
2. runtime enforcement outside the LLM,
3. user-comprehensible permission boundaries for non-expert consumer users,
4. evaluation across both task success and privacy/security failures.

## `docs/research_gap.md` format

Use these sections:

1. Working thesis
2. What existing work already covers
3. What existing work does not fully cover
4. PAPF's proposed contribution
5. Risk of overclaiming
6. Possible venue framings
7. Strongest first-paper strategy
8. Claims that require more evidence

## Venue positioning

Compare these possible framings:

- ML benchmark / datasets framing
- security systems framing
- usable privacy / HCI framing
- AI governance / FAccT framing

For each, include:

- what the paper would emphasize
- what evidence would be needed
- why it may or may not fit this project

## Requirements

- Do not claim novelty as fact.
- Use wording like "possible gap", "working hypothesis", or "candidate contribution" unless the literature supports a stronger claim.
- Do not invent citations.
- If related work is missing, mark it as `TODO`.
- Do not write the final paper introduction yet.

## Final output

Report:

1. Main gap identified
2. Best venue framing for first paper
3. Weakest evidence areas
4. Whether `CONTINUITY.md` was updated