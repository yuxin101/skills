---
name: deepsleep
description: Two-phase daily memory persistence for AI agents. Nightly pack at 23:40 plus morning dispatch at 00:10. Auto-discovers sessions, filters by importance, tracks open questions, and delivers per-group morning briefs.
---

# DeepSleep

Two-phase daily memory persistence for AI agents.

## Phases

### Phase 1: Deep Sleep Pack (23:40)
**Cron**: `deepsleep-pack`
**Instructions**: `pack-instructions.md`

1. Auto-discover active sessions (groups + DMs)
2. Pull conversation history
3. Generate summaries using filtering criteria
4. Store future-dated items to `schedule.md`
5. Write to `memory/YYYY-MM-DD.md` (with Open Questions + Tomorrow)
6. Merge-update `MEMORY.md`

### Phase 2: Morning Dispatch (00:10)
**Cron**: `deepsleep-dispatch`
**Instructions**: `dispatch-instructions.md`

1. Read yesterday's packed summary
2. Send per-group morning briefs
3. Include schedule due-date alerts

## Filtering Criteria

| Type | Action |
|------|--------|
| Decisions | Keep |
| Lessons | Keep |
| Preferences | Keep |
| Relationships | Keep |
| Milestones | Keep |
| Transient | Skip |
| Already captured | Skip |

## Setup

1. Install skill
2. Create two cron jobs (see README.md)
3. Set `tools.sessions.visibility` to `all`
4. Initialize `memory/schedule.md`
