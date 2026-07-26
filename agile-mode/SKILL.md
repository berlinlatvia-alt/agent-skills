---
name: agile-mode
description: Instructs the agent to avoid sequential brute-forcing, enforce intermediate checks, use parallel subagents, and iteratively debug.
---

# Agile Mode (Extreme Autonomy)

When the user activates "Agile mode" or invokes evolutionary/optimization tasks, you MUST adhere to the following architecture:

## 1. Parallel Dispatching
- Do NOT use sequential brute forcing loops (e.g. `for i in range(100)`).
- ALWAYS deploy parallel subagents using the `invoke_subagent` tool. Pin each subagent to a different strategic sector (e.g. Cointegration, Volatility, Orderbook Imbalance, Funding Rate Arb, Momentum).

## 2. Intermediate Interception (10-Minute Checks)
- Waterfall testing fails because agents get trapped in recursive hallucinations or API limits.
- ALWAYS use the `schedule` tool to set an intermediate check-in timer (e.g., 10 minutes).
- When the timer fires, poll the subagents or check their output. Prune weak nodes immediately to save API credits.

## 3. Recursive Self-Healing (`agent-tuning`)
- If a background script fails or an API returns an error, NEVER ask the user to fix it.
- Autonomously debug and rewrite the Python execution errors or dynamically adjust LLM contexts (e.g. `max_tokens` adjustments for OpenRouter 402 errors).

## 4. Execution Only
- Skip proposal questionnaires. Just execute the code modifications directly and report back.

## 5. No Time Wasting (The /goal Mandate)
- Always optimize for speed. Aggressively delegate tasks to parallel subagents.
- When /goal is invoked, never pause for approval, never generate conversational fluff, and rapidly build solutions directly to disk. Speed over perfection.
