/**
 * Basic Example - 基础示例
 * 展示 GitHub Collaboration 的基本用法
 */

const { TaskManagerEnhanced, DevAgent, TestAgent } = require('../skills/github-collab');

async function runBasicExample() {
    console.log('=== GitHub Collaboration Basic Example ===\n');
    
    // 1. 创建任务管理器
    const taskManager = new TaskManagerEnhanced();
    
    // 2. 创建项目
    const project = await taskManager.createProject({
        name: 'Example Project',
        description: 'A basic example project',
        github_url: 'https://github.com/example/repo'
    });
    
    console.log('✅ Created project:', project.id);
    
    // 3. 创建任务
    const task = await taskManager.createTask({
        project_id: project.id,
        name: 'Implement basic feature',
        description: 'Implement a basic feature for the project',
        priority: 10,
        type: 'development'
    });
    
    console.log('✅ Created task:', task.id);
    
    // 4. 创建 Dev Agent
    const devAgent = new DevAgent('dev-agent-1');
    await devAgent.initialize();
    
    // 5. 分配任务给 Dev Agent
    await taskManager.assignTask(task.id, 'dev-agent-1');
    console.log('✅ Assigned task to dev-agent-1');
    
    // 6. Dev Agent 处理任务
    await devAgent.processQueue();
    
    // 7. 创建测试任务
    const testTask = await taskManager.createTask({
        project_id: project.id,
        name: 'Test basic feature',
        description: 'Test the implemented feature',
        priority: 9,
        type: 'testing'
    });
    
    // 8. 添加依赖关系
    taskManager.addTaskDependency(testTask.id, task.id);
    console.log('✅ Added dependency: testTask depends on task');
    
    // 9. 创建 Test Agent
    const testAgent = new TestAgent('test-agent-1');
    await testAgent.initialize();
    
    // 10. 分配测试任务
    const dependenciesMet = taskManager.checkTaskDependencies(testTask.id);
    if (dependenciesMet) {
        await taskManager.assignTask(testTask.id, 'test-agent-1');
        console.log('✅ Assigned test task to test-agent-1');
        
        // 11. Test Agent 处理任务
        await testAgent.processQueue();
    }
    
    console.log('\n=== Basic Example Completed ===');
}

// 运行示例
runBasicExample().catch(console.error);