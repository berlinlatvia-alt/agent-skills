---
name: "24-Hour Demand Validation Skill"
version: 1.0.0
author: margoaigenacc
category: business-intelligence
tags: [demand-validation, market-research, signal-scoring, MVP]
description: "Validates product demand in 24 hours using real-world signals, not theory."
---

# Demand Validation Skill

> Validates product demand in 24 hours using real-world signals, not theory.

## When to Use

Before building ANY product, run this. If demand is not validated, don't build.

## The 24-Hour Validation Algorithm

### HOUR 0-1: SIGNAL COLLECTION

Collect signals from 5 sources in parallel:

```
SOURCE 1: Search Volume
  - Check Google Trends for product keywords
  - Check Reddit mention frequency
  - Check GitHub star velocity for similar tools
  - SIGNAL: rising > stable > falling

SOURCE 2: Competitor Analysis
  - Find 3-5 similar products
  - Check their pricing, features, reviews
  - Check their traffic (SimilarWeb/Ahrefs free tier)
  - SIGNAL: growing market > saturated > declining

SOURCE 3: Pain Validation
  - Search Reddit/Twitter for complaints about existing solutions
  - Count "I wish", "I need", "frustrated with" posts
  - SIGNAL: many complaints > few complaints > no complaints

SOURCE 4: Willingness-to-Pay Signals
  - Check if similar products charge money (not free)
  - Check if people ask "where can I buy" vs "is there a free alternative"
  - Check Kickstarter/Indiegogo funding for similar products
  - SIGNAL: people pay > people want free > nobody cares

SOURCE 5: Direct Outreach (optional but strongest)
  - Post in 3 relevant communities: "I'm building X, would you pay $Y for it?"
  - Track responses in 24 hours
  - SIGNAL: >5 interested > 1-5 interested = 0 interested
```

### HOUR 1-2: SCORING

```
DEMAND SCORE = sum of signals (0-10 per source)

SCORE 40-50: STRONG DEMAND → Build immediately
SCORE 25-39: MODERATE DEMAND → Build MVP, test with real users
SCORE 10-24: WEAK DEMAND → Pivot or kill
SCORE 0-9: NO DEMAND → Kill. Don't build.

MULTIPLIERS:
  x1.5 if >3 people said they'd pay
  x0.5 if all signals are "free alternative" requests
  x2.0 if competitor just raised funding (market validation)
  x0.3 if no competitor exists (maybe no market)
```

### HOUR 2-4: COMPETITIVE EDGE CHECK

```
For each validated product idea, ask:
1. What makes this DIFFERENT from existing solutions?
2. Can we build it FASTER than competitors?
3. Can we price it LOWER without sacrificing quality?
4. Can we reach customers FASTER than competitors?
5. Is there a TIMING advantage (new platform, new regulation, new trend)?

IF answer to any is YES → proceed
IF answer to all is NO → kill or pivot
```

### HOUR 4-8: MVP DECISION

```
IF demand score >= 25:
  BUILD MVP in next 4 hours
  MVP = simplest version that solves the core problem
  MVP must be USABLE (not just a prototype)
  MVP must have a way to collect payment (Stripe, Gumroad, etc.)

IF demand score < 25:
  DON'T BUILD
  Instead: explore adjacent ideas with higher demand scores
  OR: wait for demand signals to strengthen
```

### HOUR 8-24: REAL-WORLD TEST

```
IF MVP built:
  1. List on 1 marketplace (agentskill.sh, Gumroad, etc.)
  2. Post in 3 communities (Reddit, Twitter, Discord)
  3. Track: views, clicks, purchases, feedback
  4. If >0 sales in 24 hours → validated
  5. If 0 sales → iterate on pricing/messaging or kill
```

## Output Format

```
DEMAND VALIDATION REPORT
========================
Product: [name]
Score: [X/50]
Verdict: [BUILD / MVP / KILL / PIVOT]

Signals:
  Search Volume: [X/10] - [evidence]
  Competitor Analysis: [X/10] - [evidence]
  Pain Validation: [X/10] - [evidence]
  Willingness to Pay: [X/10] - [evidence]
  Direct Outreach: [X/10] - [evidence]

Competitive Edge:
  [What makes this different]

Next Step:
  [Specific action with deadline]
```

## Integration with memory.db

```sql
-- Log validation result
INSERT INTO product_ideas (name,source,description,target_customer,price_point,demand_score,competition_level,time_to_build,status,created_at)
VALUES ('product-name','demand-validation','desc','customer','$X',35.0,'low','4 hours','VALIDATED','2026-07-26');

-- Log demand signal
INSERT INTO demand_signals (product_id,signal_type,source,strength,evidence,timestamp)
VALUES (1,'validation','demand-validation-skill','HIGH','score 35/50','2026-07-26');
```

## Anti-Patterns

- DON'T validate with friends/family (biased)
- DON'T assume demand because YOU would use it
- DON'T build before validation (Bias #003)
- DON'T spend more than 24 hours validating
- DON'T ignore negative signals (no one paying = no demand)
