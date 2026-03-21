/**
 * Complete Example - 完整示例
 * 展示 GitHub Collaboration 的完整功能
 */

const { 
    TaskManagerEnhanced, 
    DevAgent, 
    TestAgent,
    STPIntegratorEnhanced,
    sendProgressUpdate,
    sendTaskCompletion
} = require('../skills/github-collab');

async function runCompleteExample() {
    console.log('=== GitHub Collaboration Complete Example ===\n');
    
    // 1. 创建任务管理器
    const taskManager = new TaskManagerEnhanced();
    
    // 2. 创建项目
    const project = await taskManager.createProject({
        name: 'Complete Project',
        description: 'A complete example project with all features',
        github_url: 'https://github.com/example/complete-repo'
    });
    
    console.log('✅ Created project:', project.id);
    
    // 3. 使用 STP 拆分任务
    const stp = new STPIntegratorEnhanced();
    
    const stpResult = await stp.splitTask(
        'Build a REST API with user authentication',
        'Node.js, Express, MongoDB, JWT',
        { deadline: '2024-12-31' }
    );
    
    console.log('✅ STP split task into', stpResult.tasks.length, 'subtasks');
    
    // 4. 批量创建任务
    const tasks = [];
    for (const stpTask of stpResult.tasks) {
        const task = await taskManager.createTask({
            project_id: project.id,
            name: stpTask.name,
            description: stpTask.description,
            priority: stpTask.priority,
            type: stpTask.type
        });
        tasks.push(task);
        
        // 发送任务创建通知
        await sendProgressUpdate({
            channel: 'qqbot',
            target: 'qqbot:c2c:3512D704E5667F4DF660228B731965C2',
            taskId: task.id,
            progress: 0,
            status: 'pending',
            taskName: task.name
        });
    }
    
    console.log('✅ Created', tasks.length, 'tasks');
    
    // 5. 设置任务依赖
    for (let i = 1; i < tasks.length; i++) {
        taskManager.addTaskDependency(tasks[i].id, tasks[i - 1].id);
    }
    console.log('✅ Set up task dependencies');
    
    // 6. 创建多个 Dev Agent
    const devAgents = [];
    for (let i = 0; i < 2; i++) {
        const agent = new DevAgent(`dev-agent-${i}`);
        await agent.initialize();
        devAgents.push(agent);
    }
    console.log('✅ Created 2 Dev Agents');
    
    // 7. 创建 Test Agent
    const testAgent = new TestAgent('test-agent-1');
    await testAgent.initialize();
    console.log('✅ Created Test Agent');
    
    // 8. 分配任务（考虑依赖关系）
    for (const task of tasks) {
        const dependenciesMet = taskManager.checkTaskDependencies(task.id);
        if (dependenciesMet) {
            const agentId = `dev-agent-${tasks.indexOf(task) % 2}`;
            await taskManager.assignTask(task.id, agentId);
            console.log(`✅ Assigned task ${task.id} to ${agentId}`);
        }
    }
    
    // 9. 所有 Dev Agent 处理任务
    for (const agent of devAgents) {
        await agent.processQueue();
    }
    
    // 10. 创建测试任务
    const testTask = await taskManager.createTask({
        project_id: project.id,
        name: 'Integration Test',
        description: 'Test all features together',
        priority: 5,
        type: 'testing'
    });
    
    // 添加依赖：测试任务依赖所有开发任务
    for (const task of tasks) {
        taskManager.addTaskDependency(testTask.id, task.id);
    }
    
    // 11. 检查依赖并分配测试任务
    const testDependenciesMet = taskManager.checkTaskDependencies(testTask.id);
    if (testDependenciesMet) {
        await taskManager.assignTask(testTask.id, 'test-agent-1');
        console.log('✅ Assigned test task to test-agent-1');
        
        await testAgent.processQueue();
        
        // 发送任务完成通知
        await sendTaskCompletion({
            channel: 'qqbot',
            target: 'qqbot:c2c:3512D704E5667F4DF660228B731965C2',
            taskId: testTask.id,
            taskName: testTask.name,
            agentName: 'test-agent-1',
            result: 'success'
        });
    }
    
    // 12. 获取项目状态
    const projectStatus = await taskManager.getProjectStatus(project.id);
    console.log('\n=== Project Status ===');
    console.log('Project:', projectStatus.project.name);
    console.log('Total Tasks:', projectStatus.totalTasks);
    console.log('Completed Tasks:', projectStatus.completedTasks);
    console.log('Progress:', projectStatus.progress + '%');
    
    console.log('\n=== Complete Example Completed ===');
}

// 运行示例
runCompleteExample().catch(console.error);