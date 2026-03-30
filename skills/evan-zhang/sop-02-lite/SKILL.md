---
name: sop-02-lite
description: 轻量级 SOP 执行框架。适用于预计 20 分钟内、单系统、单次确认的简单任务。触发词："创建 SOP"、"开始 SOP"、"快速任务"。超过范围（预计>20分钟/改2+系统/发布重启/多轮确认/跨gateway）时提示升级到 SOP-01。
---

# SOP-02-Lite: 轻量级任务执行框架

## 快速评估（创建前必问）

在创建实例前，询问用户以下问题：

1. **预计耗时**：这个任务大概需要多长时间？
2. **涉及系统**：需要操作几个系统/服务？

**升级判断**（满足任一条件拒绝创建，提示使用 SOP-01）：
- 预计耗时 > 20 分钟
- 涉及 ≥ 2 个系统
- 需要发布/重启操作
- 需要多轮人工确认
- 需要跨 gateway 操作

## 实例创建流程

### 1. 检查根目录

```bash
mkdir -p ~/.openclaw/sop-instances/
```

### 2. 原子性创建实例目录

**命名规则**：`SOP-YYYYMMDD-NNN`
- 日期：当天日期（YYYYMMDD）
- 序号：扫描当天已有实例，取最大序号 + 1（从 001 开始）
- **文件锁**：使用 flock 防止并发冲突

**实现**：调用 `scripts/init_instance.py`
```bash
python3 scripts/init_instance.py \
  --title "任务标题" \
  --owner "factory-orchestrator" \
  --root ~/.openclaw/sop-instances/
```

### 3. 初始化文件

自动创建以下文件（从 templates/ 复制）：
- `TASK.md`：任务定义
- `LOG.md`：执行日志
- `RESULT.md`：结果留痕
- `state.json`：状态追踪

## 5 步执行流程

### Step 1: 目标确认（TARGET）
- 明确任务目标
- 记录到 TASK.md
- state.json: `stage = "TARGET"`

### Step 2: 计划制定（PLAN）
- 制定执行步骤
- 识别风险点
- state.json: `stage = "PLAN"`

### Step 3: 确认单生成（CHECKLIST）
- 列出关键操作项
- 请求用户确认
- state.json: `stage = "CHECKLIST"`

### Step 4: 执行实施（EXECUTE）
- 按计划执行
- 实时更新 LOG.md
- state.json: `stage = "EXECUTE"`
- **超出范围时**：标记 `status = "UPGRADED"`，提示升级到 SOP-01

### Step 5: 结果留痕（ARCHIVE）
- 填写 RESULT.md
- 总结执行情况
- state.json: `stage = "ARCHIVE"`, `status = "DONE"`

## 执行前确认单门禁（R010）

在 **Step 4 执行前**，必须完成确认单。

- 若确认单未完成，`update_state.py` 拒绝进入 `RUNNING`（例如 `--status RUNNING` 或 `--stage RUNNING`）
- 建议在 `state.json` 维护 `checklistConfirmed` 字段：
  - `true`：允许进入 RUNNING
  - `false`：拒绝进入 RUNNING

## 高风险操作显式确认（R010）

以下操作属于高风险，必须传 `--confirm`，否则脚本退出码为 1 并提示：
`高风险操作需要显式确认，请加 --confirm 参数`

高风险范围：
1. owner 切换（`--owner` 导致 owner 变化）
2. 状态设置为 `DONE / ARCHIVED / UPGRADED`

## 主 Agent 回执隔离（R008）

- 子 Agent 执行过程的中间细节，**全部写入 `LOG.md`**
- 主 Agent 只从 `RESULT.md` 读取最终结果摘要
- **禁止主 Agent 轮询 `LOG.md` 中间过程**（避免干扰执行与重复解读）

## 状态管理

### state.json 字段
```json
{
  "id": "SOP-20260328-001",
  "title": "任务标题",
  "owner": "factory-orchestrator",
  "status": "DISCUSSING | READY | RUNNING | BLOCKED | PAUSED | DONE | ARCHIVED | HANDOVER_PENDING | UPGRADED",
  "stage": "TARGET | PLAN | CHECKLIST | EXECUTE | ARCHIVE | RUNNING | DONE",
  "createdAt": "2026-03-28T10:00:00Z",
  "updatedAt": "2026-03-28T10:30:00Z",
  "reason": "状态变更原因（可选）",
  "checklistConfirmed": true
}
```

### status 与 stage 职责边界

- `status`：任务运行状态（是否在执行、阻塞、暂停、完成、归档、升级等）
- `stage`：流程阶段位置（目标/计划/确认/执行/归档）

## 状态变更脚本

**更新状态**：
```bash
python3 scripts/update_state.py \
  --instance-path ~/.openclaw/sop-instances/SOP-20260328-001 \
  --status RUNNING \
  --stage RUNNING \
  --reason "开始执行"
```

**语义化操作**：
```bash
python3 scripts/update_state.py --instance-path <path> --action pause
python3 scripts/update_state.py --instance-path <path> --action resume
python3 scripts/update_state.py --instance-path <path> --action shelve --reason "等待外部输入"
python3 scripts/update_state.py --instance-path <path> --action restart --reason "阻塞解除"
```

**交接任务**：
```bash
python3 scripts/handover.py \
  --instance-path ~/.openclaw/sop-instances/SOP-20260328-001 \
  --from-owner factory-orchestrator \
  --to-owner validator \
  --reason "需要技术验证" \
  --next-steps "检查配置文件正确性"
```

## 升级机制

当任务执行中发现超出 lite 范围时：

1. **立即停止**：不再继续执行
2. **标记状态**：`status = "UPGRADED"`
3. **通知用户**：说明升级原因
4. **记录原因**：在 LOG.md 中详细记录
5. **建议升级**：引导用户创建 SOP-01 实例

## 与 SOP-01 的区别

| 维度 | SOP-02-Lite | SOP-01 |
|------|-------------|--------|
| 耗时 | ≤ 20 分钟 | 无限制 |
| 系统数 | 1 个 | 多个 |
| 确认轮次 | 1 次 | 多轮 |
| 风险等级 | 低 | 中-高 |
| 适用场景 | 快速任务 | 正式发布 |

## 注意事项

1. **严格评估**：创建前必须评估，不满足条件坚决升级
2. **原子性**：实例创建使用文件锁，防止并发冲突
3. **完整留痕**：即使 lite 也必须有完整记录
4. **及时升级**：发现超范围立即停止，不强行执行
5. **状态同步**：每次变更都更新 state.json

---

*Agent Factory - SOP-02-Lite v1.1*
