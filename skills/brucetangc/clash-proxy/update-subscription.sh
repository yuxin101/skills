#!/bin/bash
# Clash 订阅更新脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROVIDERS_DIR="$SCRIPT_DIR/providers"
CONFIG_FILE="$SCRIPT_DIR/config.yaml"
API_URL="http://127.0.0.1:9090"

# 确保目录存在
mkdir -p "$PROVIDERS_DIR"

echo "========================================"
echo "🔄 Clash 订阅更新"
echo "========================================"
echo "📂 目录：$SCRIPT_DIR"
echo "📝 提供者：$PROVIDERS_DIR"
echo "========================================"
echo ""

# 检查 Clash 是否运行
if ! pgrep -x "clash" > /dev/null; then
    echo "❌ Clash 未运行，无法更新订阅"
    exit 1
fi

# 从配置提取订阅 URL
SUBSCRIPTION_URL=$(grep -A3 "proxy-providers:" "$CONFIG_FILE" | grep "url:" | head -1 | sed 's/.*url: "\([^"]*\)".*/\1/')

if [ -z "$SUBSCRIPTION_URL" ]; then
    echo "❌ 未找到订阅 URL"
    exit 1
fi

echo "📡 订阅地址：$SUBSCRIPTION_URL"
echo ""

# 下载订阅
echo "📥 下载订阅..."
SUB_FILE="$PROVIDERS_DIR/hongkong.yaml"

if curl -sL "$SUBSCRIPTION_URL" -o "$SUB_FILE.tmp"; then
    # 检查文件类型
    FILE_TYPE=$(file "$SUB_FILE.tmp" | grep -o "ASCII text\|UTF-8 text")
    
    if [ -n "$FILE_TYPE" ]; then
        mv "$SUB_FILE.tmp" "$SUB_FILE"
        echo "✅ 订阅下载成功"
        echo "📄 文件：$SUB_FILE"
        
        # 统计节点数量
        NODE_COUNT=$(grep -c "name:" "$SUB_FILE" 2>/dev/null || echo "0")
        echo "📊 节点数量：$NODE_COUNT 个"
        
        # 检查文件格式
        if python3 -c "import yaml; yaml.safe_load(open('$SUB_FILE'))" 2>/dev/null; then
            echo "✅ 格式验证通过"
        else
            echo "⚠️  格式验证失败，保留旧文件"
            mv "$SUB_FILE" "$SUB_FILE.error"
            mv "$SUB_FILE.tmp" "$SUB_FILE" 2>/dev/null || true
        fi
    else
        echo "❌ 下载的文件格式不正确"
        rm -f "$SUB_FILE.tmp"
        exit 1
    fi
else
    echo "❌ 下载失败"
    rm -f "$SUB_FILE.tmp"
    exit 1
fi

echo ""
echo "🔄 通知 Clash 重新加载配置..."

# 通过 API 重新加载配置（Clash 不支持热重载，需要重启）
echo "⚠️  Clash 需要重启才能应用新订阅"
echo ""
read -p "是否现在重启 Clash？(y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🛑 停止 Clash..."
    pkill -x clash
    sleep 2
    
    echo "🚀 启动 Clash..."
    cd "$SCRIPT_DIR"
    nohup ./clash -d . > logs/clash.log 2>&1 &
    sleep 3
    
    if pgrep -x "clash" > /dev/null; then
        echo "✅ Clash 已重启"
        echo ""
        echo "📊 新订阅状态:"
        curl -s "$API_URL/proxies" | python3 -c "
import sys, json
data = json.load(sys.stdin)
proxy = data.get('proxies', {}).get('Proxy-Manual', {})
print(f'  可用节点：{len(proxy.get(\"all\", []))} 个')
print(f'  当前节点：{proxy.get(\"now\", \"N/A\")}')
" 2>/dev/null || echo "  (API 暂未就绪)"
    else
        echo "❌ Clash 启动失败，请检查日志"
        tail -20 logs/clash.log
        exit 1
    fi
else
    echo "ℹ️  订阅文件已更新，下次启动 Clash 时生效"
    echo "   运行：./start.sh 重启 Clash"
fi

echo ""
echo "========================================"
echo "✅ 订阅更新完成"
echo "========================================"
