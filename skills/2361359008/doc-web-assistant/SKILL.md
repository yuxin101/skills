---
name: doc-web-assistant
description: "Use native web_fetch content to build a local documentation knowledge base, query it, extract command plans, and prepare Doc Executor workflows."
metadata:
---

# Doc Web Assistant

## Purpose

This skill lets OpenClaw treat a documentation website as a local structured knowledge base.

## Read When

- Crawling documentation websites into JSON
- Building a local offline doc knowledge base
- Answering questions from documentation content
- Turning documentation steps into terminal command plans
- Preparing safe command execution from doc pages

## Runtime Requirements

- Python
- pip

## Allowed Tools

- `Bash(python:*)`
- `Bash(py:*)`
- `Bash(pip:*)`

It supports three stages:

1. Use OpenClaw native `web_fetch` to obtain page content.
2. Import fetched content into local JSON files.
3. Query the local JSON store by natural language.
4. Build an execution plan from matched documentation commands.

The acquisition path is:

1. Use native `web_fetch` first.
2. Save or pass the fetched content into this skill via `import`.

This skill is designed for documentation assistant workflows such as:

- Installing software from official docs
- Extracting build commands from long doc pages
- Creating terminal-ready command plans from documentation
- Using one prompt to let OpenClaw read docs before acting

## Skill files

- `doc_web_assistant.py`: importer, crawler, indexer, retriever, planner
- `requirements.txt`: Python dependencies
- `SKILL.md`: skill instructions for OpenClaw

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If OpenClaw runs inside the skill directory, this is enough.

If you need an explicit command with absolute path, use:

```bash
python doc_web_assistant.py --help
```

## Core commands

### 1. Import fetched content into JSON

Preferred path for OpenClaw.

First, use native `web_fetch` to get the document content from the target URL.
Then save that content to a local file such as `./fetched_doc.md` or `./fetched_doc.html`.
Finally import it with:

```bash
python doc_web_assistant.py import --input "./fetched_doc.md" --source-url "https://example.com/docs/install" --out "./doc_store"
```

You may also import HTML directly:

```bash
python doc_web_assistant.py import --input "./fetched_doc.html" --source-url "https://example.com/docs/install" --out "./doc_store" --format html
```

Output files will be created under `./doc_store`:

- `manifest.json`
- `chunks.json`
- `pages/page_0001.json`

### 2. Query imported documentation

```bash
python doc_web_assistant.py query --db "./doc_store" --query "如何安装 ARMv9 优化版 llama.cpp" --top-k 5
```

This returns the most relevant sections and code blocks from the local store.

### 3. Build a doc-grounded command plan

```bash
python doc_web_assistant.py plan --db "./doc_store" --query "根据文档给我安装 KleidiAI 优化版 llama.cpp 的命令" --top-k 5
```

This returns:

- relevant doc chunks
- extracted commands
- risk classification for each command

## Recommended OpenClaw workflow

When the user asks a documentation-driven task, follow this sequence.

### Workflow A: First-time doc import with native fetch

Use when the target documentation is not yet available locally.

1. Use OpenClaw native `web_fetch` to fetch `<DOC_URL>`.
2. Save the fetched content to a temporary file.
3. Import that file into the local doc store.

```bash
python doc_web_assistant.py import --input "./fetched_doc.md" --source-url "<DOC_URL>" --out "./doc_store"
```

Then inspect results with:

```bash
python doc_web_assistant.py query --db "./doc_store" --query "<USER_TASK>" --top-k 5
```

### Workflow B: Answer from docs

Use when the user wants explanation only.

```bash
python doc_web_assistant.py query --db "./doc_store" --query "<USER_QUESTION>" --top-k 5
```

Answer from the matched chunks and cite the source URL when possible.

### Workflow C: Plan terminal operations from docs

Use when the user wants executable steps.

```bash
python doc_web_assistant.py plan --db "./doc_store" --query "<USER_TASK>" --top-k 5
```

Then convert returned commands into an ordered plan.

### Workflow D: Execute after planning

Use only after a plan is built.

- Execute `low` risk commands directly after checking environment.
- Review `medium` risk commands before execution.
- Never auto-execute `high` risk commands without explicit user confirmation.

## Operational policy for OpenClaw

When using this skill, OpenClaw should behave as follows.

### If the user says

- "读取这个文档并告诉我怎么做"
- "根据这个网址里的安装文档帮我执行"
- "把这个文档导入成本地 JSON"
- "从这个网页里抽取命令"

### Then OpenClaw should

1. Determine whether the task needs import, query, or plan.
2. If the task references a URL and no local store exists, use native `web_fetch` first.
3. Import the fetched content with `python doc_web_assistant.py import ...`.
4. Use `query` for explanation tasks.
5. Use `plan` for terminal-execution tasks.
6. Present or execute commands according to risk level.
7. Prefer commands extracted from documentation instead of inventing commands.
8. If native `web_fetch` returns incomplete or noisy content, say so explicitly before planning execution.

## JSON schema overview

### `manifest.json`

Contains:

- root URL
- generation time
- page count
- page listing

### `pages/page_xxxx.json`

Contains per-page structured content:

- source URL
- title
- summary
- sections
- code blocks
- extracted commands
- crawl depth

### `chunks.json`

Contains flattened retrieval chunks for:

- section text
- code block text
- extracted commands

## Example: build a local doc assistant

### Native fetch + import

1. Use native `web_fetch` on:

- `https://docs.radxa.com/en/orion-o6/app-development/llama.cpp`

2. Save the fetched content to `./radxa_llama_doc.md`

3. Import it:

```bash
python doc_web_assistant.py import --input "./radxa_llama_doc.md" --source-url "https://docs.radxa.com/en/orion-o6/app-development/llama.cpp" --out "./radxa_llama_docs"
```

### Query

```bash
python doc_web_assistant.py query --db "./radxa_llama_docs" --query "KleidiAI 编译参数" --top-k 3
```

### Plan

```bash
python doc_web_assistant.py plan --db "./radxa_llama_docs" --query "根据文档生成安装和编译命令" --top-k 5
```

## Safety rules

- Do not assume extracted commands are valid for every OS or architecture.
- Always check whether the doc targets Linux, Windows, ARM64, x86_64, or Docker.
- Treat package installation, build, download, service, and docker commands as at least medium risk.
- Treat delete, format, reboot, permission-change, and destructive system commands as high risk.
- If the documentation is incomplete, say so clearly instead of guessing.

## Notes

- This skill works best on documentation pages with clear headings, paragraphs, lists, and code blocks.
- It is intended for documentation websites rather than arbitrary web apps.
- Native `web_fetch` is the acquisition method for anti-bot or dynamically rendered sites.
- The importer stores structured content for local reuse, which makes later prompts faster.

## Troubleshooting

- If `pip` is missing, install Python with pip first.
- If native `web_fetch` succeeds but the imported structure is weak, save the fetched content as Markdown and import that Markdown file.
- If the page is heavy on JavaScript rendering, use a pre-rendered documentation URL when possible.
- If query returns weak matches, use a more specific prompt including product name, component name, and action.

## Reporting issues

If the skill logic is unclear, update `SKILL.md` and keep the command examples aligned with the Python script.
