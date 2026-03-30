# 分析工作流程

## 完整分析流程

```
┌─────────────────────────────────────────────────────────┐
│                    项目分析流程                           │
└─────────────────────────────────────────────────────────┘

Phase 1: 项目扫描 (5分钟)
    │
    ├─ 1.1 识别项目类型
    │      • 检查 package.json / pom.xml / build.gradle / go.mod
    │      • 确定主要技术栈
    │
    ├─ 1.2 扫描目录结构
    │      • 列出所有目录
    │      • 识别核心模块
    │      • 标记配置目录
    │
    └─ 1.3 快速评估
           • 项目规模
           • 复杂度
           • 生成初步报告

Phase 2: 深度分析 (15-30分钟)
    │
    ├─ 2.1 代码结构分析
    │      • 扫描源码目录
    │      • 识别分层结构
    │      • 分析模块依赖
    │
    ├─ 2.2 数据库分析
    │      • 扫描 Entity/Model 类
    │      • 分析 SQL migration
    │      • 提取表结构信息
    │
    ├─ 2.3 配置分析
    │      • 读取配置文件
    │      • 提取配置项
    │      • 标记敏感配置
    │
    └─ 2.4 API 分析
           • 扫描 Controller/Router
           • 提取 API 端点
           • 分析请求/响应结构

Phase 3: 文档生成 (10分钟)
    │
    ├─ 3.1 架构文档
    │      • 系统架构图
    │      • 模块说明
    │      • 技术选型
    │
    ├─ 3.2 数据库文档
    │      • 表结构说明
    │      • ER 图
    │      • 索引说明
    │
    ├─ 3.3 开发规范
    │      • 代码规范
    │      • 命名约定
    │      • Git 规范
    │
    ├─ 3.4 快速启动
    │      • 环境要求
    │      • 安装步骤
    │      • 启动命令
    │
    └─ 3.5 测试规范
           • 测试框架
           • 测试规范
           • 覆盖率要求

Phase 4: Apifox 对接 (5分钟)
    │
    ├─ 4.1 OpenAPI 生成
    │      • 扫描 API 注解
    │      • 生成 OpenAPI 文档
    │
    ├─ 4.2 同步到 Apifox
    │      • 使用 Apifox CLI
    │      • 同步 API 文档
    │
    ├─ 4.3 测试用例生成
    │      • 自动生成测试用例
    │      • 配置测试环境
    │
    └─ 4.4 执行测试
           • 运行测试用例
           • 生成测试报告

Phase 5: 输出汇总
    │
    └─ 生成完整文档包
           docs/
           ├── architecture/
           ├── database/
           ├── development/
           ├── quick-start/
           ├── testing/
           └── api/
```

---

## 分阶段执行

### 只执行特定阶段

```bash
# 只扫描项目
"扫描项目 D:\my-project"

# 只分析数据库
"分析项目 D:\my-project 的数据库结构"

# 只生成架构文档
"生成项目 D:\my-project 的架构文档"

# 只对接 Apifox
"将项目 D:\my-project 的 API 对接到 Apifox 项目 12345"
```

---

## 分析脚本模板

### Python 分析脚本

```python
#!/usr/bin/env python3
"""
项目分析脚本
"""
import os
import json
from pathlib import Path

class ProjectAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.result = {
            "project_type": None,
            "tech_stack": [],
            "modules": [],
            "database": {},
            "api": []
        }
    
    def detect_project_type(self):
        """检测项目类型"""
        if (self.project_path / "pom.xml").exists():
            self.result["project_type"] = "maven"
            self.result["tech_stack"].append("java")
        elif (self.project_path / "package.json").exists():
            self.result["project_type"] = "nodejs"
            self.result["tech_stack"].append("nodejs")
        # ... 其他类型检测
    
    def scan_modules(self):
        """扫描模块"""
        # 实现模块扫描逻辑
        pass
    
    def analyze_database(self):
        """分析数据库"""
        # 实现数据库分析逻辑
        pass
    
    def analyze_api(self):
        """分析 API"""
        # 实现 API 分析逻辑
        pass
    
    def run(self):
        """运行完整分析"""
        self.detect_project_type()
        self.scan_modules()
        self.analyze_database()
        self.analyze_api()
        return self.result

if __name__ == "__main__":
    analyzer = ProjectAnalyzer("D:/my-project")
    result = analyzer.run()
    print(json.dumps(result, indent=2))
```

### Node.js 分析脚本

```javascript
#!/usr/bin/env node
/**
 * 项目分析脚本
 */
const fs = require('fs');
const path = require('path');

class ProjectAnalyzer {
    constructor(projectPath) {
        this.projectPath = projectPath;
        this.result = {
            projectType: null,
            techStack: [],
            modules: [],
            database: {},
            api: []
        };
    }
    
    detectProjectType() {
        if (fs.existsSync(path.join(this.projectPath, 'pom.xml'))) {
            this.result.projectType = 'maven';
            this.result.techStack.push('java');
        } else if (fs.existsSync(path.join(this.projectPath, 'package.json'))) {
            this.result.projectType = 'nodejs';
            this.result.techStack.push('nodejs');
        }
        // ... 其他类型检测
    }
    
    scanModules() {
        // 实现模块扫描逻辑
    }
    
    analyzeDatabase() {
        // 实现数据库分析逻辑
    }
    
    analyzeApi() {
        // 实现 API 分析逻辑
    }
    
    async run() {
        this.detectProjectType();
        this.scanModules();
        this.analyzeDatabase();
        this.analyzeApi();
        return this.result;
    }
}

// 使用示例
const analyzer = new ProjectAnalyzer('D:/my-project');
analyzer.run().then(result => console.log(JSON.stringify(result, null, 2)));
```

---

## 输出格式

### JSON 报告

```json
{
    "project": {
        "name": "my-project",
        "type": "spring-boot",
        "version": "1.0.0"
    },
    "tech_stack": [
        {"name": "java", "version": "17"},
        {"name": "spring-boot", "version": "3.2.0"},
        {"name": "mysql", "version": "8.0"}
    ],
    "modules": [
        {
            "name": "modo-core",
            "path": "src/main/java/com/example/core",
            "responsibility": "核心业务模块"
        }
    ],
    "database": {
        "tables": [
            {
                "name": "users",
                "columns": [
                    {"name": "id", "type": "BIGINT", "constraints": ["PK"]},
                    {"name": "email", "type": "VARCHAR(100)", "constraints": ["NOT NULL", "UNIQUE"]}
                ]
            }
        ]
    },
    "api": [
        {
            "method": "GET",
            "path": "/api/users",
            "controller": "UserController",
            "description": "获取用户列表"
        }
    ]
}
```

---

## 性能优化

### 大型项目分析

```python
# 并行分析
from concurrent.futures import ThreadPoolExecutor

def analyze_large_project(project_path):
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 并行执行分析任务
        future_modules = executor.submit(scan_modules, project_path)
        future_database = executor.submit(analyze_database, project_path)
        future_api = executor.submit(analyze_api, project_path)
        
        # 等待结果
        modules = future_modules.result()
        database = future_database.result()
        api = future_api.result()
    
    return {
        "modules": modules,
        "database": database,
        "api": api
    }
```

### 增量分析

```python
# 只分析变更部分
def incremental_analysis(project_path, git_diff):
    changed_files = parse_git_diff(git_diff)
    result = {}
    
    for file in changed_files:
        if is_entity_file(file):
            result["database"] = analyze_entity(file)
        elif is_controller_file(file):
            result["api"] = analyze_controller(file)
    
    return result
```
