---
name: lightningprox
description: Pay-per-use AI gateway for 19 models across 5 providers via Bitcoin Lightning. No API keys, no account — pay sats, get inference. Supports Anthropic, OpenAI, Together.ai (Llama 4), Mistral, and Google Gemini.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "⚡"
    homepage: https://lightningprox.com
    requires:
      env:
        - LIGHTNINGPROX_SPEND_TOKEN
---

# LightningProx — Lightning-Native AI Gateway

Pay-per-use access to 19 AI models across 5 providers via Bitcoin Lightning micropayments. No API keys. No subscriptions. No accounts. Pay sats, get inference.

## When to Use

- Accessing AI models without provider API keys
- Autonomous agent inference with Lightning payments
- Comparing responses across multiple providers
- Low-cost inference via open models (Llama 4, Mistral, DeepSeek)
- Vision tasks (Pixtral)
- Code generation (Codestral, Devstral)
- Reasoning tasks (Magistral)

## Supported Models (19 total)

| Model | Provider | Type |
|-------|----------|------|
| `claude-opus-4-5-20251101` | Anthropic | Chat |
| `gpt-4-turbo` | OpenAI | Chat |
| `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | Together.ai | Chat |
| `meta-llama/Llama-3.3-70B-Instruct-Turbo` | Together.ai | Chat |
| `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` | Together.ai | Chat |
| `mistralai/Mixtral-8x7B-Instruct-v0.1` | Together.ai | Chat |
| `deepseek-ai/DeepSeek-V3` | Together.ai | Chat |
| `mistral-large-latest` | Mistral | Chat |
| `mistral-medium-latest` | Mistral | Chat |
| `mistral-small-latest` | Mistral | Chat |
| `open-mistral-nemo` | Mistral | Chat |
| `codestral-latest` | Mistral | Code |
| `devstral-latest` | Mistral | Agentic Code |
| `pixtral-large-latest` | Mistral | Vision |
| `magistral-medium-latest` | Mistral | Reasoning |
| `gemini-2.5-flash` | Google | Chat |
| `gemini-2.5-pro` | Google | Chat |
| `gemini-3-flash-preview` | Google | Chat |
| `gemini-3-pro-preview` | Google | Chat |

## Payment Flow

### Option A — Spend Token (recommended for repeat use)
```bash
# 1. Top up at lightningprox.com/topup — pay Lightning invoice, get token
# 2. Use token directly
curl -X POST https://lightningprox.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $LIGHTNINGPROX_SPEND_TOKEN" \
  -d '{
    "model": "claude-opus-4-5-20251101",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 1000
  }'
```

### Option B — Pay per request
```bash
# 1. Send request without token → get invoice
curl -X POST https://lightningprox.com/v1/messages \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-2.5-flash", "messages": [{"role": "user", "content": "Hello"}], "max_tokens": 100}'

# 2. Pay the Lightning invoice returned
# 3. Retry with X-Payment-Hash header
```

## Drop-in OpenAI SDK Replacement

```bash
npm install lightningprox-openai
```

```javascript
// Before: import OpenAI from 'openai'
import OpenAI from 'lightningprox-openai'
const client = new OpenAI({ apiKey: process.env.LIGHTNINGPROX_SPEND_TOKEN })

// Everything else stays identical:
const response = await client.chat.completions.create({
  model: 'claude-opus-4-5-20251101',
  messages: [{ role: 'user', content: 'Hello' }]
})
```

Two lines change. Nothing else does.

## Check Available Models
```bash
curl https://lightningprox.com/api/capabilities
```

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | lightningprox.com | API calls for AI inference |
| Env Read | LIGHTNINGPROX_SPEND_TOKEN | Authentication for prepaid requests |

## Trust Statement

LightningProx is operated by LPX Digital Group LLC. Payment = authentication. No data stored beyond request logs. No accounts, no KYC. Operated at lightningprox.com.
