---
name: pdf-to-latex
description: "PDF to LaTeX - convert PDF documents (especially academic papers) to LaTeX format using MinerU. Use for re-editing or re-typesetting PDFs in LaTeX."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# PDF to LaTeX

Convert PDF documents to LaTeX format using MinerU. Best suited for academic papers and documents with formulas or complex layouts.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Convert PDF to LaTeX (requires token)
mineru-open-api extract paper.pdf -f latex -o ./out/

# With VLM model for better accuracy on complex layouts
mineru-open-api extract paper.pdf -f latex --model vlm -o ./out/

# From arXiv URL
mineru-open-api extract https://arxiv.org/pdf/2309.10918 -f latex -o ./out/
```

## Authentication

Token required:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .pdf (local file or URL)
- Output format: LaTeX (`-f latex`)
- LaTeX output requires `extract` with token — not available in `flash-extract`
- Use `--model vlm` for papers with complex math, tables, or multi-column layouts
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- LaTeX output (`-f latex`) is only available via `extract` with token
- `--model vlm` gives higher accuracy but may have rare hallucination risk; use `pipeline` for guaranteed fidelity
- Output goes to stdout by default; use `-o <dir>` to save to a file
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
