---
name: algebra
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [algebra, tool, utility]
description: "Solve equations, simplify expressions, and factor polynomials. Use when doing algebra homework, checking proofs, or plotting functions."
---

# Algebra

Algebra v2.0.0 — a versatile utility toolkit for recording, tracking, and managing algebra-related tasks from the command line. Log computations, compare results, generate reports, and export your work in multiple formats.

## Commands

| Command | Description |
|---------|-------------|
| `algebra run <input>` | Record a run entry (no args = show recent runs) |
| `algebra check <input>` | Record a check entry (no args = show recent checks) |
| `algebra convert <input>` | Record a conversion entry (no args = show recent conversions) |
| `algebra analyze <input>` | Record an analysis entry (no args = show recent analyses) |
| `algebra generate <input>` | Record a generation entry (no args = show recent generations) |
| `algebra preview <input>` | Record a preview entry (no args = show recent previews) |
| `algebra batch <input>` | Record a batch entry (no args = show recent batches) |
| `algebra compare <input>` | Record a comparison entry (no args = show recent comparisons) |
| `algebra export <input>` | Record an export entry (no args = show recent exports) |
| `algebra config <input>` | Record a config entry (no args = show recent configs) |
| `algebra status <input>` | Record a status entry (no args = show recent statuses) |
| `algebra report <input>` | Record a report entry (no args = show recent reports) |
| `algebra stats` | Show summary statistics across all log files |
| `algebra export <fmt>` | Export all data in json, csv, or txt format |
| `algebra search <term>` | Search across all entries for a keyword |
| `algebra recent` | Show the 20 most recent activity entries |
| `algebra status` | Health check — version, data dir, entry count, disk usage |
| `algebra help` | Show usage info and available commands |
| `algebra version` | Show version (v2.0.0) |

## How It Works

Each command (run, check, convert, analyze, etc.) works as a timestamped log recorder:

- **With arguments**: saves the input to `~/.local/share/algebra/<command>.log` with a timestamp, then confirms the entry count.
- **Without arguments**: displays the 20 most recent entries from that command's log file.

All activity is also recorded in a central `history.log` for cross-command traceability.

## Data Storage

- **Location**: `~/.local/share/algebra/`
- **Log files**: One `.log` file per command (e.g., `run.log`, `check.log`, `analyze.log`)
- **History**: `history.log` — central activity log across all commands
- **Export**: `export.json`, `export.csv`, or `export.txt` generated on demand
- **Format**: Each log line is `YYYY-MM-DD HH:MM|<input>`

## Requirements

- Bash (4.0+)
- Standard Unix utilities (`wc`, `du`, `grep`, `tail`, `head`, `date`)
- No external dependencies or API keys required

## When to Use

1. **Tracking algebra homework** — log each problem you solve with `algebra run "solve x^2 + 3x = 0"` and review later with `algebra recent`
2. **Comparing approaches** — use `algebra compare "method A vs method B"` to record different solution strategies side by side
3. **Batch processing** — log batch operations with `algebra batch "problems 1-20 chapter 5"` to track bulk work sessions
4. **Generating reports** — use `algebra report "weekly summary"` to create traceable report entries, then `algebra stats` to see totals
5. **Exporting for review** — run `algebra export json` to get all logged data in a structured format for sharing or backup

## Examples

```bash
# Record an algebra run
algebra run "simplify 3x + 5x - 2"

# Check a result
algebra check "verify x = 4 satisfies 2x + 1 = 9"

# Analyze an expression
algebra analyze "factor x^2 - 9"

# Compare two methods
algebra compare "substitution vs elimination for system of equations"

# Generate a template
algebra generate "quadratic formula template"

# View summary statistics
algebra stats

# Export all data as JSON
algebra export json

# Search for a keyword across all logs
algebra search "quadratic"

# Show recent activity
algebra recent

# Health check
algebra status
```

## Output

Results go to stdout. Save with `algebra run > output.txt`. All entries are also persisted in the data directory for later retrieval.

## Configuration

Set `ALGEBRA_DIR` environment variable to change the data directory. Default: `~/.local/share/algebra/`

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
