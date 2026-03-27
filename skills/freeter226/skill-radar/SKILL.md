---
name: skill-radar
description: 扫描、洞察、优化你的 AI 技能生态。一键诊断 Skill 使用情况、发现需求缺口、检查版本更新。Trigger on "skill检查", "skill雷达", "skill管理", "skill诊断", "skill优化", "检查skill", "skill radar", "skill usage".
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins: ["python3", "openclaw"]
---

# Skill Radar 📡

> 你的 AI 技能管家 — 让每一个安装的 Skill 都物尽其用

## 核心理念

**让用户使用 Skill 变得更简单更高效。**

- **更简单** — 一条命令看清全貌，不再迷失在100+个Skill里
- **更高效** — 精准识别闲置与缺口，每一分投入都有回报
- **更智能** — 基于真实使用数据做判断，不是拍脑袋

## 触发条件

- "检查skill"、"skill雷达"、"skill诊断"、"skill管理"、"skill优化"
- "skill usage"、"skill radar"、"skill insight"
- "哪些skill没用到"、"要不要装这个skill"、"skill需不需要更新"

## 功能

| 命令 | 说明 |
|------|------|
| `usage` | 📊 使用价值评估（基于6大数据源） |
| `status` | 📋 Missing/Ready 状态检查 |
| `recommend` | 💡 智能推荐（基于历史对话发现需求缺口） |
| `versions` | 🔄 版本更新检查 |
| `all` | 完整报告（以上四项） |

## 使用方法

```bash
# 完整报告（推荐首次使用）
python3 <skill-path>/scripts/health_check.py all

# 单项检查
python3 <skill-path>/scripts/health_check.py usage       # 使用价值评估
python3 <skill-path>/scripts/health_check.py status      # 状态检查
python3 <skill-path>/scripts/health_check.py recommend   # 智能推荐
python3 <skill-path>/scripts/health_check.py versions    # 版本检查

# 输出为 Markdown 文件
python3 <skill-path>/scripts/health_check.py all > report.md
```

## 使用价值评估说明

整合6大数据源推断每个Skill的使用情况：

| 数据源 | 内容 | 权重 |
|--------|------|------|
| Mem0 记忆 | 用户主动记录的重要信息 | ⭐⭐⭐ |
| 每日记忆 | 当天事件、决策、进展 | ⭐⭐⭐ |
| MEMORY.md | 核心配置、偏好 | ⭐⭐⭐ |
| HEARTBEAT.md | 定期任务配置 | ⭐⭐ |
| Session 日志 | 原始对话记录 | ⭐⭐ |
| AGENTS.md | 工作规则 | ⭐⭐ |

评分：🔵 高频（核心工具）/ 🟢 中频 / 🟡 低频 / 🔴 未使用

## 依赖

- Python 3.8+（纯标准库，无外部依赖）
- OpenClaw CLI（`openclaw`）
- ClawHub CLI（`npx clawhub`，仅版本检查需要）
