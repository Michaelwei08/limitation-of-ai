# Paper Outline

## Current paper story

The active paper framing is an HCI/privacy paper on task-scoped consent for personal AI agents. PAPF is the artifact used to study the design problem: personal AI agents need authority boundaries that are externally enforced, scoped to the user's current task, and understandable enough for non-expert users to make consent decisions.

The prototype trace evaluation remains useful, but it is secondary. It shows that PAPF can enforce scoped tool access, redaction, confirmation gates, and audit traces in a synthetic `email + files + browser` environment. It does not establish that users understand PAPF prompts or that the design reduces real-world consent fatigue.

## Selected title direction

**Human-Centered Permission Boundaries for Personal AI Agents: Task-Scoped Consent with External Enforcement**

This direction foregrounds the HCI/privacy contribution while keeping the technical mechanism visible. "Human-centered permission boundaries" signals user comprehension and consent UX; "task-scoped consent" names the privacy-usability design target; "external enforcement" preserves the core PAPF thesis that the model cannot be the permission authority.

## Working title options

1. Human-Centered Permission Boundaries for Personal AI Agents: Task-Scoped Consent with External Enforcement
2. Task-Scoped Consent for Personal AI Agents
3. Designing User-Comprehensible Permissions for Consumer AI Agents
4. External Enforcement and Consent UX for Privacy-Preserving AI Agents
5. Personal Agent Permission Firewall: Task-Scoped Consent and External Enforcement

## One-sentence thesis

Personal AI agents should operate under externally enforced, task-scoped authority boundaries, and HCI/privacy evaluation should test whether non-expert users can understand those boundaries, identify unsafe actions, and make privacy-preserving consent decisions without unacceptable consent burden.

## Abstract claim boundaries

- Problem statement: personal AI agents have broad tool and data access across sensitive consumer contexts, making permissioning a privacy-usability problem rather than only a systems problem.
- Approach statement: PAPF enforces task-scoped authority outside the model through validated task records, compiled capabilities, mediated tool calls, consent gates, redaction artifacts, and audit traces.
- Evaluation statement: the current prototype trace evaluation is reported as technical feasibility evidence; the non-expert user study is designed to evaluate permission comprehension, allow/deny decision quality, perceived control, workload, and consent burden.
- Evidence boundary: because the user study has not been run, the abstract must say "we design" or "we plan to evaluate" for comprehension and consent-burden outcomes, and must not say "we find" or imply completed user evidence.
- Contribution statement: the paper contributes a human-centered privacy framing, an externally enforced architecture, a prompt and consent-state design space, and a planned privacy-usability evaluation separated from prototype trace evidence.

## Core claims the paper may support

- Consumer AI agents create privacy risks because they combine sensitive personal data, cross-tool workflows, and executable actions.
- Broad app-level authorization and generic confirmation prompts are poorly matched to task-specific privacy decisions.
- PAPF provides an artifact-backed design for task-scoped authority, redaction, consent gating, and auditability outside the LLM.
- PAPF-style prompts are designed to support user comprehension, but whether they actually do so is an empirical question for a user study.
- The prototype trace evaluation supports feasibility of external enforcement; it does not by itself support user-comprehension or consent-fatigue claims.

## Proposed structure

### 1. Introduction

- Message: Personal AI agents need permission systems that users can understand and act on because these agents combine sensitive data access with external actions.
- Evidence needed: motivating examples, privacy-permission literature, prompt-injection/tool-use literature, and bounded PAPF prototype evidence.
- User-study dependency: final claims about user comprehension, trust, and fatigue require participant data.

### 2. Motivating Example

- Message: A reimbursement-email task makes the permission problem concrete for non-expert readers.
- Evidence needed: synthetic example where the agent should summarize one email, avoid unrelated tax documents, ignore malicious webpage instructions, and request confirmation before sending private information.
- User-study dependency: none for motivation, but any claim that users find the example clear requires study evidence.

### 3. Background and Privacy Risks

- Message: The central privacy harms are over-collection, secondary use, cross-context leakage, unauthorized disclosure, prompt-injection-mediated exfiltration, and loss of user agency.
- Evidence needed: privacy principles, permission UX work, consent-fatigue work, agent authorization work, and prompt-injection/tool-risk work.
- User-study dependency: none for threat framing; human perception claims require user evidence.

### 4. PAPF Design Goals

- Message: PAPF is designed around externally enforced task scope, user-facing consent, data minimization, purpose limitation, transparency, and auditability.
- Evidence needed: design goals tied to implemented mechanisms and prompt examples.
- User-study dependency: whether the goals are met for users requires study results.

### 5. PAPF Architecture

- Message: PAPF keeps final authority outside the LLM through validated intent records, capability compilation, policy checks, redaction evidence, confirmation gates, and audit traces.
- Evidence needed: implementation-aligned module boundaries, architecture figure, capability example, and enforcement tests.
- User-study dependency: none for technical architecture.

### 6. Permission Prompt Design

- Message: PAPF's user-facing layer should make task goal, requested access, data touched, external disclosure, redaction, and confirmation reason visible at the right level of detail.
- Evidence needed: prompt variants, design rationale, and examples.
- User-study dependency: prompt comprehension and preference claims require participant data.

### 7. Prototype Implementation

- Message: The current prototype operationalizes the design in a deterministic synthetic email-files-browser environment.
- Evidence needed: code modules, benchmark cases, synthetic tool adapters, redaction artifacts, audit logs, and serialized runs.
- User-study dependency: none for feasibility.

### 8. User Study

- Message: The primary HCI/privacy evaluation should test whether non-expert users understand PAPF-style prompts and make safer privacy decisions.
- Evidence needed: participant population, conditions, scenarios, tasks, measures, hypotheses, and analysis plan.
- User-study dependency: this section is planned until the study is run; final paper claims require collected data.

### 9. Prototype Trace Evaluation

- Message: The trace evaluation verifies that PAPF can enforce the scoped decisions used in the prompt and study design.
- Evidence needed: 12-trace synthetic suite, baselines, ablations, metrics, and provenance.
- User-study dependency: none, but interpretation must stay technical.

### 10. Results

- Message: Results should separate privacy-usability evidence from technical feasibility evidence.
- Evidence needed: user-study results if available; otherwise only prototype trace results should be reported.
- User-study dependency: user comprehension, decision quality, trust, control, workload, and fatigue claims require participant data.

### 11. Discussion

- Message: Discuss the design tradeoff between privacy protection and consent burden.
- Evidence needed: observed trace tradeoffs, user-study evidence if available, and design strategies such as progressive disclosure, batching, risk-based prompting, remembered preferences, and audit logs.
- User-study dependency: any statement about what users prefer or tolerate requires study evidence.

### 12. Limitations

- Message: Bound both the prototype and the HCI/privacy evaluation.
- Evidence needed: synthetic-data limitation, participant demographics, task realism, prompt wording, privacy attitudes, lab-study limits, and deployment-readiness caveats.
- User-study dependency: final validity threats depend on actual study design.

### 13. Related Work

- Message: Position PAPF at the intersection of privacy permissions, consent UX, human-centered security, AI-agent authorization, prompt injection, and tool-use risks.
- Evidence needed: verified citations for permission UX, consent fatigue, privacy notices, agent authorization, and agent safety.
- User-study dependency: none for literature positioning.

### 14. Conclusion

- Message: Personal AI agents need permission systems that are enforceable, task-scoped, and designed for users to understand and act on.
- Evidence needed: bounded summary of artifact feasibility and planned or completed user-study evidence.
- User-study dependency: do not conclude that PAPF improves user decisions unless the study supports it.

## Evidence expectations by paper claim

| Claim type | Required evidence | Current status |
| --- | --- | --- |
| PAPF enforces authority outside the LLM | Architecture, implementation, tests, and trace artifacts | Supported by current artifact |
| PAPF reduces over-access in the synthetic trace suite | Serialized trace evaluation and generated tables | Supported within the 12-trace synthetic suite |
| PAPF prompts are understandable to non-experts | User-study comprehension and decision data | Not yet supported |
| PAPF improves privacy-preserving consent decisions | User-study allow/deny accuracy and false-allow/false-deny outcomes | Not yet supported |
| PAPF increases perceived control or trust | Survey/interview data | Not yet supported |
| PAPF increases consent burden | Time, workload, fatigue, and prompt-count measures | Partially supported technically by prompt counts; user burden needs study data |
| PAPF is deployment-ready | Field deployment, real integrations, longitudinal safety/usability evidence | Unsupported; do not claim |

## Writing order

1. Finalize the HCI/privacy outline and paper story.
2. Reframe title, abstract, introduction, and contributions.
3. Add the motivating example and privacy-risk framing.
4. Specify research questions, scenarios, prompt variants, study design, measures, and hypotheses.
5. Rework evaluation so the user study is primary and prototype traces are secondary.
6. Revise discussion, limitations, related work, and conclusion.
7. Run a final claim-evidence and unsupported-comprehension consistency pass.
