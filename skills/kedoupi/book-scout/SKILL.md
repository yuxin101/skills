---
name: book-scout
description: Expert book recommendation engine via web search. Finds high-quality books (Douban ≥7.5 or Goodreads ≥3.8) based on topic, with deduplication and comprehensive scoring. Use when you need to recommend books for reading tasks, skill building, or research.
---

# Book Scout

Expert book recommendation engine that finds high-quality books via web search.

## When to Use

- Recommending books for a specific topic (e.g., "user growth", "decision science")
- Finding books for reading tasks (morning/noon/evening reading reports)
- Building a reading list for skill development
- Need to avoid previously analyzed books

## Input

- **topic** (required): Subject/theme (e.g., "用户增长", "决策科学", "AI技术")
- **used_models** (optional): Array of previously analyzed books to exclude

## Output

JSON object with the highest-scoring book:

```json
{
  "book_title": "书名",
  "author": "作者",
  "author_nationality": "国籍或'未知'",
  "publish_date": "YYYY-MM或YYYY",
  "rating": 8.9,
  "review_count": 15000,
  "score": 112.08,
  "summary": "100字核心简介",
  "reasoning": "推荐理由"
}
```

## Core Workflow

### Step 1: Search Strategy

**Search Query Construction** (high information density):

```
"{topic} 经典书籍推荐" OR "{topic} 必读书单" OR "{topic} 豆瓣高分"
```

**Example**:
- Topic: "用户增长"
- Queries:
  - "用户增长 经典书籍推荐"
  - "user growth best books goodreads"
  - "product growth必读书单 豆瓣高分"

**Execute**: Use `web_search` tool to fetch top 3-5 high-quality results (focus on book list articles, professional communities).

### Step 2: Data Extraction

**Extract minimum 3 candidate books** from search results.

**Required Fields**:
- book_title
- author
- rating
- review_count
- publish_date
- author_nationality

**Deduplication (Priority #1)**:
- Compare extracted books against `used_models` immediately
- If match found → discard, do not proceed to scoring

**Missing Data Handling (Strict Timeout Protocol)**:
- **Batch Search**: If 2 or more books lack rating/review_count, DO NOT search them individually. You MUST combine them into one single web_search query (e.g., "{book1} {book2} 豆瓣评分") to minimize tool calls.
- **Fast Fail & Time-Box**: You are allowed MAXIMUM 1 secondary search attempt for missing data. If the search takes too long (e.g., over 5 seconds) or fails, DO NOT retry.
- **Discard Rule**: After 1 search attempt, if a book STILL lacks a rating or review_count, DROP IT immediately from the candidate list. Do not proceed to score it.
- **publish_date missing**: Default to 2020.
- **author_nationality missing**: Output "未知" (NEVER fabricate from model memory).

### Step 3: 3D Scoring Algorithm

**⚠️ Execution Action**: Collect ALL surviving candidate books (those with complete or successfully patched data) into a single JSON array. You MUST pass this entire array to `scripts/score_books.py` AT ONCE for batch scoring. Do not score them one by one. The script will return the sorted list.

(If pure LLM without script, output CoT for all books before sorting).

**Formula**:
```
Total Score = (Base Quality + Popularity Bonus) × Recency Multiplier
```

**A. Base Quality**:
```
Base = rating × 10
If review_count < 100: Base = Base × 0.8 (small sample penalty)
```

**B. Popularity Bonus**:
```
Bonus = log₁₀(review_count) × 2
(capped to prevent bestseller spam dominance)
```

**C. Recency Multiplier** (based on publish_date):
```
Published within 2 years (2024-now):  × 1.2
Published 3-5 years ago (2021-2023):  × 1.0
Published 5+ years ago (≤2020):       × 0.8
```

**Example Calculation**:
```
Book: 《增长黑客》
- Rating: 8.5, Review Count: 10000, Publish: 2015
- Base = 8.5 × 10 = 85
- Bonus = log₁₀(10000) × 2 = 4 × 2 = 8
- Recency = 0.8 (old book)
- Total = (85 + 8) × 0.8 = 74.4
```

### Step 4: Output

Return the **highest-scoring book** in the structured JSON format.

**Reasoning Field Must Include**:
- Score justification
- Recency consideration
- Author background (if known)

**Example**:
```
"2024年硅谷最新实战派干货，评分8.9且有1.5万真实评价，作者是前Facebook增长负责人"
```

## Fallback & Error Handling

### Scenario 1: Web Search Failure (Network Error)

**Action**:
- Retry with 2-3 second interval
- Max retries: 3 times

**Termination**:
If all 3 attempts fail, return:
```json
{
  "error": "网络连接连续 3 次超时，无法获取最新书单数据，请稍后重试。"
}
```

### Scenario 2: Topic Too Niche (No Valid Results)

**Action**:
- Fallback to broader search: `"{topic} 经典必读 豆瓣高分"`
- Remove long-tail professional keywords

**Termination**:
If broad search also fails, return:
```json
{
  "error": "该主题下未找到具备足够评价数据的经典书籍，请尝试更换更宽泛的主题或行业大词。"
}
```

## Quality Filters

**Minimum Standards**:
- Douban rating ≥ 7.5 OR Goodreads rating ≥ 3.8
- At least 2 authoritative sources mention it (if rating unavailable)

**Note**: No minimum review count filter — let the scoring algorithm handle it. Books with few reviews get a 0.8× penalty in Step 3, so if a book has 9.5 rating but only 50 reviews, it still needs to earn its place through exceptional quality.

**Exclusions**:
- Books with "21天", "速成", "一本通" in title (get-rich-quick books)
- Marketing-heavy books (no substance)

## Implementation Notes

**Code vs. LLM**:
- Complex math (logarithms, conditionals) → use `scripts/score_books.py`
- Data extraction & reasoning → LLM
- Scoring calculation → code (deterministic, fast)

**Search Result Parsing**:
- Focus on structured content (book lists, community threads)
- Ignore ads and promotional content
- Prioritize Douban/Goodreads/Zhihu/Reddit sources

## Example Usage

**Input**:
```
Topic: "用户增长"
Used Models: ["《精益创业》", "《从0到1》"]
```

**Process**:
1. Search: "用户增长 经典书籍推荐"
2. Extract: [《增长黑客》, 《上瘾》, 《跨越鸿沟》]
3. Deduplicate: All 3 pass (not in used_models)
4. Score:
   - 《增长黑客》: 74.4
   - 《上瘾》: 72.9
   - 《跨越鸿沟》: 68.9
5. Select: 《增长黑客》(highest score)

**Output**:
```json
{
  "book_title": "《增长黑客》",
  "author": "肖恩·埃利斯",
  "author_nationality": "美国",
  "publish_date": "2015-04",
  "rating": 8.5,
  "review_count": 10000,
  "score": 74.4,
  "summary": "增长黑客方法论：低成本获客、数据驱动迭代、病毒式传播。Dropbox、Airbnb等硅谷公司的增长实战案例，适用于产品冷启动和用户增长。",
  "reasoning": "评分8.5且有1万真实评价，作者是增长黑客概念提出者、Dropbox早期增长负责人，虽是2015年出版但增长黑客方法论至今仍是用户增长的核心框架"
}
```
