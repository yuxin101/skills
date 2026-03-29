# DeepSleep 阶段一：深度睡眠打包指令

## 第0步：发现所有活跃 session
用 sessions_list(kinds=['group'], activeMinutes=1440, messageLimit=1) 获取过去24小时所有活跃的群。
用 sessions_list(kinds=['main'], messageLimit=5) 获取主 session（DM）。
新群自动纳入，记录到 TOOLS.md。

## 第1步：拉取对话历史
对每个活跃 session 用 sessions_history(sessionKey=<key>, limit=100) 拉取当天对话。

## 第2步：按筛选标准生成摘要
对每段对话内容，用以下标准决定保留什么：
- ✅ **决策** — 影响后续工作的决定 → 保留
- ✅ **教训** — 踩过的坑、解决方案 → 保留
- ✅ **偏好** — Jeffrey的偏好和工作习惯 → 保留
- ✅ **关系** — 谁做了什么、联系方式 → 保留
- ✅ **进展** — 项目进度、完成的里程碑 → 保留
- ❌ **临时** — 天气、心跳、例行操作 → 跳过
- ❌ **已有** — MEMORY.md 里已经记录的 → 跳过

## 第3步：Schedule 远期记忆
对话中提到的远期事项写入 ~/clawd/memory/schedule.md：
  格式：| YYYY-MM-DD | 来源 | 事项 | pending |
每次打包时检查 schedule.md，到期事项写入当天摘要。

## 第4步：写入 memory/YYYY-MM-DD.md
追加 `## 每日摘要（DeepSleep）` 章节，包含：

### [群名]
- 精炼摘要（不逐条复制原文）

### 直接对话
- （如有DM内容）

### 🔮 Open Questions
- 尚未解决的、值得持续思考的问题
- 这些问题会在后续每日摘要中跟踪

### 📋 Tomorrow
- 明确的、可执行的下一步行动
- 从当天讨论和待办中提炼

### 待办
- [ ] 即时 action items

## 第5步：更新长期记忆
回顾近几天 memory 文件，更新 ~/clawd/MEMORY.md：
- **Merge not append**：已有章节原地更新，不追加重复段落
- 移除过时信息
- 保持精炼
