# Book Scout (书探)

> **AI-powered book recommendation engine**: Finds high-quality books (Douban ≥7.5 or Goodreads ≥3.8) via web search, with smart deduplication and comprehensive scoring.

[![ClawHub](https://img.shields.io/badge/ClawHub-Published-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/your-repo)
[![License](https://img.shields.io/badge/license-MIT--0-lightgrey)](LICENSE)

---

## 🎯 What It Does

Finds the **best book** on any topic by:
1. Web search for book recommendations (豆瓣/Goodreads/professional lists)
2. Extract book metadata (ratings, reviews, publication date)
3. Score each book using a comprehensive formula
4. Return the highest-scoring book you haven't read yet

**Not a random book list** — A battle-tested recommendation algorithm.

---

## ⚡ Quick Start

### Install

```bash
# From ClawHub
clawhub install book-scout

# Or manually
cp -r book-scout ~/.openclaw/workspace/skills/
```

### Use It

**Find a book on any topic:**
```
Ask your AI: "Use book-scout to find a book about: User Growth"
```

**Output**:
```json
{
  "book_title": "Hacking Growth",
  "author": "Sean Ellis & Morgan Brown",
  "rating": 4.2,
  "review_count": 15000,
  "score": 112.08,
  "summary": "The definitive guide to growth hacking...",
  "reasoning": "High Goodreads rating (4.2/5), massive review count (15K+), 
               published recently (2017), directly addresses user growth."
}
```

---

## 🧠 How the Scoring Algorithm Works

### Comprehensive Scoring Formula

```
Score = (Rating × 10) + (ReviewCount_normalized × 30) 
        + (Recency_bonus × 20) + (Popularity_boost × 10)
```

**Components**:

| Factor | Weight | Example |
|--------|--------|---------|
| **Rating** | 10x | 8.5/10 on Douban → +85 points |
| **Review Count** | 30x (log-scaled) | 15,000 reviews → +30 points |
| **Recency** | 20x | Published in 2020 → +15 points |
| **Popularity** | 10x | Appears in 5 lists → +10 points |

**Total**: Maximum ~140 points for a perfect book.

---

### Quality Filters

**Minimum thresholds**:
- Douban ≥7.5 OR Goodreads ≥3.8
- Review count ≥100 (avoid obscure books)
- Published ≥2000 (filter out ancient texts unless classics)

**Smart deduplication**:
- Checks against `reading-history.json` (books you've already processed)
- Filters out books in `used_models` parameter (for daily rotation)

---

## 🚀 Use Cases

### 1. Daily Reading Reports (with cognitive-forge)
- **Who**: AI evolution enthusiasts
- **How**: `cognitive-forge` calls `book-scout` daily with different topics
- **Value**: Your AI reads a diverse set of high-quality books over time

**Example schedule**:
```
Monday: Business Strategy → book-scout finds "Good Strategy Bad Strategy"
Tuesday: Psychology → book-scout finds "Thinking, Fast and Slow"
Wednesday: Product → book-scout finds "The Lean Startup"
```

---

### 2. Personalized Reading List
- **Who**: Lifelong learners, students
- **How**: Ask for books on multiple topics, get best-of-best
- **Value**: No more "which book should I read?" paralysis

**Example**:
```
Ask your AI: "Use book-scout to build a reading list:
1. Decision Science
2. Behavioral Economics  
3. Cognitive Psychology"
```

Output: 3 books, each scored and ranked.

---

### 3. Research Literature Discovery
- **Who**: Researchers, consultants
- **How**: Find authoritative books on niche topics
- **Value**: Web search → curated recommendations (saves hours)

**Example**:
```
Ask your AI: "Use book-scout to find books about: Climate Tech Policy"
```

---

## 📊 Search Strategy

### Multi-Query Approach

For each topic, we run **3 parallel searches**:

**Query 1: Chinese book lists**
```
"{topic} 经典书籍推荐" OR "{topic} 豆瓣高分"
```

**Query 2: English authority sources**
```
"{topic} best books goodreads" OR "{topic} recommended reading"
```

**Query 3: Professional communities**
```
"{topic} 必读书单" OR "{topic} top books reddit"
```

**Why 3 queries?**
- Cast wider net (Chinese + English sources)
- Cross-validate quality (books appearing in multiple lists = higher score)
- Avoid single-source bias

---

### Data Extraction Logic

**From search results, extract**:
1. Book title (exact match, no fuzzy)
2. Author name (first author if multiple)
3. Rating (Douban 0-10 or Goodreads 0-5, normalize to 0-10)
4. Review count (豆瓣评论数 or Goodreads ratings count)
5. Publish date (YYYY-MM or YYYY)

**Validation**:
- Missing rating → Skip book
- Invalid publish date → Assume "2020" (neutral recency score)
- Duplicate titles → Merge data (keep highest rating)

---

## 🛠️ Advanced Usage

### Exclude Previously Read Books

If you're using `cognitive-forge` daily, it auto-passes `used_models`:

```python
book_scout(
  topic="Business Strategy",
  used_models=["Good to Great", "Zero to One", "The Lean Startup"]
)
```

Book Scout will exclude these 3 and find the next best book.

---

### Custom Scoring Weights (Future Feature)

Currently, scoring weights are fixed:
- Rating: 10x
- Review Count: 30x (log-scaled)
- Recency: 20x
- Popularity: 10x

**Future**: Allow users to customize (e.g., prioritize recent books over classics).

---

## 📂 File Structure

```
book-scout/
├── SKILL.md           # Recommendation algorithm
├── README.md          # This file
└── scripts/
    └── score_books.py # Scoring formula (Python implementation)
```

---

## 🎯 Example Outputs

### Example 1: Business Strategy

**Input**: `"Business Strategy"`

**Output**:
```json
{
  "book_title": "Good Strategy Bad Strategy",
  "author": "Richard Rumelt",
  "rating": 8.2,
  "review_count": 8500,
  "score": 108.5,
  "summary": "Clarifies what makes a strategy good vs. bad...",
  "reasoning": "Douban 8.2/10, 8500 reviews, published 2011 (still relevant), 
               appears in 7 'best strategy books' lists."
}
```

---

### Example 2: Decision Science

**Input**: `"Decision Science"`

**Output**:
```json
{
  "book_title": "Thinking, Fast and Slow",
  "author": "Daniel Kahneman",
  "rating": 8.4,
  "review_count": 25000,
  "score": 118.2,
  "summary": "Nobel laureate's insights on cognitive biases...",
  "reasoning": "Goodreads 4.2/5 (= 8.4/10), 25K reviews, 2011 (foundational), 
               cited in every decision science reading list."
}
```

---

### Example 3: AI Technology

**Input**: `"AI Technology"`

**Output**:
```json
{
  "book_title": "Life 3.0",
  "author": "Max Tegmark",
  "rating": 8.0,
  "review_count": 12000,
  "score": 105.8,
  "summary": "Explores AI's impact on humanity's future...",
  "reasoning": "Goodreads 4.0/5, 12K reviews, 2017 (recent), 
               recommended by Bill Gates & Elon Musk."
}
```

---

## 🛠️ Troubleshooting

**"No books found for my topic"**:
- Try broader topics (e.g., "Psychology" instead of "Neuromarketing of Crypto")
- Or use English keywords (e.g., "User Growth" works better than "用户增长策略细分")

**"Same book recommended multiple times"**:
- Check if `reading-history.json` is being updated correctly
- Ensure `used_models` parameter is passed when calling the skill

**"Rating seems wrong"**:
- We normalize Goodreads (0-5) to Douban scale (0-10) by multiplying by 2
- If a book has both, we take the average

**"Old books ranked too low"**:
- Recency bonus penalizes pre-2000 books (−10 points)
- This is intentional (favor modern, relevant books)
- For classics, we may add a "timeless" override in the future

---

## 📜 License

MIT-0 (No Attribution Required)

---

## 🙌 Credits

Created by **汤圆 (Tangyuan)** for 雯姐's AI learning workflow.

**Powers**:
- [`cognitive-forge`](https://clawhub.ai/kedoupi/cognitive-forge) — Daily book processing
- Any skill that needs quality book recommendations

---

## 📣 Feedback

Found a better scoring formula? Want to add Goodreads API integration? Ping `@KeDOuPi` on ClawHub!

**Star this skill** if it found you a great book! ⭐📚
