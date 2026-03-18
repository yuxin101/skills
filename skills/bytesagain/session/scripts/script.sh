#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# session — Session State Management Tool
# Version: 1.0.0
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
###############################################################################

SKILL_VERSION="1.0.0"
DATA_DIR="$HOME/.session"
DATA_FILE="$DATA_DIR/data.jsonl"
CONFIG_FILE="$DATA_DIR/config.json"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

# Initialize config if missing
if [ ! -f "$CONFIG_FILE" ]; then
  echo '{"default_ttl": 3600}' > "$CONFIG_FILE"
fi

COMMAND="${1:-help}"
shift 2>/dev/null || true

case "$COMMAND" in

  create)
    export SKILL_USER="" SKILL_TTL="" SKILL_META=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --user) SKILL_USER="$2"; shift 2 ;;
        --ttl) SKILL_TTL="$2"; shift 2 ;;
        --meta) SKILL_META="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    python3 << 'PYEOF'
import json, os, secrets, datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.session/data.jsonl"))
config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.session/config.json"))

with open(config_file, "r") as f:
    config = json.load(f)

user = os.environ.get("SKILL_USER", "") or "anonymous"
ttl_str = os.environ.get("SKILL_TTL", "")
ttl = int(ttl_str) if ttl_str else config.get("default_ttl", 3600)
meta_str = os.environ.get("SKILL_META", "")

now = datetime.datetime.utcnow()
session_id = secrets.token_hex(6)

meta = {}
if meta_str:
    for pair in meta_str.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            meta[k.strip()] = v.strip()

record = {
    "type": "session",
    "id": session_id,
    "user": user,
    "status": "active",
    "ttl": ttl,
    "meta": meta,
    "created_at": now.isoformat() + "Z",
    "last_access": now.isoformat() + "Z",
    "expires_at": (now + datetime.timedelta(seconds=ttl)).isoformat() + "Z"
}

with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")

print(json.dumps({"ok": True, "session": record}, indent=2))
PYEOF
    ;;

  get)
    SESSION_ID="${1:-}"
    if [ -z "$SESSION_ID" ]; then
      echo '{"error": "SESSION_ID required"}' >&2
      exit 1
    fi
    export SESSION_ID
    python3 << 'PYEOF'
import json, os

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.session/data.jsonl"))
session_id = os.environ["SESSION_ID"]

found = None
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
            if rec.get("id") == session_id and rec.get("type") == "session":
                found = rec
        except json.JSONDecodeError:
            continue

if found:
    print(json.dumps({"ok": True, "session": found}, indent=2))
else:
    print(json.dumps({"ok": False, "error": f"Session {session_id} not found"}))
    exit(1)
PYEOF
    ;;

  set)
    SESSION_ID="${1:-}"
    SKILL_KEY="${2:-}"
    SKILL_VALUE="${3:-}"
    if [ -z "$SESSION_ID" ] || [ -z "$SKILL_KEY" ]; then
      echo '{"error": "Usage: set SESSION_ID KEY VALUE"}' >&2
      exit 1
    fi
    export SESSION_ID SKILL_KEY SKILL_VALUE
    python3 << 'PYEOF'
import json, os, datetime, tempfile

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.session/data.jsonl"))
session_id = os.environ["SESSION_ID"]
key = os.environ["SKILL_KEY"]
value = os.environ.get("SKILL_VALUE", "")

records = []
updated = False
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("id") == session_id and rec.get("type") == "session":
            meta = rec.get("meta", {})
            meta[key] = value
            rec["meta"] = meta
            rec["last_access"] = datetime.datetime.utcnow().isoformat() + "Z"
            updated = True
            result = rec
        records.append(rec)

if not updated:
    print(json.dumps({"ok": False, "error": f"Session {session_id} not found"}))
    exit(1)

tmp = data_file + ".tmp"
with open(tmp, "w") as f:
    for rec in records:
        f.write(json.dumps(rec) + "\n")
os.replace(tmp, data_file)

print(json.dumps({"ok": True, "session": result}, indent=2))
PYEOF
    ;;

  delete)
    SESSION_ID="${1:-}"
    if [ -z "$SESSION_ID" ]; then
      echo '{"error": "SESSION_ID required"}' >&2
      exit 1
    fi
    export SESSION_ID
    python3 << 'PYEOF'
import json, os

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.session/data.jsonl"))
session_id = os.environ["SESSION_ID"]

records = []
deleted = False
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("id") == session_id and rec.get("type") == "session":
            deleted = True
            continue
        records.append(rec)

if not deleted:
    print(json.dumps({"ok": False, "error": f"Session {session_id} not found"}))
    exit(1)

tmp = data_file + ".tmp"
with open(tmp, "w") as f:
    for rec in records:
        f.write(json.dumps(rec) + "\n")
os.replace(tmp, data_file)

print(json.dumps({"ok": True, "deleted": session_id}))
PYEOF
    ;;

  list)
    export SKILL_STATUS="" SKILL_USER="" SKILL_LIMIT=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --status) SKILL_STATUS="$2"; shift 2 ;;
        --user) SKILL_USER="$2"; shift 2 ;;
        --limit) SKILL_LIMIT="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    python3 << 'PYEOF'
import json, os, datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.session/data.jsonl"))
status_filter = os.environ.get("SKILL_STATUS", "")
user_filter = os.environ.get("SKILL_USER", "")
limit_str = os.environ.get("SKILL_LIMIT", "")
limit = int(limit_str) if limit_str else None

now = datetime.datetime.utcnow()
sessions = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("type") != "session":
            continue
        # Check expiration
        expires = rec.get("expires_at", "")
        if expires:
            try:
                exp_dt = datetime.datetime.fromisoformat(expires.rstrip("Z"))
                if exp_dt < now and rec.get("status") == "active":
                    rec["status"] = "expired"
            except ValueError:
                pass
        if status_filter and rec.get("status") != status_filter:
            continue
        if user_filter and rec.get("user") != user_filter:
            continue
        sessions.append(rec)

if limit:
    sessions = sessions[:limit]

print(json.dumps({"ok": True, "count": len(sessions), "sessions": sessions}, indent=2))
PYEOF
    ;;

  expire)
    SESSION_ID="${1:-}"
    if [ -z "$SESSION_ID" ]; then
      echo '{"error": "SESSION_ID required"}' >&2
      exit 1
    fi
    export SESSION_ID
    python3 << 'PYEOF'
import json, os, datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.session/data.jsonl"))
session_id = os.environ["SESSION_ID"]

records = []
expired = False
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("id") == session_id and rec.get("type") == "session":
            rec["status"] = "expired"
            rec["expired_at"] = datetime.datetime.utcnow().isoformat() + "Z"
            expired = True
            result = rec
        records.append(rec)

if not expired:
    print(json.dumps({"ok": False, "error": f"Session {session_id} not found"}))
    exit(1)

tmp = data_file + ".tmp"
with open(tmp, "w") as f:
    for rec in records:
        f.write(json.dumps(rec) + "\n")
os.replace(tmp, data_file)

print(json.dumps({"ok": True, "session": result}, indent=2))
PYEOF
    ;;

  refresh)
    SESSION_ID="${1:-}"
    if [ -z "$SESSION_ID" ]; then
      echo '{"error": "SESSION_ID required"}' >&2
      exit 1
    fi
    shift
    export SESSION_ID SKILL_TTL=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --ttl) SKILL_TTL="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    python3 << 'PYEOF'
import json, os, datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.session/data.jsonl"))
config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.session/config.json"))
session_id = os.environ["SESSION_ID"]
ttl_str = os.environ.get("SKILL_TTL", "")

with open(config_file, "r") as f:
    config = json.load(f)

ttl = int(ttl_str) if ttl_str else config.get("default_ttl", 3600)
now = datetime.datetime.utcnow()

records = []
refreshed = False
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("id") == session_id and rec.get("type") == "session":
            rec["last_access"] = now.isoformat() + "Z"
            rec["ttl"] = ttl
            rec["expires_at"] = (now + datetime.timedelta(seconds=ttl)).isoformat() + "Z"
            rec["status"] = "active"
            refreshed = True
            result = rec
        records.append(rec)

if not refreshed:
    print(json.dumps({"ok": False, "error": f"Session {session_id} not found"}))
    exit(1)

tmp = data_file + ".tmp"
with open(tmp, "w") as f:
    for rec in records:
        f.write(json.dumps(rec) + "\n")
os.replace(tmp, data_file)

print(json.dumps({"ok": True, "session": result}, indent=2))
PYEOF
    ;;

  stats)
    python3 << 'PYEOF'
import json, os, datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.session/data.jsonl"))
now = datetime.datetime.utcnow()

total = 0
active = 0
expired = 0
users = set()
ttls = []

with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("type") != "session":
            continue
        total += 1
        expires = rec.get("expires_at", "")
        status = rec.get("status", "active")
        if expires:
            try:
                exp_dt = datetime.datetime.fromisoformat(expires.rstrip("Z"))
                if exp_dt < now:
                    status = "expired"
            except ValueError:
                pass
        if status == "active":
            active += 1
        else:
            expired += 1
        users.add(rec.get("user", "unknown"))
        ttls.append(rec.get("ttl", 0))

avg_ttl = sum(ttls) / len(ttls) if ttls else 0

stats = {
    "total_sessions": total,
    "active": active,
    "expired": expired,
    "unique_users": len(users),
    "average_ttl_seconds": round(avg_ttl, 1),
    "data_file": data_file
}
print(json.dumps({"ok": True, "stats": stats}, indent=2))
PYEOF
    ;;

  export)
    export SKILL_FORMAT="json" SKILL_OUTPUT=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --format) SKILL_FORMAT="$2"; shift 2 ;;
        --output) SKILL_OUTPUT="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    python3 << 'PYEOF'
import json, os, csv, io

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.session/data.jsonl"))
fmt = os.environ.get("SKILL_FORMAT", "json")
output = os.environ.get("SKILL_OUTPUT", "")

sessions = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("type") == "session":
            sessions.append(rec)

if fmt == "csv":
    if sessions:
        fields = ["id", "user", "status", "ttl", "created_at", "last_access", "expires_at"]
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for s in sessions:
            writer.writerow(s)
        result = buf.getvalue()
    else:
        result = ""
else:
    result = json.dumps(sessions, indent=2)

if output:
    with open(output, "w") as f:
        f.write(result)
    print(json.dumps({"ok": True, "exported": len(sessions), "file": output}))
else:
    print(result)
PYEOF
    ;;

  cleanup)
    export SKILL_BEFORE="" SKILL_DRY_RUN="false"
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --before) SKILL_BEFORE="$2"; shift 2 ;;
        --dry-run) SKILL_DRY_RUN="true"; shift ;;
        *) shift ;;
      esac
    done
    python3 << 'PYEOF'
import json, os, datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.session/data.jsonl"))
before_str = os.environ.get("SKILL_BEFORE", "")
dry_run = os.environ.get("SKILL_DRY_RUN", "false") == "true"

now = datetime.datetime.utcnow()
before = None
if before_str:
    try:
        before = datetime.datetime.fromisoformat(before_str.rstrip("Z"))
    except ValueError:
        before = now
else:
    before = now

records = []
removed = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("type") == "session":
            expires = rec.get("expires_at", "")
            status = rec.get("status", "active")
            is_expired = status == "expired"
            if expires:
                try:
                    exp_dt = datetime.datetime.fromisoformat(expires.rstrip("Z"))
                    if exp_dt < before:
                        is_expired = True
                except ValueError:
                    pass
            if is_expired:
                removed.append(rec)
                continue
        records.append(rec)

if not dry_run:
    tmp = data_file + ".tmp"
    with open(tmp, "w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    os.replace(tmp, data_file)

print(json.dumps({
    "ok": True,
    "dry_run": dry_run,
    "removed_count": len(removed),
    "remaining_count": len(records),
    "removed_ids": [r["id"] for r in removed]
}, indent=2))
PYEOF
    ;;

  config)
    SKILL_KEY="${1:-}"
    SKILL_VALUE="${2:-}"
    export SKILL_KEY SKILL_VALUE
    python3 << 'PYEOF'
import json, os

config_file = os.environ.get("CONFIG_FILE", os.path.expanduser("~/.session/config.json"))
key = os.environ.get("SKILL_KEY", "")
value = os.environ.get("SKILL_VALUE", "")

with open(config_file, "r") as f:
    config = json.load(f)

if key and value:
    try:
        config[key] = json.loads(value)
    except (json.JSONDecodeError, ValueError):
        config[key] = value
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    print(json.dumps({"ok": True, "updated": {key: config[key]}}))
elif key:
    val = config.get(key, None)
    print(json.dumps({"ok": True, key: val}))
else:
    print(json.dumps({"ok": True, "config": config}, indent=2))
PYEOF
    ;;

  help)
    cat << 'HELPEOF'
session — Session State Management Tool v1.0.0

Commands:
  create   Create a new session        [--user USER] [--ttl SECONDS] [--meta KEY=VAL]
  get      Get a session by ID         SESSION_ID
  set      Set a key-value pair        SESSION_ID KEY VALUE
  delete   Delete a session            SESSION_ID
  list     List sessions               [--status active|expired] [--user USER] [--limit N]
  expire   Mark session as expired     SESSION_ID
  refresh  Refresh session TTL         SESSION_ID [--ttl SECONDS]
  stats    Show session statistics
  export   Export sessions             [--format json|csv] [--output FILE]
  cleanup  Remove expired sessions     [--before TIMESTAMP] [--dry-run]
  config   Show/update config          [KEY] [VALUE]
  help     Show this help
  version  Show version

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
HELPEOF
    ;;

  version)
    echo "{\"tool\": \"session\", \"version\": \"$SKILL_VERSION\"}"
    ;;

  *)
    echo "{\"error\": \"Unknown command: $COMMAND. Run 'help' for usage.\"}" >&2
    exit 1
    ;;

esac
