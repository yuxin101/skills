# Aerobase API Reference

Base URL: `https://aerobase.app`

## Authentication

All API requests require `AEROBASE_API_KEY`:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Flights
- `POST /api/v1/flights/search` - Search flights with jetlag scoring
- `POST /api/v1/flights/compare` - Compare multiple flights
- `POST /api/v1/flights/score` - Score a flight for jetlag impact
- `POST /api/flights/search/agent` - Multi-provider parallel search

### Awards
- `POST /api/v1/awards/search` - Search award availability across 24+ programs
- `GET /api/v1/awards/trips` - List saved award trips

### Lounges
- `GET /api/v1/lounges` - Search airport lounges
- `GET /api/airports/{code}/lounges` - Lounges at specific airport

### Hotels
- `GET /api/v1/hotels` - Search hotels
- `GET /api/dayuse` - Day-use hotels for layovers
- `GET /api/hotels/near-airport/{code}` - Airport-adjacent hotels

### Activities
- `GET /api/attractions` - List attractions with filters
- `GET /api/attractions/{slug}/tours` - Tours for a specific attraction
- `GET /api/tours` - Search tours by destination

### Deals
- `GET /api/v1/deals` - Flight deals with filters
- `POST /api/deals/alerts` - Create deal alert
- `GET /api/deals/alerts` - List deal alerts

### Wallet & Cards
- `GET /api/v1/credit-cards` - Credit card transfer partners
- `GET /api/transfer-bonuses` - Current transfer bonuses
- `GET /api/wallet/summary` - Wallet overview
- `GET /api/user-loyalty-programs` - Linked loyalty programs
- `GET /api/user-loyalty?action=summary` - Wallet-wide value summary

### Recovery
- `POST /api/v1/recovery/plan` - Generate jetlag recovery plan

### Boarding Passes
- `POST /api/v1/boarding-passes` - Store boarding pass
- `GET /api/v1/boarding-passes?upcoming=true` - List upcoming passes

## Rate Limits

- **Free tier**: 5 API calls/day
- **Pro**: 500 API calls/month ($10.99/month)
- **Lifetime**: 500 API calls/month ($249 one-time)

## Errors

| Code | Meaning | Agent action |
|------|---------|--------------|
| 401/403 | Key missing/invalid | Direct user to https://aerobase.app/openclaw-travel-agent |
| 429 | Rate limited | Explain quota, suggest Pro upgrade |
| 5xx | Server error | Retry once, then return partial guidance |

## Full OpenAPI Spec

See: https://aerobase.app/api/v1/openapi
