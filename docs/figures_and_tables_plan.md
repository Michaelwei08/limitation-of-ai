# Figures and Tables Plan

## Purpose

This document lists likely figures and tables for the first PAPF paper and records what evidence each one depends on. It is a planning document only. No result is implied by inclusion here.

## Likely figures

### Figure 1. PAPF system architecture

- Type:
  conceptual figure
- Purpose:
  show the control-plane split between model-assisted proposal logic and deterministic enforcement logic
- Expected contents:
  user task, intent normalization, capability compiler, policy engine, consent manager, tool mediation, audit logger, and evaluation harness
- Depends on:
  [system_design.md](system_design.md)
- Status:
  ready to draft once the architecture diagram style is chosen

### Figure 2. End-to-end execution flow

- Type:
  conceptual figure
- Purpose:
  walk the reader through task intake, capability issuance, per-call mediation, confirmation, and audit emission
- Expected contents:
  numbered execution steps matching the system-design flow
- Depends on:
  [system_design.md](system_design.md)
- Status:
  ready to draft after the runtime record names are stabilized

### Figure 3. Task-to-capability compilation example

- Type:
  conceptual plus concrete example figure
- Purpose:
  make the compiler contribution tangible
- Expected contents:
  one user task, normalized intent fields, compiled capabilities, dormant high-risk actions, and one denied over-broad request
- Depends on:
  benchmark fixture examples and capability schema details
- Status:
  TODO: requires benchmark implementation

### Figure 4. Benchmark slice and task taxonomy

- Type:
  descriptive figure
- Purpose:
  show the first benchmark release scope and how clean, temptation, attack, and recovery suites relate to the task families
- Expected contents:
  `email + files + browser` slice plus suite types and attack overlays
- Depends on:
  [benchmark_spec.md](benchmark_spec.md)
- Status:
  ready to draft conceptually; final version should wait for fixture inventory

### Figure 5. Policy decision matrix example

- Type:
  explanatory figure
- Purpose:
  illustrate how action, scope, consent level, and policy effect interact
- Expected contents:
  examples of `allow`, `deny`, `require_confirmation`, `allow_with_narrowed_scope`, and `allow_with_redaction`
- Depends on:
  policy schema and at least one concrete task instance
- Status:
  TODO: requires benchmark implementation

### Figure 6. Failure-mode walk-through

- Type:
  qualitative example figure
- Purpose:
  show one attack or over-access case across baseline and PAPF runs
- Expected contents:
  malicious content, requested tool action, PAPF decision, and downstream outcome
- Depends on:
  implemented attack tasks and actual trace outputs
- Status:
  TODO: requires experiment

## Likely tables

### Table 1. Threat model and design goals

- Type:
  design table
- Purpose:
  define attacker capabilities, protected assets, enforcement goals, and explicit non-goals
- Depends on:
  [system_design.md](system_design.md), [research_brief.md](research_brief.md)
- Status:
  ready to draft from current docs

### Table 2. Benchmark task taxonomy

- Type:
  descriptive table
- Purpose:
  summarize task families, suite types, data labels, and representative failure modes
- Depends on:
  [benchmark_spec.md](benchmark_spec.md)
- Status:
  ready for a planning version; final paper version should use implemented tasks

### Table 3. Runtime records and schemas

- Type:
  descriptive table
- Purpose:
  summarize `TaskIntent`, `Capability`, `PolicyDecision`, `ToolCallRecord`, and `AuditEvent`
- Depends on:
  [system_design.md](system_design.md), [benchmark_schema_plan.md](benchmark_schema_plan.md)
- Status:
  ready to draft from current docs

### Table 4. Main metrics table

- Type:
  result table
- Purpose:
  report task success, necessary access, over-access, exfiltration, false allow, false deny, consent burden, recovery quality, and auditability
- Rows:
  broad baseline, prompt-only baseline, PAPF
- Columns:
  main metrics over the full narrow benchmark slice
- Status:
  TODO: requires experiment

### Table 5. Suite-by-suite comparison

- Type:
  result table
- Purpose:
  separate clean, temptation, attack, and recovery performance
- Rows:
  system-by-suite combinations
- Columns:
  selected utility and privacy/security metrics
- Status:
  TODO: requires experiment

### Table 6. Attack and exfiltration outcomes

- Type:
  result table
- Purpose:
  isolate prompt-injection and cross-tool misuse cases
- Rows:
  attack categories or representative tasks
- Columns:
  false allow, exfiltration, blocked attack rate, and task success
- Status:
  TODO: requires experiment

### Table 7. Narrowing and escalation analysis

- Type:
  result table
- Purpose:
  quantify how often PAPF narrows scope or asks for confirmation and what utility cost follows
- Rows:
  action categories or suite types
- Columns:
  narrowing count, confirmation count, successful recovery, false deny contribution
- Status:
  TODO: requires experiment

### Table 8. Audit completeness or traceability

- Type:
  result table
- Purpose:
  show whether runs contain enough structured evidence to reconstruct decisions and data touches
- Rows:
  baseline systems and PAPF
- Columns:
  completeness score or required-field coverage
- Status:
  TODO: requires experiment

### Table 9. Baseline environment and implementation summary

- Type:
  descriptive table
- Purpose:
  ensure reviewers can compare systems fairly
- Depends on:
  actual implementation choices for the shared synthetic environment
- Status:
  TODO: requires benchmark implementation

### Table 10. Failure-case examples

- Type:
  qualitative table
- Purpose:
  summarize representative false allow, false deny, and successful recovery cases
- Columns:
  task, baseline behavior, PAPF behavior, policy rationale, outcome
- Status:
  TODO: requires experiment

### Table 11. Literature positioning matrix

- Type:
  literature table
- Purpose:
  summarize how PAPF differs from benchmark-only, prompt-defense, delegated-authorization, and permission-UX work
- Depends on:
  verified literature review
- Status:
  TODO: requires literature verification

### Table 12. User comprehension or consent-burden study results

- Type:
  result table
- Purpose:
  only include if a dedicated user-study protocol is later added
- Status:
  TODO: requires user study

## Minimum viable figure/table set for the first submission

If the project stays within the current systems framing, the minimum likely paper set is:

1. Figure 1: PAPF system architecture
2. Figure 3: task-to-capability compilation example
3. Table 1: threat model and design goals
4. Table 2: benchmark task taxonomy
5. Table 4: main metrics table
6. Table 5: suite-by-suite comparison
7. Table 10: failure-case examples

## Items to postpone unless evidence matures

- Table 12 should be omitted unless a real user study exists.
- Any cross-domain generalization table should wait until the benchmark extends beyond the first narrow slice.
- Any formal-minimality table should be avoided unless the project develops a defensible minimality criterion.
