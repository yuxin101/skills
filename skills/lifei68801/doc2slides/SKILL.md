---
name: doc2slides
version: 3.0.0
description: "Convert PDF, Word, and Markdown documents into professional PowerPoint slides with 18+ layout types and smart layout matching. Use when: user wants to create slides from a document or convert content to PPT."
license: MIT-0
author: lifei68801
metadata:
  openclaw:
    requires:
      bins: ["python3", "pip3"]
      env:
        optional:
          - OPENAI_API_KEY
          - ZHIPU_API_KEY
          - DEEPSEEK_API_KEY
    permissions:
      - "file:read"
      - "file:write"
    behavior:
      modifiesLocalFiles: true
      network: optional
      telemetry: none
      credentials: none
---

# Doc2Slides

Turn documents into professional PowerPoint slides.

## What It Does

- **18+ Layouts**: Dashboard, Timeline, Flow Chart, Pyramid, Comparison, Matrix, and more
- **Smart Matching**: Picks the best layout per section automatically
- **LLM Enhancement**: Optional AI-powered analysis for better layout decisions
- **High Quality**: 3x resolution with charts and data visualizations
- **Batch Mode**: Handles long documents (10+ pages) via split generation

## Setup

```bash
pip3 install python-pptx playwright requests
playwright install chromium
```

LLM enhancement is optional. When enabled, it uses one of these env vars (all optional):
- `OPENAI_API_KEY` — OpenAI compatible API
- `ZHIPU_API_KEY` — Zhipu AI API
- `DEEPSEEK_API_KEY` — DeepSeek API

Without any API key set, the skill runs in template-only mode (no LLM calls, no network).

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/doc2slides/scripts
python3 workflow.py --input /path/to/document.pdf --output slides.pptx
```

## Before You Start

Ask the user: **"有什么特殊要求吗？比如风格、页数、重点内容、配色偏好等。直接说需求就行，也可以说'按默认来'。"**

Any instruction the user gives is applied via `--instruction`.

## How It Works

1. **Read** — Load document content (PDF, DOCX, Markdown)
2. **Analyze** — Identify structure and key points
3. **Match** — Select layout for each section
4. **Build** — Generate inline-styled HTML slides (SVG charts, no external JS)
5. **Render** — Chromium screenshots at 3x resolution
6. **Export** — Assemble PNG images into PPTX

## Architecture

All rendering uses inline CSS + SVG for charts. No external CDN, no Tailwind, no Chart.js — everything is self-contained HTML.

- `workflow.py` — Main orchestrator
- `llm_generate_html.py` — LLM-powered HTML slide generation
- `llm_adapter.py` — Multi-provider LLM adapter (OpenAI, Zhipu, DeepSeek, Ollama)
- `smart_layout_matcher.py` — Automatic layout selection
- `svg_charts.py` / `svg_charts_enhanced.py` — Pure SVG chart rendering
- `html2png_batch.py` — Playwright screenshot pipeline
- `png2pptx.py` — Image-to-PPTX assembly

## Tips

- Documents with clear headings and bullet points work best
- Shorter documents (1-20 pages) produce optimal results
- All source code is included for transparency and review

## License

MIT-0
