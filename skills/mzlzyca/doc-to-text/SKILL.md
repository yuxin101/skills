---
name: doc-to-text
description: "Doc to Text - extract plain readable text from Word (.doc/.docx) documents using MinerU. Output is Markdown (the closest plain-text format MinerU supports)."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Doc To Text

Extract plain readable text from Word (.doc/.docx) documents using MinerU. MinerU outputs Markdown, which is the closest format to plain text it supports.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Extract text from .docx to stdout (no token required)
mineru-open-api flash-extract report.docx

# Save to file
mineru-open-api flash-extract report.docx -o ./out/

# Extract .doc (requires token)
mineru-open-api extract report.doc -o ./out/

# JSON output contains plain text fields (requires token)
mineru-open-api extract report.docx -f json -o ./out/
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
- `.docx`: supports `flash-extract` (no token, Markdown output to stdout)
- `.doc`: requires `extract` with token
- For truly plain text: use `extract -f json` and read the text fields from the JSON output
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- MinerU does not have a `-f text` option; Markdown is the closest to plain text
- `.doc` requires `extract` with token; `.docx` works with `flash-extract`
- Output goes to stdout by default; use `-o <dir>` to save to a file or directory
- All progress/status messages go to stderr; document content goes to stdout
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
