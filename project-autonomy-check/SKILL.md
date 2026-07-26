---
name: project-autonomy-check
description: >-
  Auto-triggers at the start of any new project or agent session to ask the user whether the agent should run in autonomous (auto-approve) mode. If yes, sets trust flags for Opencode and records the decision in the project config. Prevents agents from pausing mid-task for shell command approvals when the user wants autopilot.
---

# Project Autonomy Check

## Overview

At the start of every new project session or when launching a new agent task, this skill fires **one question**:

> "Should this agent run autonomously (auto-approve all actions) or ask for approval on each step?"

Records the answer and applies the correct flags. Never asks again for the same project.

## When to Trigger

Trigger this skill when:
- User says "launch new agent", "start a new project", "new task for Opencode"
- A `task.json` is about to be created
- User has NOT already set autonomy for this workspace (check for `.autonomy` file)

## Workflow

### Step 1 — Check if already decided

Look for `c:\Users\smmgo\Documents\Agents\<project>\.autonomy` file.
- If exists and contains `autonomous=true` → skip asking, apply flags silently
- If exists and contains `autonomous=false` → skip asking, use manual mode
- If missing → proceed to Step 2

### Step 2 — Ask the user (ONE question only)

```
🤖 Autonomy check for this project:
Should the agent auto-approve all actions (shell commands, file writes) without asking?
  [Y] Yes — full autopilot, don't interrupt me
  [N] No — ask me before each shell command
```

### Step 3 — Apply the decision

**If autonomous (Y):**

For Opencode running at `localhost:PORT`:
```powershell
# Kill current instance, relaunch with --trust
Stop-Process -Name opencode -Force
Start-Process opencode -ArgumentList "--port 25110 --trust" -WorkingDirectory (Get-Location)
```

Write decision file:
```
autonomous=true
set_at=2026-06-29
```

**If manual (N):**
```
autonomous=false
set_at=2026-06-29
```

No relaunch needed — Opencode default is manual approval.

### Step 4 — Confirm and continue

Report to user:
- ✅ Autonomous: "Opencode running in full autopilot mode (`--trust`). Won't ask again for this project."
- ✅ Manual: "Opencode will ask approval before each shell command."

Then continue with the original task.

## Decision File Location

`.autonomy` in project root. Format:
```
autonomous=true|false
set_at=YYYY-MM-DD
```

To reset: delete `.autonomy` file.

## Common Mistakes

- **Never** apply `--trust` globally across all projects — only for the current workspace
- **Don't ask twice** — check for `.autonomy` file before asking
- If Opencode is not running, just write the `.autonomy` file; the launch-opencode-agent skill will read it when starting
