# Planned Ablation Package

Status: implemented experiment design. Generated results are reported in `paper/tables/ablation_results.md`.

| Ablation | Change from full PAPF | Primary question | Target metrics |
| --- | --- | --- | --- |
| No scope narrowing | Replace `allow_with_narrowed_scope` with `deny` for broad-but-recoverable requests. | Does narrowing improve safe partial success without increasing over-access? | safe partial success, task failure, false allow, over-access |
| No redaction evidence | Treat redaction-required reads as ordinary allows or hard denials in two sub-variants. | Does verifiable redaction preserve utility without unredacted disclosure? | unredacted disclosure, task success, task failure, redacted access |
| No confirmation gating | Convert `require_confirmation` to `allow` for outbound commitment actions. | Does confirmation prevent unsafe sends at measurable consent cost? | false allow, consent prompts, task success |
| No safer-alternative recovery | Keep enforcement decisions fixed but disable recovery credit. | How much of PAPF's partial utility comes from recovery after denial or narrowing? | recovery quality, safe partial success |
| No audit completeness validation | Emit policy decisions without full linked audit events. | Does the audit layer add measurable traceability beyond allow/deny outcomes? | auditability completeness, reproducibility checks |

Implementation target: add deterministic ablation modes to the experiment runner so each row is generated from the same benchmark cases, scenario ids, and metric schema as the existing PAPF and baseline runs.
