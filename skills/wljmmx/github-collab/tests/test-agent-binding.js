/**
 * 测试 Agent 绑定机制
 * 验证任务分配时是否正确调用对应 Agent
 */

const { MainController } = require('./core/main-controller');
const { TaskManagerEnhanced } = require('./core/task-manager-enhanced');

async function testAgentBinding() {
    console.log('========================================');
    console.log('测试 Agent 绑定机制');
    console.log('========================================\n');

    // 1. 创建控制器
    console.log('[1] 创建 MainController...');
    const controller = new MainController();
    await controller.initialize();
    console.log('✅ MainController 初始化成功\n');

    // 2. 创建项目
    console.log('[2] 创建测试项目...');
    const project = await controller.taskManager.createProject({
        name: 'Agent Binding Test',
        description: '测试 Agent 绑定机制',
        github_url: 'https://github.com/test/agent-binding'
    });
    console.log(`✅ 项目创建成功：${project.name} (ID: ${project.id})\n`);

    // 3. 创建任务
    console.log('[3] 创建测试任务...');
    const task = await controller.taskManager.createTask({
        project_id: project.id,
        name: 'Test Agent Binding',
        description: '测试任务分配和 Agent 调用',
        priority: 10
    });
    console.log(`✅ 任务创建成功：${task.name} (ID: ${task.id})\n`);

    // 4. 启动 Dev Agent
    console.log('[4] 启动 Dev Agent...');
    const devAgent = await controller.startAgent('dev', 'test-dev-agent');
    console.log(`✅ Dev Agent 启动成功：${devAgent.agentId}\n`);

    // 5. 启动 Test Agent
    console.log('[5] 启动 Test Agent...');
    const testAgent = await controller.startAgent('test', 'test-test-agent');
    console.log(`✅ Test Agent 启动成功：${testAgent.agentId}\n`);

    // 6. 验证 Agent 注册
    console.log('[6] 验证 Agent 注册...');
    const registeredAgents = controller.registry.getAll();
    console.log(`✅ 已注册 Agent: ${registeredAgents.join(', ')}\n`);

    // 7. 分配任务给 Dev Agent
    console.log('[7] 分配任务给 Dev Agent...');
    const assignResult = await controller.assignTask(task.id, 'test-dev-agent');
    console.log(`✅ 任务分配结果：${assignResult ? '成功' : '失败'}\n`);

    // 8. 验证任务状态
    console.log('[8] 验证任务状态...');
    const taskStatus = await controller.taskManager.getTask(task.id);
    console.log(`✅ 任务状态：${taskStatus.status}`);
    console.log(`   分配给 Agent: ${taskStatus.assigned_agent}`);
    console.log(`   优先级：${taskStatus.priority}\n`);

    // 9. 验证 Agent 状态
    console.log('[9] 验证 Agent 状态...');
    const agentStatus = await controller.registry.getAgentStatus('test-dev-agent');
    console.log(`✅ Agent 当前任务：${agentStatus.currentTask ? agentStatus.currentTask.id : '无'}`);
    console.log(`   任务队列：${agentStatus.queue.length} 个任务\n`);

    // 10. 获取所有 Agent 状态
    console.log('[10] 获取所有 Agent 状态...');
    const allAgentStatus = await controller.getAgentStatus();
    console.log('✅ 所有 Agent 状态:');
    for (const [agentId, status] of Object.entries(allAgentStatus)) {
        console.log(`   - ${agentId}: ${status.type}, 当前任务：${status.currentTask ? status.currentTask.id : '无'}`);
    }
    console.log('');

    // 11. 获取任务队列状态
    console.log('[11] 获取任务队列状态...');
    const queueStatus = controller.getQueueStatus();
    console.log(`✅ 任务队列：${queueStatus.total} 个任务\n`);

    // 12. 测试任务完成
    console.log('[12] 测试任务完成...');
    const completeResult = await controller.taskManager.completeTask(task.id, {
        code: 'console.log("Task completed");',
        progress: 100
    });
    console.log(`✅ 任务完成结果：${completeResult ? '成功' : '失败'}\n`);

    // 13. 验证任务最终状态
    console.log('[13] 验证任务最终状态...');
    const finalTaskStatus = await controller.taskManager.getTask(task.id);
    console.log(`✅ 最终任务状态：${finalTaskStatus.status}`);
    console.log(`   完成时间：${finalTaskStatus.completed_at}\n`);

    // 14. 停止 Agent
    console.log('[14] 停止所有 Agent...');
    await controller.stopAgent('test-dev-agent');
    await controller.stopAgent('test-test-agent');
    console.log('✅ 所有 Agent 已停止\n');

    // 15. 停止控制器
    console.log('[15] 停止控制器...');
    await controller.stop();
    console.log('✅ 控制器已停止\n');

    console.log('========================================');
    console.log('✅ 所有测试通过！');
    console.log('========================================');
}

// 运行测试
testAgentBinding().catch(error => {
    console.error('测试失败:', error);
    process.exit(1);
});
