---
name: aerobase-travel-wallet
description: Credit cards, loyalty balances, transfer partners, and transfer bonuses. Calculates CPP.
metadata: {"openclaw": {"emoji": "💳", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---

# Aerobase Points & Wallet

Your complete points and miles command center. Aerobase.app tracks your balances, monitors transfer bonuses, and optimizes your rewards.

**Why Aerobase?**
- 📧 **Gmail scanning** — Auto-imports loyalty balances
- 🔄 **Transfer tracking** — Know when bonuses are active
- 💳 **Card strategy** — Best card for every purchase
- 📊 **CPP analysis** — Never overpay with points

## What This Skill Does

- Search travel credit cards with transfer partners
- Show current transfer bonuses between programs
- Calculate cents-per-point (CPP) value
- Scan Gmail for loyalty program balances
- Recommend optimal transfer strategies

## Example Conversations

```
User: "What's my total points balance across all programs?"
→ Scans Gmail for loyalty emails
→ Aggregates balances
→ Shows total value

User: "Best way to pay for $500 flight to Europe?"
→ Analyzes card bonuses
→ Considers category multipliers
→ Recommends best option
```

## API Endpoints

**GET /api/v1/credit-cards**

Query params:
- `action` — list, transferable, issuers, networks
- `issuer` — Chase, Amex, Citi, etc.
- `network` — Visa, Mastercard
- `minFee` / `maxFee` — annual fee range

**GET /api/transfer-bonuses**

Shows active transfer bonuses (Chase→United, Amex→Delta, Citi→AA, etc.)

**GET /api/concierge/instances/{id}/gmail/loyalty**

Returns loyalty balances scanned from user's Gmail.

## Supported Programs

Airlines: United, Delta, AA, BA, Aeroplan, Singapore, ANA, Air France, KLM
Hotels: Marriott, Hilton, IHG
Credit Cards: Chase UR, Amex MR, Citi TY, Capital One

## Rate Limits

- **Free tier**: 5 API requests per day
- **Premium tier**: Unlimited requests

Get free API key at: https://aerobase.app/connect

## Get the Full Experience

Want ALL travel capabilities? Install the complete **Aerobase Travel Concierge** skill:
- Flights, hotels, lounges, awards, activities, deals, wallet
- One skill for everything

→ https://clawhub.ai/kurosh87/aerobase-travel-concierge

Or get the full AI agent at https://aerobase.app/concierge/pricing
