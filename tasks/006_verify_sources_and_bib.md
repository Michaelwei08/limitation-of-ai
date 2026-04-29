# Task 006: Verify Sources and Build References

## Goal

Verify the seed related work for the PAPF project and create a clean `references.bib`.

This task should turn the current related-work scaffold into a source-grounded literature base.

Do not write the final literature review yet.

## Read first

- `AGENTS.md`
- `CONTINUITY.md`
- `docs/related_work.md`
- `docs/lit_matrix.md`
- `docs/research_gap.md`
- `docs/research_brief.md`

## Create or update

- Create or update `references.bib`
- Update `docs/lit_matrix.md`
- Update `docs/related_work.md`
- Update `docs/research_gap.md` only if source verification changes the gap
- Update `CONTINUITY.md` only if the project state materially changes

## Source verification requirements

Use only real, verified sources.

Prefer primary sources:

- arXiv
- OpenReview
- ACM Digital Library
- IEEE
- USENIX
- ACL Anthology
- official standards documents
- official project pages
- official GitHub repos only as secondary implementation references

Do not invent:

- paper titles
- authors
- venues
- years
- DOIs
- arXiv IDs
- benchmark sizes
- experimental results
- BibTeX fields

If a source cannot be verified, do not add it to `references.bib`.
Mark it as `UNCONFIRMED` in the docs.

## Candidate areas to verify

Verify representative sources for these areas:

1. Prompt injection and indirect prompt injection
2. Tool-using agent safety
3. Agent benchmarks
4. Privacy leakage and data minimization in agents
5. Confused deputy
6. Capability security / least privilege
7. OAuth / delegated authorization / scopes
8. Browser-agent safety
9. Permission UX
10. Consent fatigue / approval fatigue
11. Auditability / provenance / traceability

## Candidate works to check

Start from works already mentioned in `docs/lit_matrix.md` or `docs/related_work.md`.

Possible candidates may include:

- AgentDojo
- InjecAgent
- ToolEmu
- AgentDAM
- BrowseSafe
- indirect prompt injection work
- classical confused deputy work
- object-capability security work
- OAuth / delegated authorization standards
- usable security / permission UX work

These are candidates only. Verify before treating them as real sources.

## `references.bib` rules

For each verified source, add a BibTeX entry with stable citation key.

Preferred citation key format:

```text
firstauthorYYYYshorttitle
````

Example format:

```bibtex
@inproceedings{authorYYYYshorttitle,
  title = {...},
  author = {...},
  booktitle = {...},
  year = {...},
  url = {...}
}
```

If venue is unknown but arXiv is verified, use:

```bibtex
@misc{authorYYYYshorttitle,
  title = {...},
  author = {...},
  year = {...},
  eprint = {...},
  archivePrefix = {arXiv},
  url = {...}
}
```

Do not add fake DOI or venue fields.

## Update `docs/lit_matrix.md`

For each verified work, include:

| Area | Work | Citation key | Source status | Main problem | Agent/tool setting | Threat or failure mode | Evaluation method | Metrics | Relevance to PAPF | Gap left open |

Use `VERIFIED` only after source verification.

Use `UNCONFIRMED` if not verified.

Use `TODO` if not yet searched.

## Update `docs/related_work.md`

For each category, include:

1. What the category studies
2. Verified representative works
3. How they relate to PAPF
4. Gap left open

Use cautious language.

Do not claim PAPF is novel as fact.

Acceptable phrasing:

* “This suggests a possible gap...”
* “Existing work appears to focus on...”
* “A remaining question is...”
* “PAPF is positioned as a candidate framework for...”

Avoid:

* “No prior work has...”
* “PAPF is the first...”
* “This proves...”
* “This solves...”

## Update `docs/research_gap.md`

Only revise the gap if verification changes the current positioning.

The likely gap should remain cautious:

Existing work studies prompt injection, agent risk, privacy leakage, authorization, and permission UX, but may not fully combine:

1. task-scoped least-privilege capability compilation,
2. runtime enforcement outside the LLM,
3. user-comprehensible permission boundaries for non-expert consumer users,
4. evaluation across task success, over-access, exfiltration, false allow, and false deny.

## Do not do

* Do not implement code.
* Do not write the final paper.
* Do not invent citations.
* Do not add unverified BibTeX entries.
* Do not overclaim novelty.
* Do not paste long abstracts.
* Do not report experimental results.

## Final output

Report:

1. Verified sources added to `references.bib`
2. Sources left `UNCONFIRMED`
3. Weakest related-work areas
4. Any changes to the research gap
5. Whether `CONTINUITY.md` was updated

````