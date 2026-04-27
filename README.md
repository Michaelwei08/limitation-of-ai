# Personal Agent Permission Firewall

Personal Agent Permission Firewall (PAPF) is a research project on task-scoped permission boundaries for consumer AI agents. The project studies whether an agent can complete realistic personal-assistant tasks while exposing only the data and capabilities that are necessary for that task.

The current repo state is an initialization scaffold. It contains the project framing, an initial benchmark specification, and a system design outline. It does not yet implement the PAPF runtime, benchmark loader, evaluation pipeline, or experiments.

## Research focus

- Task-scoped permissions for consumer AI agents
- User-comprehensible permission boundaries
- Enforceable runtime checks outside the LLM
- Synthetic benchmark tasks across common personal-agent domains
- Evaluation of utility, privacy, and security tradeoffs

## Current status

- Documentation scaffold created
- Repo layout initialized
- Benchmark and system design specified at a high level
- No code, experiments, or results yet

## Repo layout

```text
.
|-- AGENTS.md
|-- CONTINUITY.md
|-- README.md
|-- docs/
|   |-- benchmark_spec.md
|   |-- paper_outline.md
|   |-- related_work.md
|   |-- research_brief.md
|   `-- system_design.md
|-- experiments/
|   |-- configs/
|   `-- runs/
|-- paper/
|-- src/
|   `-- papf/
`-- tests/
```

## Key documents

- `docs/research_brief.md`: project argument, research questions, and venue framing
- `docs/benchmark_spec.md`: benchmark goals, task structure, attacks, and metrics
- `docs/system_design.md`: PAPF layer decomposition and enforcement model
- `docs/related_work.md`: placeholder map of literature categories to survey
- `docs/paper_outline.md`: candidate paper structure

## Planned implementation areas

- Intent analysis for turning user tasks into structured task descriptions
- Capability compilation for generating narrow permissions from intent
- Runtime policy enforcement for tool-call checks outside the LLM
- Risk-adaptive consent for escalation and denial handling
- Audit logging and evaluation over synthetic benchmark tasks

## Running future experiments

No runnable system exists yet. A likely future workflow is:

1. Add benchmark definitions under `src/papf/benchmark/` and configs under `experiments/configs/`.
2. Implement evaluation code and tests.
3. Run experiments and store outputs in `experiments/runs/`.
4. Validate that reported metrics come from code-generated results only.

## Contributing

- Keep changes modular and reviewable.
- Do not invent citations, results, or implementation claims.
- Mark uncertain claims as `TODO` or `UNCONFIRMED`.
- Prefer synthetic data for any benchmark or demo artifacts.
