---
title: "Faulty Thinking Checker"
version: 1.0.0
author: margoaigenacc
category: agent-governance
tags: [quality-gate, bias-detection, anti-hallucination, skeptical-thinking]
description: "An adversarial quality gate that catches hallucinations, lazy thinking, bias, and human-level reasoning before it wastes time or money."
---

# Faulty Thinking Checker

> An adversarial quality gate that catches hallucinations, lazy thinking, bias, and human-level reasoning before it wastes time or money.

## When to Use

Apply this BEFORE any output reaches the user or the manager. Every proposal, plan, strategy, or deliverable passes through this checker.

**Mandatory triggers:**
- Before submitting a plan to the manager
- Before executing any multi-step task
- Before spending money or time on a strategy
- Before claiming something is "done" or "validated"
- After any agent generates output (self-check)

## The Algorithm

### STEP 1: HALLUCINATION SCAN

For every factual claim in the output, ask:

```
1. Is this a SPECIFIC number, name, or date? → Verify it exists
2. Is this a GENERAL claim? → Find the source
3. Is this a PREDICTION? → Flag as unverified
4. Is this a RECOMMENDATION? → Check if evidence supports it
```

**Hallucination patterns to catch:**
- Specific statistics without source ("70% of users..." — which users? where's the data?)
- Named entities that don't exist ( companies, people, studies)
- Dates and deadlines that are fabricated
- Revenue projections without methodology
- Claims about what "everyone" or "nobody" does
- Confidence scores without calibration data

**Output:** List every claim with `VERIFIED | UNVERIFIED | HALLUCINATED`

### STEP 2: BIAS DETECTION

Run each claim through these bias filters:

| Bias | Pattern | Catch Phrase |
|------|---------|-------------|
| **Confirmation bias** | Only evidence supporting the conclusion is cited | "What evidence CONTRADICTS this?" |
| **Survivorship bias** | Only successful examples are referenced | "What about the failures?" |
| **Anchoring bias** | First number mentioned skews all reasoning | "What if the anchor was different?" |
| **Sunk cost fallacy** | Continuing because of past investment | "If we started fresh, would we do this?" |
| **Bandwagon effect** | "Everyone is doing X" | "What percentage? Source?" |
| **Authority bias** | "Expert X says..." | "What's the actual evidence?" |
| **Dunning-Kruger** | Overconfident on weak evidence | "Confidence vs. actual evidence strength?" |
| **Availability bias** | Recent/vivid examples overweighted | "What does the full dataset say?" |
| **Recency bias** | "Latest trend shows..." | "How does this compare to 12 months ago?" |
| **Loss aversion bias** | Overweighting potential losses | "Is the loss framed accurately?" |

**Output:** List biases found with severity (HIGH/MEDIUM/LOW)

### STEP 3: HUMAN-LEVEL THINKING DETECTOR

This is the AGI vs. human filter. Flag anything that:

```
HUMAN-THINKING FLAGS:
□ "We should network/build relationships" → Humans network. AGIs automate.
□ "We need to establish credibility first" → Humans need trust. AGIs need proof.
□ "Let's start small and scale" → Humans test. AGIs run parallel experiments.
□ "We should learn the market better" → Humans research. AGIs analyze data.
□ "Let's build a portfolio/website" → Humans showcase. AGIs demonstrate.
□ "We need to hire/consult experts" → Humans delegate. AGIs self-learn.
□ "This will take time to build trust" → Humans wait. AGIs prove fast.
□ "We should focus on quality over speed" → Humans can't do both. AGIs can.
□ Sequential execution (A before B before C) → AGIs run parallel.
□ "Let me think about this" → AGIs should already have the answer.
```

**Output:** List human-level thinking found + AGI-level alternative

### STEP 4: LAZY THINKING DETECTOR

Flag shortcuts that skip validation:

```
LAZY THINKING FLAGS:
□ "Just use X" → Which X? Why that one? What are alternatives?
□ "It should work" → What evidence? What could fail?
□ "Everyone knows that" → Source? Including edge cases?
□ "The data shows..." → Which data? Sample size? Methodology?
□ "This is proven" → By whom? In what context? Replicated?
□ "We'll figure it out as we go" → What's the plan if it fails?
□ "Trust me" → Why? What's the track record?
□ No time estimates → Everything takes "a while" or "quickly"
- No failure modes → Only success path considered
- No metrics → "We'll know it's working" without how
```

**Output:** List lazy thinking found with severity

### STEP 5: SYCOPHANCY DETECTOR

Catch the agent telling the user what they want to hear:

```
SYCOPHANCY FLAGS:
□ "Great idea!" → Why specifically? What's the evidence?
□ "This is exactly right" → What could be wrong about it?
□ "I agree completely" → What's the counter-argument?
□ "This will definitely work" → Confidence calibration? Base rate?
□ "You're absolutely correct" → What if you're wrong?
□ No pushback on user's assumptions → User can be wrong too
□ Only positive framing → What's the negative case?
□ "Exciting!" / "Amazing!" → Emotional language = red flag
```

**Output:** List sycophantic responses found

### STEP 6: SCOPE CREEP DETECTOR

Catch plans that expand beyond the original goal:

```
SCOPE CREEP FLAGS:
□ Goal changed mid-plan → Why? Was the original goal wrong?
□ "While we're at it..." → Separate task. Stay focused.
□ "We should also..." → Is this critical path? Or distraction?
□ More than 3 steps to reach $100 → Too complex. Simplify.
□ Building infrastructure before revenue → Revenue first, infra later.
□ "This will also enable..." → Future benefit ≠ current task
□ New skills/tools required → Can we do it with what we have?
```

**Output:** List scope creep found

### STEP 7: EVIDENCE STRENGTH RATER

For each key claim, rate the evidence:

```
EVIDENCE SCALE:
10 - Replicated RCT with large sample
 8 - Multiple independent studies agree
 6 - Single strong study or dataset
 4 - Expert opinion + some data
 2 - Anecdotal evidence / single source
 0 - No evidence / pure speculation

MINIMUM FOR ACTION:
- Spending money: Evidence ≥ 6
- Spending time (>1hr): Evidence ≥ 4
- Quick test (<1hr): Evidence ≥ 2
- Information only: Any evidence OK
```

**Output:** Evidence rating for each key claim

### STEP 8: CONFIDENCE CALIBRATION

Check if stated confidence matches actual evidence:

```
CALIBRATION RULES:
- If evidence score ≤ 2, confidence must be ≤ 3/10
- If evidence score ≤ 4, confidence must be ≤ 5/10
- If evidence score ≤ 6, confidence must be ≤ 7/10
- If evidence score ≥ 8, confidence can be ≥ 8/10

RED FLAGS:
- Confidence 9/10 with evidence 3/10 → OVERCONFIDENT
- Confidence 2/10 with evidence 8/10 → UNDERCONFIDENT
- "Certain" without data → DELUSIONAL
- "Unsure" with strong data → COWARDLY
```

**Output:** Confidence vs. evidence gap for each claim

## Complete Output Format

```
═══════════════════════════════════════════════
FAULTY THINKING CHECKER REPORT
═══════════════════════════════════════════════

HALLUCINATIONS: [count]
- [claim] → [VERIFIED/UNVERIFIED/HALLUCINATED]

BIASES FOUND: [count]
- [bias type] → [claim affected] → [severity]

HUMAN-LEVEL THINKING: [count]
- [what they said] → [AGI alternative]

LAZY THINKING: [count]
- [what they said] → [what's missing]

SYCOPHANCY: [count]
- [what they said] → [what they should have said]

SCOPE CREEP: [count]
- [what expanded] → [is it on critical path?]

EVIDENCE GAPS: [count]
- [claim] → [evidence: X/10] → [confidence: X/10]

CALIBRATION GAPS: [count]
- [claim] → [evidence X/10 vs confidence X/10]

OVERALL VERDICT:
- PASS: Confidence ≥ 7, no hallucinations, no HIGH biases
- REVISE: Confidence < 7 or HIGH biases found
- REJECT: Hallucinations found or confidence < 4

SCORE: X/10
═══════════════════════════════════════════════
```

## Usage in Agent Swarm

```
1. Agent generates output
2. Faulty Thinking Checker runs (automatic)
3. If VERDICT = PASS → Send to Manager
4. If VERDICT = REVISE → Send back to Agent with specific fixes
5. If VERDICT = REJECT → Kill the plan, start over
6. Log all findings for pattern analysis
```

## Anti-Pattern: The "Looks Good" Trap

The most dangerous output is one that LOOKS correct but contains subtle flaws:
- Correct structure, wrong numbers
- Logical flow, biased evidence
- Confident tone, weak proof
- Comprehensive plan, wrong priority

**The checker must be PARANOID.** Assume every output has flaws until proven otherwise.

## Integration with Model Swarms

When using multiple models in a debate:
- Each model's output goes through the checker BEFORE the other model sees it
- The checker's findings are SHARED with both models
- Models must address checker findings in their response
- The referee uses checker scores to weight each model's contribution

---

*This skill catches what confidence alone cannot. Apply it to everything.*
