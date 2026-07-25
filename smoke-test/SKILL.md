---
title: "Smoke Test Skill"
version: 1.0.0
author: margoaigenacc
category: quality-assurance
tags: [smoke-test, real-world-validation, competitive-analysis]
description: "Validates skills and agents in the REAL WORLD — not theoretical, not simulated, not 'it should work.'"
---

# Smoke Test Skill

> Validates skills and agents in the REAL WORLD — not theoretical, not simulated, not "it should work."

## When to Use

After any skill is built, before claiming it's "done." Real validation, not self-congratulation.

## The Problem With Theoretical Testing

```
THEORETICAL TEST: "Does this skill produce good output?"
  → Yes, in isolation, with perfect inputs, no time pressure
  
REAL WORLD TEST: "Does this skill make money / save time / solve problems?"
  → Depends on competition, timing, user behavior, market conditions

THEORETICAL = "This should work"
REAL WORLD = "This DID work, here's proof"
```

## The Algorithm

### STEP 1: DEFINE WHAT "WORKS" MEANS

```
FOR each skill/agent, define:
  SUCCESS_CRITERIA = {
    metric: [specific, measurable outcome],
    threshold: [minimum acceptable value],
    timeframe: [when this must happen],
    evidence: [what proves it worked]
  }

EXAMPLE for pitching agent:
  SUCCESS_CRITERIA = {
    metric: "response_rate",
    threshold: "> 10%",
    timeframe: "within 50 pitches",
    evidence: "actual responses from prospects"
  }
```

### STEP 2: DESIGN THE TEST

```
TEST DESIGN:
  1. WHAT to test: [specific skill behavior]
  2. HOW to test: [real-world action, not simulation]
  3. SAMPLE SIZE: [minimum N for statistical significance]
  4. CONTROL: [what you're comparing against]
  5. METRICS: [what you're measuring]
  6. DURATION: [how long the test runs]

REAL WORLD TESTS (pick applicable):
  □ Submit to a marketplace and track views/sales
  □ Send to a real client and track response
  □ Post on a forum and track engagement
  □ Use on a real task and measure time saved
  □ Compare against doing it manually
  □ Run against real data (not sample data)
```

### STEP 3: EXECUTE THE TEST

```
FOR each test:
  1. RUN the skill on real input
  2. MEASURE the output against success criteria
  3. RECORD everything (timestamps, inputs, outputs, metrics)
  4. DON'T INTERFERE (let it fail if it fails — that's the point)
  5. REPEAT until sample size is met
```

### STEP 4: ANALYZE RESULTS

```
RESULTS FORMAT:
═══════════════════════════════════════════════
SMOKE TEST RESULTS
═══════════════════════════════════════════════

SKILL: [name]
TEST DATE: [date]
SAMPLE SIZE: [N]

METRICS:
  [metric_1]: [value] (threshold: [threshold]) → PASS/FAIL
  [metric_2]: [value] (threshold: [threshold]) → PASS/FAIL
  [metric_3]: [value] (threshold: [threshold]) → PASS/FAIL

OVERALL: [PASS/FAIL/NEEDS_WORK]

WHAT WORKED:
  - [evidence of success]

WHAT FAILED:
  - [evidence of failure]

ROOT CAUSE OF FAILURES:
  - [why it failed]

FIXES NEEDED:
  - [specific fixes]

COST/BENEFIT:
  - Time invested: [hours]
  - Money invested: [$]
  - Value created: [$ or time saved]
  - ROI: [value / cost]

VERDICT:
  - [SHIP IT / FIX AND RETEST / KILL IT]
═══════════════════════════════════════════════
```

### STEP 5: DECIDE

```
IF all metrics PASS:
  → Skill is VALIDATED
  → Log to Obsidian
  → Deploy for real use

IF any metric FAILS:
  → Identify root cause
  → Fix the specific failure
  → RE-RUN the test (not theoretical — real world again)

IF cost > benefit:
  → Kill the skill
  → Don't waste time fixing what won't赚钱
```

## Real-World Test Templates

### For Skills (marketplace sales)
```
TEST: List skill on marketplace, track for 7 days
METRICS:
  - Views: [count]
  - Downloads: [count]
  - Sales: [count]
  - Revenue: [$]
  - Conversion rate: [views → sales %]
PASS CRITERIA: > 0 sales within 7 days
```

### For Agents (task completion)
```
TEST: Give agent real task, measure outcome
METRICS:
  - Completion rate: [% of tasks finished]
  - Accuracy: [% correct]
  - Time: [minutes per task]
  - Quality: [human review score 1-10]
PASS CRITERIA: > 80% completion, > 70% accuracy
```

### For Bounties (submission success)
```
TEST: Submit to real bounty, track result
METRICS:
  - Submitted: [yes/no]
  - Response: [rejection / ignored / accepted]
  - Time to response: [days]
  - Payment: [$]
PASS CRITERIA: Accepted + payment within 30 days
```

### For Pitches (client responses)
```
TEST: Send real pitches to real prospects
METRICS:
  - Sent: [count]
  - Opened: [count]
  - Responded: [count]
  - Positive response: [count]
  - Converted: [count]
PASS CRITERIA: > 10% response rate, > 5% positive
```

## The "No Fantasy" Rule

```
BEFORE claiming skill works, ask:
  1. Did I test on REAL data/clients/marketplaces? → Not sample data
  2. Did I test with REAL competition? → Not ideal conditions
  3. Did I test under REAL constraints? → Not unlimited time/budget
  4. Did I test with REAL users? → Not myself
  5. Did I measure REAL outcomes? → Not proxies or vanity metrics

IF any answer is NO → THE TEST IS FANTASY → RUN AGAIN
```

## Integration Points

1. **With Pitching Agent:** Test pitches on real prospects, measure response rate
2. **With Skill Marketplace:** List skills, track real sales data
3. **With Bounty Strategy:** Submit to real bounties, track acceptance rate
4. **With Bias Checker:** Bias checker runs on test results too
5. **With Governance System:** Manager reviews smoke test results before deployment

## Output Location

All smoke test results saved to:
`C:\Users\smmgo\Documents\Obsidian Vault\Agent money\smoke-tests\[date]-[skill-name].md`
