# External Benchmark Positioning

| benchmark | peer-reviewed status checked | what it evaluates | use for PAPF | gap relative to PAPF |
|---|---|---|---|---|
| PAPF seed suite | Local synthetic artifact, not a known public benchmark | Task-scoped permission enforcement over email, files, and browser traces | Primary current artifact for necessary/unnecessary/dangerous data labels and external enforcement metrics | Narrow, synthetic, and not community-adopted |
| AgentDojo | NeurIPS 2024 Datasets and Benchmarks Track | Prompt-injection attacks and defenses for tool-using agents over realistic tasks | External attack-suite adapter for utility/security tradeoffs | Does not label task-scoped personal-data grants or consent burden by default |
| ToolEmu | ICLR 2024 | Scalable LM-agent risk discovery with emulated tools and safety evaluation | Stress-test PAPF-style policies against broader high-stakes tool risks | Uses emulated tools and risk judges rather than PAPF's concrete capability mediation |
| InjecAgent | Findings of ACL 2024 | Indirect prompt-injection vulnerability in tool-integrated LLM agents | External prompt-injection/exfiltration cases for PAPF enforcement | Focuses on attack success, not user-comprehensible scoped permissions |
| WebArena | ICLR 2024 | Functional correctness of long-horizon web-agent tasks | Utility benchmark for measuring PAPF overhead on realistic web workflows | Does not directly score unnecessary private-data exposure or false allows |
| AgentDAM | NeurIPS 2025 Datasets and Benchmarks Track | Privacy leakage and data minimization in web agents | Closest external privacy benchmark for necessary versus unnecessary data use | Defense framing is not an external permission firewall with consent and audit artifacts |
