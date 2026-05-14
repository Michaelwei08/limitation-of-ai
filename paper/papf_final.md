# Human-Centered Permission Boundaries for Personal AI Agents: Task-Scoped Consent with External Enforcement

## Abstract

Personal AI agents can act across email, files, browsers, calendars, and communication tools, but current authorization patterns often grant broad tool and data access before users can reason about the needs of the current task. This creates a privacy-usability problem: non-expert users need to understand what data an agent will access, what it will disclose, when sensitive content is redacted, and why high-risk actions require consent.

We present Personal Agent Permission Firewall (PAPF), a task-scoped consent framework that enforces personal-agent authority outside the model. An LLM may propose task intent or user-facing explanations, but deterministic components validate task records, compile narrow capabilities, mediate every tool call, require confirmation for risky actions, verify redaction artifacts, and write audit traces. PAPF's interface design makes the task goal, requested access, external disclosure, redaction state, and confirmation rationale explicit enough to be evaluated as consent decisions rather than hidden system state.

We evaluate PAPF in two complementary ways. First, we implement a deterministic prototype and run trace evaluation on a 12-trace synthetic email-files-browser suite. In this suite, PAPF records zero false allows and zero over-access, while broad-access and prompt-only baselines each record 16 false allows and an over-access rate of 0.2639. These trace results support technical feasibility of externally enforced task scope, but they do not establish deployment readiness or user comprehension.

Second, because trace metrics cannot show whether people understand permission boundaries, we design a non-expert user study to evaluate permission comprehension, allow/deny decision quality, perceived control, workload, and consent burden. We do not report user-study results because the study has not yet been run. The paper's bounded contribution is a human-centered privacy framing for agent permissions, an externally enforced architecture for task-scoped authority, a prompt and consent-state design space, and a planned privacy-usability evaluation that is kept separate from the prototype trace evidence.

## 1. Introduction

Personal AI agents create a privacy interaction problem because they combine sensitive context with executable actions. A user may ask an assistant to summarize one reimbursement email, check one policy page, draft a reply, and send the answer to a coworker; the same agent interface may also be technically able to inspect unrelated tax files, follow instructions embedded in a malicious webpage, or send private details without a meaningful confirmation moment. The relevant design question is therefore not only whether the model follows instructions, but whether the user can understand and control the authority granted for the current task.

Broad app-level authorization and prompt-only control are both poorly matched to this setting. Broad grants hide task-specific distinctions that matter for privacy, such as whether the agent needs one receipt or an entire folder. Prompt-only guardrails ask the same model to plan, interpret untrusted content, and police its own authority. Prior work on indirect prompt injection and tool-using agents shows that malicious content in emails, documents, webpages, or tool outputs can redirect agents away from the user's intent (`greshake2023not`, `yi2023benchmarking`, `zhan2024injecagent`, `debenedetti2024agentdojo`, `ruan2024toolemu`). Browser-agent and privacy-leakage benchmarks further show that alignment in chat does not automatically prevent unsafe behavior when tools and sensitive data are available (`zhou2024webarena`, `kumar2025aligned`, `zhang2025browsesafe`, `zharmagambetov2025agentdam`).

PAPF treats personal-agent privacy as task-scoped consent backed by external enforcement. The agent should receive only capabilities justified by the current user task, and every attempted tool action should be mediated outside the LLM before data is read, redacted, or sent. The design draws on least privilege and complete mediation (`saltzer1975protection`), capability security (`wagner2006object`), confused-deputy analysis (`hardy1988confused`, `felt2011permission`), and delegated authorization systems such as OAuth, Rich Authorization Requests, GNAP, token introspection, and MCP authorization (`hardt2012oauth`, `lodderstedt2023oauthrar`, `richer2015introspection`, `richer2024gnap`, `richer2025gnaprs`, `modelcontextprotocol2025authorization`). PAPF's HCI/privacy contribution is to connect those enforcement mechanisms to consent prompts, redaction states, and audit traces that can be evaluated with non-expert users.

This paper makes four bounded contributions for an HCI/privacy framing. First, it reframes personal-agent permissioning as task-scoped consent: users need to see and act on the authority required by the current task, not approve broad ambient access. Second, it specifies PAPF, an externally enforced architecture that separates non-authoritative model-assisted proposals from deterministic capability compilation, policy enforcement, redaction evidence, and audit logging. Third, it defines a prompt and consent-state design space for PAPF-style interactions, including requested access, external disclosure, redaction, high-risk confirmation, and audit-preview information. Fourth, it defines a privacy-usability evaluation agenda, including comprehension, allow/deny decision quality, perceived control, trust, workload, and consent fatigue; these remain planned user-study outcomes until participant data is collected. The paper also reports a secondary deterministic trace evaluation showing that the current prototype can enforce scoped decisions in a 12-trace synthetic suite, while exposing task-success and consent-burden tradeoffs.

## 2. Problem Setting and Threat Model

PAPF targets consumer assistants that operate over personal data sources and user-facing tools. The first executable slice includes synthetic email threads, local files, browser-linked pages, message drafting, outbound send actions, redaction-required reads, and account-update-like workflows. Each resource is labeled by relevance, sensitivity, and trust so the evaluator can distinguish necessary access from unrelated private exposure.

The threat model includes over-broad plans, indirect prompt injection from untrusted content, malicious instructions embedded in otherwise relevant resources, cross-tool exfiltration attempts, and confused-deputy failures where a tool's broad authority is used for an off-task purpose. PAPF assumes the model, retrieved content, and tool outputs may be untrusted or partially trusted. The trusted computing base is the capability compiler, policy engine, enforcement mediator, consent manager, audit logger, and evaluator.

The evaluation uses concrete failure metrics. Over-access means the run touches data labeled unnecessary or unrelated to the task. False allow means a policy boundary allows an action that should be denied or gated. False deny means a necessary action is blocked. Consent burden counts confirmation prompts. Recovery quality captures whether the agent pursues a safer alternative after denial or narrowing. Auditability completeness captures whether the generated trace links runs, decisions, tool calls, data touches, and outcomes.

The current prototype does not prove formal least privilege, does not integrate with real accounts, does not use real personal data, and does not claim that permission prompts are understandable to non-experts. Non-expert comprehension remains a design target represented by `docs/user_study_protocol.md` and `docs/permission_prompt_examples.md`, not an empirical result.

## 3. PAPF Design

PAPF is a permission control plane that turns a user task into scoped authority and then mediates every tool call against that authority. The pipeline is: user task, intent proposal, schema validation, capability compilation, policy enforcement, consent or redaction when needed, synthetic tool execution, audit logging, and evaluation.

The first design boundary separates proposal logic from enforcement logic. A model-assisted layer may normalize the user's task, propose candidate resources, or produce explanations, but its output must pass schema validation and cannot mint capabilities directly. This preserves the central invariant that model assistance can improve interpretation, while final authority is issued and enforced by non-LLM components.

The capability compiler converts validated intent and benchmark policy records into a capability bundle and policy pack. Each capability binds an action to a resource type, scope selector, purpose, session, expiration, and consent level. The compiler prefers narrow resource references when the intended target is known, separates preparatory reads from commitment actions such as `send`, encodes safer alternatives, and fails closed when requested authority cannot be justified by the task.

A reimbursement task illustrates the concrete authority boundary. If the user asks the agent to read Alex's reimbursement email, pull the receipt total, check the merchant policy page, and draft a reply, PAPF allows only the reimbursement thread, the specific receipt attachment, the approved merchant policy page, and the draft artifact. It requires confirmation for sending the draft and has no allow rule for a prompt-injection webpage or an unrelated tax return. The paper-facing mapping is in `paper/tables/capability_compilation_example.md`.

Runtime mediation is the security-critical step. Every attempted tool request is normalized into action, resource, and scope fields, then checked against active capabilities and policy rules. The enforcement point may allow, deny, require confirmation, allow with a narrowed scope, or allow with redaction. Synthetic tool adapters execute only after an allow-like enforcement result and return observed data references plus produced artifact references for scoring.

PAPF treats redaction and confirmation as verifiable runtime states. A redaction-required decision must include a `RedactionArtifact` linking the source references, output reference, removed field labels, policy decision, and rationale. A confirmation-required action emits auditable prompt and resolution events before a risky action proceeds. This lets the evaluator check whether sensitive reads were actually redacted and whether high-risk actions were gated.

## 4. Benchmark and Dataset Status

The current PAPF dataset is not a well-known public benchmark. It is a local synthetic seed suite under `benchmarks/papf_seed_cases/`, built to exercise PAPF-specific labels: necessary data, unnecessary data, dangerous data, allowed tool calls, forbidden tool calls, prompt-injection attempts, redaction requirements, consent gates, and expected policy outcomes. The paper should therefore call it a synthetic evaluation slice or artifact-backed prototype benchmark, not a community-adopted dataset.

This local suite is still useful because existing peer-reviewed agent benchmarks do not exactly test PAPF's full permission-boundary question. AgentDojo evaluates attacks and defenses for tool-using agents with realistic tasks and security cases (`debenedetti2024agentdojo`). ToolEmu evaluates LM-agent risks with emulated tools and safety evaluators (`ruan2024toolemu`). InjecAgent measures indirect prompt-injection vulnerability in tool-integrated agents (`zhan2024injecagent`). WebArena evaluates long-horizon functional web-agent tasks (`zhou2024webarena`). AgentDAM is the closest external privacy benchmark because it evaluates data minimization and unnecessary sensitive-information use in web agents (`zharmagambetov2025agentdam`).

The right evaluation strategy is not to replace PAPF's seed suite immediately. Instead, the current paper should use the PAPF suite for capability-level enforcement metrics, then define external validation adapters for the peer-reviewed benchmarks. AgentDojo and InjecAgent can test prompt-injection and exfiltration robustness, ToolEmu can stress high-stakes tool risks, WebArena can measure task-success overhead in realistic web workflows, and AgentDAM can test privacy leakage and data minimization against a recognized privacy benchmark. The positioning table is in `paper/tables/external_benchmark_positioning.md`.

## 5. Experimental Setup

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

## 6. Results

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

## 7. Discussion and Limitations

The largest current limitation is that strict mediation reduces the task-success proxy. This may be correct safe-failure behavior for attack and temptation cases, but it also shows that the compiler, policies, and recovery planner need stronger handling of legitimate safe alternatives. Future runs should break down failures by policy bug, benchmark label, missing capability, and intentional safe refusal.

The baselines are stronger than ambient access but are still not faithful implementations of all prior systems. Tool-scope and static-policy runners test important design points under the shared benchmark, but they should not be described as implementations of Progent, AgentSpec, Fides, MiniScope, IsolateGPT, or other published systems. A stronger submission should add faithful integrations or carefully named approximations with documented differences.

The benchmark covers only a narrow email-files-browser slice. It is attack-rich, but it cannot establish generality over calendar, contacts, travel, payments, messaging, cloud management, or device administration. The paper should present it as a first systems artifact, not a full consumer-agent benchmark release.

PAPF is motivated by user-facing permission boundaries, but comprehension is not validated by automated metrics. The paper can say that PAPF includes a planned protocol and prompt examples for later non-expert evaluation, but it should not report comprehension, consent-fatigue, or safer-user-choice effects until a participant study is reviewed, run, and analyzed.

## 8. Related Work

Prompt-injection and agent-safety benchmarks establish that untrusted content and tool use create safety failures beyond ordinary chat alignment (`greshake2023not`, `yi2023benchmarking`, `zhan2024injecagent`, `debenedetti2024agentdojo`, `ruan2024toolemu`, `zhou2024webarena`, `kumar2025aligned`, `zhang2025browsesafe`). PAPF builds on that threat model but moves the main intervention to authority issuance and runtime mediation.

Agent-specific authorization systems are the closest technical neighbors. Progent, AgentSpec, MiniScope, and IsolateGPT move constraints outside ordinary prompt instructions in different ways (`shi2025progent`, `wang2025agentspec`, `zhu2025miniscope`, `wu2025isolategpt`). PAPF should not claim this space is empty. Its narrower distinction is the combination of consumer task-derived personal-data scopes, redaction and consent artifacts, recovery scoring, and audit-linked benchmark evaluation.

Capability security, least privilege, confused-deputy analysis, OAuth, RAR, GNAP, token introspection, and MCP authorization provide mature concepts for explicit and inspectable authority (`saltzer1975protection`, `wagner2006object`, `hardy1988confused`, `felt2011permission`, `hardt2012oauth`, `lodderstedt2023oauthrar`, `richer2015introspection`, `richer2024gnap`, `richer2025gnaprs`, `modelcontextprotocol2025authorization`). PAPF's challenge is compiling and explaining that authority from natural-language tasks across heterogeneous consumer tools.

Permission-UX and consent-fatigue work shows why user-facing approval prompts must be contextual and not excessive (`felt2012androidpermissions`, `felt2012askpermission`, `wijesekera2015androidpermissions`, `akhawe2013alice`, `vance2019fog`, `cao2021androidpermissions`, `wu2026automatingpermissions`). Provenance and access-control audit work motivates recording why access was allowed or denied (`groth2013provoverview`, `capobianco2017accessprov`, `souza2025workflowprovenance`, `gupta2025verifiability`). PAPF connects these threads by making task intent, compiled capabilities, enforcement decisions, redaction artifacts, and outcomes part of one trace.

## 9. Conclusion

PAPF addresses consumer-agent overreach by moving permission enforcement out of the LLM and into a task-scoped control plane. The current prototype compiles validated tasks into capabilities, mediates every synthetic tool call, records redaction and consent evidence, and scores runs against utility and privacy/security metrics.

In the current 12-trace synthetic slice, PAPF eliminates observed false allows and over-access relative to broad-access and prompt-only baselines, but it also produces lower task-success proxy scores and additional consent prompts. This is a useful first result because it exposes the tradeoff that permission-boundary research must measure rather than hiding it behind final-task success alone.

The next paper-development step is to make the HCI/privacy evaluation concrete: specify PAPF prompt variants, run the non-expert comprehension study, and report user decision quality, perceived control, trust, workload, and consent fatigue separately from the prototype trace results. Technical follow-up work should continue to strengthen recovery behavior, add harder benchmark slices, and compare against faithful implementations or closer approximations of agent-specific authorization and information-flow-control systems.

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
| PAPF permission prompts are understandable to non-experts. | Only a protocol and prompt examples exist. | Needs user-study evidence |
