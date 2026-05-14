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

## 7. Venue positioning

### Primary HCI/privacy and usable-security framing

- What the paper should emphasize: human-centered privacy, task-scoped consent, permission comprehension, consent interaction design, escalation flow, consent burden, perceived control, trust, and how non-expert users reason about personal-agent grants.
- What evidence is needed for a full paper: a completed empirical evaluation with non-expert users, including comprehension measures, safe/unsafe action decisions, false allows, false denies, timing, workload, trust or control measures, fatigue measures, and qualitative feedback where feasible.
- Why it fits: PAPF's central research question is whether user-comprehensible, enforceable task boundaries can protect non-technical users without destroying task utility. That is a privacy-usability and usable-security question first, with enforcement as necessary support.
- Main risk: without completed participant data, the paper can only present a design, protocol, prompt variants, and prototype feasibility evidence. It should not claim that users understand PAPF prompts or make better privacy decisions.

### Systems/security evidence as technical feasibility support

- What this evidence should show: task-to-capability compilation, runtime policy enforcement outside the LLM, redaction evidence, confirmation gates, audit logging, confused-deputy resistance, and behavior under prompt-injection or exfiltration pressure.
- How to use it: as proof that the consent states shown to users can be enforced by a backend control plane, not as the paper's primary venue identity.
- What to avoid: do not frame the first paper primarily as a top systems/security venue submission unless the contribution shifts toward new policy semantics, formal guarantees, faithful comparisons to published enforcement systems, or a substantially broader deployed prototype.

### Benchmark and dataset evidence as secondary support

- What this evidence should show: explicit labels for necessary, unnecessary, dangerous, and cross-context data; reproducible synthetic tasks; broad-access, prompt-only, and external-enforcement comparisons; and metrics for task success, over-access, false allows, false denies, recovery, consent prompts, and auditability.
- How to use it: to make the privacy and enforcement claims measurable.
- What to avoid: do not make the paper read like a primary ML benchmark or systems/security benchmark paper. The synthetic suite is a feasibility artifact for the HCI/privacy argument.

### Bounded workshop fallback

- If the non-expert user study remains planned rather than completed, the defensible fallback is a workshop, design, position, or prototype paper in an HCI/privacy, usable-security, or privacy-engineering venue.
- The fallback contribution should be bounded to the problem framing, consent interaction design, externally enforced prototype, synthetic scenarios, and evaluation protocol.
- The fallback should explicitly withhold claims about empirical user comprehension, improved consent decisions, reduced fatigue, calibrated trust, or real-world deployment readiness.

### AI governance / FAccT framing

- What the paper would emphasize: accountable permission boundaries for consumer agents, data minimization, institutional safeguards, and limits of model self-governance.
- Why it remains secondary: PAPF clearly engages with accountability and data protection, but the repo aims for a measurable privacy-usability and enforcement contribution rather than a broad governance essay.

## 8. Strongest first-paper strategy

- The most defensible current paper is an HCI/privacy or usable-security privacy paper about task-scoped consent with external enforcement, not a broad AI ethics essay, not a pure benchmark paper, and not primarily a top systems/security submission.
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
- If the user study is completed, this strategy can support a full HCI/privacy submission. If it remains planned, the bounded fallback is a workshop, design, or prototype paper with trace results presented only as technical feasibility support.

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
