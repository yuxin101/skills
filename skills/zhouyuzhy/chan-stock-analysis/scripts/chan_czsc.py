#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chan_czsc.py - 基于czsc框架的缠论多级别分析
使用方法: D:\QClawData\workspace\czsc\.venv\Scripts\python.exe scripts/chan_czsc.py --code 399006
"""
import os
import sys
import json
import argparse
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

# 添加czsc路径
CZSC_PATH = r'D:\QClawData\workspace\czsc'
sys.path.insert(0, CZSC_PATH)

# 强制使用Python实现（避免rs_czsc依赖）
os.environ['CZSC_USE_PYTHON'] = '1'

# 清理缓存
for m in list(sys.modules.keys()):
    if 'czsc' in m or 'rs_czsc' in m:
        del sys.modules[m]

# 导入czsc
from czsc import CZSC, Freq, format_standard_kline, ZS
from czsc.py.enum import Direction, Mark
from czsc.signals.cxt import (
    cxt_first_buy_V221126, cxt_first_sell_V221126,
    cxt_third_buy_V230228, cxt_second_bs_V230320, cxt_third_bs_V230319
)
print("CZSC modules loaded successfully")

# ============ 配置 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'scripts', 'cache')

LEVELS = [
    ('daily', 'Daily', Freq.D),
    ('30',    '30min', Freq.F30),
    ('5',     '5min',  Freq.F5),
    ('1',     '1min',  Freq.F1),
]

# ============ 数据加载 ============
def load_cache_bars(code: str, period: str) -> Optional[List]:
    """从缓存加载K线并转换为RawBar"""
    cache_path = os.path.join(CACHE_DIR, f"{code}_{period}.json")
    if not os.path.exists(cache_path):
        return None
    
    with open(cache_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    klines = data.get('klines', [])
    if not klines:
        return None
    
    df = pd.DataFrame(klines)
    df['dt'] = pd.to_datetime(df['datetime'])
    df['symbol'] = code
    df['vol'] = df.get('volume', df.get('vol', 0))
    if 'amount' not in df.columns:
        df['amount'] = df['vol'] * df['close']
    
    freq_map = {'daily': Freq.D, '30': Freq.F30, '5': Freq.F5, '1': Freq.F1}
    freq = freq_map.get(period, Freq.D)
    
    bars = format_standard_kline(df[['symbol', 'dt', 'open', 'high', 'low', 'close', 'vol', 'amount']], freq=freq)
    return bars

# ============ 技术指标 ============
def calc_macd(closes: List[float]) -> Dict[str, float]:
    """计算MACD指标"""
    if len(closes) < 34:
        return {'dif': 0, 'dea': 0, 'hist': 0}
    
    # EMA
    ema_f = [sum(closes[:12]) / 12]
    for i in range(12, len(closes)):
        ema_f.append((closes[i] - ema_f[-1]) * 2 / 13 + ema_f[-1])
    
    ema_s = [sum(closes[:26]) / 26]
    for i in range(26, len(closes)):
        ema_s.append((closes[i] - ema_s[-1]) * 2 / 27 + ema_s[-1])
    
    ml = min(len(ema_f), len(ema_s))
    dif = [ema_f[i] - ema_s[i] for i in range(ml)]
    
    dea = [sum(dif[:9]) / 9]
    for i in range(9, len(dif)):
        dea.append((dif[i] - dea[-1]) * 2 / 10 + dea[-1])
    
    md = len(dea)
    hist = [(dif[i] - dea[i - md]) * 2 for i in range(md, len(dif))]
    
    return {'dif': dif[-1], 'dea': dea[-1], 'hist': hist[-1] if hist else 0}

def calc_ma(closes: List[float], period: int) -> Optional[float]:
    """计算均线"""
    if len(closes) < period:
        return None
    return sum(closes[-period:]) / period

def calc_fib(high: float, low: float) -> Dict[str, float]:
    """计算斐波那契回撤位"""
    diff = high - low
    return {
        '23.6': high - diff * 0.236,
        '38.2': high - diff * 0.382,
        '50.0': high - diff * 0.5,
        '61.8': high - diff * 0.618,
        '78.6': high - diff * 0.786,
    }

# ============ 缠论分析 ============
def detect_beichi(bi_list: List) -> Optional[Dict]:
    """检测背驰"""
    if len(bi_list) < 5:
        return None
    
    last_bi = bi_list[-1]
    direction = last_bi.direction
    
    # 找进入段
    enter_bi = None
    for i in range(len(bi_list) - 2, -1, -1):
        if bi_list[i].direction == direction:
            enter_bi = bi_list[i]
            break
    
    if enter_bi is None:
        return None
    
    # 比较力度
    ratio_price = last_bi.power_price / enter_bi.power_price if enter_bi.power_price > 0 else 1
    ratio_vol = last_bi.power_volume / enter_bi.power_volume if enter_bi.power_volume > 0 else 1
    
    # 背驰条件：离开段力度 < 进入段力度
    if ratio_price >= 1:
        return None
    
    beichi_type = 'top' if direction == Direction.Down else 'bottom'
    strength = 'strong' if ratio_price < 0.5 else 'weak'
    
    return {
        'type': beichi_type,
        'strength': strength,
        'ratio': round(ratio_price, 3),
        'enter_power': round(enter_bi.power_price, 2),
        'leave_power': round(last_bi.power_price, 2),
    }

def get_signals(czsc_obj) -> Dict[str, str]:
    """获取买卖点信号"""
    signals = {
        'buy1': 'N/A', 'sell1': 'N/A',
        'buy2': 'N/A', 'sell2': 'N/A',
        'buy3': 'N/A', 'sell3': 'N/A',
    }
    
    try:
        s = cxt_first_buy_V221126(czsc_obj, di=1)
        v = list(s.values())[0]
        if '一买' in str(v):
            signals['buy1'] = str(v)
    except:
        pass
    
    try:
        s = cxt_first_sell_V221126(czsc_obj, di=1)
        v = list(s.values())[0]
        if '一卖' in str(v):
            signals['sell1'] = str(v)
    except:
        pass
    
    try:
        s = cxt_second_bs_V230320(czsc_obj, di=1)
        v = list(s.values())[0]
        if '二买' in str(v):
            signals['buy2'] = str(v)
        elif '二卖' in str(v):
            signals['sell2'] = str(v)
    except:
        pass
    
    try:
        s = cxt_third_buy_V230228(czsc_obj, di=1)
        v = list(s.values())[0]
        if '三买' in str(v):
            signals['buy3'] = str(v)
    except:
        pass
    
    try:
        s = cxt_third_bs_V230319(czsc_obj, di=1)
        v = list(s.values())[0]
        if '三卖' in str(v):
            signals['sell3'] = str(v)
    except:
        pass
    
    return signals

def judge_trend(czsc_obj, bars: List) -> str:
    """判断趋势（修复版）"""
    if len(czsc_obj.bi_list) < 3:
        closes = [b.close for b in bars]
        return 'up' if closes[-1] > closes[0] else 'down'
    
    try:
        zs = ZS(bis=czsc_obj.bi_list[-3:])
        if not zs.is_valid:
            closes = [b.close for b in bars[-10:]]
            return 'up' if closes[-1] > closes[0] else 'down'
        
        cur = bars[-1].close
        if cur > zs.zg:
            return 'up'
        elif cur < zs.zd:
            return 'down'
        else:
            return 'consolidation'
    except:
        closes = [b.close for b in bars[-10:]]
        return 'up' if closes[-1] > closes[0] else 'down'

# ============ 级别分析 ============
def analyze_level(code: str, period: str, name: str, freq_obj) -> Optional[Dict]:
    """分析单个级别"""
    bars = load_cache_bars(code, period)
    if bars is None or len(bars) < 20:
        return None
    
    # CZSC分析
    czsc_obj = CZSC(bars)
    
    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    
    # 中枢
    zs_info = None
    if len(czsc_obj.bi_list) >= 3:
        try:
            zs = ZS(bis=czsc_obj.bi_list[-3:])
            if zs.is_valid:
                zs_info = {
                    'zd': round(zs.zd, 2),
                    'zg': round(zs.zg, 2),
                    'zz': round(zs.zz, 2),
                    'sdt': str(zs.sdt)[:16],
                    'edt': str(zs.edt)[:16],
                }
        except:
            pass
    
    # 趋势
    trend = judge_trend(czsc_obj, bars)
    
    # MACD
    macd = calc_macd(closes)
    
    # 均线
    ma = {
        5: calc_ma(closes, 5),
        13: calc_ma(closes, 13),
        34: calc_ma(closes, 34),
        89: calc_ma(closes, 89),
        144: calc_ma(closes, 144),
    }
    
    # 斐波那契
    recent_high = max(highs[-20:]) if len(highs) >= 20 else max(highs)
    recent_low = min(lows[-20:]) if len(lows) >= 20 else min(lows)
    fib = calc_fib(recent_high, recent_low)
    
    # 背驰
    beichi = detect_beichi(czsc_obj.bi_list)
    
    # 买卖点信号
    signals = get_signals(czsc_obj)
    
    # 最近笔
    last_bis = []
    for bi in czsc_obj.bi_list[-5:]:
        d = bi.direction
        last_bis.append({
            'direction': 'up' if d == Direction.Up else 'down',
            'power': round(bi.power_price, 2),
            'change': round(bi.change * 100, 2),
            'sdt': str(bi.sdt)[:16],
            'edt': str(bi.edt)[:16],
        })
    
    return {
        'name': name,
        'freq': str(freq_obj),
        'current': round(bars[-1].close, 2),
        'bar_count': len(bars),
        'bi_count': len(czsc_obj.bi_list),
        'fx_count': len(czsc_obj.fx_list),
        'zs': zs_info,
        'trend': trend,
        'macd': {k: round(v, 3) for k, v in macd.items()},
        'ma': {k: round(v, 3) if v else None for k, v in ma.items()},
        'fib': {k: round(v, 2) for k, v in fib.items()},
        'beichi': beichi,
        'signals': signals,
        'last_bis': last_bis,
    }

# ============ 格式化输出 ============
def format_level_report(level_data: Dict) -> str:
    """格式化级别报告"""
    if level_data is None:
        return "  [Data not available]\n"
    
    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"  {level_data['name']} ({level_data['freq']})")
    lines.append(f"{'='*80}")
    
    # 基本信息
    trend_icon = {'up': '>>>', 'down': '<<<', 'consolidation': '---'}[level_data['trend']]
    lines.append(f"\n  Current Price: {level_data['current']}  Trend: {trend_icon} {level_data['trend'].upper()}")
    lines.append(f"  Bars: {level_data['bar_count']}  Strokes: {level_data['bi_count']}  Fenxing: {level_data['fx_count']}")
    
    # 中枢
    zs = level_data['zs']
    if zs:
        lines.append(f"\n  Zhongshu (ZS):")
        lines.append(f"    zd={zs['zd']}  zg={zs['zg']}  zz={zs['zz']}")
        lines.append(f"    period: {zs['sdt']} -> {zs['edt']}")
    else:
        lines.append(f"\n  Zhongshu (ZS): None detected")
    
    # 趋势
    lines.append(f"\n  Trend: {level_data['trend'].upper()}")
    
    # MACD
    m = level_data['macd']
    hist_dir = 'RED (Bullish)' if m['hist'] > 0 else 'GREEN (Bearish)'
    lines.append(f"\n  MACD:")
    lines.append(f"    DIF={m['dif']:.3f}  DEA={m['dea']:.3f}  HIST={m['hist']:.3f} [{hist_dir}]")
    
    # 均线
    lines.append(f"\n  Moving Averages:")
    ma = level_data['ma']
    for period, value in ma.items():
        if value:
            pos = 'above' if level_data['current'] > value else 'below'
            lines.append(f"    MA{period}={value:.3f} ({pos} current)")
    
    # 斐波那契
    lines.append(f"\n  Fibonacci Retracements (High->Low: {level_data['fib']['23.6']:.2f}->{list(level_data['fib'].values())[-1]:.2f}):")
    fib = level_data['fib']
    for pct, price in fib.items():
        pos = 'above' if level_data['current'] > price else 'below'
        lines.append(f"    {pct}%={price:.2f} ({pos} current)")
    
    # 背驰
    bc = level_data['beichi']
    if bc:
        lines.append(f"\n  Beichi (Divergence):")
        lines.append(f"    Type: {bc['type'].upper()}  Strength: {bc['strength'].upper()}")
        lines.append(f"    Ratio: {bc['ratio']:.1%} (enter={bc['enter_power']}, leave={bc['leave_power']})")
    else:
        lines.append(f"\n  Beichi (Divergence): None")
    
    # 买卖点
    lines.append(f"\n  Trading Signals:")
    sigs = level_data['signals']
    lines.append(f"    Buy1:  {sigs['buy1']}")
    lines.append(f"    Sell1: {sigs['sell1']}")
    lines.append(f"    Buy2:  {sigs['buy2']}")
    lines.append(f"    Sell2: {sigs['sell2']}")
    lines.append(f"    Buy3:  {sigs['buy3']}")
    lines.append(f"    Sell3: {sigs['sell3']}")
    
    # 最近笔
    lines.append(f"\n  Last 5 Strokes:")
    for bi in level_data['last_bis']:
        arrow = '>>>' if bi['direction'] == 'up' else '<<'
        lines.append(f"    {arrow} {bi['sdt']}->{bi['edt']}  power={bi['power']}  change={bi['change']:+.2f}%")
    
    return '\n'.join(lines)

# ============ 主函数 ============
def main(code: str):
    """主函数"""
    print(f"\n{'#'*80}")
    print(f"#  CZSC-Based Chan Theory Multi-Level Analysis")
    print(f"#  Symbol: {code}  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*80}")
    
    results = {}
    for period, name, freq_obj in LEVELS:
        print(f"\nLoading {name} data...", end=' ')
        bars = load_cache_bars(code, period)
        if bars:
            print(f"OK ({len(bars)} bars)")
            results[period] = analyze_level(code, period, name, freq_obj)
        else:
            print(f"FAILED")
            results[period] = None
    
    # 输出报告
    for period, name, freq_obj in LEVELS:
        level_data = results[period]
        if level_data:
            print(format_level_report(level_data))
    
    # 汇总
    print(f"\n{'#'*80}")
    print(f"#  SUMMARY")
    print(f"{'#'*80}")
    print(f"\n  Trend Summary:")
    for period, name, freq_obj in LEVELS:
        ld = results[period]
        if ld:
            print(f"    {name:>6}: {ld['trend'].upper():>15}  Price={ld['current']}  ZS={ld['zs']}")
    
    print(f"\n{'#'*80}\n")

# ============ 命令行入口 ============
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CZSC-based Chan Theory Analysis')
    parser.add_argument('--code', default='399006', help='Stock/Index code')
    parser.add_argument('--period', default='all', help='Period: daily, 30, 5, 1, or all')
    args = parser.parse_args()
    
    main(args.code)
