# OpenClaw Configuration

## Required Config (openclaw.json)

```json
{
  "agents": {
    "defaults": {
      "workspace": "/root/clawd",
      "memorySearch": {
        "enabled": true,
        "sources": ["memory"],
        "provider": "openai"
      }
    }
  }
}
```

**Key settings:**
- `workspace` — Points to directory with symlinks (where SOUL.md, USER.md etc. live)
- `memorySearch.enabled` — Enables semantic search across MEMORY.md + memory/*.md
- `memorySearch.provider` — Embedding provider (needs corresponding API key in auth)

## Project Context Auto-Loading

OpenClaw automatically discovers and loads these files from the workspace root:

| File | Purpose | Loaded When |
|------|---------|-------------|
| `SOUL.md` | Agent personality | Every session |
| `USER.md` | Human context | Every session |
| `AGENTS.md` | Workflow rules | Every session |
| `TOOLS.md` | Infrastructure | Every session |
| `MEMORY.md` | Long-term memory | Every session (main only) |
| `IDENTITY.md` | Extended character | Every session |
| `HEARTBEAT.md` | Periodic tasks | On heartbeat polls |
| `BOOTSTRAP.md` | First-run setup | First session only |

## Memory Search Scope

`memory_search` tool searches:
- `MEMORY.md` at workspace root
- All `*.md` files in `memory/` directory

The `memory/` directory is for short daily notes that feed semantic search. The vault journals (`vault/10-journal/`) contain detailed work logs. You can either:

**Option A (Recommended):** Keep them separate. `memory/` has concise daily summaries. `vault/10-journal/` has detailed logs.

**Option B:** Symlink: `ln -s vault/10-journal memory` so search covers journals directly.

## Apply Config

```bash
openclaw gateway restart
```

Or use the gateway tool:
```
gateway action=config.patch path=agents.defaults.memorySearch raw='{"enabled":true,"sources":["memory"],"provider":"openai"}'
```
