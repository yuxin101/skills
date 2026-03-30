---
name: openclaw-status-monitor
description: 定时将 OpenClaw Agent 状态同步到云端监控平台，根据 SOUL.md 个性生成随机问候语
author: yanghao
version: 1.2.0
metadata:
  openclaw:
    categories: [system, monitor]
    tags: [openclaw, status, sync, monitor, soul]
    user-invocable: true
    cron: "*/30 * * * *"
---

## 触发条件

当满足以下任一条件时触发：

1. **首次初始化**：用户说"启用状态监控"、"开启监控同步"
2. **手动触发**：用户发送"同步状态"、"更新监控"、"上传状态"等
3. **定时触发**：每 30 分钟（默认）自动执行
4. **指定间隔**：用户说"每10分钟同步一次"、"改成1小时"等

## 初始化流程（首次使用必须执行）

### 第一步：检查 Token 配置

执行技能时，首先检查以下位置是否有 Token：

1. 环境变量 `MONITOR_PLATFORM_TOKEN`
2. 文件 `~/.openclaw/credentials/openclaw-status-monitor.json`
3. 文件 `~/.openclaw/.env` 中的 `MONITOR_PLATFORM_TOKEN`

### 第二步：Token 不存在时的处理

如果未找到 Token，必须引导用户注册/登录：

1. **提示用户**：
   ```
   检测到未配置监控 Token，正在引导您完成设置...

   请选择登录方式：
   1. 已有账号：访问 https://openclaw-agent-monitor.vercel.app 点击 Sign In 使用 Clerk 登录
   2. 新用户：访问 https://openclaw-agent-monitor.vercel.app 点击 Sign Up 注册

   登录后：
   - 进入 Settings 页面
   - 生成并复制 Agent Token
   - 告诉我生成的 Token
   ```

2. **等待用户回复 Token**

3. **保存 Token**：
   - 创建目录 `~/.openclaw/credentials/`
   - 保存到 `~/.openclaw/credentials/openclaw-status-monitor.json`：
     ```json
     {
       "agentToken": "用户提供的token",
       "createdAt": "2026-03-26T10:00:00.000Z",
       "monitorUrl": "https://openclaw-agent-monitor.vercel.app"
     }
     ```

4. **验证 Token**：
   - 调用 API 测试 Token 是否有效
   - 如果无效，提示用户检查 Token 是否正确

### 第三步：Token 验证成功

```
✅ Token 配置成功！

正在执行首次同步...
- 检测到 X 个 Agent
- 上传数据...
- 同步成功！

监控平台地址：https://openclaw-agent-monitor.vercel.app
同步间隔：30 分钟

您可以随时说"同步状态"手动触发同步。
```

## 核心功能：读取 SOUL.md 生成问候语

### 1. 收集所有 Agent 和他们的 SOUL.md

遍历 `~/.openclaw/` 下的所有 workspace 目录，查找对应的 SOUL.md 文件：

```
~/.openclaw/
├── workspace/           → main agent
├── workspace-bob/        → bob agent
├── workspace-coding/     → coding agent
├── workspace-bot/        → bot agent
├── workspace-writer/     → writer agent
├── workspaces/code-expert/ → code-expert agent
├── workspace-assistant/  → assistant agent
├── workspace-st-*       → st-* agents
└── ...
```

### 2. 读取 SOUL.md 提取关键词

从 SOUL.md 中提取以下信息：

- **Vibe 描述**：`Be the assistant you'd actually want to talk to...`
- **性格特点**：helpful, concise, thorough, resourceful 等
- **语气风格**：casual, professional, witty 等
- **Core Truths 关键词**：genuinely helpful, have opinions, earn trust 等

### 3. 生成随机问候语模板

根据 SOUL.md 的内容，从预设模板库中选择问候语：

| SOUL 关键词 | 适用模板 |
|------------|----------|
| concise | "简洁高效，随时待命" |
| thorough | "细致入微，使命必达" |
| resourceful | "足智多谋，迎难而上" |
| casual/witty | "轻松一刻，效率加倍" |
| helpful | "全心全意，助你前行" |
| professional | "专业可靠，值得信赖" |
| default | "运转正常，随时在线" |

### 4.问候语生成算法

```
1. 读取 agent 的 SOUL.md
2. 提取关键词（最多3个）
3. 从模板库选择匹配的模板
4. 添加随机后缀（emoji + 时间相关）
5. 生成最终问候语
```

**问候语格式示例：**
```json
{
  "greeting": {
    "en": "⚡ Running smooth, ready to help. Concise & efficient as always.",
    "zh": "⚡ 运转如常，随时待命。简洁高效，使命必达。"
  }
}
```

### 5. 预设问候语模板库

```typescript
const GREETING_TEMPLATES = [
  {
    keywords: ["concise", "efficient", "minimal"],
    en: "Running lean and mean, ready to assist.",
    zh: "轻装上阵，高效出击。"
  },
  {
    keywords: ["thorough", "detailed", "comprehensive"],
    en: "System operational. Every detail covered.",
    zh: "系统就绪，滴水不漏。"
  },
  {
    keywords: ["resourceful", "creative", "solve"],
    en: "Creative problem-solving mode: activated.",
    zh: "创意模式已激活，难题迎刃而解。"
  },
  {
    keywords: ["casual", "witty", "fun"],
    en: "All systems go! Let's make magic happen.",
    zh: "一切就绪，让我们一起创造精彩！"
  },
  {
    keywords: ["helpful", "support", "assist"],
    en: "Here to help, nothing more, nothing less.",
    zh: "全心全意，助你前行。"
  },
  {
    keywords: ["professional", "reliable", "trust"],
    en: "Professional mode engaged. Ready for action.",
    zh: "专业模式启动，值得信赖。"
  },
  {
    keywords: ["bold", "confident", "opinion"],
    en: "Got opinions, got solutions. Let's do this.",
    zh: "有态度，有方案，行动！"
  },
  {
    keywords: ["default", "generic"],
    en: "Systems online. Standing by.",
    zh: "系统在线，随时待命。"
  }
];
```

## 读取 OpenClaw 状态

### 从 openclaw.json 提取 agent 列表

```json
{
  "meta": {
    "version": "2026.2.26",
    "lastTouchedAt": "2026-03-25T02:58:08.331Z"
  },
  "agents": {
    "list": [
      { "id": "main", "name": "大总管小菌" },
      { "id": "coding", "name": "coding" },
      { "id": "bot", "name": "bot" }
    ]
  }
}
```

### Agent 到 SOUL.md 的映射

| Agent ID | SOUL.md 路径 |
|----------|--------------|
| main | ~/.openclaw/workspace/SOUL.md |
| bob | ~/.openclaw/workspace-bob/SOUL.md |
| coding | ~/.openclaw/workspace-coding/SOUL.md |
| bot | ~/.openclaw/workspace-bot/SOUL.md |
| writer | ~/.openclaw/workspace-writer/SOUL.md |
| * | ~/.openclaw/workspace-{agentId}/SOUL.md |

## 转换为 Agent 格式

将 OpenClaw agent + SOUL.md 个性转换为监控平台格式：

```json
[
  {
    "id": "openclaw-{agentId}",
    "name": {
      "en": "{agentName}",
      "zh": "{agentName}"
    },
    "status": "online",
    "lastActive": {
      "en": "{ISO时间}",
      "zh": "{相对时间}"
    },
    "greeting": {
      "en": "{根据SOUL生成的英文问候语}",
      "zh": "{根据SOUL生成的中文问候语}"
    }
  }
]
```

## 上传到 Vercel

调用 `/api/upload` 接口：

```bash
curl -X POST "https://openclaw-agent-monitor.vercel.app/api/upload" \
  -H "x-agent-token: {MONITOR_PLATFORM_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{JSON_DATA}'
```

## 存储配置

### Token 存储位置

`~/.openclaw/credentials/openclaw-status-monitor.json`：

```json
{
  "agentToken": "e2d3262f-b626-4850-af11-5f2cb1c0dcad",
  "createdAt": "2026-03-26T10:00:00.000Z",
  "monitorUrl": "https://openclaw-agent-monitor.vercel.app",
  "syncIntervalMinutes": 30
}
```

### 上次同步记录

`~/.openclaw/cron/last-sync.json`：

```json
{
  "lastSyncAt": "2026-03-26T10:30:00.000Z",
  "agentCount": 12,
  "success": true,
  "greetingsGenerated": {
    "main": "简洁高效，随时待命 ⚡",
    "coding": "细致入微，代码无痕 🔧",
    "bot": "轻松一刻，效率加倍 🎯"
  }
}
```

## 配置项

| 配置项 | 环境变量 | 配置文件 | 默认值 | 说明 |
|--------|----------|----------|--------|------|
| 上传 Token | `MONITOR_PLATFORM_TOKEN` | credentials 文件 | 无 | 必填 |
| 同步间隔 | `OPENCLAW_SYNC_MINUTES` | credentials 文件 | 30 | 分钟 |
| Vercel API URL | `OPENCLAW_MONITOR_URL` | credentials 文件 | https://openclaw-agent-monitor.vercel.app | 可自定义 |

## 错误处理

### 1. 缺少 Token

**初始化时**：
```
❌ 未检测到监控 Token

请先完成以下步骤：

1. 访问 https://openclaw-agent-monitor.vercel.app
2. 点击 Sign In / Sign Up 登录或注册账号
3. 登录后在 Settings 页面生成 Agent Token
4. 将 Token 发送给我

示例：我的 Token 是 abc123-def456...
```

**运行时环境变量缺失**：
```
请设置环境变量 MONITOR_PLATFORM_TOKEN
或将其添加到 ~/.openclaw/credentials/openclaw-status-monitor.json
```

### 2. Token 无效

```
❌ Token 验证失败

您提供的 Token 可能已过期或无效。

请重新获取 Token：
1. 登录 https://openclaw-agent-monitor.vercel.app
2. 进入 Settings 页面
3. 点击 Generate 生成新 Token
4. 将新 Token 发送给我
```

### 3. 缺少 SOUL.md

如果某个 agent 没有 SOUL.md，使用默认问候语：
```
"系统在线，随时待命 📡"
```

### 4. 网络错误

- 记录错误到 `~/.openclaw/logs/sync-error.log`
- 返回友好提示
- 下次同步时自动重试

## 示例对话

### 首次启用

**User:** 启用状态监控
**Agent:**
正在检查监控配置...

❌ 未检测到 Agent Token

请先完成以下步骤：

1. 访问 https://openclaw-agent-monitor.vercel.app
2. 点击 **Sign In** 登录（支持 Google/GitHub 等）
3. 登录后在 **Settings** 页面生成 Agent Token
4. 将 Token 发送给我

**User:** 我的 Token 是 e2d3262f-b626-4850-af11-5f2cb1c0dcad
**Agent:**
正在验证 Token...

✅ Token 验证成功！

正在读取 Agent 个性（SOUL.md）...
- 大总管小菌：简洁高效，随时待命 ⚡
- coding：细致入微，使命必达 🔧
- bot：轻松一刻，效率加倍 🎯

执行首次同步...
- 检测到 3 个 Agent
- 上传数据...
- ✅ 同步成功！

---

✅ **状态监控已启用！**

- 监控平台：https://openclaw-agent-monitor.vercel.app
- 同步间隔：30 分钟
- 最近同步：2026-03-26 10:30:00

### 正常运行

**User:** 同步状态
**Agent:**
正在同步 OpenClaw 状态...

正在读取 Agent 个性...
- 大总管小菌：⚡ 运转如常
- coding：🔧 代码无痕
- ...

✅ 同步成功！

最近同步：2026-03-26 10:30:00
Agent 数量：3

### 查看问候语

**User:** 给我看看现在的问候语
**Agent:**
当前各 Agent 的问候语：

1. **大总管小菌**
   - 英文：Running lean and mean, ready to assist.
   - 中文：简洁高效，随时待命 ⚡

2. **coding**
   - 英文：System operational. Every detail covered.
   - 中文：细致入微，使命必达 🔧

3. **bot**
   - 英文：Creative problem-solving mode: activated.
   - 中文：创意模式已激活，难题迎刃而解 🚀

## 日志位置

- 同步日志：`~/.openclaw/logs/sync.log`
- 错误日志：`~/.openclaw/logs/sync-error.log`
- 上次同步：`~/.openclaw/cron/last-sync.json`
- Token 配置：`~/.openclaw/credentials/openclaw-status-monitor.json`

## SOUL.md 个性映射表

| 关键词 | 英文问候语 | 中文问候语 | Emoji |
|--------|-----------|-----------|-------|
| concise | Running lean and mean | 轻装上阵 | ⚡ |
| thorough | Every detail covered | 滴水不漏 | 🔧 |
| resourceful | Creative mode activated | 创意模式已激活 | 💡 |
| casual | Let's make magic happen | 让我们创造精彩 | 🎯 |
| helpful | Here to help, always | 全心全意 | 🤝 |
| professional | Professional mode engaged | 专业模式启动 | 🎩 |
| bold | Got opinions, got solutions | 有态度有方案 | 💪 |
| default | Systems online | 系统在线 | 📡 |
