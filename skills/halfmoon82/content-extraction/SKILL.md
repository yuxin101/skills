---
name: content-extraction
description: |
  Extract clean Markdown from URLs and documents. Routes WeChat articles to browser-based extraction, Feishu/Lark docs to Feishu tools, YouTube to transcript tools, and generic URLs through a proxy cascade.
  Use when the user shares a URL and wants readable content, summaries, or Markdown output.
---

# Content Extraction

把任意 URL 或文档转成干净的 Markdown。

## 这套技能是怎么工作的

这个技能由两层组成：

1. **router**：先识别输入来源，生成执行计划
2. **extractor**：再用对应工具实际抓内容，转成 Markdown

router 的可执行入口在：
- `skills/content-extraction/scripts/extract_router.py`

## 核心路由

先判断输入类型，再选通道：

| 输入类型 | 识别规则 | 首选通道 | 失败后 |
|----------|----------|----------|--------|
| 公众号 | `mp.weixin.qq.com` | browser | 代理级联 / 本地回退 |
| 飞书文档 | `feishu.cn` / `larksuite.com` 且含 `doc` / `docx` | Feishu 工具 | 只在权限不足时说明失败 |
| 飞书知识库 | `feishu.cn` / `larksuite.com` 且含 `wiki` | Feishu 工具 | 先解节点，再读内容 |
| YouTube | `youtube.com` / `youtu.be` | transcript 链 | 明确返回无字幕 / 无法访问 |
| 其他 URL | 以上都不匹配 | `r.jina.ai` → `defuddle.md` → `web_fetch` → browser | 逐层降级 |

## 判定原则

- **先平台、后内容**：先识别站点类型，再决定抓取策略
- **先专用、后通用**：平台原生工具优先于代理抓取
- **先结构化、后文本化**：能读 blocks 就别直接 OCR/HTML 清洗
- **先稳定、后完整**：优先保证可读和可复用，而不是盲目全量
- **先净化、后转写**：通用网页优先用能去噪的抽取层（Jina / Defuddle），再做 Markdown 化

## 可执行入口

### 路由器

输入 URL 后，先生成执行计划：

```bash
python3 skills/content-extraction/scripts/extract_router.py 'https://mp.weixin.qq.com/s/xxx'
python3 skills/content-extraction/scripts/extract_router.py --format json 'https://www.feishu.cn/docx/xxx'
python3 skills/content-extraction/scripts/extract_router.py --title 'My Article' 'https://example.com'
```

### 执行规范生成器

把路由计划进一步固化成 extractor spec：

```bash
python3 skills/content-extraction/scripts/extract.py 'https://mp.weixin.qq.com/s/xxx'
python3 skills/content-extraction/scripts/extract.py --json 'https://www.feishu.cn/docx/xxx'
python3 skills/content-extraction/scripts/extract.py --title 'My Article' 'https://example.com'
```

### 实际抓取

执行时按路由计划使用对应工具：
- 公众号 → browser
- 飞书 → feishu
- YouTube → transcript
- 通用网页 → `r.jina.ai` / `defuddle.md` / `web_fetch` / browser

### 固化后模块

- `notes/executor-spec.md`
- `notes/solidification.md`

## 抽取规则

- 优先保留正文、标题、图片说明、引用、代码块和列表结构
- 去掉导航、推荐、页脚、重复链接和明显广告噪音
- 如果抽取层返回的是杂乱 HTML，继续降级，不把噪音结果当成功
- 如果页面是 JS 重度渲染，优先 browser / 可见文本，再考虑通用抽取

## 输出约束

抓取成功后，默认输出：

```md
**标题**: ...
**作者**: ...
**来源**: 公众号 / 飞书文档 / 飞书知识库 / 网页 / YouTube
**URL**: ...

### 内容摘要
...

### 正文
...
```

- 字段拿不到就省略，不要写 `Unknown`
- 长内容优先保存本地文件，正文只返回摘要 + 路径
- 保存名优先用 `title`，没有标题就用 `source_type`
- 图片、表格、引用、代码块要尽量保结构
- 失败时必须说明：失败层、失败原因、下一层是否尝试

## 设计原则

- **先路由，再抓取**：不同平台用不同通道，不要一把梭
- **先专用，再通用**：平台原生 API 优先于代理
- **先高质量，再降级**：可读性优先于盲目抓全
- **默认保存**：长内容建议保存到本地文件，再返回摘要和路径

## 典型场景

- 读公众号文章并总结
- 把飞书文档导出为 Markdown
- 将社交平台内容整理成研究材料
- 给 LLM 提供干净上下文，而不是 HTML 噪音

## 备注

如果输入链接属于受限页面，优先选择最稳的专用通道；如果专用通道失败，再进入降级链。
