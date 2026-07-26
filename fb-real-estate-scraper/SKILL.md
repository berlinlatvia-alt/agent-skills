---
name: fb-real-estate-scraper
description: >-
  Orchestrates autonomous hybrid scraping across Facebook Marketplace and Facebook Groups via CDP, enforces strict freshness filters, applies pet-friendly scoring alpha (Panama Law 31 & Park Proximity), runs VLM image analysis, and generates a unified tabbed dashboard.
---

# Facebook Real Estate Scraper & Pet-Friendly Alpha Engine

## Overview
This skill automates the discovery, scoring, and visual dashboard generation for rental properties across Facebook Marketplace and private/public Facebook Groups. It enforces strict regional housing laws (such as Panama Law 31 Horizontal Property rules) and applies visual LLM (VLM) design evaluations.

## Dependencies
- `browser-session-rules`: Enforces connecting to existing Chrome/Brave CDP sessions on port 9222.
- `agent_dsl_language`: Ensures quantitative strategy output and manifest definitions conform to standard JSON DSL schemas.

## Quick Start
To trigger the hybrid scraper and generate the report:
```bash
# 1. Ensure Brave or Chrome is running with remote debugging
# 2. Run the multi-channel scraper
uv run task_01_scrape.py --include-groups opencode_fb_groups_module/groups_config.json

# 3. Score listings with VLM + Recursive Learning Pet Alpha
uv run task_02_score.py --config opencode_fb_groups_module/groups_config.json

# 4. Generate the tabbed HTML report
uv run task_03_report.py --tabbed
```

## Core Workflow Alpha
1. **CDP Connection & Tab Separation**: Connects to port 9222. Marketplace GraphQL intercepts run on the main feed tab, while Group DOM parsing (`[role="feed"]`) runs in an isolated dedicated tab to prevent UI session collision.
2. **Strict Freshness Boundary**: Screens out listings older than 60 days (1-2 months max) using timestamp string regex (`3 months`, `4 meses`, `2024`, `2023`).
3. **Realistic Price Floor & Negative Constraint Rejection**: Enforces a strict realistic minimum price floor of **$600** (to eliminate room shares and metal window bar slum housing) and immediately excludes properties stating `no pets`, `no mascotas`, or `sin mascotas` *before* invoking VLM vision calls to conserve API tokens.
4. **Pet-Friendly Proximity & Legal Alpha**:
   - +30 points for explicit pet acceptance (`pet friendly`, `aceptan mascotas`).
   - +10 points if verified under building regulations (`ley 31`, `ph permite mascotas`).
   - +10 points for dog walking outdoor landmarks (`parque omar`, `cinta costera`, `san francisco`, `avenida balboa`, beaches/playas, hiking trails/senderos, promenades/malecón).
5. **Unified Dashboard**: Client-side JavaScript filtering and persistent `localStorage` favoriting and disliking (`fav_listings`, `disliked_listings`) across separated channel tabs with a reset control.

## Rate Limiting & Safeguards
- VLM calls to OpenRouter (`google/gemini-2.5-flash-lite`) are capped at top 40 pre-filtered candidates with a 0.5s mandatory delay.
