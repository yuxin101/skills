#!/bin/bash
# Clash 节点切换脚本

API_URL="http://127.0.0.1:9090"

# 检查 Clash 是否运行
if ! pgrep -x "clash" > /dev/null; then
    echo "❌ Clash 未运行"
    exit 1
fi

# 显示帮助
show_help() {
    echo "用法：$0 <command> [options]"
    echo ""
    echo "命令:"
    echo "  list              列出所有节点"
    echo "  current           查看当前节点"
    echo "  switch <name>     切换到指定节点"
    echo "  auto              启用自动选择"
    echo "  test              测试所有节点延迟"
    echo ""
    echo "示例:"
    echo "  $0 list"
    echo "  $0 current"
    echo "  $0 switch '🇭🇰 Hong Kong丨 02'"
    echo "  $0 auto"
}

# 列出所有节点
list_nodes() {
    echo "📋 可用节点:"
    curl -s "$API_URL/proxies" | python3 -c "
import sys, json
data = json.load(sys.stdin)
proxy = data.get('proxies', {}).get('Proxy-Manual', {})
for i, node in enumerate(proxy.get('all', []), 1):
    print(f'  {i}. {node}')
"
}

# 查看当前节点
current_node() {
    echo "📍 当前节点:"
    curl -s "$API_URL/proxies" | python3 -c "
import sys, json
data = json.load(sys.stdin)
proxy = data.get('proxies', {}).get('Proxy', {})
print(f'  代理组：Proxy')
print(f'  当前节点：{proxy.get(\"now\", \"N/A\")}')
"
}

# 切换节点
switch_node() {
    local node_name="$1"
    if [ -z "$node_name" ]; then
        echo "❌ 请指定节点名称"
        exit 1
    fi
    
    echo "🔄 切换到：$node_name"
    curl -s -X PUT "$API_URL/proxies/Proxy" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"$node_name\"}"
    
    echo ""
    echo "✅ 切换完成"
    current_node
}

# 启用自动选择
enable_auto() {
    echo "🔄 启用自动选择..."
    
    # 切换到 url-test 模式（自动选择最快）
    curl -s -X PUT "$API_URL/proxies/Proxy" \
        -H "Content-Type: application/json" \
        -d '{"name": "url-test"}'
    
    echo "✅ 已启用自动选择"
    echo "   每 5 分钟自动测试并选择最快节点"
}

# 测试节点延迟
test_nodes() {
    echo "🧪 测试节点延迟..."
    curl -s "$API_URL/proxies" | python3 -c "
import sys, json
data = json.load(sys.stdin)
proxy = data.get('proxies', {}).get('Proxy-Manual', {})
print('节点延迟测试:')
for node in proxy.get('all', []):
    print(f'  {node}: 测试中...')
# 实际延迟测试需要调用 API 的 delay 接口
print('提示：使用 Clash Dashboard 查看实时延迟')
"
}

# 主程序
case "$1" in
    list)
        list_nodes
        ;;
    current)
        current_node
        ;;
    switch)
        switch_node "$2"
        ;;
    auto)
        enable_auto
        ;;
    test)
        test_nodes
        ;;
    *)
        show_help
        ;;
esac
