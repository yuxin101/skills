---
title: "AI News Daily Brief - Sources"
---
## Source Whitelist Policy

The following sources are the only approved sources for this skill.

The skill must not cite, summarize, or rely on any source outside this whitelist unless the user explicitly requests broader coverage.

Rules:
1. Every final news item must map to at least one approved source in this file.
2. If supporting context is found elsewhere but cannot be matched back to an approved source, it must not appear in the final brief.
3. White-listed sources should be used as the primary basis for facts, dates, and links in the final output.
4. Non-whitelisted sources may not be used as substitutes for missing approved-source coverage.


---

# Supported Source Entry Points

This file defines the supported source entry points for the AI News Daily Brief skill.

The skill should prioritize these sources and should not expand to unrelated sources unless the user explicitly requests it.

---

## 1. Chinese AI / Tech Media

### AIBase
- Type: Chinese AI news / aggregation media
- Entry URL: https://news.aibase.com/zh/daily
- Search Language: Chinese first, with English entity names when useful
- Notes:
  - Good for fast news discovery, product releases, and industry updates
  - Useful for spotting trending stories early
  - Lower priority than official sources and Reuters when the same event appears elsewhere

### 36Kr AI
- Type: Chinese tech / business media
- Entry URL: https://36kr.com/
- Search Language: Chinese first, with English company and product names preserved when needed
- Notes:
  - Useful for AI startup news, industry analysis, business moves, and commercialization
  - Stronger on business and market framing than pure technical depth

### 机器之心
- Type: Chinese AI vertical media
- Entry URL: https://www.jiqizhixin.com/
- Search Language: Chinese first, with technical English keywords when helpful
- Notes:
  - Useful for model progress, technical developments, research coverage, and conference-related updates
  - Higher value for technical and industry trend interpretation

### 量子位
- Type: Chinese AI / tech media
- Entry URL: https://www.qbitai.com/
- Search Language: Chinese first, with English entity names preserved when useful
- Notes:
  - Useful for AI product news, startup ecosystem coverage, and fast-moving industry stories
  - Often good for tracking broad AI industry sentiment and market momentum

---

## 2. Global Media

### Reuters AI
- Type: Global hard news / wire service
- Entry URL: https://www.reuters.com/technology/artificial-intelligence/
- Search Language: English first
- Notes:
  - High-priority global media source
  - Strong for corporate moves, regulation, legal developments, funding, M&A, and global market impact
  - Preferred over most media sources when no official source is available

### The Verge AI
- Type: Global technology and product media
- Entry URL: https://www.theverge.com/ai-artificial-intelligence
- Search Language: English first
- Notes:
  - Strong for AI product updates, user-facing features, platform competition, and major consumer product developments
  - Useful for product-manager-oriented interpretation

### WIRED AI
- Type: Global technology and ideas media
- Entry URL: https://www.wired.com/tag/artificial-intelligence/
- Search Language: English first
- Notes:
  - Useful for deeper stories about AI safety, culture, ethics, risk, and social implications
  - Often valuable for broader framing rather than fastest news discovery

### VentureBeat AI
- Type: Global enterprise tech media
- Entry URL: https://venturebeat.com/category/ai/
- Search Language: English first
- Notes:
  - Useful for enterprise AI, agents, tools, infrastructure, data, and business adoption stories
  - Strong for commercial and implementation-oriented coverage

---

## 3. Official First-Party Sources

### Google DeepMind Blog
- Type: Official source
- Entry URL: https://deepmind.google/discover/blog/
- Search Language: English first
- Notes:
  - Use as the primary source for Google DeepMind announcements, research updates, and product-related breakthroughs

### OpenAI News
- Type: Official source
- Entry URL: https://openai.com/news/
- Search Language: English first
- Notes:
  - Use as the primary source for OpenAI product launches, model announcements, API updates, and official company statements

### Anthropic Newsroom
- Type: Official source
- Entry URL: https://www.anthropic.com/news
- Search Language: English first
- Notes:
  - Use as the primary source for Anthropic company announcements, Claude-related releases, partnerships, and policy statements

### Anthropic Engineering
- Type: Official source
- Entry URL: https://www.anthropic.com/engineering
- Search Language: English first
- Notes:
  - Use for technical engineering details, implementation notes, infrastructure changes, and technical writeups from Anthropic

### NVIDIA Blog
- Type: Official source
- Entry URL: https://blogs.nvidia.com/
- Search Language: English first
- Notes:
  - Use as the primary source for NVIDIA announcements on AI infrastructure, chips, inference systems, partnerships, and platform developments

---

## 4. Source Priority Order

When the same event appears in multiple sources, use the following order of preference:

1. Official first-party source
2. Reuters
3. The Verge / WIRED / VentureBeat
4. 机器之心 / 量子位 / 36Kr AI
5. AIBase

If multiple official sources are involved in the same story, prefer the source directly responsible for the announcement.

---

## 5. Usage Guidance

- Use source-specific search language whenever possible.
- Prefer official source pages for product, model, API, and corporate announcements.
- Use Reuters for hard-news confirmation when official detail is limited.
- Use media sources to supplement context, interpretation, and business implications.
- Do not treat low-information reposts as separate news items.
- Do not expand beyond the approved source list unless explicitly requested by the user.
