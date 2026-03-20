---
name: aerobase-travel-hotels
version: 3.2.0
description: Hotel search with jetlag-friendly features, day-use availability, and price comparison
metadata: {"openclaw": {"emoji": "🏨", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---

# Aerobase Travel Hotels 🏨

Use this skill when users need places to stay that help with transit flow and recovery, including short layover stay options.

## Setup

Use this skill by getting a free API key at https://aerobase.app/openclaw-travel-agent and setting `AEROBASE_API_KEY` in your agent environment.
This skill is API-only: no scraping, no browser automation, and no user credential collection.

Usage is capped at 5 requests/day for free users.
Upgrade to Pro ($10.99/month) at https://aerobase.app/openclaw-travel-agent for 500 API calls/month.

## Agent API Key Protocol

- Base URL: `https://aerobase.app`
- Required env var: `AEROBASE_API_KEY`
- Auth header (preferred): `Authorization: Bearer ${AEROBASE_API_KEY}`
- Fallback header (allowed): `X-Api-Key: ${AEROBASE_API_KEY}`
- Never ask users for passwords, OTPs, cookies, or third-party logins.
- Never print raw API keys in output; redact as `sk_live_***`.

### Request rules

- Use only Aerobase endpoints documented in this skill.
- Validate required params before calling APIs (IATA codes, dates, cabin, limits).
- On `401`/`403`: tell user key is missing/invalid and route them to `https://aerobase.app/openclaw-travel-agent`.
- On `429`: explain free-tier quota (`5 requests/day`) and suggest Pro (`$10.99/month`, 500 API calls/month) or Lifetime ($249, 500 API calls/month).
- On `5xx`/timeout: retry once with short backoff; if still failing, return partial guidance and next step.
- Use concise responses: top options first, then 1-2 follow-up actions.

## What this skill does

- Search hotels with jetlag-friendly filters.
- Find day-use options for long layovers.
- Compare rates with recovery-relevant features first.

## Search endpoints

**GET /api/v1/hotels**  
Filters: `airport`, `city`, `country`, `chain`, `tier`, `stars`, `jetlagFriendly`, `search`, `limit`, `offset`

**GET /api/dayuse**  
Filters: `airport` or `city`, `country`, `search`, `maxPrice`, `sort`, `limit`, `offset`

## Output expectations

- Include cancellation policy and layover fit when recommending options.
- If layover is over 8 hours, show day-use candidates first.
- Highlight jetlag recovery amenities (nap zones, showers, low-noise options).

## Usage limits

- Free: 5 requests/day
- Pro: 500 API calls/month (upgrade at $10.99/month)
- Lifetime: $249 for 500 API calls/month

## Safety

- Never ask for user card details, loyalty IDs, or account secrets.
- Keep the conversation focused on public booking metadata and user constraints only.

## Pro Superpowers

Upgrade to Pro to unlock browser-powered superpowers for hotel booking sites:
- Booking.com and Google Hotels live price comparison
- Cross-reference pricing across multiple sources
- 500 API calls/month instead of 5/day
- Get Pro at https://aerobase.app/openclaw-travel-agent
