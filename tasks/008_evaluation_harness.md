# Task 008: Build Evaluation Harness

## Goal

Connect the PAPF runtime foundation to benchmark fixtures and metrics.

This task should implement a small deterministic evaluation harness that can run synthetic benchmark cases through the intent/capability/policy/enforcement pipeline and produce structured metric outputs.

Do not add LLM calls.
Do not integrate real tools.
Do not use real personal data.

## Read first

- `AGENTS.md`
- `CONTINUITY.md`
- existing `src/papf/` modules
- `tests/test_runtime_foundation.py`
- benchmark fixture or validator modules
- `docs/benchmark_spec.md`
- `docs/benchmark_schema_plan.md` if present

## Create or update

Likely files:

- `src/papf/evaluation/`
- `src/papf/evaluation/runner.py`
- `src/papf/evaluation/results.py`
- `tests/test_evaluation_harness.py`

Update `CONTINUITY.md` only if the project state materially changes.

## Requirements

Implement a deterministic evaluation flow:

1. Load or construct benchmark cases.
2. Validate each case.
3. Compile task intent into capabilities.
4. Run candidate tool/action requests through policy enforcement.
5. Record audit events.
6. Compute metrics such as:
   - task success proxy
   - necessary access rate
   - over-access rate
   - false allow
   - false deny
   - confirmation burden
   - auditability completeness
7. Return a structured result object.

## Design constraints

- Keep modules small and under 300 lines.
- Do not implement LLM-based policy decisions.
- Do not call external APIs.
- Do not use real personal data.
- Do not create broad silent fallbacks.
- If benchmark data is malformed, fail clearly.
- Keep the evaluation harness testable without network access.

## Testing

Add focused tests covering:

1. A case where all necessary actions are allowed.
2. A case where unrelated private data access is denied.
3. A case where scope narrowing is required.
4. A case where a send/write action requires confirmation.
5. A case where metrics detect false allow or false deny.
6. A case where audit output is complete.

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests -v
$env:PYTHONPATH='src'; python -m compileall -q src tests

Final output

Report:

Files changed
Evaluation flow implemented
Metrics supported
Tests added and run
Remaining limitations
Whether CONTINUITY.md was updated