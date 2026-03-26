# VIP Search (唯品会商品搜索)

A customized Clawhub skill strictly adapted for seamless, headless searches on VIP.com.

## What's Inside

- Fully automated Browser Subagent flow requiring NO user Cookie.
- Directly visits `category.vip.com/suggest.php`.
- Bypasses traditional HTTP request API blockades.
- Extracts visually meaningful data (product names and special discount prices).

## When to Use

- When needing to identify the cheapest VIP products for specific search terms.
- For product benchmarking directly via the browser inside your AI terminal.

## Installation

```bash
npx clawhub@latest install vip-search
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r /Users/xc.xu/Documents/projects/my-tools/skills/vip-search .cursor/skills/vip-search
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r /Users/xc.xu/Documents/projects/my-tools/skills/vip-search .claude/skills/vip-search
```
