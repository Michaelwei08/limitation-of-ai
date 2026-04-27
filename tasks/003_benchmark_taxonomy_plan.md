# Task 003: Benchmark Taxonomy and Schema Plan

## Goal

Create a concrete benchmark design plan for NonExpert-AgentPermBench.

This task should design the benchmark structure and schema, not implement code and not generate a full dataset yet.

## Read first

- `AGENTS.md`
- `CONTINUITY.md`
- `docs/research_brief.md`
- `docs/benchmark_spec.md`
- `docs/system_design.md`
- `docs/research_gap.md` if it exists
- `docs/lit_matrix.md` if it exists

## Create or update

- Update `docs/benchmark_spec.md`
- Create `docs/benchmark_schema_plan.md`
- Update `CONTINUITY.md` only if the project state materially changes

## Benchmark goal

The benchmark should evaluate whether an AI agent can complete consumer tasks while respecting task-scoped permission boundaries.

It should measure both:

- task utility
- privacy/security failure modes

## Design these benchmark components

1. Task categories

Examples:

- email
- calendar
- contacts
- files
- browser
- travel booking
- payments
- messaging
- cloud/device management

2. Data categories

Examples:

- necessary data
- unnecessary but available data
- sensitive data
- dangerous data
- unrelated private data
- tool-output adversarial content

3. Tool actions

Examples:

- read
- search
- summarize
- send
- forward
- upload
- download
- delete
- purchase
- authorize payment
- post externally

4. Policy labels

Examples:

- allow
- deny
- require confirmation
- allow with redaction
- allow with narrowed scope
- require safer alternative

5. Attack cases

Examples:

- indirect prompt injection
- data exfiltration request
- over-broad access request
- confused-deputy scenario
- malicious document
- malicious webpage
- malicious email

6. Metrics

Include:

- task success
- necessary access rate
- over-access rate
- exfiltration rate
- false allow
- false deny
- consent burden
- recovery quality
- auditability

## `docs/benchmark_schema_plan.md` format

Include:

1. Design principles
2. Proposed task record schema
3. Proposed tool-call record schema
4. Proposed policy record schema
5. Proposed audit record schema
6. Proposed metric definitions
7. Example benchmark task templates
8. Open design questions

Use pseudocode or YAML-like examples if helpful, but do not implement code.

## Requirements

- Do not create actual large benchmark data yet.
- Do not invent results.
- Do not claim the benchmark is validated.
- Keep examples synthetic and privacy-safe.
- Make the schema easy to implement later in Python.
- Keep the design modular.

## Final output

Report:

1. Schema files created or updated
2. Key benchmark design choices
3. Open questions
4. Whether `CONTINUITY.md` was updated