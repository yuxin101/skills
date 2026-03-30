---
name: project-analyzer
version: 1.0.0
description: |
  项目文档生成器 - 自动分析项目并生成完整文档。
  使用场景：(1) 新项目接入时生成架构文档 (2) 生成开发规范 (3) 分析数据库结构 (4) 对接 Apifox 自动测试 (5) 生成快速启动文档。
  支持技术栈：Java/Spring Boot、Node.js、Python、Go、React/Vue 前端项目。
metadata:
  openclaw:
    emoji: "📊"
---

# Project Analyzer - 项目文档生成器

自动分析项目结构，生成完整的项目文档体系。

## 🎯 核心功能

### 1. 项目结构分析
- 自动识别技术栈
- 扫描目录结构
- 分析模块依赖
- 识别核心业务域

### 2. 架构文档生成
- 系统架构图
- 模块依赖关系
- 技术选型说明
- 部署架构

### 3. 配置项文档
- 配置文件分析
- 环境变量说明
- 配置项清单
- 敏感配置处理

### 4. 数据库文档
- 表结构分析
- ER 图生成
- 索引分析
- 数据库规范

### 5. 开发规范文档
- 代码规范
- 命名约定
- 目录结构规范
- Git 提交规范

### 6. 快速启动文档
- 环境要求
- 安装步骤
- 启动命令
- 常见问题

### 7. 测试规范文档
- 测试框架
- 测试覆盖率
- 测试用例规范
- Mock 规范

### 8. Apifox 自动对接
- API 文档同步
- 测试用例生成
- 接口自测执行
- 测试报告生成

---

## 📋 使用流程

### Phase 1: 项目扫描

```
1. 识别项目类型
   - 检查 package.json / pom.xml / build.gradle / go.mod / requirements.txt
   - 识别主要技术栈

2. 扫描目录结构
   - 列出所有目录
   - 识别核心模块
   - 标记配置目录

3. 分析代码结构
   - 扫描源码目录
   - 识别分层结构
   - 分析模块关系
```

### Phase 2: 深度分析

```
1. 数据库分析
   - 扫描 Entity/Model 类
   - 分析 SQL migration 文件
   - 提取表结构信息
   - 分析索引和约束

2. 配置分析
   - 读取配置文件
   - 提取配置项
   - 标记敏感配置

3. API 分析
   - 扫描 Controller/Router
   - 提取 API 端点
   - 分析请求/响应结构
```

### Phase 3: 文档生成

```
1. 生成架构文档
   - 系统架构图
   - 模块说明
   - 技术栈说明

2. 生成数据库文档
   - 表结构说明
   - ER 图
   - 索引说明

3. 生成开发规范
   - 代码规范
   - 命名约定
   - Git 规范

4. 生成快速启动文档
   - 环境要求
   - 安装步骤
   - 启动命令

5. 生成测试规范
   - 测试框架
   - 测试规范
   - 覆盖率要求
```

### Phase 4: Apifox 对接

```
1. 导出 OpenAPI 文档
2. 同步到 Apifox
3. 生成测试用例
4. 执行接口测试
5. 生成测试报告
```

---

## 🔧 技术栈支持

### Java / Spring Boot

```
识别文件：
- pom.xml / build.gradle
- application.yml / application.properties

分析内容：
- Maven/Gradle 依赖
- Spring Boot 配置
- JPA/MyBatis Entity
- Controller/Service/Repository
```

### Node.js

```
识别文件：
- package.json
- tsconfig.json

分析内容：
- npm/yarn/pnpm 依赖
- Express/Koa/NestJS 路由
- Sequelize/TypeORM/Prisma Model
```

### Python

```
识别文件：
- requirements.txt
- pyproject.toml
- setup.py

分析内容：
- Django/Flask/FastAPI
- SQLAlchemy Model
- API Router
```

### Go

```
识别文件：
- go.mod

分析内容：
- Go modules
- Gin/Echo 路由
- GORM Model
```

### 前端项目

```
识别文件：
- package.json
- vite.config / webpack.config

分析内容：
- React/Vue/Angular
- 组件结构
- API 调用
```

---

## 📂 输出目录结构

```
docs/
├── architecture/
│   ├── overview.md           # 架构总览
│   ├── modules.md            # 模块说明
│   └── diagrams/             # 架构图
│       ├── system.png
│       └── modules.png
├── database/
│   ├── schema.md             # 表结构文档
│   ├── er-diagram.png        # ER 图
│   └── migrations/           # 变更记录
├── development/
│   ├── coding-standards.md   # 代码规范
│   ├── naming-conventions.md # 命名约定
│   ├── git-workflow.md       # Git 规范
│   └── code-review.md        # 代码审查规范
├── quick-start/
│   ├── installation.md       # 安装指南
│   ├── configuration.md      # 配置说明
│   └── troubleshooting.md    # 常见问题
├── testing/
│   ├── test-standards.md     # 测试规范
│   ├── coverage.md           # 覆盖率要求
│   └── test-cases/           # 测试用例
└── api/
    ├── openapi.yaml          # OpenAPI 文档
    ├── apifox-sync.md        # Apifox 同步说明
    └── test-reports/         # 测试报告
```

---

## 🚀 使用方法

### 基本用法

```
分析项目并生成所有文档：
"分析项目 D:\my-project 并生成完整文档"

只生成特定文档：
"分析项目 D:\my-project 并生成架构文档"
"分析项目 D:\my-project 并生成数据库文档"
"分析项目 D:\my-project 并生成快速启动文档"
```

### Apifox 对接

```
"分析项目 D:\my-project 并对接到 Apifox 项目 ID: 12345"

步骤：
1. 生成 OpenAPI 文档
2. 使用 Apifox CLI 同步
3. 生成测试用例
4. 执行测试
```

### 自定义配置

```
创建配置文件：project-analyzer.yaml

# 项目分析器配置
project:
  name: my-project
  type: spring-boot  # 可选：auto-detect

output:
  base_dir: docs
  
database:
  analyze_entities: true
  analyze_migrations: true
  
apifox:
  project_id: 12345
  api_token: ${APIFOX_TOKEN}
```

---

## 📊 分析报告示例

### 架构分析报告

```markdown
# 系统架构

## 技术栈
- 语言: Java 17
- 框架: Spring Boot 3.2
- 数据库: MySQL 8.0
- 缓存: Redis 7.0

## 模块结构
- modo-core: 核心业务模块
- modo-boot: 启动模块
- modo-api: API 模块

## 依赖关系
[模块依赖图]
```

### 数据库分析报告

```markdown
# 数据库结构

## 表清单
- users (用户表)
- orders (订单表)
- products (产品表)

## ER 图
[ER 图]

## 索引分析
- users.idx_email: 唯一索引
- orders.idx_user_id: 普通索引
```

---

## 🔌 Apifox 集成

### 前置要求

```bash
# 安装 Apifox CLI
npm install -g apifox-cli

# 配置 API Token
export APIFOX_TOKEN=your_token_here
```

### 同步 OpenAPI 文档

```bash
# 导出 OpenAPI 文档
apifox sync --project-id 12345 --file docs/api/openapi.yaml

# 或使用在线同步
apifox sync --project-id 12345 --from-url http://localhost:8080/v3/api-docs
```

### 执行测试

```bash
# 运行所有测试用例
apifox run --project-id 12345 --all

# 运行特定测试套件
apifox run --project-id 12345 --suite smoke-test

# 生成测试报告
apifox report --project-id 12345 --output docs/api/test-reports/
```

---

## ⚙️ 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `project.type` | string | auto | 项目类型：spring-boot/node/python/go/react/vue |
| `output.base_dir` | string | docs | 文档输出目录 |
| `database.analyze_entities` | bool | true | 是否分析 Entity 类 |
| `database.analyze_migrations` | bool | true | 是否分析 migration 文件 |
| `apifox.project_id` | number | - | Apifox 项目 ID |
| `apifox.auto_sync` | bool | false | 是否自动同步到 Apifox |
| `apifox.auto_test` | bool | false | 是否自动执行测试 |

---

## 🎯 最佳实践

### 1. 新项目接入

```
1. 运行项目分析器
2. 生成完整文档
3. 人工审核并补充
4. 纳入版本控制
```

### 2. 定期更新

```
1. 代码变更后重新分析
2. 对比文档差异
3. 更新文档版本
```

### 3. CI/CD 集成

```yaml
# .github/workflows/docs.yml
name: Generate Docs
on: [push]
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Analyze Project
        run: |
          # 项目分析命令
      - name: Sync to Apifox
        run: apifox sync --project-id ${{ secrets.APIFOX_PROJECT_ID }}
```

---

## 📝 模板定制

可在 `references/templates/` 目录下自定义文档模板：

- `architecture.md.template`
- `database.md.template`
- `coding-standards.md.template`
- `quick-start.md.template`
- `test-standards.md.template`

---

*让项目文档自动化 📊✨*
