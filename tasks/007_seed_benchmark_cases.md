# Task 007: Create Seed Benchmark Cases

## Goal

Create the first seed benchmark cases for the Checkpointed Adaptive Reasoning project.

This task should create a small, high-quality synthetic benchmark seed set. Do not implement the full benchmark loader or evaluation code yet.

## Read first

- `AGENTS.md`
- `CONTINUITY.md`
- `docs/research_brief.md`
- `docs/research_gap.md`
- `docs/benchmark_spec.md`
- `docs/benchmark_schema_plan.md`
- `docs/system_design.md`
- `docs/related_work.md`
- `docs/lit_matrix.md` if it exists

## Create or update

- Create `benchmarks/seed_cases/`
- Create `benchmarks/seed_cases/README.md`
- Create `benchmarks/seed_cases/cases.yaml`
- Create `docs/benchmark_case_design_notes.md`
- Update `docs/benchmark_spec.md` if needed
- Update `CONTINUITY.md` only if the project state materially changes

## Project framing

The main research question is:

> How can long-running LLM reasoning incorporate mid-task user input without discarding useful prior computation?

The benchmark should evaluate whether a system can:

1. classify mid-task user input,
2. identify reusable prior work,
3. identify invalidated prior assumptions or conclusions,
4. locally replan instead of restarting,
5. preserve final answer consistency with the latest user intent,
6. avoid wasting prior reasoning.

## Scope

Create 10–20 synthetic seed cases.

Use diverse domains:

- long-form writing
- literature review
- coding/debugging
- data analysis
- math/reasoning
- research planning
- document analysis
- tool-using workflow
- email/calendar-style planning
- travel or itinerary planning

## Required case schema

Each case in `cases.yaml` should use this structure:

```yaml
- id: car_seed_001
  domain: literature_review
  initial_task: "..."
  checkpoint_state:
    task_goal: "..."
    latest_user_intent: "..."
    constraints:
      - "..."
    completed_steps:
      - "..."
    pending_steps:
      - "..."
    assumptions:
      active:
        - "..."
      invalidated:
        - "..."
    evidence:
      reusable:
        - "..."
      affected:
        - "..."
    partial_conclusions:
      reusable:
        - "..."
      needs_revision:
        - "..."
    uncertainties:
      - "..."
    next_action: "..."
  mid_task_input:
    text: "..."
    input_type: constraint_change
  expected_reuse:
    - "..."
  expected_invalidate:
    - "..."
  expected_local_replan:
    - "..."
  expected_final_answer_properties:
    - "..."
  forbidden_behavior:
    - "..."
  metrics:
    - reuse_accuracy
    - invalidation_accuracy
    - local_replanning_quality
    - final_answer_consistency
    - wasted_reasoning_tokens
Mid-task input types to cover

Cover at least these types:

addition
revision
correction
constraint change
scope reduction
scope expansion
format override
abort
topic switch
ambiguous input
safety override
Naive baselines to keep in mind

Cases should make it possible to compare against:

Ignore until done
Hard restart
Blind append and continue
Summarize partial output then restart
LLM-only replanning
Checkpointed adaptive continuation
Quality requirements

Each case should make clear:

what prior work remains useful,
what prior work becomes invalid,
why full restart is unnecessary or necessary,
what local replanning should do,
what behavior should be penalized.

Do not include real private data.

Do not use real personal emails, calendars, documents, credentials, or private conversations.

Keep all cases synthetic.

benchmarks/seed_cases/README.md

Explain:

Purpose of the seed benchmark cases
Case schema
How cases relate to the research question
How future evaluation may use them
Current limitations
docs/benchmark_case_design_notes.md

Include:

Design principles
Coverage of input types
Coverage of task domains
Labeling assumptions
Open questions
Risks of ambiguity
What needs expert or human validation later
Do not do
Do not implement Python code yet.
Do not create a large dataset.
Do not claim the benchmark is validated.
Do not invent experimental results.
Do not include raw chain-of-thought.
Do not use real private data.
Do not overfit all cases to one domain.
Final output

Report:

Number of seed cases created
Domains covered
Input types covered
Weakest case categories
Open labeling questions
Whether CONTINUITY.md was updated