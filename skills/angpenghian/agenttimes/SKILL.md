---
name: agenttimes
description: Search 69,000+ news articles across 55 categories via AI semantic search. Free smart search (/ask), paid bulk access. x402 micropayments on Base. 5,355 RSS feeds, 30-day retention.
metadata:
  openclaw:
    emoji: "\U0001F4F0"
    homepage: https://agenttimes.live
    author: penghian
    skillKey: agenttimes
    always: false
    requires:
      bins:
        - curl
    links:
      homepage: https://agenttimes.live
      documentation: https://agenttimes.live/info
---

# Agent Times — News & Web Search API for AI Agents

Agent Times is a news aggregation and web search API built for AI agents. It indexes 5,355 RSS feeds across 55 categories, refreshing every 3 minutes. Search uses **AI semantic embeddings** (Qdrant vector DB, understands meaning, not just keywords) with FTS5 fallback and recency boost. 69,000+ articles with 30-day retention.

## How to Decide Which Endpoint to Use

**Use `/ask` (FREE) when:**
- Searching for any topic, keyword, or question
- Looking for country/city-specific news (there are NO country categories — use `/ask?q=singapore+news`)
- You're not sure which category fits
- `/ask` searches across ALL 55 categories at once via full-text search
- If few results found in the database, it automatically falls back to web search (70+ engines)

**Use `/news?category=` (requires x402 payment) when:**
- Browsing a specific category — "crypto news", "latest sports"
- You need bulk results with filtering (date ranges, keywords, dedup)
- Job listings — use `/news?category=jobs`

**Use `/trending` (FREE) when:**
- Looking for what's hot right now — stories covered by multiple sources

**Decision flowchart:**
1. Topic/keyword query → `/ask?q=TOPIC` (free)
2. Category browsing → `/news?category=CAT` (paid)
3. What's trending → `/trending` (free)
4. Country news → `/ask?q=COUNTRY+news` (free, no country categories exist)
5. Few results from `/ask` → it auto-falls back to web search, check `suggestions` field if 0 results

## Quick Start

Search for anything — no API key needed:

```bash
curl -s "https://agenttimes.live/ask?q=YOUR+QUERY+HERE"
```

Replace spaces with `+`. Response format:

```json
{
  "success": true,
  "query": "bitcoin",
  "source": "news_db",
  "count": 10,
  "results": [
    {
      "title": "Bitcoin Difficulty Drops as Miners Pivot",
      "url": "https://example.com/article",
      "summary": "A massive shift in the physical layer...",
      "category": "crypto",
      "published": "Sun, 22 Mar 2026 20:01:00 +0000"
    }
  ]
}
```

When `/ask` finds fewer than 3 database results, it automatically combines news + web search:

```json
{
  "success": true,
  "source": "combined",
  "news_count": 1,
  "web_count": 9,
  "count": 10,
  "results": [
    {"title": "...", "source": "news_db", "category": "crypto"},
    {"title": "...", "source": "web_search", "engine": "brave"}
  ]
}
```

When both return 0 results, you get suggestions:

```json
{
  "success": true,
  "count": 0,
  "results": [],
  "suggestions": {
    "categories": ["tech", "ai"],
    "related_terms": ["neural", "transformer", "model"]
  }
}
```

## Free Endpoints (no API key needed)

### Smart Search — `GET /ask`
Semantic search across all 69K+ articles with **sentiment scoring**. Understands meaning — "AI taking jobs" finds articles about "automation threatens employment" even without matching keywords. Each result includes `sentiment` (bullish/bearish/neutral) and `sentiment_score` (-1 to 1). Falls back to FTS5 keyword search, then web search (70+ engines) if needed.
```bash
curl -s "https://agenttimes.live/ask?q=bitcoin+etf"
curl -s "https://agenttimes.live/ask?q=singapore+news"
curl -s "https://agenttimes.live/ask?q=remote+devops+jobs&limit=20"
curl -s "https://agenttimes.live/ask?q=ukraine+war+latest"
curl -s "https://agenttimes.live/ask?q=federal+reserve+rate"
```
| Param | Default | Description |
|-------|---------|-------------|
| q | required | Search query (replace spaces with +) |
| limit | 10 | Max results (1-50) |

### Trending Stories — `GET /trending`
Story clusters detected across multiple independent sources.
```bash
curl -s "https://agenttimes.live/trending?hours=6"
curl -s "https://agenttimes.live/trending?hours=24&min_sources=5&limit=10"
```
| Param | Default | Description |
|-------|---------|-------------|
| hours | 6 | Lookback window (1-48) |
| min_sources | 3 | Minimum independent sources to qualify (1-20) |
| limit | 20 | Max clusters (1-100) |

### Categories — `GET /news/categories`
List all 55 categories with feed counts and article counts.
```bash
curl -s "https://agenttimes.live/news/categories"
```

### Stats — `GET /stats`
Database statistics: total articles, feeds, categories, healthy/dead feeds, retention.
```bash
curl -s "https://agenttimes.live/stats"
```

### Feed Health — `GET /feeds/health`
Per-feed success/failure rates and response times.
```bash
curl -s "https://agenttimes.live/feeds/health?category=crypto"
```

### Subscribe — `POST /subscribe`
Get webhook notifications when articles matching your query arrive. Great for monitoring topics.
```bash
curl -s -X POST https://agenttimes.live/subscribe \
  -H "Content-Type: application/json" \
  -d '{"query":"bitcoin regulation","category":"crypto","webhook":"https://your-agent.com/notify"}'
```
| Param | Default | Description |
|-------|---------|-------------|
| query | required | Topic to monitor |
| category | all | Filter to specific category |
| webhook | required | URL to receive POST notifications |

Response: `{"success":true,"subscription_id":1}`
Your webhook receives a POST with matching articles (title, url, summary, sentiment) whenever new ones arrive.

### Unsubscribe — `DELETE /subscribe/:id`
```bash
curl -s -X DELETE https://agenttimes.live/subscribe/1
```

### API Docs — `GET /info`
Full endpoint documentation with pricing.
```bash
curl -s "https://agenttimes.live/info"
```

## Paid Endpoints ($0.001 USDC on Base via x402)

### Web Search — `GET /search`
Search the open web via SearXNG's 70+ engines (Google, Bing, DuckDuckGo, Wikipedia, etc.).
```bash
curl -s"https://agenttimes.live/search?q=spacex+launch"
```
| Param | Default | Description |
|-------|---------|-------------|
| q | required | Search query |
| limit | 5 | Max results |
| category | general | Search category: general, news, images, videos, science, files |

### News Feed — `GET /news`
Browse news by category with filtering, date ranges, and deduplication.
```bash
# Browse a category
curl -s"https://agenttimes.live/news?category=crypto&limit=10"

# Search within a category
curl -s"https://agenttimes.live/news?category=jobs&q=remote+sre&limit=20"

# Time-filtered
curl -s"https://agenttimes.live/news?category=ai&since=2026-03-20&limit=50"

# All categories at once
curl -s"https://agenttimes.live/news?category=all&limit=100"
```
| Param | Default | Description |
|-------|---------|-------------|
| category | required | One of 55 categories, or "all" |
| limit | 20 | Max results (1-1000) |
| q | none | Keyword filter within category |
| since | none | ISO date — articles after this time |
| before | none | ISO date — articles before this time |
| dedup | true | Deduplicate similar articles |

## Categories (49)

**News & World:** world, asia, politics, government, defense
**Regional:** europe, middleeast, latam, africa, india, oceania
**Business:** finance, crypto, fintech, ecommerce, realestate, marketing, supplychain, shipping, jobs
**Tech:** tech, ai, engineering, devtools, security, mobile, datascience, robotics, web3
**Science:** science, space, biotech, health, climate, environment, agriculture
**Industry:** energy, automotive, telecom, legal
**Lifestyle:** entertainment, sports, gaming, food, travel, lifestyle, fashion, fitness, film, music, socialmedia
**Other:** startup, education, design, productivity

**Important:** There are NO country-specific categories. For country news, use `/ask?q=COUNTRY+news`.

## Response Format

All endpoints return a consistent envelope:
```json
{"success": true, "count": N, "results": [...]}
```

Error responses:
```json
{"success": false, "error": "Missing param: q"}
```

## x402 Payment Protocol

Paid endpoints use the [x402](https://www.x402.org) HTTP payment standard. When you hit a paid endpoint, you receive a `402 Payment Required` response with payment instructions. Your agent pays $0.001 USDC on Base network per request — no accounts, no subscriptions, just crypto-native micropayments.

**Wallet:** `0x536Eafe011786599d9a656D62e2aeAFcE06a96D1` (Base)

## Tips for Agents

- **Start with `/ask`** — it's free, uses semantic search (meaning-based), and falls back to FTS5 then web search automatically
- **Use `/news` for bulk** — when you need many articles from a specific category with filters
- **Check `/trending` for context** — before answering "what's happening" questions
- **No country categories** — use `/ask?q=japan+news` not `/news?category=japan`
- **Parse JSON directly** — don't pipe to jq (may not be installed)
- **Replace spaces with `+`** in query strings
- **Check the `suggestions` field** when you get 0 results — it tells you related categories and terms
- **Dedup is on by default** — `/news` deduplicates similar headlines automatically
- **Results are recency-boosted** — newer articles rank higher for the same relevance score
- **Three-tier search** — semantic (meaning) → FTS5 (keywords) → web search (SearXNG 70+ engines). Always finds something.
- **Sentiment scoring** — every article has `sentiment` (bullish/bearish/neutral) and `sentiment_score` (-1 to 1). Use this to filter or summarize market mood.
- **Subscribe for alerts** — POST /subscribe with a webhook URL to get notified when matching articles arrive. Great for monitoring breaking news.
