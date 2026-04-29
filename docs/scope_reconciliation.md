# Scope Reconciliation

## Decision

`benchmarks/seed_cases/` stays in the repository for now as a quarantined auxiliary artifact, but it is not part of PAPF, NonExpert-AgentPermBench, or the first paper's evidence base.

The primary project remains PAPF: task-scoped external permission enforcement for consumer AI agents.

## Rationale

Task 007 requested Checkpointed Adaptive Reasoning seed cases, which do not match the PAPF project goal in [AGENTS.md](../AGENTS.md). The files were completed as written, but using them as PAPF benchmark evidence would blur the research contribution and create false continuity between two different projects.

The safe choice is to retain the files without deletion or renaming until the user explicitly decides whether to move them out. This preserves work while preventing accidental use in PAPF claims.

## Affected Files

- [benchmarks/seed_cases/README.md](../benchmarks/seed_cases/README.md)
- [benchmarks/seed_cases/cases.yaml](../benchmarks/seed_cases/cases.yaml)
- [docs/benchmark_case_design_notes.md](benchmark_case_design_notes.md)
- [tasks/007_seed_benchmark_cases.md](../tasks/007_seed_benchmark_cases.md)

## Operating Rule

- Do not cite `benchmarks/seed_cases/` as PAPF benchmark evidence.
- Do not use Checkpointed Adaptive Reasoning cases in PAPF metric tables.
- Do not delete, rename, or move the files without explicit user confirmation.
- If retained long term, move them to a clearly separate project namespace or repository.

## Next Step

Continue PAPF via [tasks/011_evaluation_run_serialization.md](../tasks/011_evaluation_run_serialization.md), which directly advances the current deterministic evaluation path.
