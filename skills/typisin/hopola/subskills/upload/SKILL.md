---
name: "hopola-upload"
description: "上传图片与结果资源到 Gateway。Invoke when generated assets need stable hosted URLs for delivery."
---

# Hopola Upload

## 作用
负责上传生成资源并返回稳定链接，供报告引用与分发。

## 触发时机
- `upload_enabled=true`
- 主技能阶段为 `upload`

## 输入
- `files`
- `metadata`

## 输出
- `uploaded_urls`
- `upload_status`
- `error_message`

## 规则
- 使用 `X-OpenClaw-Key` 头鉴权。
- 上传图片字段名固定 `image`。
- 单文件大小不得超过 20MB。
