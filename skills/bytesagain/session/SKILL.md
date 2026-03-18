---
name: session
version: "1.0.0"
description: "Manage session state and lifecycle using JSONL storage. Use when tracking user sessions, expiring stale data, or auditing session activity."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: [session, state, management, lifecycle, tracking]
---

# Session — Session State Management Tool

Manage session state, lifecycle, and metadata using a local JSONL-backed store. Create, read, update, and delete sessions with support for expiration, refresh, bulk cleanup, and export.

## Prerequisites

- Python 3.8+
- `bash` shell
- No external dependencies required

## Data Storage

All session data is stored in `~/.session/data.jsonl`. Each line is a JSON object representing a session record. The tool auto-creates the directory and file on first use.

## Commands

| Command   | Description                                      | Usage                                                        |
|-----------|--------------------------------------------------|--------------------------------------------------------------|
| create    | Create a new session with optional metadata      | `create [--user USER] [--ttl SECONDS] [--meta KEY=VAL ...]`  |
| get       | Retrieve a session by ID                         | `get SESSION_ID`                                             |
| set       | Set or update a key-value pair in a session      | `set SESSION_ID KEY VALUE`                                   |
| delete    | Delete a session by ID                           | `delete SESSION_ID`                                          |
| list      | List all sessions, optionally filter by status   | `list [--status active\|expired] [--user USER] [--limit N]`  |
| expire    | Mark a session as expired                        | `expire SESSION_ID`                                          |
| refresh   | Refresh a session's TTL / last-access timestamp  | `refresh SESSION_ID [--ttl SECONDS]`                         |
| stats     | Show summary statistics for all sessions         | `stats`                                                      |
| export    | Export sessions to JSON or CSV                   | `export [--format json\|csv] [--output FILE]`                |
| cleanup   | Remove all expired sessions from the store       | `cleanup [--before TIMESTAMP] [--dry-run]`                   |
| config    | Show or update tool configuration                | `config [KEY] [VALUE]`                                       |
| help      | Show usage information                           | `help`                                                       |
| version   | Show version number                              | `version`                                                    |

## Examples

```bash
# Create a session for user "alice" with 1-hour TTL
bash scripts/script.sh create --user alice --ttl 3600

# Get session details
bash scripts/script.sh get abc123

# Update session data
bash scripts/script.sh set abc123 theme dark

# List active sessions
bash scripts/script.sh list --status active

# Export all sessions to JSON
bash scripts/script.sh export --format json --output sessions.json

# Clean up expired sessions (dry-run first)
bash scripts/script.sh cleanup --dry-run

# Show statistics
bash scripts/script.sh stats
```

## Output Format

All commands output structured JSON to stdout. Errors are written to stderr with a non-zero exit code.

## Error Handling

- Missing session ID → exit 1 with descriptive error
- Invalid command → shows help text
- Corrupt JSONL line → skipped with warning to stderr

## Notes

- Session IDs are generated as 12-character hex strings by default.
- TTL defaults to 3600 seconds (1 hour) if not specified.
- The `cleanup` command permanently removes expired sessions from the JSONL file.
- The `refresh` command updates `last_access` and optionally resets the TTL.
- All timestamps are stored as ISO 8601 UTC strings.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
