---
name: vip-search
description: 在唯品会(VIP.com)无感搜索商品，直接调用 Browser Subagent 进行网页内容提取。
---

# 唯品会商品搜索助手 (VIP Search)

本Skill用于在唯品会(VIP.com)网站上检索特定关键字的商品。通过大模型内置的 Browser Subagent 工具，可以在无用户 Cookie 和不用登录的情况下直接抓取搜索结果。

## Capabilities

1. **Browser 自动化抓取**: 利用内置的 Browser Subagent 工具模拟浏览器打开网页并解析 DOM 提取结果。
2. **数据处理并返回结果**: 将浏览后的商品结果总结为直观格式展现给用户。

## Usage / 工作流

当用户请求在唯品会搜索商品（例如：“帮我在唯品会搜索一下蓝牙耳机”）时，请严格按照以下步骤执行：

### 第一步：调用 Browser Subagent 执行搜索
直接调用你内置的 `browser_subagent` 工具即可，**不用要求用户提供任何 Cookie，也不要运行任何 Python 请求脚本**。

构建目标 URL（注意对 user 提供的 keyword 进行 URL 编码）：
`https://category.vip.com/suggest.php?keyword={url_encoded_keyword}`

**向 subagent 传递的 Task 描述应当类似于**：
`Navigate to https://category.vip.com/suggest.php?keyword={url_encoded_keyword}. Wait for the page to load, and extract the top product names and their prices from the search results.`

### 第二步：返回与展示
等待 Subagent 运行并完成任务后，解析它返回的观察结果与日志。
然后，将收集到的商品列表结果（包含产品名称、特卖价等）以 Markdown 列表或表格的形式友好地提取并呈现给用户即可。

## 注意事项
- 你必须直接且自主地操作 `browser_subagent` 工具；该工具擅长视觉及 DOM 数据提取。利用它你可以省去以往对抗反爬虫的心智成本。
