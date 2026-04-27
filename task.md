# Task

## Goal

Populate the related-work scaffold with a verified seed literature map for the PAPF project.

Do not write a full literature review yet. Create a concise, source-grounded map of relevant papers, benchmarks, and gaps.

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
- Update `CONTINUITY.md` if the project state changes meaningfully

## Requirements

Use only real, verified sources.

Do not invent:
- citations
- venues
- paper claims
- benchmark sizes
- results
- author names

If a source cannot be verified, mark it as `UNCONFIRMED`.

Prefer primary sources:
- arXiv pages
- OpenReview pages
- ACL Anthology
- ACM/IEEE/USENIX pages
- official GitHub repos only as secondary implementation references

## Seed works to include if verified

Start with these areas:

1. AgentDojo
   - dynamic environment for evaluating prompt injection attacks and defenses in tool-using agents

2. InjecAgent
   - benchmark for indirect prompt injection in tool-integrated LLM agents

3. ToolEmu
   - LM-emulated tool environment for identifying risks of LM agents

4. AgentDAM
   - privacy leakage / data minimization evaluation for autonomous web agents

Then find additional sources for:

5. confused deputy
6. object-capability / least privilege security
7. data minimization
8. OAuth / delegated authorization
9. usable permission systems
10. consent fatigue / approval fatigue

## `docs/lit_matrix.md` format

Use a table with columns:

| Area | Work | Source status | Main problem | Agent/tool setting | Threat or failure mode | Evaluation method | Metrics | Relevance to PAPF | Gap left open |

Keep each row concise.

## `docs/related_work.md` format

For each category, write:

1. What this category studies
2. Key representative works
3. How it relates to PAPF
4. What gap remains

Use cautious wording. Example:

"These benchmarks show that tool-using agents are vulnerable to prompt-injection and exfiltration attacks, but they do not by themselves define a user-comprehensible, task-scoped permission firewall for non-expert consumer users."

## Do not do

- Do not implement code.
- Do not write the paper introduction yet.
- Do not claim PAPF is novel until the gap is better verified.
- Do not add fake BibTeX entries.
- Do not overfill the document with raw abstracts.

## Final output

Report:

1. Sources added
2. Categories still weak
3. Claims that remain UNCONFIRMED
4. Whether `CONTINUITY.md` was updated