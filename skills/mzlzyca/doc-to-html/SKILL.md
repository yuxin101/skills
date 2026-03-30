---
name: doc-to-html
description: "Doc to HTML - convert Word (.doc/.docx) documents to HTML using MinerU. Use when you need HTML output from a Word file."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Doc To HTML

Convert Word (.doc/.docx) documents to HTML using MinerU.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Convert .docx to HTML (requires token)
mineru-open-api extract report.docx -f html -o ./out/

# Convert .doc to HTML (requires token)
mineru-open-api extract report.doc -f html -o ./out/

# With language hint
mineru-open-api extract report.docx -f html --language en -o ./out/
```

## Authentication

Token required:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .doc, .docx (local file or URL)
- Output format: HTML (`-f html`)
- HTML output requires `extract` with token — not available in `flash-extract`
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- HTML output (`-f html`) is only available via `extract` with token
- Output goes to stdout by default; use `-o <dir>` to save to a file
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
