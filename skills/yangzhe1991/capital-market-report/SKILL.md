---
name: capital-market-report
description: Generate comprehensive capital market briefings covering global indices (A-shares, Hong Kong stocks, US stocks), commodities (gold, oil, Bitcoin), and categorized news from Chinese and international financial media. Automatically detects trading hours to display real-time quotes for open markets and last close prices for closed markets. Use when user requests "capital market briefing", "market report", "资本市场简报", "资本市场报告", or any request for market summary with stock indices, commodity prices, and financial news classification into bullish/bearish/neutral categories.
---

# Capital Market Report Skill

Generate professional capital market briefings with real-time data and categorized news. Automatically detects market trading hours to show real-time quotes for open markets and last close prices for closed markets.

## Key Features

- **Trading Hour Detection**: Automatically identifies which markets are currently trading
- **Real-time vs Last Close**: Displays appropriate data based on market status
- **Comprehensive Coverage**: A-shares, HK stocks, US stocks, commodities, crypto
- **News Classification**: Bullish/Bearish/Neutral categorization with source attribution
- **Multi-language Support**: Chinese (default) and English

## Workflow

### Step 1: Check Market Status

Determine which markets are currently trading based on Beijing time:

| Market | Trading Hours (Beijing Time) | Status |
|--------|------------------------------|--------|
| A-shares | Mon-Fri 09:30-11:30, 13:00-15:00 | Real-time if open |
| Hong Kong | Mon-Fri 09:30-12:00, 13:00-16:00 | Real-time if open |
| US Stocks | Mon-Fri 21:30-04:00 (DST) / 22:30-05:00 (Standard) | Real-time if open |
| Commodities/Crypto | 24/7 | Always real-time |

### Step 2: Get Market Data

**A-shares, HK stocks, US stocks:**
```bash
uv run ~/.openclaw/skills/tencent-finance-stock-price/scripts/query_stock.py 上证指数 科创50 创业板指 恒生指数 恒生科技 标普500 纳指100
```

**Cryptocurrency (Bitcoin):**
```bash
uv run ~/.openclaw/workspace-group/skills/cryptoprice/scripts/cryptoprice.py BTC
```

**Gold & Oil:**
- Use web_search to get latest prices
- Search query: "gold price today", "crude oil price WTI"

### Step 3: Collect News (24-hour window)

**Chinese Media:**
- 36Kr: https://www.36kr.com/feed
- Sina Finance: https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&num=10
- Cailianshe (财联社)

**International Media:**
- BBC Business: https://feeds.bbci.co.uk/news/business/rss.xml
- Bloomberg Markets
- Yahoo Finance
- WSJ Markets

### Step 4: News Classification

**🟢 Bullish (利好):**
- Policy support / stimulus
- Strong earnings / guidance
- Market rallies / inflows
- M&A deals
- Positive economic data

**🔴 Bearish (利空):**
- Geopolitical conflicts
- Weak earnings / guidance cuts
- Market selloffs / outflows
- Regulatory tightening
- Economic slowdown signals

**⚪ Neutral (中性):**
- Executive changes
- Corporate restructuring
- Industry analysis
- Neutral policy announcements

### Step 5: Report Format

```
📊 Capital Market Briefing | YYYY-MM-DD HH:MM

---

### 🟢 Trading (Real-time Data)

**A-shares**
• Shanghai Composite: X,XXX.XX pts (+/-X / +/-X%)
• STAR 50: X,XXX.XX pts (+/-X / +/-X%)
• ChiNext: X,XXX.XX pts (+/-X / +/-X%)

**Commodities**
• Gold: $X,XXX/oz (+/-$X / +/-X%)
• Crude Oil (WTI): $XX.XX/barrel (+/-$X / +/-X%)
• Bitcoin: $XX,XXX

---

### 🔴 Market Closed (Last Close)

**Hong Kong**
• Hang Seng Index: XX,XXX.XX pts (+/-X / +/-X%)
• Hang Seng Tech: X,XXX.XX pts (+/-X / +/-X%)

**US Stocks**
• S&P 500: X,XXX.XX pts (+/-X / +/-X%)
• Nasdaq 100: XX,XXX.XX pts (+/-X / +/-X%)

---

### 📰 24-Hour News Briefing

#### 🟢 Bullish

1. **Headline**
   📰 Source | Time
   Summary

#### 🔴 Bearish

1. **Headline**
   📰 Source | Time
   Summary

#### ⚪ Neutral

1. **Headline**
   📰 Source | Time
   Summary

---

### 📡 News Sources
Chinese: 36Kr, Sina Finance, Cailianshe
International: BBC, Bloomberg, Yahoo Finance, WSJ

---

⏰ Trading Hours (Beijing Time):
• A-shares: 09:30-11:30, 13:00-15:00 (Mon-Fri)
• Hong Kong: 09:30-12:00, 13:00-16:00 (Mon-Fri)
• US Stocks: 21:30-04:00 DST / 22:30-05:00 Standard (Mon-Fri)
• Commodities/Crypto: 24/7
```

## Helper Script

Use the bundled script with trading hour detection:
```bash
uv run ~/.openclaw/workspace-group/skills/capital-market-report/scripts/generate-report.py
```

## Key Rules

1. **Trading Hour Detection**: Always check current time vs market hours before displaying data
2. **Label Data Type**: Clearly mark real-time vs last close prices
3. **Never fabricate data**: Always fetch real data before generating report
4. **24-hour news window**: Only include news from last 24 hours
5. **Source attribution**: Every news item must have source and timestamp
6. **Mobile-friendly**: Use list format, avoid tables for Telegram
7. **DST handling**: US market hours change with daylight saving time

## Market Trading Hours Reference

- **A-shares**: Mon-Fri 09:30-11:30, 13:00-15:00 (Beijing time)
- **Hong Kong**: Mon-Fri 09:30-12:00, 13:00-16:00 (Hong Kong time = Beijing time)
- **US Stocks**: 
  - Daylight Saving (Mar-Nov): Mon-Fri 21:30-04:00 next day (Beijing time)
  - Standard Time (Nov-Mar): Mon-Fri 22:30-05:00 next day (Beijing time)
- **Commodities/Crypto**: 24/7
