#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
INSTALLER="$SCRIPT_DIR/scripts/install_web_app.py"
DOCTOR="$SCRIPT_DIR/scripts/doctor.py"

if [[ -t 1 ]]; then
  C_RESET=$'\033[0m'
  C_BOLD=$'\033[1m'
  C_GREEN=$'\033[32m'
  C_YELLOW=$'\033[33m'
  C_RED=$'\033[31m'
  C_BLUE=$'\033[34m'
  C_CYAN=$'\033[36m'
else
  C_RESET=''; C_BOLD=''; C_GREEN=''; C_YELLOW=''; C_RED=''; C_BLUE=''; C_CYAN=''
fi

section() { printf "\n%s%s== %s ==%s\n" "$C_BLUE" "$C_BOLD" "$1" "$C_RESET"; }
ok() { printf "%s[OK]%s %s\n" "$C_GREEN" "$C_RESET" "$1"; }
warn() { printf "%s[WARN]%s %s\n" "$C_YELLOW" "$C_RESET" "$1"; }
err() { printf "%s[ERROR]%s %s\n" "$C_RED" "$C_RESET" "$1" >&2; }
keyv() { printf "%s%-12s%s %s%s%s\n" "$C_CYAN" "$1" "$C_RESET" "$C_BOLD" "$2" "$C_RESET"; }

if ! command -v python3 >/dev/null 2>&1; then
  err "未找到 python3，请先安装 Python 3。"
  exit 1
fi

if [[ ! -f "$INSTALLER" ]]; then
  err "缺少安装脚本：$INSTALLER"
  exit 1
fi

section "OPENAI AUTH SWITCHER PUBLIC"
ok "开始安装 Web 预览入口"
printf "workspace     %s\n" "$WORKSPACE_DIR"

set +e
INSTALL_JSON="$(python3 "$INSTALLER" --json 2>&1)"
INSTALL_CODE=$?
set -e

if [[ $INSTALL_CODE -ne 0 ]]; then
  err "安装失败"
  printf "%s\n\n" "$INSTALL_JSON" >&2
  warn "建议执行诊断： python3 $DOCTOR --json"
  exit $INSTALL_CODE
fi

mapfile -t LINES < <(INSTALL_JSON="$INSTALL_JSON" python3 - <<'PY'
import json, os, sys
raw = os.environ.get('INSTALL_JSON', '')
try:
    data = json.loads(raw)
except Exception:
    print('__RAW__')
    print(raw)
    sys.exit(0)
service = data.get('service') or {}
print('__STATUS__')
print('ok')
print('__WARNING__')
print(service.get('warning') or service.get('fallback_reason') or '')
print('__WEB__')
print(data.get('local_url') or '')
print(str(data.get('port') or ''))
print('__LOGIN__')
print(data.get('username') or '')
print(data.get('password') or '')
print('__SSH__')
print(data.get('ssh_tunnel') or '')
print('__SERVICE__')
print(service.get('mode') or '')
print(str(data.get('ready')))
print(service.get('unit_name') or '')
print(service.get('log_path') or '')
PY
)

if [[ ${LINES[0]:-} == "__RAW__" ]]; then
  printf "%s\n" "${LINES[@]:1}"
  exit 0
fi

WARNING_MSG="${LINES[3]:-}"
WEB_URL="${LINES[5]:-}"
WEB_PORT="${LINES[6]:-}"
WEB_USER="${LINES[8]:-}"
WEB_PASS="${LINES[9]:-}"
SSH_TUNNEL="${LINES[11]:-}"
SERVICE_MODE="${LINES[13]:-}"
SERVICE_READY="${LINES[14]:-}"
SYSTEMD_UNIT="${LINES[15]:-}"
LOG_FILE="${LINES[16]:-}"

section "RESULT"
ok "安装完成"
if [[ "$SERVICE_READY" == "True" ]]; then
  ok "Service ready: TRUE"
else
  warn "Service ready: $SERVICE_READY"
fi
if [[ -n "$WARNING_MSG" ]]; then
  warn "$WARNING_MSG"
fi

section "WEB"
keyv "URL" "$WEB_URL"
keyv "PORT" "$WEB_PORT"

section "LOGIN"
keyv "USERNAME" "$WEB_USER"
keyv "PASSWORD" "$WEB_PASS"

section "SSH TUNNEL"
printf "%s%s%s\n" "$C_BOLD" "$SSH_TUNNEL" "$C_RESET"

section "SERVICE"
keyv "MODE" "$SERVICE_MODE"
if [[ -n "$SYSTEMD_UNIT" ]]; then
  keyv "UNIT" "$SYSTEMD_UNIT"
fi
if [[ -n "$LOG_FILE" ]]; then
  keyv "LOG" "$LOG_FILE"
fi
