#!/bin/bash
# Clash Proxy - 启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/clash.log"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

echo "========================================"
echo "🌐 Clash Proxy"
echo "========================================"
echo "📂 目录：$SCRIPT_DIR"
echo "📝 日志：$LOG_FILE"
echo "========================================"
echo ""

# 检查是否已运行
if pgrep -x "clash" > /dev/null; then
    echo "✅ Clash 已在运行"
    echo ""
    python3 "$SCRIPT_DIR/main.py" status
    exit 0
fi

# 检查二进制文件
if [ ! -x "$SCRIPT_DIR/clash" ]; then
    echo "❌ Clash 二进制文件不存在或不可执行"
    exit 1
fi

# 检查配置文件
if [ ! -f "$SCRIPT_DIR/config.yaml" ]; then
    echo "❌ 配置文件不存在：$SCRIPT_DIR/config.yaml"
    exit 1
fi

# 启动 Clash
echo "🚀 启动 Clash..."
cd "$SCRIPT_DIR"
nohup ./clash -d . > "$LOG_FILE" 2>&1 &

# 等待启动
sleep 3

if pgrep -x "clash" > /dev/null; then
    echo "✅ Clash 已启动"
    echo ""
    echo "📊 代理信息:"
    echo "   HTTP/SOCKS5: http://127.0.0.1:7890"
    echo "   API:         http://127.0.0.1:9090"
    echo ""
    python3 "$SCRIPT_DIR/main.py" status
else
    echo "❌ Clash 启动失败"
    echo ""
    echo "📝 日志:"
    tail -20 "$LOG_FILE"
    exit 1
fi
