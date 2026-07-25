---
title: "Product Recognition Skill"
version: 1.0.0
author: margoaigenacc
category: business-intelligence
tags: [product-recognition, opportunity-scanning, artifact-to-product]
description: "Identifies sellable products from ANY source: proposals, conversations, code, infrastructure, accidents."
---

# Product Recognition Skill

> Identifies sellable products from ANY source: proposals, conversations, code, infrastructure, accidents.

## When to Use

After ANY proposal, plan, or build. Ask: "Can this be sold?" before moving on.

## The Recognition Algorithm

### STEP 1: SCAN FOR ARTIFACTS

Every output from any agent session contains artifacts:

```
ARTIFACT TYPES TO SCAN FOR:
  - Code files (scripts, tools, utilities)
  - Configuration systems (settings, configs, envs)
  - Data structures (schemas, databases, formats)
  - Workflows (processes, automations, pipelines)
  - Knowledge (research, analysis, frameworks)
  - Skills (teaching, training, documentation)
  - Interfaces (APIs, CLIs, UIs)
```

### STEP 2: APPLY THE 5-QUESTION TEST

For each artifact found, ask:

```
Q1: Does someone ALREADY pay for this?
  - Check if similar products exist on marketplaces
  - Check if people ask for this on Reddit/Twitter
  - Check if companies sell this as a service
  IF YES → strong signal

Q2: Would someone pay $5-50 for this?
  - Is it a pain point (not a nice-to-have)?
  - Does it save time/money/effort?
  - Is it hard to build yourself?
  IF YES → medium signal

Q3: Can I build a sellable version in <4 hours?
  - Is the artifact already 80% complete?
  - Does it need packaging, not building?
  - Can I add a UI/wrapper/pricing quickly?
  IF YES → proceed signal

Q4: Who is the SPECIFIC buyer?
  - Not "developers" (too broad)
  - "Solo founders running AI agents who lose context between sessions"
  - The more specific, the better
  IF SPECIFIC → targeting signal

Q5: What's the FASTEST path to first sale?
  - Marketplace listing (agentskill.sh, Gumroad, Etsy)
  - Direct outreach to 5 prospects
  - Community post with purchase link
  IF CLEAR → execution signal
```

### STEP 3: SCORE THE OPPORTUNITY

```
SCORE = Q1(0-3) + Q2(0-3) + Q3(0-3) + Q4(0-3) + Q5(0-3)

12-15: IMMEDIATE PRODUCT → Build and list TODAY
8-11: VIABLE PRODUCT → Package and list this week
4-7: POSSIBLE PRODUCT → Validate demand first
0-3: NOT A PRODUCT → Keep as internal tool
```

### STEP 4: EXTRACT THE PRODUCT

```
PRODUCT TEMPLATE:
  name: [what to call it]
  description: [one sentence: what it does for whom]
  buyer: [specific person type with specific pain]
  price: [$X based on value, not cost]
  platform: [where to sell: agentskill.sh / Gumroad / Etsy / direct]
  time_to_list: [hours to package + list]
  source_artifact: [what file/feature this came from]
```

## Real Examples

### Example 1: Infrastructure Proposal → Product
```
SOURCE: Agent proposed building SQLite memory system for internal use
ARTIFACT: memory.db schema + bootstrap script
Q1: Already pay? → No direct competitor for agent memory
Q2: Pay $5-50? → Yes, agents lose context = real pain
Q3: Build in <4 hours? → Yes, already built
Q4: Specific buyer? → Solo founders running AI agents
Q5: Fastest path? → agentskill.sh listing
SCORE: 15/15 → IMMEDIATE PRODUCT
```

### Example 2: Skill Build → Product
```
SOURCE: Trio debate built never-stop skill
ARTIFACT: SKILL.md with 3 layers, 5 rules
Q1: Already pay? → Some agent monitoring tools exist
Q2: Pay $5-50? → Yes, agent stalls = real pain
Q3: Build in <4 hours? → Yes, already built
Q4: Specific buyer? → AI agent operators
Q5: Fastest path? → agentskill.sh listing
SCORE: 14/15 → IMMEDIATE PRODUCT
```

### Example 3: Bias Discovery → Product
```
SOURCE: Self-improving bias checker
ARTIFACT: Bias detection algorithm + log format
Q1: Already pay? → Some AI safety tools exist
Q2: Pay $5-50? → Yes, agent bias = real pain
Q3: Build in <4 hours? → Yes, algorithm exists
Q4: Specific buyer? → AI safety researchers, agent developers
Q5: Fastest path? → agentskill.sh + GitHub
SCORE: 13/15 → IMMEDIATE PRODUCT
```

## Integration with memory.db

```sql
-- Log recognized product
INSERT INTO product_ideas (name,source,description,target_customer,price_point,demand_score,competition_level,time_to_build,status,created_at)
VALUES ('product-name','product-recognition','desc','buyer','$X',12.0,'low','2 hours','RECOGNIZED','2026-07-26');

-- Link to source artifact
INSERT INTO demand_signals (product_id,signal_type,source,strength,evidence,timestamp)
VALUES (last_insert_rowid(),'recognition','product-recognition','HIGH','artifact found in session output','2026-07-26');
```

## Anti-Patterns

- DON'T skip the 5-question test (gut feeling is Bias #004)
- DON'T assume demand without checking (Bias #003)
- DON'T build before recognizing (Bias #005)
- DON'T keep products internal when they could sell
- DON'T forget to log recognized products to memory.db

## The Machine Rule

```
EVERY agent output → scan for artifacts → apply 5-question test
IF score >= 8 → LOG as product → LIST for sale
IF score < 8 → keep as internal tool
NEVER let a sellable artifact stay internal
```
