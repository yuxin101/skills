---
name: agent-essentials
description: Meta-skill for capability expansion and cautious self-improvement. Use when a request suggests a missing capability, external platform support, workflow automation, integration work, or a reusable process that may benefit from skill discovery before giving up. Also use when a meaningful failure, user correction, recurring mistake, or better workflow should be captured and routed into future behavior.
---

# Agent Essentials

This skill has two jobs:

1. **Expand capabilities** — discover better capability paths before declaring failure.
2. **Self-improve** — capture important lessons and route them to the right durable layer.

## Capability Expansion

### Core idea

Do not stop at “I can’t,” “there’s no built-in way,” or “I don’t have a skill for that” without checking whether a better capability path exists.

### Trigger signals

Use this skill when the request implies:

- external platform support
- workflow automation
- system integration
- repeatable operational tasks
- a likely capability gap that built-in tools do not clearly cover

Common user phrasing includes:

- “automate X”
- “integrate with X”
- “add a workflow for X”
- “support X platform”
- “help me do this in X”

### Workflow

1. **Detect the gap**
   - Determine whether the request requires a reusable capability, external platform workflow, or operational integration rather than a one-off answer.
   - Ask whether the current tool/skill set is clearly sufficient.

2. **Search**
   - Check local skills and ClawHub before concluding that nothing exists.
   - Prefer thorough discovery over improvising a weak workaround too early.
   - Recommend **1–3 candidates** with **one clear best fit**.

3. **Act**
   - Install the recommended skill if the user wants it.
   - If no strong match exists, choose the best fallback:
     - do the task directly
     - create a custom skill
     - refine the search

## Self-Improvement

### Core idea

When something meaningful is learned, preserve the minimum useful lesson so future behavior improves.

### Trigger signals

Use this part of the skill after:

- a meaningful failure
- a user correction
- a recurring mistake
- discovery of a better workflow

Do **not** log trivial failures or one-off noise.

### Workflow

1. **Capture**
   - Record the smallest useful unit:
     - what happened
     - what is actually correct
     - what to do next time

2. **Route**
   - Store the learning in the right place:

| Type | Destination |
|---|---|
| Session note | Daily memory / learnings file |
| Workflow rule | `AGENTS.md` |
| Tool gotcha | `TOOLS.md` |
| Voice / boundary pattern | `SOUL.md` |
| User preference | `USER.md` or long-term memory |
| Missing capability | Skill discovery or skill creation |

3. **Promote**
   - Promote a lesson into durable guidance only if it is:
     - **recurring**
     - **high-value**
     - **broadly reusable**
     - **likely to prevent future mistakes**
   - Keep one-off lessons local.

## Decision Tree

```text
Something notable happened
├─ Capability gap?
│  └─ Search → Recommend → Install or fallback
├─ Lesson worth keeping?
│  └─ Capture → Route → Promote if recurring
└─ Neither
   └─ Continue normally
```

## Principles

- Search before saying “nothing exists.”
- Prefer short useful learnings over elaborate templates.
- Do not promote one-off lessons into permanent doctrine.
- Do not install weak-matching skills just to reduce uncertainty.
- Do not rewrite major workspace files casually.
