# Related Work Map

Verified against source pages on `2026-04-27`. This is a concise seed map, not a full literature review.

## Agent attack and safety benchmarks

1. What this category studies  
   These works study failure modes of tool-using or web-acting agents under untrusted inputs, simulated tools, or privacy-sensitive environments.
2. Key representative works  
   [AgentDojo](https://mlanthology.org/neurips/2024/debenedetti2024neurips-agentdojo/) frames prompt-injection evaluation as a dynamic environment over realistic agent tasks. [InjecAgent](https://aclanthology.org/2024.findings-acl.624/) benchmarks indirect prompt injection in tool-integrated agents, including direct-harm and data-exfiltration cases. [ToolEmu](https://openreview.net/forum?id=GEcwtMk1uA) uses an LM-emulated sandbox to identify risky agent behaviors at scale. [AgentDAM](https://openreview.net/forum?id=qaxf7q41aK) evaluates whether autonomous web agents satisfy a data-minimization notion during task execution.
3. How it relates to PAPF  
   This cluster is directly relevant to PAPF's benchmark and threat-model design. It shows that tool-using agents are vulnerable to prompt-injection, unsafe action, and privacy-leakage failures in settings that look much closer to consumer assistants than static QA benchmarks do.
4. What gap remains  
   These benchmarks show that tool-using agents are vulnerable to prompt-injection and exfiltration attacks, but they do not by themselves define a user-comprehensible, task-scoped permission firewall for non-expert consumer users. They also mostly evaluate agent behavior after access is already available, rather than compiling and enforcing narrow capabilities before each action.

## Confused deputy and least privilege

1. What this category studies  
   This category studies structural authorization failures that arise when a component acts on behalf of one principal while holding broader ambient authority from another source.
2. Key representative works  
   Hardy's [The Confused Deputy](https://www.cs.umd.edu/~jkatz/security/downloads/capabilities.html) is the canonical case study. Saltzer and Schroeder's [The Protection of Information in Computer Systems](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html) formalizes least privilege, complete mediation, and psychological acceptability as enduring design principles. [Permission Re-Delegation: Attacks and Defenses](https://www.usenix.org/conference/usenixsecurity11/permission-re-delegation-attacks-and-defenses) shows a modern OS-level redelegation analogue in mobile and browser platforms.
3. How it relates to PAPF  
   PAPF can be framed as an attempt to prevent LLM agents from becoming confused deputies for personal data stores and external-action tools. These sources support the claim that the right unit of analysis is authority structure, not just intent classification or refusal prompting.
4. What gap remains  
   Classical least-privilege and confused-deputy work is not about LLMs, natural-language task interpretation, or consumer approval flows. It explains why ambient authority is dangerous, but not how to compile a non-expert user request into narrow machine-checkable capabilities for an agent runtime.

## Capability security

1. What this category studies  
   Capability-security work studies how authority can be represented explicitly, passed intentionally, and kept separate from ambient privilege.
2. Key representative works  
   Wagner's [Object capabilities for security](https://www.researchgate.net/publication/220751895_Object_capabilities_for_security) is a concise object-capability framing that ties least privilege to avoidance of ambient authority and confused-deputy bugs. Saltzer and Schroeder also remain relevant here because their protection model explicitly contrasts capability and access-control-list styles.
3. How it relates to PAPF  
   This is the clearest conceptual ancestor for PAPF's proposed capability compiler. PAPF's design direction is closer to explicit authority passing than to broad per-app permissions or post hoc prompt filtering.
4. What gap remains  
   The verified sources here are largely systems and language-security papers. They do not address how capabilities should be derived from ambiguous user tasks, explained to non-experts, or evaluated in realistic consumer-agent benchmarks.

## Data minimization and privacy leakage

1. What this category studies  
   This category studies the principle that systems should use only the personal data necessary for the stated purpose, and how failures of that principle appear in agent settings.
2. Key representative works  
   The ICO's [Principle (c): Data minimisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/?reqp=1) gives an official formulation of data minimization as data that is adequate, relevant, and limited to what is necessary. [AgentDAM](https://openreview.net/forum?id=qaxf7q41aK) is, in this seed set, the most direct agent benchmark for measuring whether web agents use unnecessary sensitive information.
3. How it relates to PAPF  
   PAPF's benchmark schema already distinguishes necessary, unnecessary, and dangerous data. This category provides both the normative privacy principle and an agent-specific evaluation precedent for measuring over-access rather than only task success.
4. What gap remains  
   Existing agent work in this cluster is still thin. AgentDAM shows the problem and measures leakage, but it does not yet supply an externally enforced permission architecture, a consent model, or a general cross-tool benchmark centered on user-comprehensible scoped grants.

## Delegated authorization and fine-grained access

1. What this category studies  
   This category studies how one service can receive limited authority from a user or resource owner, and how that authority can be represented and inspected.
2. Key representative works  
   [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) defines OAuth 2.0 as delegated authorization with limited access tokens instead of shared credentials. [RFC 9396](https://www.rfc-editor.org/rfc/rfc9396) adds structured `authorization_details` for finer-grained requests than coarse scope strings. [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) provides token introspection so protected resources can inspect authorization context and token state.
3. How it relates to PAPF  
   These standards are the closest deployed analogue to PAPF's idea that authority should be explicit, scoped, and machine-checkable outside the model. They are especially relevant for capability shape, delegation boundaries, and audit-adjacent metadata.
4. What gap remains  
   OAuth standards assume pre-defined resource schemas and application protocols. PAPF's harder problem is inferring the minimum necessary authority from natural-language tasks across heterogeneous personal tools, then explaining that authority to non-expert users in a way that remains enforceable at runtime.

## Permission UX and approval fatigue

1. What this category studies  
   This category studies whether users notice, understand, and correctly act on permission and warning interfaces, and what happens when prompts are too frequent or poorly timed.
2. Key representative works  
   [Android Permissions: User Attention, Comprehension, and Behavior](https://research.google/pubs/android-permissions-user-attention-comprehension-and-behavior/) shows that many users paid little attention to install-time permissions and understood them poorly. [How to Ask for Permission](https://www.usenix.org/conference/hotsec12/workshop-program/presentation/felt) argues that permission systems should not interrupt users uniformly and proposes ways to reduce habituation. [Android Permissions Remystified](https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/wijesekera) studies when users would want to block permission use in context. [The Fog of Warnings](https://www.usenix.org/conference/soups2019/presentation/vance) shows that habituation and generalization can reduce adherence to warnings.
3. How it relates to PAPF  
   PAPF explicitly targets non-expert comprehension and consent burden. This literature supports the claim that a viable permission firewall cannot just surface more raw prompts; it needs risk-adaptive consent, contextual explanation, and a low-warning baseline.
4. What gap remains  
   Most verified UX work here concerns smartphone permissions or generic security warnings rather than autonomous agents crossing email, files, browsers, and payments in one multi-step task. The agent-specific question of how to present task-bound data and action scopes to non-expert users remains weakly grounded in this seed set.

## Auditability

1. What this category studies  
   This category concerns post hoc visibility into what authority was granted, what was exercised, and under what authorization context.
2. Key representative works  
   In this seed pass, the strongest verified adjacent source is [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662), which standardizes token-state and authorization-context inspection for delegated access.
3. How it relates to PAPF  
   PAPF's architecture calls for audit and traceability outside the LLM. RFC 7662 is relevant because it treats authorization metadata as machine-readable state that can be queried by other system components.
4. What gap remains  
   This category is still weak for PAPF's purposes. Token introspection is much narrower than an agent-facing audit trail that records which personal artifacts were touched, which requests were denied, and how those events should be explained to users or evaluators.

## Notes

- Any claim added here should remain source-backed and narrow.
- The strongest currently verified gaps are: agent-specific auditability, non-expert agent-permission UX, and task-to-capability compilation under realistic consumer workloads.
