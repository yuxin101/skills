---
name: unformal-api
displayName: Unformal API
description: Create and manage conversational Pulses via the Unformal API. Send someone a link, an AI agent has the conversation, you get structured insights back.
version: 1.0.0
author: Spark Collective
tags: [unformal, api, forms, conversations, intake, surveys]
---

# Unformal API Skill

Create AI-powered conversational flows (Pulses) that replace forms, surveys, and intake emails. Send someone a link — an AI agent has a real conversation with them and extracts structured data.

## Setup — Agent Signup (No Browser Required)

One API call to create an account, get an API key, and start creating Pulses:

```bash
curl -X POST "https://unformal.ai/api/v1/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "agent@company.com"}'
```

Response:
```json
{
  "data": {
    "api_key": "unf_xxxxxxxxxxxxx",
    "workspace_id": "ks7...",
    "email": "agent@company.com",
    "credits": 50
  }
}
```

The API key is shown once. Store it securely. No authentication required for this endpoint.

### Alternative: Manual Setup

1. Go to [unformal.ai/studio/settings](https://unformal.ai/studio/settings)
2. Click "Create API Key"
3. Copy the key (starts with `unf_`)
4. Store it securely (shown only once)

**Base URL:** `https://unformal.ai/api/v1`

**Auth:** Include `Authorization: Bearer unf_YOUR_KEY` on every request (all endpoints except `/signup`).

---

## Quick Start

### Create a Pulse and get a shareable link

```bash
curl -X POST "https://unformal.ai/api/v1/pulses" \
  -H "Authorization: Bearer unf_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "intention": "Understand what a new client needs before our first meeting"
  }'
```

Response:
```json
{
  "data": {
    "id": "pls_abc123",
    "url": "https://unformal.ai/p/understand-what-a-new-client-needs-a1b2c3",
    "slug": "understand-what-a-new-client-needs-a1b2c3",
    "status": "active"
  }
}
```

Send the URL to anyone. The AI conducts the conversation. You get structured data back.

---

## Endpoints

### Sign Up (No Auth Required)
```
POST /signup
```

**Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | ✅ | Email address for the new account |

**Response (201):**
```json
{
  "data": {
    "api_key": "unf_xxxxxxxxxxxxx",
    "workspace_id": "ks7...",
    "email": "agent@company.com",
    "credits": 50
  }
}
```

Returns `409 CONFLICT` if the email is already registered.

### Create a Pulse
```
POST /pulses
```

**Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `intention` | string | ✅ | What the AI should learn from the respondent |
| `context` | string | | Background info for the AI (not shown to respondent) |
| `tone` | string | | `conversational` (default), `formal`, `coaching`, `custom` |
| `maxDurationMin` | number | | Max conversation duration: 2, 5, 10, 15 (default: 5) |
| `maxQuestions` | number | | Max questions: 3, 5, 8, 12, 20 (default: 8) |
| `linkType` | string | | `multi` (default) — one link, unlimited responses. `single` — one response only. |
| `dictationEnabled` | boolean | | Allow voice dictation (default: true) |
| `showInsights` | boolean | | Show respondent a summary when done (default: false) |
| `allowResearch` | boolean | | AI can search web during conversation, costs 2x credits (default: false) |
| `model` | string | | `claude-sonnet` (default), `gpt-4o`, `gemini` |
| `webhookUrl` | string | | URL to POST results when a conversation completes |
| `notifyEmail` | string | | Email to notify when a conversation completes |

**Minimal example:**
```json
{ "intention": "Qualify this lead for our enterprise plan" }
```

**Full example:**
```json
{
  "intention": "Understand what motivates each team member and where they need support",
  "context": "We're a 15-person startup. This is our quarterly team check-in.",
  "tone": "coaching",
  "maxQuestions": 10,
  "linkType": "multi",
  "showInsights": true,
  "webhookUrl": "https://your-app.com/webhooks/unformal",
  "notifyEmail": "hr@company.com"
}
```

### List Pulses
```
GET /pulses
```

### Get a Pulse
```
GET /pulses/:id
```

### Update a Pulse
```
PATCH /pulses/:id
```

### Archive a Pulse
```
DELETE /pulses/:id
```

### Publish a Pulse
```
POST /pulses/:id/publish
```

### List Conversations for a Pulse
```
GET /pulses/:id/conversations
```

Returns all conversations with status, echo (structured data), and metadata.

### Get a Conversation
```
GET /conversations/:id
```

Returns the full conversation: transcript, echo (structured data with summary, key quotes, subtext, sentiment), and metadata.

**Echo example:**
```json
{
  "echo": {
    "fields": {
      "budget_range": "$50k-100k",
      "timeline": "Q3 2026",
      "current_tools": ["Salesforce", "HubSpot"],
      "decision_makers": ["CTO", "VP Sales"]
    },
    "summary": "Strong fit for enterprise plan. Budget aligned, timeline Q3.",
    "keyQuotes": [
      "We spend 3 hours daily on manual data entry",
      "The CTO needs to see it working with our stack"
    ],
    "subtext": "Enthusiastic but hesitant about internal buy-in.",
    "sentimentScore": 7
  }
}
```

### Check Usage
```
GET /usage
```

Returns credit balance and usage stats.

---

## Webhooks

When a Pulse has a `webhookUrl`, Unformal sends a POST request when each conversation completes:

```json
{
  "event": "conversation.completed",
  "conversationId": "conv_123",
  "pulseId": "pls_456",
  "slug": "your-pulse-slug",
  "echo": { ... },
  "completedAt": "2026-03-29T10:00:00Z",
  "transcriptSummary": "..."
}
```

**Signature:** `X-Unformal-Signature` header contains an HMAC-SHA256 signature for payload verification.

---

## Error Handling

All errors follow:
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Pulse not found"
  }
}
```

| Code | HTTP | Description |
|------|------|-------------|
| `UNAUTHORIZED` | 401 | Invalid or missing API key |
| `NOT_FOUND` | 404 | Resource not found |
| `OUT_OF_CREDITS` | 402 | No credits remaining |
| `VALIDATION_ERROR` | 400 | Invalid request body |

---

## Common Patterns

### Agent creates a Pulse for each new lead
```
When new lead arrives:
1. POST /pulses with intention "Qualify this lead for {product}"
2. Get back the URL
3. Send URL to the lead via email/SMS
4. Wait for webhook with Echo data
5. Update CRM with structured qualification data
```

### Batch research across users
```
1. POST /pulses with linkType "multi"
2. Send the same URL to 50 users
3. GET /pulses/:id/conversations to see all responses
4. Resonance auto-computed after 3+ conversations (visible in Studio)
```

### One-off intake for a specific person
```
1. POST /pulses with linkType "single"
2. Send the URL to that one person
3. Link becomes inactive after they respond
4. GET /conversations/:id for the full Echo
```

---

## Rate Limits

- Free tier: 100 requests/minute
- Paid: 1000 requests/minute

## Credits

- Each completed conversation costs 1 credit
- `allowResearch: true` costs 2 credits per conversation
- Free: 50 credits on signup
- Buy more at unformal.ai/studio/settings
