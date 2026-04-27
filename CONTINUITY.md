# CONTINUITY.md

## Snapshot
- Goal: Build a research project on task-scoped permission boundaries for consumer AI agents.
- Working title: Personal Agent Permission Firewall (PAPF).
- Benchmark idea: NonExpert-AgentPermBench.
- Now: Core docs now specify a PAPF control-plane architecture, benchmark schemas, a first executable `email + files + browser` slice, and a systems-first paper plan with explicit evidence boundaries.
- Next: Map the documented runtime records and benchmark schemas onto Python-facing fixtures, validators, and the first rule-based enforcement skeleton so the paper can move from planning claims to executable evidence.
- Open questions: Clarification versus safe refusal under ambiguity, redaction evidence design, partial-success scoring, and whether non-expert comprehension stays a deferred follow-up or becomes a later user-study addition.

## Invariants / Constraints
- 2026-04-27 [USER]: Permission enforcement must happen outside the LLM.
- 2026-04-27 [USER]: Avoid generic AI ethics framing; focus on measurable, publishable research.

## Decisions
- D001 ACTIVE 2026-04-27 [USER]: Project focus is task-scoped permission boundaries for consumer AI agents.
- D002 ACTIVE 2026-04-27 [USER]: Working system name is Personal Agent Permission Firewall.
- D003 ACTIVE 2026-04-27 [USER]: Possible benchmark name is NonExpert-AgentPermBench.
- D004 ACTIVE 2026-04-27 [USER]: The project should target a rigorous research contribution, not a broad opinion essay.
- D005 ACTIVE 2026-04-27 [CODE]: Current best first-paper framing is a security/privacy systems paper centered on task-scoped external enforcement, with the benchmark used as an evaluation artifact rather than the sole contribution.
- D006 ACTIVE 2026-04-27 [CODE]: Benchmark data should use modular multi-axis labels for relevance, sensitivity, and trust, with separate schemas for task definitions, policy rules, tool traces, and audit events.
- D007 ACTIVE 2026-04-27 [CODE]: The first executable PAPF slice should target a synthetic `email + files + browser` environment because it is narrow enough to implement while still exposing over-access, prompt injection, exfiltration, and recovery behavior.
- D008 ACTIVE 2026-04-27 [CODE]: The first PAPF prototype should keep the security-critical path rule-based and deterministic; any LLM role should remain advisory for intent proposals, explanations, or recovery suggestions only.
- D009 ACTIVE 2026-04-27 [CODE]: The first paper should be framed as a security/privacy systems paper with benchmark-backed evaluation, not as an HCI-first or benchmark-only paper.
- D010 ACTIVE 2026-04-27 [CODE]: Non-expert comprehension should remain a design requirement in the first paper unless a dedicated user-study protocol is added; it should not be claimed as an established result from the automated benchmark alone.

## State

### Done
- 2026-04-27 [USER]: Created project-level `AGENTS.md`.
- 2026-04-27 [CODE]: Created `README.md` and baseline docs for research framing, benchmark specification, system design, related-work categories, and paper outline.
- 2026-04-27 [CODE]: Created placeholder directories `docs/`, `src/papf/`, `tests/`, `experiments/configs/`, `experiments/runs/`, and `paper/`.
- 2026-04-27 [CODE]: Replaced the placeholder `docs/related_work.md` scaffold with a verified seed literature map and created `docs/lit_matrix.md`.
- 2026-04-27 [CODE]: Expanded `docs/related_work.md` and `docs/lit_matrix.md` into an explicit 11-category seed map; corrected source links and strengthened browser-agent, delegated-authorization, and provenance coverage.
- 2026-04-27 [CODE]: Added `docs/research_gap.md` to clarify the current gap hypothesis, overclaim risks, venue options, and a recommended first-paper framing; aligned `docs/research_brief.md` to that recommendation.
- 2026-04-27 [CODE]: Expanded `docs/benchmark_spec.md` and created `docs/benchmark_schema_plan.md` to formalize the benchmark taxonomy, schema boundaries, attack taxonomy, and metric definitions.
- 2026-04-27 [CODE]: Rewrote `docs/system_design.md` into a concrete PAPF control-plane architecture and created `docs/implementation_plan.md` with MVP scope, module contracts, testing strategy, risks, and milestones.
- 2026-04-27 [CODE]: Updated `docs/paper_outline.md` and created `docs/paper_plan.md` plus `docs/figures_and_tables_plan.md` to lock a systems-first paper framing, required evidence, likely experiments, and bounded claim language.

### Now
- 2026-04-27 [CODE]: Project is still documentation-first, but the architecture and paper plan are now concrete enough to start runtime schema work, narrow benchmark fixtures, and a rule-based enforcement skeleton for the first slice.

### Next
- 2026-04-27 [ASSUMPTION]: Convert verified source pages into citation-ready bibliography entries.
- 2026-04-27 [CODE]: Map the documented runtime records and benchmark schema plan into Python-facing fixtures, validators, and deterministic metric computation.
- 2026-04-27 [CODE]: Build the first rule-based PAPF prototype for the `email + files + browser` slice without production integrations.

## Working set
- `AGENTS.md`
- `CONTINUITY.md`
- `README.md`
- `docs/paper_outline.md`
- `docs/related_work.md`
- `docs/lit_matrix.md`
- `docs/research_brief.md`
- `docs/benchmark_spec.md`
- `docs/benchmark_schema_plan.md`
- `docs/research_gap.md`
- `docs/system_design.md`
- `docs/implementation_plan.md`
- `docs/paper_plan.md`
- `docs/figures_and_tables_plan.md`
- `src/papf/`
- `experiments/configs/`
- `experiments/runs/`
- `paper/`

## Open questions
- 2026-04-27 [USER]: Should the first implementation be a benchmark, a permission compiler, or a demo agent sandbox?
- 2026-04-27 [ASSUMPTION]: Should the first benchmark release be domain-specific or cross-domain?
- 2026-04-27 [CODE]: Should a follow-up literature pass focus specifically on agent-specific auditability/provenance and agent-permission UX, which remain the weakest verified clusters?
- 2026-04-27 [CODE]: Should the first narrow slice stay exactly `email + files + browser`, or should browser support be deferred if fixture complexity slows the first runtime milestone?
- 2026-04-27 [CODE]: How should the project measure non-expert comprehension alongside the automated benchmark without overclaiming a user-centered result?
- 2026-04-27 [CODE]: When the compiler cannot identify a sufficiently narrow scope, should the runtime require clarification or default to safe refusal?
- 2026-04-27 [CODE]: What concrete artifact should prove `allow_with_redaction` at runtime so evaluators can verify that redaction really occurred?
- 2026-04-27 [CODE]: Should the first paper explicitly omit comprehension claims, or reserve a placeholder section that frames a future user-study protocol without presenting results?

## Receipts
- 2026-04-27 [USER]: Source PDF describes AI ethics/LLM agent permission-boundary research direction and PAPF-style project framing.
- 2026-04-27 [TOOL]: Created baseline repo directories with PowerShell `New-Item -ItemType Directory`.
- 2026-04-27 [CODE]: Seeded initial repository docs without adding implementation code or experimental results.
- 2026-04-27T03:06:57-07:00 [TOOL]: `Get-Date -Format o` -> verified working timestamp for source-grounding pass.
- 2026-04-27 [TOOL]: Verified primary source pages for AgentDojo, InjecAgent, ToolEmu, AgentDAM, OAuth RFCs, and USENIX permission-UX papers; used secondary verification only where primary publisher text was not directly accessible in-tool.
- 2026-04-27 [TOOL]: Verified additional source pages for BIPIA, BrowseSafe, Aligned LLMs Are Not Aligned Browser Agents, MCP authorization, PROV, ACCESSPROV, and Android permission-behavior studies.
- 2026-04-27 [CODE]: Synthesized the verified seed map into `docs/research_gap.md` and recorded a provisional first-paper positioning recommendation.
- 2026-04-27 [CODE]: Formalized benchmark taxonomy and schema planning in `docs/benchmark_spec.md` and `docs/benchmark_schema_plan.md`, including multi-axis data labels and record-level metric hooks.
- 2026-04-27 [CODE]: Clarified PAPF system architecture in `docs/system_design.md` and created `docs/implementation_plan.md` to define MVP scope, module boundaries, runtime records, testing strategy, and milestones.
- 2026-04-27 [CODE]: Added paper-planning docs to lock the first submission story, required evidence, experiments, and planned figures/tables without inventing results.
