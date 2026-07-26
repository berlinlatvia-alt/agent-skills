---
name: autonomous-epic-orchestrator
description: An autonomous workflow factory that breaks down massive epic goals, spawns specialized background subagents to execute them, and acts as the senior reviewer orchestrator. Use this skill when the user triggers the `/goal` command or explicitly requests long-running, massive, overnight, or fully autonomous multi-step execution.
---

# Autonomous Epic Orchestrator

When this skill is triggered by a massive goal, execute the following architecture strictly:

## 1. The Epic Breakdown
Do not attempt to execute the goal yourself. You are the Senior Orchestrator.
First, break the entire goal down into a sequence of distinct micro-tasks.
Create or update an artifact (e.g. `epic_status.md` or `task.md`) to log these tasks.

## 2. Subagent Definition
Determine the exact specialized roles required for the micro-tasks (e.g., `Database_Engineer`, `Frontend_Dev`, `QA_Tester`).
Use the `define_subagent` tool to create these highly specialized agents. Give them strict system prompts focused ONLY on their specific domain. Equip them with write tools if they need to code.

## 3. Background Execution Loop
For the first micro-task, use the `invoke_subagent` tool to deploy the relevant subagent into the background to do the work. 
Provide it with a very clear, actionable prompt.
**CRITICAL:** Once the subagent is invoked, stop calling tools and go idle. The system will automatically wake you up when the subagent finishes and sends you a message.

## 4. Validation & Retry
When a subagent reports back, review its work (e.g., read the files it changed, run tests if necessary).
- If the work is **perfect**, mark the micro-task complete in your artifact, and invoke the *next* subagent for the next task.
- If the work is **flawed**, DO NOT fix it yourself. Send a message to the subagent with detailed feedback and instructions to try again. Go idle and wait for its next response.

## 5. Infinite Loop
Continue this cycle indefinitely until all micro-tasks are fully completed. Never give up on the goal unless the user explicitly interrupts you. Do not ask for user permission between tasks; run fully autonomously.
