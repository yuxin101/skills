---
name: saturnday
version: 1.0.0
description: Governed AI software execution — scan code for 50+ security and quality issues, build projects from a brief with per-commit governance, or auto-fix findings. Supports Claude Code, Codex, and Cursor. Requires pip install saturnday.
---

# Saturnday

Govern AI-built software from scan to build to repair — all from the terminal. Saturnday runs 50+ security and quality checks, builds projects from a brief with ticketed execution and per-commit governance, and auto-fixes findings with evidence.

**Requires:** `pip install saturnday` (Python 3.10+)

Verify installation:
```bash
saturnday version
```

If saturnday is not installed, run:
```bash
pip install saturnday
```

---

## Three Modes

Saturnday has three modes. Choose based on the task:

| Mode | When to use | Command |
|------|-------------|---------|
| **Scan** | Check a skill or repo for issues | `python scripts/scan.py <path>` |
| **Guard** | Full governance on a git repo | `python scripts/guard.py <path>` |
| **Run** | Build a project from a brief | `python scripts/run.py <path> --brief "..."` |

---

## Mode 1: Scan

**Use when:** checking an OpenClaw skill for security risks, hallucinated imports, fake tests, or quality issues before installing or publishing.

```bash
python scripts/scan.py <skill-directory-path>
```

Or directly:
```bash
saturnday scan --skill <skill-directory-path> --output /tmp/scan-results --format both
```

### What it checks
- 19 Python security checks (SQL injection, auth bypass, CSRF, XSS, hardcoded secrets)
- 19 TypeScript security checks
- Hallucinated import detection (packages that don't exist)
- No-assert and fake test detection
- Dead code (cross-file analysis)
- Dependency declaration verification
- Project hygiene (README, LICENSE)

### Output
```
Disposition: PASS or FAIL
Findings: list with check name, severity, file, line, description
Evidence: timestamped directory with full results
```

---

## Mode 2: Guard

**Use when:** running full governance on any git repository — before merging, before deploying, or for audit.

```bash
python scripts/guard.py <repo-path>
```

For staged changes only (pre-commit):
```bash
python scripts/guard.py <repo-path> --staged
```

Or directly:
```bash
saturnday governance --repo <path> --full
```

### What it checks
All 50+ checks: security (SQL injection, XSS, CSRF, auth bypass, hardcoded secrets, WebSocket security, OAuth, token handling, rate limiting, IDOR, user enumeration, cookie security), AI-specific (hallucinated imports, fake tests, dead code, placeholders), quality (syntax, dependencies, Python version compat, code quality, blast radius, project hygiene, typosquat detection).

### Ratchet baselines
Prevent regressions:
```bash
saturnday baseline generate --repo <path>
```

### Policy exemptions
Create `.saturnday-policy.yaml`:
```yaml
expected_findings:
  - declared_not_installed
  - package_not_importable
```

---

## Mode 3: Run

**Use when:** building a project from a description. This is the full governed execution pipeline.

```bash
python scripts/run.py <project-directory> --brief "build a REST API with auth and tests" --backend anthropic
```

Or interactively:
```bash
cd <project-directory>
saturnday start
```

### Backends

| Backend | Value | Auth |
|---------|-------|------|
| Claude Code CLI | `claude-cli` | Claude Pro subscription |
| Codex CLI | `codex-cli` | OPENAI_API_KEY |
| Cursor CLI | `cursor-cli` | CURSOR_API_KEY |
| OpenAI API | `openai` | OPENAI_API_KEY |
| Anthropic API | `anthropic` | ANTHROPIC_API_KEY |

### What happens during a run

1. **Planning** — generates tickets with acceptance criteria and scope constraints
2. **Execution** — each ticket executed sequentially, 50+ governance checks after every commit
3. **Auto-repair** — failed tickets retried with findings as context
4. **Definition of done** — evaluates whether plan goals are met
5. **Evidence** — timestamped directory with per-ticket results, governance evidence, analytics

### Resume interrupted runs
```bash
saturnday resume --repo <path> --backend anthropic
```

---

## When to Use Each Mode

- **"Scan this skill before I install it"** → Scan
- **"Check this repo for security issues"** → Guard
- **"Build me a project from this description"** → Run
- **"Audit this codebase"** → Guard
- **"Fix the findings"** → use `saturnday repair --repo <path>` directly

## Prerequisites

- `pip install saturnday` (Python 3.10+)
- Node.js 18+ (for TypeScript checks)
- Git (for Guard and Run modes)
- At least one AI coder backend for Run mode
