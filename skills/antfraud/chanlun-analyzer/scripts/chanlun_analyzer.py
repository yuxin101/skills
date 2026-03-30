#!/usr/bin/env python3
"""
Copaw 缠论分析引擎 v3.0
严格对齐 czsc (waditu/czsc) 算法

6层处理架构：
L0 数据获取 → L1 包含处理(remove_include) → L2 分型识别(check_fx/check_fxs) → L3 笔生成(check_bi) → L4 中枢构建 → L5 动力学信号

v3.0 核心改进（对齐 czsc）：
- L1 包含处理：严格对齐 czsc remove_include（k1.high < k2.high 判断方向，严格包含关系）
- L2 分型识别：严格 >/<（非 >=/<=），强制顶底交替
- L3 笔生成：czsc check_bi 算法（首分型→找最极端突破分型→包含检查→min_bi_len）
- 中枢：基于3笔重叠区 ZG=min(hi) ZD=max(lo)，支持扩展
- 买卖点：背驰面积法（MACD柱面积）
"""

import argparse
import json
import sys
import urllib.request
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple
from datetime import datetime, date


# ============================================================
# Data Structures
# ============================================================

class FenxingType(Enum):
    TOP = "top"
    BOTTOM = "bottom"


class BiDirection(Enum):
    UP = "up"
    DOWN = "down"


@dataclass
class KLine:
    """原始K线或包含处理后的K线"""
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0
    elements: list = field(default_factory=list)  # 包含合并的原始K线


@dataclass
class Fenxing:
    index: int        # 在 processed_bars 中的索引
    type: FenxingType
    high: float       # 分型K线的 high
    low: float        # 分型K线的 low
    fx: float         # 顶分型=high，底分型=low（对齐 czsc FX.fx）
    time: str
    elements: list = field(default_factory=list)  # [k1, k2, k3] 三根K线


@dataclass
class Bi:
    start_idx: int
    end_idx: int
    start_price: float
    end_price: float
    direction: BiDirection
    high: float
    low: float
    # 对齐 czsc BI：fx_a / fx_b 引用分型
    fx_a: Optional[Fenxing] = None
    fx_b: Optional[Fenxing] = None


@dataclass
class Zhongshu:
    zg: float
    zd: float
    gg: float
    dd: float
    start_idx: int   # bi_list 索引
    end_idx: int     # bi_list 索引
    bi_count: int


@dataclass
class BuyPoint:
    point_type: int
    price: float
    time: str
    stop_loss: float
    strength: str
    description: str = ""


# ============================================================
# L0: 数据获取
# ============================================================

def fetch_kline(symbol: str, days: int = 250) -> List[KLine]:
    """日K线获取 — TDX(主力) > 腾讯(fallback)，前复权"""
    # ── 主源: TDX kline-history（更可靠） ──
    try:
        url = f"http://127.0.0.1:8080/api/kline-history?code={symbol[2:]}&period=daily&count={days}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        items = data.get("data", {}).get("list", [])
        if items:
            klines = []
            for item in items[-days:]:
                klines.append(KLine(
                    time=item["date"], open=float(item["open"]), close=float(item["close"]),
                    high=float(item["high"]), low=float(item["low"]), volume=float(item.get("volume", item.get("vol", 0)))
                ))
            return klines
    except Exception:
        pass

    # ── 备源: TDX kline ──
    try:
        url = f"http://127.0.0.1:8080/api/kline?code={symbol[2:]}&period=daily&count={days}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        items = data.get("data", {}).get("list", [])
        if items:
            klines = []
            for item in items:
                klines.append(KLine(
                    time=item["date"], open=float(item["open"]), close=float(item["close"]),
                    high=float(item["high"]), low=float(item["low"]), volume=float(item["volume"])
                ))
            return klines
    except Exception:
        pass

    # ── 备源: 腾讯 ──
    try:
        url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={symbol},day,,,300,qfq"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0", "Referer": "https://gu.qq.com/"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        items = data.get("data", {}).get(symbol, {}).get("qfqday", [])
        if isinstance(items, str):
            items = json.loads(items)
        if not items:
            return []
        # klines 从 API 返回时正序（旧→新），直接用
        klines = []
        for item in items[-days:]:
            klines.append(KLine(
                time=item[0], open=float(item[1]), close=float(item[2]),
                high=float(item[3]), low=float(item[4]), volume=float(item[5])
            ))
        return klines
    except Exception as e:
        print(f"⚠️ K线获取失败: {e}", file=sys.stderr)
        return []


def fetch_stock_name(symbol: str) -> str:
    """获取股票名称"""
    try:
        url = f"https://web.ifzq.gtimg.cn/appstock/app/quotekq/get?param={symbol}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        info = data.get("data", {}).get(symbol, {})
        return info.get("name", symbol)
    except:
        return symbol


# ============================================================
# L1: 包含处理（严格对齐 czsc remove_include）
# ============================================================

def _check_include(k1: KLine, k2: KLine, k3: KLine) -> Tuple[bool, KLine]:
    """
    严格对齐 czsc remove_include：
    输入 k1, k2（无包含关系的已处理K线），k3（原始K线）
    返回 (merged: bool, result: KLine)
    """
    # 方向判断：k1.high < k2.high → Up，k1.high > k2.high → Down
    if k1.high < k2.high:
        direction_up = True
    elif k1.high > k2.high:
        direction_up = False
    else:
        # 高点相等，直接保留 k3
        return False, KLine(time=k3.time, open=k3.open, high=k3.high,
                            low=k3.low, close=k3.close, volume=k3.volume, elements=[k3])

    # 包含判断：k2 包含 k3，或 k3 包含 k2
    has_include = (k2.high >= k3.high and k2.low <= k3.low) or \
                  (k3.high >= k2.high and k3.low <= k2.low)

    if not has_include:
        return False, KLine(time=k3.time, open=k3.open, high=k3.high,
                            low=k3.low, close=k3.close, volume=k3.volume, elements=[k3])

    # 合并：取 k2 + k3 的所有 elements
    elems = list(k2.elements) if k2.elements else [k2]
    if k3.time != (elems[-1].time if elems else ""):
        elems.append(k3)

    if direction_up:
        # 向上：取高点最大、低点最大（取强势端）
        new_high = max(k2.high, k3.high)
        new_low = max(k2.low, k3.low)
        # 时间戳：取高点所在的K线
        dt = k2.time if k2.high >= k3.high else k3.time
    else:
        # 向下：取高点最小、低点最小（取弱势端）
        new_high = min(k2.high, k3.high)
        new_low = min(k2.low, k3.low)
        # 时间戳：取低点所在的K线
        dt = k2.time if k2.low <= k3.low else k3.time

    new_vol = (k2.volume or 0) + (k3.volume or 0)
    # open/close：取 k3 的（后续K线为准）
    new_close = k3.close if direction_up else k3.close

    return True, KLine(time=dt, open=k3.open, high=new_high, low=new_low,
                       close=new_close, volume=new_vol, elements=elems)


def process_inclusion(klines: List[KLine]) -> List[KLine]:
    """包含处理：对齐 czsc 逐步滑动窗口算法"""
    if len(klines) < 3:
        # 不足3根，无法做包含处理，保留前2根
        result = [KLine(time=k.time, open=k.open, high=k.high, low=k.low,
                        close=k.close, volume=k.volume, elements=[k]) for k in klines[:2]]
        return result

    result = []
    for k in klines[:2]:
        result.append(KLine(time=k.time, open=k.open, high=k.high, low=k.low,
                            close=k.close, volume=k.volume, elements=[k]))

    for k3 in klines[2:]:
        k1, k2 = result[-2], result[-1]
        merged, new_k = _check_include(k1, k2, k3)
        if merged:
            result[-1] = new_k
        else:
            result.append(new_k)

    return result


# ============================================================
# L2: 分型识别（严格对齐 czsc check_fx / check_fxs）
# ============================================================

def _check_fx(k1: KLine, k2: KLine, k3: KLine) -> Optional[Fenxing]:
    """
    对齐 czsc check_fx：严格 > / < （非 >= / <=）
    顶分型：k2.high > k1.high 且 k2.high > k3.high 且 k2.low > k1.low 且 k2.low > k3.low
    底分型：k2.high < k1.high 且 k2.high < k3.high 且 k2.low < k1.low 且 k2.low < k3.low
    """
    # 顶分型
    if k1.high < k2.high > k3.high and k1.low < k2.low > k3.low:
        return Fenxing(index=k2.elements[0].index if hasattr(k2, 'index') else 0,
                       type=FenxingType.TOP, high=k2.high, low=k2.low, fx=k2.high,
                       time=k2.time, elements=[k1, k2, k3])
    # 底分型
    if k1.low > k2.low < k3.low and k1.high > k2.high < k3.high:
        return Fenxing(index=k2.elements[0].index if hasattr(k2, 'index') else 0,
                       type=FenxingType.BOTTOM, high=k2.high, low=k2.low, fx=k2.low,
                       time=k2.time, elements=[k1, k2, k3])
    return None


def identify_fenxing(bars: List[KLine]) -> List[Fenxing]:
    """
    对齐 czsc check_fxs：
    1. 遍历 bars[1:-1]，三根一窗口检测分型
    2. 强制顶底交替（连续同类型跳过）
    3. 返回分型列表
    """
    fxs = []
    for i in range(1, len(bars) - 1):
        fx = _check_fx(bars[i - 1], bars[i], bars[i + 1])
        if fx is None:
            continue
        # 对齐 czsc：强制顶底交替
        if len(fxs) >= 1 and fx.type == fxs[-1].type:
            continue
        fx.index = i  # 在 processed_bars 中的索引
        fxs.append(fx)

    return fxs


# ============================================================
# L3: 笔生成（严格对齐 czsc check_bi）
# ============================================================

def generate_bi(bars: List[KLine], fxs: List[Fenxing], min_bi_len: int = 5) -> List[Bi]:
    """
    对齐 czsc check_bi 算法：
    1. 从 fxs[0] 开始（第一个分型）
    2. 如果是底分型(D)，找后续的顶分型(G)，条件：dt > fx_a.dt 且 fx > fx_a.fx（突破）
    3. 在所有满足条件的 G 中选 high 最高的
    4. 检查 fx_a/fx_b 价格范围是否包含（有包含则返回 None）
    5. 检查 bars_a 长度 >= min_bi_len
    6. 形成一笔后，将剩余 bars 递归处理
    """
    if len(fxs) < 2:
        return []

    fx_a = fxs[0]

    if fx_a.type == FenxingType.BOTTOM:
        # 找突破的顶分型：dt > fx_a.dt 且 fx（high）> fx_a.fx（low）
        candidates = [x for x in fxs[1:] if x.type == FenxingType.TOP
                      and x.fx > fx_a.fx]
        if not candidates:
            return []
        # czsc: 选 high 最高的
        fx_b = max(candidates, key=lambda x: x.high)
        direction = BiDirection.UP
    elif fx_a.type == FenxingType.TOP:
        # 找突破的底分型：dt > fx_a.dt 且 fx（low）< fx_a.fx（high）
        candidates = [x for x in fxs[1:] if x.type == FenxingType.BOTTOM
                      and x.fx < fx_a.fx]
        if not candidates:
            return []
        # czsc: 选 low 最低的
        fx_b = min(candidates, key=lambda x: x.low)
        direction = BiDirection.DOWN
    else:
        return []

    # 价格范围包含检查（对齐 czsc ab_include）
    ab_include = ((fx_a.high > fx_b.high and fx_a.low < fx_b.low) or
                  (fx_a.high < fx_b.high and fx_a.low > fx_b.low))
    if ab_include:
        return []

    # 范围：fx_a.elements[0].dt ~ fx_b.elements[2].dt 对应的 bars
    # 我们的 bars 用 index 定位
    start_bar_idx = fx_a.index
    end_bar_idx = fx_b.index
    bars_count = end_bar_idx - start_bar_idx + 1

    if bars_count < min_bi_len:
        return []

    # 形成 BI
    start_price = fx_a.fx  # 底=low，顶=high
    end_price = fx_b.fx

    if direction == BiDirection.UP:
        bi_high = max(fx_a.high, fx_b.high)
        bi_low = min(fx_a.low, fx_b.low)
    else:
        bi_high = max(fx_a.high, fx_b.high)
        bi_low = min(fx_a.low, fx_b.low)

    bi = Bi(
        start_idx=start_bar_idx, end_idx=end_bar_idx,
        start_price=round(start_price, 2), end_price=round(end_price, 2),
        direction=direction, high=round(bi_high, 2), low=round(bi_low, 2),
        fx_a=fx_a, fx_b=fx_b,
    )

    # 递归处理剩余 bars（从 fx_b 的位置继续）
    # 找 fx_b 之后的分型
    remaining_fxs = [x for x in fxs if x.index >= fx_b.index]
    remaining_bars = bars[fx_b.index:]

    more_bis = generate_bi(remaining_bars, remaining_fxs, min_bi_len)

    return [bi] + more_bis


# ============================================================
# L4: 中枢构建
# ============================================================

def build_zhongshu(bi_list: List[Bi]) -> List[Zhongshu]:
    """基于3笔重叠区构建中枢（标准缠论定义）"""
    if len(bi_list) < 3:
        return []

    zhongshu_list = []
    i = 0
    while i < len(bi_list) - 2:
        b1, b2, b3 = bi_list[i], bi_list[i + 1], bi_list[i + 2]
        zg = min(b1.high, b2.high, b3.high)
        zd = max(b1.low, b2.low, b3.low)

        if zg > zd:
            gg = max(b1.high, b2.high, b3.high)
            dd = min(b1.low, b2.low, b3.low)
            end_idx = i + 2

            for j in range(i + 3, len(bi_list)):
                next_bi = bi_list[j]
                new_zg = min(zg, next_bi.high)
                new_zd = max(zd, next_bi.low)

                if new_zg > new_zd:
                    zg, zd = new_zg, new_zd
                    gg = max(gg, next_bi.high)
                    dd = min(dd, next_bi.low)
                    end_idx = j
                else:
                    break

            zhongshu_list.append(Zhongshu(
                zg=round(zg, 2), zd=round(zd, 2),
                gg=round(gg, 2), dd=round(dd, 2),
                start_idx=i, end_idx=end_idx,
                bi_count=end_idx - i + 1
            ))
            i = end_idx + 1
        else:
            i += 1

    return zhongshu_list


# ============================================================
# L5: MACD & 买卖点
# ============================================================

def calc_ema(values: List[float], period: int) -> List[float]:
    if len(values) < period:
        return []
    k = 2 / (period + 1)
    ema = [sum(values[:period]) / period]
    for v in values[period:]:
        ema.append(v * k + ema[-1] * (1 - k))
    return ema


def calculate_macd(closes: List[float], fast: int = 12, slow: int = 26,
                   signal: int = 9) -> dict:
    if len(closes) < slow:
        return {'dif': [], 'dea': [], 'macd_hist': []}
    ema_fast = calc_ema(closes, fast)
    ema_slow = calc_ema(closes, slow)
    dif = [f - s for f, s in zip(ema_fast, ema_slow)]
    dea = calc_ema(dif, signal)
    macd_hist = [(d - e) * 2 for d, e in zip(dif, dea)]
    return {'dif': dif, 'dea': dea, 'macd_hist': macd_hist}


def detect_divergence(macd_hist: List[float], bi_list: List[Bi],
                      zhongshu: Zhongshu) -> dict:
    """背驰检测 - 面积法（MACD柱绝对值面积）"""
    if len(bi_list) < zhongshu.end_idx + 2:
        return {'divergence': False}

    bi_in = bi_list[zhongshu.start_idx - 1] if zhongshu.start_idx > 0 else None
    bi_out = bi_list[zhongshu.end_idx + 1] if zhongshu.end_idx + 1 < len(bi_list) else None

    if bi_in is None or bi_out is None:
        return {'divergence': False}

    def calc_area(start, end, direction):
        if start >= end or end > len(macd_hist):
            return 0
        return sum(abs(macd_hist[i]) for i in range(start, end))

    in_area = calc_area(bi_in.start_idx, bi_in.end_idx, bi_in.direction)
    out_area = calc_area(bi_out.start_idx, bi_out.end_idx, bi_out.direction)

    is_div = False
    if bi_in.direction == BiDirection.UP and bi_out.direction == BiDirection.UP:
        is_div = bi_out.end_price < bi_in.end_price and out_area < in_area
    elif bi_in.direction == BiDirection.DOWN and bi_out.direction == BiDirection.DOWN:
        is_div = bi_out.end_price > bi_in.end_price and out_area < in_area

    return {'divergence': is_div, 'in_area': in_area, 'out_area': out_area}


def detect_buy_points(bars: List[KLine], bi_list: List[Bi],
                      zhongshu_list: List[Zhongshu],
                      macd_hist: List[float]) -> List[BuyPoint]:
    """检测1买、2买、3买"""
    buy_points = []

    if not zhongshu_list:
        return buy_points

    zs = zhongshu_list[-1]
    time_str = bars[-1].time if bars else ""

    # 1买：中枢下方，底背驰
    if zs and bi_list and bi_list[-1].direction == BiDirection.DOWN:
        div = detect_divergence(macd_hist, bi_list, zs)
        if div.get('divergence'):
            bp = BuyPoint(
                point_type=1, price=round(bi_list[-1].end_price, 2),
                time=time_str, stop_loss=round(zs.zd, 2),
                strength="强" if div.get('out_area', 0) < div.get('in_area', 0) * 0.5 else "中",
                description=f"1买：中枢下方底背驰 (ZD={zs.zd})"
            )
            buy_points.append(bp)

    # 2买：回调不破中枢ZD
    if zs and len(bi_list) >= 2:
        last_bi = bi_list[-1]
        prev_bi = bi_list[-2]
        if last_bi.direction == BiDirection.DOWN and prev_bi.direction == BiDirection.UP:
            if last_bi.low > zs.zd:
                bp = BuyPoint(
                    point_type=2, price=round(last_bi.end_price, 2),
                    time=time_str, stop_loss=round(last_bi.low * 0.98, 2),
                    strength="中",
                    description=f"2买：回调不破ZD ({zs.zd})"
                )
                buy_points.append(bp)

    # 3买：回踩中枢上沿
    if zs and len(bi_list) >= 3:
        last_bi = bi_list[-1]
        if last_bi.direction == BiDirection.DOWN and last_bi.low >= zs.zg:
            bp = BuyPoint(
                point_type=3, price=round(last_bi.end_price, 2),
                time=time_str, stop_loss=round(zs.zg * 0.98, 2),
                strength="弱",
                description=f"3买：回踩ZG ({zs.zg})"
            )
            buy_points.append(bp)

    return buy_points


# ============================================================
# Main Analyzer
# ============================================================

class ChanLunAnalyzer:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.name = fetch_stock_name(symbol)
        self.klines: List[KLine] = []
        self.processed: List[KLine] = []
        self.fenxing_list: List[Fenxing] = []
        self.bi_list: List[Bi] = []
        self.zhongshu_list: List[Zhongshu] = []
        self.macd_data: dict = {}
        self.buy_points: List[BuyPoint] = []

    def analyze(self, days: int = 250) -> dict:
        self.klines = fetch_kline(self.symbol, days)
        if len(self.klines) < 50:
            return self._empty_result("K线数据不足")

        # L1: 包含处理
        self.processed = process_inclusion(self.klines)

        # L2: 分型识别
        self.fenxing_list = identify_fenxing(self.processed)

        if len(self.fenxing_list) < 4:
            return self._empty_result("分型不足")

        # L3: 笔生成
        self.bi_list = generate_bi(self.processed, self.fenxing_list)

        if not self.bi_list:
            return self._empty_result("笔不足")

        # L4: 中枢构建
        self.zhongshu_list = build_zhongshu(self.bi_list)

        # L5: MACD + 买卖点
        closes = [k.close for k in self.processed]
        self.macd_data = calculate_macd(closes)
        self.buy_points = detect_buy_points(
            self.processed, self.bi_list, self.zhongshu_list, self.macd_data["macd_hist"])

        return self.get_result()

    def _empty_result(self, reason: str) -> dict:
        return {"symbol": self.symbol, "name": self.name, "error": reason}

    def get_result(self) -> dict:
        price = self.processed[-1].close if self.processed else 0

        structure = "震荡"
        if len(self.zhongshu_list) >= 2:
            zs1, zs2 = self.zhongshu_list[-2], self.zhongshu_list[-1]
            if zs2.zd > zs1.gg:
                structure = "上涨趋势"
            elif zs2.zg < zs1.dd:
                structure = "下跌趋势"

        active_zs = None
        if self.zhongshu_list:
            zs = self.zhongshu_list[-1]
            active_zs = {"zg": round(zs.zg, 2), "zd": round(zs.zd, 2),
                         "gg": round(zs.gg, 2), "dd": round(zs.dd, 2),
                         "bi_count": zs.bi_count}

        recent_bps = []
        for bp in self.buy_points[-5:]:
            recent_bps.append({
                "type": bp.point_type,
                "price": round(bp.price, 2),
                "time": bp.time,
                "stop_loss": round(bp.stop_loss, 2),
                "strength": bp.strength,
                "description": bp.description,
            })

        latest_bp_days = 999
        for bp in reversed(self.buy_points):
            if bp.point_type in (1, 2, 3):
                try:
                    latest_bp_days = (date.today() - date.fromisoformat(bp.time)).days
                except:
                    pass
                break

        # 完整笔列表
        all_bi = []
        for bi in self.bi_list:
            s_time = self.processed[bi.start_idx].time if bi.start_idx < len(self.processed) else ""
            e_time = self.processed[bi.end_idx].time if bi.end_idx < len(self.processed) else ""
            all_bi.append({
                "direction": bi.direction.name,
                "start_idx": bi.start_idx, "end_idx": bi.end_idx,
                "start_price": round(bi.start_price, 2),
                "end_price": round(bi.end_price, 2),
                "high": round(bi.high, 2), "low": round(bi.low, 2),
                "start_time": s_time, "end_time": e_time,
            })

        # 完整中枢列表
        all_zs = []
        for zs in self.zhongshu_list:
            first_bi = self.bi_list[zs.start_idx] if zs.start_idx < len(self.bi_list) else None
            last_bi = self.bi_list[zs.end_idx] if zs.end_idx < len(self.bi_list) else None
            s_time = self.processed[first_bi.start_idx].time if first_bi and first_bi.start_idx < len(self.processed) else ""
            e_time = self.processed[last_bi.end_idx].time if last_bi and last_bi.end_idx < len(self.processed) else ""
            all_zs.append({
                "zg": round(zs.zg, 2), "zd": round(zs.zd, 2),
                "gg": round(zs.gg, 2), "dd": round(zs.dd, 2),
                "bi_count": zs.bi_count,
                "bi_start": zs.start_idx, "bi_end": zs.end_idx,
                "start_time": s_time, "end_time": e_time,
            })

        processed_bars = [{"time": p.time, "open": round(p.open, 2),
                           "high": round(p.high, 2), "low": round(p.low, 2),
                           "close": round(p.close, 2)} for p in self.processed]

        fenxing_data = []
        for fx in self.fenxing_list:
            fx_time = self.processed[fx.index].time if fx.index < len(self.processed) else ""
            fenxing_data.append({"index": fx.index, "type": fx.type.value,
                                 "high": round(fx.high, 2), "low": round(fx.low, 2),
                                 "fx": round(fx.fx, 2), "time": fx_time})

        return {
            "symbol": self.symbol,
            "name": self.name,
            "price": round(price, 2),
            "structure": structure,
            "active_zhongshu": active_zs,
            "zhongshu_list": all_zs,
            "bi_list": all_bi,
            "fenxing_list": fenxing_data,
            "processed_bars": processed_bars,
            "buy_points": recent_bps,
            "latest_bp_days": latest_bp_days,
            "stats": {
                "klines": len(self.klines),
                "processed": len(self.processed),
                "fenxing": len(self.fenxing_list),
                "bi": len(self.bi_list),
                "zhongshu": len(self.zhongshu_list),
            },
        }


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Copaw 缠论分析引擎 v3.0 (czsc-aligned)")
    parser.add_argument("--symbol", help="股票代码 (sh600519)")
    parser.add_argument("--symbols", help="多股逗号分隔")
    parser.add_argument("--days", type=int, default=250)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    symbols = []
    if args.symbol:
        symbols = [args.symbol]
    elif args.symbols:
        symbols = args.symbols.split(",")

    results = []
    for sym in symbols:
        analyzer = ChanLunAnalyzer(sym)
        r = analyzer.analyze(args.days)
        results.append(r)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            if "error" in r:
                print(f"⚠️ {r['symbol']}: {r['error']}")
                continue
            print(f"\n{'='*50}")
            print(f"📊 {r['name']}（{r['symbol']}）")
            print(f"   价格: {r['price']}  结构: {r['structure']}")
            print(f"   笔: {r['stats']['bi']}  中枢: {r['stats']['zhongshu']}  分型: {r['stats']['fenxing']}")
            if r.get('active_zhongshu'):
                zs = r['active_zhongshu']
                print(f"   活跃中枢: ZG={zs['zg']} ZD={zs['zd']} GG={zs['gg']} DD={zs['dd']}")
            for bp in r.get('buy_points', []):
                print(f"   🔔 {bp['type']}买 {bp['price']} ({bp['time']}) {bp['strength']}")
            print(f"{'='*50}")


if __name__ == "__main__":
    main()
