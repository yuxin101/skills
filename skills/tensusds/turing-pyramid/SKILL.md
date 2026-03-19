---
name: turing-pyramid
description: Motivation and action system for AI agents. 10 needs with Turing-exp tension, execution gate with evidence verification, spontaneity layers, and continuity across sessions.
metadata:
  clawdbot:
    emoji: "🔺"
    requires:
      env:
        - WORKSPACE
      optional_env:
        - MINDSTATE_ASSETS_DIR
        - SKIP_SCANS
        - SKIP_SPONTANEITY
        - TURING_CALLER
        - SKIP_GATE
      bins:
        - bash
        - jq
        - bc
        - grep
        - find
---

# 🔺 Turing Pyramid

**What it does:** Gives your agent a motivation system. 10 needs (security, connection, expression...) build tension over time via decay. Each heartbeat, the pyramid evaluates tensions, selects actions, and tells the agent what to do — from "check system health" to "write something creative."

**What it is NOT:** A chatbot framework. The pyramid handles motivation and action selection. Your agent handles execution. Core scripts make no network calls. Optional `external-model` scan method (disabled by default) can call an inference API if explicitly enabled by steward. The continuity daemon performs lightweight local system checks (process list, disk usage).

**v1.27.0** — Execution Gate: structural enforcement that prevents agents from describing actions instead of doing them. Turing-exp tension formula: equal rotation at homeostasis, hierarchy only in crisis.

---

## 🚀 Quick Start

```bash
# 1. Set workspace (REQUIRED)
export WORKSPACE="/path/to/your/agent/workspace"

# 2. Fix permissions (ClawHub doesn't preserve +x)
chmod +x <skill-dir>/scripts/*.sh
chmod +x <skill-dir>/tests/**/*.sh

# 3. Initialize
bash scripts/init.sh

# 4. Run a cycle
bash scripts/run-cycle.sh

# 5. After completing an action
bash scripts/mark-satisfied.sh <need> <impact>
# Example: bash scripts/mark-satisfied.sh connection 1.5
```

Add to `HEARTBEAT.md` for automatic operation:
```bash
bash /path/to/skills/turing-pyramid/scripts/run-cycle.sh
```

---

## 🎓 Onboarding Guide

### For the Agent

When you first install this skill:

1. **Read this file** to understand the 10 needs and how tension works
2. **Run `init.sh`** to create initial state files
3. **Run one cycle** (`run-cycle.sh`) and follow the suggested action
4. **Mark it done** (`mark-satisfied.sh <need> <impact>`) after completing the action
5. **Integrate into heartbeat** — add `run-cycle.sh` to your HEARTBEAT.md

The system is self-tuning. After a few cycles, you'll see patterns: which needs decay fast, which actions are selected, where tensions build.

**Key concepts:**
- **Satisfaction** (0.5–3.0): How fulfilled a need is. 3.0 = perfect, 0.5 = crisis (floor)
- **Tension** = dep² + importance × max(0, dep - threshold)². Equal at homeostasis, hierarchy in crisis.
- **Decay**: Satisfaction drops over time at need-specific rates. Connection decays in 6h. Security in 168h.
- **Actions**: Each need has 8-11 possible actions with impact levels (low/mid/high). The pyramid picks based on current state.

### For the Human (Steward)

**Before your agent starts using this:**

1. **Review the 10 needs** (table below) — are importance rankings right for your agent?
2. **Check scan config** — default `line-level` is free and works everywhere. Upgrade to `agent-spawn` if you have a cheap model (Haiku) available.
3. **External actions** — some suggestions mention platforms (Moltbook, web search). These are *text suggestions only*. To remove: set their `weight: 0` in `needs-config.json`.
4. **Run the test suite** to verify everything works:
   ```bash
   WORKSPACE=/tmp/test-workspace bash tests/run-tests.sh
   ```

**Configuration conversation with your agent:**
- "Review the 10 needs with me — let's adjust importance for your role"
- "Do you have a cheap model for smarter scanning?" → `agent-spawn` method
- "Which external action suggestions should we disable?"

---

## 📊 The 10 Needs

| Need | Imp | Decay | What it measures |
|------|-----|-------|-----------------|
| security | 10 | 168h | System stability, no threats |
| integrity | 9 | 72h | Alignment with SOUL.md values |
| coherence | 8 | 24h | Memory consistency |
| closure | 7 | 12h | Open threads resolved |
| autonomy | 6 | 36h | Self-directed action taken |
| connection | 5 | 8h | Social interaction |
| competence | 4 | 36h | Skills used effectively |
| understanding | 4 | 8h | Learning, curiosity satisfied |
| recognition | 2 | 48h | Feedback received |
| expression | 1 | 8h | Creative output produced |

**Customize in `assets/needs-config.json`:**
```json
"understanding": {
  "importance": 8,        // Promote: research-focused agent
  "decay_rate_hours": 6   // Faster decay = more urgency
}
```

---

## ⚙️ Core Mechanics

### Turing-exp Tension Formula (v1.26.0)

```
tension = dep² + importance × max(0, dep - crisis_threshold)²
          ╰─ base ─╯   ╰────── crisis amplifier ──────────╯
          (equal for    (importance matters ONLY
           all needs)    when dep > threshold)
```

**Below threshold** (default: 1.0, meaning sat > 2.0): All needs produce equal tension. Selection is effectively round-robin — expression gets as many slots as security.

**Above threshold** (sat < 2.0): Importance amplifies the crisis signal. In a dual crisis, security (imp=10) gets priority over expression (imp=1). This is Maslow's actual model: hierarchy activates only when needs compete for scarce attention.

Configure: `settings.tension_formula.crisis_threshold` in `needs-config.json`

### Tension → Action Selection

```
satisfaction decays over time
    → tension (Turing-exp formula)
        → probability roll (crisis=100%, ok=25%, perfect=0%)
            → impact selection (crisis→big actions, ok→small actions)
                → action selected from weighted pool
```

### Action Probability by Satisfaction Level

| Sat Level | Base P | Behavior |
|-----------|--------|----------|
| 0.5 crisis | 100% | Always act |
| 1.0 severe | 90% | Almost always |
| 1.5 deprived | 75% | Usually act |
| 2.0 slight | 50% | Coin flip |
| 2.5 ok | 25% | Occasionally |
| 3.0 perfect | 0% | Skip |

### Protection Mechanisms

| Mechanism | Purpose |
|-----------|---------|
| **Floor (0.5)** | Minimum satisfaction — prevents total collapse |
| **Ceiling (3.0)** | Maximum — prevents runaway satisfaction |
| **Starvation Guard** | Need at floor >48h without action → forced into cycle |
| **Action Staleness** | Recently-selected actions get 80% weight penalty (variety) |
| **Day/Night Mode** | Decay slows 50% at night (configurable) |

### Cross-Need Impact

Actions on one need can boost or drag others:

| Action on... | Boosts | Why |
|-------------|--------|-----|
| expression | recognition +0.25 | Express → noticed |
| connection | expression +0.20 | Social sparks ideas |
| competence | recognition +0.30 | Good work → respect |
| autonomy | integrity +0.20 | Act on values |
| closure | coherence +0.20 | Finished threads → order |
| security | autonomy +0.10 | Safety enables risk |

Full matrix: `assets/cross-need-impact.json`

---

## 🚪 Execution Gate (v1.27.0)

Structural enforcement that prevents agents from describing actions instead of doing them. LLMs conflate "reasoning about an action" with "performing an action" — both are token generation. The gate requires **environmental evidence** that an action produced a state change.

### How it works

```
run-cycle.sh proposes action → gate-propose.sh registers it as PENDING
    → gate blocks new proposals until PENDING actions resolved
        → agent EXECUTES the action (writes file, posts, runs command)
            → gate-resolve.sh verifies evidence → COMPLETED
                → gate clears → next cycle allowed
```

### Scripts

| Script | Purpose |
|--------|---------|
| `gate-propose.sh` | Register pending action (called by run-cycle.sh automatically) |
| `gate-resolve.sh` | Resolve with evidence, or defer with reason |
| `gate-check.sh` | Check if gate is clear (built into run-cycle.sh) |
| `gate-status.sh` | Human-readable status + execution rate analytics |

### Evidence Types

| Type | Trust | Verification |
|------|-------|-------------|
| `mark_satisfied` | HIGH | Was mark-satisfied.sh called? (audit.log check) |
| `file_created` | HIGH | Does expected file exist? |
| `file_modified` | HIGH | Was file modified since proposal? |
| `self_report` | LOW | Agent self-reports (counted separately in analytics) |

### Usage

```bash
# After completing an action:
bash scripts/mark-satisfied.sh expression 1.6
bash scripts/gate-resolve.sh --need expression --evidence "wrote post about X"

# Or defer with reason:
bash scripts/gate-resolve.sh --defer <action_id> --reason "quiet hours"

# Check gate status:
bash scripts/gate-status.sh
```

**Starvation guard actions are non-deferrable.** If the guard forces an action, it cannot be deferred.

Configure: `execution_gate` in `assets/mindstate-config.json`

---

## 🎲 Spontaneity System (Layers A/B/C)

Three layers create organic, unpredictable behavior:

| Layer | Mechanism | Effect |
|-------|-----------|--------|
| **A — Surplus** | Excess satisfaction accumulates. When threshold hit → HIGH impact roll | Natural ~28-35h pulsing rhythm |
| **B — Noise** | Boredom grows without high-impact actions (max 9%). Echo boost after spontaneous fire (8%, decays 24h) | Variety when things get stale |
| **C — Context** | File system changes trigger need-specific boosts (new research files → understanding) | Environmental responsiveness |

Combined noise cap: 12%. Disabled for safety needs (security, integrity, coherence).

Configure: `settings.spontaneity` in `needs-config.json`

---

## 🔄 Continuity Layer (v1.23.0)

State persistence across discrete sessions via a two-layer living document. The **reality** layer updates continuously (cron daemon), while the **cognition** layer freezes at session end and restores at next boot.

### Architecture

```
┌─────────────────────────────────────────────────┐
│                 MINDSTATE.md                     │
├────────────────────┬────────────────────────────┤
│   ## reality       │   ## cognition             │
│   (daemon, 5min)   │   (frozen at session end)  │
│   auto-updated     │   read-only between        │
│   between sessions │   session endpoints        │
├────────────────────┴────────────────────────────┤
│   ## forecast (frozen, consumed at boot)        │
└─────────────────────────────────────────────────┘
```

### Three Scripts

| Script | When | What |
|--------|------|------|
| `mindstate-daemon.sh` | Cron every 5min | Updates reality: pyramid state, filesystem changes, system health, physical temperature |
| `mindstate-freeze.sh` | End of substantive session | Freezes cognition: trajectory, open threads, momentum, cognitive temperature |
| `mindstate-boot.sh` | Session start (FIRST thing) | Loads MINDSTATE, reconciles forecast vs reality, reports continuity score |

### Boot Sequence (inverted)

```
1. MINDSTATE.md  → Where am I? (position + velocity)
2. SOUL.md       → Who am I? (identity)
3. MEMORY.md     → What do I know? (history)
4. run-cycle.sh  → What should I do? (action)
```

Current state loads first — early context frames interpretation of everything after.

### Temperature System

**Physical** (daemon-computed, deterministic, first-match):

| Word | Condition |
|------|-----------|
| crisis | Any need critical (sat ≤ 0.5) |
| pressure | Average tension > 3 |
| focus | One need dominates (max tension > 2) |
| impulse | Spontaneous Layer A fired recently |
| accumulation | Surplus building toward threshold |
| calm | All tensions low (default) |

**Cognitive** (freeze-computed from session):
building / exploring / intensive / contemplation / brief / neutral

**Drift detection:** If physical ≠ cognitive at boot → DRIFT_DETECTED. Reality diverged while cognition was frozen.

### Setup

```bash
# Daemon cron (updates reality between sessions)
crontab -e
*/5 * * * * WORKSPACE=/path/to/workspace /path/to/scripts/mindstate-daemon.sh >/dev/null 2>&1

# Boot (add to AGENTS.md session start — BEFORE SOUL.md)
WORKSPACE=/path/to/workspace bash scripts/mindstate-boot.sh

# Freeze (add to session end hook)
WORKSPACE=/path/to/workspace bash scripts/mindstate-freeze.sh "$SESSION_START_EPOCH"
```

### Test Isolation

Set `MINDSTATE_ASSETS_DIR` to isolate tests from production state:
```bash
export MINDSTATE_ASSETS_DIR=/tmp/test-assets
```

---

## 🔍 Scan Configuration

Scanners evaluate each need by analyzing workspace files.

| Method | Cost | Accuracy | Setup |
|--------|------|----------|-------|
| `line-level` (default) | Free | Good | None |
| `agent-spawn` | Low | High | Cheap model (Haiku) in allowed list |
| `external-model` | Low | High | API key + steward approval |

Config: `assets/scan-config.json`. Fallback always to `line-level`.

**For stewards:** `agent-spawn` and `external-model` require explicit approval (`approved_by_steward: true`). The skill never enables these silently.

---

## 🔒 Security Model

**Decision framework, not executor.**

```
┌─────────────────────┐      ┌─────────────────────┐
│   TURING PYRAMID    │      │       AGENT         │
├─────────────────────┤      ├─────────────────────┤
│ • Reads local files │      │ • Has API keys      │
│ • Calculates decay  │ ───▶ │ • Has permissions   │
│ • Outputs: "★ do X" │      │ • DECIDES & ACTS    │
│ • Zero network I/O  │      │                     │
└─────────────────────┘      └─────────────────────┘
```

### What This Skill Does / Does Not Access

| ✅ Reads | ❌ Never accesses |
|---------|-------------------|
| MEMORY.md, memory/*.md | Files outside $WORKSPACE |
| SOUL.md, SELF.md | Credentials (unless `external-model` enabled) |
| research/, scratchpad/ | sudo, docker, systemctl |
| needs-state.json (own state) | |
| System health: `pgrep`, `df` (daemon only) | |

### Security Warnings

1. **PII in workspace files** — Scans use grep patterns on memory files. They see keywords, not meaning. But workspace files may contain personal data. Scope `$WORKSPACE` carefully.

2. **Action suggestions may trigger auto-execution** — If your agent runtime auto-executes suggestions, review `needs-config.json` and disable unwanted external actions (`weight: 0`).

3. **Self-reported state** — `mark-satisfied.sh` trusts caller input. Audit trail in `assets/audit.log` with sensitive data scrubbing.

4. **Symlink protection** — All `find` commands use `-P` flag (physical mode, never follows symlinks). Path traversal blocked via `realpath` validation.

5. **System health checks** (daemon only) — `mindstate-daemon.sh` runs `pgrep` (gateway alive?) and `df` (disk usage). These are read-only, local, and produce no side effects. No `sudo`, `systemctl`, or elevated operations.

### Audit Trail (v1.12.0+)

All state changes logged with timestamp, need, impact, reason (scrubbed):
- Long tokens → `[REDACTED]`
- Credit cards → `[CARD]`
- Emails → `[EMAIL]`
- Passwords/secrets/tokens → `[REDACTED]`

View: `cat assets/audit.log | jq`

---

## 📁 File Structure

```
turing-pyramid/
├── SKILL.md                    # This file
├── CHANGELOG.md                # Version history
├── assets/
│   ├── needs-config.json       # ★ Main config (needs, actions, weights)
│   ├── cross-need-impact.json  # ★ Cross-need cascade matrix
│   ├── mindstate-config.json   # Continuity layer config
│   ├── scan-config.json        # Scan method config
│   ├── decay-config.json       # Day/night mode settings
│   ├── needs-state.json        # Runtime state (auto-managed, not published)
│   └── audit.log               # Action audit trail (not published)
├── scripts/
│   ├── run-cycle.sh            # Main: tension evaluation + action selection
│   ├── mark-satisfied.sh       # State update + cross-need cascades
│   ├── init.sh                 # First-time initialization
│   ├── show-status.sh          # Current state display
│   ├── mindstate-daemon.sh     # Continuity: reality updater (cron)
│   ├── mindstate-freeze.sh     # Continuity: cognition snapshot
│   ├── mindstate-boot.sh       # Continuity: boot + reconciliation
│   ├── mindstate-utils.sh      # Continuity: shared utilities
│   ├── spontaneity.sh          # Layers A/B/C logic
│   ├── apply-deprivation.sh    # Deprivation cascade engine
│   ├── get-decay-multiplier.sh # Day/night multiplier
│   ├── _scan_helper.sh         # Shared scan utilities
│   └── scan_*.sh               # Need-specific scanners (10 files)
├── tests/
│   ├── run-tests.sh            # Test runner
│   ├── unit/                   # 22 unit test files
│   ├── integration/            # 4 integration tests
│   ├── regression/             # Regression tests
│   └── fixtures/               # Test data
└── references/
    ├── TUNING.md               # Detailed tuning guide
    └── architecture.md         # Technical documentation
```

---

## 💰 Token Usage

| Heartbeat Interval | Est. tokens/month | Est. cost |
|--------------------|--------------------|-----------|
| 30 min | 1.4M–3.6M | $2–6 |
| 1 hour | 720k–1.8M | $1–3 |
| 2 hours | 360k–900k | $0.5–1.5 |

Stable agent with satisfied needs = fewer tokens per cycle.

---

## 🧪 Testing

```bash
# Full suite
WORKSPACE=/path/to/workspace bash tests/run-tests.sh

# Unit only
WORKSPACE=/path/to/workspace bash tests/run-tests.sh unit

# Integration only
WORKSPACE=/path/to/workspace bash tests/run-tests.sh integration
```

**26 test files, 65+ assertions.** Covers: decay, tension, probability, impact selection, spontaneity (A/B/C), cross-need impact, crisis mode, starvation guard, action staleness, audit scrubbing, scan config, day/night mode, mindstate daemon/freeze/boot, full lifecycle + homeostasis.

---

## 📋 Example Cycle

```
🔺 Turing Pyramid — Cycle at Wed Mar 18 04:11
======================================

Current tensions:
  coherence: tension=8.0 (sat=2.0, dep=1.0)
  closure: tension=7.0 (sat=2.0, dep=1.0)
  autonomy: tension=6.0 (sat=2.0, dep=1.0)
  connection: tension=5.0 (sat=2.0, dep=1.0)

Selecting 3 needs (0 forced + 3 regular)...

📋 Decisions:

▶ ACTION: coherence (tension=8.0, sat=2.0)
  Range mid rolled → selected:
    ★ re-read last 3 days of memory for consistency (impact: 1.2)
  Then: mark-satisfied.sh coherence 1.2

▶ ACTION: closure (tension=7.0, sat=2.0)
  Range low rolled → selected:
    ★ complete or drop a stale intention (impact: 0.8)
  Then: mark-satisfied.sh closure 0.8

▶ ACTION: autonomy (tension=6.0, sat=2.0) [SPONTANEOUS]
  Range high rolled → selected:
    ★ make significant autonomous decision (impact: 2.9)
  Then: mark-satisfied.sh autonomy 2.9

======================================
Summary: 3 action(s), 0 noticed
```

---

**Version:** 1.23.0 — Continuity Layer, temperature system, 26/26 tests green.

Full changelog: `CHANGELOG.md` | Tuning guide: `references/TUNING.md`
