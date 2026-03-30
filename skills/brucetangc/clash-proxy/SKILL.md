---
name: clash-proxy
version: 1.0.0
author: BruceTang
license: MIT
description: Clash 代理管理服务（基于 Mihomo 内核），提供 HTTP/SOCKS 代理、订阅管理、节点切换、流量统计、自动更新等功能
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["clash"]
      system_deps: ["systemd"]
    provides:
      service: "HTTP Proxy"
      port: 7890
    install:
      - id: clash
        kind: binary
        url: https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-linux-amd64-compatible.gz
        label: Install Mihomo (Clash) Binary
---

# Clash Proxy Skill

基于 [Mihomo](https://github.com/MetaCubeX/mihomo) (原 Clash.Meta) 的代理管理服务。

## 功能特性

- ✅ HTTP/SOCKS5 代理服务
- ✅ 订阅管理（自动更新）
- ✅ 节点切换（自动选择最快）
- ✅ 故障转移（节点挂了自动切）
- ✅ 状态监控
- ✅ 日志查看
- ✅ 流量统计
- ✅ 内核自动更新
- ✅ systemd 托管（开机自启）

## 快速开始

### 1. 启动服务

```bash
# 方式 1：使用启动脚本
cd ~/.openclaw/workspace/skills/clash-proxy
./start.sh

# 方式 2：使用 systemd
systemctl start clash-proxy

# 方式 3：直接运行
./clash -d .
```

### 2. 检查状态

```bash
# 查看运行状态
systemctl status clash-proxy

# 查看监听端口
netstat -tlnp | grep 7890

# 测试代理
curl -I -x http://127.0.0.1:7890 https://www.google.com
```

### 3. 配置代理

其他 skill 使用本代理：

```python
import requests

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

response = requests.get("https://www.google.com", proxies=proxies)
```

## 目录结构

```
clash-proxy/
├── SKILL.md              # 本文件
├── README.md             # 详细文档
├── main.py               # 管理脚本
├── start.sh              # 启动脚本
├── clash                 # Mihomo 二进制
├── config.yaml           # 代理配置
├── logs/                 # 日志目录
│   └── clash.log
└── providers/            # 订阅文件目录
```

## 配置说明

### config.yaml

```yaml
mixed-port: 7890          # 代理监听端口
allow-lan: false          # 允许局域网访问
mode: rule                # 模式：rule/global/direct
log-level: info           # 日志级别

proxy-providers:          # 订阅管理
  HongKong:
    type: http
    url: "你的订阅地址"
    interval: 3600        # 每小时更新

proxies:                  # 代理节点
  - name: 🇭🇰 Hong Kong
    type: ss
    server: example.com
    port: 16001
    cipher: aes-256-gcm
    password: your_password

proxy-groups:             # 代理组
  - name: Proxy
    type: url-test        # 自动选择最快
    use:
      - HongKong
    url: 'http://www.gstatic.com/generate_204'
    interval: 300
    tolerance: 50

rules:                    # 规则
  - DOMAIN-SUFFIX,garmin.com,Proxy
  - GEOIP,CN,DIRECT
  - MATCH,Proxy
```

## API 接口

Clash 提供 RESTful API（端口 9090）：

```bash
# 查看代理组
curl http://127.0.0.1:9090/proxies

# 切换节点
curl -X PUT http://127.0.0.1:9090/proxies/Proxy \
  -d '{"name": "🇭🇰 Hong Kong"}'

# 查看日志
curl http://127.0.0.1:9090/logs
```

## 与其他 Skill 集成

### Garmin Sync Pro

```ini
# .env 配置
GLOBAL_PROXY=http://127.0.0.1:7890
```

### 其他 Python 脚本

```python
import os

# 检查 Clash 是否运行
def is_clash_running():
    import subprocess
    result = subprocess.run(
        ["pgrep", "-x", "clash"],
        capture_output=True
    )
    return result.returncode == 0

# 获取代理配置
def get_proxy():
    return {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    } if is_clash_running() else None
```

## 故障排查

### Q: 服务无法启动

```bash
# 查看日志
journalctl -u clash-proxy -f

# 检查配置
./clash -t -d .
```

### Q: 代理无法连接

```bash
# 检查端口
netstat -tlnp | grep 7890

# 测试连通性
curl -I -x http://127.0.0.1:7890 https://www.google.com
```

### Q: 节点无法使用

```bash
# 查看当前节点
curl http://127.0.0.1:9090/proxies | python3 -m json.tool

# 切换节点
curl -X PUT http://127.0.0.1:9090/proxies/Proxy \
  -d '{"name": "🇭🇰 Hong Kong"}'
```

## 更新订阅

```bash
# 手动更新
./update-subscription.sh

# 自动更新（每小时）
# 配置在 config.yaml 的 proxy-providers 中
# interval: 3600
```

## 更新内核

```bash
# 自动更新（每周一 3:00）
# systemd timer: clash-proxy-update.timer

# 手动更新
python3 update-core.py --auto
```

## 相关项目

- **Mihomo:** https://github.com/MetaCubeX/mihomo
- **Clash Meta:** https://github.com/MetaCubeX/Clash.Meta
- **OpenClaw:** https://github.com/openclaw/openclaw

---

**版本：** 1.0.0  
**最后更新：** 2026-03-26  
**作者：** BruceTang  
**许可：** MIT
