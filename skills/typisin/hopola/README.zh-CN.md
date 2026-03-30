# Hopola（ClawHub 发布版）

## 简介
Hopola 是一个从检索到多媒体生成再到交付的流水线技能，覆盖：
- 网页检索
- 图片生成
- 视频生成
- 3D 模型生成
- Logo 设计
- 商品图生成
- 结果上传
- Markdown 报告输出

## 能力架构
- 主技能：`SKILL.md`
- 版本文件：`VERSION.txt`
- 子技能：`subskills/` 下 8 个能力单元
- 问询模板：`playbooks/design-intake.md`
- 脚本：`scripts/` 下发布校验与打包工具
- 资产：`assets/` 下 logo、cover、flow

## 安全配置
- 必须由用户主动配置环境变量 `OPENCLOW_KEY`。
- `config.template.json` 仅保存 `key_env_name` 和空 `key_value` 占位。
- 发布前执行校验脚本阻断明文 key。

## 快速开始
```bash
cd .trae/skills/Hopola
python3 scripts/check_tools_mapping.py
python3 scripts/validate_release.py
python3 scripts/build_release_zip.py
```

## 调度策略
- 生成类任务采用“固定工具优先，自动发现回退”。
- 当固定工具不可用时，调用 `/api/gateway/mcp/tools` 选择匹配工具。

## 上架文件
- `Hopola-Skills/hopola-clawhub-v<version>-*.zip`
- `README.zh-CN.md`
- `README.en.md`
- `RELEASE.md`
