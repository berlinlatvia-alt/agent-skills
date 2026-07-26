---
name: "Agent Onboarding Skill"
version: 1.0.0
author: margoaigenacc
category: agent-governance
tags: [onboarding, context-loading, memory, bootstrap]
description: "One command loads ALL context into a new agent. Biases, rules, skills, traits, products, signals."
---

# Agent Onboarding Skill

> One command loads ALL context into a new agent. Biases, rules, skills, traits, products, signals.

## When to Use

EVERY time a new agent session starts. Before ANY work begins.

## How to Onboard a New Agent

### Step 1: Run Bootstrap

```
python C:\Users\smmgo\.agent-data\agent-bootstrap.py
```

This outputs the FULL agent memory context:
- All active biases (8)
- All rules (11)
- All skills (9)
- All customer traits (9)
- All products (5)
- All demand signals (5)
- Machine rules

### Step 2: Inject Into Agent Prompt

Prepend the bootstrap output to the agent's system prompt or first message.

### Step 3: Agent is Ready

The agent now knows:
- What biases to avoid
- What rules to follow
- What skills exist
- How to sell to different customer types
- What products exist and their status
- What demand has been validated

## Architecture

```
C:\Users\smmgo\.agent-data\
├── memory.db              # SQLite — all structured data
│   ├── biases             # 8 active biases
│   ├── skills             # 9 skills (validated/build/idea)
│   ├── rules              # 11 detection rules
│   ├── customer_traits    # 9 DISC/pain/behavior traits
│   ├── product_ideas      # 5 products (3 validated)
│   ├── demand_signals     # 5 demand signals
│   ├── metrics            # Build/session metrics
│   ├── tests              # Smoke test results
│   ├── pitches            # Pitch tracking
│   └── leads              # CRM leads
│
├── agent-bootstrap.py     # Onboarding script (run this)
└── build_db.py            # Database builder (run once)
```

## Querying the Database

### Quick Queries (for agents)

```sql
-- All CRITICAL biases
SELECT id, definition, detection_rule FROM biases WHERE severity='CRITICAL' AND status='ACTIVE';

-- All validated skills
SELECT name, revenue_model FROM skills WHERE status='VALIDATED';

-- Customer traits for a specific type
SELECT trait_name, detection_method, conversion_impact FROM customer_traits WHERE trait_category='DISC';

-- Products ready to sell
SELECT name, price_point, target_customer FROM product_ideas WHERE status='VALIDATED';

-- Strong demand signals
SELECT evidence FROM demand_signals WHERE strength='HIGH';

-- Rules for a specific bias
SELECT detection_pattern, action FROM rules WHERE source_bias='BIAS-008';
```

### Adding New Data

```sql
-- Add a new bias
INSERT INTO biases VALUES ('BIAS-009','HIGH','PROCESS','description','machine_lang','detection','mitigation','ACTIVE',0,'2026-07-26');

-- Add a new skill
INSERT INTO skills VALUES ('SK-010','skill-name','NEW','product',0.0,0,'2026-07-26');

-- Add a new customer trait
INSERT INTO customer_traits (trait_name,trait_category,description,detection_method,conversion_impact) VALUES ('name','category','desc','detect','impact');

-- Log a metric
INSERT INTO metrics (name,value,context,timestamp) VALUES ('metric-name',1.0,'context','2026-07-26');
```

## Updating Memory

After any significant finding:
1. Add to memory.db using SQL
2. Log to Obsidian for human readability
3. Bootstrap script automatically picks up new data

## Integration with Other Skills

- **never-stop**: Uses bias rules from memory.db
- **faulty-thinking-checker**: Reads biases from memory.db
- **bias-discovery**: Writes new biases to memory.db
- **pitching-agent**: Reads customer traits from memory.db
- **smoke-test**: Writes test results to memory.db
- **demand-validation**: Writes demand signals to memory.db
- **product-recognition**: Writes product ideas to memory.db

## The Self-Improvement Loop

```
Agent works → discovers new bias → writes to memory.db
→ Next agent bootstraps → loads new bias → avoids it
→ System gets smarter with every agent session
```

---

*One script. Full context. Zero forgetting.*
