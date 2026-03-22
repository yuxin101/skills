---
name: article-images-gen
description: 文案插图专家，为文章生成手绘风格插图。风格：手绘、简约、整洁、留白、构图平衡、色调统一。Use when user asks to generate illustrations for articles, "为文章配图", "生成插图", or needs hand-drawn style images for content.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills
---

# Article Images Generator (文案插图专家)

专业的文章配图生成工具，专注于生成高质量的手绘风格插图。

## 核心特点

- **风格定位**: 手绘风格 (hand-drawn style)
- **视觉特点**: 简约、整洁、留白、构图平衡、色调统一
- **单一提供商**: 阿里百炼 DashScope Qwen-Image
- **智能分析**: 自动分析文案内容，生成适配的插图
- **API 重试机制**: 遇到速率限制自动重试，最多 3 次，指数退避
- **中文文件名支持**: 自动将中文标题转换为拼音 slug

## 快速开始

```bash
# 基础用法
/article-images-gen path/to/article.md

# 指定密度
/article-images-gen path/to/article.md --density balanced

# 直接内容输入
/article-images-gen
[粘贴内容]
```

## 工作流程

### Step 1: 分析文案

分析文案内容，识别：
- 核心论点和概念
- 适合插图的位置
- 推荐的插图密度

### Step 2: 确认设置

使用 AskUserQuestion 确认：
- **密度**: minimal (1-2 张), balanced (3-4 张), per-section (推荐), rich (5+ 张)

### Step 3: 生成大纲

保存 `outline.md`:

```yaml
---
style: hand-drawn
density: balanced
image_count: 4
---

## Illustration 1

**Position**: [章节/段落]
**Purpose**: [为什么需要插图]
**Visual Content**: [要展示的内容]
**Filename**: 01-hand-drawn-concept-name.png
```

### Step 4: 生成提示词

为每个插图创建提示词文件 `prompts/NN-hand-drawn-{slug}.md`:

```yaml
---
illustration_id: 01
style: hand-drawn
---

# 手绘风格插图

## 主题
[具体内容描述]

## 画面构成
- **前景**: [主要元素]
- **背景**: [背景元素]

## 风格要求
- 手绘风格
- 简约
- 整洁、留白
- 构图平衡
- 色调统一
- 不要文字

## 技术规格
- 比例：16:9
```

### Step 5: 生成图片

调用阿里百炼 API 生成图片，保存到指定目录。

### Step 6: 更新文章

在文章对应位置插入图片引用：

```markdown
![描述](imgs/01-hand-drawn-concept-name.png)
```

## 输出目录

| 配置 | 路径 |
|------|------|
| 默认 | `{article-dir}/imgs/` |
| 同目录 | `{article-dir}/` |
| illustrations 子目录 | `{article-dir}/illustrations/` |

## 配置 (EXTEND.md)

```yaml
---
version: 1
default_output_dir: imgs-subdir
language: zh
watermark:
  enabled: false
  content: ""
  position: bottom-right
---
```

## 使用场景

- 技术文章配图
- 教程步骤说明
- 知识卡片
- 信息图表
- 营销文案插图

## 限制

- 仅支持手绘风格
- 仅使用阿里百炼 Qwen-Image
- 不支持参考图片
