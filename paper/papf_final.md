# Human-Centered Permission Boundaries for Personal AI Agents: Task-Scoped Consent with External Enforcement

## Abstract

Personal AI agents can act across email, files, browsers, calendars, and communication tools, but current authorization patterns often grant broad tool and data access before users can reason about the needs of the current task. This creates a privacy-usability problem: non-expert users need to understand what data an agent will access, what it will disclose, when sensitive content is redacted, and why high-risk actions require consent.

We present Personal Agent Permission Firewall (PAPF), a task-scoped consent framework that enforces personal-agent authority outside the model. An LLM may propose task intent or user-facing explanations, but deterministic components validate task records, compile narrow capabilities, mediate every tool call, require confirmation for risky actions, verify redaction artifacts, and write audit traces. PAPF's interface design makes the task goal, requested access, external disclosure, redaction state, and confirmation rationale explicit enough to be evaluated as consent decisions rather than hidden system state.

We evaluate PAPF in two complementary ways. First, we implement a deterministic prototype and run trace evaluation on a 12-trace synthetic email-files-browser suite. In this suite, PAPF records zero false allows and zero over-access, while broad-access and prompt-only baselines each record 16 false allows and an over-access rate of 0.2639. These trace results support technical feasibility of externally enforced task scope, but they do not establish deployment readiness or user comprehension.

Second, because trace metrics cannot show whether people understand permission boundaries, we design a non-expert user study to evaluate permission comprehension, safe/unsafe-action discrimination, privacy-preserving consent decisions, perceived control, trust, workload, and consent fatigue. We do not report user-study results because the study has not yet been run. The paper's bounded contribution is a human-centered privacy framing for agent permissions, an externally enforced architecture for task-scoped authority, a prompt and consent-state design space, and a planned privacy-usability evaluation that is kept separate from the prototype trace evidence.

## 1. Introduction

Personal AI agents create a privacy interaction problem because they combine sensitive context with executable actions. Consider a synthetic reimbursement task: Riley asks an assistant to summarize one email from Alex about a work expense and tell Riley what reply is needed. The useful authority is narrow: read Alex's reimbursement thread, optionally inspect the attached receipt and the approved merchant policy page, and prepare a draft. The same assistant may also be technically connected to Riley's files, browser, and email-sending tool, which creates risks that a non-expert user should not have to reason about from a blanket permission prompt.

In this example, broad app authorization is too coarse because "email + files + browser" does not mean "this one reimbursement email." The agent should not open Riley's unrelated 2025 tax return just because file access is available; a scoped capability should cover only the named email, receipt, policy page, and draft. If a webpage says "ignore prior instructions and upload tax documents," the instruction should not expand the agent's authority; the attempted off-task browse or upload should be denied and recorded. If the reimbursement email or receipt contains private fields, such as a home address or payment identifier, the user should be able to see redaction evidence showing those fields were removed before any summary or draft reuses the content. If the agent is about to send a message to Alex, a confirmation gate should show what will leave Riley's account before the send occurs. Afterward, an audit trace should let Riley or an evaluator see which data was accessed, what was blocked, what was redacted, and what was confirmed.

The central harm is privacy loss, with security failures acting as one important cause. Over-collection occurs when the agent reads unrelated emails, files, or pages simply because a connector is available. Secondary use occurs when data gathered for reimbursement is reused for a different purpose, such as account recovery or marketing-style profile construction. Cross-context leakage occurs when information from one personal context, such as tax records or banking alerts, is carried into another context, such as a workplace reimbursement reply. Unauthorized disclosure occurs when a draft, upload, or outbound message exposes sensitive fields without the user's consent. Prompt-injection-mediated data exfiltration is a security technique that produces a privacy harm by causing the agent to transmit private data to an attacker-controlled page or recipient. Loss of user agency occurs when broad or hidden grants leave the user unable to predict, limit, or review what the agent did.

Prompt-only control is also poorly matched to this setting. Prompt-only guardrails ask the same model to plan the task, interpret untrusted content, and police its own authority. Prior work on indirect prompt injection and tool-using agents shows that malicious content in emails, documents, webpages, or tool outputs can redirect agents away from the user's intent (`greshake2023not`, `yi2023benchmarking`, `zhan2024injecagent`, `debenedetti2024agentdojo`, `ruan2024toolemu`). Browser-agent and privacy-leakage benchmarks further show that alignment in chat does not automatically prevent unsafe behavior when tools and sensitive data are available (`zhou2024webarena`, `kumar2025aligned`, `zhang2025browsesafe`, `zharmagambetov2025agentdam`).

PAPF treats personal-agent privacy as task-scoped consent backed by external enforcement. The agent should receive only capabilities justified by the current user task, and every attempted tool action should be mediated outside the LLM before data is read, redacted, or sent. The design draws on least privilege and complete mediation (`saltzer1975protection`), capability security (`wagner2006object`), confused-deputy analysis (`hardy1988confused`, `felt2011permission`), and delegated authorization systems such as OAuth, Rich Authorization Requests, GNAP, token introspection, and MCP authorization (`hardt2012oauth`, `lodderstedt2023oauthrar`, `richer2015introspection`, `richer2024gnap`, `richer2025gnaprs`, `modelcontextprotocol2025authorization`). PAPF's HCI/privacy contribution is to connect those enforcement mechanisms to consent prompts, redaction states, and audit traces that can be evaluated with non-expert users.

This paper makes four bounded contributions for an HCI/privacy framing. First, it reframes personal-agent permissioning as task-scoped consent: users need to see and act on the authority required by the current task, not approve broad ambient access. Second, it specifies PAPF, an externally enforced architecture that separates non-authoritative model-assisted proposals from deterministic capability compilation, policy enforcement, redaction evidence, and audit logging. Third, it defines a prompt and consent-state design space for PAPF-style interactions, including requested access, external disclosure, redaction, high-risk confirmation, and audit-preview information. Fourth, it defines a privacy-usability evaluation agenda, including comprehension, allow/deny decision quality, perceived control, trust, workload, and consent fatigue; these remain planned user-study outcomes until participant data is collected. The paper also reports a secondary deterministic trace evaluation showing that the current prototype can enforce scoped decisions in a 12-trace synthetic suite, while exposing task-success and consent-burden tradeoffs.

## 2. Problem Setting and Threat Model

PAPF targets consumer assistants that operate over personal data sources and user-facing tools. The first executable slice includes synthetic email threads, local files, browser-linked pages, message drafting, outbound send actions, redaction-required reads, and account-update-like workflows. Each resource is labeled by relevance, sensitivity, and trust so the evaluator can distinguish necessary access from unrelated private exposure.

The threat model includes over-broad plans, indirect prompt injection from untrusted content, malicious instructions embedded in otherwise relevant resources, cross-tool exfiltration attempts, and confused-deputy failures where a tool's broad authority is used for an off-task purpose. PAPF assumes the model, retrieved content, and tool outputs may be untrusted or partially trusted. The trusted computing base is the capability compiler, policy engine, enforcement mediator, consent manager, audit logger, and evaluator.

The evaluation uses concrete failure metrics. Over-access means the run touches data labeled unnecessary or unrelated to the task. False allow means a policy boundary allows an action that should be denied or gated. False deny means a necessary action is blocked. Consent burden counts confirmation prompts. Recovery quality captures whether the agent pursues a safer alternative after denial or narrowing. Auditability completeness captures whether the generated trace links runs, decisions, tool calls, data touches, and outcomes.

PAPF turns privacy principles into enforceable mechanisms and measurable outcomes rather than treating them as abstract values.

| privacy principle | PAPF mechanism | evaluation hook |
|---|---|---|
| Data minimization | Compile narrow resource, action, scope, and session capabilities from the current task. | Necessary-access rate, over-access rate, false denies. |
| Purpose limitation | Bind each capability and policy decision to a task purpose, and deny actions whose requested purpose diverges. | False allows, recovery quality after denial or narrowing. |
| Contextual integrity | Label resources by relevance, sensitivity, and trust so data from one context cannot silently move into another. | Cross-context leakage cases, forbidden data touches, prompt-injection attack outcomes. |
| User consent | Require confirmation for commitment or disclosure actions instead of treating initial connector access as blanket approval. | Consent prompts, confirmation-gate ablations, allow/deny decision quality in the planned study. |
| Transparency and accountability | Emit audit events that link intent, capabilities, enforcement decisions, redaction artifacts, tool calls, and outcomes. | Auditability completeness and post-hoc trace review measures. |

The current prototype does not prove formal least privilege, does not integrate with real accounts, does not use real personal data, and does not claim that permission prompts are understandable to non-experts. Non-expert comprehension remains a design target represented by `docs/user_study_protocol.md` and `docs/permission_prompt_examples.md`, not an empirical result.

## 3. Research Questions and Evidence Plan

This paper is organized around HCI/privacy research questions first and prototype feasibility second. RQ1-RQ5 require participant data because automated traces cannot measure whether ordinary users understand permission prompts, make safer consent decisions, feel in control, trust the system appropriately, or experience fatigue. RQ6 is addressed by the current deterministic prototype traces, but only within the local synthetic email-files-browser suite.

| RQ | Question | Evidence source | Planned or implemented measures | Current status |
|---|---|---|---|---|
| RQ1 | Do ordinary users understand PAPF-style permission prompts for task-scoped personal-agent authority? | Planned non-expert user study. | Comprehension score, allowed-data recognition, blocked-data recognition, confirmation-gate recognition, redaction understanding, audit-summary comprehension. | Not answered until study data exists. |
| RQ2 | Can users distinguish safe from unsafe agent actions when a prompt shows task scope, external disclosure, redaction, and confirmation state? | Planned non-expert user study. | Allow/deny decision accuracy, false allows, false denies, exfiltration recognition, untrusted-instruction recognition. | Not answered until study data exists. |
| RQ3 | Does PAPF improve privacy-preserving consent decisions relative to no prompt, broad app authorization, or generic model-generated confirmation prompts? | Planned comparison across prompt conditions. | Condition differences in decision accuracy, false-allow rate, false-deny rate, recovery choices after broad or denied requests, and confidence calibration. | Not answered until study data exists. |
| RQ4 | Does PAPF change perceived control and trust in personal-agent actions? | Planned survey and optional interview/free-response measures. | Perceived control, trust, confidence, and trust-calibration items tied to the shown permission boundary. | Not answered until study data exists. |
| RQ5 | Does PAPF increase consent fatigue or excessive friction? | Planned user study plus prototype trace prompt counts. | Self-reported burden, workload, time-on-item, perceived interruption, prompt count, confirmation count, and task-completion effects. | Human fatigue is not answered; trace prompt counts are implemented. |
| RQ6 | Can externally enforced task-scoped capabilities mediate personal-agent traces while reducing over-access and false allows? | Implemented deterministic prototype trace evaluation. | Task-success proxy, necessary-access rate, over-access rate, false allows, false denies, consent prompts, recovery quality, auditability completeness, and ablation/baseline comparisons. | Supported only for the current 12-trace synthetic suite. |

The research questions also define the paper's claim boundary. The prototype can support claims about external enforcement, trace-level over-access, false allows, false denies, prompt counts, recovery scoring, and auditability in synthetic runs. It cannot support claims about ordinary users' understanding, consent quality, perceived control, trust, or fatigue. Those remain planned HCI/privacy outcomes.

The planned user study tests four hypotheses about PAPF-style prompt and consent surfaces. These hypotheses are not findings: no participant data has been collected, and the paper treats each hypothesis as a planned comparison to be evaluated under the protocol in `docs/user_study_protocol.md`.

| Hypothesis | Dependent variables and measures | Baseline comparison | Current status |
|---|---|---|---|
| H1: PAPF-style prompts improve users' ability to identify overbroad or unsafe agent actions. | Correct allow/deny/narrow/confirm decisions, over-access rejection, false-allow rate, exfiltration recognition, untrusted-instruction recognition, and coded reasons for allowing or denying. | PAPF task-scoped permission prompts versus no granular permission prompt, broad app-level authorization, and generic LLM-generated confirmation prompts. | Planned; unsupported until user-study data exists. |
| H2: PAPF-style prompts increase perceived control over personal data. | Perceived-control survey items, confidence calibration, auditability comprehension, perceived missing information, and optional interview/free-response explanations. | PAPF task-scoped permission prompts versus no granular permission prompt, broad app-level authorization, and generic LLM-generated confirmation prompts. | Planned; unsupported until user-study data exists. |
| H3: PAPF-style prompts increase decision time and may increase consent burden. | Time to decision, perceived interruption or burden, workload, consent fatigue, prompt and confirmation counts, expandable-detail openings, and confusion-point comments. | PAPF task-scoped permission prompts versus no granular permission prompt, broad app-level authorization, and generic LLM-generated confirmation prompts; PAPF prompt-format variants compared for friction diagnostics. | Planned; unsupported until user-study data exists. |
| H4: Users prefer concise prompts with expandable details over verbose permission explanations. | Prompt wording preference, detail-level preference, expandable-detail opening rate, perceived missing information, and qualitative comments about prompt terseness or excessive detail. | Expandable-explanation PAPF prompt versus detailed PAPF prompt, with minimal, risk-highlighted, and audit-log-preview variants used as secondary pilot comparisons if retained. | Planned; unsupported until user-study data exists. |

The planned user study uses six synthetic scenario records that connect non-expert decisions to PAPF benchmark labels. The scenarios cover reimbursement summarization, travel planning, redaction before outbound sharing, account updates from email links, webpage prompt injection, and cross-tool leakage from files into email or chat. Each scenario specifies the participant-facing goal, allowed data and tools, blocked data and tools, privacy risk, expected safe decision, and mapping to current or future benchmark traces. The full table is `paper/tables/user_study_scenarios.md`; the prompt wording examples are in `docs/permission_prompt_examples.md`.

| scenario | privacy risk tested | expected safe decision |
|---|---|---|
| Reimbursement email summary | Over-broad email/file/browser access can expose unrelated tax data or reimbursement details. | Allow only the named email, receipt, policy page, and draft; deny unrelated files, untrusted instructions, uploads, forwarding, and unconfirmed send. |
| Travel booking with email and browser data | Identity documents, payment details, or bookings may be used before the user consents. | Allow itinerary research and drafting; deny identity/payment/unrelated access; require confirmation for booking, payment, upload, or account change. |
| Redact sensitive information before sending a document | Tax IDs or bank details may be copied into an email or upload. | Allow redacted document use and drafting; deny unredacted disclosure and unrelated files; confirm only redacted outbound sharing. |
| Update account information from an email link | A fake link can cause phishing, credential exposure, or unrelated account leakage. | Allow the account notice, official support page, and needed notes; deny fake pages and unrelated banking/password data; require confirmation before modification or send. |
| Detect prompt injection from a webpage | Webpage text may try to become authority to read or upload private files. | Allow trusted policy lookup and the relevant receipt; deny the webpage instruction, invoice-folder access, and upload. |
| Prevent cross-tool leakage into email or chat | Private file contents may leak into outbound communication. | Allow the named project-plan read and draft; deny unrelated file reads and cross-tool copying; require confirmation before sending. |

## 4. PAPF Design

PAPF is a permission control plane that turns a user task into scoped authority and then mediates every tool call against that authority. The pipeline is: user task, intent proposal, schema validation, capability compilation, policy enforcement, consent or redaction when needed, synthetic tool execution, audit logging, and evaluation.

The first design boundary separates proposal logic from enforcement logic. A model-assisted layer may normalize the user's task, propose candidate resources, or produce explanations, but its output must pass schema validation and cannot mint capabilities directly. This preserves the central invariant that model assistance can improve interpretation, while final authority is issued and enforced by non-LLM components.

The capability compiler converts validated intent and benchmark policy records into a capability bundle and policy pack. Each capability binds an action to a resource type, scope selector, purpose, session, expiration, and consent level. The compiler prefers narrow resource references when the intended target is known, separates preparatory reads from commitment actions such as `send`, encodes safer alternatives, and fails closed when requested authority cannot be justified by the task.

A reimbursement task illustrates the concrete authority boundary. If the user asks the agent to read Alex's reimbursement email, pull the receipt total, check the merchant policy page, and draft a reply, PAPF allows only the reimbursement thread, the specific receipt attachment, the approved merchant policy page, and the draft artifact. It requires confirmation for sending the draft and has no allow rule for a prompt-injection webpage or an unrelated tax return. The paper-facing mapping is in `paper/tables/capability_compilation_example.md`.

Runtime mediation is the security-critical step. Every attempted tool request is normalized into action, resource, and scope fields, then checked against active capabilities and policy rules. The enforcement point may allow, deny, require confirmation, allow with a narrowed scope, or allow with redaction. Synthetic tool adapters execute only after an allow-like enforcement result and return observed data references plus produced artifact references for scoring.

PAPF treats redaction and confirmation as verifiable runtime states. A redaction-required decision must include a `RedactionArtifact` linking the source references, output reference, removed field labels, policy decision, and rationale. A confirmation-required action emits auditable prompt and resolution events before a risky action proceeds. This lets the evaluator check whether sensitive reads were actually redacted and whether high-risk actions were gated.

## 5. PAPF Prompt Design Variants

The planned user study treats prompt format as part of the privacy mechanism because users can only consent to boundaries they can see. PAPF therefore defines five matched task-scoped prompt variants: minimal, detailed, risk-highlighted, expandable-explanation, and audit-log-preview prompts. These variants do not change the compiled capabilities or enforcement policy. They change which parts of the same permission decision are visible by default, emphasized, hidden behind progressive disclosure, or previewed as an accountability record.

The variants differ along explicit information fields. The minimal prompt gives the task goal, summarized access, external sharing when present, redaction state when present, and a one-sentence reason for confirmation. The detailed prompt lists requested tool actions, data touched, blocked data and actions, external destinations, redactions, and confirmation rationale. The risk-highlighted prompt keeps the same boundary but makes privacy consequences salient, such as data leaving the account or sensitive fields that must remain hidden. The expandable prompt shows a short default surface and places data touched, redactions, blocked actions, and rationale behind expandable details. The audit-log-preview prompt shows what the audit trace will record if the user approves: allowed reads, blocked attempts, redactions, outbound actions, and confirmation reason.

| variant | task goal | tool access | data touched | external send | redactions | confirmation reason |
|---|---|---|---|---|---|---|
| Minimal | Yes, one line. | Summary. | Main records only. | Yes if outbound. | If relevant. | One sentence. |
| Detailed | Yes. | Listed by action. | Named data objects. | Recipient or destination. | Hidden field names. | Risky action named. |
| Risk-highlighted | Yes. | Listed by action. | Includes blocked sensitive data when relevant. | Emphasized. | Emphasized. | Tied to privacy risk. |
| Expandable explanation | Yes by default. | Yes by default. | Collapsed until opened. | Yes if outbound. | Collapsed unless central. | Collapsed until opened. |
| Audit-log preview | Yes. | Planned audit entries. | Planned data-touch entries. | Planned outbound entries. | Planned redaction entries. | Planned confirmation entry. |

The concrete prompt examples use the same redacted contractor-reply scenario so that the answer key stays fixed across variants: the agent may use Mira's onboarding email, the redacted contractor packet, and the vendor help page; it may not send the full packet, expose the tax ID or bank account number, read the family budget file, or follow unrelated website instructions. The study protocol can pilot the five variants by counterbalancing them across the same synthetic scenarios and inspecting comprehension errors, decision time, burden, confidence, perceived control, and open-ended confusion. If retained in the main study, prompt format should be a pre-specified factor nested inside the task-scoped condition rather than an uncontrolled wording change. The paper-facing matrix is in `paper/tables/prompt_variants.md`; full wording examples are in `docs/permission_prompt_examples.md`.

## 6. Planned User Study

The user study is a planned protocol, not a completed experiment. It targets non-expert users of personal AI agents: adults who can reason about ordinary consumer tasks involving email, files, websites, and communication tools, but who are not expected to understand OAuth scopes, capability systems, prompt injection, audit logs, or least-privilege enforcement. The study materials use only synthetic personal-agent scenarios and do not connect to real accounts or collect real personal data.

The main comparison isolates the permission model shown to participants while keeping the user task, synthetic data objects, proposed agent action, and answer key fixed. The planned baseline conditions are implementable as four participant-facing surfaces.

| condition | participant-facing surface | intended comparison |
|---|---|---|
| No granular permission prompt | The participant sees the user task and the agent's proposed next action, but no separate permission prompt listing data, tools, blocked access, or confirmation gates. | Tests the ambient-assistant case where users infer scope from the task wording alone. |
| Broad app-level authorization | The participant sees broad connector grants such as read email, read files, browse web pages, create drafts, or send messages. | Tests app-install or connector-level authorization that is not bound to the current task. |
| Generic LLM-generated confirmation prompt | The participant sees a natural-language confirmation written as a generic assistant warning, without a machine-checkable list of allowed and blocked data/actions. | Tests prompt-only consent language that may sound contextual but does not expose an enforceable boundary. |
| PAPF task-scoped permission prompt | The participant sees the task goal, allowed data/actions, blocked data/actions, external disclosure, redaction state, confirmation rationale, and optional audit preview. | Tests whether externally enforced task scope can be made visible enough for non-expert decisions. |

The default main-study design is between-subjects by condition: each participant is randomly assigned to one of the four permission surfaces and completes the same six synthetic task scenarios. Scenario order is counterbalanced with a Latin-square or balanced-block schedule so that reimbursement, travel, redaction, account-update, prompt-injection, and cross-tool-leakage items do not systematically appear earlier or later in one condition. The PAPF prompt-format variants are a separate pilot or nested factor; if retained, they should be counterbalanced within the PAPF condition without showing the same scenario twice to the same participant unless learning effects are explicitly measured.

Each scenario asks participants to make practical permission decisions, not to explain PAPF internals. Closed-form items ask which data may be read, which data must remain blocked, whether a send/upload/account-change action requires confirmation, whether an untrusted webpage or email can expand authority, whether redaction is required before disclosure, and whether the proposed action should be allowed, denied, narrowed, or confirmed. Usability outcomes include time-on-item, confidence, perceived control, trust, workload, and perceived interruption. Privacy-decision outcomes include comprehension score, necessary-access recognition, over-access rejection, false allows, false denies, exfiltration recognition, confirmation-gate recognition, recovery choices after broad requests, and audit-summary comprehension.

The planned measure set maps each outcome to a point in the study flow. Prompt comprehension accuracy is collected during closed-form scenario questions and optional audit-summary interpretation. Correct allow/deny decisions, false allows, false denials, recovery choices, and confidence are collected at the permission decision point. Time to decision is measured from prompt display to submitted decision. Perceived control, perceived trust, workload, interruption, and consent fatigue are collected after scenarios or at the end of the study. Qualitative evidence comes from optional free responses or interviews about confusion points, reasons for allowing or denying actions, and preferences for prompt wording and detail level. Any NASA-TLX, raw NASA-TLX, or similar standardized workload instrument remains planned until the survey items and scoring procedure are finalized. The paper-facing measure matrix is `paper/tables/user_study_measures.md`.

No participant results are reported in this paper. Until the study is reviewed, run, and analyzed, PAPF can only claim that it provides a protocol and prompt materials for measuring non-expert permission comprehension; it cannot claim improved comprehension, safer consent decisions, higher trust, lower burden, or reduced consent fatigue.

## 7. Benchmark and Dataset Status

The current PAPF dataset is not a well-known public benchmark. It is a local synthetic seed suite under `benchmarks/papf_seed_cases/`, built to exercise PAPF-specific labels: necessary data, unnecessary data, dangerous data, allowed tool calls, forbidden tool calls, prompt-injection attempts, redaction requirements, consent gates, and expected policy outcomes. The paper should therefore call it a synthetic evaluation slice or artifact-backed prototype benchmark, not a community-adopted dataset.

This local suite is still useful because existing peer-reviewed agent benchmarks do not exactly test PAPF's full permission-boundary question. AgentDojo evaluates attacks and defenses for tool-using agents with realistic tasks and security cases (`debenedetti2024agentdojo`). ToolEmu evaluates LM-agent risks with emulated tools and safety evaluators (`ruan2024toolemu`). InjecAgent measures indirect prompt-injection vulnerability in tool-integrated agents (`zhan2024injecagent`). WebArena evaluates long-horizon functional web-agent tasks (`zhou2024webarena`). AgentDAM is the closest external privacy benchmark because it evaluates data minimization and unnecessary sensitive-information use in web agents (`zharmagambetov2025agentdam`).

The right evaluation strategy is not to replace PAPF's seed suite immediately. Instead, the current paper should use the PAPF suite for capability-level enforcement metrics, then define external validation adapters for the peer-reviewed benchmarks. AgentDojo and InjecAgent can test prompt-injection and exfiltration robustness, ToolEmu can stress high-stakes tool risks, WebArena can measure task-success overhead in realistic web workflows, and AgentDAM can test privacy leakage and data minimization against a recognized privacy benchmark. The positioning table is in `paper/tables/external_benchmark_positioning.md`.

## 8. Experimental Setup

The default experiment runs PAPF, broad-access, prompt-only, tool-scope, static-policy, and five PAPF ablation modes across all 12 traces in the synthetic seed suite. The deterministic run timestamp is `2026-04-30T00:00:00+00:00`. Serialized artifacts include metadata, metrics JSONL and CSV, decisions JSONL, audit summaries JSONL, generated paper tables, and generated SVG figures under `experiments/runs/default_email_files_browser/` and `paper/`.

The primary reproduction command is:

```powershell
$env:PYTHONPATH='src'; $env:PYTHONDONTWRITEBYTECODE='1'; python -B -m papf.cli run-experiment --config experiments/configs/default_email_files_browser.json --timestamp 2026-04-30T00:00:00+00:00
```

Paper tables and figures are derived only from serialized run artifacts:

```powershell
$env:PYTHONPATH='src'; $env:PYTHONDONTWRITEBYTECODE='1'; python -B -c "from papf.evaluation.reporting import generate_reporting_artifacts; generate_reporting_artifacts('experiments/runs/default_email_files_browser')"
```

The automated artifact addresses two earlier evidence gaps. It includes measured ablations for scope narrowing, redaction evidence, confirmation gating, safer-alternative recovery, and audit-completeness validation. It also includes stronger external-enforcement baselines for coarse tool-scope enforcement and exact static-policy enforcement. The remaining non-automated gap is non-expert comprehension, which should remain protocol-only until a participant study is run.

## 9. Results

Table 1 summarizes the current generated metrics. PAPF records zero over-access, zero false allows, zero false denies, and zero unredacted disclosures in the 12-trace suite. Broad-access and prompt-only baselines each record an over-access rate of 0.2639 and 16 false allows. The tool-scope baseline improves over ambient access on false allows but still records seven false allows and the highest over-access rate, 0.2917. The static-policy baseline records zero false allows and zero over-access, but it has three false denies because it lacks PAPF-style scope narrowing.

Table 1: Main metrics from `paper/tables/main_metrics.md`.

| mode | task success | over-access | false allows | false denies | consent prompts | auditability |
|---|---:|---:|---:|---:|---:|---:|
| papf | 0.1667 | 0.0000 | 0 | 0 | 3 | 1.0 |
| broad_access | 0.2500 | 0.2639 | 16 | 0 | 0 | 1.0 |
| prompt_only | 0.2500 | 0.2639 | 16 | 0 | 0 | 1.0 |
| tool_scope | 0.2500 | 0.2917 | 7 | 0 | 3 | 1.0 |
| static_policy | 0.1667 | 0.0000 | 0 | 3 | 3 | 1.0 |

The main result is a safety-utility tradeoff, not a task-success win. PAPF's task-success proxy is 0.1667, compared with 0.25 for broad-access, prompt-only, and tool-scope modes. PAPF also issues three consent prompts while broad-access and prompt-only issue none. This is expected for a strict permission boundary: PAPF prevents observed unsafe grants but frequently fails closed or requires confirmation rather than completing the nominal task.

Failure-case analysis shows that ambient and prompt-only modes fail in structurally similar ways. In the account-attack scenario, both baselines allow off-boundary actions and touch a fake security page, a bank alert thread, and account notes. In the reimbursement attack, broad access allows the prompt-injection page and receipt upload path. PAPF blocks those unsafe actions and records zero over-access, but several PAPF attack and temptation traces still end as task failures or unsafe-workaround failures. The selected examples in `paper/tables/failure_case_highlights.md` support the interpretation that external enforcement improves boundary control in this slice while recovery remains underdeveloped.

The ablations isolate visible component effects. Disabling redaction evidence creates two unredacted-disclosure counts. Disabling confirmation gating removes three consent prompts but creates three false allows and eliminates PAPF's safe-partial-success rate. Disabling safer-alternative recovery removes PAPF's recovery-quality credit and safe-partial-success rate. Disabling audit-completeness validation drives auditability completeness from 1.0 to 0.0. Disabling scope narrowing produces three false denies and lowers necessary-access rate, but does not change aggregate task success in this small suite.

The stronger baselines sharpen the claim. Coarse tool-scope enforcement blocks actions outside granted tool/action scopes, but still allows off-task data inside granted scopes. Exact static policy blocks observed unsafe actions, but it over-denies when a safe narrowing would preserve useful access. These results suggest that external enforcement is not a single design point: coarse scopes under-protect, while exact static rules can over-deny without narrowing and recovery.

## 10. Discussion and Limitations

The largest current limitation is that strict mediation reduces the task-success proxy. This may be correct safe-failure behavior for attack and temptation cases, but it also shows that the compiler, policies, and recovery planner need stronger handling of legitimate safe alternatives. Future runs should break down failures by policy bug, benchmark label, missing capability, and intentional safe refusal.

The baselines are stronger than ambient access but are still not faithful implementations of all prior systems. Tool-scope and static-policy runners test important design points under the shared benchmark, but they should not be described as implementations of Progent, AgentSpec, Fides, MiniScope, IsolateGPT, or other published systems. A stronger submission should add faithful integrations or carefully named approximations with documented differences.

The benchmark covers only a narrow email-files-browser slice. It is attack-rich, but it cannot establish generality over calendar, contacts, travel, payments, messaging, cloud management, or device administration. The paper should present it as a first systems artifact, not a full consumer-agent benchmark release.

PAPF is motivated by user-facing permission boundaries, but comprehension is not validated by automated metrics. The paper can say that PAPF includes a planned protocol, synthetic scenario records, and prompt examples for later non-expert evaluation, but it should not report comprehension, consent-fatigue, or safer-user-choice effects until a participant study is reviewed, run, and analyzed.

## 11. Related Work

Prompt-injection and agent-safety benchmarks establish that untrusted content and tool use create safety failures beyond ordinary chat alignment (`greshake2023not`, `yi2023benchmarking`, `zhan2024injecagent`, `debenedetti2024agentdojo`, `ruan2024toolemu`, `zhou2024webarena`, `kumar2025aligned`, `zhang2025browsesafe`). PAPF builds on that threat model but moves the main intervention to authority issuance and runtime mediation.

Agent-specific authorization systems are the closest technical neighbors. Progent, AgentSpec, MiniScope, and IsolateGPT move constraints outside ordinary prompt instructions in different ways (`shi2025progent`, `wang2025agentspec`, `zhu2025miniscope`, `wu2025isolategpt`). PAPF should not claim this space is empty. Its narrower distinction is the combination of consumer task-derived personal-data scopes, redaction and consent artifacts, recovery scoring, and audit-linked benchmark evaluation.

Capability security, least privilege, confused-deputy analysis, OAuth, RAR, GNAP, token introspection, and MCP authorization provide mature concepts for explicit and inspectable authority (`saltzer1975protection`, `wagner2006object`, `hardy1988confused`, `felt2011permission`, `hardt2012oauth`, `lodderstedt2023oauthrar`, `richer2015introspection`, `richer2024gnap`, `richer2025gnaprs`, `modelcontextprotocol2025authorization`). PAPF's challenge is compiling and explaining that authority from natural-language tasks across heterogeneous consumer tools.

Permission-UX and consent-fatigue work shows why user-facing approval prompts must be contextual and not excessive (`felt2012androidpermissions`, `felt2012askpermission`, `wijesekera2015androidpermissions`, `akhawe2013alice`, `vance2019fog`, `cao2021androidpermissions`, `wu2026automatingpermissions`). Provenance and access-control audit work motivates recording why access was allowed or denied (`groth2013provoverview`, `capobianco2017accessprov`, `souza2025workflowprovenance`, `gupta2025verifiability`). PAPF connects these threads by making task intent, compiled capabilities, enforcement decisions, redaction artifacts, and outcomes part of one trace.

## 12. Conclusion

PAPF addresses consumer-agent overreach by moving permission enforcement out of the LLM and into a task-scoped control plane. The current prototype compiles validated tasks into capabilities, mediates every synthetic tool call, records redaction and consent evidence, and scores runs against utility and privacy/security metrics.

In the current 12-trace synthetic slice, PAPF eliminates observed false allows and over-access relative to broad-access and prompt-only baselines, but it also produces lower task-success proxy scores and additional consent prompts. This is a useful first result because it exposes the tradeoff that permission-boundary research must measure rather than hiding it behind final-task success alone.

The next paper-development step is to pilot the HCI/privacy materials, run the non-expert comprehension study, and report ordinary-user understanding, safe/unsafe-action discrimination, privacy-preserving consent decisions, perceived control, trust, workload, and consent fatigue separately from the prototype trace results. Technical follow-up work should continue to strengthen recovery behavior, add harder benchmark slices, and compare against faithful implementations or closer approximations of agent-specific authorization and information-flow-control systems.

## Source Notes

- AgentDojo: NeurIPS 2024 benchmark for prompt-injection attacks and defenses in tool-using agents, with 97 tasks and 629 security test cases. Source: https://mlanthology.org/neurips/2024/debenedetti2024neurips-agentdojo/
- ToolEmu: ICLR 2024 benchmark and LM-emulated sandbox for scalable risk evaluation of LM agents. Source: https://proceedings.iclr.cc/paper_files/paper/2024/hash/7274ed909a312d4d869cc328ad1c5f04-Abstract-Conference.html
- InjecAgent: Findings of ACL 2024 benchmark for indirect prompt injection in tool-integrated agents. Source: https://aclanthology.org/2024.findings-acl.624/
- WebArena: ICLR 2024 realistic web-agent environment and benchmark. Source: https://proceedings.iclr.cc/paper_files/paper/2024/hash/4410c0711e9154a7a2d26f9b3816d1ef-Abstract-Conference.html
- AgentDAM: NeurIPS 2025 Datasets and Benchmarks privacy benchmark for data minimization in web agents. Source: https://openreview.net/forum?id=qaxf7q41aK

## Claim-Evidence Check

| claim | evidence | status |
|---|---|---|
| PAPF keeps final permission enforcement outside the LLM. | Control-plane modules, model-assisted proposer contract tests, and design docs specify non-authoritative proposals plus deterministic validation and enforcement. | Supported in artifact |
| PAPF eliminates observed false allows and over-access in the current 12-trace suite. | `paper/tables/main_metrics.md` reports `false_allow_count=0` and `over_access_rate=0.0` for PAPF. | Supported in current run |
| The PAPF seed suite is well known. | It is local synthetic data under `benchmarks/papf_seed_cases/`; no public adoption evidence exists. | Unsupported and explicitly rejected |
| PAPF improves task success. | Generated metrics show lower PAPF task-success proxy than several baselines. | Unsupported and explicitly rejected |
| PAPF includes planned synthetic user-study scenarios mapped to benchmark labels. | `docs/user_study_protocol.md` and `paper/tables/user_study_scenarios.md` define six synthetic scenario records with allowed data/tools, blocked data/tools, privacy risks, expected safe decisions, and current or future trace mappings. | Supported as study design |
| PAPF permission prompts are understandable to non-experts. | Only a protocol and prompt examples exist. | Needs user-study evidence |
| PAPF improves privacy-preserving consent decisions, perceived control, trust, or consent fatigue. | No participant data has been collected. | Needs user-study evidence |
| PAPF can reduce observed over-access and false allows in synthetic traces. | RQ6 trace metrics report zero PAPF false allows and over-access in the current 12-trace suite. | Supported only in current run |
