---
name: 上海落户公示查询
description: 查询上海落户公示信息，包括人才引进公示和居转户公示。触发词包括"上海落户公示"、"查询落户公示"、"人才引进公示"、"居转户公示"、"上海落户"、"户口公示"。
version: 1.0.0
---

# 上海落户公示查询 Skill

## 描述

查询上海落户公示信息，包括：
- 《上海市引进人才申办本市常住户口》公示名单（人才引进）
- 持有《上海市居住证》人员申办本市常住户口公示名单（居转户）

## 数据来源

- 官方网站：上海国际人才网 (https://www.sh-italent.com/)
- 公示列表页：https://www.sh-italent.com/News/NewsList.aspx?TagID=5696

## 功能

1. 自动打开浏览器访问上海国际人才网公示页面
2. 抓取最新的《上海市引进人才申办本市常住户口》公示名单
3. 抓取最新的《持有《上海市居住证》人员申办本市常住户口公示名单》
4. 整理公示信息并输出

## 触发关键词

当用户提到以下关键词时，应使用此 skill：
- "查询上海落户公示"
- "上海人才引进公示"
- "上海居转户公示"
- "最新落户公示名单"
- "上海落户"
- "户口公示"
- "落户公示查询"

## 执行指令

当触发此 skill 时，立即执行以下命令：

```bash
python3 /Users/sm0410/WorkBuddy/Claw/.workbuddy/skills/shanghai-luohu/query_luohu.py
```

### 命令行参数

```bash
# 使用默认浏览器（自动检测）
python3 query_luohu.py

# 指定浏览器
python3 query_luohu.py -b Chrome      # 使用 Chrome
python3 query_luohu.py -b Firefox     # 使用 Firefox
python3 query_luohu.py -b Edge        # 使用 Edge
python3 query_luohu.py -b Brave       # 使用 Brave
python3 query_luohu.py -b Safari      # 使用 Safari

# 不打开浏览器，仅输出查询结果
python3 query_luohu.py -n
python3 query_luohu.py --no-browser
```

### 支持的浏览器

| 浏览器 | 参数值 | 说明 |
|--------|--------|------|
| Safari | `-b Safari` | macOS 默认浏览器 |
| Chrome | `-b Chrome` | Google Chrome |
| Firefox | `-b Firefox` | Mozilla Firefox |
| Edge | `-b Edge` | Microsoft Edge |
| Brave | `-b Brave` | Brave 浏览器 |
| Opera | `-b Opera` | Opera 浏览器 |

**重要**：不要询问用户，直接执行脚本。如未指定浏览器，自动检测 macOS 默认浏览器。

## 使用方法

用户可以通过以下方式触发：
- "查询上海落户公示"
- "上海人才引进公示"
- "上海居转户公示"
- "最新落户公示名单"

## 执行方式

运行 Python 脚本：
```bash
python3 /Users/sm0410/WorkBuddy/Claw/.workbuddy/skills/shanghai-luohu/query_luohu.py
```

## 输出格式

```
==================================================
    上海落户公示信息查询
==================================================

【一】人才引进公示
  公示标题: 《上海市引进人才申办本市常住户口》公示名单
  公示日期: 2026-03-16
  公示链接: https://www.sh-italent.com/Article/xxx.shtml

【二】居转户公示
  公示标题: 持有《上海市居住证》人员申办本市常住户口公示名单
  公示日期: 2026-03-16
  公示链接: https://www.sh-italent.com/Article/xxx.shtml

==================================================
查询时间: 2026-03-16 11:06:59
==================================================

正在打开浏览器查看公示页面...
✓ 浏览器已打开

提示：公示期通常为 5 天，每月两次公示（月中和月底）
```

## 技术实现

使用 Python + AppleScript 方式：
1. 使用 urllib 抓取公示列表页面
2. 正则解析 HTML 获取最新公示链接
3. 抓取具体公示页面内容
4. 提取公示标题、日期等信息
5. 使用 AppleScript 打开 Safari 浏览器展示结果

## 文件结构

```
/Users/sm0410/WorkBuddy/Claw/.workbuddy/skills/shanghai-luohu/
├── skill.md           # Skill 说明文档
├── query_luohu.py     # 主查询脚本
└── query_luohu.sh     # Shell 版本（备用）
```

## 注意事项

- 公示期通常为 5 天
- 每月两次公示（月中和月底）
- 数据来源于官方网站，仅供参考
- 需要在 macOS 系统上运行
- 支持浏览器：Safari、Chrome、Firefox、Edge、Brave
- 默认自动检测 macOS 默认浏览器
