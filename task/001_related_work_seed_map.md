# Task 001: Related Work Seed Map

## Goal

Create a verified seed literature map for the PAPF project.

Do not write a full literature review yet. The goal is to identify relevant research areas, representative works, and the gaps they leave open.

## Read first

- `AGENTS.md`
- `CONTINUITY.md`
- `docs/related_work.md`
- `docs/research_brief.md`
- `docs/benchmark_spec.md`
- `docs/system_design.md`

## Create or update

- Create `docs/lit_matrix.md`
- Update `docs/related_work.md`
- Update `CONTINUITY.md` only if the project state materially changes

## Requirements

Use only real, verified sources.

Do not invent:

- paper titles
- authors
- venues
- years
- claims
- benchmark sizes
- results
- citation metadata

If a source cannot be verified, mark it as `UNCONFIRMED`.

Prefer primary sources:

- arXiv
- OpenReview
- ACL Anthology
- ACM
- IEEE
- USENIX
- official project pages
- official GitHub repos only as secondary implementation references

## Seed areas

Cover these categories:

1. Prompt injection / indirect prompt injection
2. Tool-using agent safety
3. Excessive agency
4. Confused deputy
5. Capability security / least privilege
6. Data minimization
7. Browser-agent safety
8. MCP / OAuth / delegated authorization
9. Permission UX
10. Consent fatigue / approval fatigue
11. Auditability and provenance

## Suggested seed works to verify

Start by verifying whether these are real and relevant:

- AgentDojo
- InjecAgent
- ToolEmu
- AgentDAM
- BrowseSafe
- related work on indirect prompt injection
- classical confused deputy work
- object-capability security
- OAuth delegated authorization
- usable permission systems in mobile / browser / app ecosystems

Do not include any work unless verified.

## `docs/lit_matrix.md` format

Use this table:

| Area | Work | Source status | Main problem | Agent/tool setting | Threat or failure mode | Evaluation method | Metrics | Relevance to PAPF | Gap left open |
|---|---|---|---|---|---|---|---|---|---|

Keep each row concise.

## `docs/related_work.md` format

For each category, write:

1. What the category studies
2. Representative works
3. How it relates to PAPF
4. Gap left open

Use cautious wording.

Example gap sentence:

"These works show that tool-using agents can be vulnerable to prompt injection and data exfiltration, but they do not by themselves define a user-comprehensible, task-scoped permission firewall for non-expert consumer users."

## Do not do

- Do not implement code.
- Do not write the paper introduction.
- Do not add fake BibTeX.
- Do not overclaim novelty.
- Do not paste raw abstracts.

## Final output

Report:

1. Sources added
2. Categories still weak
3. Claims marked `UNCONFIRMED`
4. Whether `CONTINUITY.md` was updated