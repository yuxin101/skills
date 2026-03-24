#!/usr/bin/env bash
set -euo pipefail

VERSION="3.0.0"
SCRIPT_NAME="puzzle"
DATA_DIR="$HOME/.local/share/puzzle"
mkdir -p "$DATA_DIR"

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com

_info()  { echo "[INFO]  $*"; }
_error() { echo "[ERROR] $*" >&2; }
die()    { _error "$@"; exit 1; }

cmd_riddle() {
    local riddles=('I speak without a mouth. (Echo)' 'I have keys but no locks. (Keyboard)' 'I have hands but cannot clap. (Clock)'); echo ${riddles[$((RANDOM % 3))]}
}

cmd_math() {
    local a=$((RANDOM % 50 + 1)); local b=$((RANDOM % 50 + 1)); echo "$a + $b = ?"
}

cmd_word() {
    echo 'Unscramble: '$(echo 'puzzle' | fold -w1 | shuf | tr -d '\n')
}

cmd_logic() {
    echo 'If all cats are animals, and some animals are pets, are all cats pets? (Yes)'
}

cmd_daily() {
    cmd_riddle
}

cmd_streak() {
    echo 'Puzzles solved: '$(wc -l < $DATA_DIR/solved.log 2>/dev/null || echo 0)
}

cmd_help() {
    echo "$SCRIPT_NAME v$VERSION"
    echo ""
    echo "Commands:"
    printf "  %-25s\n" "riddle"
    printf "  %-25s\n" "math"
    printf "  %-25s\n" "word"
    printf "  %-25s\n" "logic"
    printf "  %-25s\n" "daily"
    printf "  %-25s\n" "streak"
    printf "  %%-25s\n" "help"
    echo ""
    echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"
}

cmd_version() { echo "$SCRIPT_NAME v$VERSION"; }

main() {
    local cmd="${1:-help}"
    case "$cmd" in
        riddle) shift; cmd_riddle "$@" ;;
        math) shift; cmd_math "$@" ;;
        word) shift; cmd_word "$@" ;;
        logic) shift; cmd_logic "$@" ;;
        daily) shift; cmd_daily "$@" ;;
        streak) shift; cmd_streak "$@" ;;
        help) cmd_help ;;
        version) cmd_version ;;
        *) die "Unknown: $cmd" ;;
    esac
}

main "$@"
