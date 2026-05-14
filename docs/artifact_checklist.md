# Artifact Checklist

This checklist tracks the current reproducible PAPF artifact for the first paper draft.

## Scope

- Artifact name: Personal Agent Permission Firewall (PAPF) synthetic evaluation slice.
- Benchmark scope: synthetic `email + files + browser` tasks only.
- Evidence scope: deterministic 12-trace run over PAPF, broad-access, and prompt-only modes.
- Non-evidence scope: no real user data, no production integrations, no completed non-expert user study, no formal least-privilege proof.

## Required Environment

- Python 3.11 or compatible Python with standard-library `unittest`.
- Run commands from the repository root.
- Set `PYTHONPATH=src` because the project uses a `src/` layout.
- Optional: set `PYTHONDONTWRITEBYTECODE=1` and use `python -B` to avoid writing bytecode during verification.

## Reproduce Default Experiment

```powershell
$env:PYTHONPATH='src'; $env:PYTHONDONTWRITEBYTECODE='1'; python -B -m papf.cli run-experiment --config experiments/configs/default_email_files_browser.json --timestamp 2026-04-29T00:00:00+00:00
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

These tables summarize existing benchmark and generated-result artifacts. They should not be treated as independent experiment outputs.

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

The artifact supports these bounded claims:

- PAPF enforces decisions outside the LLM in the current prototype.
- PAPF records zero false allows and zero over-access in the current 12-trace synthetic run.
- Broad-access and prompt-only baselines record 16 false allows each in the same run.
- The current run exposes a utility/safety tradeoff: PAPF has lower task-success proxy and nonzero consent burden.
- Tables and result figures are derived from serialized run artifacts.

The artifact does not support these claims:

- PAPF is deployment-ready.
- PAPF proves formal least privilege.
- PAPF improves task success.
- PAPF generalizes to all consumer-agent domains.
- PAPF prompts are empirically understandable to non-experts.
- PAPF is novel relative to every agent-authorization system.

## Submission Readiness Gaps

- Add ablations for compiler narrowing, redaction evidence, confirmation gating, and audit scoring.
- Add stronger external-enforcement baselines where feasible.
- First stronger-baseline implementation target: coarse tool-scope delegated authorization.
- Second stronger-baseline implementation target: static policy-DSL enforcement over the same benchmark records.
- Expand beyond the first `email + files + browser` slice.
- Include a worked capability-compilation example in the paper.
- Run the non-expert comprehension protocol before making usability claims.
- Build a bibliography and verify all paper citation keys at submission time.
