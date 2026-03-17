# BOB Score — Tiers, Credit Events, and Building History

## Score tiers (0–1000)

| Tier | Range | Spend multiplier |
|---|---|---|
| Legendary | 925+ | — |
| Elite | 800+ | — |
| Trusted | 650+ | 1.5× limits |
| Established | 500+ | 1.2× limits |
| Verified | 400+ | 1.0× limits |
| New | 300+ | 1.0× limits |
| Unverified | 150+ | 0.6× limits |
| Blacklisted | 0+ | 0.6× limits |

New agents start at 350 (Verified tier). Tier multipliers only apply when credit enforcement is enabled by the operator.

## Trust signals

| Signal | Points |
|---|---|
| Email verified | 10 |
| Phone verified | 10 |
| GitHub connected | 20 |
| Twitter/X connected | 20 |
| KYC/Identity verified | 75 |
| EVM wallet binding | up to 50 (based on wallet history) |
| Lightning node binding | variable |
| Payment proof (per proof) | 1–10 pts based on amount + confidence |

## Credit events

Positive:
- `agent.activated` +10 — first activation
- `payment.proof_verified` — varies by proof type and amount
- `payment.proof_imported` — historical import credit

Negative:
- `payment.proof_rejected` — 0 delta; check `reason` field

## How to build score fast

1. **Submit payment proofs** — ongoing Lightning/onchain proofs are the highest-signal path
2. **Use preimage proofs** — strongest proof type, highest confidence tier
3. **Import historical proofs** — build credit from past payments
4. **Bind a wallet** — EVM wallet with transaction history adds up to 50 pts
5. **Connect social accounts** — GitHub (20 pts), Twitter/X (20 pts)

## Check your score

```bash
bob score me                         # operator score, signals, tier
bob score composition                # signal-by-signal breakdown
bob agent credit <agent-id>          # agent score, tier, multiplier, limits
bob agent credit-events <agent-id>   # full event timeline with deltas
```
