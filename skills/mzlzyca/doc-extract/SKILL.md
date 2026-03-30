---
name: doc-extract
description: "Doc Extract - extract text and content from Word (.doc/.docx) documents to Markdown using MinerU. Use when reading or parsing Word files."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Doc Extract

Extract text and content from Word (.doc/.docx) files to Markdown using MinerU.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Quick extraction from .docx (no token required)
mineru-open-api flash-extract report.docx

# Save to directory
mineru-open-api flash-extract report.docx -o ./out/

# Extract .doc file (requires token)
mineru-open-api extract report.doc -o ./out/

# Extract with language hint
mineru-open-api extract report.docx --language en -o ./out/
```

## Authentication

No token needed for `flash-extract` on `.docx`. Token required for `.doc` and `extract`:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .doc, .docx (local file or URL)
- `.docx`: supports `flash-extract` (no token, max 10 MB / 20 pages) and `extract`
- `.doc`: requires `extract` with token
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (e.g. `1-10`)

## Notes

- `.doc` requires `extract` with token; `.docx` works with `flash-extract` for quick extraction
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
