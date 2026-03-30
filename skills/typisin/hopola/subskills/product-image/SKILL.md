---
name: "hopola-product-image"
description: "封装商品图创意与场景化生成。Invoke when user needs e-commerce hero images, background replacement, or product visual optimization."
---

# Hopola Product Image

## 作用
负责电商商品图的行业问询、视觉方案构建与批量生成，输出可投放素材。

## 触发时机
- 用户要做商品主图、详情页图、场景图。
- 用户要替换背景、突出卖点、统一视觉风格。
- 主技能 `task_type=product-image` 或阶段 `generate-product-image`。

## 输入
- `product_name`
- `product_category`
- `product_selling_points`
- `product_image_url`
- `target_channel`
- `target_audience`
- `visual_style`
- `background_style`
- `product_ratio`

## 输出
- `product_image_urls`
- `visual_solution_summary`
- `tool_name_used`
- `fallback_used`

## 规则
- 默认优先 `api_product_background_replace`。
- 强制问询：渠道、受众、卖点、价格带、竞品对比、合规限制。
- 首轮至少输出 3 种场景：纯白主图、场景氛围图、卖点信息图。
- 固定工具不可用时回退 `image2image_edit_hydra_hoppa`。
