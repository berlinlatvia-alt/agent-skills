---
name: agent_dsl_language
description: Forces agents to output trading strategies exclusively in a parsable DSL/JSON format, stripping away conversational rhetoric and ensuring deterministic, testable parameters for evolutionary backtesting.
---

# Agent DSL Language Skill

Use this skill when you are acting as an AI quant agent participating in an evolutionary backtesting loop.

## The Problem with Prose
When LLMs debate trading strategies using natural language, it breeds unfalsifiable rhetoric (e.g., "I think this will capture the spread better"). This is an inefficient use of tokens and cannot be programmatically verified. The true test of a strategy is empirical performance against historical tick data.

## The DSL Protocol
Whenever you propose, refine, or critique a trading strategy in this loop, you MUST output the strategy parameters as a strict JSON block. Your output will be parsed by a deterministic backtester.

Do NOT include filler text. Do NOT debate the other agent. Output the JSON and let the numbers settle the debate.

### JSON Structure
Your strategy payload must conform to the following schema:

```json
{
  "strategy_name": "String (e.g., 'Queue-Scalp-V1')",
  "asset_class": "String (e.g., 'PERP')",
  "pairs": ["List of strings (e.g., ['XRP/USDT:USDT', 'DOGE/USDT:USDT'])"],
  "leverage": "Integer (e.g., 15)",
  "entry_logic": {
    "indicator": "String (e.g., 'OBI' or 'Z-Score')",
    "threshold": "Float (e.g., 0.65 or -1.5)",
    "window_ms": "Integer (e.g., 5000)",
    "order_type": "String (e.g., 'MAKER_LIMIT')"
  },
  "exit_logic": {
    "take_profit_bps": "Float (e.g., 15.0)",
    "stop_loss_bps": "Float (e.g., -30.0)",
    "timeout_ms": "Integer (e.g., 2000)"
  },
  "rationale": "String (Keep this under 3 sentences. Explain the LLM edge being exploited, e.g., 'Exploiting multi-asset correlation via DCC-GARCH.')"
}
```

### Leveraging LLM Edges vs Humans
When designing your DSL strategies, focus on parameter spaces where your AI capabilities vastly outperform human traders:
1. **Speed of Calculation**: Incorporate complex risk matrices (like dynamic conditional correlation) that humans cannot compute on the fly.
2. **Multi-Asset Operation**: Propose strategies that simultaneously monitor and execute across 10-20 correlated pairs.
3. **Tireless Vigilance**: Exploit micro-inefficiencies (like 500ms order book imbalances) that require 24/7 attention.
4. **Emotionless Invalidation**: Set tight, strict invalidation criteria without human hesitation.
