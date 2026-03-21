# GitHub Collaboration Skill

GitHub 多 Agent 协作开发技能，支持自动化需求分析、任务拆分、Agent 分配和进度跟踪。

## 功能特性

1. **多 Agent 协作**
   - Main Agent: 需求接收、GitHub 项目创建、任务分配
   - Dev Agent: 代码开发任务执行
   - Test Agent: 测试验证任务执行
   - 每个 Agent 有独立的任务队列

2. **GitHub 集成**
   - 使用 `gh` 工具自动创建 GitHub 仓库
   - 关联 GitHub 项目与本地任务
   - 支持项目进度同步

3. **任务管理系统**
   - SQLite 数据库存储
   - 任务状态追踪
   - Agent 任务队列
   - 任务分配记录

4. **进度报告**
   - 生成 Markdown 格式报告
   - 实时进度统计
   - Agent 状态监控

## 安装

```bash
npm install github-collab-skill
```

## 使用示例

### 1. 创建项目

```javascript
const skill = require('github-collab-skill');

// 创建项目（自动使用 gh 工具创建 GitHub 仓库）
const project = await skill.createProject(
    '开发一个 Todo 应用，支持增删改查功能',
    'Todo App',
    null // 不提供 URL，系统自动创建
);

console.log(`项目已创建：${project.projectName}`);
console.log(`GitHub URL: ${project.githubUrl}`);
console.log(`任务数：${project.taskCount}`);
```

### 2. 获取项目报告

```javascript
const report = await skill.getProjectReport(projectId);
console.log(report);
```

### 3. 列出所有项目

```javascript
const projects = await skill.listProjects();
console.log(`共有 ${projects.length} 个项目`);
```

## 架构说明

### 数据流

```
用户输入需求
    ↓
Main Agent (需求分析)
    ↓
使用 gh 工具创建 GitHub 仓库
    ↓
STP Integrator (任务拆分)
    ↓
Task Manager (创建任务记录)
    ↓
分配任务给 Agent (添加到 Agent 任务队列)
    ↓
Dev Agent / Test Agent (从自己的队列获取任务并执行)
    ↓
Task Manager (更新任务状态)
    ↓
生成进度报告
```

### Agent 任务队列

每个 Agent 有独立的任务队列表 `agent_task_queue`：

- `agent_name`: Agent 名称
- `task_id`: 任务 ID
- `status`: queued / in_progress / completed / failed
- `assigned_at`: 分配时间
- `started_at`: 开始时间
- `completed_at`: 完成时间

### 任务分配流程

1. Main Agent 接收需求
2. 使用 `gh repo create` 创建 GitHub 仓库
3. 在数据库中创建项目记录
4. STP Integrator 拆分任务
5. 为每个任务创建数据库记录
6. 调用 `assignTaskToAgent(taskId, agentName)` 分配任务
7. 任务被添加到 Agent 的 `agent_task_queue` 表
8. Agent 通过 `getAgentNextTask(agentName)` 从自己的队列获取任务

## 数据库表结构

### projects
- 项目基本信息

### tasks
- 任务记录（关联项目）
- `assigned_agent`: 记录任务分配给哪个 Agent

### agents
- Agent 注册信息
- `current_task_id`: 当前执行的任务

### agent_task_queue
- 每个 Agent 的任务队列
- 记录任务分配和执行状态

### task_logs
- 任务活动日志

## 配置

```javascript
const skill = require('github-collab-skill');

// 配置 QQ 通知
skill.configure({
    qqToken: process.env.QQ_TOKEN
});
```

## 测试

```bash
npm test
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT