---
name: mama-crawler
description: 妈妈网育儿知识爬虫。爬取妈妈网（m.mama.cn）育儿文章，输出 Markdown 格式并存入御知库（~/.yuzhi/crawls/mama_cn/）。帝说"爬取妈妈网"、"/爬虫"或需要采集育儿知识时触发。
---

# 妈妈网育儿知识爬虫

## 命令

### `python3 scripts/mama_crawler.py --category <分类> --max-pages <页数> --max-articles <数量>`
按分类爬取妈妈网文章。

分类选项：
- `baby` — 亲子
- `yingyang` — 营养
- `disease` — 疾病
- `lady` — 女性
- `yongpin` — 用品
- `life` — 生活

### `python3 scripts/mama_crawler.py --search <关键词> --max-articles <数量>`
通过搜索爬取相关文章。

### `python3 scripts/mama_crawler.py --all --max-pages 3 --max-articles 30`
爬取所有分类（慎用，会花较长时间）。

## 输出

文章保存到 `~/.yuzhi/crawls/mama_cn/<分类名>/` 目录下，每个文章一个 `.md` 文件，包含标题、来源、日期和正文。

## 反爬机制

- 每次请求间隔 2-5 秒随机延迟
- 使用 iPhone User-Agent
- 不验证 SSL 证书（妈妈网证书问题）

## 使用场景

- 帝要求"爬取妈妈网育儿知识"
- 帝要求"把妈妈网 xxx 分类的文章存到知识库"
- 帝要求"采集育儿内容"

## 安全说明

本爬虫仅用于采集妈妈网公开内容，遵守 robots.txt，只小规模使用。
