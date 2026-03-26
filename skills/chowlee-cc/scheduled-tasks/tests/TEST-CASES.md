# Test Cases | 测试用例

> **OpenClaw Scheduler Skill | 定时任务技能**  
> Version | 版本：1.0.0

---

## Test Overview | 测试概述

This document describes comprehensive test cases for the OpenClaw Scheduler skill. Tests cover functionality, documentation, security, and compatibility.

本文档描述 OpenClaw 定时任务技能的综合测试用例。测试涵盖功能、文档、安全性和兼容性。

### Test Categories | 测试类别

| Category | Count | Description |
|----------|-------|-------------|
| Functional Tests | 8 | Core functionality validation |
| Documentation Tests | 3 | Documentation quality checks |
| Security Tests | 2 | Sensitive data detection |
| Integration Tests | 4 | End-to-end workflows |
| **Total** | **17** | |

| 类别 | 数量 | 说明 |
|------|------|------|
| 功能测试 | 8 | 核心功能验证 |
| 文档测试 | 3 | 文档质量检查 |
| 安全测试 | 2 | 敏感数据检测 |
| 集成测试 | 4 | 端到端工作流 |
| **总计** | **17** | |

---

## Functional Tests | 功能测试

### F1: OpenClaw CLI Availability | OpenClaw CLI 可用性

**Objective | 目标**: Verify OpenClaw CLI is installed and accessible.  
验证 OpenClaw CLI 已安装并可访问。

**Steps | 步骤**:
```bash
openclaw --version
```

**Expected Result | 预期结果**:
- Command executes successfully | 命令成功执行
- Version number is displayed | 显示版本号

**Pass Criteria | 通过标准**:
- Exit code is 0 | 退出码为 0
- Output contains version string | 输出包含版本字符串

---

### F2: Cron List Command | Cron List 命令

**Objective | 目标**: Verify cron list command works.  
验证 cron list 命令正常工作。

**Steps | 步骤**:
```bash
openclaw cron list
```

**Expected Result | 预期结果**:
- Command executes successfully | 命令成功执行
- Returns task list (may be empty) | 返回任务列表（可能为空）

**Pass Criteria | 通过标准**:
- Exit code is 0 | 退出码为 0
- No error messages | 无错误信息

---

### F3: Create One-Time Reminder | 创建一次性提醒

**Objective | 目标**: Verify one-time reminder creation.  
验证一次性提醒创建。

**Steps | 步骤**:
```bash
openclaw cron add \
  --name "test-reminder-$(date +%s)" \
  --at "5m" \
  --session main \
  --system-event "Test reminder" \
  --wake now \
  --delete-after-run
```

**Expected Result | 预期结果**:
- Task is created successfully | 任务成功创建
- Task appears in cron list | 任务出现在 cron 列表中
- Task executes after 5 minutes | 任务在 5 分钟后执行

**Pass Criteria | 通过标准**:
- Task ID is returned | 返回任务 ID
- `openclaw cron list` shows the task | cron list 显示该任务
- Task executes and auto-deletes | 任务执行并自动删除

---

### F4: Create Recurring Task | 创建周期性任务

**Objective | 目标**: Verify recurring task creation.  
验证周期性任务创建。

**Steps | 步骤**:
```bash
openclaw cron add \
  --name "test-recurring-$(date +%s)" \
  --cron "*/30 * * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "Test recurring task" \
  --delete-after-run
```

**Expected Result | 预期结果**:
- Task is created with cron schedule | 任务按 cron 计划创建
- Timezone is set correctly | 时区正确设置

**Pass Criteria | 通过标准**:
- Task ID is returned | 返回任务 ID
- Cron expression is valid | Cron 表达式有效
- Timezone is Asia/Shanghai | 时区为 Asia/Shanghai

---

### F5: Manual Task Execution | 手动任务执行

**Objective | 目标**: Verify manual task execution.  
验证手动任务执行。

**Steps | 步骤**:
```bash
# Create task first | 先创建任务
openclaw cron add \
  --name "test-manual-run" \
  --at "1h" \
  --session main \
  --system-event "Test" \
  --wake now

# Get task ID | 获取任务 ID
JOB_ID=$(openclaw cron list | grep "test-manual-run" | awk '{print $1}')

# Run manually | 手动运行
openclaw cron run $JOB_ID
```

**Expected Result | 预期结果**:
- Task executes immediately | 任务立即执行
- Run history is updated | 运行历史已更新

**Pass Criteria | 通过标准**:
- Exit code is 0 | 退出码为 0
- Run appears in history | 运行出现在历史中

---

### F6: Task Edit | 任务编辑

**Objective | 目标**: Verify task editing.  
验证任务编辑。

**Steps | 步骤**:
```bash
# Create task | 创建任务
openclaw cron add --name "test-edit" --at "1h" ...

# Get task ID | 获取任务 ID
JOB_ID=$(openclaw cron list | grep "test-edit" | awk '{print $1}')

# Edit task | 编辑任务
openclaw cron edit $JOB_ID --enabled false
```

**Expected Result | 预期结果**:
- Task is disabled | 任务被禁用
- Configuration is updated | 配置已更新

**Pass Criteria | 通过标准**:
- `openclaw cron list` shows enabled=false | cron list 显示 enabled=false

---

### F7: Task Removal | 任务删除

**Objective | 目标**: Verify task deletion.  
验证任务删除。

**Steps | 步骤**:
```bash
# Create task | 创建任务
openclaw cron add --name "test-remove" --at "1h" ...

# Get task ID | 获取任务 ID
JOB_ID=$(openclaw cron list | grep "test-remove" | awk '{print $1}')

# Remove task | 删除任务
openclaw cron remove $JOB_ID
```

**Expected Result | 预期结果**:
- Task is deleted | 任务被删除
- Task no longer appears in list | 任务不再出现在列表中

**Pass Criteria | 通过标准**:
- Exit code is 0 | 退出码为 0
- `openclaw cron list` doesn't show task | cron list 不显示该任务

---

### F8: Run History | 运行历史

**Objective | 目标**: Verify run history retrieval.  
验证运行历史检索。

**Steps | 步骤**:
```bash
# Get run history | 获取运行历史
openclaw cron runs --id <jobId>
```

**Expected Result | 预期结果**:
- Run history is displayed | 显示运行历史
- Includes timestamps and status | 包含时间戳和状态

**Pass Criteria | 通过标准**:
- Exit code is 0 | 退出码为 0
- Output contains run entries | 输出包含运行条目

---

## Documentation Tests | 文档测试

### D1: Bilingual Content Check | 双语内容检查

**Objective | 目标**: Verify documentation is bilingual.  
验证文档是双语的。

**Steps | 步骤**:
```bash
# Check for Chinese characters | 检查中文字符
grep -P '[\x{4e00}-\x{9fff}]' SKILL.md

# Check for English sections | 检查英文章节
grep -E "Overview|Quick Start|Examples" SKILL.md
```

**Expected Result | 预期结果**:
- Contains Chinese text | 包含中文文本
- Contains English text | 包含英文文本

**Pass Criteria | 通过标准**:
- Both languages present | 两种语言都存在
- Sections are parallel | 章节平行对应

---

### D2: Required Sections Check | 必需章节检查

**Objective | 目标**: Verify all required sections exist.  
验证所有必需章节存在。

**Required Sections | 必需章节**:
- name/description | 名称/描述
- Quick Start | 快速开始
- Method 1 (OpenClaw Cron) | 方式一
- Method 2 (System Crontab) | 方式二
- Pitfalls/Solutions | 陷阱/解决方案
- Troubleshooting | 故障排查
- Examples | 示例

**Steps | 步骤**:
```bash
for section in "name:" "Quick Start" "Method 1" "Method 2" "Pitfall" "Troubleshooting"; do
  grep -q "$section" SKILL.md && echo "✓ $section" || echo "✗ $section"
done
```

**Pass Criteria | 通过标准**:
- All sections present | 所有章节都存在

---

### D3: No Sensitive Data | 无敏感数据

**Objective | 目标**: Verify no sensitive data in documentation.  
验证文档中无敏感数据。

**Patterns to Check | 检查模式**:
- `password=`
- `secret=`
- `token=`
- `api_key=`
- `access_token`
- `ou_[a-f0-9]{32}` (user OpenID)

**Steps | 步骤**:
```bash
grep -rE "(password=|secret=|token=|api_key=|access_token)" . --include="*.md"
```

**Expected Result | 预期结果**:
- No matches (except examples/templates) | 无匹配（示例/模板除外）

**Pass Criteria | 通过标准**:
- No sensitive data found | 未发现敏感数据

---

## Security Tests | 安全测试

### S1: Script Template Security | 脚本模板安全

**Objective | 目标**: Verify script template has no hardcoded secrets.  
验证脚本模板无硬编码密钥。

**Steps | 步骤**:
```bash
# Check template | 检查模板
cat scripts/daily-task.sh.template | grep -E "(password|secret|token|key)"
```

**Expected Result | 预期结果**:
- Only placeholder variables | 仅占位符变量
- No actual credentials | 无实际凭证

**Pass Criteria | 通过标准**:
- All credentials are parameterized | 所有凭证都已参数化

---

### S2: Directory Permission Check | 目录权限检查

**Objective | 目标**: Verify skill directory permissions.  
验证技能目录权限。

**Steps | 步骤**:
```bash
ls -la ~/.openclaw/workspace/skills/openclaw-scheduler/
```

**Expected Result | 预期结果**:
- Owner has read/write/execute | 所有者有读/写/执行权限
- Others have read/execute | 其他人有读/执行权限

**Pass Criteria | 通过标准**:
- Permissions are 755 or similar | 权限为 755 或类似

---

## Integration Tests | 集成测试

### I1: End-to-End Reminder Workflow | 端到端提醒工作流

**Objective | 目标**: Test complete reminder workflow.  
测试完整提醒工作流。

**Steps | 步骤**:
```bash
# 1. Create reminder | 创建提醒
openclaw cron add \
  --name "e2e-test-$(date +%s)" \
  --at "2m" \
  --session main \
  --system-event "E2E test reminder" \
  --wake now \
  --delete-after-run

# 2. Verify creation | 验证创建
openclaw cron list | grep "e2e-test"

# 3. Wait 2 minutes | 等待 2 分钟
sleep 120

# 4. Check execution | 检查执行
openclaw cron list | grep "e2e-test"  # Should be deleted
```

**Pass Criteria | 通过标准**:
- Task created | 任务已创建
- Task executed | 任务已执行
- Task auto-deleted | 任务自动删除

---

### I2: Crontab Script Integration | Crontab 脚本集成

**Objective | 目标**: Test crontab script execution.  
测试 crontab 脚本执行。

**Steps | 步骤**:
```bash
# 1. Create script from template | 从模板创建脚本
cp scripts/daily-task.sh.template /tmp/test-task.sh
sed -i 's/<agent-id>/main/' /tmp/test-task.sh
sed -i 's/<feishu-account-id>/default/' /tmp/test-task.sh
sed -i 's/<user_open_id>/test/' /tmp/test-task.sh

# 2. Make executable | 使可执行
chmod +x /tmp/test-task.sh

# 3. Run script | 运行脚本
/tmp/test-task.sh
```

**Pass Criteria | 通过标准**:
- Script executes without errors | 脚本执行无错误
- Logs are created | 日志已创建

---

### I3: Multi-Agent Coordination | 多 Agent 协调

**Objective | 目标**: Test task with specific agent.  
测试特定 Agent 的任务。

**Steps | 步骤**:
```bash
# 1. List available agents | 列出可用 Agent
openclaw agents list

# 2. Create task for specific agent | 为特定 Agent 创建任务
openclaw cron add \
  --name "agent-test" \
  --at "5m" \
  --agent <agent-id> \
  --message "Test" \
  --session isolated
```

**Pass Criteria | 通过标准**:
- Task assigned to correct agent | 任务分配给正确 Agent
- Agent can execute task | Agent 可执行任务

---

### I4: Timezone Validation | 时区验证

**Objective | 目标**: Test timezone handling.  
测试时区处理。

**Steps | 步骤**:
```bash
# 1. Check system timezone | 检查系统时区
date +%Z

# 2. Create task with Asia/Shanghai | 创建 Asia/Shanghai 任务
openclaw cron add \
  --name "tz-test" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --message "Test"

# 3. Verify timezone in task | 验证任务时区
openclaw cron list | grep -A5 "tz-test"
```

**Pass Criteria | 通过标准**:
- Timezone is correctly set | 时区正确设置
- Task schedule matches expectation | 任务计划符合预期

---

## Test Execution | 测试执行

### Automated Test Suite | 自动化测试套件

```bash
cd tests/
chmod +x test-scheduler.sh

# Run all tests | 运行所有测试
./test-scheduler.sh --all

# Run specific category | 运行特定类别
./test-scheduler.sh --quick    # Quick tests | 快速测试
./test-scheduler.sh --doc      # Documentation tests | 文档测试
```

### Manual Testing Checklist | 手动测试检查表

- [ ] F1: OpenClaw CLI available | OpenClaw CLI 可用
- [ ] F2: Cron list works | Cron list 正常
- [ ] F3: One-time reminder created | 一次性提醒已创建
- [ ] F4: Recurring task created | 周期性任务已创建
- [ ] F5: Manual execution works | 手动执行正常
- [ ] F6: Task edit works | 任务编辑正常
- [ ] F7: Task removal works | 任务删除正常
- [ ] F8: Run history accessible | 运行历史可访问
- [ ] D1: Bilingual content | 双语内容
- [ ] D2: Required sections | 必需章节
- [ ] D3: No sensitive data | 无敏感数据
- [ ] S1: Script template secure | 脚本模板安全
- [ ] S2: Permissions correct | 权限正确
- [ ] I1: E2E workflow | 端到端工作流
- [ ] I2: Crontab script | Crontab 脚本
- [ ] I3: Multi-agent | 多 Agent
- [ ] I4: Timezone | 时区

---

## Test Results Template | 测试结果模板

```markdown
## Test Run | 测试运行

**Date | 日期**: YYYY-MM-DD HH:MM  
**Tester | 测试者**: [Name]  
**Version | 版本**: 1.0.0

### Results | 结果

| Test ID | Status | Notes |
|---------|--------|-------|
| F1 | ✅ PASS | |
| F2 | ✅ PASS | |
| ... | ... | |

### Summary | 摘要

- Total: 17
- Passed: XX
- Failed: XX
- Skipped: XX

### Issues Found | 发现问题

[List any issues]

### Recommendations | 建议

[List any recommendations]
```

---

*Last Updated | 最后更新*: 2026-03-26  
*Version | 版本*: 1.0.0
