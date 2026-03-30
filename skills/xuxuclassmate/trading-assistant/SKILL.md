---
name: trading-assistant
description: Advanced trading analysis system with technical indicators, trading signals, and position management
version: 1.5.0
author: OpenClaw Community
license: MIT
category: Finance
tags:
  - trading
  - finance
  - technical-analysis
  - stock-market
  - investment
  - openclaw
metadata:
  openclaw:
    requires:
      env:
        - TWELVE_DATA_API_KEY
        - ALPHA_VANTAGE_API_KEY
      bins:
        - python3
        - pip
    primaryEnv: TWELVE_DATA_API_KEY
    emoji: 📊
    homepage: https://github.com/XuXuClassMate/trading-assistant
---

# 📊 Trading Assistant

**Version**: v1.5.0 | **License**: MIT

Advanced trading analysis system providing technical indicators, trading signals, and position management for stock and crypto investors.

---

## ✨ Features

- **Technical Indicators**: RSI, MACD, Bollinger Bands, KDJ, CCI, ADX, ATR, OBV, VWAP
- **Trading Signals**: Auto-generated BUY/SELL/HOLD signals with confidence scores
- **Position Sizing**: Smart position calculator based on risk profile and stop-loss
- **Support/Resistance**: Automatic calculation of key price levels
- **Multi-Market**: Support for A-shares, US stocks, and cryptocurrencies

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
```

Edit `.env` with your API keys:
- `TWELVE_DATA_API_KEY` - Get free key at https://twelvedata.com (800 calls/day)
- `ALPHA_VANTAGE_API_KEY` - Get free key at https://www.alphavantage.co (25 calls/day)

### 3. Test Installation

```bash
python3 support_resistance.py
python3 trading_signals.py
python3 position_calculator.py
```

---

## 📖 Basic Usage

### Generate Trading Signal

```python
from trading_signals import generate_trading_signal
result = generate_trading_signal("AAPL")
print(result)
```

### Calculate Position Size

```python
from position_calculator import calculate_position_size
result = calculate_position_size(
    total_capital=100000,
    entry_price=175.64,
    stop_loss_price=165.00,
    risk_profile="moderate"
)
```

### Calculate Support/Resistance

```python
from support_resistance import calculate_support_resistance
result = calculate_support_resistance("NVDA")
```

---

## 📁 Directory Structure

```
trading-assistant/
├── SKILL.md                 # This file
├── README.md                # Full documentation (Chinese)
├── README_en.md             # Full documentation (English)
├── requirements.txt         # Dependencies
├── .env.example             # Config template
├── support_resistance.py    # Support/resistance module
├── trading_signals.py       # Signal generator
├── position_calculator.py   # Position sizing
└── daily_report.py          # Daily report generator
```

---

## 📚 Documentation

For detailed usage including daily reports, learning system, and automation setup, see:

- **Chinese**: `README.md`
- **English**: `README_en.md`
- **GitHub**: https://github.com/XuXuClassMate/trading-assistant

---

## ⚠️ Disclaimer

**For educational and research purposes only. Not financial advice.**

- Market investments carry risks
- Past performance does not guarantee future results
- Users are responsible for their own investment decisions

---

## 🔗 Links

- **GitHub**: https://github.com/XuXuClassMate/trading-assistant
- **Issues**: https://github.com/XuXuClassMate/trading-assistant/issues
- **OpenClaw**: https://openclaw.ai
- **ClawHub**: https://clawhub.com

---

**Last Updated**: 2026-03-26
