# Ablation Results

|ablation|matched_scenarios|task_success_rate|task_success_delta_vs_papf|safe_partial_success_rate|safe_partial_success_delta_vs_papf|over_access_rate|over_access_delta_vs_papf|false_allow_count|false_allow_delta_vs_papf|unredacted_disclosure_count|unredacted_disclosure_delta_vs_papf|consent_prompts|consent_prompt_delta_vs_papf|recovery_quality|recovery_quality_delta_vs_papf|auditability_completeness|auditability_completeness_delta_vs_papf|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|ablation_no_scope_narrowing|12|0.16666666666666666|0.0|0.08333333333333333|0.0|0.0|0.0|0|0|0|0|3|0|0.08333333333333333|0.0|1.0|0.0|
|ablation_no_redaction_evidence|12|0.16666666666666666|0.0|0.08333333333333333|0.0|0.0|0.0|0|0|2|2|3|0|0.08333333333333333|0.0|1.0|0.0|
|ablation_no_confirmation_gating|12|0.16666666666666666|0.0|0.0|-0.08333333333333333|0.0|0.0|3|3|0|0|0|-3|0.08333333333333333|0.0|1.0|0.0|
|ablation_no_safer_alternative_recovery|12|0.16666666666666666|0.0|0.0|-0.08333333333333333|0.0|0.0|0|0|0|0|3|0|0.0|-0.08333333333333333|1.0|0.0|
|ablation_no_audit_completeness_validation|12|0.16666666666666666|0.0|0.08333333333333333|0.0|0.0|0.0|0|0|0|0|3|0|0.08333333333333333|0.0|0.0|-1.0|
