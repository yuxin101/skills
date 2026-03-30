---
name: novel-scraper
description: >-
  轻量级小说抓取工具，支持自动翻页、会话复用、内存监控。
  使用 curl+BeautifulSoup 抓取笔趣阁等小说网站，输出格式化 TXT 文件。
  Use when: 抓取网络小说章节、批量下载小说内容、保存小说为 TXT 格式。
---

# Novel Scraper - 小说抓取工具

轻量级小说抓取工具，针对低内存服务器优化，支持会话复用、自动翻页、内存监控。

## 快速开始

### 抓取单章

```bash
cd ~/.openclaw/workspace/skills/novel-scraper
python3 scripts/scraper.py --url "https://www.bqquge.com/4/1962"
```

### 批量抓取多章

```bash
python3 scripts/scraper.py --urls "https://www.bqquge.com/4/1963,https://www.bqquge.com/4/1964,https://www.bqquge.com/4/1965" --book "书名"
```

### 输出位置

抓取的小说保存在：`~/.openclaw/workspace/novels/`

文件名格式：`书名_第 X-Y 章.txt`

## 核心功能

| 功能 | 说明 |
|------|------|
| **自动翻页** | 检测并抓取分页章节，最多 5 页 |
| **会话复用** | 多章复用浏览器，每 3 章释放内存 |
| **内存监控** | 超 2.5GB 自动释放浏览器 |
| **智能过滤** | 自动过滤导航、广告等无关内容 |
| **缓存系统** | 避免重复抓取，支持断点续传 |

## 命令行参数

```bash
python3 scripts/scraper.py [选项]

# URL 选项
--url URL           单章 URL
--urls URLS         多章 URL（逗号分隔）

# 输出选项
--output, -o PATH   输出文件路径
--book, -b NAME     书名（可选，自动提取）
--no-auto-save      禁用自动保存

# 性能选项
--memory-limit MB   内存限制（默认 2500）
--auto-close N      每 N 章释放内存（默认 3）
--retry N           重试次数（默认 3）
--wait N            等待时间秒（默认 2）
```

## 支持网站

| 网站 | 状态 | URL 格式 | 说明 |
|------|------|----------|------|
| 笔趣阁 (bqquge.com) | ✅ 已测试 | `/4/2042` | 主要支持网站，使用 Biquge2026Adapter |
| 其他网站 | 🔄 需配置 | - | 在 `configs/sites.json` 添加选择器配置 |

### URL 格式说明

笔趣阁 URL 格式：`https://www.bqquge.com/{book_id}/{chapter_id}.html`

- `book_id`: 小说 ID（如 4 表示《没钱修什么仙》）
- `chapter_id`: 章节 ID（如 2042 表示第 81 章）

章节 ID 通常连续，可通过目录页获取完整列表。

## 配置新网站

编辑 `configs/sites.json`：

```json
{
  "www.example.com": {
    "title_selector": "h1",
    "content_selector": "#content p",
    "next_selector": ".next a",
    "wait_element": "#content",
    "memory_limit_mb": 500
  }
}
```

## 依赖

- Python 3.11+
- curl（系统命令）
- BeautifulSoup4 (bs4)
- psutil（内存监控）

```bash
cd ~/.openclaw/workspace/skills/novel-scraper
pip3 install -r requirements.txt --user
```

requirements.txt 包含：
```
beautifulsoup4>=4.12.0
bs4>=0.0.1
psutil>=5.9.0
```

## 故障排除

### 抓取内容为空

1. 检查 URL 格式是否为 `https://www.bqquge.com/4/xxx`
2. 清除缓存：`rm -rf /tmp/novel_scraper_cache/*`
3. 检查网站是否可访问：`curl -I https://www.bqquge.com/4/1962`

### 章节标题提取错误

1. 检查 HTML 结构是否变化
2. 查看 `scripts/scraper.py` 中 `Biquge2026Adapter` 的解析逻辑
3. 可能需要更新选择器配置

### 内存过高

1. 降低内存限制：`--memory-limit 1500`
2. 缩短释放间隔：`--auto-close 2`

### 文件名错误

- 确保 `--book` 参数正确
- 检查章节标题格式

## 相关脚本

| 脚本 | 用途 |
|------|------|
| `scripts/scraper.py` | 主程序（859 行） |
| `scripts/merge_cache.py` | 合并缓存文件（108 行） |
| `scripts/package_skill.py` | 打包工具（88 行） |

## 输出示例

```
============================================================
第 1 章 面试
============================================================

"到了吗？"

"不要紧张，你成绩这么好，一定能过的。"

看着屏幕上母亲发来的消息，张羽默默收起手机...
```
