#!/usr/bin/env bash
set -euo pipefail

# OpenClaw Safe Change Runner
# Usage:
#   safe-change.sh --main-cmd '<command applying main config change>' [--wife-cmd '<command applying wife change>'] [--wife-token '<token>']

MAIN_CFG="${MAIN_CFG:-$HOME/.openclaw/openclaw.json}"
WIFE_CFG="${WIFE_CFG:-$HOME/.openclaw-wife/.openclaw/openclaw.json}"
WIFE_HOME="${WIFE_HOME:-$HOME/.openclaw-wife}"
WIFE_URL="${WIFE_URL:-ws://127.0.0.1:18889}"
WIFE_TOKEN="${WIFE_TOKEN:-wife-instance-token-18889}"

MAIN_CMD=""
WIFE_CMD=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --main-cmd) MAIN_CMD="$2"; shift 2 ;;
    --wife-cmd) WIFE_CMD="$2"; shift 2 ;;
    --wife-token) WIFE_TOKEN="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

if [[ -z "$MAIN_CMD" ]]; then
  echo "ERROR: --main-cmd is required"
  exit 2
fi

TS=$(date +%Y%m%d-%H%M%S)
MAIN_BAK="${MAIN_CFG}.bak.safe-${TS}"
WIFE_BAK="${WIFE_CFG}.bak.safe-${TS}"

cp "$MAIN_CFG" "$MAIN_BAK"
[[ -f "$WIFE_CFG" ]] && cp "$WIFE_CFG" "$WIFE_BAK" || true

echo "[1/5] backups created"

echo "[2/5] apply main change"
bash -lc "$MAIN_CMD"

if [[ -n "$WIFE_CMD" ]]; then
  echo "[2b/5] apply wife change"
  bash -lc "$WIFE_CMD"
fi

rollback() {
  echo "[rollback] restoring backups..."
  cp "$MAIN_BAK" "$MAIN_CFG" || true
  if [[ -f "$WIFE_BAK" ]]; then cp "$WIFE_BAK" "$WIFE_CFG" || true; fi
  openclaw gateway restart >/dev/null 2>&1 || true
  if command -v launchctl >/dev/null 2>&1; then
    launchctl kickstart -k "gui/$(id -u)/ai.openclaw.gateway.wife" >/dev/null 2>&1 || true
  fi
  echo "[rollback] done"
}

echo "[3/5] validate main"
if ! openclaw status --deep >/dev/null 2>&1; then
  echo "[error] main validation failed"
  rollback
  exit 1
fi

echo "[4/5] validate wife (if exists)"
if [[ -f "$WIFE_CFG" ]]; then
  if ! OPENCLAW_HOME="$WIFE_HOME" openclaw gateway health --url "$WIFE_URL" --token "$WIFE_TOKEN" >/dev/null 2>&1; then
    echo "[error] wife validation failed"
    rollback
    exit 1
  fi
fi

echo "[5/5] success: changes applied safely"
echo "main backup: $MAIN_BAK"
[[ -f "$WIFE_BAK" ]] && echo "wife backup: $WIFE_BAK" || true
