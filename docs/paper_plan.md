# Paper Plan

## Purpose

This document tracks the active plan for revising PAPF into an HCI/privacy paper. It is not a results report and must not imply that user-comprehension findings exist before a study is run.

## Active framing

- Primary framing: HCI/privacy or human-centered security/privacy paper on task-scoped consent and permission UX for personal AI agents.
- Core artifact stack:
  - an externally enforced task-to-capability control plane,
  - PAPF-style permission prompts and consent states,
  - a non-expert user-study protocol,
  - a secondary prototype trace evaluation showing technical feasibility.
- Scope discipline:
  - user comprehension, consent decisions, perceived control, trust, and fatigue are the central empirical questions,
  - the deterministic 12-trace synthetic evaluation is secondary feasibility evidence,
  - non-expert comprehension must remain a hypothesis or design goal until participant data exists.

## Venue positioning rule

- Full-paper target: HCI/privacy or human-centered security/privacy venue, with human-centered privacy, consent interaction design, user comprehension, and empirical evaluation with non-expert users as the lead story.
- Evidence threshold: a full empirical submission should include completed non-expert user-study results. The study should measure comprehension, safe/unsafe action discrimination, consent choices that avoid unnecessary disclosure, perceived control, trust calibration, workload, and consent fatigue.
- Systems/security material: supporting technical feasibility evidence. The capability compiler, runtime policy checks, redaction evidence, confirmation gates, audit logs, baselines, and ablations show that PAPF's consent states can be enforced outside the LLM.
- Benchmark material: supporting measurement infrastructure. The synthetic suite should be described as a local evaluation slice, not as the paper's primary identity.
- Fallback: if the user study remains planned rather than completed, position the work as a bounded HCI/privacy workshop, design, position, or prototype paper. The fallback can contribute the framing, prompt/consent design space, scenario set, protocol, and enforceable prototype, but must not claim empirical user comprehension, improved consent decisions, reduced consent fatigue, or deployment readiness.

## Working title options

1. Task-Scoped Consent for Personal AI Agents
2. Human-Centered Permission Boundaries for Personal AI Agents
3. Designing for User Comprehension in Consumer AI-Agent Permissions
4. External Enforcement and Consent UX for Privacy-Bounded AI Agents
5. Personal Agent Permission Firewall: Task-Scoped Consent and External Enforcement

## One-sentence thesis

Personal AI agents should receive externally enforced authority scoped to the user's current task, and permission UX should be evaluated by whether non-expert users can correctly identify, question, and act on that authority without excessive consent burden.

## Candidate contributions

These are planning claims, not final accepted novelty claims.

1. A human-centered problem framing for personal AI-agent privacy as task-scoped consent rather than broad app authorization or prompt-only refusal.
2. The PAPF architecture, which separates model-assisted task interpretation from deterministic capability issuance, runtime enforcement, redaction evidence, confirmation gates, and audit logging.
3. A permission-prompt design space for personal AI agents, including concise, detailed, risk-highlighted, expandable, and audit-preview prompts.
4. A primary non-expert privacy-usability evaluation protocol for measuring prompt comprehension, allow/deny decision quality, perceived control, trust, workload, and consent fatigue.
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

### 4. Research Questions and Evidence Plan

- Goal: make the HCI/privacy questions explicit before design and evaluation details.
- Required evidence: an RQ table mapping each question to user-study evidence, prototype trace evidence, or both.
- Notes: RQ1-RQ5 require participant data; RQ6 is the prototype feasibility question addressed by synthetic traces.

### 5. PAPF Design Goals

- Goal: state the user-facing and enforcement goals PAPF is designed to support.
- Required evidence: design goals mapped to mechanisms and prompt fields.
- Notes: design-goal language is acceptable; positive comprehension claims require study data.

### 6. PAPF Architecture

- Goal: explain the externally enforced control plane.
- Required evidence: modules, capability example, redaction artifact, confirmation event, audit trace.
- Notes: preserve the invariant that the LLM cannot mint or enforce final permissions.

### 7. Permission Prompt Design

- Goal: define the prompt variants and what information each exposes.
- Required evidence: prompt examples, design dimensions, and scenario mappings.
- Notes: this section prepares the user study; do not claim preference or comprehension yet.

### 8. Prototype Implementation

- Goal: describe the deterministic artifact backing the design.
- Required evidence: benchmark cases, tool adapters, policy engine, enforcement mediator, audit logs, run artifacts.
- Notes: implementation supports feasibility, not deployment readiness.

### 9. Primary Privacy-Usability Evaluation: User Study

- Goal: make the user study the core HCI/privacy evaluation of whether people correctly interpret and act on task-scoped permission boundaries.
- Required evidence: participants, conditions, scenarios, measures, hypotheses, procedure, and analysis plan.
- Notes: if the study remains planned, label it as planned and do not include results; still place it before prototype trace evaluation to preserve the privacy-usability framing.

### 10. Secondary Prototype Feasibility Evaluation

- Goal: show that the proposed authority boundaries can be executed and scored.
- Required evidence: 12 traces, baselines, ablations, metrics, provenance.
- Notes: label this section secondary or feasibility-focused; it shows enforcement behavior, not human comprehension.

### 11. Results

- Goal: report user-study findings if available, then report technical trace findings separately as feasibility evidence.
- Required evidence: empirical participant data for usability claims; serialized run artifacts for technical claims.
- Notes: if no participant data exists, say that RQ1-RQ5 remain unanswered; do not mix automated trace metrics with human comprehension, consent quality, perceived control, trust, or fatigue outcomes.

### 12. Discussion

- Goal: interpret privacy-usability tradeoffs.
- Required evidence: decision quality, false allows, false denials, time, workload, fatigue, and trace-level consent prompts.
- Notes: discuss batching, progressive disclosure, risk-based prompting, remembered preferences, and audit logs as design strategies.

### 13. Limitations

- Goal: bound HCI/privacy and prototype claims.
- Required evidence: participant demographics, task realism, prompt wording, privacy attitudes, lab-study limitations, synthetic data, and prototype scope.
- Notes: state that user comprehension is measured only within tested scenarios.

### 14. Related Work

- Goal: make HCI/privacy literature central and systems/security work supporting.
- Required evidence: privacy permissions, mobile/web permission UX, consent fatigue, privacy notices, human-centered security, agent authorization, prompt injection, and tool-use risks.
- Notes: keep source verification strict.

### 15. Conclusion

- Goal: close on enforceable, task-scoped permission systems designed for empirical user-comprehension evaluation in personal AI agents.
- Required evidence: only claims supported by prototype traces or user-study data.
- Notes: avoid ending primarily with benchmark claims.

## Research questions and evidence mapping

| RQ | Question | Evidence source | Measure mapping | Current status |
| --- | --- | --- | --- | --- |
| RQ1 | Can ordinary users correctly identify the authority shown in PAPF-style permission prompts for task-scoped personal-agent authority? | Planned non-expert user study. | Comprehension score, allowed-data recognition, blocked-data recognition, confirmation-gate recognition, redaction understanding, audit-summary comprehension. | Planned; no participant result yet. |
| RQ2 | Can users distinguish safe from unsafe agent actions when PAPF prompts expose task scope, disclosure, redaction, and confirmation state? | Planned non-expert user study. | Allow/deny decision accuracy, false allows, false denies, exfiltration recognition, untrusted-instruction recognition. | Planned; no participant result yet. |
| RQ3 | Does PAPF improve consent decisions that avoid unnecessary disclosure relative to raw tool permissions or generic warnings? | Planned comparison across prompt conditions. | Condition differences in decision quality, false-allow rate, false-deny rate, recovery choices after broad or denied requests, confidence calibration. | Planned; no participant result yet. |
| RQ4 | Does PAPF change perceived control and trust in personal-agent actions? | Planned survey and optional interview/free-response measures. | Perceived control, trust, confidence, trust calibration, and explanation themes. | Planned; no participant result yet. |
| RQ5 | Does PAPF increase consent fatigue or excessive friction? | Planned user study plus prototype prompt counts as supporting context. | Self-reported burden, workload, time-on-item, perceived interruption, prompt count, confirmation count, and task-completion effects. | Human fatigue planned; trace prompt counts already available. |
| RQ6 | Can externally enforced task-scoped capabilities mediate personal-agent traces while reducing over-access and false allows? | Implemented deterministic prototype trace evaluation. | Task-success proxy, necessary-access rate, over-access rate, false allows, false denies, consent prompts, recovery quality, auditability completeness, and ablation/baseline comparisons. | Supported only within the current 12-trace synthetic suite. |

RQ1-RQ5 are the central HCI/privacy questions and require user-study evidence.
RQ6 is the technical feasibility question addressed by prototype traces. Trace
logs may motivate RQ5 by counting prompts, but they cannot establish fatigue.

## Evaluation framing rule

The paper's evaluation should be ordered and worded as follows:

1. Primary privacy-usability evaluation: planned or completed user study for comprehension, consent decisions, perceived control, trust, workload, and consent fatigue.
2. Secondary prototype feasibility evaluation: 12-trace synthetic artifact for enforcement behavior, false allows, over-access, redaction, confirmation gates, recovery, auditability, baselines, and ablations.
3. Results boundary: trace metrics can show that PAPF can enforce scoped decisions in the prototype; only participant data can show whether people correctly interpret and act on those decisions.
4. Venue boundary: without completed participant data, the paper should fall back to workshop, design, or prototype positioning rather than presenting itself as a full empirical HCI/privacy paper or a primary systems/security benchmark paper.

## HCI/privacy claim-evidence map

| Candidate claim | Required evidence | Current status |
| --- | --- | --- |
| Broad personal-agent authorization creates privacy decision problems | Literature plus motivating examples | Partially supported by current literature map |
| PAPF can enforce task-scoped authority outside the LLM | Prototype modules, tests, and trace artifacts | Supported by current artifact |
| PAPF prompt and consent materials are ready for non-expert evaluation | Scenario records, prompt variants, measures, and protocol | Supported as study design |
| Ordinary-user comprehension of PAPF prompts | User-study comprehension and audit-summary interpretation scores | Unsupported until study is run |
| PAPF prompts improve unsafe-action detection | User-study decision accuracy and false-allow rates | Unsupported until study is run |
| PAPF improves consent decisions that avoid unnecessary disclosure | User-study comparison against raw tool permissions and generic warnings | Unsupported until study is run |
| PAPF improves perceived control or trust | Survey and interview data | Unsupported until study is run |
| PAPF increases decision time or workload | Timing and workload/fatigue measures | Unsupported until study is run |
| PAPF reduces over-access in synthetic traces | Generated metrics and provenance | Supported within current 12-trace suite |
| Prototype trace metrics establish user comprehension, consent quality, perceived control, trust, or fatigue | Participant decisions, timing, survey, and qualitative data | Unsupported and explicitly rejected |
| Prototype prompt counts alone establish human consent fatigue | Participant timing, workload, interruption, and fatigue measures | Unsupported; trace prompt counts are supporting context only |
| PAPF is deployable for real personal accounts | Real integration and field evidence | Unsupported; out of scope |
| PAPF is ready as a full empirical HCI/privacy submission | Completed non-expert study plus prototype evidence | Unsupported until study is run |
| PAPF can be positioned as a bounded workshop/design/prototype paper | Clear claim boundaries plus protocol and trace artifacts | Supported if user-study results remain planned |

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

- Current non-expert comprehension of PAPF prompts.
- PAPF improves user consent decisions that avoid unnecessary disclosure.
- PAPF reduces real-world consent fatigue.
- PAPF is deployment-ready for personal accounts.
- PAPF's synthetic traces generalize across consumer-agent domains.
- PAPF grants are formally minimal rather than task-scoped and externally enforced.
