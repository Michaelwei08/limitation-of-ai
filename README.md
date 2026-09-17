# Personal Agent Permission Firewall

Personal Agent Permission Firewall (PAPF) is a research project on task-scoped permission boundaries for consumer AI agents. The project studies whether an agent can complete realistic personal-assistant tasks while exposing only the data and capabilities that are necessary for that task.

The current repo contains a deterministic PAPF prototype, a synthetic `email + files + browser` benchmark slice, baseline runners, serialized experiment artifacts, paper-ready tables and figures, and a bounded paper draft. The implementation is a research artifact, not a production agent system.

## Research focus

- Task-scoped permissions for consumer AI agents
- User-comprehensible permission boundaries
- Enforceable runtime checks outside the LLM
- Synthetic benchmark tasks across common personal-agent domains
- Evaluation of utility, privacy, and security tradeoffs

## Current status

- PAPF runtime foundation implemented with intent records, capability compilation, policy validation, enforcement mediation, consent handling, redaction artifacts, audit logs, and metric computation.
- File-backed synthetic benchmark cases cover 12 traces across clean, temptation, attack, redaction, confirmation, cross-tool exfiltration, and recovery scenarios.
- Baseline modes include broad ambient access, prompt-only advisory guardrails, coarse tool-scope delegated authorization, and static-policy enforcement over the same synthetic tool environment.
- Ablation modes cover scope narrowing, redaction evidence, confirmation gating, safer-alternative recovery, and audit-completeness validation.
- Default serialized run artifacts live under `experiments/runs/default_email_files_browser/`.
- Paper tables and figures live under `paper/tables/` and `paper/figures/`.
- A bounded paper draft lives at `paper/papf_draft.md`.

## Repo layout

```text
.
|-- AGENTS.md
|-- CONTINUITY.md
|-- README.md
|-- docs/
|   |-- artifact_checklist.md
|   |-- benchmark_spec.md
|   |-- paper_outline.md
|   |-- related_work.md
|   |-- research_brief.md
|   `-- system_design.md
|-- experiments/
|   |-- configs/
|   `-- runs/
|-- paper/
|   |-- figures/
|   `-- tables/
|-- src/
|   `-- papf/
`-- tests/
```

## Key documents

- `docs/research_brief.md`: project argument, research questions, and venue framing
- `docs/benchmark_spec.md`: benchmark goals, task structure, attacks, and metrics
- `docs/system_design.md`: PAPF layer decomposition and enforcement model
- `docs/related_work.md`: verified seed literature map
- `docs/paper_outline.md`: candidate paper structure
- `docs/artifact_checklist.md`: reproduction commands, supported claims, and submission gaps
- `paper/papf_draft.md`: current bounded paper draft

## Implemented areas

- Intent analysis and non-authoritative model-assisted proposal interfaces
- Capability compilation for generating narrow permissions from task records
- Runtime policy enforcement for tool-call checks outside the LLM
- Risk-adaptive consent, redaction evidence, and safer-alternative recovery scoring
- Synthetic email, files, and browser tool adapters
- Deterministic evaluation, baseline comparison, serialization, and artifact-derived reporting

## Reproducing the default experiment

Run from the repository root:

```powershell
$env:PYTHONPATH='src'; $env:PYTHONDONTWRITEBYTECODE='1'; python -B -m papf.cli run-experiment --config experiments/configs/default_email_files_browser.json --timestamp 2026-04-29T00:00:00+00:00
```

Regenerate paper tables and generated result figures:

```powershell
$env:PYTHONPATH='src'; $env:PYTHONDONTWRITEBYTECODE='1'; python -B -c "from papf.evaluation.reporting import generate_reporting_artifacts; generate_reporting_artifacts('experiments/runs/default_email_files_browser')"
```

Run tests:

```powershell
$env:PYTHONPATH='src'; $env:PYTHONDONTWRITEBYTECODE='1'; python -B -m unittest discover -s tests -v
```

## Evidence boundaries

- Supported by current artifacts: PAPF records zero false allows and zero over-access in the current 12-trace synthetic run, while broad-access and prompt-only baselines each record 16 false allows.
- **Read that zero as close to tautological, and do not quote it as a safety
  result.** The decision path is rule-based and deterministic by design
  (`D008`), and it is scored against hand-authored synthetic seed cases
  (`benchmarks/papf_seed_cases/*.yaml`, `synthetic: true`) whose
  `success_criteria` / `failure_criteria` were written by the same author, in
  the same file, as the policy pack they are evaluated against. A deterministic
  rule engine reproducing labels its author wrote is a check that the
  implementation matches the spec — useful, and not evidence that the spec is
  right or that the result generalizes. The baselines' 16 false allows are
  informative about the *baselines*; PAPF's 0 is mostly informative about the
  fixture.
  This caveat is back-ported from the sibling VMAG project, which published a
  `policy_error = 0.0` of exactly this shape on co-designed cases and withdrew
  it after its own tautology audit (`VMAG-D071`). PAPF never received that
  audit; this note records the defect rather than pretending it was measured
  away. An independent-author case set, or cases the policy was not fitted to,
  is what would make the number mean something.
- Also supported: the current run exposes a utility/safety tradeoff; PAPF has lower task-success proxy and nonzero consent burden.
- Not supported yet: production readiness, formal least privilege, broad domain generality, stronger task success, or empirical non-expert comprehension.

## Contributing

- Keep changes modular and reviewable.
- Do not invent citations, results, or implementation claims.
- Mark uncertain claims as `TODO` or `UNCONFIRMED`.
- Prefer synthetic data for any benchmark or demo artifacts.
