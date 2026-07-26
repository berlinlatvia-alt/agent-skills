---
name: launch-opencode-agent
description: >-
  Launches a new autonomous Opencode agent for any task. Triggered by "launch new agent", "new agent for [task]", or "run this with Opencode". Reads all available skills first, then architects a task.json in the Opencode step format (write_file + run steps), outputs the JSON for the user to paste into Opencode. Agent executes everything autonomously — human touches no code.
---

# Launch Opencode Agent

## Dependencies

- **project-autonomy-check** — fires first, asks once if agent should run in autopilot (`--trust`) mode
- **browser-session-rules** — if task involves a browser: always CDP connect to existing Brave/Chrome on port 9222, never launch new

## Overview

When the user says **"launch new agent"** or **"new agent for [task]"**, this skill:

1. Reads all available skills (so we don't reinvent wheels)
2. Designs a `task.json` — a machine-readable instruction set for Opencode
3. Outputs the JSON ready to paste into Opencode
4. Opencode executes all steps autonomously: writes files, runs commands, fixes errors

## task.json Schema

Every task.json MUST follow this exact schema. Opencode reads and executes it step by step.

```json
{
  "task": "snake_case_task_name",
  "goal": "One sentence: what the agent must produce.",
  "autonomous": true,
  "steps": [
    {
      "id": "unique_step_id",
      "run": "shell command to execute"
    },
    {
      "id": "write_a_script",
      "write_file": "filename.py",
      "content": "full file content as a single escaped string"
    }
  ],
  "on_error": {
    "error_scenario": "What agent should try if this happens"
  }
}
```

### Step types

| Field | Meaning |
|---|---|
| `run` | Execute shell command (uv, python, curl, etc.) |
| `write_file` + `content` | Create file with given content |
| `read_file` | Read file for context before next step |

### Rules for task.json generation

- `write_file` steps MUST come before their corresponding `run` steps
- All Python runs via `uv run filename.py` — never `python`
- Deps installed via `uv add package1 package2`
- Content strings: single-line, escape newlines as `\n`, escape quotes as `\"`
- `on_error`: cover the 2-3 most likely failure modes with recovery instructions
- Last step: open or print the output file path

## Workflow

### 1. Read Available Skills

Before designing anything, list all skills and check which ones apply:

```
GET http://localhost:25110/skill
```

Or simply recall from the skills list in context. Reference any matching skill rather than reimplementing its logic.

### 2. Understand the Task

Extract from the user's request:
- **Goal**: what is the final deliverable?
- **Inputs**: what does the agent need access to? (files, browser, APIs, DB)
- **Outputs**: file? HTML? JSON? database row?
- **Dependencies**: packages, browser CDP, credentials?

### 3. Design Steps

Order: deps install → write scripts → run scripts → output

Common step patterns:

```json
{"id":"deps","run":"uv add playwright geopy httpx && uv run playwright install chromium"}
{"id":"write_scraper","write_file":"scraper.py","content":"..."}
{"id":"run_scraper","run":"uv run scraper.py"}
{"id":"open_result","run":"start output\\result.html"}
```

### 4. Output

Write `task.json` to the current workspace directory.

Then tell the user:

> Paste this into Opencode:
> `Execute task.json — run every step in order. Fix errors using on_error hints. Do not stop until [final output] exists.`

## Paste Prompt Template

```
Execute task.json — run every step in order: write each file, run each command, 
fix errors using on_error hints. Do not stop until [DELIVERABLE] exists.
```

Replace `[DELIVERABLE]` with the specific output file or success condition.

## Opencode API Reference

Running at `http://localhost:25110` (or user-specified port).

- `GET /global/health` — confirm running
- `GET /skill` — list available skills
- `GET /agent` — list available agents  
- `POST /session` → `{id}` — create session
- `POST /session/{id}/message` → stream — send task
- `GET /event` — subscribe to events (SSE)

## Common Mistakes

- **Forgetting CDP prereq**: If task uses Playwright, remind user: close Brave, relaunch with `--remote-debugging-port=9222`
- **Inline content too long**: Split large scripts into multiple `write_file` steps if content exceeds ~8KB
- **No on_error block**: Always include at least 2 error recovery hints — agent will hit something unexpected
- **Wrong uv syntax**: Use `uv add` not `uv pip install`; use `uv run file.py` not `python file.py`
