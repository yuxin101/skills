#!/usr/bin/env python3
"""
Earnings Tracker - AI 驱动的财报追踪器

功能：
1. 扫描 A 股财报日历（AKShare）
2. 筛选关注的公司
3. 推送到 Discord/Telegram
"""

import json
import sys
from datetime import datetime, timedelta

try:
    import akshare as ak
except ImportError:
    print("❌ 请先安装 akshare: pip install akshare")
    sys.exit(1)

# 配置
CONFIG = {
    "watchlist": {
        "us": ["NVDA", "MSFT", "GOOGL", "META", "AMZN", "TSLA", "AMD"],
        "cn": ["600519", "000858", "601318", "000001"]
    },
    "notify": {
        "channel": "discord",
        "to": "channel:1478698808631361647"
    }
}

def get_cn_earnings_calendar():
    """获取 A 股财报预约披露时间表"""
    try:
        # 获取当前季度
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1
        date_str = f"{now.year}{quarter:02d}31"
        
        print(f"\n📊 获取 A 股财报预约披露时间表...")
        df = ak.stock_yysj_em(date=date_str)
        
        # 筛选关注的公司
        watchlist = CONFIG["watchlist"]["cn"]
        my_stocks = df[df["股票代码"].isin(watchlist)]
        
        if my_stocks.empty:
            print("  ℹ️  本季度暂无关注公司的财报预约")
            return []
        
        # 格式化结果
        results = []
        for _, row in my_stocks.iterrows():
            results.append({
                "code": row["股票代码"],
                "name": row["股票简称"],
                "date": row.get("首次预约时间", "待定"),
                "type": "cn"
            })
        
        print(f"  ✅ 找到 {len(results)} 个 A 股财报预约")
        return results
    
    except Exception as e:
        print(f"  ❌ 获取 A 股财报日历失败: {e}")
        return []

def format_earnings_report(cn_earnings):
    """格式化财报报告"""
    report = []
    report.append("📅 下周财报日历\n")
    report.append("=" * 50)
    
    if cn_earnings:
        report.append("\n🇨🇳 A股：\n")
        for e in cn_earnings:
            report.append(f"• {e['code']} {e['name']} - {e['date']}")
    
    if not cn_earnings:
        report.append("\nℹ️  本周暂无关注公司的财报\n")
    
    report.append("\n" + "=" * 50)
    report.append("\n请回复要跟踪的公司（例如：600519, NVDA）")
    
    return "\n".join(report)

def main():
    print("📊 Earnings Tracker 启动\n")
    print("=" * 50)
    
    # 获取 A 股财报日历
    cn_earnings = get_cn_earnings_calendar()
    
    # 格式化报告
    report = format_earnings_report(cn_earnings)
    print("\n" + report)
    
    # 保存结果
    result = {
        "timestamp": datetime.now().isoformat(),
        "cn_earnings": cn_earnings,
        "report": report
    }
    
    output_file = "/Users/xufan65/.openclaw/workspace/memory/earnings-calendar.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 结果已保存到: {output_file}")
    print("\n" + "=" * 50)
    print("✅ Earnings Tracker 完成\n")

if __name__ == "__main__":
    main()
