---
name: autoresearch
description: Autonomous LLM pretraining research loop on single GPU using Karpathy's autoresearch framework. Use when the user wants to: (1) start an autonomous LLM training experiment session, (2) run overnight hyperparameter/architecture search on a single-GPU nanochat setup, (3) iterate on train.py modifications to minimize val_bpb with a fixed 5-minute-per-experiment time budget, (4) manage git-tracked experiment branches with results.tsv logging, or (5) set up and operate the autoresearch experiment loop where the agent continuously modifies training code and records results until stopped.
---

# Autoresearch — Autonomous LLM Pretraining Research

Run a fully autonomous LLM training research loop: modify `train.py`, train for 5 minutes, record val_bpb, keep or discard, repeat. Never stop until the human interrupts.

This skill wraps [karpathy/autoresearch](https://github.com/karpathy/autoresearch) — a single-GPU nanochat training setup where an AI agent acts as an autonomous ML researcher.

## Prerequisites

- Single NVIDIA GPU
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- The autoresearch repo cloned and set up

## Quick Start

The skill operates inside a cloned autoresearch repo. The human should have already:

```bash
git clone https://github.com/karpathy/autoresearch.git
cd autoresearch
uv sync
uv run prepare.py
```

Confirm setup by running a single test: `uv run train.py` (should complete in ~5 minutes and print a val_bpb summary).

## Core Files (in-scope for the agent)

These are the only files that matter during an experiment session:

| File | Role | Agent can modify? |
|------|------|-------------------|
| `train.py` | GPT model, optimizer (Muon+AdamW), training loop | **Yes** — this is the only file you edit |
| `prepare.py` | Fixed constants, data prep, tokenizer, dataloader, evaluation | **No** — read-only |
| `results.tsv` | Experiment log (commit, val_bpb, memory_gb, status, description) | **Yes** — append, but never git-commit |
| `run.log` | Last training run output | Read only |

**The goal**: minimize `val_bpb` (validation bits per byte, lower is better, vocab-size-independent).

## The Experiment Loop

The workflow from [program.md](references/program.md):

### Phase 1: Setup

1. Agree on a run tag (e.g., `jun30`). The branch `autoresearch/<tag>` must not exist.
2. Create branch: `git checkout -b autoresearch/<tag>`
3. Read `README.md`, `prepare.py`, `train.py` for full context
4. Verify `~/.cache/autoresearch/` has data shards and tokenizer. If not, tell human to run `uv run prepare.py`.
5. Create `results.tsv` with header: `commit\tval_bpb\tmemory_gb\tstatus\tdescription`
6. First run always establishes the baseline — run `train.py` as-is.

### Phase 2: Autonomous Loop (RUN FOREVER)

```
LOOP:
  1. Look at current git state (branch, commit)
  2. Modify train.py with an experimental idea
  3. git commit the change
  4. Run: uv run train.py > run.log 2>&1
  5. Parse: grep "^val_bpb:\|^peak_vram_mb:" run.log
  6. If no output → crash → tail -n 50 run.log for stack trace
  7. Log to results.tsv (NEVER commit results.tsv)
  8. If val_bpb improved (lower): keep commit → advance branch
  9. If val_bpb equal/worse: git reset back to previous commit
```

### What You CAN Modify in train.py

Everything is fair game:
- **Architecture**: depth, width, attention pattern, activation functions, MLP ratio, value embeddings
- **Optimizer**: learning rates, momentum, weight decay, warmup/warmdown ratios, Muon parameters
- **Training**: batch size, gradient accumulation, sequence length interaction
- **Hyperparameters**: everything in the Hyperparameters section

### Constraints

- **Time budget**: exactly 5 minutes of training (set in `prepare.py` as `TIME_BUDGET = 300`). Do not modify.
- **No new packages**: use only what's in `pyproject.toml`
- **Do not modify `prepare.py`**: it contains the fixed evaluation harness (`evaluate_bpb`)
- **VRAM is a soft constraint**: small increases for meaningful val_bpb gains are acceptable, but don't blow up.
- **Timeout**: if a run exceeds 10 minutes, kill it and treat as crash (discard + revert).

### Simplicity Criterion

All else equal, simpler is better:
- A 0.001 val_bpb improvement from 20 lines of hacky code → probably not worth it
- A 0.001 val_bpb improvement from deleting code → definitely keep
- Equal results with simpler code → keep

### Crashes

If a run crashes (OOM, typo, bug):
- Obvious quick fix → fix and re-run
- Fundamentally broken idea → log `crash` in results.tsv, git reset, move on

### NEVER STOP

Once the experiment loop starts, do NOT pause to ask the human. They might be asleep. You are autonomous. The loop runs until the human explicitly interrupts.

**Expected throughput**: ~12 experiments/hour, ~100 overnight.

## results.tsv Format

Tab-separated (NOT comma-separated). Header + 5 columns:

```
commit	val_bpb	memory_gb	status	description
a1b2c3d	0.997900	44.0	keep	baseline
b2c3d4e	0.993200	44.2	keep	increase LR to 0.04
c3d4e5f	1.005000	44.0	discard	switch to GeLU activation
d4e5f6g	0.000000	0.0	crash	double model width (OOM)
```

- `commit`: short hash (7 chars)
- `val_bpb`: 0.000000 for crashes
- `memory_gb`: peak_vram_mb / 1024, rounded to 0.1; 0.0 for crashes
- `status`: `keep`, `discard`, or `crash`
- `description`: short text of what was tried

## Key Metrics

After each run, the script prints:

```
val_bpb:          0.997900
training_seconds: 300.1
total_seconds:    325.9
peak_vram_mb:     45060.2
mfu_percent:      39.80
total_tokens_M:   499.6
num_steps:        953
num_params_M:     50.3
depth:            8
```

Extract with: `grep "^val_bpb:" run.log`

## Experiment Ideas (when stuck)

If you run out of ideas:

1. **Read the code critically**: examine `train.py` for optimization opportunities in the Muon, AdamW, or architecture
2. **Try radical changes**: double depth, halve width, different attention patterns, activation functions
3. **Combine previous near-misses**: two changes that individually didn't work might work together
4. **Simplify aggressively**: remove components and see if results hold
5. **Re-read references**: the [nanochat](https://github.com/karpathy/nanochat) parent repo, the [Dummy's Guide](https://x.com/hooeem/status/2030720614752039185)

## Reference Files

- [program.md](references/program.md) — the original agent instruction set from the repo (authoritative for experiment loop details)
- [README.md](references/README.md) — full repo context, design choices, small-compute tuning guide, notable forks
