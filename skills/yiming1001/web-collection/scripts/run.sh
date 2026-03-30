#!/usr/bin/env bash
set -euo pipefail

KEYWORD=""
MAX_ITEMS="10"
ENSURE_BRIDGE="false"
BRIDGE_CMD="${WEB_COLLECTION_BRIDGE_CMD:-}"
BRIDGE_URL="${WEB_COLLECTION_BRIDGE_URL:-http://127.0.0.1:19820}"

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage:
  run.sh --keyword "<关键词>" [--max-items 10] [--ensure-bridge] [--bridge-cmd '<cmd>']

Env:
  WEB_COLLECTION_BRIDGE_URL  default: http://127.0.0.1:19820
  WEB_COLLECTION_BRIDGE_CMD  optional bridge start command
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --keyword)
      KEYWORD="${2:-}"
      shift 2
      ;;
    --max-items)
      MAX_ITEMS="${2:-10}"
      shift 2
      ;;
    --ensure-bridge)
      ENSURE_BRIDGE="true"
      shift 1
      ;;
    --bridge-cmd)
      BRIDGE_CMD="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$KEYWORD" ]]; then
  echo "--keyword is required" >&2
  exit 1
fi

default_bridge_cmd() {
  local source_server="/Users/zhym/coding/web_pluging/web_collection/bridge/bridge-server.js"
  if command -v node >/dev/null 2>&1 && [[ -f "$source_server" ]]; then
    printf "node '%s'" "$source_server"
    return 0
  fi

  local runtime="/Library/Application Support/meixi-connector/runtime/node"
  local server="/Library/Application Support/meixi-connector/connector/connector-server.js"
  if [[ -x "$runtime" && -f "$server" ]]; then
    printf "'%s' '%s'" "$runtime" "$server"
    return 0
  fi
  return 1
}

if [[ -z "$BRIDGE_CMD" ]]; then
  BRIDGE_CMD="$(default_bridge_cmd || true)"
fi

CMD=(
  bash "$SKILL_DIR/scripts/collect_and_export_loop.sh"
  --platform douyin
  --method videoKeyword
  --keyword "$KEYWORD"
  --max-items "$MAX_ITEMS"
  --feature video
  --mode search
  --interval 300
  --fetch-detail true
  --detail-speed fast
  --auto-export true
  --export-mode personal
  --force-stop-before-start
  --base-url "$BRIDGE_URL"
)

if [[ "$ENSURE_BRIDGE" == "true" ]]; then
  CMD+=(--ensure-bridge)
  if [[ -n "$BRIDGE_CMD" ]]; then
    CMD+=(--bridge-cmd "$BRIDGE_CMD")
  fi
fi

"${CMD[@]}"
