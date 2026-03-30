---
name: openclaw-config-master
description: Edit and validate OpenClaw Gateway config (openclaw.json / JSON5). Use when adding/changing config keys (gateway.*, agents.*, models.*, channels.*, tools.*, skills.*, plugins.*, $include) or diagnosing openclaw doctor/config validation errors, to avoid schema mismatches that prevent the Gateway from starting or weaken security policies.
---

# OpenClaw Config

## Overview

Safely edit `~/.openclaw/openclaw.json` (or the path set by `OPENCLAW_CONFIG_PATH`) using a schema-first workflow. Validate before and after changes to avoid invalid keys/types that can break startup or change security behavior.

## Workflow (Safe Edit)

1. **Identify the active config path**

- Precedence: `OPENCLAW_CONFIG_PATH` > `OPENCLAW_STATE_DIR/openclaw.json` > `~/.openclaw/openclaw.json`
- The config file is **JSON5** (comments + trailing commas allowed).

2. **Get an authoritative schema (do not guess keys)**

- If the Gateway is running: use `openclaw gateway call config.schema --params '{}'` to fetch a JSON Schema matching the running version.
- Otherwise: use `openclaw/openclaw` source-of-truth, primarily:
  - `src/config/zod-schema.ts` (`OpenClawSchema` root keys like `gateway`/`skills`/`plugins`)
  - `src/config/zod-schema.*.ts` (submodules: channels/providers/models/agents/tools)
  - `docs/gateway/configuration.md` (repo docs + examples)

3. **Apply changes with the smallest safe surface**

- Prefer small edits: `openclaw config get|set|unset` (dot path or bracket notation).
- If the Gateway is online and you want "write + validate + restart" in one step: use RPC `config.patch` (merge patch) or `config.apply` (replaces the entire config; use carefully).
- For complex setups, split config with `$include` (see below).

4. **Validate strictly**

- Run `openclaw doctor`, then fix issues using the reported `path` + `message`.
- Do not run `openclaw doctor --fix/--yes` without explicit user consent (it writes to config/state files).

### 复杂配置操作流程

对于复杂的配置变更（如添加新模型提供者、配置新频道等），遵循以下增强流程：

1. **前置检查**
   - 确认所有必需的凭证和参数
   - 验证目标平台/服务的可用性
   - 备份当前配置文件
   - 停止运行中的 Gateway

2. **详细配置**
   - 参考 `references/complex-operations.md` 获取完整步骤
   - 使用最小安全表面进行修改
   - 遵循渐进式修改原则（一次修改一个部分）

3. **验证和测试**
   - 运行 `openclaw doctor` 验证配置
   - 逐步测试新功能
   - 监控日志输出
   - 准备回滚方案

4. **文档记录**
   - 记录配置变更
   - 更新相关文档
   - 保存配置版本信息

### 版本升级流程

升级 OpenClaw 配置到新版本时：

1. **升级前准备**
   - 参阅 `references/version-migration.md`
   - 创建完整备份
   - 检查版本兼容性矩阵
   - 查看破坏性变更列表

2. **执行迁移**
   - 使用迁移脚本（如可用）
   - 更新配置字段
   - 处理废弃字段
   - 验证配置完整性

3. **验证和回滚**
   - 运行完整测试套件
   - 监控系统行为
   - 准备快速回滚方案

## Guardrails (Avoid Schema Bugs)

- **Most objects are strict** (`.strict()`): unknown keys usually fail validation and the Gateway will refuse to start.
- `channels` is `.passthrough()`: extension channels (matrix/zalo/nostr, etc.) can add custom keys, but most provider configs remain strict.
- `env` is `.catchall(z.string())`: you can put string env vars directly under `env`, and you can also use `env.vars`.
- **Secrets**: prefer environment variables/credential files. Avoid committing long-lived tokens/API keys into `openclaw.json`.

## $include (Modular Config)

`$include` is resolved before schema validation and lets you split config across JSON5 files:

- Supports `"$include": "./base.json5"` or `"$include": ["./a.json5", "./b.json5"]`
- Relative paths are resolved against the directory of the current config file.
- Deep-merge rules (per implementation):
  - objects: merge recursively
  - arrays: **concatenate** (not replace)
  - primitives: later value wins
- If sibling keys exist alongside `$include`, sibling keys override included values.
- Limits: max depth 10; circular includes are detected and rejected.

## Common Recipes (Examples)

1. Set default workspace

```bash
openclaw config set agents.defaults.workspace '"~/.openclaw/workspace"' --json
openclaw doctor
```

2. Change Gateway port

```bash
openclaw config set gateway.port 18789 --json
openclaw doctor
```

3. Split config (example)

```json5
// ~/.openclaw/openclaw.json
{
  "$include": ["./gateway.json5", "./channels/telegram.json5"],
}
```

4. Telegram open DMs (must explicitly allow senders)

> Schema constraint: when `dmPolicy="open"`, `allowFrom` must include `"*"`.

```bash
openclaw config set channels.telegram.dmPolicy '"open"' --json
openclaw config set channels.telegram.allowFrom '["*"]' --json
openclaw doctor
```

5. Discord token (config or env fallback)

```bash
# Option A: write to config
openclaw config set channels.discord.token '"YOUR_DISCORD_BOT_TOKEN"' --json

# Option B: env var fallback (still recommend a channels.discord section exists)
# export DISCORD_BOT_TOKEN="..."

openclaw doctor
```

6. Enable web_search (Brave / Perplexity)

```bash
openclaw config set tools.web.search.enabled true --json
openclaw config set tools.web.search.provider '"brave"' --json

# Recommended: provide the key via env var (or write tools.web.search.apiKey)
# export BRAVE_API_KEY="..."

openclaw doctor
```

## 快速链接

### 复杂配置操作

当需要执行复杂配置时，参考以下详细指南：

- **添加新的模型提供者** → `references/complex-operations.md#1-添加新的模型提供者`
  - 认证配置、环境变量设置、模型注册
  
- **配置新的频道** → `references/complex-operations.md#2-配置新的频道`
  - Telegram、Discord、Slack 完整配置示例
  
- **修改 Agent 工具配置** → `references/complex-operations.md#3-修改-agent-工具配置`
  - 工具权限、预设配置、允许/拒绝列表
  
- **调整诊断和日志设置** → `references/complex-operations.md#4-调整诊断和日志设置`
  - 日志级别、OpenTelemetry、会话维护

### 故障诊断

遇到配置问题时：

1. **快速诊断** → 运行 `openclaw doctor`
2. **常见错误模式** → 参考各操作指南中的"常见错误"表格
3. **配置验证** → 使用 `scripts/openclaw-config-check.sh`
4. **日志分析** → 检查 `~/.openclaw/logs/openclaw.log`

### 版本升级

升级到新版本时：

- **完整迁移指南** → `references/version-migration.md`
  - 升级前准备、兼容性矩阵、字段变更追踪
  - 迁移步骤、验证方法、回滚方案
  - 实用脚本（版本比较、自动迁移、健康检查）

- **快速检查清单**：
  - [ ] 备份当前配置
  - [ ] 查看版本兼容性
  - [ ] 阅读破坏性变更
  - [ ] 准备回滚方案
  - [ ] 在测试环境验证

### 工具和脚本

- **配置检查** → `scripts/openclaw-config-check.sh`
- **版本比较** → `references/version-migration.md#实用脚本`
- **健康检查** → `references/version-migration.md#健康检查脚本`

## Resources

Load these when you need a field index or source locations:

### 快速参考

- `references/openclaw-config-fields.md` (root key index + key field lists with sources)
- `references/schema-sources.md` (how to locate schema + constraints in openclaw repo)

### 深度指南

- `references/complex-operations.md` (复杂配置操作完整指南)
  - 添加新的模型提供者
  - 配置新的频道（Telegram/Discord/Slack）
  - 修改 Agent 工具配置
  - 调整诊断和日志设置
- `references/version-migration.md` (版本迁移和升级指南)
  - 升级前准备和检查清单
  - 版本兼容性矩阵
  - 字段变更追踪方法
  - 迁移步骤和验证流程
  - 破坏性变更处理
  - 回滚方案和实用脚本

### 工具脚本

- `scripts/openclaw-config-check.sh` (print config path + run doctor)
