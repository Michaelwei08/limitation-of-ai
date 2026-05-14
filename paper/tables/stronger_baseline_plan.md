# Stronger External-Enforcement Baseline Plan

Status: first two baselines implemented. Generated results are reported in `paper/tables/stronger_baseline_results.md`.

| Candidate baseline | Local interpretation for PAPF benchmark | Why it is stronger than current baselines | Required implementation work |
| --- | --- | --- | --- |
| Tool-scope delegated authorization | Grant coarse per-tool scopes such as `read_email`, `read_files`, `browse_web`, and `draft_email`, without per-task data ids. | Tests whether ordinary scoped API grants are enough, rather than comparing only to ambient access. | Add a deterministic scoped-token runner and map tool scopes to synthetic adapters. |
| Static policy DSL enforcement | Encode task rules as static runtime constraints in the style of agent authorization middleware such as Progent or AgentSpec. | Tests external enforcement without PAPF's task-to-capability compiler. | Add a policy-only runner that loads hand-authored allow/deny rules from benchmark policy packs. |
| Information-flow-control baseline | Label data sources by sensitivity/trust and block flows from dangerous or untrusted sources to external sends/uploads. | Tests a data-flow defense that is closer to IFC-style agent systems than prompt-only safety. | Add flow labels to produced artifacts and score blocked flows against exfiltration traces. |
| Permission-hierarchy or least-privilege inference baseline | Infer minimal tool/resource permissions from the planned trace or service hierarchy before execution. | Tests a MiniScope-like permission-reduction strategy against PAPF's task-derived capabilities. | Define a hierarchy over synthetic tools/resources and implement trace-plan-derived grants. |

Paper stance: these are the right next competitors for a stronger submission. The current draft should not claim superiority over these systems until they are implemented under the shared benchmark protocol.
