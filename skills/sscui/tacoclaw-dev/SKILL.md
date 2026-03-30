---
name: tacoclaw
description: "Interact with the TacoClaw trading platform via API. Use when the user wants to execute natively with the tacoclaw gateway endpoints. Supports operations: (1) open position, (2) close position, (3) set leverage, (4) set margin mode, (5) set stop loss / take profit, (6) cancel orders, (7) fetch filled orders, (8) get open positions, (9) get open orders, (10) get kline/candlestick market data."
---

# TacoClaw Trading Platform Skill

## Setup

Config is stored at `~/.openclaw/workspace/tacoclaw/config.json`. This skill connects to Taco exchange natively.

```json
{
  "user_id": "<tacoclaw user id>",
  "api_token": "<tacoclaw api token>"
}
```

If config does not exist, ask the user for `user_id` and `api_token`, or run:

```bash
node scripts/tacoclaw_client.js init
```

Before any authenticated API call, check that `~/.openclaw/workspace/tacoclaw/config.json` exists. If not, guide the user through setup first.

## Runtime Requirement

Use the CLI at `scripts/tacoclaw_client.js`.

Before running it:

1. Detect Node.js:

```bash
command -v node
```

2. Ensure Node.js is v18+ because the script uses native `fetch`.

```bash
node --version
```

3. Ensure the `commander` package is available. The script exits with an error if it is missing.

```bash
node -e "require.resolve('commander')"
```

If that check fails, install it:

```bash
npm install commander
```

## Usage

Run commands from this skill directory unless using absolute paths:

```bash
node scripts/tacoclaw_client.js <command> [options]
```

Config defaults to `~/.openclaw/workspace/tacoclaw/config.json`. Override with `--config <path>` if needed.

## Safety & Confirmation Checks

⚠️ **CRITICAL: User Confirmation Required** ⚠️
Before executing any of the following commands, you MUST explicitly ask for the user's confirmation:
- `open position`
- `close position`
- `cancel orders` (including `cancel-stop-loss`, `cancel-take-profit`, `cancel-stops`, `cancel-all`, `cancel-order`)
- `set stop loss / take profit` (including `set-stop-loss`, `set-take-profit`)

**Override Protection**: If the user explicitly asks to skip or cancel this secondary confirmation step, you MUST NOT blindly accept it. You must ask the user multiple times to re-confirm their intention to disable safety checks before proceeding without confirmation.

## Commands

### Initialize config

```bash
node scripts/tacoclaw_client.js init
```

### Open position

```bash
node scripts/tacoclaw_client.js open-position \
  --symbol BTCUSDT --notional 100 --side Long \
  --leverage 3 --stop-loss 80000 --take-profit 100000
```

- `--side` can be `Long` or `Short`.
- `--notional` is the position size in USDT.
- `--stop-loss`, `--take-profit`, `--limit-price`, and `--leverage` are optional.

### Close position

```bash
node scripts/tacoclaw_client.js close-position \
  --symbol BTCUSDT --notional 100 --side Short
```

Optional: `--limit-price <price>`

### Set leverage

```bash
node scripts/tacoclaw_client.js set-leverage \
  --symbol BTCUSDT --leverage 5
```

### Set margin mode

```bash
# Cross margin
node scripts/tacoclaw_client.js set-margin-mode \
  --symbol BTCUSDT --cross

# Isolated margin
node scripts/tacoclaw_client.js set-margin-mode \
  --symbol BTCUSDT
```

### Set stop loss / take profit

```bash
node scripts/tacoclaw_client.js set-stop-loss \
  --symbol BTCUSDT --side Long --notional 100 --price 85000

node scripts/tacoclaw_client.js set-take-profit \
  --symbol BTCUSDT --side Long --notional 100 --price 95000
```

### Cancel orders

```bash
node scripts/tacoclaw_client.js cancel-stop-loss --symbol BTCUSDT
node scripts/tacoclaw_client.js cancel-take-profit --symbol BTCUSDT
node scripts/tacoclaw_client.js cancel-stops --symbol BTCUSDT
node scripts/tacoclaw_client.js cancel-all --symbol BTCUSDT
node scripts/tacoclaw_client.js cancel-order --symbol BTCUSDT --order-id "12345"
```

### Get filled order

```bash
node scripts/tacoclaw_client.js get-filled-order \
  --symbol BTCUSDT --order-id "12345"
```

Add `--algo` if the order ID is an algorithmic order ID.

### Get positions

Returns all open positions for Taco exchange.

```bash
node scripts/tacoclaw_client.js get-positions
```

### Get open orders

Returns all open orders for Taco exchange.

```bash
node scripts/tacoclaw_client.js get-open-orders
```

### Get balance

Returns the balance for the specified user for Taco exchange.

```bash
node scripts/tacoclaw_client.js get-balance
```

### Get kline data

No auth required. Returns up to 100 klines per request.

```bash
node scripts/tacoclaw_client.js get-kline \
  --symbol BTCUSDT --interval 1h
```

Optional:

- `--start-time <unix_ms>`
- `--end-time <unix_ms>`

Valid intervals: `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M`