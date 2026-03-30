# Changelog

## 2026-03-26
- ✅ **模型自动判断逻辑**
  - CN 区：根据 prompt 关键词自动选择 `image-01`（写实）或 `image-01-live`（艺术风格）
  - Global 区：只用 `image-01`
  - 新增参数：`--model`、`--region`、`--api-key`、`--base-url`
  - 艺术风格关键词：手绘、卡通、漫画、动漫、油画、蜡笔、素描、水彩、国画、插画、原画 等
  - 写实关键词：写实、真实、逼真、照片、摄影、realistic、photorealistic 等

- ✅ **参考图 URL 处理优化**
  - `http://` 或 `https://` 开头 → 直接作为公网 URL 传给模型，无需下载转换
  - 本地路径 → 仍然转为 base64 Data URL

- ✅ **Prompt 长度校验**
  - 超过 1500 字符会报错退出，提醒用户缩短描述

- ✅ **prompt_optimizer 智能自动判断**
  - 短描述（< 80字符）→ 自动开启优化，丰富细节
  - 长描述（≥ 80字符）→ 自动关闭优化，保留原意
  - 用户可手动覆盖：`--prompt-optimizer` 或 `--no-prompt-optimizer`

- ✅ **aigc_watermark 水印自动开启**
  - 默认 `false`
  - 检测到「水印/版权/标识/logo/watermark/copyright」等关键词 → 自动开启

- ✅ **输出目录改为共享目录**
  - `~/.openclaw/media/minimax/`（多 Agent 共用，方便跨 Agent 共享图片）
