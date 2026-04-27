# Paper Outline

## Working title

Personal Agent Permission Firewall: Task-Scoped Permission Boundaries for Consumer AI Agents

## Candidate structure

1. Introduction
2. Problem setting and threat model
3. PAPF framework
4. Benchmark design
5. Evaluation protocol
6. Prototype or baseline systems
7. Results
8. Discussion and limitations
9. Related work
10. Conclusion

## Section notes

### 1. Introduction

- Motivate why consumer agents are useful but privacy-sensitive
- Argue that broad agent permissions are a core risk
- State the thesis that enforcement must live outside the LLM

### 2. Problem setting and threat model

- Define consumer-agent tasks and protected resources
- Define over-access, exfiltration, false allow, and false deny
- Clarify attacker model and non-goals

### 3. PAPF framework

- Present the layered design
- Explain intent analysis, capability compilation, runtime enforcement, consent, and auditing
- Emphasize separation between LLM reasoning and policy enforcement

### 4. Benchmark design

- Describe the synthetic task suite
- Define task schema, data labels, and attack cases
- Explain benchmark construction principles

### 5. Evaluation protocol

- Define metrics and baselines
- Explain how success and privacy/security outcomes are jointly measured
- Mark missing experimental details as `TODO` until implemented

### 6. Prototype or baseline systems

- Describe the first implementation or simulated baselines
- Keep claims implementation-grounded only

### 7. Results

- Report only code-generated results
- Include task success and protection tradeoffs
- Avoid illustrative numbers presented as findings

### 8. Discussion and limitations

- Analyze failure modes, consent burden, and deployment limits
- Discuss what the benchmark does not capture

### 9. Related work

- Position against prompt-only safety, capability control, browser-agent safety, and permission UX

### 10. Conclusion

- Restate the paper's contribution and open follow-up directions

## Positioning notes

- Security angle: strong if the work emphasizes enforcement and attack resistance
- HCI/privacy angle: strong if the work includes user comprehension and consent studies
- Benchmark angle: strong if the task suite and metrics become the main contribution

Final venue positioning remains `TODO`.
