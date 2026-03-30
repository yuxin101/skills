---
name: skill-analyst
description: Analyze OpenClaw skills before installing or publishing. Compare against installed or ClawHub skills, check overlap, run security review, and give a clear go/no-go recommendation. Use when: user wants to evaluate a skill for installation, compare skills on ClawHub, or check if a local skill is ready to publish. Triggers on "analyze skill-name", "evaluate install/publish skill-name", "璇勪及瀹夎/鍙戝竷鏌愭煇鎶€鑳?, "杩欎釜skill鍊煎緱瑁呭悧", "鑳藉彂甯冨悧".
---

# Skill Analyst

鍒嗘瀽鍛樻ā寮忥細鍦ㄤ綘瀹夎鎴栧彂甯?skill 涔嬪墠锛屽府浣犲垎鏋愩€佸姣斻€佹妸鍏炽€?
## Prerequisites

- `clawhub` CLI available (for search and inspect)
- `skill-vetter` optional (for security audit)

## Tools

Two helper scripts in `scripts/`:

```
node <skill-dir>/scripts/analyst-search.mjs <query> [--limit N]
node <skill-dir>/scripts/analyst-inspect.mjs <skill-name> [--files]
```

Both output structured JSON.

## Workflow: Install analyst

Trigger: "analyst install <skill-name>" or "杩欎釜skill鍊煎緱瑁呭悧"

### Step 1: analyst the target

```
node scripts/analyst-search.mjs "<skill-name>"
node scripts/analyst-inspect.mjs "<top-result>"
```

Capture: name, owner, version, summary, license, last updated.

### Step 2: Check installed skills

```
clawhub list
```

Or scan the skills directory for SKILL.md files.

### Step 3: Find overlap

Compare target's summary and description against installed skills:

- Search for skills with similar keywords or functionality
- Rate overlap: HIGH / MEDIUM / LOW / NONE
- Note key differences

### Step 4: Security check (optional)

If `skill-vetter` is installed, run it against the target.

If not available, note that security review was skipped.

### Step 5: Report

Generate a structured report:

```
## 馃攳 Analysis Report: Install <skill-name>

### Overview
| Field | Value |
|-------|-------|
| Name | ... |
| Owner | ... |
| Version | ... |
| License | ... |
| Updated | ... |

### Overlap with Installed Skills
- skill-a: MEDIUM 鈥?similar purpose but different approach
- skill-b: NONE 鈥?unrelated

### What It Adds
- Feature X (not covered by any installed skill)
- Improved Y over existing skill-z

### Risks
- Requires API key for Z
- No updates in 3 months

### Verdict
鉁?GO 鈥?Unique value, safe to install
鈿狅笍 HOLD 鈥?Consider X first
鉂?SKIP 鈥?Redundant with skill-a
```

## Workflow: Publish analyst

Trigger: "analyst publish <skill-name>" or "鑳藉彂甯冨悧"

### Step 1: Read local skill

Read the SKILL.md from workspace or skills directory.

Extract: name, description, functionality, file list.

### Step 2: Search for competitors

```
node scripts/analyst-search.mjs "<skill-name>"
node scripts/analyst-search.mjs "<keywords-from-description>"
```

Use 2-3 query variations to catch overlapping skills.

### Step 3: Inspect competitors

For each relevant hit:

```
node scripts/analyst-inspect.mjs "<competitor>"
```

Compare: features, version maturity, update frequency, uniqueness.

### Step 4: Report

```
## 馃攳 Analysis Report: Publish <skill-name>

### Your Skill
| Field | Value |
|-------|-------|
| Name | ... |
| Files | ... |
| Description | ... |

### Competitors on ClawHub
| Skill | Owner | Version | Overlap | Updated |
|-------|-------|---------|---------|---------|
| ... | ... | ... | HIGH/MED/LOW | ... |

### Your Edge
- What makes yours different or better
- Gaps you fill that competitors don't

### Suggested Improvements
- Add X for better usability
- Consider Y before publishing

### Verdict
鉁?PUBLISH 鈥?Unique contribution, ready
鈿狅笍 ITERATE 鈥?Needs X improvements first
鉂?RETHINK 鈥?Too similar to existing, contribute there instead
```

## Config

Edit `config.json` to customize:

```json
{
  "searchLimit": 8,           // max results per search
  "overlapThresholds": {      // overlap classification
    "high": 0.7,
    "medium": 0.4,
    "low": 0.2
  },
  "securityRequired": false,  // require security audit
  "securitySkill": "skill-vetter"
}
```

## Output Guidelines

- Always use tables for structured comparisons
- Keep analysis concise and actionable
- End with a clear verdict (GO / HOLD / SKIP / PUBLISH / ITERATE / RETHINK)
- Use the report templates above 鈥?don't freestyle

