# Related Work Map

Verified against source pages on `2026-04-27` and `2026-04-29`. This remains a seed map rather than the final literature review, but the retained categories below now point only to checked sources with stable citation keys from [references.bib](../references.bib).

## Prompt injection and indirect prompt injection

1. What this category studies
   This category studies how malicious instructions, embedded directly in prompts or indirectly in retrieved content, can steer an LLM or agent away from the user's intent.
2. Verified representative works
   Greshake et al. provide an early indirect-prompt-injection threat framing for LLM-integrated applications (`greshake2023not`). Yi et al. introduce the BIPIA benchmark for indirect prompt injection in LLM systems (`yi2023benchmarking`). Zhan et al. extend the problem to tool-integrated agents with InjecAgent (`zhan2024injecagent`).
3. How they relate to PAPF
   This literature is directly relevant because PAPF assumes attackers can hide instructions in emails, files, or webpages that the agent may need to read during task execution.
4. Gap left open
   These works establish that prompt injection and exfiltration are real risks, but they do not by themselves define a user-comprehensible, task-scoped permission boundary enforced outside the model.

## Tool-using agent safety and benchmarks

1. What this category studies
   This category studies safety failures that arise when language-model agents can invoke tools, act over realistic environments, or operate with broad autonomy.
2. Verified representative works
   AgentDojo evaluates attacks and defenses in dynamic agent environments (`debenedetti2024agentdojo`). ToolEmu studies scalable risk discovery with LM-emulated tools (`ruan2024toolemu`). AgentDAM evaluates privacy leakage and unnecessary sensitive-data use in autonomous web agents (`zharmagambetov2025agentdam`).
3. How they relate to PAPF
   These papers provide concrete evaluation precedents for benchmarking agents that read sensitive data, call tools, and sometimes fail in ways that matter for privacy and security.
4. Gap left open
   Existing agent-safety benchmarks mostly evaluate behavior after meaningful tool access is already available. PAPF is positioned around the earlier control point: how authority is requested, narrowed, granted, denied, and enforced.

## Agent-specific authorization middleware

1. What this category studies
   This category studies runtime systems that constrain what an LLM agent may do, usually by mediating tool calls, checking structured policies, or isolating execution contexts outside the model.
2. Verified representative works
   Progent enforces fine-grained privilege-control policies over LLM-agent tool calls with deterministic runtime checks (`shi2025progent`). AgentSpec provides a domain-specific language for specifying and enforcing runtime constraints on LLM agents (`wang2025agentspec`). MiniScope reconstructs permission hierarchies and infers least-privilege grants for tool-calling agents (`zhu2025miniscope`). IsolateGPT studies execution isolation for LLM-based agentic systems and third-party apps (`wu2025isolategpt`).
3. How they relate to PAPF
   These are the closest prior works for PAPF's systems thesis because they move enforcement out of the LLM and toward an explicit runtime boundary.
4. Gap left open
   The gap is now narrower than the earlier seed map implied. PAPF should avoid claiming that no agent permission firewall exists. The remaining opportunity is a consumer-agent framing that combines task-derived personal-data scopes, non-expert permission prompts, per-tool enforcement, recovery from denial, and audit records in one benchmarked system.

## Privacy leakage and data minimization in agents

1. What this category studies  
   This category studies whether agents use only the personal data necessary for task completion, rather than broadly consuming whatever sensitive context is available.
2. Verified representative works  
   AgentDAM is the clearest direct benchmark in the current verified set for unnecessary sensitive-data use by autonomous web agents (`zharmagambetov2025agentdam`).
3. How they relate to PAPF  
   PAPF's benchmark plan already distinguishes necessary, unnecessary, and dangerous data. AgentDAM provides a concrete precedent for treating over-access as a measurable failure mode, not only a policy principle.
4. Gap left open  
   The verified agent-specific literature here is still thin. It appears stronger on measuring leakage than on providing an externally enforced, cross-tool permission architecture for consumer assistants.

## Browser-agent safety

1. What this category studies  
   This category studies safety failures specific to agents that browse the open web and can take actions inside browser sessions.
2. Verified representative works  
   Kumar et al. show that safety alignment in chat models does not necessarily transfer to browser agents (`kumar2025aligned`). BrowseSafe studies prompt-injection attacks and defenses for browser agents (`zhang2025browsesafe`).
3. How they relate to PAPF  
   Browser tasks are likely to be part of PAPF's benchmark, and browser agents are a concrete setting where prompt injection, over-access, and dangerous action capabilities meet.
4. Gap left open  
   These works focus on attack exposure, alignment transfer, or defensive filtering. They do not define a cross-tool permission firewall that scopes what a browser agent may read, extract, or transmit for a non-expert user.

## Confused deputy

1. What this category studies  
   This category studies authority confusion, where a component serving one principal unintentionally spends authority that came from another source.
2. Verified representative works  
   Hardy's classic confused-deputy case study provides the canonical structural pattern (`hardy1988confused`). Felt et al. show a modern version of the same problem in browsers and smartphone operating systems (`felt2011permission`).
3. How they relate to PAPF  
   PAPF can be framed as an attempt to keep an LLM agent from becoming a confused deputy for personal data stores and high-impact tools.
4. Gap left open  
   These works explain why ambient authority is dangerous, but they do not solve task interpretation, non-expert approval, or multi-tool agent orchestration.

## Capability security and least privilege

1. What this category studies  
   This category studies how authority can be represented explicitly, passed intentionally, and kept separate from ambient privilege.
2. Verified representative works  
   Saltzer and Schroeder articulate least privilege, complete mediation, and related design principles (`saltzer1975protection`). Wagner connects least privilege to object-capability security and avoidance of ambient authority (`wagner2006object`).
3. How they relate to PAPF  
   This is the clearest conceptual ancestor for PAPF's proposed capability compiler and external enforcement layer.
4. Gap left open  
   Capability-security work does not by itself explain how to derive narrow capabilities from ambiguous natural-language tasks or how to present those capabilities to non-expert users.

## Information-flow control for agents

1. What this category studies
   This category studies confidentiality and integrity labels that constrain how information may flow through an agent planner and its tool calls.
2. Verified representative works
   Costa et al. model security and expressiveness tradeoffs for AI-agent planners and present Fides, an IFC-style planner that tracks confidentiality and integrity labels while enforcing policies deterministically (`costa2025securing`).
3. How they relate to PAPF
   IFC gives PAPF a stronger formal vocabulary for data-flow restrictions than ordinary allow/deny tool lists, especially for prompt-injection and exfiltration cases.
4. Gap left open
   IFC does not replace the need to compile task-specific authority, explain data access to non-experts, or record user-facing audit trails. PAPF can cite IFC as a complementary enforcement strategy rather than as a complete permission UX.

## OAuth, delegated authorization, and MCP

1. What this category studies  
   This category studies how a service receives limited authority from a resource owner and how that authority is represented, challenged, and inspected.
2. Verified representative works  
   OAuth 2.0 provides the basic delegated-authorization framework (`hardt2012oauth`). Rich Authorization Requests add structured fine-grained access requests (`lodderstedt2023oauthrar`). Token Introspection standardizes inspection of token state and authorization context (`richer2015introspection`). GNAP standardizes grant negotiation for software clients and resource owners (`richer2024gnap`), with a companion resource-server connection specification (`richer2025gnaprs`). The MCP authorization specification adapts OAuth-style transport authorization to MCP servers and clients (`modelcontextprotocol2025authorization`).
3. How they relate to PAPF  
   These are the closest deployed analogues to PAPF's idea that authority should be explicit, scoped, machine-checkable, and enforced outside the model.
4. Gap left open  
   These standards assume pre-modeled resources and APIs. PAPF's harder problem is inferring minimum necessary authority from natural-language consumer tasks across heterogeneous tools, then explaining that authority to non-experts and verifying each runtime access against the compiled task policy.

## Permission UX

1. What this category studies  
   This category studies whether users notice, understand, and correctly act on permission requests, especially when access decisions depend on context.
2. Verified representative works  
   Felt et al. study user attention and comprehension of Android permission warnings (`felt2012androidpermissions`). Wijesekera et al. examine contextual integrity in mobile permission use (`wijesekera2015androidpermissions`). Cao et al. study permission decisions, expectations, and explanations at larger scale (`cao2021androidpermissions`). Wu et al. directly study data-access permission decisions for AI agents and develop an automated permission-management assistant (`wu2026automatingpermissions`).
3. How they relate to PAPF  
   PAPF explicitly cares about non-expert comprehension and user expectations, not only backend correctness.
4. Gap left open  
   Agent-specific permission UX now has at least one close empirical source, but PAPF should not overclaim from it. The open question for this project is how to combine understandable prompts with enforceable task-scoped capabilities and measurable security outcomes.

## Consent fatigue and approval fatigue

1. What this category studies  
   This category studies what happens when systems ask for consent too often, at the wrong time, or in a form users stop meaningfully processing.
2. Verified representative works  
   Felt et al. argue that not every permission should interrupt the user in the same way (`felt2012askpermission`). Vance et al. study habituation and warning generalization (`vance2019fog`). Akhawe and Felt show that warning effectiveness depends strongly on interface and context (`akhawe2013alice`).
3. How they relate to PAPF  
   This literature supports PAPF's risk-adaptive consent layer and its emphasis on reducing consent burden rather than showing more raw prompts.
4. Gap left open  
   The literature explains why repetitive approvals fail, but it does not yet provide an agent-specific interface for task-bound data and action grants that remain understandable under multi-step autonomy.

## Auditability, provenance, and traceability

1. What this category studies  
   This category studies how to record what happened, why it happened, and which data or policy inputs influenced the outcome.
2. Verified representative works  
   PROV-Overview defines a standard provenance model for interoperable records (`groth2013provoverview`). ACCESSPROV studies provenance for access-control enforcement decisions (`capobianco2017accessprov`). Souza et al. use LLM agents as an interface for querying workflow provenance data (`souza2025workflowprovenance`). Gupta proposes action attestations and lightweight audit agents for autonomous LLM systems, but this is an early arXiv preprint and performance claims should be treated as provisional (`gupta2025verifiability`). Token Introspection is also relevant because it standardizes machine-readable inspection of delegated-authorization context (`richer2015introspection`).
3. How they relate to PAPF  
   PAPF's architecture calls for audit and traceability outside the LLM, including records of what was requested, granted, denied, and accessed.
4. Gap left open  
   The verified sources here still do not define a mature user-facing consumer-agent audit model that links task intent, compiled capabilities, denials, grants, redactions, sensitive-data touches, and recovery attempts in one trace.

## Notes

- The strongest verified precedents are currently in agent-specific runtime authorization, prompt injection, agent-safety benchmarks, delegated authorization, and mobile plus agent permission UX.
- The weakest still-agent-specific cluster is user-facing agent-session auditability; available sources are either generic provenance, workflow-provenance interfaces, or early audit-agent preprints.
