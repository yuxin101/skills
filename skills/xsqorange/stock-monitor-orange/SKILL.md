---
name: stock-monitor
description: 股票监控分析技能。自定义股票池监控、实时行情获取、K线技术指标分析、涨跌趋势预测、信号提醒。用于：(1) 查询股票行情 (2) 分析技术指标 (3) 设置预警规则 (4) 获取买卖信号 (5) 持仓管理与分析 (6) 智能预警 (7) 综合报告生成
---

# Stock Monitor - 股票监控分析 (v1.7.0)

## 🎯 核心特色

### 1. 七大预警规则

| 规则 | 触发条件 | 权重 |
|------|----------|------|
| 成本百分比 | 盈利+15% / 亏损-12% | ⭐⭐⭐ |
| 日内涨跌幅 | 个股±4% / ETF±2% / 黄金±2.5% | ⭐⭐ |
| 成交量异动 | 放量>2倍均量 / 缩量<0.5倍 | ⭐⭐ |
| 均线金叉/死叉 | MA5上穿/下穿MA10 | ⭐⭐⭐ |
| RSI超买超卖 | RSI>70超买 / RSI<30超卖 | ⭐⭐ |
| 跳空缺口 | 向上/向下跳空>1% | ⭐⭐ |
| 动态止盈 | 盈利10%+后回撤5%/10% | ⭐⭐⭐ |

### 2. 分级预警系统

- 🚨 **紧急级**: 多条件共振 (如: 放量+均线金叉+突破成本)
- ⚠️ **警告级**: 2个条件触发 (如: RSI超卖+放量)
- 📢 **提醒级**: 单一条件触发

### 3. 多维度技术分析

- **趋势评估**: ADX趋势强度 + 多空力量对比
- **支撑阻力**: 近30日高低点 + BOLL轨道 + 枢轴点
- **三周期信号**: 短期(MA5/MA10) + 中期(MA20) + 长期(MA60)
- **能量指标**: OBV资金潮 + DMI动向 + WR威廉

### 4. 资讯情感分析

- 📰 东方财富公告+资讯（A股）
- 📰 东方财富+新浪财经（港股）
- 🧠 情感打分：积极/消极/中性，加权评分
- 🚨 高影响新闻标记（重组/业绩、减持等关键词分级）

### 5. 持仓智能管理

- 自动追踪成本、盈亏、市值
- 从交易记录自动同步（FIFO原则）
- 结合技术面给出操作建议

### 6. 中国股市习惯
- 🔴 红色 = 上涨 / 盈利
- 🟢 绿色 = 下跌 / 亏损

---

## 功能概述

- 📊 实时行情查询 (新浪+腾讯双源)
- 📈 技术指标分析 (MA/MACD/KDJ/RSI/BOLL/OBV/DMI/WR)
- 📍 支撑阻力计算
- 📈 趋势强度评估 (ADX)
- 🔔 信号提醒 (分级预警)
- ⏰ 定时监控 (智能频率)
- 💰 持仓管理
- 📝 交易记录
- 🛡️ 智能预警
- 📋 综合报告生成

---

## ⚠️ 重要规则

### 数据优先级规则

**【强制】报告中所有"现价/涨跌幅/涨跌额"必须使用脚本返回的数据，禁止使用搜索结果中的价格。**

执行顺序：
1. 脚本行情数据（`index`/`monitor-a`/`monitor-hk`）— 权威数据
2. 搜索资讯数据（`web_fetch`）— 仅用于资讯分析

---

## CLI 命令参考

工作目录：`.openclaw\skills\stock-monitor\scripts`

所有命令格式：`python stock_monitor.py <command> [args]`

### 行情与指数

| 命令 | 说明 | 示例 |
|------|------|------|
| `quote <code>` | 查询单只股票行情 | `python stock_monitor.py quote 600900` |
| `index` | 查询大盘指数 | `python stock_monitor.py index` |

### 技术分析

| 命令 | 说明 | 示例 |
|------|------|------|
| `analyze <code>` | 分析股票技术指标 | `python stock_monitor.py analyze 600900` |
| `monitor-a` | 监控所有A股（技术面） | `python stock_monitor.py monitor-a` |
| `monitor-hk` | 监控所有港股（技术面） | `python stock_monitor.py monitor-hk` |

### 综合报告

| 命令 | 说明 | 示例 |
|------|------|------|
| `report` | 生成完整综合报告 | `python stock_monitor.py report` |
| `report-a` | 生成A股综合报告 | `python stock_monitor.py report-a` |
| `report-hk` | 生成港股综合报告 | `python stock_monitor.py report-hk` |

### 持仓管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `position add <code> <qty> <cost>` | 添加/更新持仓 | `python stock_monitor.py position add 600900 6000 28.69` |
| `position remove <code>` | 清除持仓 | `python stock_monitor.py position remove 600900` |
| `position list` | 查看持仓 | `python stock_monitor.py position list` |
| `position <code>` | 分析单只持仓 | `python stock_monitor.py position 600900` |

### 交易记录

| 命令 | 说明 | 示例 |
|------|------|------|
| `trade buy <code> <qty> <price>` | 记录买入 | `python stock_monitor.py trade buy 600900 1000 28.50` |
| `trade sell <code> <qty> <price>` | 记录卖出 | `python stock_monitor.py trade sell 600900 500 30.00` |
| `trades [code]` | 查看交易记录 | `python stock_monitor.py trades` |

---

## 定时报告生成流程

### 标准流程（早报/午报/晚报）

当作为定时任务执行时，按照以下步骤生成报告：

### 第一步：获取大盘指数

```bash
python .openclaw\skills\stock-monitor\scripts\stock_monitor.py index
```

**返回数据：** 上证、深证、创业板、沪深300等指数实时行情

### 第二步：读取股票池

读取 `.openclaw\stock-pool.json` 获取股票列表

### 第三步：获取技术面数据

```bash
# A股
python .openclaw\skills\stock-monitor\scripts\stock_monitor.py monitor-a

# 港股
python .openclaw\skills\stock-monitor\scripts\stock_monitor.py monitor-hk
```

**返回数据：** 每只股票的现价、涨跌幅、成交量、MACD、KDJ、RSI、BOLL等技术指标

### 第四步：获取资讯（可选）

对重点股票使用 `web_fetch` 获取最新资讯：

**A股搜索词：**
```
https://www.baidu.com/s?wd=股票名+股票代码+最新消息+2026
```

**港股搜索词：**
```
https://www.baidu.com/s?wd=股票名+股票代码+港股+最新消息+2026
```

**早盘可加关键词：** `隔夜`、`美股`

### 第五步：生成报告

结合技术指标和资讯生成综合分析报告。

### 第六步：推送

发送到已配置社交账号

---

## 报告模板

### 早报模板

```
📈 【市场早报】{日期} {时段}

【大盘指数】
{指数表格}

【市场情绪】
{涨跌统计} | {资讯情感}

【持仓股动态】
{持仓股涨跌幅排行}

【重点资讯】
{关键新闻摘要}

【今日关注】
{值得关注的信号}
```

### 午报模板

```
☀️ 【市场午报】{日期}

【大盘指数】
{指数表格}

【上午市场回顾】
{涨跌幅统计}

【持仓股表现】
{持仓股详情}

【午后展望】
{技术面分析}
```

### 晚报模板

```
🌙 【市场晚报】{日期}

【大盘收盘】
{指数表格}

【今日涨跌统计】
{涨/跌/平数量}

【持仓股今日表现】
{持仓股涨跌幅} | {总盈亏}

【重点资讯回顾】
{关键新闻}

【明日展望】
{技术信号}
```

### 盘中监控模板

```
📊 【盘中监控】{日期} {时间}

【大盘动态】
{指数涨跌}

【持仓股异动】
{触发预警的股票}

【技术信号】
{金叉/死叉/超买/超卖}

【建议】
{操作建议}
```

---

## 配置文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 股票池 | `~/.openclaw/stock-pool.json` | 监控的股票列表 |
| 持仓记录 | `~/.openclaw/stock-positions.json` | 当前持仓 |
| 交易记录 | `~/.openclaw/stock-trades.json` | 买卖交易历史 |
| 预警配置 | `~/.openclaw/stock-alerts.json` | 预警规则配置 |

---

## 智能频率 (北京时间)

| 时间段 | 频率 | 监控标的 |
|--------|------|----------|
| 交易时间 9:30-15:00 | 每5分钟 | 全部+技术指标 |
| 午休 11:30-13:00 | 每10分钟 | 全部 |
| 收盘后 15:00-24:00 | 每30分钟 | 全部(日线数据) |
| 凌晨 0:00-9:30 | 每1小时 | 仅伦敦金 |
| 周末 | 每1小时 | 仅伦敦金 |


---

## 技术指标说明

| 指标 | 说明 | 信号 |
|------|------|------|
| MA5/10/20 | 移动平均线 | 金叉/死叉 |
| MACD | 趋势指标 | DIF上穿DEA买入 |
| KDJ | 随机指标 | K>80超买 K<20超卖 |
| RSI | 相对强弱 | >70超买 <30超卖 |
| BOLL | 布林带 | 突破上/下轨 |
| OBV | 能量潮 | 背离信号 |
| DMI | 动向指标 | 多头/空头趋势 |
| WR | 威廉指标 | 超买超卖 |
| ADX | 趋势强度 | >25趋势确认 >40趋势强劲 |
| 支撑/阻力 | 近30日高低点+BOLL | 接近支撑/阻力位操作建议 |

---

## ⚠️ 使用提示

- 技术指标有滞后性: 均线、MACD等都是滞后指标，用于确认趋势而非预测
- 避免过度交易: 预警只是参考，不要每个信号都操作
- 多条件共振更可靠: 单一指标容易假信号，多条件共振更准确
- 动态止盈要灵活: 回撤5%减仓、10%清仓是建议，根据市场灵活调整
- **数据优先级**: 脚本行情数据 > 搜索结果数据

**核心原则**: 预警系统目标是"不错过大机会，不犯大错误"，不是"抓住每一个波动"。

---

## 目录结构

```
stock-monitor/
├── SKILL.md              # 本技能说明文件
├── fetch.js              # 行情获取脚本
├── fetchA.js             # A股行情获取
├── fetchAll.js           # 全部行情获取
├── references/           # 操作参考文档
│   ├── index.md          # 参考文档导航
│   ├── commands.md       # 命令速查表
│   ├── config.md         # 配置文件说明
│   └── troubleshooting.md # 故障排查
├── reports/              # 报告模板
│   ├── templates.md      # 各类报告模板
│   └── prompts.md        # Cron任务Prompt模板
└── scripts/
    ├── stock_monitor.py  # 主监控脚本
    └── stock_capital.py  # 资金流向脚本
```


