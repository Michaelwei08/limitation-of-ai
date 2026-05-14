# Research Gap and Positioning

## 1. Working thesis

- Working hypothesis: PAPF's strongest possible contribution is not any single idea in isolation, but the combination of four elements in one consumer-agent setting:
  1. task-scoped least-privilege capability compilation,
  2. runtime enforcement outside the LLM,
  3. permission boundaries that non-expert users can plausibly understand, and
  4. evaluation across task utility, concrete privacy harms, and security failure modes.
- The verified seed map still suggests a possible gap at that intersection. Existing work already covers important pieces of the problem, but the current checked sources do not yet show a paper that fully combines all four.
- The most defensible near-term claim is therefore a human-centered privacy contribution with an enforceable systems artifact and evaluation protocol, not a claim that PAPF is categorically the first or only approach.
- `UNCONFIRMED`: a deeper literature pass may surface adjacent work on agent authorization, policy enforcement, or user-facing permission mediation that narrows this gap.

## 2. Privacy harm framing

- PAPF should describe privacy harms before or alongside security failures. The harms are over-collection, secondary use, cross-context leakage, unauthorized disclosure, prompt-injection-mediated data exfiltration, and loss of user agency.
- The measurable consequence of over-collection is unnecessary data touched during a run; PAPF measures it with necessary-access and over-access rates.
- The measurable consequence of secondary use is data collected for one task purpose being used for another; PAPF should bind capabilities to a purpose and count off-purpose false allows or unsafe workarounds.
- The measurable consequence of cross-context leakage is data from one personal context moving into another workflow; PAPF should evaluate forbidden data touches, attack cases, and trace evidence for context transitions.
- The measurable consequence of unauthorized disclosure is sensitive content leaving the user's account or appearing in an output without the right gate; PAPF should measure redaction failures, unredacted disclosures, and confirmation-gate ablations.
- The measurable consequence of prompt-injection-mediated data exfiltration is an attacker-controlled instruction causing private data to be sent to an attacker-controlled resource or recipient; PAPF should measure false allows, exfiltration outcomes, and recovery after denial.
- The measurable consequence of lost user agency is that users cannot predict, limit, or review agent authority; PAPF should evaluate consent burden, perceived control, comprehension, and auditability.
- Privacy principles map to PAPF mechanisms as follows: data minimization maps to narrow capabilities and over-access metrics; purpose limitation maps to purpose-bound grants and false-allow metrics; contextual integrity maps to relevance/sensitivity/trust labels and cross-context leakage cases; user consent maps to risk-adaptive confirmation and consent-burden measures; transparency and accountability map to audit traces and trace-review measures.

## 3. What existing work already covers

- Verified prompt-injection work already shows that agents can be steered by untrusted content and can leak or misuse data. The current checked map covers indirect prompt injection, BIPIA, InjecAgent, AgentDojo, BrowseSafe, and browser-agent alignment failures.
- Verified tool-using agent benchmarks already show how to evaluate privacy leakage, unsafe tool use, and task robustness once tools are available to the agent. AgentDojo, ToolEmu, and AgentDAM are the clearest examples in the current set.
- Capability-security, least-privilege, and confused-deputy literature already provides the conceptual foundation for PAPF's architecture. Saltzer and Schroeder, object-capability security, and confused-deputy work explain why ambient authority is dangerous and why explicit authority boundaries matter.
- OAuth, Rich Authorization Requests, token introspection, and the MCP authorization specification already provide deployed analogues for explicit, machine-checkable delegated authority outside the model.
- Permission-UX and consent-fatigue work already shows that users often misunderstand permission requests, contextual expectations matter, and frequent warnings degrade decision quality.
- Provenance and access-control-audit work already provides useful concepts for logging what was requested, granted, denied, and later inspected.

## 4. What existing work does not fully cover

- The current seed literature does not yet show a complete pipeline from natural-language consumer task to narrow machine-checkable capability set across heterogeneous tools such as email, files, browser, messaging, and payments.
- Current agent benchmarks mostly study what happens after an agent already has meaningful tool access. They are strong on attack exposure and outcome measurement, but much thinner on pre-access capability issuance and per-call external policy enforcement.
- Capability and delegated-authorization work assumes resources, actions, and policy objects are already structured. PAPF's harder problem is deriving useful narrow authority from an ambiguous user task before the agent acts.
- Permission-UX work in the current verified map is largely about app ecosystems or warnings, not multi-step autonomous agents that move across tools within a single task.
- The audit/provenance cluster in the current repo is still generic. It does not yet establish an agent-specific audit model that links user intent, compiled capabilities, consent decisions, denied actions, and actual sensitive-data touches in one trace.
- The current seed map suggests, but does not yet prove, that few papers evaluate all of the following together in one framework: task success, over-collection, secondary use, cross-context leakage, unauthorized disclosure, exfiltration, false allow, false deny, consent burden, recovery quality, user agency, and auditability.
- `TODO`: targeted follow-up review on adjacent work in agent-specific authorization, policy engines for LLM tool use, information-flow control for assistants, and user-facing agent permission mediation.

## 5. PAPF's proposed contribution

- Candidate contribution 1: a clearer problem formulation for consumer AI agents as a task-scoped privacy problem, not just an alignment, refusal, or generic safety problem.
- Candidate contribution 2: an architecture in which intent interpretation may be LLM-assisted, but permission issuance and enforcement remain external, machine-checkable, and auditable.
- Candidate contribution 3: a capability representation that binds authority to resource, action, scope, purpose, session, and consent level rather than relying on broad ambient tool access.
- Candidate contribution 4: a benchmark and measurement protocol that explicitly labels necessary, unnecessary, dangerous, and cross-context data and evaluates both utility and privacy/security outcomes.
- Candidate contribution 5: a user-facing permission framing for non-experts that tries to make scoped grants legible without falling back to repeated raw tool prompts.
- Candidate contribution 6: a principle-to-mechanism mapping that connects data minimization, purpose limitation, contextual integrity, user consent, transparency, and accountability to concrete PAPF mechanisms and evaluation measures.

## 6. Risk of overclaiming

- Do not claim novelty as fact. The safer phrasing is that PAPF addresses a possible gap at the intersection of multiple lines of work.
- Do not claim "least privilege" in a formal sense unless the system can justify why a compiled capability set is minimal rather than merely narrower than broad baselines.
- Do not claim "user-comprehensible" without direct empirical evidence from non-expert users. At most, the current materials support a design goal or working requirement.
- Do not claim privacy principles are satisfied merely because they are named. Each principle must map to a runtime mechanism, a logged artifact, or an evaluation measure.
- Do not claim strong privacy protection from prompt injection or exfiltration without comparative evaluation against realistic attacks and strong baselines.
- Do not claim cross-domain generality until the benchmark and enforcement prototype are tested across more than one narrow domain slice.
- Do not claim auditability as a solved property until the audit schema and its use in debugging, post-hoc review, or user explanation are operationalized.
- `TODO`: deeper source coverage is still needed for agent-specific permission UX and agent-session provenance.

## 7. Possible venue framings

### ML benchmark / datasets framing

- What the paper would emphasize: benchmark construction, task schema, attack cases, synthetic personal-data environments, and multi-metric evaluation of agent behavior.
- What evidence would be needed: a stable benchmark format, diverse tasks, reproducible environments, baseline agents, clear scoring, and evidence that the benchmark reveals behavior not captured by existing suites.
- Why it may fit: the repo already has a credible benchmark direction, explicit metrics, and a literature-backed motivation for measuring over-access and exfiltration.
- Why it may not fit: this framing risks making PAPF look like "another agent benchmark" while underselling the external enforcement thesis that currently seems most distinctive.

### Security systems framing

- What the paper would emphasize: threat model, task-to-capability compilation, runtime policy enforcement outside the LLM, confused-deputy prevention, data-minimization goals, and attack-resistant behavior under prompt injection or exfiltration pressure.
- What evidence would be needed: an executable prototype, clear policy semantics, well-defined capabilities, attack cases, and comparisons against broad-access or prompt-only baselines on both task success and privacy/security metrics.
- Why it may fit: this framing aligns most directly with the core thesis in `AGENTS.md`, the layered architecture in `docs/system_design.md`, and the repo's emphasis on measurable enforcement rather than a purely normative argument.
- Why it may not fit: it still requires enough implementation depth to avoid reading as a paper-only architecture proposal.

### Usable privacy / HCI framing

- What the paper would emphasize: privacy harms, task-scoped consent, permission comprehension, explanation quality, consent burden, escalation flow, user agency, and how non-experts reason about task-scoped grants.
- What evidence would be needed: formative design work, prototype UI flows, user studies with non-experts, comprehension measures, and likely qualitative plus quantitative usability evidence.
- Why it may fit: non-expert comprehension and privacy agency are central to PAPF's stated research question, and the current paper direction already separates planned user-study outcomes from prototype trace evidence.
- Why it may not fit: the current project state is still stronger on system architecture and evaluation design than on completed user-study evidence, so the paper must avoid claiming empirical comprehension results.

### AI governance / FAccT framing

- What the paper would emphasize: accountable permission boundaries for consumer agents, data minimization, institutional safeguards, and limits of model self-governance.
- What evidence would be needed: stronger normative framing, stakeholder analysis, deployment implications, and possibly empirical evidence about governance or user impact beyond system performance.
- Why it may fit: PAPF clearly engages with accountability, data protection, and consumer-facing AI governance concerns.
- Why it may not fit: the repo explicitly aims for a measurable technical contribution rather than a broad governance essay, so this framing is likely secondary for the first paper.

## 8. Strongest first-paper strategy

- The most defensible current paper is an HCI/privacy paper about task-scoped consent with external enforcement, not a broad AI ethics essay and not a pure benchmark paper.
- The paper should center concrete privacy harms and user agency first, then use one narrow but attack-relevant implementation slice to show that the proposed privacy boundary is enforceable. A reasonable first slice is a small cross-tool setting such as email plus files or email plus browser-linked tasks, where over-collection, cross-context leakage, unauthorized disclosure, prompt injection, and exfiltration pressure are all plausible.
- The artifact stack should be:
  1. a task-to-capability compiler,
  2. an external runtime policy checker,
  3. a compact audit trail schema, and
  4. a benchmark slice with necessary, unnecessary, dangerous, and cross-context data labels plus attack cases.
- The baseline comparison should be explicit:
  1. broad ambient tool access,
  2. prompt-only policy instructions or refusal prompting, and
  3. PAPF external enforcement.
- The trace evaluation should prioritize task success, over-access, exfiltration, false allow, false deny, recovery quality, consent burden, redaction failures, and auditability.
- The planned user evaluation should prioritize comprehension, allow/deny decision quality, perceived control, workload, trust calibration, and consent fatigue. Strong usability claims should wait for dedicated user evidence.
- This strategy preserves PAPF's core thesis while keeping scope tight enough to be executable.

## 9. Claims that require more evidence

- Claim that PAPF materially reduces over-access or exfiltration compared with broad-access or prompt-only baselines.
- Claim that PAPF materially reduces secondary use, cross-context leakage, unauthorized disclosure, or loss of agency compared with alternative permission designs.
- Claim that compiled capabilities are close to the minimum necessary authority rather than just narrower than a broad baseline.
- Claim that non-expert users understand task-scoped permission bundles better than raw tool permissions, app-style prompts, or generic warnings.
- Claim that risk-adaptive consent reduces approval fatigue without hiding high-risk actions.
- Claim that the architecture generalizes across multiple consumer domains rather than one carefully chosen prototype slice.
- Claim that the audit trail is genuinely useful for debugging, user review, or security investigation.
- Claim that PAPF represents a distinct research contribution rather than a repackaging of nearby authorization or agent-safety work.
- `TODO`: literature depth is still weakest in agent-specific permission UX, agent-session provenance, and possible adjacent work on agent authorization middleware.
