# IELTS Reading Review 雅思阅读复盘助手

> Finish a reading passage, hand it to AI, get a complete review — error analysis, synonym tracking, vocabulary tagging, and mistake pattern detection, all in one go.

做完阅读题，丢给 AI，自动出复盘笔记——错题拆解、同义替换积累、考点词标注、易错模式追踪，一步到位。

## Features

### 🎯 Per-question Error Analysis
Locates source sentences, maps synonyms, and classifies the error cause into 8 categories (synonym failure, NOT GIVEN/FALSE confusion, over-inference, stem-word duplication, grammar misread, incomplete option matching, vocabulary gap, carelessness).

### 🔄 Synonym Accumulation Table
Extracts synonym pairs from each passage and builds a running collection over time. Only includes question-relevant synonyms.

### 📝 Vocabulary Tagging
Tags every unknown word with IELTS frequency rating based on:
- **Liu Hongbo's 538 IELTS Keywords** (Category 1 ⭐⭐⭐ / Category 2 ⭐⭐ / Category 3 ⭐)
- **COCA 5000** for general English frequency

### 💡 Recurring Mistake Tracker
Detects error patterns across passages — like always confusing NOT GIVEN with FALSE, or copying words already in the question stem.

### 📄 Professional HTML Review Notes
Generates beautifully formatted review documents with optional PDF export (via Puppeteer).

## How to Use

1. Install the Skill
2. Finish an IELTS Academic Reading passage
3. Send the passage + answer key + your answers to AI
4. Say **"帮我复盘"** or **"IELTS reading review"**

## File Structure

```
ielts-reading-review/
├── SKILL.md                          # Skill definition
├── README.md                         # This file
├── assets/
│   └── review-template.html          # HTML template with full CSS
├── references/
│   ├── error-taxonomy.md             # 8-category error classification
│   ├── 538-keywords-guide.md         # IELTS vocabulary rating guide
│   └── review-style-guide.md         # Writing & formatting conventions
└── scripts/
    └── generate-pdf.js               # PDF generation (Node.js + puppeteer-core)
```

## Error Analysis Methodology

### T/F/NG Three-Step Method
1. **Find the topic** — Does the passage discuss this? → If NO → **NOT GIVEN**
2. **Find the stance** — Agrees or contradicts? → **TRUE** / **FALSE**
3. **Verify** — "Can I point to the exact sentence?" If not → likely **NOT GIVEN**

### Fill-in-the-blank
Never repeat words already in the question stem. Re-read the complete sentence after filling in.

### Multiple Choice
Every keyword in a chosen option must find correspondence in the passage. "Roughly related" ≠ "correct answer".

## Who It's For

IELTS candidates targeting band 6–7+ in Academic Reading, especially those who:
- Struggle with review efficiency
- Keep making the same mistakes
- Want systematic vocabulary building tied to real Cambridge tests

## Requirements

- An AI agent that supports SKILL.md (e.g., OpenClaw, Claude Code, WorkBuddy)
- For PDF export: Node.js + puppeteer-core + Chrome/Chromium installed locally

## License

MIT-0
