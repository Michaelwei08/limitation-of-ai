# Paper Plan

## Purpose

This document tracks the active plan for revising PAPF into an HCI/privacy paper. It is not a results report and must not imply that user-comprehension findings exist before a study is run.

## Active framing

- Primary framing: HCI/privacy paper on task-scoped consent and permission UX for personal AI agents.
- Core artifact stack:
  - an externally enforced task-to-capability control plane,
  - PAPF-style permission prompts and consent states,
  - a non-expert user-study protocol,
  - a prototype trace evaluation showing technical feasibility.
- Scope discipline:
  - user comprehension, consent decisions, perceived control, trust, and fatigue are the central empirical questions,
  - the deterministic 12-trace synthetic evaluation is secondary feasibility evidence,
  - non-expert comprehension must remain a hypothesis or design goal until participant data exists.

## Working title options

1. Task-Scoped Consent for Personal AI Agents
2. Human-Centered Permission Boundaries for Personal AI Agents
3. Designing User-Comprehensible Permissions for Consumer AI Agents
4. External Enforcement and Consent UX for Privacy-Preserving AI Agents
5. Personal Agent Permission Firewall: Task-Scoped Consent and External Enforcement

## One-sentence thesis

Personal AI agents should receive externally enforced authority scoped to the user's current task, and permission UX should be evaluated by whether non-expert users can understand, question, and act on that authority without excessive consent burden.

## Candidate contributions

These are planning claims, not final accepted novelty claims.

1. A human-centered problem framing for personal AI-agent privacy as task-scoped consent rather than broad app authorization or prompt-only refusal.
2. The PAPF architecture, which separates model-assisted task interpretation from deterministic capability issuance, runtime enforcement, redaction evidence, confirmation gates, and audit logging.
3. A permission-prompt design space for personal AI agents, including concise, detailed, risk-highlighted, expandable, and audit-preview prompts.
4. A non-expert user-study protocol for measuring prompt comprehension, allow/deny decision quality, perceived control, trust, workload, and consent fatigue.
5. A secondary prototype trace evaluation that validates technical feasibility of scoped enforcement over synthetic email, file, browser, and communication tasks.

## Planned paper structure

### 1. Introduction

- Goal: establish why personal AI agents create a new privacy-permission interaction problem.
- Required evidence: motivating example, privacy UX citations, agent prompt-injection/tool-use citations, and bounded artifact evidence.
- Notes: open with user-facing privacy consequences, not benchmark mechanics.

### 2. Motivating Example

- Goal: make task-scoped authority concrete through a reimbursement-email scenario.
- Required evidence: synthetic example mapping allowed data, disallowed data, malicious webpage content, confirmation, redaction, and auditability.
- Notes: write for non-expert readability before introducing PAPF internals.

### 3. Background and Privacy Risks

- Goal: connect PAPF to privacy harms and principles.
- Required evidence: over-collection, secondary use, cross-context leakage, unauthorized disclosure, prompt-injection-mediated exfiltration, data minimization, purpose limitation, contextual integrity, user consent, transparency, and accountability.
- Notes: avoid generic AI ethics framing by tying each harm to a measurable user or trace outcome.

### 4. PAPF Design Goals

- Goal: state the user-facing and enforcement goals PAPF is designed to support.
- Required evidence: design goals mapped to mechanisms and prompt fields.
- Notes: "designed to support comprehension" is acceptable; "users understand" requires study data.

### 5. PAPF Architecture

- Goal: explain the externally enforced control plane.
- Required evidence: modules, capability example, redaction artifact, confirmation event, audit trace.
- Notes: preserve the invariant that the LLM cannot mint or enforce final permissions.

### 6. Permission Prompt Design

- Goal: define the prompt variants and what information each exposes.
- Required evidence: prompt examples, design dimensions, and scenario mappings.
- Notes: this section prepares the user study; do not claim preference or comprehension yet.

### 7. Prototype Implementation

- Goal: describe the deterministic artifact backing the design.
- Required evidence: benchmark cases, tool adapters, policy engine, enforcement mediator, audit logs, run artifacts.
- Notes: implementation supports feasibility, not deployment readiness.

### 8. User Study

- Goal: evaluate whether PAPF-style prompts help non-expert users make safer privacy decisions.
- Required evidence: participants, conditions, scenarios, measures, hypotheses, procedure, and analysis plan.
- Notes: if the study remains planned, label it as planned and do not include results.

### 9. Prototype Trace Evaluation

- Goal: show that the proposed authority boundaries can be executed and scored.
- Required evidence: 12 traces, baselines, ablations, metrics, provenance.
- Notes: place after the user-study design in the HCI/privacy version.

### 10. Results

- Goal: report user-study findings if available and technical trace findings separately.
- Required evidence: empirical participant data for usability claims; serialized run artifacts for technical claims.
- Notes: do not mix automated trace metrics with human comprehension outcomes.

### 11. Discussion

- Goal: interpret privacy-usability tradeoffs.
- Required evidence: decision quality, false allows, false denials, time, workload, fatigue, and trace-level consent prompts.
- Notes: discuss batching, progressive disclosure, risk-based prompting, remembered preferences, and audit logs as design strategies.

### 12. Limitations

- Goal: bound HCI/privacy and prototype claims.
- Required evidence: participant demographics, task realism, prompt wording, privacy attitudes, lab-study limitations, synthetic data, and prototype scope.
- Notes: state that user comprehension is measured only within tested scenarios.

### 13. Related Work

- Goal: make HCI/privacy literature central and systems/security work supporting.
- Required evidence: privacy permissions, mobile/web permission UX, consent fatigue, privacy notices, human-centered security, agent authorization, prompt injection, and tool-use risks.
- Notes: keep source verification strict.

### 14. Conclusion

- Goal: close on enforceable, task-scoped, understandable permission systems for personal AI agents.
- Required evidence: only claims supported by prototype traces or user-study data.
- Notes: avoid ending primarily with benchmark claims.

## Planned user-study questions

1. Do ordinary users understand PAPF-style permission prompts?
2. Can users distinguish safe from unsafe agent actions using PAPF prompts?
3. Does PAPF improve users' ability to make privacy-preserving consent decisions?
4. Does PAPF increase perceived control and trust?
5. Does PAPF introduce consent fatigue or excessive friction?

## Required evidence by major claim

| Candidate claim | Required evidence | Current status |
| --- | --- | --- |
| Broad personal-agent authorization creates privacy decision problems | Literature plus motivating examples | Partially supported by current literature map |
| PAPF can enforce task-scoped authority outside the LLM | Prototype modules, tests, and trace artifacts | Supported by current artifact |
| PAPF prompts improve unsafe-action detection | User-study decision accuracy and false-allow rates | Unsupported until study is run |
| PAPF improves perceived control or trust | Survey and interview data | Unsupported until study is run |
| PAPF increases decision time or workload | Timing and workload/fatigue measures | Unsupported until study is run |
| PAPF reduces over-access in synthetic traces | Generated metrics and provenance | Supported within current 12-trace suite |
| PAPF is deployable for real personal accounts | Real integration and field evidence | Unsupported; out of scope |

## HCI/privacy revision order

1. `tasks/027_new_hci_privacy_paper_outline.md`
2. `tasks/028_hci_privacy_reframing.md`
3. `tasks/029_title_abstract_hci_privacy.md`
4. `tasks/030_motivating_example_intro.md`
5. `tasks/031_strengthen_privacy_framing.md`
6. `tasks/032_hci_privacy_research_questions.md`
7. `tasks/033_user_study_scenarios.md`
8. `tasks/034_prompt_design_variants.md`
9. `tasks/035_user_study_design.md`
10. `tasks/036_user_study_measures.md`
11. `tasks/037_hci_privacy_hypotheses.md`
12. `tasks/038_rework_evaluation_hci_privacy.md`
13. `tasks/039_consent_fatigue_discussion.md`
14. `tasks/040_related_work_hci_privacy.md`
15. `tasks/041_hci_privacy_limitations.md`
16. `tasks/042_revise_conclusion_hci_privacy.md`
17. `tasks/043_venue_positioning_hci_privacy.md`
18. `tasks/044_user_comprehension_claims.md`
19. `tasks/045_final_hci_consistency_pass.md`

## Unsupported claims to avoid

- PAPF prompts are understandable to non-experts.
- PAPF improves privacy-preserving user decisions.
- PAPF reduces real-world consent fatigue.
- PAPF is deployment-ready for personal accounts.
- PAPF's synthetic traces generalize across consumer-agent domains.
- PAPF grants are formally minimal rather than task-scoped and externally enforced.
