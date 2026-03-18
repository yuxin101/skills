---
title: "AI News Daily Brief - Search Rules"
---

# Search Rules and Deduplication Rules

This file defines how the skill should search, filter, merge, and rank AI news items for the daily brief.

The goal is to maximize signal quality, reduce duplication, and improve consistency.

---

## 1. Search Scope

The default time range is the last 24 hours.

The skill should search only within the approved sources listed in `sources.md`.

Do not expand beyond the approved source list unless the user explicitly requests broader coverage.

---

## 2. Search Language Rules

### For Chinese sources
Applicable sources:
- AIBase
- 36Kr AI
- 机器之心
- 量子位

Rules:
1. Search primarily in Chinese.
2. Use Chinese topic phrases, event summaries, and translated subject terms.
3. Preserve important English company names, product names, and technical terms when helpful, such as:
   - OpenAI
   - Anthropic
   - NVIDIA
   - Google DeepMind
   - Agent
   - RAG
   - API
4. Prefer Chinese search phrasing for business, industry, and product news.
5. When a topic is highly cross-border, use bilingual keyword expansion as needed.

Examples:
- OpenAI 发布 新模型
- 英伟达 AI 芯片 推理
- 谷歌 DeepMind 多模态 模型
- 智能体 办公 自动化
- 企业 AI 知识库 RAG

### For global and official sources
Applicable sources:
- Reuters
- The Verge
- WIRED
- VentureBeat
- Google DeepMind Blog
- OpenAI News
- Anthropic Newsroom
- Anthropic Engineering
- NVIDIA Blog

Rules:
1. Search primarily in English.
2. Use original English names for companies, products, models, APIs, and technical terms.
3. Map Chinese user intent into English search queries when needed.
4. Use domain-specific technical wording where appropriate.

Examples:
- OpenAI new model release
- Anthropic Claude enterprise update
- NVIDIA inference chip launch
- AI agent workflow automation
- RAG enterprise deployment
- DeepMind multimodal model

### Cross-language event rules
1. For major stories with likely coverage in both Chinese and English sources, try both Chinese and English query variants.
2. Merge duplicated results across languages into one event.
3. Prefer the most authoritative primary source, but use cross-language coverage for context if helpful.

---

## 3. Inclusion Rules

Include only stories that are directly related to AI and have real informational value.

Priority topics:
- model launches and major upgrades
- multimodal models, reasoning models, agent systems
- API and platform changes
- AI products and major feature releases
- AI agents and workflow automation
- enterprise AI, knowledge bases, RAG, copilots
- chips, GPUs, inference systems, data centers, compute
- major partnerships, acquisitions, funding, and business strategy moves
- policy, regulation, safety, copyright, governance
- research with clear industry or product relevance

---

## 4. Exclusion Rules

Do not include:
- weakly related general tech news
- vague opinion pieces without concrete developments
- promotional or marketing-heavy content
- reposts with no added information
- trivial updates with little industry significance
- rumor-only content without credible basis
- duplicate stories already represented elsewhere in the brief

If relevance or value is unclear, exclude the item.

---

## 5. Deduplication Rules

Before drafting the brief, deduplicate all overlapping reports.

Rules:
1. Treat all coverage of the same event as one story.
2. Use the most authoritative and information-rich source as the primary source.
3. Record other strong sources as supplementary sources.
4. Merge repeated media coverage into one unified event summary.
5. Do not repeat the same event in multiple categories.
6. Do not keep separate entries just because different outlets use different headlines.

Example:
If OpenAI announces a new feature and Reuters, The Verge, and 36Kr all report it:
- Primary source: OpenAI News
- Supplementary sources: Reuters, The Verge, 36Kr
- Final output: one merged story

---

## 6. Source Priority Rules

When multiple sources cover the same event, use this priority order:

1. Official first-party source
2. Reuters
3. The Verge / WIRED / VentureBeat
4. 机器之心 / 量子位 / 36Kr AI
5. AIBase

If the official source and media framing differ:
- prefer the official source for factual claims
- use media coverage only for interpretation or additional context

---

## 7. Ranking Rules

The skill should rank stories by importance, not by publication time alone.

Signals that increase importance:
- official product or model release
- major API or capability update
- broad market or industry impact
- strategic funding, acquisition, or partnership
- infrastructure or compute implications
- regulatory or policy significance
- direct relevance to enterprise AI, product strategy, or competitive dynamics

Signals that lower importance:
- minor feature tweaks
- repetitive commentary
- weak evidence
- shallow repost-style coverage
- stories with low product or industry implications

---

## 8. Target Volume Rules

Prefer to keep 12–15 curated news items in the daily brief.

If there are fewer genuinely high-value stories, the brief may be reduced to 8–10 items.

Do not add filler or weakly related stories just to meet a target count.

If there are more than 15 strong candidate stories, keep only the most important ones.

In exceptional high-volume news cycles, the brief may expand up to 20 items, but only if quality remains high.

Always prioritize:
- information quality
- signal density
- readability
- usefulness to the end user

---

## 9. Final Review Rules

Before final output, verify:
1. duplicates were merged
2. all items are clearly AI-related
3. official and media sources are clearly distinguished
4. each item has a valid source reference
5. ranking reflects true importance
6. weak content has been filtered out
7. summaries explain why the story matters
8. final output language is Simplified Chinese unless the user explicitly requests another language


---

## 10. Publication Time Verification Rules

Before including any story in the daily brief, the skill must verify the original publication time from the source page itself.

Required procedure:
1. Open the original source page.
2. Locate the explicit publication date/time on the page.
3. Normalize the date/time to a consistent reference timezone.
4. Check whether the story falls within the last 24 hours.
5. Only then may the story be included in the final brief.

Strict rules:
- Do not use search result snippets alone as proof of recency.
- Do not infer recency from topic relevance, URL patterns, page ordering, or “latest” labels.
- Do not treat “recent”, “updated”, “this month”, or “March 2026” as sufficient evidence.
- If the publication date/time cannot be confirmed precisely, exclude the story.
- If the page is an evergreen page, archive page, tag page, topic page, or rolling update page without a clear timestamp for the specific story, exclude it unless a specific dated article page is opened and verified.

Examples of items to exclude:
- old articles resurfacing in search
- archive pages and topic hubs
- release-note hubs without clear post-level timing
- pages labeled only with approximate time such as “recently”