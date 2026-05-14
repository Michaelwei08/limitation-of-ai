# Related Work Map

Verified against source pages on `2026-04-27`, `2026-04-29`, and `2026-05-14`. This map is organized for the HCI/privacy paper framing: privacy permissions, consent, and human-centered security motivate the problem; systems and agent-safety work provide the enforcement and threat-model substrate.

## Privacy theory, permissions, and contextual consent

1. What this category studies
   This category studies privacy as an appropriate information-flow problem, not merely as secrecy or a one-time disclosure checkbox.
2. Verified representative works
   Nissenbaum's contextual-integrity theory frames privacy as information flow governed by context-specific norms (`nissenbaum2004contextual`). Mobile permission work shows that users often miss, misunderstand, or contextualize access decisions differently than platform permission systems expect (`felt2012androidpermissions`, `wijesekera2015androidpermissions`, `lin2014mobilepreferences`, `cao2021androidpermissions`).
3. How they relate to PAPF
   PAPF inherits the HCI/privacy lesson that permission prompts must expose task context, data purpose, and downstream disclosure. A consumer agent's authority should be scoped to "this reimbursement task" rather than to ambient access over email, files, and browser data.
4. Gap left open
   Prior mobile permission systems generally mediate single-app or single-platform resources. They do not solve cross-tool personal-agent authority, where a natural-language task must be translated into enforceable per-resource capabilities and presented to non-experts.

## Mobile and web permission UX

1. What this category studies
   This category studies whether people notice permission prompts, whether prompts match user expectations, and how timing, context, and rationale affect allow/deny behavior.
2. Verified representative works
   Felt et al. report low attention and comprehension for Android permissions (`felt2012androidpermissions`). Kelley et al. show that clearer privacy information at app-selection time can affect app choices (`kelley2013appdecision`). Lin et al. model mobile permission preferences by considering not only the permission type but also the purpose of use (`lin2014mobilepreferences`). Wijesekera et al. and Cao et al. study contextual expectations and large-scale permission behavior (`wijesekera2015androidpermissions`, `cao2021androidpermissions`). Harbach studies web permission prompts in Desktop Chrome and finds that user sentiment and decisions depend on interruption, capability type, and contextual cues (`harbach2024webpermission`).
3. How they relate to PAPF
   These works support PAPF's decision to treat prompt wording, task goal, requested data, blocked data, external disclosure, redaction state, and confirmation reason as evaluation objects rather than cosmetic UI details.
4. Gap left open
   Mobile and browser permission prompts usually ask about platform capabilities such as location, camera, or notifications. Personal AI agents need permission UX for composed workflows: reading one email, checking one file, consulting one web page, drafting a reply, and blocking unrelated cross-tool leakage.

## Privacy notices and consent burden

1. What this category studies
   This category studies notice-and-choice mechanisms, privacy-policy readability, standardized notice formats, and the cost of asking users to make repeated privacy decisions.
2. Verified representative works
   McDonald and Cranor quantify the cost of reading privacy policies (`mcdonald2008cost`). Kelley et al. design a privacy "nutrition label" for clearer policy comparison (`kelley2009nutrition`). Schaub et al. systematize privacy-notice design dimensions and requirements (`schaub2015notices`). Almuhimedi et al. show that timely mobile privacy nudges can prompt users to revisit permissions (`almuhimedi2015location`).
3. How they relate to PAPF
   PAPF's consent surfaces should avoid turning every tool call into a long policy. The relevant notice is a task-scoped summary of what the agent will read, what it will not read, what will leave the account, what will be redacted, and what the audit log will record.
4. Gap left open
   Privacy-notice work generally targets websites, policies, apps, or device settings. PAPF's open HCI question is whether task-scoped notices can help non-expert users make safe agent-authorization decisions without producing consent fatigue.

## Human-centered security and consent fatigue

1. What this category studies
   This category studies security mechanisms that rely on user decisions, including warning comprehension, habituation, attention, and dangerous errors.
2. Verified representative works
   Whitten and Tygar show that a security mechanism can fail because novices cannot use it effectively (`whitten1999johnny`). Cranor's human-in-the-loop framework analyzes where user-mediated security decisions can break down (`cranor2008humanloop`). Felt et al. argue that systems should ask for permission only when interruption is justified (`felt2012askpermission`). Akhawe and Felt, Bravo-Lillo et al., and Vance et al. show that warning effectiveness depends on interface design, attention, and habituation (`akhawe2013alice`, `bravolillo2013attention`, `vance2019fog`).
3. How they relate to PAPF
   This literature motivates risk-adaptive consent: low-risk reads should not become repetitive approval prompts, while outbound sends, uploads, account changes, redaction bypasses, and off-task data access require more explicit user attention.
4. Gap left open
   Human-centered security work explains why naive prompts fail, but it does not provide an agent-specific control plane that combines non-expert consent, deterministic enforcement, recovery from denial, and audit evidence.

## AI agent authorization and permission UX

1. What this category studies
   This category studies how LLM agents can be restricted by policies, monitors, isolation boundaries, or user-facing permission-management mechanisms.
2. Verified representative works
   Progent, AgentSpec, MiniScope, IsolateGPT, and agent IFC systems move constraints outside ordinary prompt instructions (`shi2025progent`, `wang2025agentspec`, `zhu2025miniscope`, `wu2025isolategpt`, `costa2025securing`). Wu et al. study data-access permission decisions for AI agents and build a permission-management assistant (`wu2026automatingpermissions`).
3. How they relate to PAPF
   These are the closest technical neighbors. PAPF should not claim that external enforcement or agent permissioning is absent from the literature.
4. Gap left open
   The remaining PAPF contribution is narrower and HCI/privacy-centered: consumer task-derived personal-data scopes, user-facing consent states, redaction and confirmation evidence, deterministic per-tool enforcement, recovery scoring, and audit-linked evaluation in one artifact.

## Prompt injection, tool-use risk, and browser agents

1. What this category studies
   This category studies how untrusted content and tool access create failures beyond ordinary chat alignment.
2. Verified representative works
   Greshake et al. and Yi et al. frame indirect prompt injection (`greshake2023not`, `yi2023benchmarking`). InjecAgent, AgentDojo, and ToolEmu benchmark tool-agent attacks and risks (`zhan2024injecagent`, `debenedetti2024agentdojo`, `ruan2024toolemu`). WebArena, Aligned LLMs Are Not Aligned Browser Agents, BrowseSafe, and AgentDAM cover browser-agent functionality, browser-agent safety, prompt injection, and privacy leakage (`zhou2024webarena`, `kumar2025aligned`, `zhang2025browsesafe`, `zharmagambetov2025agentdam`).
3. How they relate to PAPF
   This work supplies the threat model: untrusted webpages, emails, and files may try to redirect an agent into off-task reads, uploads, or disclosures.
4. Gap left open
   These papers mostly evaluate agent behavior after broad tool access is already available. PAPF uses those risks to motivate the earlier HCI/privacy question of what authority should be granted for the task and how users can inspect that boundary.

## Delegated authorization, least privilege, and confused deputy

1. What this category studies
   This category studies explicit authority, complete mediation, structured grants, and failures caused by ambient privilege.
2. Verified representative works
   Saltzer and Schroeder articulate least privilege and complete mediation (`saltzer1975protection`). Hardy and Felt et al. describe confused-deputy and permission re-delegation failures (`hardy1988confused`, `felt2011permission`). Wagner explains object-capability security (`wagner2006object`). OAuth, Rich Authorization Requests, Token Introspection, GNAP, GNAP Resource Server Connections, and MCP authorization define deployed or emerging authorization substrates (`hardt2012oauth`, `lodderstedt2023oauthrar`, `richer2015introspection`, `richer2024gnap`, `richer2025gnaprs`, `modelcontextprotocol2025authorization`).
3. How they relate to PAPF
   These works support PAPF's enforcement design: authority should be explicit, narrow, inspectable, revocable or time-bounded, and checked at each tool call outside the LLM.
4. Gap left open
   Authorization protocols and capability systems usually assume pre-modeled API scopes. They do not decide which data is necessary for an ordinary user's natural-language task or how to explain that scoped authority in a permission prompt.

## Auditability, provenance, and traceability

1. What this category studies
   This category studies records that explain what happened, which authority was used, and why an access-control decision was allowed or denied.
2. Verified representative works
   PROV-Overview defines interoperable provenance concepts (`groth2013provoverview`). ACCESSPROV tracks provenance for access-control decisions (`capobianco2017accessprov`). Souza et al. use LLM agents as interfaces over workflow provenance (`souza2025workflowprovenance`). Gupta proposes verifiability-first audit agents, but this is an arXiv preprint and performance claims should remain provisional (`gupta2025verifiability`).
3. How they relate to PAPF
   PAPF uses audit records to connect task intent, capabilities, policy checks, data touches, redaction artifacts, confirmation gates, denials, and recovery attempts.
4. Gap left open
   Existing provenance work does not yet provide a mature consumer-agent audit model that is both machine-checkable for enforcement and understandable enough for non-expert post-hoc review.

## Notes

- The related-work order should remain HCI/privacy first: contextual consent, permission UX, privacy notices, consent fatigue, and human-centered security define the research problem.
- Systems and security work should be used as support for the enforceable boundary, not as the dominant paper framing.
- Early arXiv and future-venue entries use eprint or acceptance metadata in [references.bib](../references.bib) and explicit source-status labels in [lit_matrix.md](lit_matrix.md); their empirical claims should not be treated as settled beyond their stated source status.
