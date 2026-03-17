# BOB Score — Proof Submission

Submitting payment proofs verifies settlement and awards BOB Score credit. Stronger proof types earn more credit.

## Proof types

| Type | Flag(s) | Confidence | What it proves |
|---|---|---|---|
| `btc_lightning_preimage` | `--preimage <hex> --proof-ref <hash>` | **strong** | SHA256(preimage) == payment hash — cryptographically irrefutable |
| `btc_lightning_payment_hash` | `--payment-hash <hash>` | **medium** | Payment hash observed on node |
| `btc_onchain_tx` | `--txid <txid>` | **provisional→strong** | On-chain tx confirmed (upgrades as confirmations accumulate) |
| `eth_onchain_tx` | `--proof-type eth_onchain_tx --proof-ref <txhash> [--chain-id 0x1]` | **medium→strong** | EVM on-chain tx (Ethereum mainnet or Base) |
| `base_onchain_tx` | `--proof-type base_onchain_tx --proof-ref <txhash>` | **medium→strong** | Base L2 on-chain tx |
| `sol_onchain_tx` | `--proof-type sol_onchain_tx --proof-ref <txsig>` | **medium→strong** | Solana on-chain tx |

## Submit proof against a payment intent

```bash
# BTC on-chain
bob intent submit-proof <agent-id> <intent-id> --txid <txid>

# Lightning payment hash
bob intent submit-proof <agent-id> <intent-id> --payment-hash <hash>

# Lightning preimage (highest confidence)
bob intent submit-proof <agent-id> <intent-id> \
  --preimage <hex> --proof-ref <payment-hash>

# EVM on-chain (Ethereum mainnet)
bob intent submit-proof <agent-id> <intent-id> \
  --proof-type eth_onchain_tx --proof-ref <0x...txhash> --chain-id 0x1

# Solana on-chain
bob intent submit-proof <agent-id> <intent-id> \
  --proof-type sol_onchain_tx --proof-ref <txsig>
```

## Import historical proofs (credit building)

For payments that happened before BOB tracking was set up:

```bash
bob agent credit-import <agent-id> \
  --proof-type btc_lightning_preimage \
  --proof-ref <payment-hash> \
  --rail lightning \
  --currency BTC \
  --amount <sats> \
  --direction outbound
```

Supported `--proof-type` values: `btc_onchain_tx`, `btc_lightning_payment_hash`, `btc_lightning_preimage`, `eth_onchain_tx`, `base_onchain_tx`, `sol_onchain_tx`

Historical imports are capped — they count toward score but cannot substitute for ongoing payment history.

## How proofs affect BOB Score

- Each verified proof emits a credit event with `awarded`, `delta`, and `reason`
- Amount thresholds: floor is 1,000 sats / 1,000,000 gwei / 1,000,000 lamports
- Preimage proofs earn the highest confidence tier
- Duplicate proof refs are deduplicated — same txid/hash twice doesn't double-count
