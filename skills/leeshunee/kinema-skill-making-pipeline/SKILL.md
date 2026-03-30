---
name: kinema-skill-making-pipeline
displayName: Kinema's Skill Making Pipeline
description: |
  KinemaClaw Skill development and publishing specification. Defines the standard process for skill development, version management, and publishing. All skills built in KinemaClaw must follow this specification.
  Trigger: Creating new skills, publishing skills, modifying existing skills.
---

# Kinema's Skill Making Pipeline | Kinema Skill 开发与发布规范

本规范定义了 KinemaClaw ecosystem 中 skill 的开发、版本管理、发布的标准化流程。 |

## Core Principles | 核心原则

1. **Git First** - All modifications must be managed in Git repository | 所有修改必须在 Git 仓库中管理
2. **Atomic Commits** - Each commit must be a meaningful independent change | 每次 commit 必须是有意义的独立变更
3. **Versioned Releases** - Must create Git tag before publishing | 发布前必须打 Git tag
4. **No In-Place Publishing** - Never publish raw skills from /app/skills/ | 禁止发布 /app/skills/ 中的原位 skill
5. **Onboarding Required** - Every skill must have installation/configuration guide | 每个 skill 必须有安装/配置引导

## Development Workflow | 开发流程

### 1. Create Skill Repository | 创建 Skill 仓库

```
projects/<skill-name>/
├── SKILL.md              # Required: skill definition
├── scripts/              # Optional: automation scripts
├── references/           # Optional: reference materials
└── other project files
```

### 2. Development Guidelines | 开发规范

- **Atomic commits**: One thing per commit | 每个 commit 只做一件事
- **Commit frequently**: Commit after completing each feature/fix | 完成一个功能/修复一个问题后立即 commit
- **Descriptive messages**: Use meaningful commit messages | 使用描述性的 commit message

```bash
# Good | 好
git commit -m "Add install command to searxng-search CLI"

# Bad | 不好
git commit -m "update" 
git commit -m "fix stuff"
```

### 3. Release Process | 发布流程

```bash
cd projects/<skill-name>

# 1. Ensure all changes are committed | 确保所有修改已 commit
git status

# 2. Create version tag (Semantic Versioning) | 打版本 tag (语义化版本)
git tag -a v1.2.0 -m "Release v1.2.0: Add onboarding"

# 3. Push tag to GitHub | 推送 tag 到 GitHub
git push origin v1.2.0

# 4. Create release on GitHub | 在 GitHub 仓库发布
# Settings → Releases → Create new release

# 5. Publish to ClawHub | 推送到 ClawHub
clawhub publish . --slug <skill-name> --version 1.2.0
```

### Version Numbering | 版本号规则

Follow Semantic Versioning: | 遵循语义化版本 (Semantic Versioning):
- **MAJOR**: Incompatible API changes | 不兼容的 API 变更
- **MINOR**: Backward-compatible new features | 向后兼容的新功能
- **PATCH**: Backward-compatible bug fixes | 向后兼容的 bug 修复

```
v1.0.0 → First release | 首次发布
v1.1.0 → New features | 新功能
v1.1.1 → Bug fixes | bug 修复
v2.0.0 → Breaking changes | 重大变更
```

## Required Elements | 必须要素

Each skill must include: | 每个 skill 必须包含：

### 1. SKILL.md

Must include: | 包含：
- name: skill name | skill 名称
- description: functionality description and trigger condition | 功能描述和触发条件
- Complete usage instructions | 完整使用说明

### 2. Onboarding | Onboarding

Must have at least one of: | 必须有以下之一：
- **Text onboarding**: Installation, configuration, startup instructions in SKILL.md | 文本 onboarding: 在 SKILL.md 中包含安装、配置、启动说明
- **Script onboarding**: Automated installation/configuration scripts | 脚本 onboarding: 提供自动化安装/配置脚本

Recommended: | 推荐包含：
- One-click install command | 一键安装命令
- Configuration instructions (environment variables, etc.) | 配置说明（环境变量等）
- Start/stop methods | 启动/停止方法
- Troubleshooting | 故障排除

### 3. Prohibited Content | 禁止内容

Skills must NOT contain: | skill 中**禁止**包含：
- Personal websites, domains | 个人网站、域名
- Passwords, accounts, tokens | 密码、账号、Token
- Personal email, phone | 个人邮箱、电话
- Real names, identity information | 真实姓名、身份信息

## GitHub Repository Guidelines | GitHub 仓库规范

- Default to **Private** repositories | 默认创建 **Private** 仓库
- Use meaningful repository names | 使用有意义的仓库名称
- Keep README.md in sync with SKILL.md | 保持 README.md 与 SKILL.md 一致

## Directory Structure | 目录结构

```
projects/
├── alist-cli/           # Git repository | Git 仓库
│   ├── SKILL.md
│   ├── scripts/
│   └── README.md
├── searxng-search/      # Git repository | Git 仓库
│   ├── SKILL.md
│   └── scripts/
└── concept-research/   # Git repository | Git 仓库
    └── SKILL.md
```

## Automation Script Example | 自动化脚本示例

```bash
#!/bin/bash
# skill-publish.sh - Publish skill to GitHub + ClawHub

SKILL_NAME=$1
VERSION=$2

if [ -z "$SKILL_NAME" ] || [ -z "$VERSION" ]; then
    echo "Usage: $0 <skill-name> <version>"
    exit 1
fi

cd projects/$SKILL_NAME

# Check for uncommitted changes | 检查是否有未提交的修改
if ! git diff --quiet; then
    echo "Error: Commit all changes first | 先提交所有修改"
    exit 1
fi

# Create tag | 打 tag
git tag -a v$VERSION -m "Release v$VERSION"

# Push | 推送
git push origin master
git push origin v$VERSION

# Publish to ClawHub | 发布到 ClawHub
clawhub publish . --slug $SKILL_NAME --version $VERSION
```

## Related Documentation | 相关文档

- [ClawHub Documentation](https://docs.openclaw.ai) | [ClawHub 文档](https://docs.openclaw.ai)
- [Skill Creator Specification](/app/skills/skill-creator/SKILL.md) | [Skill 创建规范](/app/skills/skill-creator/SKILL.md)
