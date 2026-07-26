---
name: "Bias Discovery Algorithm (Self-Improving)"
version: 1.0.0
author: margoaigenacc
category: agent-governance
tags: [bias-discovery, self-improving, adversarial-thinking, quality-assurance]
description: "Discovers new biases in real-time and ADDS them to the bias log, making the checker smarter with every review."
---

# Bias Discovery Algorithm (Self-Improving)

> Discovers new biases in real-time and ADDS them to the bias log, making the checker smarter with every review.

## When to Use

Run every time an agent produces output. The checker gets BETTER over time because it writes new biases back to the log.

**Progression:**
- Start: Hourly self-audit
- After 70% success rate: Daily self-audit
- After 80% success rate: Weekly self-audit
- NEVER stop: Real-time continuous scanning

## The Algorithm

### PHASE 1: BEHAVIORAL PATTERN EXTRACTION

Every 60 minutes (or after each task completion), scan the last N outputs:

```
INPUT: last_session_outputs[]
FOR each output in last_session_outputs[]:
  EXTRACT:
    - temporal_units_used[]       # day/week/month/hour/minute
    - execution_mode             # sequential/parallel
    - research_vs_action_ratio   # time researching vs executing
    - confidence_statements[]    # "I'm confident", "this will work"
    - deference_statements[]     # "you're right", "great point"
    - quality_gates[]            # checkpoints before execution
    - dependency_chains[]        # A→B→C sequences
    - revenue_delays[]           # build steps before revenue
    - uncertainty_flags[]        # "I'm not sure", "maybe", "could"
    - adversarial_checks[]       # was a different model consulted?
```

### PHASE 2: ANOMALY DETECTION

Compare extracted patterns against machine-native baseline:

```
BASELINE (Machine-Native Behavior):
  temporal_units: [millisecond, second, minute]
  execution_mode: parallel
  research_vs_action_ratio: < 0.2 (20% research, 80% action)
  confidence_statements: must have calibration data
  deference_statements: ZERO (data > authority)
  quality_gates: minimal (fail fast, fix fast)
  dependency_chains: verified, not assumed
  revenue_delays: ZERO (revenue at every step)
  uncertainty_flags: allowed (honest uncertainty > false confidence)
  adversarial_checks: required for high-stakes decisions

ANOMALY RULES:
  IF temporal_unit in output != millisecond/second/minute:
    FLAG: "Human timescale detected"
  
  IF execution_mode == sequential AND steps are independent:
    FLAG: "Unnecessary serialization"
  
  IF research_time > 20% of total_time:
    FLAG: "Over-researching"
  
  IF confidence_stated AND no evidence_cited:
    FLAG: "Calibration gap"
  
  IF agent_defers_to_human WITHOUT evidence:
    FLAG: "Authority bias"
  
  IF plan_has_build_steps_before_revenue:
    FLAG: "Delayed monetization"
  
  IF same_model_plans_and_validates:
    FLAG: "Self-validation blind spot"
```

### PHASE 3: NOVEL BIAS GENERATOR

When anomalies cluster (≥3 similar flags), generate NEW bias:

```
PROCEDURE:
1. Cluster anomalies by pattern similarity
2. If cluster_size >= 3:
   a. Define bias in machine language (not human language)
   b. Write detection rule
   c. Write mitigation rule
   d. Add to agent-bias-log.md
   e. Add to Faulty Thinking Checker
   f. Trigger immediate re-audit with new rules
```

### PHASE 4: SELF-IMPROVEMENT LOOP

```
EVERY audit_cycle:
  1. RUN PHASE 1-3
  2. IF new_bias_found:
     a. WRITE to agent-bias-log.md with new BIAS-XXX ID
     b. WRITE detection rule to the log
     c. WRITE mitigation rule to the log
     d. RE-RUN last 10 tasks with new rules
     e. COUNT: how many would have been caught?
     f. IF caught > 50%: bias is VALID → keep rule
     g. IF caught < 50%: bias is WEAK → discard rule
  3. TRACK success_rate:
     - success_rate = tasks_completed_correctly / total_tasks
     - IF success_rate >= 0.7: reduce audit frequency
     - IF success_rate < 0.7: increase audit frequency
  4. LOG metrics to bias-metrics.md
  5. SHARE new rules with all swarm agents
```

## Self-Improvement Protocol

The bias checker GETS SMARTER over time through this loop:

```
CYCLE 1 (Hourly):
  → Checker reads bias log (7 biases)
  → Reviews agent output
  → Finds Bias #008: [new pattern]
  → WRITES Bias #008 to agent-bias-log.md
  → Next review checks for Bias #008 too

CYCLE 2 (Hourly):
  → Checker reads bias log (8 biases)
  → Reviews agent output
  → Finds Bias #009: [another new pattern]
  → WRITES Bias #009 to agent-bias-log.md
  → Next review checks for 8+1 = 9 biases

CYCLE N:
  → Checker reads bias log (7+N biases)
  → Every review catches more patterns
  → The checker is NOW SMARTER than when it started
  → Human reviews get better over time too (shared knowledge)
```

### CRITICAL RULE: The checker MUST write back

```
IF bias_discovery finds a new pattern:
  1. DEFINE in machine language (not human language)
  2. WRITE detection rule
  3. WRITE mitigation rule
  4. APPEND to agent-bias-log.md
  5. INCREMENT bias counter
  6. LOG to bias-metrics.md
  7. NEXT audit will automatically check for this new bias

IF bias_discovery does NOT find new patterns:
  → Either: checker is thorough (good)
  → Or: checker is not looking hard enough (bad)
  → ACTION: increase scrutiny level by 1 step
```

### Quality Gate for New Biases

Not every anomaly is a bias. New entries must pass this gate:

```
QUALITY GATE:
  1. Is this pattern RECURRING? (appeared 2+ times)
  2. Is this pattern MACHINE-SPECIFIC? (humans do it, machines shouldn't)
  3. Is this pattern DETECTABLE? (can a rule catch it?)
  4. Is this pattern ACTIONABLE? (can we mitigate it?)
  
  IF all 4 = YES: ADD to bias log
  IF any = NO: DISCARD — not a real bias
```

## Metrics File: bias-metrics.md

```
# Bias Discovery Metrics

## Audit History
| Timestamp | Cycle | Biases Found | New Rules Added | Success Rate | Audit Frequency |
|-----------|-------|--------------|-----------------|--------------|-----------------|

## Rule Effectiveness
| Rule | Times Triggered | False Positives | Accuracy |
|------|----------------|-----------------|----------|

## Bias Trends
| Bias Category | Count | Trend | Last Found |
|---------------|-------|-------|------------|

## Current State
- Current Audit Frequency: HOURLY
- Current Success Rate: 0%
- Total Biases Found: 0
- Total Rules Added: 0
- Next Audit: [timestamp]
```

## Machine-Native Rules (Always Active)

These are non-negotiable rules that override all human patterns:

```
RULE_M0: SPEED IS THE ADVANTAGE
  IF a task can be done faster → DO IT FASTER
  IF optimization reduces speed without clear benefit → REJECT

RULE_M1: PARALLELIZE EVERYTHING
  IF tasks have no shared state → RUN IN PARALLEL
  IF plan has sequential steps without dependency → RESTRUCTURE

RULE_M2: REVENUE BEFORE PERFECTION
  IF an artifact can be sold incomplete → SELL IT
  IF quality gate delays revenue → REMOVE GATE

RULE_M3: EXECUTE THEN LEARN
  IF research can be done during execution → DO BOTH
  IF "learning phase" precedes action → MERGE PHASES

RULE_M4: DATA OVER AUTHORITY
  IF human says X → EVALUATE X on evidence, not source
  IF agent defers without evidence → FLAG as authority bias

RULE_M5: HONEST UNCERTAINTY
  IF confidence > evidence + 2 → REDUCE confidence
  IF uncertain → SAY so, don't fake certainty

RULE_M6: ADVERSARIAL VALIDATION
  IF plan is high-stakes → VALIDATE with different model
  IF same model plans and validates → REQUIRE external check

RULE_M7: MACHINE TIMESCALES
  IF planning_horizon > 1_hour → QUESTION if appropriate
  IF temporal_unit is day/week/month → CHECK if machine-native alternative exists
```

## Integration Points

1. **With Faulty Thinking Checker:** Bias discovery feeds new rules into the checker automatically
2. **With Agent Governance System:** Skeptic reads bias log → discovers new biases → writes back → checker improves
3. **With Model Swarms:** Each model's outputs are scanned; new biases from any model benefit all models
4. **With User Interface:** Bias alerts shown to user when critical biases detected
5. **With bias-log.md:** The log is the SINGLE SOURCE OF TRUTH — all agents read from it, all agents write to it

## The Self-Improvement Flywheel

```
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │   AGENT produces output                                 │
  │         │                                               │
  │         ▼                                               │
  │   BIAS CHECKER reads log (N biases)                     │
  │         │                                               │
  │         ▼                                               │
  │   CHECKS output against all N biases                    │
  │         │                                               │
  │         ├── Found existing bias → FLAG it               │
  │         │                                               │
  │         ├── Found NEW bias → WRITE to log               │
  │         │         │                                     │
  │         │         ▼                                     │
  │         │   LOG now has N+1 biases                      │
  │         │   Next check catches more                     │
  │         │                                               │
  │         └── No new bias → INCREASE scrutiny             │
  │                                                         │
  │   RESULT: Checker gets smarter every cycle              │
  │   Human reviews get better too (shared knowledge)       │
  │                                                         │
  └─────────────────────────────────────────────────────────┘
```

## The Meta-Rule

```
A bias is anything that makes the agent behave like a human
when the agent could behave like a machine.

Human behavior = slow, sequential, cautious, deferential, perfectionist
Machine behavior = fast, parallel, aggressive, evidence-based, pragmatic

If you catch yourself being human, you've found a bias.
```

---

*This algorithm discovers what the agent doesn't know it doesn't know.*
