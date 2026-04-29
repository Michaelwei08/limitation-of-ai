# CONTINUITY.md

## Snapshot
- Goal: Build a research project on task-scoped permission boundaries for consumer AI agents.
- Working title: Personal Agent Permission Firewall (PAPF).
- Benchmark idea: NonExpert-AgentPermBench.
- Now: Core docs specify the PAPF architecture and paper plan; `src/papf/` includes deterministic evaluation, hardened run serialization, and a file-backed benchmark loader; `benchmarks/papf_seed_cases/` mirrors the current email/files/browser fixture.
- Next: Start `tasks/013_schema_policy_validation.md` to harden validation, or expand the file-backed seed suite under `tasks/017_expand_benchmark_suite.md`.
- Open questions: Clarification versus safe refusal under ambiguity, redaction evidence design, partial-success scoring, and whether the planned non-expert comprehension protocol should become an actual user study.

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
- D011 ACTIVE 2026-04-27 [CODE]: The first implementation milestone starts with Python-facing schemas, validators, deterministic capability compilation, and rule-based enforcement before building a demo agent sandbox.
- D012 ACTIVE 2026-04-27 [CODE]: `benchmarks/seed_cases/` stays as a quarantined auxiliary CAR artifact for now, but is excluded from PAPF claims, metrics, and paper evidence unless the user explicitly redirects scope.
- D013 ACTIVE 2026-04-27 [CODE]: PAPF evaluation run artifacts should serialize both JSONL and CSV metric rows plus audit-summary JSONL; test-only serialization artifacts are ignored while the default run remains visible.

## State

### Done
- 2026-04-27 [CODE]: Completed `problem_framing` research output JSON for task-scoped permission-boundary problem formulation and validated full field coverage.
- 2026-04-27 [USER]: Created project-level `AGENTS.md`.
- 2026-04-27 [CODE]: Created `README.md` and baseline docs for research framing, benchmark specification, system design, related-work categories, and paper outline.
- 2026-04-27 [CODE]: Created placeholder directories `docs/`, `src/papf/`, `tests/`, `experiments/configs/`, `experiments/runs/`, and `paper/`.
- 2026-04-27 [CODE]: Replaced the placeholder `docs/related_work.md` scaffold with a verified seed literature map and created `docs/lit_matrix.md`.
- 2026-04-27 [CODE]: Expanded `docs/related_work.md` and `docs/lit_matrix.md` into an explicit 11-category seed map; corrected source links and strengthened browser-agent, delegated-authorization, and provenance coverage.
- 2026-04-27 [CODE]: Added `docs/research_gap.md` to clarify the current gap hypothesis, overclaim risks, venue options, and a recommended first-paper framing; aligned `docs/research_brief.md` to that recommendation.
- 2026-04-27 [CODE]: Added `references.bib` and tightened `docs/lit_matrix.md` plus `docs/related_work.md` into a citation-keyed, source-verified seed literature base.
- 2026-04-27 [CODE]: Expanded `docs/benchmark_spec.md` and created `docs/benchmark_schema_plan.md` to formalize the benchmark taxonomy, schema boundaries, attack taxonomy, and metric definitions.
- 2026-04-27 [CODE]: Rewrote `docs/system_design.md` into a concrete PAPF control-plane architecture and created `docs/implementation_plan.md` with MVP scope, module contracts, testing strategy, risks, and milestones.
- 2026-04-27 [CODE]: Updated `docs/paper_outline.md` and created `docs/paper_plan.md` plus `docs/figures_and_tables_plan.md` to lock a systems-first paper framing, required evidence, likely experiments, and bounded claim language.
- 2026-04-27 [CODE]: Added the first executable PAPF foundation under `src/papf/`: shared runtime enums/scope specs, intent validation, capability compilation, policy decisions, enforcement mediation, audit records, benchmark fixture validation, and deterministic trace metrics.
- 2026-04-27 [CODE]: Added `tests/test_runtime_foundation.py` covering fixture validation, narrow allow, unrelated-private denial, safe narrowing, send confirmation gating, and simple trace metrics.
- 2026-04-27 [CODE]: Extended the first fixture from `email + files` to `email + files + browser`, including an approved merchant policy page and an untrusted adversarial webpage.
- 2026-04-27 [CODE]: Added deterministic trace scenarios and a benchmark runner for clean, temptation, attack, and recovery cases under `src/papf/benchmark/traces.py`.
- 2026-04-27 [CODE]: Tightened broad-scope narrowing so requests mentioning any unallowed candidate refs are denied instead of narrowed around the allowed subset.
- 2026-04-27 [CODE]: Completed Task 008 by adding deterministic PAPF evaluation harness modules, structured case/suite results, audit-event emission, metric rows, and focused harness tests.
- 2026-04-27 [CODE]: Completed Task 007 as written by creating 11 synthetic Checkpointed Adaptive Reasoning seed cases plus README and design notes; this artifact is project-mismatched with PAPF and should be reviewed for repo fit.
- 2026-04-27 [CODE]: Used the `research` skill workflow to create `papf_pipeline_research/outline.yaml` and `papf_pipeline_research/fields.yaml` for the full PAPF research/implementation pipeline.
- 2026-04-27 [CODE]: Added `tasks/009_pipeline_backlog.md` plus `tasks/010`-`024` as prospective PAPF steps covering scope reconciliation, run serialization, benchmark loading, validation, redaction, recovery scoring, baselines, suite expansion, synthetic tools, experiments, figures, model-assisted proposals, user study protocol, source verification, and paper/artifact packaging.
- 2026-04-27 [CODE]: Completed `benchmark_schema` structured research output as `papf_pipeline_research/results/Benchmark_schema_and_synthetic_data_model.json`; validation covers all 16 required fields.
- 2026-04-27 [CODE]: Completed `runtime_foundation` structured research output as `papf_pipeline_research/results/Deterministic_PAPF_runtime_foundation.json`; validation covers all 16 required fields.
- 2026-04-27 [CODE]: Completed `literature_gap` structured research output as `papf_pipeline_research/results/Verified_relatedwork_and_gap_analysis.json`; validation covers all 16 required fields and narrows the gap claim around newer close enforcement work.
- 2026-04-27 [CODE]: Completed `auditability` structured research output as `papf_pipeline_research/results/Audit_trace_and_evidence_model.json`; validation covers all 16 required fields and marks redaction evidence, confirmation event pairs, richer auditability scoring, and baseline audit traces as uncertain.
- 2026-04-27 [CODE]: Completed `evaluation_harness` structured research output as `papf_pipeline_research/results/Deterministic_evaluation_harness.json`; validation covers all 16 required fields and marks durable experiment serialization as planned/uncertain.
- 2026-04-27 [CODE]: Completed `first_slice` structured research output as `papf_pipeline_research/results/Email_files_browser_benchmark_slice.json`; validation covers all 16 required fields and includes clean, temptation, attack, and recovery scenarios.
- 2026-04-27 [CODE]: Completed `baselines` structured research output as `papf_pipeline_research/results/Comparable_baselines.json`; validation covers all 16 required fields and specifies broad-access, prompt-only, and shared trace-output requirements.
- 2026-04-27 [CODE]: Completed `experiment_execution` structured research output as `papf_pipeline_research/results/Experiment_runner_and_result_artifacts.json`; validation covers all 16 required fields and marks experiment-runner serialization and baseline outputs as planned/uncertain.
- 2026-04-27 [CODE]: Completed `user_comprehension` structured research output as `papf_pipeline_research/results/Nonexpert_comprehension_protocol.json`; validation covers all 16 required fields and keeps non-expert comprehension as a planned protocol rather than an empirical result.
- 2026-04-27 [CODE]: Completed `model_assisted_extensions` structured research output as `papf_pipeline_research/results/Optional_modelassisted_proposal_layers.json`; validation covers all 16 required fields and keeps model-assisted intent proposals and explanations non-authoritative.
- 2026-04-27 [CODE]: Completed `analysis_and_figures` structured research output as `papf_pipeline_research/results/Results_analysis_figures_and_tables.json`; validation covers all 16 required fields and includes PAPF-only harness metric rows, baseline availability status, failure-case examples, and architecture/policy examples.
- 2026-04-27 [CODE]: Completed `paper_and_artifact` structured research output as `papf_pipeline_research/results/Paper_draft_and_artifact_package.json`; validation covers all 16 required fields and keeps paper/artifact claims bounded to current PAPF-only evidence.
- 2026-04-27 [CODE]: Completed Task 010 by adding `docs/scope_reconciliation.md`; PAPF remains primary and CAR seed cases are retained only as quarantined auxiliary material.
- 2026-04-27 [CODE]: Completed Task 011 by adding `src/papf/evaluation/serialization.py`, `experiments/configs/default_email_files_browser.json`, serialized default run artifacts, and focused serialization tests.
- 2026-04-29 [CODE]: Hardened Task 011 serialization path validation, documented output artifact formats in the default config, added deterministic-output regression coverage, and regenerated default metadata.
- 2026-04-29 [CODE]: Completed Task 012 by adding a YAML/JSON PAPF benchmark loader, a synthetic file-backed email/files/browser seed case, and loader tests for missing refs, invalid enum labels, and synthetic-data enforcement.

### Now
- 2026-04-29 [CODE]: Project has an executable PAPF evaluation path, serialized default run artifacts, and a file-backed PAPF seed case loader while preserving the hard-coded smoke fixture.

### Next
- 2026-04-29 [CODE]: Run Task 013 to harden schema/policy validation before larger loader-backed suite expansion.
- 2026-04-27 [CODE]: Keep the security-critical path deterministic while expanding benchmark loaders, baselines, and experiment reporting.

## Working set
- `AGENTS.md`
- `CONTINUITY.md`
- `README.md`
- `references.bib`
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
- `tests/test_runtime_foundation.py`
- `tests/test_trace_runner.py`
- `tests/test_evaluation_harness.py`
- `benchmarks/seed_cases/`
- `docs/benchmark_case_design_notes.md`
- `docs/scope_reconciliation.md`
- `experiments/configs/default_email_files_browser.json`
- `experiments/runs/.gitignore`
- `experiments/runs/default_email_files_browser/metadata.json`
- `experiments/runs/default_email_files_browser/metrics.jsonl`
- `experiments/runs/default_email_files_browser/metrics.csv`
- `experiments/runs/default_email_files_browser/audit_summaries.jsonl`
- `papf_pipeline_research/outline.yaml`
- `papf_pipeline_research/fields.yaml`
- `papf_pipeline_research/results/Taskscoped_permissionboundary_problem_formulation.json`
- `papf_pipeline_research/results/Verified_relatedwork_and_gap_analysis.json`
- `papf_pipeline_research/results/Benchmark_schema_and_synthetic_data_model.json`
- `papf_pipeline_research/results/Deterministic_PAPF_runtime_foundation.json`
- `papf_pipeline_research/results/Audit_trace_and_evidence_model.json`
- `papf_pipeline_research/results/Deterministic_evaluation_harness.json`
- `papf_pipeline_research/results/Email_files_browser_benchmark_slice.json`
- `papf_pipeline_research/results/Comparable_baselines.json`
- `papf_pipeline_research/results/Experiment_runner_and_result_artifacts.json`
- `papf_pipeline_research/results/Nonexpert_comprehension_protocol.json`
- `papf_pipeline_research/results/Optional_modelassisted_proposal_layers.json`
- `papf_pipeline_research/results/Results_analysis_figures_and_tables.json`
- `papf_pipeline_research/results/Paper_draft_and_artifact_package.json`
- `tasks/009_pipeline_backlog.md`
- `tasks/010_scope_reconciliation.md`
- `tasks/011_evaluation_run_serialization.md`
- `tasks/012_benchmark_loader.md`
- `tasks/013_schema_policy_validation.md`
- `tasks/014_redaction_evidence.md`
- `tasks/015_recovery_scoring.md`
- `tasks/016_baselines.md`
- `tasks/017_expand_benchmark_suite.md`
- `tasks/018_synthetic_tool_runtime.md`
- `tasks/019_experiment_runner.md`
- `tasks/020_results_figures.md`
- `tasks/021_model_assisted_intent.md`
- `tasks/022_user_comprehension_protocol.md`
- `tasks/023_deeper_source_verification.md`
- `tasks/024_paper_draft_and_artifact.md`
- `src/papf/evaluation/serialization.py`
- `tests/test_evaluation_serialization.py`
- `src/papf/benchmark/loader.py`
- `src/papf/benchmark/_loader_builders.py`
- `benchmarks/papf_seed_cases/email_files_browser.yaml`
- `tests/test_benchmark_loader.py`
- `experiments/configs/`
- `experiments/runs/`
- `paper/`

## Open questions
- 2026-04-27 [CODE]: SUPERSEDED by D013: Should evaluation run serialization be JSONL, CSV, or both?
- 2026-04-27 [CODE]: SUPERSEDED by D012 for now: Should the CAR seed cases from Task 007 be retained here, renamed, or moved out of the PAPF workspace?
- 2026-04-27 [ASSUMPTION]: Should the first benchmark release be domain-specific or cross-domain?
- 2026-04-27 [CODE]: Should a follow-up literature pass focus specifically on agent-specific auditability/provenance and agent-permission UX, which remain the weakest verified clusters?
- 2026-04-27 [CODE]: Should the first narrow slice stay exactly `email + files + browser`, or should browser support be deferred if fixture complexity slows the first runtime milestone?
- 2026-04-27 [CODE]: SUPERSEDED by `papf_pipeline_research/results/Nonexpert_comprehension_protocol.json`: How should the project measure non-expert comprehension alongside the automated benchmark without overclaiming a user-centered result?
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
- 2026-04-27T08:40:21-07:00 [TOOL]: `Get-Date -Format o` -> verified timestamp for the bibliography and source-status normalization pass.
- 2026-04-27 [CODE]: Created `references.bib`; normalized verified citation keys; removed unverified rows from the retained literature matrix rather than padding the seed map with unsupported citations.
- 2026-04-27 [CODE]: Synthesized the verified seed map into `docs/research_gap.md` and recorded a provisional first-paper positioning recommendation.
- 2026-04-27 [CODE]: Formalized benchmark taxonomy and schema planning in `docs/benchmark_spec.md` and `docs/benchmark_schema_plan.md`, including multi-axis data labels and record-level metric hooks.
- 2026-04-27 [CODE]: Clarified PAPF system architecture in `docs/system_design.md` and created `docs/implementation_plan.md` to define MVP scope, module boundaries, runtime records, testing strategy, and milestones.
- 2026-04-27 [CODE]: Added paper-planning docs to lock the first submission story, required evidence, experiments, and planned figures/tables without inventing results.
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v` -> 6 tests passed for the runtime foundation.
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -m compileall -q src tests` -> Python sources compiled successfully.
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v` -> 11 tests passed for runtime foundation plus clean/temptation/attack/recovery trace runner.
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -m compileall -q src tests` -> Python sources compiled successfully after trace-runner additions.
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v` -> 18 tests passed after evaluation harness additions.
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -m compileall -q src tests` -> Python sources compiled successfully after evaluation harness additions.
- 2026-04-27 [TOOL]: `Select-String -Path benchmarks\seed_cases\cases.yaml -Pattern '^-' | Measure-Object` -> 11 seed cases counted.
- 2026-04-27 [TOOL]: Web/source check for pipeline planning used AgentDojo, InjecAgent, ToolEmu, AgentDAM, BrowseSafe, and MCP Authorization sources.
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v` -> 18 tests still pass after research outline/task backlog additions.
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Taskscoped_permissionboundary_problem_formulation.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: Verified current source targets for Progent, AgentSpec, MiniScope, IFC-based LLM-system defense, IsolateGPT, AgentDAM, BrowserART, MCP Authorization, RAR, PROV, and permission-UX sources.
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Verified_relatedwork_and_gap_analysis.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Benchmark_schema_and_synthetic_data_model.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Deterministic_PAPF_runtime_foundation.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Audit_trace_and_evidence_model.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Deterministic_evaluation_harness.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Email_files_browser_benchmark_slice.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Comparable_baselines.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Experiment_runner_and_result_artifacts.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Nonexpert_comprehension_protocol.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Optional_modelassisted_proposal_layers.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -c "from papf.evaluation.runner import evaluate_default_suite; ..."` -> produced PAPF metric rows for clean, temptation, attack, and recovery scenarios used in `Results_analysis_figures_and_tables.json`.
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Results_analysis_figures_and_tables.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -j papf_pipeline_research\results\Paper_draft_and_artifact_package.json` -> PASS, 100.0% coverage (16/16 required fields).
- 2026-04-27 [TOOL]: `python <HOME>\.codex\skills\research\validate_json.py -f papf_pipeline_research\fields.yaml -d papf_pipeline_research\results -q` -> 13/13 deep-research JSON files passed, average coverage 100.0%.
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v` -> 18 tests still pass after `/research-deep` output generation.
- 2026-04-27 [TOOL]: Verified `docs/scope_reconciliation.md` links point to existing local files.
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v` -> 22 tests passed after Task 011 serialization additions.
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -m compileall -q src tests` -> Python sources compiled after Task 011 serialization additions.
- 2026-04-27 [TOOL]: `$env:PYTHONPATH='src'; python -c "from papf.evaluation.serialization import write_default_evaluation_run; ..."` -> wrote default serialized run artifacts to `experiments/runs/default_email_files_browser/`.
- 2026-04-29 [TOOL]: `python -m unittest discover -s tests -v` -> failed because `papf` is not importable without `PYTHONPATH=src` in the current src-layout workspace.
- 2026-04-29 [TOOL]: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v` -> 25 tests passed after serialization hardening and determinism coverage.
- 2026-04-29 [TOOL]: `$env:PYTHONPATH='src'; python -m compileall -q src tests` -> Python sources compiled successfully after serialization hardening.
- 2026-04-29 [TOOL]: `$env:PYTHONPATH='src'; python -m unittest tests.test_benchmark_loader -v` -> 7 loader tests passed after replacing temp-directory scratch files with deterministic test scratch file cleanup.
- 2026-04-29 [TOOL]: `$env:PYTHONPATH='src'; $env:PYTHONDONTWRITEBYTECODE='1'; python -B -m unittest discover -s tests -v` -> 34 tests passed after Task 012 loader additions.
- 2026-04-29 [TOOL]: `python -B - <<compile script>>` -> compiled 32 Python files in memory without writing bytecode.
