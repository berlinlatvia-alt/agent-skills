---
name: obsidian_work_logger
description: Automatically saves session summaries, walkthroughs, and critical context to the Obsidian Vault to preserve project continuity.
---

# Obsidian Work Logger

Use this skill at the end of a session, after completing an epic, or when generating a `walkthrough.md` artifact.

## Protocol
Instead of just writing summaries or walkthroughs to the ephemeral artifact directory, you MUST also mirror or log a comprehensive summary into the user's Obsidian Vault. This ensures the user retains permanent context across all agent sessions.

**Obsidian Vault Path**: `C:\Users\smmgo\Documents\Obsidian Vault\HF-Trading-Project\`

### Guidelines:
1. **Naming Convention**: Name the file descriptively with a date, e.g., `Session-Summary-YYYY-MM-DD.md` or `Walkthrough-FeatureX-YYYY-MM-DD.md`.
2. **Content**: Include the goal of the session, files changed, architectural decisions made, test results, and any pending issues.
3. **Tags**: Include YAML frontmatter with relevant tags (e.g., `tags: [summary, walkthrough, progress]`).
4. **Trigger**: Whenever you would normally output a `walkthrough.md` or present a final report to the user, proactively write a copy to the Obsidian path.
