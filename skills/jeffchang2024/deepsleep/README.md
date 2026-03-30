# 🌙 DeepSleep

**Two-phase daily memory persistence for AI agents.**

> Like humans need sleep for memory consolidation, AI agents need DeepSleep to persist context across sessions.

![DeepSleep Overview](overview.png)

## What is DeepSleep?

AI agents wake up fresh every session — they forget everything. DeepSleep solves this with a two-phase nightly process:

1. **🛌 Phase 1: Deep Sleep Pack (23:40)** — Collects all conversations from the day, generates summaries, extracts action items, and stores everything to disk.
2. **☀️ Phase 2: Morning Dispatch (00:10)** — Reads yesterday's packed summary and delivers personalized morning briefs to each chat group.

## Features

- **Auto-discovery** — Automatically finds all active sessions (groups, DMs, new groups) — no manual list maintenance
- **Smart filtering** — Keeps decisions, lessons, preferences, relationships, milestones; skips noise
- **Schedule memory** — Future-dated reminders stored in `schedule.md` with automatic due-date alerts
- **Open Questions** — Tracks unresolved questions across days for continuity
- **Tomorrow section** — Clear, actionable next-steps for each morning
- **Merge, not append** — Long-term memory stays lean by updating in place
- **Per-group dispatch** — Each group gets only its own relevant summary

## Architecture

```
                    23:40                           00:10
                  ┌────────┐                     ┌────────┐
  Active Groups ──▸│  Pack  │──▸ memory/日期.md ──▸│Dispatch│──▸ Group A: 📋
  DMs ────────────▸│ Phase  │──▸ MEMORY.md       │ Phase  │──▸ Group B: 📋
  New Groups ─────▸│   1    │──▸ schedule.md     │   2    │──▸ Group C: 📋
                  └────────┘                     └────────┘
```

## File Structure

```
workspace/
├── MEMORY.md                      # Long-term curated memory (merge-updated)
├── memory/
│   ├── YYYY-MM-DD.md             # Daily records (morning report + summary + todos)
│   └── schedule.md               # Future-dated reminders with triggers
└── skills/deepsleep/
    ├── SKILL.md                  # Skill definition
    ├── pack-instructions.md      # Phase 1 detailed instructions
    └── dispatch-instructions.md  # Phase 2 detailed instructions
```

## Daily Summary Template

```markdown
## Daily Summary (DeepSleep)

### [Group Name]
- Concise summary of key discussions and decisions

### Direct Messages
- (DM content if any)

### 🔮 Open Questions
- Unresolved questions, tracked across days

### 📋 Tomorrow
- Actionable next steps

### Todo
- [ ] Immediate action items
```

## Filtering Criteria

Inspired by [memory-reflect](https://clawhub.ai) best practices:

| Type | Action | Example |
|------|--------|---------|
| Decisions | ✅ Keep | "Chose platform A over B" |
| Lessons | ✅ Keep | "Config X blocks cross-session reads" |
| Preferences | ✅ Keep | "User prefers midnight dispatch" |
| Relationships | ✅ Keep | "Bot Y responds slowly" |
| Milestones | ✅ Keep | "Feature Z completed" |
| Transient | ❌ Skip | Heartbeats, weather checks, routine ops |
| Already captured | ❌ Skip | Already in MEMORY.md |

## Setup

### 1. Install the skill

```bash
# From ClawHub
clawhub install deepsleep

# Or clone from GitHub
git clone https://github.com/JeffChang2024/deepsleep.git skills/deepsleep
```

### 2. Create the cron jobs

```bash
# Phase 1: Pack at 23:40 local time
openclaw cron add \
  --name "deepsleep-pack" \
  --cron "40 23 * * *" \
  --tz "Your/Timezone" \
  --system-event "Execute DeepSleep Phase 1. Read skills/deepsleep/pack-instructions.md and follow the process." \
  --timeout-seconds 180

# Phase 2: Dispatch at 00:10 local time
openclaw cron add \
  --name "deepsleep-dispatch" \
  --cron "10 0 * * *" \
  --tz "Your/Timezone" \
  --system-event "Execute DeepSleep Phase 2. Read skills/deepsleep/dispatch-instructions.md and follow the process." \
  --timeout-seconds 120
```

### 3. Enable cross-session visibility

```bash
openclaw config set tools.sessions.visibility all
openclaw gateway restart
```

### 4. Initialize schedule file

Create `memory/schedule.md`:

```markdown
# Schedule — Future Reminders

| Date | Source | Item | Status |
|------|--------|------|--------|
```

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) (any recent version)
- `tools.sessions.visibility` set to `all` (for cross-session history access)
- Cron jobs must use `systemEvent` mode (runs in main session for full permissions)

## Customization

- **Timing**: Adjust cron schedules to match your timezone and sleep habits
- **Filtering**: Edit `pack-instructions.md` to tune what gets kept vs skipped
- **Dispatch targets**: Phase 2 auto-discovers groups from the packed summary — no hardcoded list needed
- **Long-term memory**: Adjust merge strategy in `pack-instructions.md` step 5

## Inspirations & Credits

Built with insights from the OpenClaw community:

| Project | What we borrowed |
|---------|-----------------|
| [agent-sleep](https://clawhub.ai) | Multi-level sleep concept, forgetting curve ideas |
| [memory-reflect](https://clawhub.ai) | Filtering criteria, merge-not-append strategy |
| [jarvis-memory-architecture](https://clawhub.ai) | Cron inbox pattern, sub-agent context templates |
| [memory-curator](https://clawhub.ai) | Open Questions + Tomorrow sections, index-first architecture |

## Roadmap

- [ ] **Forgetting curve** — Auto-decay low-frequency memories, strengthen high-frequency ones
- [ ] **Index layer** — Master index file when daily files grow numerous
- [ ] **Diary layer** — Separate factual summaries from personal reflections
- [ ] **Cron inbox** — Sub-agents report back via shared inbox file

## License

MIT License — use it, fork it, make it better.

---

*Made with 🌙 by JeffreyBOT*
