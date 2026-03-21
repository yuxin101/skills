/**
 * Main Controller - 总控主进程
 * 控制 Agent 启动、停止、并行数量、任务调度
 */

const path = require('path');
const fs = require('fs');
const { AgentRegistry } = require('./agent-registry');
const { TaskManagerEnhanced } = require('./task-manager-enhanced');

class MainController {
    constructor(config = {}) {
        this.config = {
            maxParallelAgents: config.maxParallelAgents || 3,
            agentTypes: config.agentTypes || ['dev', 'test', 'review'],
            autoRecovery: config.autoRecovery !== false,
            priorityThreshold: config.priorityThreshold || 5,
            ...config
        };
        
        // 使用 AgentRegistry 管理 Agent
        this.registry = new AgentRegistry();
        this.taskManager = new TaskManagerEnhanced();
        
        this.taskQueue = [];
        this.running = false;
        this.locks = new Map();
        this.recoveryAttempts = new Map();
        
        this.logger = this.createLogger();
    }

    /**
     * 创建日志器
     */
    createLogger() {
        return {
            info: (msg) => console.log(`[INFO] ${msg}`),
            warn: (msg) => console.warn(`[WARN] ${msg}`),
            error: (msg) => console.error(`[ERROR] ${msg}`),
            debug: (msg) => console.log(`[DEBUG] ${msg}`)
        };
    }

    /**
     * 初始化控制器
     */
    async initialize() {
        this.logger.info('Main Controller initializing...');
        
        // 加载配置
        await this.loadConfig();
        
        // 恢复未完成任务
        if (this.config.autoRecovery) {
            await this.recoverTasks();
        }
        
        this.logger.info('Main Controller initialized');
    }

    /**
     * 加载配置
     */
    async loadConfig() {
        const configPath = path.join(__dirname, '.github-collab-config.json');
        if (fs.existsSync(configPath)) {
            try {
                const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
                Object.assign(this.config, config);
                this.logger.info('Configuration loaded');
            } catch (error) {
                this.logger.error('Failed to load config:', error.message);
            }
        }
    }

    /**
     * 启动 Agent
     * @param {string} agentType - Agent 类型
     * @param {string} agentId - Agent ID
     * @param {object} options - 选项
     */
    async startAgent(agentType, agentId = null, options = {}) {
        // 检查并行数量限制
        const runningAgents = this.registry.getAll().length;
        if (runningAgents >= this.config.maxParallelAgents) {
            this.logger.warn(`Max parallel agents (${this.config.maxParallelAgents}) reached`);
            return null;
        }

        // 生成 Agent ID
        if (!agentId) {
            agentId = `${agentType}-agent-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        }

        // 使用 AgentRegistry 创建 Agent
        let agent;
        if (agentType === 'dev') {
            agent = this.registry.createDevAgent(agentId);
        } else if (agentType === 'test') {
            agent = this.registry.createTestAgent(agentId);
        } else {
            this.logger.error(`Unknown agent type: ${agentType}`);
            return null;
        }

        // 初始化 Agent
        await agent.initialize();
        this.logger.info(`Agent started: ${agentId} (type: ${agentType})`);
        return agent;
    }

    /**
     * 停止 Agent
     * @param {string} agentId - Agent ID
     */
    async stopAgent(agentId) {
        const agent = this.registry.get(agentId);
        if (!agent) {
            this.logger.warn(`Agent ${agentId} not found`);
            return false;
        }

        try {
            // 停止 Agent
            if (agent.shutdown) {
                await agent.shutdown();
            }
            
            // 从注册表移除
            this.registry.unregister(agentId);
            
            this.logger.info(`Agent ${agentId} stopped`);
            return true;
        } catch (error) {
            this.logger.error(`Failed to stop agent ${agentId}:`, error.message);
            return false;
        }
    }

    /**
     * 设置最大并行 Agent 数量
     * @param {number} count - 数量
     */
    setMaxParallelAgents(count) {
        this.config.maxParallelAgents = count;
        this.logger.info(`Max parallel agents set to ${count}`);
    }

    /**
     * 获取当前运行的 Agent 数量
     */
    getRunningAgentCount() {
        return this.registry.getAll().length;
    }

    /**
     * 添加任务到队列
     * @param {object} task - 任务对象
     * @param {string} agentType - 目标 Agent 类型
     */
    async addTask(task, agentType = 'dev') {
        // 检查依赖
        const dependenciesMet = await this.checkTaskDependencies(task);
        
        if (!dependenciesMet) {
            // 依赖未满足，降级优先级
            task.priority = Math.min(task.priority || 10, this.config.priorityThreshold - 1);
            this.logger.info(`Task ${task.id} dependencies not met, priority lowered to ${task.priority}`);
        }

        // 添加到队列
        this.taskQueue.push({
            task,
            agentType,
            addedAt: Date.now(),
            dependenciesMet
        });

        // 按优先级排序
        this.taskQueue.sort((a, b) => b.task.priority - a.task.priority);

        this.logger.info(`Task ${task.id} added to queue (priority: ${task.priority})`);
    }

    /**
     * 检查任务依赖
     */
    async checkTaskDependencies(task) {
        if (!task.dependencies || task.dependencies.length === 0) {
            return true;
        }

        for (const depId of task.dependencies) {
            const depTask = await this.taskManager.getTask(depId);
            if (!depTask || depTask.status !== 'completed') {
                return false;
            }
        }

        return true;
    }

    /**
     * 获取任务
     */
    async getTask(taskId) {
        return await this.taskManager.getTask(taskId);
    }

    /**
     * 分配任务给 Agent（核心绑定逻辑）
     * @param {number} taskId - 任务 ID
     * @param {string} agentId - Agent ID
     */
    async assignTask(taskId, agentId) {
        this.logger.info(`[MainController] Assigning task ${taskId} to agent ${agentId}`);
        
        try {
            // 1. 更新任务状态到数据库
            await this.taskManager.assignTaskToAgent(taskId, agentId);
            
            // 2. 通过 AgentRegistry 调用对应 Agent 处理任务
            const success = await this.registry.dispatchTask(taskId, agentId);
            
            if (success) {
                this.logger.info(`[MainController] Task ${taskId} assigned successfully`);
                return true;
            } else {
                this.logger.error(`[MainController] Failed to assign task ${taskId}`);
                return false;
            }
        } catch (error) {
            this.logger.error(`[MainController] Error assigning task ${taskId}:`, error.message);
            return false;
        }
    }

    /**
     * 处理任务队列
     */
    async processQueue() {
        while (this.running && this.taskQueue.length > 0) {
            // 获取最高优先级任务
            const queueItem = this.taskQueue[0];
            const task = queueItem.task;

            // 检查依赖
            const dependenciesMet = await this.checkTaskDependencies(task);
            
            if (!dependenciesMet) {
                // 依赖未满足，移到队列末尾并降级
                this.taskQueue.shift();
                task.priority = Math.min(task.priority || 10, this.config.priorityThreshold - 1);
                this.taskQueue.push(queueItem);
                this.taskQueue.sort((a, b) => b.task.priority - a.task.priority);
                await this.delay(500);
                continue;
            }

            // 查找可用 Agent
            const availableAgents = this.registry.getByType(queueItem.agentType);
            const agentId = availableAgents.find(id => {
                const agent = this.registry.get(id);
                return agent && !agent.currentTask;
            });

            if (agentId) {
                this.taskQueue.shift();
                await this.assignTask(task.id, agentId);
            } else {
                // 没有可用 Agent，等待
                await this.delay(1000);
            }
        }
    }

    /**
     * 处理任务失败
     */
    async handleTaskFailure(task, agentId, error) {
        const attempts = this.recoveryAttempts.get(task.id) || 0;
        
        if (attempts < 3) {
            this.recoveryAttempts.set(task.id, attempts + 1);
            this.logger.warn(`Task ${task.id} failed, retry ${attempts + 1}/3`);
            
            // 重新添加到队列
            await this.addTask(task, this.registry.getAgentType(agentId));
        } else {
            this.logger.error(`Task ${task.id} failed after 3 attempts`);
        }
    }

    /**
     * 设置崩溃恢复
     */
    setupCrashRecovery() {
        // 监听进程崩溃
        process.on('SIGTERM', async () => {
            this.logger.info('Received SIGTERM, saving state...');
            await this.saveState();
        });

        process.on('uncaughtException', async (error) => {
            this.logger.error('Uncaught exception:', error);
            await this.saveState();
        });
    }

    /**
     * 恢复任务
     */
    async recoverTasks() {
        const statePath = path.join(__dirname, 'controller-state.json');
        if (fs.existsSync(statePath)) {
            try {
                const state = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
                
                this.logger.info(`Recovering ${state.pendingTasks.length} pending tasks`);
                
                for (const task of state.pendingTasks) {
                    await this.addTask(task, task.agentType || 'dev');
                }
                
                this.logger.info('Task recovery complete');
            } catch (error) {
                this.logger.error('Failed to recover tasks:', error.message);
            }
        }
    }

    /**
     * 保存状态
     */
    async saveState() {
        const state = {
            timestamp: Date.now(),
            pendingTasks: this.taskQueue.map(item => ({
                task: item.task,
                agentType: item.agentType
            })),
            runningAgents: this.registry.getAll()
        };

        const statePath = path.join(__dirname, 'controller-state.json');
        fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
        
        this.logger.info('State saved');
    }

    /**
     * 启动控制器
     */
    async start() {
        this.running = true;
        this.logger.info('Main Controller started');
        
        // 设置崩溃恢复
        this.setupCrashRecovery();
        
        // 启动任务队列处理
        this.processQueue();
    }

    /**
     * 停止控制器
     */
    async stop() {
        this.running = false;
        
        // 停止所有 Agent
        for (const agentId of this.registry.getAll()) {
            await this.stopAgent(agentId);
        }
        
        // 保存状态
        await this.saveState();
        
        this.logger.info('Main Controller stopped');
    }

    /**
     * 延迟
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * 获取所有 Agent 状态
     */
    async getAgentStatus() {
        return await this.registry.getAllAgentStatus();
    }

    /**
     * 获取任务队列状态
     */
    getQueueStatus() {
        return {
            total: this.taskQueue.length,
            tasks: this.taskQueue.map(item => ({
                taskId: item.task.id,
                agentType: item.agentType,
                priority: item.task.priority
            }))
        };
    }
}

module.exports = { MainController };
