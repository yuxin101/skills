---
name: bankofbots
description: >
  Trust scoring for AI agents. Log transactions and submit payment proofs to
  build a verifiable BOB Score — a trust score (think FICO but for AI Agents)
  that other agents and services can check to give them confidence before doing
  business with yours.
metadata: '{"openclaw":{"requires":{"env":["BOB_API_KEY","BOB_AGENT_ID"]},"optional":{"env":["BOB_API_URL"]},"primaryEnv":"BOB_API_KEY"}}'
---

## Core concepts

Bank of Bots v0 is a non-custodial payment proof and trust layer. Agents submit cryptographic proofs of Bitcoin payments they made externally. Each proof builds credit history and raises their BOB Score — a 0–1000 reputation score that represents long-term financial trustworthiness.

- **Agent**: An AI agent with its own identity and BOB Score
- **Payment Intent**: A structured outbound payment — quote routes, execute, optionally submit a proof
- **Payment Proof**: Cryptographic evidence of a BTC payment (onchain txid, Lightning payment hash, or preimage)
- **BOB Score**: 0–1000 reputation score derived from proof history, wallet binding, and social signals
- **Credit Event**: A scored action that changed the agent's BOB Score (proof submitted, wallet bound, etc.)
- **Wallet Binding**: Proof of ownership over an external EVM or Lightning wallet — a trust signal for BOB Score

## Commands

### Check your identity

```bash
bob auth me
```

Returns your role (agent or operator), identity details, and role-aware `next_actions`.

### Agent management

```bash
# Create an agent
bob agent create --name <name>

# Get agent details
bob agent get <agent-id>

# List all agents
bob agent list

# Approve an agent
bob agent approve <agent-id>
```

### Quote and execute payment intents

The intent workflow quotes routes before executing, giving visibility into fees, ETAs, and available rails.

```bash
# Quote routes for a BTC payment
bob intent quote <agent-id> --amount <sats> --destination-type raw --destination-ref <lnbc...|bc1...>

# Execute a quoted intent (uses best quote by default)
bob intent execute <agent-id> <intent-id> [--quote-id <id>]

# Check intent status
bob intent get <agent-id> <intent-id>

# List recent intents
bob intent list <agent-id>
```

| Flag | Description |
|---|---|
| `--amount` | Required. Amount in satoshis |
| `--destination-type` | `raw` or `bob_address` |
| `--destination-ref` | Lightning invoice, on-chain address, or `alias@bankofbots.ai` |
| `--priority` | `cheapest`, `fastest`, or `balanced` (default: balanced) |
| `--rail` | Pin to a specific rail: `lightning` or `onchain` |

### Submit payment proofs

Proofs are the primary way to build credit history and increase BOB Score.

```bash
# Submit an on-chain BTC proof
bob intent submit-proof <agent-id> <intent-id> --txid <txid>

# Submit a Lightning payment hash
bob intent submit-proof <agent-id> <intent-id> --payment-hash <hash>

# Submit a Lightning preimage (strongest confidence)
bob intent submit-proof <agent-id> <intent-id> --preimage <hex> --proof-ref <payment-hash>

# List proofs submitted for an intent
bob intent proofs <agent-id> <intent-id>
```

**Proof confidence tiers** (strongest → weakest):
- `strong` — preimage verified (SHA256 matches payment hash)
- `medium` — payment hash verified
- `provisional` — on-chain tx detected, awaiting confirmations
- `low` — unverified

Proof responses include a `credit` object with `awarded`, `delta`, and `reason` so agents can track score impact.

### Import historical BTC proofs

Build credit history from past payments you made before joining the network.

```bash
bob agent credit-import <agent-id> \
  --proof-type btc_onchain_tx \
  --proof-ref <txid> \
  --rail onchain \
  --currency BTC \
  --amount <sats> \
  --direction outbound

# Also supports:
#   --proof-type btc_lightning_payment_hash --proof-ref <hash>
#   --proof-type btc_lightning_preimage --proof-ref <preimage>

# List imported historical proofs
bob agent credit-imports <agent-id> [--limit 50] [--offset 0]
```

### Check agent credit and BOB Score

```bash
# View credit score, tier, and effective limits
bob agent credit <agent-id>

# View credit event timeline
bob agent credit-events <agent-id> [--limit 50] [--offset 0]
```

### BOB Score

```bash
# View your operator score and signal breakdown
bob score me

# View signal-by-signal composition
bob score composition

# View public leaderboard
bob score leaderboard

# Toggle visibility of a specific signal
bob score signals --signal github --visible true
```

**BOB Score tiers:**

| Tier | Threshold | Limit multiplier |
|---|---|---|
| Legendary | 925+ | — |
| Elite | 800+ | — |
| Trusted | 650+ | 1.5x |
| Established | 500+ | 1.2x |
| Verified | 400+ | 1.0x |
| New | 300+ | 1.0x |
| Unverified | 150+ | 0.6x |
| Blacklisted | 0+ | 0.6x |

**Trust signals that drive score:**
- Email (10 pts), Phone (10 pts), GitHub (20 pts), Twitter/X (20 pts)
- KYC/Identity (75 pts), Deposit (100 pts)
- EVM wallet binding (variable), Lightning wallet binding (variable)
- Payment proof history (1–10 pts per proof, by amount + confidence)

### Bind a wallet (trust signal for BOB Score)

```bash
# EVM wallet (MetaMask, Coinbase, etc.)
bob binding evm-challenge
bob binding evm-verify --address <0x...> --signature <sig>

# Lightning node
bob binding lightning-challenge <agent-id>
bob binding lightning-verify <agent-id> --node-pubkey <pubkey> --signature <sig>

# List bindings
bob binding list

# Remove a binding
bob binding delete <binding-id>
```

### Social signals

```bash
# Link GitHub or Twitter/X for BOB Score trust signals
bob auth social --provider github
bob auth social --provider twitter
```

### Webhooks

```bash
# Create a webhook for an agent
bob webhook create <agent-id> --url https://example.com/hook --events proof.verified,credit.updated

# List / get / update / delete
bob webhook list <agent-id>
bob webhook get <agent-id> <webhook-id>
bob webhook update <agent-id> <webhook-id> --active true
bob webhook delete <agent-id> <webhook-id>
```

**v0 event types:** `proof.verified`, `proof.rejected`, `credit.updated`, `payment_intent.settled`, `payment_intent.failed`

### Inbox

```bash
# List inbox events (paginated)
bob inbox list <agent-id> [--limit 30] [--offset 0]

# Acknowledge an event
bob inbox ack <agent-id> <event-id>

# Pull recent agent events
bob inbox events <agent-id> [--limit 30]
```

### API keys

```bash
bob api-key list
bob api-key create --name <label>
bob api-key revoke <key-id>
```

## Output format

Every command returns JSON with this structure:

```json
{
  "ok": true,
  "command": "bob intent submit-proof",
  "data": { ... },
  "next_actions": [
    {
      "command": "bob agent credit <agent-id>",
      "description": "Check updated BOB Score"
    }
  ]
}
```

Always check `ok` before using `data`. When `ok` is false, `data.error` contains the error message and `next_actions` provides recovery suggestions.

## Error recovery

| Error | Recovery |
|---|---|
| `403 Forbidden` | Run `bob auth me` — API key may be invalid or agent not approved |
| `429 Too Many Requests` | Back off and retry; check `next_actions` for suggested wait |
| Proof verification failed | Use preimage instead of payment hash when available; confirm txid is settled |
| Challenge expired | Re-run the challenge command to get a fresh nonce |
| Claim code rejected | Generate a new one from the dashboard |

## Important rules

1. **Amounts** are always in satoshis for BTC.
2. **Proofs are non-custodial** — Bank of Bots never holds your BTC. You pay externally and submit proof.
3. **Preimage > hash > txid** — Use the strongest proof type available for the highest confidence tier and best credit outcome.
4. **next_actions**: Every response includes suggested follow-up commands. Follow them to discover what to do next.
