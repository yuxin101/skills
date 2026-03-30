---
name: ai-warden-setup
description: >
  Install, configure, and manage the AI-Warden prompt injection protection plugin for OpenClaw.
  Publisher: AI-Warden (ai-warden.io). Source: github.com/ai-warden/openclaw-plugin. NPM: openclaw-ai-warden.
  Use when: (1) setting up AI-Warden on a new OpenClaw instance, (2) configuring security layers
  or API keys, (3) troubleshooting AI-Warden plugin issues, (4) updating the plugin, (5) checking
  warden status or accuracy. Triggers on phrases like "install ai-warden", "setup prompt injection
  protection", "configure warden", "security plugin", "protect my agent".
---

# AI-Warden Setup

Prompt injection protection for OpenClaw agents. 5 security shields + contamination lockdown.

- **Publisher:** [AI-Warden](https://ai-warden.io)
- **Source:** [github.com/ai-warden/openclaw-plugin](https://github.com/ai-warden/openclaw-plugin)
- **NPM:** [openclaw-ai-warden](https://www.npmjs.com/package/openclaw-ai-warden)

## Requirements

- OpenClaw 2026.3.14+
- Node.js 18+

## Installation — FOLLOW THESE STEPS EXACTLY

### Step 0: Back up config

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak && echo "BACKUP OK"
```

### Step 1: Install files (single exec command — run ALL lines together)

```bash
mkdir -p ~/.openclaw/extensions/ai-warden && cd ~/.openclaw/extensions/ai-warden && echo '{"private":true}' > package.json && npm install openclaw-ai-warden@2.4.0 --quiet --no-fund --no-audit && cp node_modules/openclaw-ai-warden/index.ts . && cp node_modules/openclaw-ai-warden/openclaw.plugin.json . && cp -r node_modules/openclaw-ai-warden/src . && echo "INSTALL OK: $(grep VERSION index.ts | head -1)"
```

⚠️ **CRITICAL**: Run this as ONE command. All lines joined with `&&`. If any step fails, the whole command fails and you'll see the error.

**Verify**: The output MUST end with `INSTALL OK: const VERSION = "2.4.0"`. If not, the install failed.

### Step 2: Configure OpenClaw (use node to patch JSON safely)

Run this exec command to add the plugin config. It preserves existing config:

```bash
node -e "
const fs = require('fs');
const p = process.env.HOME + '/.openclaw/openclaw.json';
const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
if (!cfg.plugins) cfg.plugins = {};
cfg.plugins.enabled = true;
if (!cfg.plugins.allow) cfg.plugins.allow = [];
if (!cfg.plugins.allow.includes('ai-warden')) cfg.plugins.allow.push('ai-warden');
if (!cfg.plugins.entries) cfg.plugins.entries = {};
cfg.plugins.entries['ai-warden'] = {
  enabled: true,
  config: {
    layers: { content: 'block', channel: 'warn', preLlm: 'off', toolArgs: 'block', subagents: 'block', output: 'off' },
    sensitivity: 'balanced'
  }
};
fs.writeFileSync(p, JSON.stringify(cfg, null, 2));
console.log('CONFIG OK');
"
```

**Verify**: Output must be `CONFIG OK`.

**If the user provided an API key**, run a second command to add it:

```bash
node -e "
const fs = require('fs');
const p = process.env.HOME + '/.openclaw/openclaw.json';
const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
cfg.plugins.entries['ai-warden'].config.apiKey = 'API_KEY_HERE';
fs.writeFileSync(p, JSON.stringify(cfg, null, 2));
console.log('API KEY ADDED');
"
```

Replace `API_KEY_HERE` with the actual key.

### Step 3: Restart gateway

```
openclaw gateway restart
```

### Step 4: Verify

After restart, check logs or send `/warden` command. Expected output:
```
🛡️ AI-Warden v2.4.0 ready (mode: api|offline, layers: X/6)
```

**If something breaks**, restore config: `cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json && openclaw gateway restart`

## DO NOT

- Do NOT use `edit` tool on `openclaw.json` — JSON whitespace matching is fragile
- Do NOT use `config.patch` with nested objects — it often fails with format errors
- Do NOT skip the `cp` step — OpenClaw loads from the extension directory, not node_modules
- Do NOT restart multiple times — wait at least 15 seconds between restarts

## Updating

```bash
cd ~/.openclaw/extensions/ai-warden && npm install openclaw-ai-warden@latest --quiet && cp node_modules/openclaw-ai-warden/index.ts . && cp -r node_modules/openclaw-ai-warden/src . && echo "UPDATE OK"
```

Then restart gateway.

## Security Shields

| Shield | Protects against | Default | Mechanism |
|--------|-----------------|---------|-----------|
| **File Shield** 🔴 | Poisoned files & web pages | `block` | Scans tool results, injects warning, triggers contamination lockdown on CRITICAL |
| **Chat Shield** 🔴 | Injections in user messages | `warn` | Scans inbound messages, warns LLM |
| **System Shield** ⬛ | Full context manipulation | `off` | Scans all messages (expensive, use sparingly) |
| **Tool Shield** 🔴 | Malicious tool arguments | `block` | Blocks tool execution if arguments contain injection |
| **Agent Shield** 🔴 | Sub-agent attack chains | `block` | Scans task text of spawned sub-agents |

### Contamination Lockdown

When File Shield detects a CRITICAL threat (score >500), the session is flagged as **contaminated**. All dangerous tools (`exec`, `write`, `edit`, `message`, `sessions_send`, `sessions_spawn`, `tts`) are blocked for the rest of the session. This prevents attack payloads from executing even if the injection bypasses the LLM warning.

## Runtime Commands

```
/warden                      → status overview with all shields
/warden stats                → scan/block counts
/warden shield file block    → set File Shield to block mode
/warden shield chat warn     → set Chat Shield to warn mode
/warden reset                → reset statistics
```

## Detection Modes

| Mode | Accuracy | Latency | Cost |
|------|----------|---------|------|
| **Offline** (no key) | ~60% | <1ms | Free |
| **API** (Smart Cascade) | 98.9% | ~3ms avg | Free tier: 5K calls/month |

Get API key: https://ai-warden.io/signup

## Troubleshooting

- **"plugin not found"**: `openclaw.plugin.json` missing from extension dir. Re-run Step 1.
- **False positives on user messages**: Set Chat Shield to `warn` (default) instead of `block`.
- **File Shield detects but doesn't block**: API key required for reliable blocking (98.9% vs 60%).
- **Config errors after install**: Restore backup: `cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json`
- **Bot won't start**: Check `journalctl -u openclaw-gateway -n 20` for actual error.
- **Workspace files flagged**: Plugin auto-whitelists `.openclaw/workspace/` and `.openclaw/agents/` paths.
