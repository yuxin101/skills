---
name: "hopola-report"
description: "拼装统一 Markdown 结果报告。Invoke when pipeline or stage execution needs readable delivery output."
---

# Hopola Report

## 作用
将检索、生成、上传结果组装为标准 Markdown 报告。

## 触发时机
- 全流程完成后输出最终结果。
- 阶段模式下需要单独出报告。

## 输入
- `search_result`
- `generation_result`
- `upload_result`
- `errors`

## 输出
- `markdown_report`

## 规则
- 必含章节：检索摘要、生成结果、上传结果、安全告警、结论建议。
- 失败场景必须展示阶段、原因、重试结论与下一步建议。
- 若命中 403001，必须展示 `redirect_url`。
