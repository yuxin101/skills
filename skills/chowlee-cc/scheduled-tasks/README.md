# OpenClaw Scheduler Skill | OpenClaw 定时任务技能

> **Version | 版本**: 2.1.0  
> **Bilingual | 双语**: English & Chinese  
> **License | 许可证**: MIT

[![ClawHub](https://img.shields.io/badge/ClawHub-available-blue)](https://clawhub.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Overview | 概述

A comprehensive OpenClaw skill for creating, managing, and troubleshooting scheduled tasks. Supports both OpenClaw Cron API and system crontab with best practices and extensive documentation.

一个全面的 OpenClaw 技能，用于创建、管理和调试定时任务。支持 OpenClaw Cron API 和系统 crontab，包含最佳实践和详尽文档。

### Features | 特性

- ✅ **Bilingual Documentation** - English & Chinese | 双语文档
- ✅ **Two Approaches** - OpenClaw Cron & System Crontab | 两种方式
- ✅ **Best Practices** - Proven patterns and templates | 最佳实践
- ✅ **Pitfall Guide** - Common issues and solutions | 避坑指南
- ✅ **Test Suite** - Comprehensive test scripts | 测试套件
- ✅ **No Sensitive Data** - Safe for public distribution | 无敏感数据

---

## Installation | 安装

### Option 1: From ClawHub (Recommended) | 方式一：从 ClawHub 安装（推荐）

```bash
clawhub install openclaw-scheduler
```

### Option 2: Manual Installation | 方式二：手动安装

```bash
# Clone or copy to skills directory | 克隆或复制到 skills 目录
git clone https://github.com/your-org/openclaw-scheduler.git
# OR: Copy folder to ~/.openclaw/workspace/skills/

# Verify installation | 验证安装
ls ~/.openclaw/workspace/skills/openclaw-scheduler/
```

### Option 3: Local Development | 方式三：本地开发

```bash
# Navigate to skills directory | 进入 skills 目录
cd ~/.openclaw/workspace/skills/

# Create skill directory | 创建技能目录
mkdir -p openclaw-scheduler/{scripts,tests,references}

# Copy files | 复制文件
cp /path/to/skill/* openclaw-scheduler/
```

---

## Quick Start | 快速开始

### Create One-Time Reminder | 创建一次性提醒

```bash
openclaw cron add \
  --name "Water Reminder | 喝水提醒" \
  --at "20m" \
  --session main \
  --system-event "Time to drink water! 💧 | 主人，该喝水了 💧" \
  --wake now \
  --delete-after-run
```

### Create Daily Scheduled Task | 创建每日定时任务

```bash
openclaw cron add \
  --name "Daily News | 每日新闻" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent <agent-id> \
  --message "Search today's news | 搜索今日新闻" \
  --announce \
  --channel feishu \
  --to "user:<user_open_id>"
```

### View Existing Tasks | 查看已有任务

```bash
openclaw cron list
```

---

## Documentation | 文档

| File | Description |
|------|-------------|
| [SKILL.md](SKILL.md) | Main skill documentation |
| [references/troubleshooting.md](references/troubleshooting.md) | Troubleshooting guide |
| [scripts/daily-task.sh.template](scripts/daily-task.sh.template) | Script template |
| [tests/test-scheduler.sh](tests/test-scheduler.sh) | Test suite |

| 文件 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 主要技能文档 |
| [references/troubleshooting.md](references/troubleshooting.md) | 故障排查指南 |
| [scripts/daily-task.sh.template](scripts/daily-task.sh.template) | 脚本模板 |
| [tests/test-scheduler.sh](tests/test-scheduler.sh) | 测试套件 |

---

## Usage Examples | 使用示例

### Example 1: Meeting Reminder | 会议提醒

```bash
openclaw cron add \
  --name "meeting-reminder | 会议提醒" \
  --at "2026-03-27T09:00:00+08:00" \
  --session main \
  --system-event "Meeting in 5 minutes! | 5 分钟后开会！" \
  --wake now \
  --delete-after-run
```

### Example 2: Daily News Briefing | 每日新闻播报

```bash
openclaw cron add \
  --name "daily-news | 每日新闻" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent <agent-id> \
  --message "Search today's news | 搜索今日新闻" \
  --announce \
  --channel feishu \
  --to "user:<user_open_id>"
```

### Example 3: Workday Report | 工作日简报

```bash
openclaw cron add \
  --name "workday-report | 工作日简报" \
  --cron "55 22 * * 1-5" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "Summarize today's work | 总结今日工作" \
  --announce \
  --channel feishu \
  --to "user:<user_open_id>"
```

---

## Testing | 测试

### Run Test Suite | 运行测试套件

```bash
# Navigate to test directory | 进入测试目录
cd ~/.openclaw/workspace/skills/openclaw-scheduler/tests/

# Make test script executable | 使测试脚本可执行
chmod +x test-scheduler.sh

# Run all tests | 运行所有测试
./test-scheduler.sh --all

# Run quick tests | 运行快速测试
./test-scheduler.sh --quick

# Run documentation tests | 运行文档测试
./test-scheduler.sh --doc
```

### Test Output | 测试输出

```
========================================
OpenClaw Scheduler Test Suite | 定时任务技能测试套件
========================================
INFO: Test started at | 测试开始时间：2026-03-26 16:30:00
INFO: Test log file | 测试日志文件：/tmp/scheduler-test-20260326-163000.log

TEST 1: Check OpenClaw CLI availability | 检查 OpenClaw CLI 可用性
✓ PASS: OpenClaw CLI is available | OpenClaw CLI 可用

TEST 2: List existing cron tasks | 列出已有定时任务
✓ PASS: Cron list command works | Cron list 命令正常

...

========================================
Test Summary | 测试摘要
========================================
INFO: Total tests run | 总测试数：10
INFO: Passed | 通过：10
INFO: Failed | 失败：0
INFO: Test log saved to | 测试日志保存至：/tmp/scheduler-test-20260326-163000.log

========================================
All tests passed! | 所有测试通过！
========================================
✓ SUCCESS
```

---

## Directory Structure | 目录结构

```
scheduled-tasks/
├── SKILL.md                          # Main documentation | 主要文档
├── README.md                         # This file | 本文件
├── LICENSE                           # License file | 许可证
├── scripts/
│   ├── task-manager.sh               # Task management tool | 任务管理工具
│   └── daily-task.sh.template        # Script template | 脚本模板
├── tests/
│   ├── test-scheduler.sh             # Test suite | 测试套件
│   ├── TEST-CASES.md                 # Test cases | 测试用例
│   ├── TEST-REPORT.md                # Test report | 测试报告
│   └── SENSITIVE-DATA-AUDIT.md       # Security audit | 安全审查
└── references/
    └── troubleshooting.md            # Troubleshooting guide | 故障排查
```

---

## Best Practices | 最佳实践

### 1. Always Specify Timezone | 始终指定时区

```bash
# ✅ Good | 好
openclaw cron add --cron "0 9 * * *" --tz "Asia/Shanghai" ...
openclaw cron add --at "2026-03-27T09:00:00+08:00" ...

# ❌ Bad | 不好
openclaw cron add --cron "0 9 * * *" ...  # Defaults to UTC
```

### 2. Use Descriptive Names | 使用描述性名称

```bash
# ✅ Good | 好
--name "daily-news-briefing-08:00 | 每日新闻播报 -08 点"

# ❌ Bad | 不好
--name "task1"
```

### 3. Test Before Deploying | 部署前测试

```bash
# Create test task | 创建测试任务
openclaw cron add --at "1m" ... --delete-after-run

# Verify | 验证
openclaw cron list

# Manual run | 手动运行
openclaw cron run <jobId>

# Check result | 检查结果
openclaw cron runs --id <jobId>
```

### 4. No Sensitive Data | 不含敏感数据

```bash
# ✅ Good | 好
# Use environment variables from ~/.openclaw/.env
# 使用~/.openclaw/.env 中的环境变量

# ❌ Bad | 不好
# Never hardcode tokens, passwords, or user IDs
# 切勿硬编码 token、密码或用户 ID
```

---

## Troubleshooting | 故障排查

See [references/troubleshooting.md](references/troubleshooting.md) for detailed troubleshooting guide.

详细故障排查指南请见 [references/troubleshooting.md](references/troubleshooting.md)。

### Quick Checks | 快速检查

```bash
# Task not running? | 任务未运行？
openclaw cron list

# Check run history | 检查运行历史
openclaw cron runs --id <jobId>

# Enable debug mode | 启用调试模式
export OPENCLAW_DEBUG=1
```

---

## Contributing | 贡献

1. Fork the repository | Fork 仓库
2. Create feature branch | 创建功能分支
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit changes | 提交更改
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push to branch | 推送到分支
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open Pull Request | 打开 Pull Request

---

## Changelog | 变更日志

### Version 2.1.0 (2026-03-26)

- ✅ Merged + Cleaned release | 合并清理版本
- ✅ Bilingual documentation (EN/CN) | 双语文档
- ✅ OpenClaw Cron API support | OpenClaw Cron API 支持
- ✅ System crontab support | 系统 crontab 支持
- ✅ Comprehensive test suite | 综合测试套件
- ✅ Troubleshooting guide | 故障排查指南
- ✅ Script templates | 脚本模板

---

## License | 许可证

MIT License - See [LICENSE](LICENSE) file for details.

---

## Support | 支持

- **Documentation | 文档**: https://docs.openclaw.ai
- **Community | 社区**: https://discord.com/invite/clawd
- **Skill Market | 技能市场**: https://clawhub.com
- **Issues | 问题**: https://github.com/your-org/openclaw-scheduler/issues

---

*Made with 💙 by OpenClaw Community*
