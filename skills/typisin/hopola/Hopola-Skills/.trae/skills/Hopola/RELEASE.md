# Hopola 发布清单

## 发布前检查
- 目录完整：主技能、6 个子技能、脚本、资产、双语文档。
- 安全通过：无明文 key，`gateway.key_value` 为空。
- 映射通过：图片/视频/3D 的固定工具与回退策略有效。
- 版本通过：`VERSION.txt` 为 `x.y.z` 语义化版本格式。

## 执行命令
```bash
cd .trae/skills/Hopola
python3 scripts/check_tools_mapping.py
python3 scripts/validate_release.py
python3 scripts/build_release_zip.py
```

## 产物
- `Hopola-Skills/hopola-clawhub-v<version>-<timestamp>.zip`

## 当前版本
- 版本号：`1.0.1`
- 变更摘要：补齐版本管理基线，新增统一版本文件与发布产物版本命名。
- 新增能力：发布校验新增语义化版本检查，打包产物名自动携带版本号。
- 兼容性说明：不改变技能执行逻辑，仅影响发布流程与打包文件输出位置和命名。
- 风险与回滚：如需回滚，恢复旧打包命名规则并调整 `VERSION.txt` 内容即可。

## 版本说明模板
- 版本号：`x.y.z`
- 变更摘要：
- 新增能力：
- 兼容性说明：
- 风险与回滚：
