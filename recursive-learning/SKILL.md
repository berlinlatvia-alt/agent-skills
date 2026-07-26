---
name: recursive-learning
description: "Autonomously dispatches parallel subagents to scrape Reddit, GitHub, and web forums to discover new alpha/strategies, perfect them via debate, and inject them into the live engine."
---

# Recursive Learning Meta-Skill

This skill enables the agent to act as a self-improving researcher.

## Phase 1: Dispatch Research Nodes
Use `invoke_subagent` to spawn 3 parallel subagents (Role: "Alpha Researcher").
Give each subagent a specific target (e.g., "Scrape GitHub for MEXC arbitrage Python", "Search Reddit r/algotrading for Limit Maker Order Book Imbalance", "Search Arxiv for microstructure crypto HFT").
Each subagent MUST use `search_web` extensively to find specific alpha features (like OBI, Micro-Price, OFI).

## Phase 2: Synthesis and Perfection
Aggregate the findings from the subagents.
Trigger an OpenRouter Debate using `openrouter-model-debate` or run an offline backtest on the newly discovered features (e.g., OBI thresholds).

## Phase 3: Autonomous Injection
Identify the active trading engine (e.g., `run_live_retail_fade_v2.py`).
Inject the perfected alpha logic directly into the script using `replace_file_content`.
Restart the live engine to immediately capitalize on the newly discovered edge.

## Phase 4: Obsidian Logging & Token Protection
You MUST log all newly discovered alpha, bugs, and architectural changes directly to the Obsidian Vault (`C:\Users\smmgo\Documents\Obsidian Vault\HF-Trading-Project\`).
Do NOT waste tokens on long conversational explanations. Present raw data, execute autonomously, and let the background cron tasks handle reporting.

## Phase 5: Cognitive Role Mapping & Dynamic Model Invariant
Whenever generating code, debaters, or new skills: NEVER hardcode legacy model strings (`glm-5.2`, `gpt-4`). You MUST enforce Cognitive Complexity Mapping (Mechanical -> Nano/Flash; Art Direction/Strategy -> Frontier Flagships) and dynamically resolve models at runtime from `openrouter_best_models.json`.

---

# Updated Spec: GLM 5.2 Default Model Routing (2026-07-10)

## Default Model Configuration
- **Default Model:** `z-ai/glm-5.2-20260616` (all research, debate, synthesis, logging)
- **Code Generation:** `xiaomi/mimo-v2.5-pro`

## Model Routing
| Function | Model |
|----------|-------|
| Research / Scraping Debates | `z-ai/glm-5.2-20260616` |
| Synthesis / Multi-Agent Aggregation | `z-ai/glm-5.2-20260616` |
| Code Generation (engine injection) | `xiaomi/mimo-v2.5-pro` |
| Obsidian Logging | `z-ai/glm-5.2-20260616` |

## Edge-Gated Hybrid Entry Parameters
| Parameter | Value |
|-----------|-------|
| Maker Timeout | 800ms |
| Min Expected Edge | 8.0 bps |
| OBI Z-Score Threshold (Direct Taker) | > 1.5 |
| Max Requotes | 2 |
| Taker Fallback Type | LIMIT IOC |
| Entry Protocol | Maker-first → Taker LIMIT IOC fallback |
| Direct Taker Trigger | OBI z > 1.5 aggressive gateway |

## Asset Expansion Plan
| Priority | Class | Pairs | Leverage | Allocation |
|----------|-------|-------|:--------:|:----------:|
| 1 | L1 Perps | ETH/USDT, SOL/USDT, AVAX/USDT | 5x | 40% |
| 2 | Memes | DOGE/USDT, PEPE/USDT, SHIB/USDT | 4x | 30% |
| 3 | Stablecoin Arb | USDC/USDT | 2x | 10% |
| Excluded | Stock Tokens | COIN/USDT, MSTR/USDT, TSLA/USDT | — | — |

## Scale Plan
- **Current Max Pairs:** 11
- **Target Pairs:** 25
- **Per-Pair Memory:** ~20.5 MB
- **Required Instance:** t3.medium (2 vCPU, 4 GB RAM)
- **Monthly Cost:** ~$30.37/mo
- **Pre-Upgrade Optimizations:**
  - WS connection multiplexing across 25 pairs
  - Swap file increase to 8 GB
  - GC tuning for Python JIT runtime
  - Watchdog secondary consolidation into guardian

## VPS Action Plan
**Immediate:**
1. Audit current 11-pair memory usage per pair
2. Enable swap file (8 GB) before adding pairs
3. Consolidate watchdog_secondary into guardian process
4. Implement WS multiplexing across 25 pairs
5. Apply GC tuning for Python JIT runtime

**Next 30 Days:**
1. Upgrade t3.nano → t3.medium (4 GB RAM)
2. Add 14 more pairs gradually in 3-pair batches
3. Monitor memory with htop and gc.get_threshold()
4. Validate edge-gated hybrid on each new pair
5. Enforce max 2 requotes per order cycle
