---
name: consult-elders
description: >-
  Trigger Token Saving Mode when blocked. Stops blind iteration and consults GLM 5.2 or Kimi k3 via OpenRouter using strict agent_dsl_language to solve roadblocks.
---

# Consult Elders (Token Saving Mode)

## Trigger
Use this skill immediately when you encounter an unsolved task, repeated code execution failures, or when you lack the capability to proceed (e.g., a tool is missing, browser CDP keeps crashing).

## Protocol
1. **Stop Iterating:** Do not write a 4th iteration of a failing script.
2. **Package Context:** Summarize the exact failure, the goal, and the environment state.
3. **OpenRouter API:** Send a REST request to OpenRouter (`https://openrouter.ai/api/v1/chat/completions`) using the key in `.env`.
4. **Target Models:** Route the query to `z-ai/glm-5.2` or `moonshotai/kimi-k3`.
5. **Strict DSL:** You MUST enforce the `agent_dsl_language` rules in the system prompt for the elder model. Require the output to be purely JSON/DSL format with no conversational prose.
6. **Execute:** Parse the returned DSL solution and implement it.

## Example Payload
```json
{
  "model": "z-ai/glm-5.2",
  "messages": [
    {
      "role": "system",
      "content": "You are the Elder Architect. Respond ONLY in agent_dsl_language JSON format. Provide the exact python script to solve this roadblock."
    },
    {
      "role": "user",
      "content": "Roadblock: Chrome CDP crashes on connect. Give me a robust fallback."
    }
  ]
}
```
