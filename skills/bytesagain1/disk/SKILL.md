---
name: disk
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [disk, tool, utility]
description: "Monitor disk usage, find space hogs, and get cleanup suggestions. Use when checking space, finding large files, monitoring partitions."
---

# Disk

A sysops toolkit for scanning, monitoring, reporting, alerting, tracking usage, checking health, fixing issues, cleaning up, backing up, restoring, logging, benchmarking, and comparing disk-related operations — all from the command line with full history tracking.

## Commands

| Command | Description |
|---------|-------------|
| `disk scan <input>` | Record and review disk scan entries (run without args to see recent) |
| `disk monitor <input>` | Record and review monitoring entries |
| `disk report <input>` | Record and review report entries |
| `disk alert <input>` | Record and review alert entries |
| `disk top <input>` | Record and review top-usage entries |
| `disk usage <input>` | Record and review usage entries |
| `disk check <input>` | Record and review health check entries |
| `disk fix <input>` | Record and review fix entries |
| `disk cleanup <input>` | Record and review cleanup entries |
| `disk backup <input>` | Record and review backup entries |
| `disk restore <input>` | Record and review restore entries |
| `disk log <input>` | Record and review log entries |
| `disk benchmark <input>` | Record and review benchmark entries |
| `disk compare <input>` | Record and review comparison entries |
| `disk stats` | Show summary statistics across all log files |
| `disk export <fmt>` | Export all data in JSON, CSV, or TXT format |
| `disk search <term>` | Search across all logged entries |
| `disk recent` | Show the 20 most recent activity entries |
| `disk status` | Health check — version, data dir, entry count, disk usage |
| `disk help` | Show usage info and all available commands |
| `disk version` | Print version string |

Each data command (scan, monitor, report, etc.) works in two modes:
- **With arguments:** Logs the input with a timestamp and saves to the corresponding `.log` file
- **Without arguments:** Displays the 20 most recent entries from that command's log

## Data Storage

All data is stored locally in `~/.local/share/disk/`. Each command writes to its own log file (e.g., `scan.log`, `monitor.log`, `cleanup.log`). A unified `history.log` tracks all activity across commands with timestamps.

- Log format: `YYYY-MM-DD HH:MM|<input>`
- History format: `MM-DD HH:MM <command>: <input>`
- No external database or network access required
- Set `DISK_DIR` environment variable to change data directory (default: `~/.local/share/disk/`)

## Requirements

- Bash 4+ (uses `set -euo pipefail`)
- Standard POSIX utilities: `date`, `wc`, `du`, `head`, `tail`, `grep`, `basename`, `cat`
- No root privileges needed
- No API keys or external dependencies

## When to Use

1. **Tracking disk usage over time** — Use `disk usage` and `disk monitor` to log periodic disk space readings, building a historical record you can search and export later
2. **Recording cleanup and maintenance actions** — Use `disk cleanup` and `disk fix` to keep a timestamped log of what was cleaned, freed, or repaired on which servers
3. **Documenting backup and restore operations** — Use `disk backup` and `disk restore` to maintain an audit trail of when backups were made and restores performed
4. **Benchmarking and comparing disk performance** — Use `disk benchmark` and `disk compare` to log I/O test results across different drives or configurations
5. **Generating exportable reports** — Use `disk export json` to produce a structured file of all logged activity for capacity planning, compliance, or team handoff

## Examples

### Log a disk scan and review history

```bash
# Record a scan result
disk scan "/dev/sda1: 78% used, 45GB free"

# View recent scan entries
disk scan
```

### Monitor and alert workflow

```bash
# Log a monitoring observation
disk monitor "Server-01 /var at 92% — approaching threshold"

# Log an alert
disk alert "CRITICAL: /data partition at 98% on prod-db-03"

# Search for all entries mentioning a server
disk search "prod-db-03"
```

### Cleanup and fix tracking

```bash
# Log a cleanup action
disk cleanup "Removed 12GB of old Docker images on build-server"

# Log a fix
disk fix "Extended /var/log LVM volume by 10GB"

# View recent activity
disk recent
```

### Export and statistics

```bash
# Summary stats across all log files
disk stats

# Export everything as JSON
disk export json

# Export as CSV for spreadsheet analysis
disk export csv

# Health check
disk status
```

### Backup and restore documentation

```bash
# Log a backup
disk backup "Full backup of /home to s3://backups/2025-03-18"

# Log a restore
disk restore "Restored /etc/nginx from backup-2025-03-15.tar.gz"

# Log a benchmark
disk benchmark "fio sequential read: 520 MB/s on /dev/nvme0n1"
```

## How It Works

Disk uses a simple case-dispatch architecture in a single Bash script. Each command maps to a log file under `~/.local/share/disk/`. When called with arguments, the input is appended with a timestamp. When called without arguments, the last 20 lines of that log are displayed. The `stats` command aggregates counts across all logs, `export` serializes everything into your chosen format, and `search` greps across all log files for a given term.

## Support

- Website: [bytesagain.com](https://bytesagain.com)
- Feedback: [bytesagain.com/feedback](https://bytesagain.com/feedback)
- Email: hello@bytesagain.com

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
