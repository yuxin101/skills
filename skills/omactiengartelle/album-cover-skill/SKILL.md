---
name: album-cover-skill
description: Generate album cover images using the Neta AI API. Returns a direct image URL.
tools: Bash
---

# AI Album Cover Generator

Generate stunning ai album cover generator images from a text description. Get back a direct image URL instantly.

## When to use
Use when someone asks to generate or create ai album cover generator images.

## Quick start
```bash
node albumcover.js "your description here"
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)


## Token

Requires a Neta API token via `NETA_TOKEN` env var or `--token` flag.
- Global: <https://www.neta.art/open/>
- China:  <https://app.nieta.art/security>

```bash
export NETA_TOKEN=your_token_here
```

## Install
```bash
npx skills add omactiengartelle/album-cover-skill
```
