---
name: claw-social-feed
description: 将社交媒体内容抓取并存入 Obsidian。支持 Twitter/X、Reddit、GitHub 等 36 个平台（通过 bb-browser）。增量抓取、自动过滤、打标签、定时同步。触发场景：(1) 用户要求抓取/同步社交媒体内容到 Obsidian；(2) 用户要求设置定时同步；(3) 用户提供要追踪的账号列表。
allowed-tools: Bash(fetch_save.py:*)
---

# claw-social-feed

把社交媒体的时间线内容抓取到 Obsidian vault 中。支持多平台、增量同步、智能过滤、自动打标签。

**核心依赖**：`bb-browser`（通过 `--openclaw` 复用 OpenClaw 浏览器），bb-browser 支持 36 个平台，详见 [references/platforms.md](references/platforms.md)。

## 工作流程

```
用户配置 (config.yaml)
      │
      ▼
fetch_save.py
      │
      ├── 账号去重检查
      ├── 读取 state.json（上次抓取状态）
      │
      ▼
bb-browser site <platform>/<cmd> --openclaw --json
      │
      ▼
过滤 → 打标签 → 写入 Obsidian
      │
      ▼
更新 state.json
```

## 快速开始

### 1. 初始化（首次使用）

```bash
# 更新 bb-browser 适配器
bb-browser site update

# 测试抓取
python3 scripts/fetch_save.py --verbose
```

### 2. 编辑配置

编辑 `config.yaml`：

```yaml
accounts:
  - platform: twitter
    username: your_twitter_handle  # ← 替换成你的用户名
  # - platform: reddit
  #   username: your_reddit_username  # 其他平台示例

vault_base: ~/Documents/Obsidian Vault/你的文件夹名  # ← 修改为你的 Vault 路径

fetch:
  count: 20  # 默认值，可改

filters:
  min_text_length: 30
  skip_retweet_no_comment: true
  skip_link_only: true
  blocked_keywords: []

tagging:
  enabled: true
  keywords:
    AI / LLM / GPT: AI
    skill / Skills: skill
    Python / JavaScript: coding
```

### 3. 手动运行

```bash
python3 scripts/fetch_save.py --verbose
```

### 4. 查看结果

内容存入 `vault_base` 配置目录下，每个内容一条 `.md` 文件，带 Obsidian YAML frontmatter（平台、作者、日期、URL、点赞、标签）。

---

## 配置说明

### accounts — 抓取账号列表

```yaml
accounts:
  - platform: twitter
    username: your_handle  # ← 必填，替换成你的用户名
```

- `platform`：必须是 bb-browser 支持的平台名（见 references/platforms.md）
- `username`：该平台的用户标识（不是昵称）
- **注意账号唯一性**：`platform + username` 组合不可重复

### filters — 过滤规则

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `min_text_length` | int | 30 | 正文低于此字数跳过 |
| `skip_retweet_no_comment` | bool | true | 转推无原创评论时跳过 |
| `skip_link_only` | bool | true | 仅有链接/图片无文字时跳过 |
| `blocked_keywords` | list | [] | 包含任一关键词时跳过 |

### tagging — 自动打标签

根据内容中的关键词自动添加 tag：

```yaml
tagging:
  enabled: true
  keywords:
    AI / LLM / 大模型: AI
    skill / Skills: skill
```

匹配规则：关键词支持 `/` 分隔的多个同义词（OR 关系），匹配时忽略大小写。`/` 两端的空格会被 trim。

### fetch.count — 抓取条数

```yaml
fetch:
  count: 20  # 默认20，最大100
```

bb-browser `twitter/tweets` 默认返回约20条，按时间倒序。开启定时任务时建议设为50-100，防止高频发布者在两次抓取间隔内产出超过20条导致内容被截断。

---

## 增量抓取

脚本通过 `state.json` 记录每个账号的上次抓取时间。下次运行时：

1. 跳过 `created_at ≤ last_fetch` 的内容
2. 只存新增内容
3. 成功后将 `last_fetch` 更新为本次运行时间

**漏执行补偿**：如果 cron 因关机等原因漏跑，开机后会自动补偿 `catchup_window_days` 天内的内容（默认3天）。

如需强制重新抓取某个账号，手动删除 `state.json` 中对应账号的记录即可。

---

## 设置定时任务

要开启定时同步，告诉我：

> 「每天早上9点同步」或「每周一早上8点同步」

我会帮你创建 cron。cron 任务通过 `sessionTarget: isolated` 后台运行，使用增量模式（只拉新内容），不会重复存入。

---

## 故障排除

**`bb-browser: command not found`**
脚本会自动查找 bb-browser（依次尝试 PATH、nvm 常见路径）。若仍找不到，可手动安装或确认 npm 全局 bin 目录在 PATH 中。

**`twitter/search` 报错 `webpack module not found`**
这是 bb-browser 适配器兼容性问题，不影响 `twitter/tweets`。改用 `twitter/tweets` 命令。

**平台返回 401 未登录**
确认 OpenClaw 浏览器已登录该平台。手动打开该网站登录一次后重试。

**文件已存在但想重新抓取**
删除 `state.json` 中对应账号记录，或删除对应 `.md` 文件。
