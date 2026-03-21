/**
 * 完整测试套件
 * 测试所有模块功能
 */

const assert = require('assert');
const path = require('path');

console.log('========================================');
console.log('GitHub Collab - 完整测试套件');
console.log('========================================\n');

let passed = 0;
let failed = 0;

async function runTest(name, testFn) {
    try {
        await testFn();
        console.log(`✅ ${name}`);
        passed++;
    } catch (error) {
        console.error(`❌ ${name}`);
        console.error(`   Error: ${error.message}`);
        failed++;
    }
}

async function main() {
    // 测试 1: TaskManager 基础功能
    console.log('\n📦 测试 TaskManager 基础功能');
    console.log('----------------------------------------');
    
    const { TaskManager } = require('../core/task-manager');
    const taskManager = new TaskManager(':memory:');
    
    await runTest('创建项目', async () => {
        const project = await taskManager.createProject({
            name: 'Test Project',
            description: 'Test Description',
            github_url: 'https://github.com/test/repo'
        });
        assert(project.id > 0, 'Project ID should be positive');
        assert(project.name === 'Test Project', 'Project name should match');
    });
    
    await runTest('创建任务', async () => {
        const project = await taskManager.createProject({
            name: 'Test Project 2',
            description: 'Test',
            github_url: 'https://github.com/test/repo2'
        });
        
        const task = await taskManager.createTask({
            project_id: project.id,
            name: 'Test Task',
            description: 'Test Description',
            priority: 10
        });
        
        assert(task.id > 0, 'Task ID should be positive');
        assert(task.name === 'Test Task', 'Task name should match');
    });
    
    await runTest('任务状态更新', async () => {
        const project = await taskManager.createProject({
            name: 'Test Project 3',
            description: 'Test',
            github_url: 'https://github.com/test/repo3'
        });
        
        const task = await taskManager.createTask({
            project_id: project.id,
            name: 'Test Task 2',
            description: 'Test',
            priority: 10
        });
        
        await taskManager.assignTaskToAgent(task.id, 'test-agent');
        const updatedTask = await taskManager.getTask(task.id);
        
        assert(updatedTask.status === 'assigned', 'Task status should be assigned');
        assert(updatedTask.assigned_agent === 'test-agent', 'Agent should be assigned');
    });
    
    await runTest('任务依赖管理', async () => {
        const project = await taskManager.createProject({
            name: 'Test Project 4',
            description: 'Test',
            github_url: 'https://github.com/test/repo4'
        });
        
        const task1 = await taskManager.createTask({
            project_id: project.id,
            name: 'Task 1',
            description: 'Test',
            priority: 10
        });
        
        const task2 = await taskManager.createTask({
            project_id: project.id,
            name: 'Task 2',
            description: 'Test',
            priority: 10
        });
        
        await taskManager.addTaskDependency(task2.id, task1.id);
        const deps = await taskManager.getTaskDependencies(task2.id);
        
        assert(deps.length === 1, 'Should have 1 dependency');
        assert(deps[0] === task1.id, 'Dependency should match');
    });
    
    // 测试 2: Agent 绑定机制
    console.log('\n🤖 测试 Agent 绑定机制');
    console.log('----------------------------------------');
    
    const { AgentRegistry } = require('../core/agent-registry');
    const registry = new AgentRegistry();
    
    await runTest('创建 Dev Agent', async () => {
        const agent = registry.createDevAgent('test-dev-agent');
        assert(agent !== null, 'Agent should be created');
        assert(agent.agentId === 'test-dev-agent', 'Agent ID should match');
    });
    
    await runTest('创建 Test Agent', async () => {
        const agent = registry.createTestAgent('test-test-agent');
        assert(agent !== null, 'Agent should be created');
        assert(agent.agentId === 'test-test-agent', 'Agent ID should match');
    });
    
    await runTest('Agent 注册', async () => {
        const agents = registry.getAll();
        assert(agents.length >= 2, 'Should have at least 2 agents');
    });
    
    await runTest('Agent 状态查询', async () => {
        const status = await registry.getAgentStatus('test-dev-agent');
        assert(status !== null, 'Status should exist');
        assert(status.type === 'dev', 'Agent type should be dev');
    });
    
    // 测试 3: MainController
    console.log('\n🎮 测试 MainController');
    console.log('----------------------------------------');
    
    const { MainController } = require('../core/main-controller');
    const controller = new MainController();
    
    await runTest('控制器初始化', async () => {
        await controller.initialize();
        assert(controller.registry !== null, 'Registry should exist');
        assert(controller.taskManager !== null, 'TaskManager should exist');
    });
    
    await runTest('启动 Agent', async () => {
        const agent = await controller.startAgent('dev', 'controller-test-agent');
        assert(agent !== null, 'Agent should be started');
        assert(agent.agentId === 'controller-test-agent', 'Agent ID should match');
    });
    
    await runTest('获取 Agent 状态', async () => {
        const status = await controller.getAgentStatus();
        assert(status !== null, 'Status should exist');
    });
    
    // 测试 4: STP 集成
    console.log('\n🧠 测试 STP 集成');
    console.log('----------------------------------------');
    
    const { STPIntegratorEnhanced } = require('../core/stp-integrator-enhanced');
    const stp = new STPIntegratorEnhanced();
    
    await runTest('任务拆分', async () => {
        const result = await stp.splitTask(
            'Build a simple web application',
            'Node.js, Express',
            { deadline: '2024-12-31' }
        );
        
        assert(result !== null, 'Result should exist');
        assert(result.tasks.length > 0, 'Should have tasks');
    });
    
    await runTest('依赖验证', async () => {
        const result = await stp.splitTask(
            'Create user authentication system',
            'Node.js, MongoDB',
            { deadline: '2024-12-31' }
        );
        
        assert(result !== null, 'Result should exist');
        assert(result.dependencies !== null, 'Dependencies should exist');
    });
    
    // 测试 5: 性能测试
    console.log('\n⚡ 测试性能');
    console.log('----------------------------------------');
    
    await runTest('批量创建任务', async () => {
        const project = await taskManager.createProject({
            name: 'Performance Test',
            description: 'Test',
            github_url: 'https://github.com/test/repo-perf'
        });
        
        const startTime = Date.now();
        for (let i = 0; i < 100; i++) {
            await taskManager.createTask({
                project_id: project.id,
                name: `Task ${i}`,
                description: 'Performance test',
                priority: 10
            });
        }
        const duration = Date.now() - startTime;
        
        assert(duration < 5000, `Should complete in < 5s, took ${duration}ms`);
        console.log(`   创建 100 个任务耗时：${duration}ms`);
    });
    
    // 总结
    console.log('\n========================================');
    console.log('测试完成');
    console.log(`✅ 通过：${passed}`);
    console.log(`❌ 失败：${failed}`);
    console.log('========================================\n');
    
    if (failed > 0) {
        process.exit(1);
    }
}

main().catch(error => {
    console.error('测试套件错误:', error);
    process.exit(1);
});
