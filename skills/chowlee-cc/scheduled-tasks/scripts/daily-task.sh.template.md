#!/bin/bash
# OpenClaw Scheduler - Daily Task Script Template | 定时任务脚本模板
# Version | 版本: 1.0.0
# Description | 描述: Template for creating scheduled tasks with system crontab
#              使用系统 crontab 创建定时任务的模板

set -e

# Configuration | 配置
# =============================================================================

# Agent ID to execute the task | 执行任务的 Agent ID
AGENT_ID="<agent-id>"

# Feishu account ID for reply | 飞书回复账号 ID
REPLY_ACCOUNT="<feishu-account-id>"

# Target user OpenID | 目标用户 OpenID
TARGET_USER="user:<user_open_id>"

# Task message (bilingual) | 任务消息（双语）
TASK_MESSAGE="Execute scheduled task | 执行定时任务"

# Log file path | 日志文件路径
LOG_FILE="/tmp/openclaw-scheduler-$(basename "$0" .sh).log"

# =============================================================================

# Setup | 设置
# =============================================================================

# Ensure PATH is set correctly for cron environment
# 确保 PATH 在 cron 环境中正确设置
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Get script directory | 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Timestamp function | 时间戳函数
timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# Log function | 日志函数
log() {
    echo "[$(timestamp)] $1" | tee -a "$LOG_FILE"
}

# =============================================================================

# Main execution | 主执行
# =============================================================================

log "========================================="
log "Task started | 任务开始"
log "Agent: $AGENT_ID"
log "Target: $TARGET_USER"
log "Message: $TASK_MESSAGE"
log "========================================="

# Execute OpenClaw agent command | 执行 OpenClaw agent 命令
openclaw agent \
  --agent "$AGENT_ID" \
  --deliver \
  --reply-account "$REPLY_ACCOUNT" \
  --reply-to "$TARGET_USER" \
  -m "$TASK_MESSAGE"

# Check exit status | 检查退出状态
if [ $? -eq 0 ]; then
    log "Task completed successfully | 任务成功完成"
else
    log "Task failed with exit code $? | 任务失败，退出码 $?"
    exit 1
fi

log "========================================="

# =============================================================================

# End of script | 脚本结束
