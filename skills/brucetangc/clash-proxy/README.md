# Clash Proxy Skill

基于 [Mihomo](https://github.com/MetaCubeX/mihomo) 的代理管理服务。

## 安装

### 1. 复制 Clash 二进制

```bash
# 从官方下载最新版本
wget https://github.com/MetaCubeX/mihomo/releases/download/v1.18.0/mihomo-linux-amd64-compatible-v1.18.0.gz
gunzip mihomo-linux-amd64-compatible-v1.18.0.gz
mv mihomo-linux-amd64-compatible-v1.18.0 clash
chmod +x clash
```

### 2. 配置订阅

编辑 `config.yaml` 或导入订阅：

```bash
python3 main.py update --subscription "你的订阅地址"
```

### 3. 安装 systemd 服务

```bash
sudo cp clash-proxy.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable clash-proxy
sudo systemctl start clash-proxy
```

## 使用

### 启动/停止/重启

```bash
# 使用脚本
./start.sh

# 使用管理脚本
python3 main.py start
python3 main.py stop
python3 main.py restart

# 使用 systemd
systemctl start clash-proxy
systemctl stop clash-proxy
systemctl restart clash-proxy
```

### 查看状态

```bash
# 查看运行状态
python3 main.py status

# 查看 systemd 状态
systemctl status clash-proxy

# 查看监听端口
netstat -tlnp | grep 7890
```

### 测试代理

```bash
python3 main.py test

# 或手动测试
curl -I -x http://127.0.0.1:7890 https://www.google.com
```

### 查看日志

```bash
# 查看日志
python3 main.py logs

# 实时查看
tail -f logs/clash.log

# 查看 systemd 日志
journalctl -u clash-proxy -f
```

### 🆕 流量统计

```bash
# 查看总流量
python3 traffic-stats.py total

# 查看当前连接
python3 traffic-stats.py connections

# 查看各节点流量
python3 traffic-stats.py proxies

# 实时监控流量
python3 traffic-stats.py watch

# 重置流量统计
python3 traffic-stats.py reset
```

### 🆕 订阅更新

```bash
# 手动更新订阅
./update-subscription.sh

# 自动更新（每小时）
# 配置在 config.yaml 的 proxy-providers 中
# interval: 3600
```

### 节点切换

```bash
# 查看当前节点
./switch-node.sh current

# 列出所有节点
./switch-node.sh list

# 切换到指定节点
./switch-node.sh switch '🇭🇰 Hong Kong丨 02'

# 启用自动选择
./switch-node.sh auto
```

## 配置说明

### config.yaml

```yaml
# 代理端口
mixed-port: 7890

# 允许局域网访问
allow-lan: false

# 模式：rule/global/direct
mode: rule

# 日志级别
log-level: info

# DNS 配置
dns:
  enable: true
  enhanced-mode: fake-ip
  nameserver:
    - 223.5.5.5
    - 8.8.8.8

# 代理节点
proxies:
  - name: 🇭🇰 Hong Kong
    type: ss
    server: example.com
    port: 16001
    cipher: aes-256-gcm
    password: your_password

# 代理组
proxy-groups:
  - name: Proxy
    type: select
    proxies: [🇭🇰 Hong Kong, DIRECT]

# 规则
rules:
  - DOMAIN-SUFFIX,garmin.com,Proxy
  - GEOIP,CN,DIRECT
  - MATCH,Proxy
```

## API 接口

Clash 提供 RESTful API（端口 9090）：

```bash
# 查看所有代理
curl http://127.0.0.1:9090/proxies

# 查看代理组
curl http://127.0.0.1:9090/proxies/Proxy

# 切换节点
curl -X PUT http://127.0.0.1:9090/proxies/Proxy \
  -H "Content-Type: application/json" \
  -d '{"name": "🇭🇰 Hong Kong"}'

# 查看实时日志
curl http://127.0.0.1:9090/logs
```

## 与其他 Skill 集成

### Garmin Sync Pro

```ini
# skills/garmin-sync-pro/.env
GLOBAL_PROXY=http://127.0.0.1:7890
```

### Python 脚本

```python
import requests

def get_proxy():
    """获取代理配置"""
    return {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }

# 使用代理
response = requests.get(
    "https://www.google.com",
    proxies=get_proxy(),
    timeout=10
)
```

### 检查代理状态

```python
import subprocess

def is_clash_running():
    """检查 Clash 是否运行"""
    result = subprocess.run(
        ["pgrep", "-x", "clash"],
        capture_output=True
    )
    return result.returncode == 0

# 使用
if is_clash_running():
    print("Clash 运行中")
else:
    print("Clash 未运行")
```

## 故障排查

### Q: 服务无法启动

```bash
# 检查配置语法
./clash -t -d .

# 查看日志
tail -f logs/clash.log

# 查看 systemd 日志
journalctl -u clash-proxy -f
```

### Q: 代理无法连接

```bash
# 检查进程
ps aux | grep clash

# 检查端口
netstat -tlnp | grep 7890

# 测试连通性
curl -v -x http://127.0.0.1:7890 https://www.google.com
```

### Q: 节点无法使用

```bash
# 查看当前节点
curl -s http://127.0.0.1:9090/proxies | python3 -m json.tool

# 切换节点
curl -X PUT http://127.0.0.1:9090/proxies/Proxy \
  -d '{"name": "🇭🇰 Hong Kong"}'
```

### Q: 内存占用过高

```bash
# 查看内存
ps aux | grep clash

# 重启服务
systemctl restart clash-proxy

# 检查配置（减少节点数量）
cat config.yaml | grep -c "name:"
```

## 更新

### 更新 Clash 内核

```bash
cd ~/.openclaw/workspace/skills/clash-proxy

# 下载新版本
wget https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-linux-amd64-compatible.gz

# 解压
gunzip -f mihomo-linux-amd64-compatible.gz
mv mihomo-linux-amd64-compatible clash
chmod +x clash

# 重启
systemctl restart clash-proxy
```

### 更新订阅

```bash
# 手动更新
python3 main.py update --subscription "订阅地址"

# 自动更新（配置 systemd timer）
# 参考 garmin-sync.timer 配置
```

## 相关项目

- **Mihomo:** https://github.com/MetaCubeX/mihomo
- **Clash Meta:** https://github.com/MetaCubeX/Clash.Meta
- **OpenClaw:** https://github.com/openclaw/openclaw
- **Garmin Sync Pro:** ../garmin-sync-pro/

---

**版本：** 1.0.0  
**最后更新：** 2026-03-26
