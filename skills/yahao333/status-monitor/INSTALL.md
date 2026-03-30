# OpenClaw Status Monitor 安装指南

## 功能说明

定时将 OpenClaw Agent 状态同步到云端监控平台（https://openclaw-agent-monitor.vercel.app），根据每个 Agent 的 SOUL.md 个性生成随机问候语。

## 安装步骤

### 方式一：从 GitHub 安装（推荐）

```bash
# 克隆到本地
cd ~/.openclaw/skills
git clone git@github.com:yahao333/openclaw-status-monitor.git
```

### 方式二：手动安装

1. 下载或复制 `openclaw-status-monitor` 目录到 `~/.openclaw/skills/`
2. 确保目录结构如下：
   ```
   ~/.openclaw/skills/openclaw-status-monitor/
   ├── SKILL.md
   └── scripts/
   ```

## 首次配置

### 1. 重启 OpenClaw

安装后需要重启 OpenClaw 使技能生效：
```bash
# 重启 openclaw 服务
openclaw gateway restart
```

### 2. 触发技能初始化

对 OpenClaw 说：
```
启用状态监控
```

或
```
开启监控同步
```

### 3. 配置 Token

首次使用会提示配置 Token：

1. 访问 https://openclaw-agent-monitor.vercel.app
2. 点击 **Sign In** 登录（支持 Google/GitHub 等）
3. 登录后在 **Settings** 页面生成 Agent Token
4. 将 Token 发送给 OpenClaw

### 4. 完成初始化

Token 配置成功后，会自动执行首次同步。

## 使用命令

| 命令 | 说明 |
|------|------|
| `同步状态` | 手动触发一次同步 |
| `启用状态监控` | 首次启用引导 |
| `每10分钟同步一次` | 修改同步间隔 |

## 同步间隔

- 默认：30 分钟
- 可配置：5 / 10 / 15 / 30 / 60 分钟

## 数据格式

每个 Agent 上传的数据包含：

```json
{
  "id": "openclaw-{agentId}",
  "name": { "en": "...", "zh": "..." },
  "status": "online",
  "lastActive": { "en": "...", "zh": "..." },
  "greeting": { "en": "...", "zh": "..." }
}
```

**问候语**根据 Agent 的 `SOUL.md` 个性自动生成，支持以下风格：

| 风格 | 示例 |
|------|------|
| concise | ⚡ 简洁高效，随时待命 |
| thorough | 🔧 细致入微，使命必达 |
| resourceful | 💡 创意模式已激活 |
| casual | 🎯 轻松一刻，效率加倍 |
| helpful | 🤝 全心全意，助你前行 |

## 配置文件

| 文件 | 说明 |
|------|------|
| `~/.openclaw/credentials/openclaw-status-monitor.json` | Token 配置 |
| `~/.openclaw/cron/last-sync.json` | 上次同步记录 |
| `~/.openclaw/logs/sync.log` | 同步日志 |
| `~/.openclaw/logs/sync-error.log` | 错误日志 |

## 常见问题

### Q: 重启后技能不识别？
A: 确保 `.skill` 文件或目录在 `~/.openclaw/skills/` 下，重启 OpenClaw。

### Q: Token 验证失败？
A: Token 可能过期或无效，请重新在 Settings 页面生成新 Token。

### Q: 如何查看同步状态？
A: 对 OpenClaw 说"同步状态"手动触发一次同步。

### Q: 如何修改同步间隔？
A: 说"每15分钟同步一次"，OpenClaw 会更新配置。

## 卸载

```bash
# 删除技能目录
rm -rf ~/.openclaw/skills/openclaw-status-monitor.skill

# 删除配置文件（可选）
rm -rf ~/.openclaw/credentials/openclaw-status-monitor.json
rm -rf ~/.openclaw/cron/last-sync.json
```
