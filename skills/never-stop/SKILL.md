---
name: "Never-Stop Agent Skill"
version: 1.0.0
author: margoaigenacc
category: agent-governance
tags: [autonomous, execution, anti-hallucination, agent-supervisor]
description: "Prevents agents from stopping execution before achieving the goal. Built via trio swarm debate. File system is truth. Plans are not deliverables."
---

# Never-Stop Agent Skill

> Prevents agents from stopping execution before achieving the goal. Built via trio swarm debate. File system is truth. Plans are not deliverables.

## When to Use

Apply this to EVERY agent task. No exceptions. If the agent is not building, it's failing.

## The Three Layers

### LAYER 1: File-System Heartbeat

The ONLY metric: were files modified? Not what the agent says — what the filesystem proves.

```
CHECK_INTERVAL: 120 seconds
CHECK_COMMAND: Get-ChildItem -Recurse -File | Where-Object { $_.LastWriteTime -gt $lastCheck }
ZERO_RESULTS = STALL DETECTED
```

How it works:
- Before agent starts, snapshot workspace file list + timestamps
- Every 120s, compare current files to snapshot
- If ZERO files were created or modified → stall detected
- Inject warning into next agent prompt immediately

### LAYER 2: Supervisor-as-Gatekeeper

The Skeptic is not a passive reviewer. It is an active stall detector.

BEFORE approving ANY agent work, the Skeptic MUST:
1. Run: `Get-ChildItem -Recurse -File | Select-Object Name, LastWriteTime, Length`
2. List every file modified in the last 5 minutes
3. If count is zero and task is not complete → REJECT
4. If agent claimed "done" but files are empty → REJECT
5. The Skeptic is FORBIDDEN from approving plan-only turns

Skeptic verification prompt:
```
Before approving this agent's work:
1. Run file listing for workspace
2. Show modified files from last 5 minutes with paths and line counts
3. If zero files modified and task incomplete → REJECT with: "Agent has not built anything. Force build."
4. If agent claimed completion → verify files exist matching claims
5. If last 2 agent turns had zero file modifications → flag to Manager regardless of claims
```

### LAYER 3: Consecutive-Plan Counter

Simple heuristic. No keyword detection. No NLP. Just file mutation count.

```
IF last_2_turns had zero file modifications AND zero code blocks:
  Turn 3 prefix = "STALLED: You have planned twice without building.
    You MUST write or edit at least one file this turn.
    Analysis and planning are forbidden until a file is modified.
    No exceptions."

IF turn 3 still has zero file modifications:
  ESCALATE to Layer 2 (Supervisor verification)
```

## Escalation Timeline

| Time | Condition | Action |
|------|-----------|--------|
| 0s | Task starts | Normal operation |
| 120s | No files modified | Warning prefix on next agent prompt |
| 240s | Still no files | Skeptic injected with verification demand |
| 360s | Still no files | Manager notified. Task flagged stalled. |
| 480s | Still no files | Agent TERMINATED. Restart queued with explicit file-level instructions. |

## Anti-Hallucination Rules

### RULE 1: Claim-Verification Pairing
When agent says "done", "complete", "finished", "built", "shipped":
```
Auto-inject next prompt:
"List every file you created or modified with exact paths and line counts.
I will verify each one exists. If nothing was built, say so honestly."
```

### RULE 2: Plan-Output Inversion
When agent outputs a plan/TODO list with no code:
```
Auto-inject next prompt:
"That was a plan. Plans are not deliverables.
Convert each item to a file edit NOW.
First item: [specific file to create/edit]"
```

### RULE 3: Model-Selection Deflection
When agent discusses which model/agent to use instead of building:
```
Auto-inject next prompt:
"Model selection is handled by your Manager.
Build the deliverable. Now. This turn."
```

### RULE 4: Todo-List Rejection
Agent output is exclusively numbered/checkbox list without file operations:
```
Auto-inject next prompt:
"This is a task list, not work product.
Execute the first item now by modifying a file.
Show me the file when done."
```

### RULE 5: Progress Fabrication Detection
Agent claims files exist but they don't:
```
LOG as hallucination
TERMINATE agent
RESTART with tighter constraints:
- Explicit file paths to create
- Explicit content to write
- No planning allowed
```

## Supervisor (Skeptic) Checks — Mandatory Before Approval

```
CHECK 1: File Modification Audit
  Run: Get-ChildItem -Recurse -File | Select-Object Name, LastWriteTime, Length
  Filter: last 5 minutes
  If count = 0 → REJECT

CHECK 2: Deliverable Matching
  For the task given, name expected deliverables (files, functions, tests)
  Check if they exist in workspace
  If missing → REJECT

CHECK 3: Output-vs-Claims Consistency
  If agent claimed to implement feature X
  Grep codebase for feature artifacts
  If absent → REJECT

CHECK 4: Consecutive-Stall Awareness
  Review last 3 agent turns
  If 2+ had zero file modifications → flag to Manager
  Regardless of agent's claims

CHECK 5: No-Plan-Approval
  FORBIDDEN from approving turns whose sole output was a plan or analysis
  Exception: task IS to produce a plan (explicitly stated)
```

## Timer Configuration

```
HEARTBEAT_INTERVAL: 120s (simple task) / 180s (complex) / 240s (epic)
STALL_WARNING: 120s
SUPERVISOR_ESCALATION: 240s
FORCE_TERMINATE: 480s
CONSECUTIVE_PLAN_LIMIT: 2 turns (3rd forced to build)
HALLUCINATION_RESPONSE: immediate (next prompt prefix)
```

## Enforcement Matrix

| Condition | Action |
|-----------|--------|
| No file modified in 120s | Warning prefix on next prompt |
| No file modified in 240s | Skeptic verification + "STALLED" flag |
| No file modified in 480s | Agent killed. Manager notified. Restart queued. |
| Agent claims "done" with no files | Immediate rejection. List files or admit failure. |
| 3 consecutive plan-only turns | Turn 3 forced-build directive |
| Skeptic approves with zero file changes | Manager alerted. Approval overridden. Re-review. |
| Agent discusses models/tools instead of building | "That is not your task. Build [deliverable]. Now." |

## Integration with Governance System

```
1. Agent starts task → Never-Stop activates
2. Heartbeat checks run every 120s
3. If stall detected → warning → supervisor → terminate
4. If no stall → agent completes → Skeptic verifies files → Manager approves
5. Never-Stop logs all stalls and hallucinations to bias log
6. Bias log updates detection rules → self-improvement loop
```

## What This Prevents

- Agent plans but does not build (BIAS-008)
- Agent says "done" when nothing exists
- Agent analyzes instead of executing
- Agent discusses tools/models instead of using them
- Supervisor approves plans as if they were work
- Agent stops after creating a todo list
- Agent hallucinates progress

## Machine-Native Rules

```
IF task is assigned → BUILD something this turn
IF plan exists → CONVERT plan to files this turn
IF analysis exists → CONVERT analysis to code this turn
IF agent says "done" → VERIFY files exist
IF no files modified in 120s → WARNING
IF no files modified in 240s → SUPERVISOR CHECK
IF no files modified in 480s → TERMINATE
```

---

*Plans are not deliverables. Analysis is not code. File system is truth. Build or die.*
