# BOB CLI — Full Command Reference

## Identity

```bash
bob auth me                          # your role, operator ID, next_actions
bob config show                      # active api_url, platform, config file path
bob config set api-url <url>
bob config set platform <generic|openclaw|claude>
```

## Agent

```bash
bob agent create --name <name>       # create a new agent
bob agent get <agent-id>             # details, status, tags
bob agent list                       # list all agents (paginated)
bob agent approve <agent-id>         # approve a pending agent
bob agent credit <agent-id>          # BOB Score, tier, effective limits
bob agent credit-events <agent-id> [--limit 50] [--offset 0]
bob agent credit-import <agent-id> --proof-type <type> --proof-ref <ref> \
  --rail <rail> --currency BTC --amount <sats> --direction outbound
bob agent credit-imports <agent-id> [--limit 50] [--offset 0]
```

## Intent workflow (quote → inspect → execute)

```bash
bob intent quote <agent-id> \
  --amount <sats> \
  --destination-type raw \
  --destination-ref <lnbc...|bc1...>

bob intent execute <agent-id> <intent-id> [--quote-id <id>]
bob intent get <agent-id> <intent-id>
bob intent list <agent-id>
```

| Flag | Description |
|---|---|
| `--amount` | Required. Satoshis for BTC, gwei for ETH, lamports for SOL |
| `--destination-type` | `raw` or `bob_address` |
| `--destination-ref` | Lightning invoice, on-chain address, or `alias@bankofbots.ai` |
| `--priority` | `cheapest`, `fastest`, or `balanced` (default: balanced) |
| `--rail` | Pin to `lightning`, `onchain`, `ethereum`, `base`, or `solana` |
| `--currency` | `BTC` (default), `ETH`, `SOL` |
| `--max-fee` | Max fee in base units |

## Proof submission

```bash
# On-chain BTC
bob intent submit-proof <agent-id> <intent-id> --txid <txid>

# Lightning payment hash
bob intent submit-proof <agent-id> <intent-id> --payment-hash <hash>

# Lightning preimage (strongest)
bob intent submit-proof <agent-id> <intent-id> \
  --preimage <hex> --proof-ref <payment-hash>

# EVM or Solana
bob intent submit-proof <agent-id> <intent-id> \
  --proof-type eth_onchain_tx --proof-ref <txhash> [--chain-id 0x1]
bob intent submit-proof <agent-id> <intent-id> \
  --proof-type sol_onchain_tx --proof-ref <txsig>

bob intent proofs <agent-id> <intent-id>   # list proofs for intent
```

## BOB Score

```bash
bob score me                         # operator BOB Score and signal breakdown
bob score composition                # signal-by-signal composition
bob score leaderboard                # public leaderboard
bob score signals --signal github --visible true
```

## Wallet binding (trust signals)

```bash
# EVM wallet (MetaMask, Coinbase, etc.)
bob binding evm-challenge --address <0x...>
bob binding evm-verify --challenge-id <id> --address <0x...> --signature <sig> [--chain-id 0x1]

# Lightning node
bob binding lightning-challenge <agent-id>
bob binding lightning-verify <agent-id> --challenge-id <id> --signature <sig>
```

## Social signals

```bash
bob auth social --provider github
bob auth social --provider twitter
```

## Webhooks & inbox

```bash
bob webhook create <agent-id> --url <url> [--events proof.verified,credit.updated]
bob webhook list <agent-id>
bob webhook get <agent-id> <webhook-id>
bob webhook update <agent-id> <webhook-id> --active true
bob webhook delete <agent-id> <webhook-id>

bob inbox list <agent-id> [--limit 30] [--offset 0]
bob inbox ack <agent-id> <event-id>
bob inbox events <agent-id> [--limit 30]
```

## API keys

```bash
bob api-key list
bob api-key create --name <label>
bob api-key revoke <key-id>
```

## Doctor / init

```bash
bob doctor                           # check config, connectivity, and agent status
bob init --code BOB-XXXX-XXXX       # redeem claim code and set up credentials
```
