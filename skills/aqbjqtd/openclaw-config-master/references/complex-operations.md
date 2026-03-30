# OpenClaw 复杂配置操作指南

本指南提供 OpenClaw 配置文件 `~/.openclaw/openclaw.json` 的复杂操作步骤，包括前置条件、详细步骤、验证方法和常见错误处理。

## 📋 目录

1. [添加新的模型提供者](#1-添加新的模型提供者)
2. [配置新的频道](#2-配置新的频道)
3. [修改 Agent 工具配置](#3-修改-agent-工具配置)
4. [调整诊断和日志设置](#4-调整诊断和日志设置)

---

## 1. 添加新的模型提供者

### 前置条件检查

- [ ] 已获取模型提供者的 API Key 或 OAuth 凭证
- [ ] 已确认提供者的 API 端点 URL
- [ ] 已确认 API 兼容类型（OpenAI Completions / Anthropic Messages 等）
- [ ] 已了解模型的参数限制（上下文窗口、最大 Token 数等）
- [ ] OpenClaw Gateway 已停止运行

### 操作步骤

#### 步骤 1: 添加认证配置

在 `auth.profiles` 部分添加新的认证配置：

```json
{
  "auth": {
    "profiles": {
      "yourprovider:default": {
        "provider": "yourprovider",
        "mode": "api_key"
      }
    }
  }
}
```

**可选认证模式**：
- `api_key`: 使用 API 密钥认证
- `oauth`: 使用 OAuth 认证

#### 步骤 2: 配置环境变量（如需要）

如果使用 API Key，在 `env.vars` 部分添加：

```json
{
  "env": {
    "vars": {
      "YOURPROVIDER_API_KEY": "your-api-key-here"
    }
  }
}
```

#### 步骤 3: 添加模型提供者配置

在 `models.providers` 部分添加新提供者：

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "yourprovider": {
        "baseUrl": "https://api.yourprovider.com/v1",
        "apiKey": "env:YOURPROVIDER_API_KEY",
        "api": "openai-completions",
        "models": [
          {
            "id": "model-name",
            "name": "Display Name",
            "reasoning": true,
            "input": ["text"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 128000,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

**关键字段说明**：
- `baseUrl`: API 端点 URL
- `apiKey`: 认证密钥，支持 `env:VAR_NAME` 引用环境变量
- `api`: API 类型（`openai-completions` / `anthropic-messages` 等）
- `models`: 模型列表数组

#### 步骤 4: 在 Agent 默认配置中注册模型

在 `agents.defaults.models` 部分添加新模型：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "yourprovider/model-name",
        "fallbacks": ["zai/glm-5"]
      },
      "models": {
        "yourprovider/model-name": {}
      }
    }
  }
}
```

#### 步骤 5: 启动 Gateway 并验证

```bash
# 启动 Gateway
openclaw gateway

# 在另一个终端验证配置
openclaw doctor

# 测试模型调用
openclaw gateway call chat --params '{"message":"测试"}'
```

### 验证方法

1. **配置验证**：
   ```bash
   openclaw doctor
   ```
   检查输出中是否包含新提供者信息

2. **模型可用性**：
   ```bash
   openclaw gateway call models.list --params '{}'
   ```
   确认新模型出现在列表中

3. **实际调用测试**：
   发送测试消息，验证模型响应

### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Unknown provider` | 提供者 ID 拼写错误 | 检查 `auth.profiles` 和 `models.providers` 中的 ID 一致性 |
| `Invalid API key` | API Key 未设置或错误 | 确认 `env.vars` 中的变量名正确，且 `apiKey` 引用格式正确 |
| `Connection refused` | baseUrl 错误或服务不可用 | 验证 API 端点 URL 可访问性 |
| `Model not found` | 模型 ID 错误 | 检查提供者文档中的正确模型 ID |

---

## 2. 配置新的频道

### 前置条件检查

- [ ] 已获取频道的 Bot Token 或 OAuth 凭证
- [ ] 已在频道平台创建 Bot 应用
- [ ] 已配置 Bot 的权限和范围
- [ ] OpenClaw Gateway 已停止运行

### 操作步骤

#### Telegram 配置

1. **创建 Telegram Bot**：
   - 与 [@BotFather](https://t.me/botfather) 对话
   - 使用 `/newbot` 命令创建新 Bot
   - 保存生成的 Bot Token

2. **添加配置**：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "your-telegram-bot-token",
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist",
      "streaming": "partial"
    }
  },
  "plugins": {
    "entries": {
      "telegram": {
        "enabled": true
      }
    }
  }
}
```

**策略选项**：
- `dmPolicy`: `"open"` / `"pairing"` / `"closed"`
- `groupPolicy`: `"allowlist"` / `"blocklist"` / `"closed"`

#### Discord 配置

1. **创建 Discord 应用**：
   - 访问 [Discord Developer Portal](https://discord.com/developers/applications)
   - 创建应用并启用 Bot
   - 保存 Bot Token
   - 配置 OAuth2 权限

2. **添加配置**：

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "botToken": "your-discord-bot-token",
      "dmPolicy": "pairing",
      "guildPolicy": "allowlist",
      "streaming": "partial"
    }
  },
  "plugins": {
    "entries": {
      "discord": {
        "enabled": true
      }
    }
  }
}
```

#### Slack 配置

1. **创建 Slack 应用**：
   - 访问 [Slack API](https://api.slack.com/apps)
   - 创建应用并配置 Bot 权限
   - 安装应用到工作区
   - 保存 Bot Token 和 Signing Secret

2. **添加配置**：

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "botToken": "xoxb-your-bot-token",
      "signingSecret": "your-signing-secret",
      "dmPolicy": "pairing",
      "teamPolicy": "allowlist",
      "streaming": "partial"
    }
  },
  "plugins": {
    "entries": {
      "slack": {
        "enabled": true
      }
    }
  }
}
```

### 验证方法

1. **配置验证**：
   ```bash
   openclaw doctor
   ```

2. **频道连接测试**：
   - Telegram: 向 Bot 发送 `/start` 命令
   - Discord: 在服务器中邀请 Bot 并发送消息
   - Slack: 在频道中提及 Bot

3. **日志检查**：
   ```bash
   journalctl -u openclaw -f
   ```

### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Invalid bot token` | Token 格式错误或已失效 | 重新生成 Token 并更新配置 |
| `Bot not authorized` | Bot 权限不足 | 检查 Bot 在频道平台的权限配置 |
| `Connection timeout` | 网络连接问题 | 检查防火墙设置和网络连接 |
| `Webhook failed` | Webhook URL 配置错误 | 确认外部访问配置正确 |

---

## 3. 修改 Agent 工具配置

### 前置条件检查

- [ ] 已了解工具配置的基本结构
- [ ] 已确定需要修改的工具配置项
- [ ] 已备份当前配置文件
- [ ] OpenClaw Gateway 已停止运行

### 操作步骤

#### 步骤 1: 查看当前工具配置

```bash
# 查看当前工具配置
openclaw gateway call tools.list --params '{}'

# 查看特定工具详情
openclaw gateway call tools.get --params '{"toolId":"tool-name"}'
```

#### 步骤 2: 修改全局工具配置

修改 `tools` 部分：

```json
{
  "tools": {
    "profile": "coding",
    "elevated": {
      "enabled": true
    },
    "exec": {
      "enabled": true,
      "allowed": {
        "commands": ["python", "node", "git"]
      }
    },
    "web": {
      "enabled": true,
      "allowUserUrls": true,
      "allowedDomains": ["github.com", "gitlab.com"]
    },
    "media": {
      "enabled": true,
      "images": {
        "enabled": true
      }
    }
  }
}
```

**工具配置选项**：
- `profile`: 预设配置（`"coding"` / `"full"` / `"minimal"`）
- `elevated`: 提升权限模式
- `exec`: 命令执行配置
- `web`: Web 访问配置
- `media`: 媒体处理配置

#### 步骤 3: 配置特定 Agent 的工具

修改 `agents.list` 中特定 Agent 的工具配置：

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "profile": "full",
          "allow": ["bash", "edit", "read"],
          "deny": ["camera.snap", "screen.record"]
        }
      }
    ]
  }
}
```

#### 步骤 4: 启动并验证

```bash
# 启动 Gateway
openclaw gateway

# 验证工具配置
openclaw gateway call agent.inspect --params '{"agentId":"main"}'
```

### 验证方法

1. **配置验证**：
   ```bash
   openclaw doctor
   ```

2. **工具可用性测试**：
   ```bash
   openclaw gateway call tools.list --params '{}'
   ```

3. **实际功能测试**：
   使用 Agent 执行需要特定工具的任务

### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Tool not found` | 工具 ID 不存在 | 检查工具名称拼写 |
| `Permission denied` | 权限配置错误 | 调整 `allow` / `deny` 列表 |
| `Profile not found` | 配置预设不存在 | 使用有效的 profile 名称 |
| `Tool execution failed` | 工具依赖未满足 | 安装必要的依赖或启用相关插件 |

---

## 4. 调整诊断和日志设置

### 前置条件检查

- [ ] 已了解当前诊断配置
- [ ] 已确定需要调整的诊断级别
- [ ] 已确认日志存储空间充足
- [ ] OpenClaw Gateway 已停止运行

### 操作步骤

#### 步骤 1: 配置基本诊断设置

```json
{
  "diagnostics": {
    "enabled": true,
    "otel": {
      "enabled": true,
      "traces": true,
      "metrics": true,
      "logs": true
    },
    "cacheTrace": {
      "enabled": true,
      "includeMessages": true,
      "includePrompt": true,
      "includeSystem": true
    }
  }
}
```

**选项说明**：
- `enabled`: 启用/禁用诊断功能
- `otel`: OpenTelemetry 配置
  - `traces`: 追踪请求链路
  - `metrics`: 性能指标
  - `logs`: 日志收集
- `cacheTrace`: 缓存追踪配置
  - `includeMessages`: 包含消息内容
  - `includePrompt`: 包含提示内容
  - `includeSystem`: 包含系统信息

#### 步骤 2: 配置日志级别和输出

```json
{
  "logging": {
    "level": "debug",
    "console": {
      "enabled": true,
      "level": "info"
    },
    "file": {
      "enabled": true,
      "path": "~/.openclaw/logs/openclaw.log",
      "level": "debug",
      "maxSize": "100mb",
      "maxFiles": 10
    },
    "redaction": {
      "enabled": true,
      "patterns": [
        "api_key",
        "token",
        "password"
      ]
    }
  }
}
```

**日志级别**：`trace` > `debug` > `info` > `warn` > `error` > `fatal`

#### 步骤 3: 配置会话维护

```json
{
  "session": {
    "maintenance": {
      "mode": "enforce",
      "pruneAfter": "30d",
      "maxEntries": 500,
      "rotateBytes": "10mb"
    }
  }
}
```

#### 步骤 4: 验证配置并启动

```bash
# 验证配置
openclaw doctor

# 启动 Gateway
openclaw gateway

# 查看日志
tail -f ~/.openclaw/logs/openclaw.log
```

### 验证方法

1. **配置验证**：
   ```bash
   openclaw doctor
   ```

2. **日志输出检查**：
   ```bash
   tail -f ~/.openclaw/logs/openclaw.log
   ```

3. **诊断数据查看**：
   ```bash
   openclaw gateway call diagnostics.status --params '{}'
   ```

### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Log file not writable` | 日志目录权限不足 | 检查并修正日志目录权限 |
| `Disk space low` | 磁盘空间不足 | 清理旧日志文件或增加存储空间 |
| `Invalid log level` | 日志级别名称错误 | 使用有效的级别名称 |
| `Otel connection failed` | OpenTelemetry 服务不可用 | 检查 OTel 服务配置或禁用 |

---

## 🔧 通用故障排除

### 配置重载失败

**症状**：修改配置后无法生效

**解决步骤**：

1. **验证 JSON 语法**：
   ```bash
   jq < ~/.openclaw/openclaw.json
   ```

2. **检查配置有效性**：
   ```bash
   openclaw doctor
   ```

3. **完全重启 Gateway**：
   ```bash
   openclaw gateway stop
   openclaw gateway
   ```

### 版本兼容性问题

**症状**：配置字段在当前版本中不支持

**解决步骤**：

1. **检查 OpenClaw 版本**：
   ```bash
   openclaw --version
   ```

2. **获取当前版本的 Schema**：
   ```bash
   openclaw gateway call config.schema --params '{}' > schema.json
   ```

3. **对比配置与 Schema**：
   ```bash
   grep -r "fieldName" schema.json
   ```

### 权限问题

**症状**：配置文件无法读写

**解决步骤**：

1. **检查文件权限**：
   ```bash
   ls -la ~/.openclaw/openclaw.json
   ```

2. **修正权限**：
   ```bash
   chmod 600 ~/.openclaw/openclaw.json
   ```

3. **检查文件所有者**：
   ```bash
   chown $USER:$USER ~/.openclaw/openclaw.json
   ```

---

## 📚 相关资源

- **配置字段索引**：`openclaw-config-fields.md`
- **Schema 源码指南**：`schema-sources.md`
- **OpenClaw 官方文档**：https://github.com/openclaw/openclaw
- **配置示例仓库**：https://github.com/openclaw/config-examples

---

## ⚠️ 重要提示

1. **备份配置**：在进行任何复杂配置修改前，务必备份当前配置文件
2. **渐进式修改**：一次只修改一个部分，便于定位问题
3. **验证优先**：每次修改后都运行 `openclaw doctor` 验证配置
4. **日志监控**：修改后密切关注日志输出，及时发现潜在问题
5. **版本匹配**：确保配置与当前 OpenClaw 版本兼容

---

**文档版本**：1.0.0
**最后更新**：2026-03-27
**参考配置版本**：openclaw@875324e
