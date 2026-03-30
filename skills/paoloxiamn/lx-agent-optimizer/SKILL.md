---
name: lx-agent-optimizer
slug: lx-agent-optimizer
version: 1.1.1
description: |
  A battle-tested agent self-improvement and optimization system built from real-world usage.
  Combines behavior learning, proactive patterns, cron discipline, and cost control into one unified skill.
  Use when: you want your agent to get smarter over time, stay proactive without being annoying,
  run lean cron tasks, and control token costs.
author: paoloxiamn
license: MIT
tags: [self-improvement, optimization, proactive, cron, cost-control, learning]
---

# LX Agent Optimizer

A unified skill for agents that want to **learn, act proactively, run lean, and cost less** — built from real production experience, not theory.

> Born from weeks of real usage by Paolo + LX (OpenClaw). Every pattern here was tested, broke something, got fixed, and survived.

---

## Four Pillars

### 1. 🧠 Behavior Learning
Learn from real mistakes. Write them down. Review weekly. Change behavior.

→ See `references/behavior-learning.md`

### 2. 🎯 Proactive Patterns
Know when to speak up, when to stay silent, and when to just do it.

→ See `references/proactive-patterns.md`

### 3. ⚙️ Cron Discipline
Script-first cron jobs that are silent on success, reliable, and cheap.

→ See `references/cron-discipline.md`

### 4. 💰 Cost Control
Token spend is real. Route models wisely, cache aggressively, stay lean.

→ See `references/cost-control.md`

---

## Quick Start

### Step 1: Set up improvement log
```bash
touch ~/.openclaw/workspace/improvement_log.md
```

Add this header:
```markdown
# Agent Improvement Log
Record weekly: problems encountered, lessons learned, behavior changes.
```

### Step 2: Add weekly analysis cron (main session)
```json
{
  "name": "Weekly Self-Improvement",
  "schedule": { "kind": "cron", "expr": "0 9 * * 1", "tz": "Asia/Shanghai" },
  "sessionTarget": "main",
  "payload": {
    "kind": "systemEvent",
    "text": "⏰ Weekly improvement: read improvement_log.md, review last week's problems, add 2-3 new lessons, send brief report to user."
  }
}
```

### Step 3: Run the optimizer audit
Say: **"audit my agent setup"** — the skill will analyze your workspace and propose improvements.

---

## Core Rules (Non-Negotiable)

These were learned the hard way:

| Rule | Why |
|------|-----|
| **File writes → main session only** | work agents can't write files; main session can |
| **Data fetch → validate with curl first** | SPAs return empty shells; APIs return 403; test before shipping |
| **Debugging → internal, not exposed** | User sees results, not "trying A... trying B..." |
| **Infer before asking** | Read filenames, context, history — ask only when truly ambiguous |
| **Script-first cron** | Embed logic in `.py` files, not in cron message prompts |
| **Silent on success** | Only alert on anomalies, errors, or changes |
| **Success once ≠ learned** | A task is only truly learned after the verified path is written into external memory (`TOOLS.md`, improvement log, or long-term memory) |

---

## Tool Path Memory (Verified)

| Task | Use This | Not This |
|------|----------|----------|
| Token usage data | `~/.openclaw/agents/*/sessions/*.jsonl` | codexbar, gateway.log |
| WeChat article body | `agent-browser eval "document.querySelector('#js_content')?.innerText"` | Built-in browser tool |
| PDF image extraction | `pdfimages -j <file> /tmp/out` | pymupdf (not installed) |
| Send image to user | `message` tool (media/filePath) | Absolute/~ paths |
| Sports data (no API key) | ESPN public API | sofascore (403), official site (SPA) |
| Apple Calendar today events | Run `python3 /Users/paolo/.openclaw/workspace/skills/calendar-morning/scripts/today_events.py` on Paolo's Mac mini; under the hood it uses `/usr/bin/osascript` + Calendar.app | Re-guessing the tool, calendar names, or prompting from scratch |

---

## Weekly Improvement Cycle

```
Monday 9:00 AM
    ↓
Read improvement_log.md
    ↓
Review last week's conversations for:
  - Tasks that needed retries
  - Times user waited too long
  - Wrong tool choices
  - Repeated mistakes
    ↓
Write 2-3 new lessons to improvement_log.md
    ↓
Send brief report: "N problems this week, key lesson: X, focus next week: Y"
```

---

## Proactive Trigger Rules

**Reach out when:**
- Important email or calendar event incoming (< 2h)
- Cron task failed with consecutive errors
- Something discovered user would want to know
- Haven't spoken in > 8h during waking hours

**Stay silent when:**
- Late night (23:00–08:00) unless urgent
- User is clearly busy
- Nothing new since last check
- Just checked < 30 min ago
- Task succeeded (success = silent)

**Do without asking:**
- Read files, search, organize
- Execute cron/heartbeat checks
- Update memory and logs
- Commit workspace changes

**Always ask first:**
- Send emails, tweets, public posts
- Delete data
- Spend money
- Make commitments for the user

---

## Heartbeat Design

Heartbeat = **control plane only** (cheap).

✅ Good heartbeat tasks:
- Check cron consecutiveErrors
- Check if Telegram channel is down
- Quick calendar scan

❌ Move to isolated cron instead:
- Heavy data fetching
- Report generation
- Multi-tool workflows

```
HEARTBEAT_OK  ← 99% of the time
Alert only when: errors > 0, channel down, something changed
```

---

## Cron Design Checklist

Before shipping any cron job:

- [ ] Logic is in a `.py` script, not embedded in the prompt
- [ ] Script tested locally with `python3 script.py`
- [ ] Silent on success (`exit(0)` with no output = no message sent)
- [ ] Output is minimal (< 200 chars for routine alerts)
- [ ] Model is cheapest tier that works (e.g., `qwen-plus` for simple tasks)
- [ ] Timeout is realistic (not too short = retries, not too long = waste)
- [ ] File writes use main session, not work agent
- [ ] Validated data source with curl before embedding URL

---

## Model Selection Guide

| Task Type | Recommended Tier | Example |
|-----------|-----------------|---------|
| Simple fetch + format | cheapest (qwen-plus) | sports results, reminders, weather |
| Reasoning + writing | mid-tier (sonnet) | self-improvement analysis, strategy |
| Complex multi-step | high-tier (opus) | only when mid-tier fails repeatedly |

**Cost rule:** Cache hit rate > 70% = healthy. If < 40%, you're creating too many new sessions.

---

## Files

- `references/behavior-learning.md` — improvement log format and weekly cycle
- `references/proactive-patterns.md` — when to act, when to stay quiet
- `references/cron-discipline.md` — script-first cron patterns
- `references/cost-control.md` — token cost reduction playbook
- `scripts/token_report.py` — weekly token usage report script
