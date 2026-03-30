# NoddyAI API Skill

Call the NoddyAI platform API (graine.ai) to manage voice agents, place calls, handle telephony, and retrieve call records.

## ClawHub / OpenClaw notes

- This skill describes **HTTP calls** to `https://api.graine.ai`. It does **not** require a local `openclaw run` command (many CLI versions have no `run` - use `openclaw --help`).
- **Test locally** with `curl` or any HTTP client; see `README.md` for CLI troubleshooting and ClawHub publish tips (slug conflicts, network status codes).

## Setup

All requests require:
- **Base URL**: `https://api.graine.ai`
- **Auth header**: `Authorization: Bearer <API_KEY>` (keys start with `gat_`)
- **org_id**: your organization ID (format: `organization-XXXX`)

Refer to `endpoints.md` for the full endpoint reference and `examples.md` for ready-to-use request bodies.

## How to use this skill

When the user asks you to interact with NoddyAI, identify which operation they need from the list below and construct the HTTP request using the details in `endpoints.md`.

### Operations available

| # | Operation | Method | Path |
|---|-----------|--------|------|
| 1 | Validate API token | GET | `/api/v1/api-tokens/validate-token` |
| 2 | List API tokens | GET | `/api/v1/api-tokens/list-tokens` |
| 3 | Revoke API token | DELETE | `/api/v1/api-tokens/revoke-token/{token}` |
| 4 | Create voice agent | POST | `/api/v1/agents` |
| 5 | Get agent (runtime format) | GET | `/api/v1/agents/{agent_id}` |
| 6 | List agents | GET | `/api/v1/agents` |
| 7 | Update agent voice/synthesizer | PATCH | `/api/v1/agents/{agent_id}` |
| 8 | Update agent system prompt | PATCH | `/api/v1/agents/{agent_id}` |
| 9 | Add API tool/skill to agent | PATCH | `/api/v1/agents/{agent_id}` |
| 10 | Delete agent | DELETE | `/api/v1/agents/{agent_id}` |
| 11 | Make outbound call | POST | `/api/v1/telephony/call` |
| 12 | Get call status | GET | `/api/v1/telephony/call/{call_sid}` |
| 13 | Transfer call (human handoff) | POST | `/api/v1/telephony/transfer` |
| 14 | Create inbound agent | POST | `/api/v1/telephony/inbound-agents` |
| 15 | Update inbound webhook URLs | PATCH | `/api/v1/telephony/inbound-agents/webhooks` |
| 16 | Submit batch call | POST | `/api/v1/batch/calls` |
| 17 | Upload CSV batch | POST | `/api/v1/batch/upload` |
| 18 | List call records | GET | `/api/v1/calls` |
| 19 | Get single call record | GET | `/api/v1/calls/{call_sid}` |

## Response behavior

- Always show the HTTP status and response body.
- For `call_sid` values returned from telephony calls, save them for subsequent status checks.
- For agent IDs returned from create operations, save for subsequent PATCH/DELETE operations.
- Webhook payloads are described in `webhooks.md` - use that reference when building webhook handlers.
