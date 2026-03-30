# Skill Radar 📡

> 你的 AI 技能管家 — 让每一个安装的 Skill 都物尽其用

## 核心理念

**让用户使用 Skill 变得更简单更高效。**

装了太多 Skill 不知道哪些在用？不知道还缺什么？不知道版本是不是最新？

Skill Radar 一键扫描，给你完整的洞察。

### 三个层面

- **更简单** — 降低认知负担，一条命令看清全貌
- **更高效** — 减少无效投入，精准识别闲置与缺口
- **更智能** — 从被动管理到主动优化，基于真实数据做判断

## 功能

| 命令 | 说明 |
|------|------|
| `usage` | 📊 使用价值评估 — 哪些在用、哪些闲置、使用频率如何 |
| `status` | 📋 状态检查 — Ready/Missing 统计，清理建议 |
| `recommend` | 💡 智能推荐 — 基于历史对话发现需求缺口，推荐安装 |
| `versions` | 🔄 版本检查 — 对比 ClawHub 最新版本，一键更新 |
| `all` | 完整报告（以上四项） |

## 安装

```bash
# 通过 ClawHub 安装（推荐）
npx clawhub install skill-radar

# 或手动安装
cp -r skill-radar ~/.openclaw/workspace/skills/
```

## 使用

```bash
SKILL_PATH=~/.openclaw/workspace/skills/skill-radar

# 完整报告（推荐首次使用）
python3 $SKILL_PATH/scripts/health_check.py all

# 单项检查
python3 $SKILL_PATH/scripts/health_check.py usage       # 使用价值评估
python3 $SKILL_PATH/scripts/health_check.py status      # 状态检查
python3 $SKILL_PATH/scripts/health_check.py recommend   # 智能推荐
python3 $SKILL_PATH/scripts/health_check.py versions    # 版本检查

# 输出到文件
python3 $SKILL_PATH/scripts/health_check.py all > skill-report.md
```

## 使用价值评估

整合6大数据源，精准判断每个Skill是否被使用：

| 数据源 | 内容 | 说明 |
|--------|------|------|
| 🧠 Mem0 记忆 | 用户主动记录的重要信息 | 质量最高的数据源 |
| 📝 每日记忆 | 当天事件、决策、进展 | 时间线清晰，能看趋势 |
| 📋 MEMORY.md | 核心配置、偏好 | 长期稳定的需求 |
| 💓 HEARTBEAT.md | 定期任务配置 | 说明持续在用的能力 |
| 💬 Session 日志 | 原始对话记录 | 过滤系统消息后分析 |
| 🤖 AGENTS.md | 工作规则 | 反映长期使用模式 |

**评分体系**：

| 评分 | 含义 | 判定 |
|------|------|------|
| 🔵 高频 | 核心工具 | 多数据源高频出现 |
| 🟢 中频 | 经常用 | 2+数据源出现 |
| 🟡 低频 | 偶尔用 | 仅关键词匹配 |
| 🔴 未使用 | 从未提及 | 所有数据源无命中 |

## 智能推荐

基于历史对话和工作空间配置，主动发现需求缺口：

- 分析用户经常做什么
- 对比已安装Skill
- 推荐缺失的能力
- 区分高频需求和低频需求

## 依赖

- Python 3.8+（纯标准库，无外部依赖）
- OpenClaw CLI（`openclaw`，状态检查需要）
- ClawHub CLI（`npx clawhub`，版本检查和推荐搜索需要）

## 平台支持

- ✅ macOS（Homebrew / npm global）
- ✅ Linux（Linuxbrew / npm global）
- ⚠️ Windows（未测试，暂不保证）

## 安全机制

推荐安装的 Skill 会经过自动安全扫描（基于 skill-vetter 协议）：

- **已安装 Skill**：代码级扫描（25+ 红旗规则）
- **未安装 Skill**：元数据级检查（作者、更新时间等）
- 🔴 高危 Skill 自动从推荐列表移除
- 扫描结果缓存 7 天，推荐结果缓存 24 小时

## 零配置原则

所有外部组件均为可选，缺失时优雅降级：

- 没有 Mem0？照样评估，只是少一个数据源
- 没有 Session 日志？没问题，用工作空间文件评估
- 有啥用啥，不报错不报❌

## License

MIT
