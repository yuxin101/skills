"""
Wyckoff 2.0 诊股系统 v2
输入股票代码，输出完整分析报告
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from wyckoff_engine import calculate_vp, detect_phase, score_stock, detect_columns
import efinance as ef
import pandas as pd


def diagnose(code: str) -> str:
    df = ef.stock.get_quote_history(
        code, beg='20220101', end='20500101', klt=101, fqt=1
    )
    if df is None or len(df) < 60:
        return f'股票 {code} 数据不足，无法分析'

    cols = detect_columns(df)
    name = df[cols.get('name', 'name')].iloc[-1] if cols.get('name') else code

    prof = calculate_vp(df)
    ph = detect_phase(df)
    sc = score_stock(df)

    lines = []
    lines.append(f"{'='*55}")
    lines.append(f"  Wyckoff 诊股报告  |  {name} ({code})")
    lines.append(f"{'='*55}")

    # --- Phase 状态 ---
    phase_desc = {
        'A': '筑底/筑顶（趋势停止）',
        'B': '横盘（积累/派发区间）',
        'C': '测试（Spring/Upthrust）',
        'D': '突破（趋势启动）',
        'E': '趋势运行中',
        'unknown': '信号不足',
    }
    dir_desc = {
        'accumulation': '积累（看多✅）',
        'distribution': '派发（看空🔴）',
        'spring_test': 'Spring测试（待确认⚠️）',
        'upthrust_test': 'Upthrust测试（诱多🔴）',
        'uptrend': '上涨趋势✅',
        'downtrend': '下跌趋势🔴',
        'uptrend_pullback': '上涨趋势回踩（正常⚠️）',
        'downtrend_pullback': '下跌趋势反弹',
        'stopping': '趋势停止',
        'breakout_up': '向上突破✅',
        'breakout_down': '向下突破🔴',
    }
    rating_map = {
        'S': '🅢 强烈推荐',
        'A': '🄰 重点关注',
        'B': '🄱 观察',
        'C': '🄲 不建议',
        'D': '🄳 回避',
        'N': '未知',
    }

    lines.append(f"\n【评级】{rating_map.get(sc.get('rating','N'), sc.get('rating','N'))}  {sc.get('verdict','')}")

    lines.append(f"\n【当前状态】")
    lines.append(f"  Phase: {ph['phase']} - {phase_desc.get(ph['phase'], ph['phase'])}")
    lines.append(f"  方向: {ph['dir']} - {dir_desc.get(ph['dir'], ph['dir'])}")
    lines.append(f"  置信度: {ph['conf']}%")

    # --- Volume Profile ---
    if prof:
        lines.append(f"\n【关键价位】")
        lines.append(f"  VPOC: {prof['vpoc']}（控制点/重心）")
        lines.append(f"  VAH:  {prof['vah']}（价值区上沿）")
        lines.append(f"  VAL:  {prof['val']}（价值区下沿）")
        lines.append(f"  现价:  {prof['cur']}  位置: {prof['position']}")

        pos_emoji = '✅' if 'above' in prof['position'] else ('🔴' if 'below' in prof['position'] else '⚠️')
        lines.append(f"  {pos_emoji} 价格相对VPOC: {prof['position']}")

        if prof.get('lvn'):
            lvn_str = ', '.join([f"LVN@{l['price']}" for l in prof['lvn'][:3]])
            lines.append(f"  支撑（LVN）: {lvn_str}")
        if prof.get('hvn'):
            hvn_str = ', '.join([f"HVN@{h['price']}" for h in prof['hvn'][:3]])
            lines.append(f"  阻力（HVN）: {hvn_str}")

    # --- 综合评分 ---
    lines.append(f"\n【评分】{sc.get('score', 0)}/100")

    for g in sc.get('green_flags', []):
        lines.append(f"  {g}")
    for r in sc.get('red_flags', []):
        lines.append(f"  {r}")

    # --- 操作建议 ---
    rating = sc.get('rating', 'N')
    lines.append(f"\n【操作建议】")

    if rating == 'S':
        lines.append(f"  🅢 强烈推荐：积极关注，回调买入")
        lines.append(f"  止损：{prof['val'] if prof else 'N/A'}  目标：{prof['vah'] if prof else 'N/A'}")
    elif rating == 'A':
        lines.append(f"  🄰 重点关注：满足买入条件")
        lines.append(f"  止损：{prof['val'] if prof else 'N/A'}  目标：{prof['vah'] if prof else 'N/A'}")
    elif rating == 'B':
        lines.append(f"  🄱 观察：信号不明确，等待确认")
        if prof:
            lines.append(f"  参考区间：{prof['val']} ~ {prof['vah']}")
    elif rating == 'C':
        lines.append(f"  🄲 不建议：存在风险，不宜买入")
    elif rating == 'D':
        lines.append(f"  🄳 回避：风险过高")
    else:
        lines.append(f"  信号不足，继续观察")

    # --- Wyckoff 事件提示 ---
    lines.append(f"\n【关注事项】")
    if ph['phase'] in ['B'] and ph['dir'] == 'accumulation':
        lines.append(f"  - 等待 Spring 出现（价格跌破VAL后快速收回）")
        lines.append(f"  - 确认信号：放量阳线收复失地 + 站上VPOC")
    elif ph['phase'] == 'C' and ph['dir'] == 'spring_test':
        lines.append(f"  - 等待价格放量阳线收回VPOC确认 Spring")
        lines.append(f"  - 失败信号：缩量阴线继续下跌")
    elif ph['phase'] == 'D' and 'up' in ph['dir']:
        lines.append(f"  - 突破后等待回踩确认（Test to VPOC）")
        lines.append(f"  - 回踩获得支撑 = 二次入场点")
    elif ph['phase'] == 'E' and ph['dir'] == 'uptrend':
        lines.append(f"  - 趋势延续，耐心持有，不追高")
        lines.append(f"  - 止损上移：跌破VPOC离场")

    lines.append(f"\n{'='*55}")
    lines.append(f"  ⚠️ 本报告仅供参考，不构成投资建议")
    lines.append(f"{'='*55}")

    return '\n'.join(lines)


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1:
        code = _sys.argv[1]
    else:
        code = '000001'
    print(diagnose(code))
