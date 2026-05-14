# Artifact Checklist

This checklist tracks the current reproducible PAPF artifact for secondary prototype validation in the HCI/privacy paper draft.

## Scope

- Artifact name: Personal Agent Permission Firewall (PAPF) synthetic trace evaluation slice.
- Benchmark scope: synthetic `email + files + browser` tasks only.
- Evidence scope: deterministic 12-trace run over PAPF, broad-access, prompt-only, tool-scope, static-policy, and PAPF ablation modes.
- Non-evidence scope: no real user data, no production integrations, no completed non-expert user study, no human-comprehension evidence, no formal least-privilege proof.

## Evaluation Role

The artifact is secondary feasibility evidence for the paper. It shows whether PAPF can enforce scoped decisions, block unsafe synthetic tool calls, require redaction or confirmation, and produce audit-backed metrics under controlled traces.

The primary HCI/privacy evaluation is the planned non-expert user study. That study, not the synthetic trace run, is responsible for evaluating permission comprehension, privacy-preserving consent decisions, perceived control, trust, workload, and consent fatigue.

## Required Environment

- Python 3.11 or compatible Python with standard-library `unittest`.
- Run commands from the repository root.
- Set `PYTHONPATH=src` because the project uses a `src/` layout.
- Optional: set `PYTHONDONTWRITEBYTECODE=1` and use `python -B` to avoid writing bytecode during verification.

## Reproduce Default Experiment

```powershell
$env:PYTHONPATH='src'; $env:PYTHONDONTWRITEBYTECODE='1'; python -B -m papf.cli run-experiment --config experiments/configs/default_email_files_browser.json --timestamp 2026-04-30T00:00:00+00:00
```

Expected output directory:

```text
experiments/runs/default_email_files_browser/
```

Expected run artifacts:

- `metadata.json`
- `config_snapshot.json`
- `metrics.jsonl`
- `metrics.csv`
- `decisions.jsonl`
- `audit_summaries.jsonl`

## Regenerate Paper Tables and Result Figures

```powershell
$env:PYTHONPATH='src'; $env:PYTHONDONTWRITEBYTECODE='1'; python -B -c "from papf.evaluation.reporting import generate_reporting_artifacts; generate_reporting_artifacts('experiments/runs/default_email_files_browser')"
```

Expected paper artifacts:

- `paper/tables/main_metrics.md`
- `paper/tables/baseline_comparison.md`
- `paper/tables/ablation_results.md`
- `paper/tables/stronger_baseline_results.md`
- `paper/tables/failure_cases.md`
- `paper/tables/run_provenance.md`
- `paper/figures/task_success_rate_by_mode.svg`
- `paper/figures/false_allows_by_mode.svg`

## Static Paper Figures

The draft also includes hand-authored workflow figures:

- `paper/figures/papf_pipeline.svg`
- `paper/figures/papf_runtime_workflow.svg`

These figures explain architecture and workflow. They are not generated from experiment metrics.

The draft also includes hand-authored paper-facing explanatory tables:

- `paper/tables/capability_compilation_example.md`
- `paper/tables/failure_case_highlights.md`
- `paper/tables/ablation_plan.md`
- `paper/tables/stronger_baseline_plan.md`
- `paper/tables/user_study_scenarios.md`
- `paper/tables/prompt_variants.md`
- `paper/tables/user_study_measures.md`

These tables summarize existing benchmark, generated-result, and planned-study artifacts. They should not be treated as independent experiment outputs or participant results.

## Verification Commands

Run the test suite:

```powershell
$env:PYTHONPATH='src'; $env:PYTHONDONTWRITEBYTECODE='1'; python -B -m unittest discover -s tests -v
```

Check that generated paper numbers are artifact-derived:

```powershell
$env:PYTHONPATH='src'; $env:PYTHONDONTWRITEBYTECODE='1'; python -B -m unittest tests.test_reporting -v
```

Check citation keys used in paper-facing docs manually before submission. The current draft uses citation keys present in `references.bib`, but this checklist does not replace a full bibliography build.

## Paper Claim Boundaries

The artifact supports these bounded secondary technical claims:

- PAPF enforces decisions outside the LLM in the current prototype.
- PAPF can enforce scoped decisions in the current synthetic trace suite.
- PAPF records zero false allows and zero over-access in the current 12-trace synthetic run.
- Broad-access and prompt-only baselines record 16 false allows each in the same run.
- The current run exposes a utility/safety tradeoff: PAPF has lower task-success proxy and nonzero consent burden.
- Ablations and stronger baselines provide supporting evidence about redaction evidence, confirmation gates, safer-alternative recovery, auditability, coarse tool-scope enforcement, and static policy enforcement.
- Tables and result figures are derived from serialized run artifacts.

The artifact does not support these claims:

- PAPF is deployment-ready.
- PAPF proves formal least privilege.
- PAPF improves task success.
- PAPF generalizes to all consumer-agent domains.
- PAPF prompts are empirically understandable to non-experts.
- PAPF improves privacy-preserving consent decisions, perceived control, trust, workload, or consent fatigue.
- Synthetic traces prove human comprehension or user-facing effectiveness.
- PAPF is novel relative to every agent-authorization system.

## Submission Readiness Gaps

- Treat the current trace metrics, ablations, and stronger baselines as supporting feasibility evidence, not the primary HCI/privacy evaluation.
- Expand beyond the first `email + files + browser` slice before making broad consumer-agent generalization claims.
- Run the non-expert privacy-usability study before making comprehension, consent-decision, perceived-control, trust, workload, or fatigue claims.
- Build a bibliography and verify all paper citation keys at submission time.
