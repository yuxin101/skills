# GitHub Collaboration

GitHub 项目协作开发系统 - 多 Agent 协作完成 GitHub 项目开发任务

## 📋 目录

- [快速开始](#快速开始)
- [安装指南](#安装指南)
- [项目结构](#项目结构)
- [功能特性](#功能特性)
- [使用示例](#使用示例)
- [测试验证](#测试验证)
- [配置说明](#配置说明)
- [常见问题](#常见问题)

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/openclaw/github-collab.git
cd github-collab
```

### 2. 安装依赖

```bash
npm install
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

### 4. 运行测试

```bash
npm test
```

### 5. 启动系统

```bash
npm start
```

## 📦 安装指南

详细安装步骤请参考 [INSTALL.md](INSTALL.md)

### 系统要求

- Node.js >= 14.0.0
- npm >= 6.0.0
- SQLite3 支持

### 依赖包

| 包名 | 版本 | 用途 |
|------|------|------|
| better-sqlite3 | ^9.0.0 | SQLite 数据库操作 |

### 安装检查清单

- [ ] Node.js 已安装（版本 >= 14.0.0）
- [ ] npm 已安装（版本 >= 6.0.0）
- [ ] 依赖已安装（`npm install` 成功）
- [ ] 环境变量已配置（`.env` 文件存在）
- [ ] 项目配置已创建（`core/.github-collab-config.json`）
- [ ] 测试通过（`npm test` 成功）

## 📁 项目结构

```
github-collab/
├── README.md                    # 项目总说明
├── INSTALL.md                   # 安装指南
├── package.json                 # 项目配置
├── .gitignore
├── .env.example                 # 环境变量示例
├── core/                        # 核心模块
│   ├── main-controller.js       # 主控制器
│   ├── agent-registry.js        # Agent 注册表
│   ├── task-manager.js          # 任务管理器
│   ├── task-manager-enhanced.js # 增强版任务管理器
│   ├── stp-integrator.js        # STP 集成
│   ├── stp-integrator-enhanced.js # 增强版 STP
│   └── openclaw-message.js      # OpenClaw 消息工具
├── agents/                      # Agent 模块
│   ├── dev-agent.js             # 开发 Agent
│   ├── test-agent.js            # 测试 Agent
│   ├── main-agent.js            # 主 Agent
│   └── agent-worker.js          # Agent 工作器
├── tests/                       # 测试文件
│   ├── test-all.js              # 完整测试套件
│   ├── test-task-manager.js     # TaskManager 测试
│   ├── test-agent-binding.js    # Agent 绑定测试
│   ├── test-stp-integration.js  # STP 集成测试
│   └── TESTING_GUIDE.md         # 测试指南
├── examples/                    # 示例代码
│   ├── basic-example.js         # 基础示例
│   ├── complete-example.js      # 完整示例
│   └── stp-example.js           # STP 集成示例
├── scripts/                     # 脚本文件
│   ├── main.js                  # 主脚本
│   ├── scheduler.js             # 调度器
│   └── task-breakdown.js        # 任务拆分
├── utils/                       # 工具函数
│   └── openclaw-message-tool.js # OpenClaw 消息工具
└── docs/                        # 文档
    ├── AGENT_BINDING_GUIDE.md   # Agent 绑定指南
    └── AGENT_BINDING_ANALYSIS.md # 分析报告
```

## ✨ 功能特性

### 1. 任务管理

- ✅ 任务创建、分配、执行
- ✅ 任务依赖管理
- ✅ 并发锁机制
- ✅ 崩溃恢复
- ✅ 性能优化（批量创建、缓存、索引）

### 2. 多 Agent 协作

- ✅ Dev Agent - 代码开发
- ✅ Test Agent - 单元测试
- ✅ Review Agent - 代码审查（规划中）
- ✅ Deploy Agent - 自动部署（规划中）

### 3. STP 任务规划

- ✅ 任务自动拆分
- ✅ 依赖关系验证
- ✅ 执行计划生成
- ✅ 资源估算

### 4. 消息通知

- ✅ QQ 消息通知
- ✅ 进度更新
- ✅ 任务完成通知
- ✅ 错误通知

## 📖 使用示例

### 基础示例

```javascript
const { TaskManagerEnhanced, DevAgent, TestAgent } = require('./core');

// 创建任务管理器
const taskManager = new TaskManagerEnhanced();

// 创建项目
const project = await taskManager.createProject({
    name: 'My Project',
    description: 'A sample project',
    github_url: 'https://github.com/example/repo'
});

// 创建任务
const task = await taskManager.createTask({
    project_id: project.id,
    name: 'Implement feature',
    description: 'Implement new feature',
    priority: 10
});

// 启动 Agent
const devAgent = new DevAgent('dev-agent');
await devAgent.initialize();
await devAgent.processQueue();
```

### 任务依赖示例

```javascript
// 创建开发任务
const devTask = await taskManager.createTask({
    name: 'Implement feature',
    type: 'development'
});

// 创建测试任务
const testTask = await taskManager.createTask({
    name: 'Test feature',
    type: 'testing'
});

// 添加依赖关系
taskManager.addTaskDependency(testTask.id, devTask.id);

// 检查依赖是否满足
const dependenciesMet = taskManager.checkTaskDependencies(testTask.id);
if (dependenciesMet) {
    await taskManager.assignTask(testTask.id, 'test-agent');
}
```

### STP 集成示例

```javascript
const { STPIntegratorEnhanced } = require('./core/stp-integrator-enhanced');

const stp = new STPIntegratorEnhanced();

// 拆分任务
const result = await stp.splitTask(
    'Build a web application with user authentication',
    'Node.js, Express, MongoDB',
    { deadline: '2024-12-31' }
);

console.log('拆分后的任务:', result.tasks);
console.log('执行计划:', result.executionPlan);
```

## 🧪 测试验证

### 运行所有测试

```bash
npm test
```

### 运行特定测试

```bash
# TaskManager 测试
npm run test:basic

# Agent 绑定测试
npm run test:agent

# STP 集成测试
npm run test:stp

# 完整测试套件
node tests/test-all.js
```

### 测试覆盖范围

- ✅ TaskManager 基础功能
- ✅ Agent 绑定机制
- ✅ MainController 控制
- ✅ STP 任务规划
- ✅ 性能测试

详细测试指南请参考 [tests/TESTING_GUIDE.md](tests/TESTING_GUIDE.md)

## ⚙️ 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|-------|------|--------|
| GITHUB_TOKEN | GitHub API Token | - |
| GITHUB_OWNER | GitHub 用户名 | default-owner |
| DEV_AGENT_COUNT | Dev Agent 数量 | 2 |
| TEST_AGENT_COUNT | Test Agent 数量 | 1 |
| REVIEW_AGENT_COUNT | Review Agent 数量 | 1 |
| LOG_LEVEL | 日志级别 | info |
| QQ_ENABLED | 启用 QQ 通知 | false |
| QQ_TOKEN | QQ Token | - |
| QQ_TARGET | QQ 目标用户 | - |

### 配置文件

创建 `core/.github-collab-config.json` 文件：

```json
{
    "github": {
        "token": "your_token",
        "owner": "your_username"
    },
    "agents": {
        "dev_count": 2,
        "test_count": 1
    },
    "logging": {
        "level": "info"
    },
    "max_parallel_agents": 3
}
```

## 🔧 常见问题

### 问题 1: better-sqlite3 安装失败

**解决方案：**

```bash
# 安装 Python 和构建工具
sudo apt-get install python3 build-essential

# 重新安装
npm install better-sqlite3
```

### 问题 2: 数据库文件权限错误

**解决方案：**

```bash
# 修改数据库文件权限
chmod 666 github-collab.db
```

### 问题 3: Agent 无法启动

**解决方案：**

1. 检查配置文件是否正确
2. 检查环境变量是否设置
3. 查看日志文件：`core/controller-state.json`

### 问题 4: 测试失败

**解决方案：**

1. 检查数据库文件权限
2. 清理缓存：`rm -rf core/*.db`
3. 重新安装依赖：`npm install`

## 📊 性能指标

| 操作 | 时间 |
|------|------|
| 任务创建 | ~1ms |
| 任务分配 | ~2ms |
| 并发锁 | ~0.5ms |
| 缓存命中率 | ~90% |
| 数据库查询 | ~5ms |

## 📝 更新日志

### v1.0.0 (2024-12-19)

- ✅ 初始版本发布
- ✅ 任务管理功能
- ✅ 多 Agent 协作
- ✅ STP 任务规划
- ✅ QQ 消息通知
- ✅ 完整测试套件
- ✅ 安装指南

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 技术支持

如有问题，请提交 Issue 或联系 OpenClaw 社区。
