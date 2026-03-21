/**
 * TaskManagerEnhanced - 增强版任务管理器
 * 在原有 TaskManager 基础上增加更多功能
 */

const { TaskManager } = require('./task-manager');

class TaskManagerEnhanced extends TaskManager {
    constructor(dbPath = './github-collab.db') {
        super(dbPath);
    }

    /**
     * 创建任务（增强版）
     */
    async createTask(taskData) {
        const result = await super.createTask(taskData);
        
        // 额外处理：记录任务创建日志
        await this.logTaskEvent(result.id, 'created', 'Task created');
        
        return result;
    }

    /**
     * 分配任务给 Agent（增强版）
     */
    async assignTaskToAgent(taskId, agentId) {
        const result = await super.assignTaskToAgent(taskId, agentId);
        
        // 额外处理：记录任务分配日志
        await this.logTaskEvent(taskId, 'assigned', `Assigned to agent ${agentId}`);
        
        return result;
    }

    /**
     * 完成任务（增强版）
     */
    async completeTask(taskId, resultData = {}) {
        const result = await super.completeTask(taskId, resultData);
        
        // 额外处理：记录任务完成日志
        await this.logTaskEvent(taskId, 'completed', 'Task completed');
        
        return result;
    }

    /**
     * 记录任务事件日志
     */
    async logTaskEvent(taskId, eventType, message) {
        try {
            this.db.prepare(`
                INSERT INTO task_logs (task_id, event_type, message, created_at)
                VALUES (?, ?, ?, datetime('now'))
            `).run(taskId, eventType, message);
        } catch (error) {
            console.error(`[TaskManagerEnhanced] Failed to log event:`, error.message);
        }
    }
}

module.exports = { TaskManagerEnhanced };
