# pylinter-assist — OpenClaw Skill

## Description

Context-aware Python linting with smart pattern heuristics for PR review.

## Usage

```bash
uv run lint-pr [TARGET] [OPTIONS]
```

## Targets

- `pr <number>` — lint all files changed in a GitHub PR
- `staged` — lint git-staged files
- `diff <file>` — lint files from a unified diff file
- `files <path>...` — lint explicit files or directories

## Options

| Flag | Description |
|------|-------------|
| `--format text\|json\|markdown` | Output format (default: markdown) |
| `--config <path>` | Custom `.linting-rules.yml` path |
| `--post-comment` / `--no-post-comment` | Post result as GitHub PR comment |
| `--fail-on-warning` | Also fail on warnings (default: errors only) |

## Installation

```bash
uv sync
```

