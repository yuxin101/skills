---
name: tech-radar-daily
description: "每日技术情报雷达 - 自动发现有趣工具、技术趋势、赚钱项目。扫描 GitHub Trending、Product Hunt、Hacker News、Awesome Lists，智能评分筛选高价值项目，每日推送 7-9 条精选情报到飞书。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📡",
        "requires": { "env": ["FEISHU_WEBHOOK_URL"] },
        "install":
          [
            {
              "id": "manual",
              "kind": "manual",
              "label": "手动配置环境变量",
              "steps": ["在 ~/.zshrc 中添加: export FEISHU_WEBHOOK_URL=\"你的飞书Webhook URL\""]
            }
          ],
        "actions":
          {
            "run": { "command": "node scripts/run-cycle.js", "description": "运行每日技术情报扫描" },
            "test": { "command": "node scripts/run-cycle.js --test", "description": "测试模式运行（不推送飞书）" }
          }
      }
  }
---

# Tech Radar Daily

每日技术情报雷达 - 自动发现有趣工具、技术趋势、赚钱项目

## 功能

- 🔍 扫描 GitHub Trending、Product Hunt、Hacker News、Awesome Lists
- 📊 智能评分筛选高价值项目（趋势热度 + 历史影响 + AI属性 + 大厂加分）
- 🚀 每日推送 7-9 条精选情报到飞书
- 🔄 自动去重，7 天内不重复推荐
- ⏰ 自动运行，每天 09:00 Cron 定时任务

## 使用方法

### 手动运行
```bash
cd /Users/mini/.openclaw/workspace/skills/tech-radar-daily
node scripts/run-cycle.js
```

### 测试模式（不推送飞书）
```bash
node scripts/run-cycle.js --test
```

### 定时任务
```bash
# 已配置：每天 09:00 自动运行
```

## ⚠️ Gotchas（常见陷阱）

### 🔴 高风险

- ❌ **不要忘记设置 Cron timeout**
 ✅ 正确做法：`openclaw cron add --timeout 650`

- ❌ **不要重复推荐同一项目（7 天内）**
 ✅ 正确做法：维护 seen_repos 数据库

### 🟡 中风险

- ❌ **不要一次性抓取太多数据**
 ✅ 正确做法：每个情报源限制 20 个候选

- ❌ **不要忘记置信度标注**
 ✅ 正确做法：每条情报标注 🟢🟡🟠

## 配置

环境变量：
- `FEISHU_WEBHOOK_URL`: 飞书机器人 webhook 地址（必需）
- `HTTP_PROXY`: 代理地址（可选）
- `GITHUB_TOKEN`: GitHub API Token（可选，提高限额）

代理说明：
- 如果已配置本地 Clash（系统代理），无需设置 `HTTP_PROXY`
- 如果需要指定代理：`export HTTP_PROXY=http://127.0.0.1:7890`
