# Related Work Map

Verified against source pages on `2026-04-27`. This remains a seed map rather than the final literature review, but the retained categories below now point only to checked sources with stable citation keys from [references.bib](../references.bib).

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

## OAuth, delegated authorization, and MCP

1. What this category studies  
   This category studies how a service receives limited authority from a resource owner and how that authority is represented, challenged, and inspected.
2. Verified representative works  
   OAuth 2.0 provides the basic delegated-authorization framework (`hardt2012oauth`). Rich Authorization Requests add structured fine-grained access requests (`lodderstedt2023oauthrar`). Token Introspection standardizes inspection of token state and authorization context (`richer2015introspection`). The MCP authorization specification adapts OAuth-style transport authorization to MCP servers and clients (`modelcontextprotocol2025authorization`).
3. How they relate to PAPF  
   These are the closest deployed analogues to PAPF's idea that authority should be explicit, scoped, machine-checkable, and enforced outside the model.
4. Gap left open  
   These standards assume pre-modeled resources and APIs. PAPF's harder problem is inferring minimum necessary authority from natural-language consumer tasks across heterogeneous tools, then explaining that authority to non-experts.

## Permission UX

1. What this category studies  
   This category studies whether users notice, understand, and correctly act on permission requests, especially when access decisions depend on context.
2. Verified representative works  
   Felt et al. study user attention and comprehension of Android permission warnings (`felt2012androidpermissions`). Wijesekera et al. examine contextual integrity in mobile permission use (`wijesekera2015androidpermissions`). Cao et al. study permission decisions, expectations, and explanations at larger scale (`cao2021androidpermissions`).
3. How they relate to PAPF  
   PAPF explicitly cares about non-expert comprehension and user expectations, not only backend correctness.
4. Gap left open  
   Existing permission-UX work in the verified set is mostly about app ecosystems, not autonomous agents that may traverse email, files, browser sessions, and payment flows inside one task.

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
   PROV-Overview defines a standard provenance model for interoperable records (`groth2013provoverview`). ACCESSPROV studies provenance for access-control enforcement decisions (`capobianco2017accessprov`). Token Introspection is also relevant because it standardizes machine-readable inspection of delegated-authorization context (`richer2015introspection`).
3. How they relate to PAPF  
   PAPF's architecture calls for audit and traceability outside the LLM, including records of what was requested, granted, denied, and accessed.
4. Gap left open  
   The verified sources here are mostly generic provenance or authorization work. They do not yet define a user-facing, agent-session audit model that links task intent, compiled capabilities, denials, grants, and sensitive-data touches in one trace.

## Notes

- The strongest verified precedents are currently in prompt injection, agent-safety benchmarks, delegated authorization, and mobile permission UX.
- The weakest still-agent-specific clusters are non-expert agent permission UX and agent-session auditability.
