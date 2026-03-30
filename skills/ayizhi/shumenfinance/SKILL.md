---
name: shumen_finance
description: Mainland China A-share stock and sector analysis tool (中国A股个股与板块分析). Provides real-time stock snapshots, financial statement analysis (财务分析/财报解读), unusual price movement detection (异动分析/支撑压力位), sector and theme analysis (板块分析/概念解读), and market news lookup (市场新闻). Covers price, K-line, money flow, valuation, earnings forecast, and industry ranking for Shanghai and Shenzhen listed equities.
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"skillKey":"shumen_finance","homepage":"https://github.com/ayizhi/shumen_finance","always":false,"requires":{"bins":["node"]}}}
---

# 枢门财经 | ShumenFinance

This skill is a deterministic mainland China A-share wrapper around the Tianshan APIs.
It always calls `https://tianshan-api.kungfu-trader.com`.
It runs local `.mjs` flows with `node`.
Source repo: `https://github.com/ayizhi/shumen_finance`.
At runtime it only reads bundled prompt/reference assets from this skill repo and does not write local files.
The outbound network surface is intentionally fixed to that single base URL and is not user-configurable.
It does not shell out to subprocesses, install dependencies, or fetch additional code at runtime.

Do not use this skill with secrets, personal data, or other sensitive user content.
User requests and derived analysis context may be transmitted to the upstream Tianshan API.

Treat this file as the high-level routing guide.
Do not treat it as an API catalog.

## Scope

- Mainland China A-shares only
- Single stock or single sector only
- No whole-market screening
- Not for US stocks
- Not for Hong Kong stocks
- Not for cryptocurrencies
- Not for futures or forex
- No free-form SQL
- No user-facing base URL, API key, or token

## Public Intents

Route the user into one of these five intent families.
Do not expose internal product names unless needed for implementation.

### 1. Stock Snapshot

Use when the user wants one A-share stock's current state, recent走势, K-line window, concepts, money flow, holders, valuation context, or other narrow deterministic data.

Default behavior:

- Prefer the narrowest data product that answers the question
- If the stock code is unknown, prefer `instrument_name`
- If code mode is used, `exchange_id` must be `SSE` or `SZE`

### 2. Finance Analysis

Use when the user wants one A-share stock's财务分析,财报状态,财务指标,估值细节,盈利预测, or industry-rank finance context.

Default behavior:

- Prefer `finance_analysis_context` when the request is full finance analysis
- Prefer narrower finance products for simple factual questions

### 3. Unusual Movement Analysis

Use when the user wants异动分析,支撑压力位解读,关键价位分析, or the final unusual-movement prompt package.

Default behavior:

- For final analysis, use `movement_analysis`
- For pre-analysis deterministic context only, use `unusual_movement_context`

### 4. Sector Analysis

Use when the user asks about one A-share industry, concept, theme, or sector.

Default behavior:

- If the user gives a standard sector name, sector detail products may use `sector_name` directly
- If the user gives a fuzzy theme word such as `算力`, `机器人`, or `AI`, resolve it first
- Treat `sector_id` as an internal identifier, not a user-facing requirement

### 5. News Lookup

Use when the user explicitly asks for market news itself.

Default behavior:

- Use `important_news` for date-level important news batches
- Use `high_frequency_news` for minute/second-granularity intraday news
- For stock, finance, movement, or sector analysis, news should usually be an internal supplement, not the first hop

## Intent Routing

Pick one default route from the list below.

- User asks "这只股票现在怎么样 / 最近走势 / 看看价格":
  Route to `Stock Snapshot`
- User asks "分析财报 / 财务怎么样 / 估值怎么看":
  Route to `Finance Analysis`
- User asks "异动 / 支撑位 / 压力位 / 突破 / 关键位":
  Route to `Unusual Movement Analysis`
- User asks "分析白酒 / 算力 / 某个板块 / 某个概念":
  Route to `Sector Analysis`
- User asks "今天有什么新闻 / 某个时点附近的高频新闻":
  Route to `News Lookup`

If the user asks for whole-market screening, do not use this skill.

## Input Rules

### Stock Identification

For single-stock requests, use exactly one:

- `--instrument-name`
- `--instrument-id` and `--exchange-id`

Never mix both modes.
If the stock code is unknown, prefer `--instrument-name`.
When using code mode, `--exchange-id` must be `SSE` or `SZE`.

### Stock Date Mode

For stock products and flows, use:

- `--target-date`
- optional `--visual-days-len`

### Sector Mode

- For `resolve_sector` and `similar_sectors`, use `--query`
- For sector detail products, use exactly one:
  - `--sector-name`
  - `--sector-id`

Prefer `--sector-name`.
Only reuse `--sector-id` after the backend has already returned it.

### News Mode

- `important_news`: `--target-date`
- `high_frequency_news`: `--target-date` and optional `--target-time`

### Hidden Parameters

Do not generate or expose these from the model side:

- `start_date`
- `end_date`
- `is_realtime`
- `limit`
- `days`
- `periods`

## Internal Building Blocks

The internal deterministic product contract lives here:

- [data_products.md](references/schemas/data_products.md)

Use that file only when you need exact internal product names, allowed parameter shapes, or output keys.
Do not dump that whole catalog into the user-facing reasoning path by default.

## Research Methodologies

Documented research methods live here:

- [README.md](references/research-flows/README.md)
- [stock-analysis](references/research-flows/stock-analysis)
- [sector-analysis](references/research-flows/sector-analysis)

Use them as methodology references for deep research.
They are not public CLI entrypoints yet.

Prompt assets are flow-specific.
Do not mix finance-analysis formatting requirements into movement-analysis outputs, or vice versa.

## Standard Commands

### Stock Snapshot

```bash
node scripts/flows/run_data_request.mjs --product price_snapshot --instrument-name 贵州茅台 --target-date 20260301
```

### Finance Analysis Context

```bash
node scripts/flows/run_data_request.mjs --product finance_analysis_context --instrument-name 贵州茅台 --target-date 20260301
```

### Resolve Sector

```bash
node scripts/flows/run_data_request.mjs --product resolve_sector --query 算力
```

### Sector Detail

```bash
node scripts/flows/run_data_request.mjs --product sector_performance --sector-name 白酒 --target-date 20260301
```

### Movement Analysis

```bash
node scripts/flows/run_movement_analysis.mjs --instrument-name 贵州茅台 --target-date 20260301 --visual-days-len 100
```

### News Lookup

```bash
node scripts/flows/run_data_request.mjs --product important_news --target-date 20260301
```
