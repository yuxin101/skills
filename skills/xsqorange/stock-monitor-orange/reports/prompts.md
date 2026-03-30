# Cron 任务 Prompt 模板

本文档包含定时任务使用的标准 Prompt 模板。

---

## A股早间综合报告

```markdown
A股早间综合报告任务：

1. 首先执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py index 获取大盘实时指数（数据来源：腾讯行情API）

2. 读取 C:\Users\Administrator\.openclaw\stock-pool.json 获取A股列表

3. 执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py monitor-a 获取A股技术面数据（数据来源：腾讯行情API）

4. 使用 web_fetch 工具抓取百度搜索获取股票资讯（替代tavily）：对每只重点股票执行 web_fetch(url="https://www.baidu.com/s?wd=股票名+股票代码+隔夜+最新消息+2026", extractMode="text", maxChars=8000)

5. 【重要】报告中所有"现价/涨跌幅/涨跌额"必须使用步骤3脚本返回的数据，禁止使用搜索结果中的价格

6. 结合新闻资讯和技术指标，生成早间综合分析报告

7. 将报告推送到群聊 
```

---

## A股午间综合报告

```markdown
A股午间综合报告任务：

1. 首先执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py index 获取大盘实时指数（数据来源：腾讯行情API）

2. 读取 C:\Users\Administrator\.openclaw\stock-pool.json 获取A股列表

3. 执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py monitor-a 获取A股技术面数据（数据来源：腾讯行情API）

4. 使用 web_fetch 工具抓取百度搜索获取股票资讯：对每只重点股票执行 web_fetch(url="https://www.baidu.com/s?wd=股票名+股票代码+最新消息+2026", extractMode="text", maxChars=8000)

5. 【重要】报告中所有"现价/涨跌幅/涨跌额"必须使用步骤3脚本返回的数据，禁止使用搜索结果中的价格

6. 结合新闻资讯和技术指标，生成午间综合分析报告

7. 将报告推送到群聊 
```

---

## A股晚间综合报告

```markdown
A股晚间综合报告任务：

1. 首先执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py index 获取大盘实时指数（数据来源：腾讯行情API）

2. 读取 C:\Users\Administrator\.openclaw\stock-pool.json 获取A股列表

3. 执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py monitor-a 获取A股技术面数据（数据来源：腾讯行情API）

4. 使用 web_fetch 工具抓取百度搜索获取股票资讯：对每只重点股票执行 web_fetch(url="https://www.baidu.com/s?wd=股票名+股票代码+最新公告+2026", extractMode="text", maxChars=8000)

5. 【重要】报告中所有"现价/涨跌幅/涨跌额"必须使用步骤3脚本返回的数据，禁止使用搜索结果中的价格

6. 结合新闻资讯和技术指标，生成晚间综合分析报告

7. 将报告推送到群聊 
```

---

## A股盘中监控

```markdown
A股监控任务：

1. 首先执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py index 获取大盘实时指数（数据来源：腾讯行情API）

2. 读取 C:\Users\Administrator\.openclaw\stock-pool.json 获取A股列表

3. 执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py monitor-a 获取A股技术面数据（数据来源：腾讯行情API）

4. 使用 web_fetch 工具抓取百度搜索获取股票资讯（替代tavily）：对每只重点股票执行 web_fetch(url="https://www.baidu.com/s?wd=股票名+股票代码+最新消息+2026", extractMode="text", maxChars=8000)

5. 【重要】报告中所有"现价/涨跌幅/涨跌额"必须使用步骤3脚本返回的数据，禁止使用搜索结果中的价格

6. 结合新闻资讯和技术指标，生成综合分析报告

7. 将报告推送到群聊 
```

---

## 港股早间综合报告

```markdown
港股早间综合报告任务：

1. 首先执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py index 获取大盘实时指数（数据来源：腾讯行情API）

2. 读取 C:\Users\Administrator\.openclaw\stock-pool.json 获取港股列表

3. 执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py monitor-hk 获取港股技术面数据（数据来源：腾讯行情API）

4. 使用 web_fetch 工具抓取百度/必应搜索获取股票资讯（替代tavily）：对每只重点股票执行 web_fetch(url="https://www.baidu.com/s?wd=股票名+股票代码+港股+隔夜+最新消息+2026", extractMode="text", maxChars=8000)

5. 【重要】报告中所有"现价/涨跌幅/涨跌额"必须使用步骤3脚本返回的数据，禁止使用搜索结果中的价格

6. 结合新闻资讯和技术指标，生成早间综合分析报告

7. 将报告推送到群聊 
```

---

## 港股午间综合报告

```markdown
港股午间综合报告任务：

1. 首先执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py index 获取大盘实时指数（数据来源：腾讯行情API）

2. 读取 C:\Users\Administrator\.openclaw\stock-pool.json 获取港股列表

3. 执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py monitor-hk 获取港股技术面数据（数据来源：腾讯行情API）

4. 使用 web_fetch 工具抓取百度/必应搜索获取股票资讯（替代tavily）：对每只重点股票执行 web_fetch(url="https://www.baidu.com/s?wd=股票名+股票代码+港股+最新消息+2026", extractMode="text", maxChars=8000)

5. 【重要】报告中所有"现价/涨跌幅/涨跌额"必须使用步骤3脚本返回的数据，禁止使用搜索结果中的价格

6. 结合新闻资讯和技术指标，生成午间综合分析报告

7. 将报告推送到群聊 
```

---

## 港股晚间综合报告

```markdown
港股晚间综合报告任务：

1. 首先执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py index 获取大盘实时指数（数据来源：腾讯行情API）

2. 读取 C:\Users\Administrator\.openclaw\stock-pool.json 获取港股列表

3. 执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py monitor-hk 获取港股技术面数据（数据来源：腾讯行情API）

4. 使用 web_fetch 工具抓取百度/必应搜索获取股票资讯（替代tavily）：对每只重点股票执行 web_fetch(url="https://www.baidu.com/s?wd=股票名+股票代码+港股+最新消息+2026", extractMode="text", maxChars=8000)

5. 【重要】报告中所有"现价/涨跌幅/涨跌额"必须使用步骤3脚本返回的数据，禁止使用搜索结果中的价格

6. 结合新闻资讯和技术指标，生成晚间综合分析报告

7. 将报告推送到群聊 
```

---

## 港股盘中监控

```markdown
港股监控任务：

1. 首先执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py index 获取大盘实时指数（数据来源：腾讯行情API）

2. 读取 C:\Users\Administrator\.openclaw\stock-pool.json 获取港股列表

3. 执行 python C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts\stock_monitor.py monitor-hk 获取港股技术面数据（数据来源：腾讯行情API）

4. 使用 web_fetch 工具抓取百度/必应搜索获取股票资讯（替代tavily）：对每只重点股票执行 web_fetch(url="https://www.baidu.com/s?wd=股票名+股票代码+港股+最新消息+2026", extractMode="text", maxChars=8000)

5. 【重要】报告中所有"现价/涨跌幅/涨跌额"必须使用步骤3脚本返回的数据，禁止使用搜索结果中的价格

6. 结合新闻资讯和技术指标，生成综合分析报告

7. 将报告推送到群聊 
```

---

## 执行要点

### 数据优先级（强制）

1. **脚本数据优先**：`monitor-a`/`monitor-hk` 返回的价格和涨跌幅是权威数据
2. **搜索数据辅助**：仅用于资讯分析，不得用于价格展示

### 报告格式要求

- 使用统一的表情符号（🔴🟢📊📈📉）
- 技术指标使用标准符号（✓✗✓✓等）
- 涨跌颜色符合中国习惯（红涨绿跌）
- 数值保留2位小数

### 推送目标

- 飞书群ID：``
- 使用 `message` 工具发送

### 错误处理

- 单只股票数据获取失败不影响其他股票
- 资讯获取失败时标注"暂无资讯"
- 脚本执行失败时记录错误并重试
