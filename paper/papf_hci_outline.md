# HCI/Privacy Outline for PAPF Paper

This outline is the working structure for revising PAPF into an HCI/privacy paper. It intentionally separates implemented technical evidence from user-study evidence that has not yet been collected.

## Mini-outline

- Open with the privacy interaction problem: personal AI agents can act across email, files, browser content, and communication tools, but ordinary users are asked to approve permissions without task-specific visibility.
- Use a reimbursement-email example to show why broad app authorization and generic confirmations are too coarse.
- Present PAPF as an externally enforced task-scoped consent framework, not as a model self-regulation technique.
- Define PAPF-style prompts and consent states as the user-facing layer over deterministic capability enforcement.
- Make the user study the primary HCI/privacy evaluation and the trace benchmark the secondary feasibility evaluation.
- Keep unsupported user-comprehension claims as hypotheses or design goals.

## Section plan

| section | paragraph-level message | evidence needed | user-study dependency |
| --- | --- | --- | --- |
| 1. Introduction | Personal AI agents need task-scoped consent because they combine sensitive data access and executable action. | Motivating scenario, permission UX literature, agent-risk literature, PAPF artifact summary. | Human comprehension claims require study data. |
| 2. Motivating Example | One reimbursement task exposes over-access, malicious webpage instructions, external disclosure, redaction, and auditability needs. | Synthetic scenario and capability mapping. | None for motivation. |
| 3. Background and Privacy Risks | Privacy harms include over-collection, secondary use, cross-context leakage, unauthorized disclosure, exfiltration, and loss of agency. | Privacy principles and prior work. | None unless discussing user perception. |
| 4. PAPF Design Goals | PAPF is designed for data minimization, purpose limitation, consent, transparency, auditability, and external enforcement. | Mechanism-to-principle mapping. | Claims of success require study or trace data. |
| 5. PAPF Architecture | PAPF validates tasks, compiles capabilities, mediates tool calls, gates risky actions, verifies redaction, and writes audits outside the LLM. | Existing implementation and tests. | None. |
| 6. Permission Prompt Design | PAPF prompts should expose task goal, requested access, touched data, external disclosure, redactions, and confirmation reason. | Prompt examples and variants. | Preferences/comprehension require study data. |
| 7. Prototype Implementation | The current prototype operationalizes the design in a deterministic synthetic environment. | Code modules, benchmark cases, synthetic tools, serialized runs. | None. |
| 8. User Study | Non-expert users compare baseline and PAPF-style prompts across realistic privacy-sensitive scenarios. | Protocol, conditions, scenarios, measures, hypotheses. | Core empirical section. |
| 9. Prototype Trace Evaluation | The trace evaluation shows the authority boundary can be executed and scored. | 12-trace run, baselines, ablations, metrics. | None. |
| 10. Results | Report user-study outcomes separately from prototype trace outcomes. | Participant data if available; generated metrics otherwise. | Required for privacy-usability findings. |
| 11. Discussion | Interpret safety versus consent burden and design strategies for reducing friction. | Study findings or planned measures plus trace prompt counts. | User-burden claims require study data. |
| 12. Limitations | Bound participant, task, prompt, lab-study, synthetic-data, and deployment limitations. | Protocol and prototype scope. | Final details depend on study. |
| 13. Related Work | HCI/privacy literature should lead; agent authorization and prompt-injection work should support the argument. | Verified citations. | None. |
| 14. Conclusion | Enforceable task-scoped authority must be paired with permission UX users can understand and act on. | Artifact evidence plus user-study findings if available. | Strong user-facing claims require study data. |

## Claim-evidence guardrails

| claim | allowed current phrasing | disallowed current phrasing |
| --- | --- | --- |
| User comprehension | PAPF is designed to support user comprehension and will be evaluated with non-expert users. | PAPF prompts are understandable to users. |
| Consent decisions | The study will test whether PAPF-style prompts improve privacy-preserving consent decisions. | PAPF improves users' consent decisions. |
| Consent burden | The trace artifact counts confirmation prompts; user burden remains an empirical question. | PAPF reduces consent fatigue. |
| Technical enforcement | PAPF enforces task-scoped decisions outside the LLM in the synthetic prototype. | PAPF is deployment-ready. |
| Benchmark result | PAPF reduces observed over-access in the 12-trace synthetic run. | PAPF generalizes across all personal-agent domains. |
