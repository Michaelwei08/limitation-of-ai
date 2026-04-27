# Related Work Map

Verified against source pages on `2026-04-27`. This is a seed map, not a full literature review.

## Prompt injection and indirect prompt injection

1. What this category studies  
   This category studies how malicious instructions, embedded either directly in user input or indirectly in external content, can steer an LLM or agent away from the user's intent.
2. Representative works  
   [Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://doi.org/10.1145/3605764.3623985) is an early systems paper on indirect prompt injection against LLM-integrated applications. [Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models](https://www.microsoft.com/en-us/research/publication/benchmarking-and-defending-against-indirect-prompt-injection-attacks-on-large-language-models/) introduces the BIPIA benchmark. [InjecAgent](https://aclanthology.org/2024.findings-acl.624/) evaluates indirect prompt injection in tool-integrated agents, and [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html) studies prompt-injection attacks and defenses in dynamic agent environments.
3. How it relates to PAPF  
   This literature is directly relevant to PAPF's threat model because the project assumes attackers can hide instructions in emails, files, or webpages that an agent must read to complete a task.
4. Gap left open  
   These works show that tool-using agents can be vulnerable to prompt injection and data exfiltration, but they do not by themselves define a user-comprehensible, task-scoped permission firewall for non-expert consumer users.

## Tool-using agent safety

1. What this category studies  
   This category studies safety failures that arise when language-model agents can invoke external tools or act over realistic environments.
2. Representative works  
   [ToolEmu: Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://proceedings.iclr.cc/paper_files/paper/2024/hash/7274ed909a312d4d869cc328ad1c5f04-Abstract-Conference.html) proposes scalable risk evaluation with emulated tools. [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html) evaluates agents under realistic task and attack conditions. [AgentDAM](https://openreview.net/forum?id=qaxf7q41aK) focuses on privacy leakage during autonomous web-agent execution.
3. How it relates to PAPF  
   These papers provide concrete evaluation precedents for benchmarking agents that read sensitive data, call tools, and sometimes fail in ways that matter for privacy and security.
4. Gap left open  
   Most of this work evaluates agent behavior after tools are already available. PAPF's harder question is how to issue, deny, and enforce narrow capabilities before or during each action.

## Excessive agency

1. What this category studies  
   This category studies the risk that an LLM-based system is given more functionality, permission, or autonomy than is necessary for the user's task.
2. Representative works  
   [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) provides a current security taxonomy for excessive functionality, excessive permissions, and excessive autonomy. [ToolEmu](https://proceedings.iclr.cc/paper_files/paper/2024/hash/7274ed909a312d4d869cc328ad1c5f04-Abstract-Conference.html) and [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html) give empirical evidence that broad tool access can translate into harmful actions.
3. How it relates to PAPF  
   PAPF is explicitly trying to reduce excessive agency by constraining what the agent may access and do for a given task, rather than trusting prompt-level self-restraint.
4. Gap left open  
   The excessive-agency literature is useful for threat naming and diagnosis, but it does not yet provide a consumer-oriented mechanism for compiling natural-language tasks into externally enforced, least-privilege grants.

## Confused deputy

1. What this category studies  
   This category studies authority confusion, where a component serves one principal while unintentionally spending authority that came from another source.
2. Representative works  
   Norm Hardy's [The Confused Deputy](https://web.cs.wpi.edu/~cs557/f14/papers/confused_deputy-hardy.pdf) is the canonical case study. [Permission Re-Delegation: Attacks and Defenses](https://www.usenix.org/conference/usenixsecurity11/permission-re-delegation-attacks-and-defenses) shows a modern version of the same structural problem in browsers and smartphone operating systems.
3. How it relates to PAPF  
   PAPF can be framed as an attempt to stop an LLM agent from becoming a confused deputy for personal data stores and high-impact tools.
4. Gap left open  
   These works explain why ambient authority is dangerous, but they do not solve task interpretation, non-expert approval, or cross-tool agent orchestration.

## Capability security and least privilege

1. What this category studies  
   This category studies how authority can be represented explicitly, passed intentionally, and kept separate from ambient privilege.
2. Representative works  
   [The Protection of Information in Computer Systems](https://web.mit.edu/Saltzer/www/publications/protection/) is the classic source for least privilege, complete mediation, and psychological acceptability. [Object capabilities for security](https://dblp.org/rec/conf/pldi/Wagner06) connects least privilege to capability-style programming and avoidance of ambient authority.
3. How it relates to PAPF  
   This is the clearest conceptual ancestor for PAPF's proposed capability compiler and external enforcement layer.
4. Gap left open  
   Capability-security work does not by itself explain how to derive minimal capabilities from ambiguous user requests or how to present those capabilities to non-expert users.

## Data minimization

1. What this category studies  
   This category studies the principle that systems should process only the personal data necessary for the stated purpose.
2. Representative works  
   The ICO's [Principle (c): Data minimisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/?reqp=1) provides an official formulation of the principle. [AgentDAM](https://openreview.net/forum?id=qaxf7q41aK) is a direct agent benchmark for measuring whether web agents use unnecessary sensitive information.
3. How it relates to PAPF  
   PAPF's benchmark design already distinguishes necessary, unnecessary, and dangerous data. This literature gives both the normative privacy principle and an agent-specific evaluation precedent.
4. Gap left open  
   Data-minimization work in agent settings is still thin. It does not yet provide a general, externally enforced permission architecture for cross-tool consumer assistants.

## Browser-agent safety

1. What this category studies  
   This category studies safety failures specific to agents that browse the open web and can take actions within browser sessions.
2. Representative works  
   [Aligned LLMs Are Not Aligned Browser Agents](https://openreview.net/forum?id=NsFZZU9gvk) studies whether chat-style refusal behavior transfers to browser agents. [BrowseSafe: Understanding and Preventing Prompt Injection Within AI Browser Agents](https://research.perplexity.ai/articles/browsesafe) focuses on prompt-injection detection for browser agents. [AgentDAM](https://openreview.net/forum?id=qaxf7q41aK) is also relevant because it evaluates privacy leakage in autonomous web navigation.
3. How it relates to PAPF  
   Browser tasks are likely to be part of PAPF's benchmark, and browser agents are a concrete setting where prompt injection, over-access, and dangerous action capabilities meet.
4. Gap left open  
   These works focus on attack exposure, detection, or alignment transfer. They do not define a cross-tool permission firewall that scopes what a browser agent may read, extract, or transmit on behalf of a non-expert user.

## MCP, OAuth, and delegated authorization

1. What this category studies  
   This category studies how one service receives limited authority from a resource owner and how that authority is represented, challenged, and inspected.
2. Representative works  
   [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) defines OAuth 2.0 delegated authorization. [RFC 9396](https://www.rfc-editor.org/rfc/rfc9396) adds structured `authorization_details` for finer-grained requests. [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) defines token introspection. The current [Model Context Protocol authorization specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) applies OAuth-style authorization to HTTP-based MCP transports.
3. How it relates to PAPF  
   These standards are the closest deployed analogue to PAPF's idea that authority should be explicit, scoped, machine-checkable, and enforced outside the model.
4. Gap left open  
   These standards assume pre-modeled resources and application protocols. PAPF's harder problem is inferring minimum necessary authority from natural-language tasks across heterogeneous personal tools, then explaining that authority to non-experts.

## Permission UX

1. What this category studies  
   This category studies whether users notice, understand, and correctly act on permission requests, especially when access decisions depend on context.
2. Representative works  
   [Android Permissions: User Attention, Comprehension, and Behavior](https://research.google/pubs/android-permissions-user-attention-comprehension-and-behavior/) studies whether users actually notice and understand permission warnings. [Android Permissions Remystified](https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/wijesekera) examines contextual integrity in mobile permission use. [A Large Scale Study of User Behavior, Expectations and Engagement with Android Permissions](https://www.usenix.org/conference/usenixsecurity21/presentation/cao-weicheng) studies permission decisions and expectations at larger scale.
3. How it relates to PAPF  
   PAPF explicitly cares about non-expert comprehension and user expectations, not only backend correctness.
4. Gap left open  
   Existing permission-UX work is mostly about app ecosystems, not autonomous agents that may traverse email, files, browser sessions, and payment flows inside one task.

## Consent fatigue and approval fatigue

1. What this category studies  
   This category studies what happens when systems ask for consent too often, at the wrong time, or in a form users stop meaningfully processing.
2. Representative works  
   [How to Ask for Permission](https://www.usenix.org/conference/hotsec12/workshop-program/presentation/felt) argues that not every permission should interrupt the user in the same way. [The Fog of Warnings](https://www.usenix.org/conference/soups2019/presentation/vance) studies habituation and generalization across warnings. [Alice in Warningland](https://www.usenix.org/conference/usenixsecurity13/technical-sessions/presentation/akhawe) shows that warning effectiveness depends strongly on interface and context.
3. How it relates to PAPF  
   This literature supports PAPF's risk-adaptive consent layer and its emphasis on reducing consent burden rather than showing more raw prompts.
4. Gap left open  
   The literature explains why repetitive approvals fail, but it does not yet provide an agent-specific interface for task-bound data and action grants that remain understandable under multi-step autonomy.

## Auditability and provenance

1. What this category studies  
   This category studies how to record what happened, why it happened, and which data or policy inputs influenced the outcome.
2. Representative works  
   [PROV-Overview](https://www.w3.org/TR/prov-overview/) defines a standard model for provenance on the web. [ACCESSPROV: Tracking the Provenance of Access Control Decisions](https://www.usenix.org/conference/tapp17/workshop-program/presentation/capobianco) studies provenance for access-control enforcement. [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) is also relevant because it standardizes machine-readable inspection of delegated-authorization context.
3. How it relates to PAPF  
   PAPF's architecture calls for audit and traceability outside the LLM, including records of what was requested, granted, denied, and accessed.
4. Gap left open  
   The verified sources here are mostly generic provenance or authorization work. They do not yet define a user-facing, agent-session audit model for consumer assistants that mix semantic task intent, scoped grants, denials, and sensitive-data touches.

## Notes

- The strongest verified precedents are currently in prompt injection, delegated authorization, and mobile/browser permission UX.
- The weakest still-agent-specific clusters are auditability/provenance and agent-permission UX for non-expert users.
