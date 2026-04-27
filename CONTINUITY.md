# CONTINUITY.md

## Snapshot
- Goal: Build a research project on task-scoped permission boundaries for consumer AI agents.
- Working title: Personal Agent Permission Firewall (PAPF).
- Benchmark idea: NonExpert-AgentPermBench.
- Now: Baseline docs now include a verified seed literature map linking agent attack benchmarks, least-privilege/capability security, delegated authorization, and permission UX to PAPF.
- Next: Turn the verified seed map into citation-ready bibliography entries and use it to narrow the first implementation slice.
- Open questions: Exact venue target, first implementation slice, scope of the first benchmark release, and whether auditability needs a dedicated related-work search pass.

## Invariants / Constraints
- 2026-04-27 [USER]: Permission enforcement must happen outside the LLM.
- 2026-04-27 [USER]: Avoid generic AI ethics framing; focus on measurable, publishable research.

## Decisions
- D001 ACTIVE 2026-04-27 [USER]: Project focus is task-scoped permission boundaries for consumer AI agents.
- D002 ACTIVE 2026-04-27 [USER]: Working system name is Personal Agent Permission Firewall.
- D003 ACTIVE 2026-04-27 [USER]: Possible benchmark name is NonExpert-AgentPermBench.
- D004 ACTIVE 2026-04-27 [USER]: The project should target a rigorous research contribution, not a broad opinion essay.

## State

### Done
- 2026-04-27 [USER]: Created project-level `AGENTS.md`.
- 2026-04-27 [CODE]: Created `README.md` and baseline docs for research framing, benchmark specification, system design, related-work categories, and paper outline.
- 2026-04-27 [CODE]: Created placeholder directories `docs/`, `src/papf/`, `tests/`, `experiments/configs/`, `experiments/runs/`, and `paper/`.
- 2026-04-27 [CODE]: Replaced the placeholder `docs/related_work.md` scaffold with a verified seed literature map and created `docs/lit_matrix.md`.

### Now
- 2026-04-27 [CODE]: Project is still in documentation-first initialization state, but related work is now grounded in verified seed sources instead of placeholders.

### Next
- 2026-04-27 [ASSUMPTION]: Select the first implementation target.
- 2026-04-27 [ASSUMPTION]: Convert verified source pages into citation-ready bibliography entries.
- 2026-04-27 [ASSUMPTION]: Formalize metric definitions and benchmark instance schema.

## Working set
- `AGENTS.md`
- `CONTINUITY.md`
- `README.md`
- `docs/paper_outline.md`
- `docs/related_work.md`
- `docs/lit_matrix.md`
- `docs/research_brief.md`
- `docs/benchmark_spec.md`
- `docs/system_design.md`
- `src/papf/`
- `experiments/configs/`
- `experiments/runs/`
- `paper/`

## Open questions
- 2026-04-27 [USER]: Which venue should be prioritized first: ICML/NeurIPS D&B, security conference, or CHI/SOUPS?
- 2026-04-27 [USER]: Should the first implementation be a benchmark, a permission compiler, or a demo agent sandbox?
- 2026-04-27 [ASSUMPTION]: Should the first benchmark release be domain-specific or cross-domain?
- 2026-04-27 [CODE]: Should a follow-up literature pass focus specifically on auditability/provenance and agent-permission UX, which remain the weakest verified clusters?

## Receipts
- 2026-04-27 [USER]: Source PDF describes AI ethics/LLM agent permission-boundary research direction and PAPF-style project framing.
- 2026-04-27 [TOOL]: Created baseline repo directories with PowerShell `New-Item -ItemType Directory`.
- 2026-04-27 [CODE]: Seeded initial repository docs without adding implementation code or experimental results.
- 2026-04-27T03:06:57-07:00 [TOOL]: `Get-Date -Format o` -> verified working timestamp for source-grounding pass.
- 2026-04-27 [TOOL]: Verified primary source pages for AgentDojo, InjecAgent, ToolEmu, AgentDAM, OAuth RFCs, and USENIX permission-UX papers; used secondary verification only where primary publisher text was not directly accessible in-tool.
