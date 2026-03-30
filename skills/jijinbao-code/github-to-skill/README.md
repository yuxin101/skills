# GitHub to Skill - 开源项目转换器

**自动将 GitHub 下载的.zip 源代码转换成 OpenClaw 技能**

---

## 🎯 用途

看到好的开源软件 → 下载.zip → 一键转换成 OpenClaw 技能 → 立即使用

---

## 🚀 快速开始

### 方式 1: 直接对 SuperMike 说

```
把这个.zip 转成技能：Y:\Downloads\youtube-dl-master.zip
```

### 方式 2: 命令行

```bash
cd D:\Personal\OpenClaw\skills\github-to-skill

# 仅分析
python analyzer.py Y:\Downloads\project.zip

# 完整转换
python analyzer.py Y:\Downloads\project.zip -o D:\Personal\OpenClaw\skills
```

---

## 📋 使用流程

```
1. 从 GitHub 下载项目.zip
   ↓
2. 调用 github-to-skill 技能
   ↓
3. 自动分析（语言、结构、功能）
   ↓
4. 生成技能文件（SKILL.md, index.js 等）
   ↓
5. 安装依赖
   ↓
6. 完成！可以使用了
```

---

## 🎯 适用项目

### ✅ 适合转换
- CLI 工具（youtube-dl, httpie 等）
- Python 库（数据处理、工具库）
- JavaScript 库
- API 客户端
- 自动化脚本

### ❌ 不适合
- 大型框架（Django, React 等）
- GUI 应用（依赖图形界面）
- 数据库系统
- 操作系统级工具

---

## 📁 生成的文件

```
skills/[project-name]/
├── SKILL.md          # OpenClaw 技能说明
├── index.js          # 技能入口
├── package.json      # 包配置
├── config.json       # 配置
├── README.md         # 使用指南
└── src/              # 原始项目代码
```

---

## 💡 使用示例

### 示例 1: 转换 YouTube 下载工具
```
输入：Y:\Downloads\youtube-dl-master.zip

输出：skills/youtube-dl/

使用：
"使用 youtube-dl: 下载这个视频 https://youtube.com/watch?v=xxx"
```

### 示例 2: 转换数据处理库
```
输入：Y:\Downloads\pandas-extension.zip

输出：skills/pandas-extension/

使用：
"使用 pandas-extension: 处理这个 Excel 文件"
```

### 示例 3: 转换 API 客户端
```
输入：Y:\Downloads\github-api-client.zip

输出：skills/github-api-client/

使用：
"使用 github-api-client: 获取我的 issues"
```

---

## 🔧 高级用法

### 自定义输出目录
```
python analyzer.py project.zip -o D:\MySkills
```

### 仅分析不生成
```
python analyzer.py project.zip --analyze-only
```

### 批量转换
```
扫描 Y:\github-downloads\ 目录下所有.zip
逐个转换
生成批量报告
```

---

## 📊 分析内容

| 分析项 | 说明 |
|--------|------|
| **项目名称** | 从 package.json/setup.py 提取 |
| **编程语言** | Python/JavaScript/TypeScript等 |
| **项目类型** | CLI/库/Web/API |
| **入口文件** | main.py, index.js 等 |
| **依赖列表** | requirements.txt, package.json |
| **功能函数** | 公共函数和类 |
| **文档说明** | README 描述 |

---

## ⚠️ 注意事项

### 转换前
- ✅ 确认.zip 文件完整
- ✅ 检查项目许可证（是否允许复用）
- ✅ 查看原始文档

### 转换后
- ✅ 安装依赖
- ✅ 测试基本功能
- ✅ 检查与 OpenClaw 兼容性
- ✅ 阅读生成的 SKILL.md

### 法律合规
- ✅ 遵守原项目许可证
- ✅ 保留原作者版权信息
- ✅ 不用于商业用途（除非许可证允许）

---

## 🐛 故障排除

### 问题：分析失败
```
解决：
1. 检查.zip 是否完整
2. 确认是标准 GitHub 导出格式
3. 查看错误日志
```

### 问题：依赖冲突
```
解决：
1. 使用虚拟环境
2. 检查 requirements.txt
3. 解决版本冲突
```

### 问题：功能缺失
```
解决：
1. 手动调整 index.js
2. 补充配置参数
3. 添加必要的包装代码
```

---

## 🎯 实际案例

### 案例 1: youtube-dl 转换
```
时间：2 分钟
难度：⭐
结果：完美运行
使用："下载这个 YouTube 视频"
```

### 案例 2: 数据清洗工具
```
时间：5 分钟
难度：⭐⭐
结果：需要手动调整配置
使用："清洗这个 Excel 文件"
```

### 案例 3: GitHub API 客户端
```
时间：3 分钟
难度：⭐⭐
结果：需要配置 API Key
使用："获取我的 GitHub repos"
```

---

## 📈 转换质量评估

| 等级 | 分数 | 说明 |
|------|------|------|
| **A** | 90-100 | 完美转换，直接使用 |
| **B** | 75-89 | 良好，少量优化 |
| **C** | 60-74 | 可用，需要改进 |
| **D** | <60 | 需要大量修改 |

---

## 🚀 未来改进

- [ ] 自动测试生成
- [ ] 智能依赖解决
- [ ] GUI 项目适配
- [ ] 批量转换优化
- [ ] 技能质量评分
- [ ] 自动发布到 ClawHub

---

## 📚 参考

- **OpenClaw 文档:** https://docs.openclaw.ai
- **ClawHub:** https://clawhub.com
- **GitHub API:** https://docs.github.com/en/rest

---

**创建时间:** 2026-03-27  
**维护者:** SuperMike  
**理念:** 让开源软件复用变得简单！
