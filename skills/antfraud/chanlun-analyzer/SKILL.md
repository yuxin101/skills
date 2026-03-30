---
name: chanlun-analyzer
description: "缠论分析引擎 v3.0 — 基于czsc算法的6层处理架构（包含处理→分型→笔→中枢→背驰），识别2买/3买卖点。零外部依赖，纯Python实现。触发词：缠论分析、笔和中枢、缠论结构。"
tags: "finance,stock,chanlun,technical-analysis,python"
---

# 缠论分析引擎 v3.0

基于 czsc (waditu/czsc) 算法的纯 Python 缠论引擎，6层确定性买卖点识别。

## 6层处理架构

```
L0 数据获取（腾讯K线 qfq复权日K）
  → L1 包含处理（严格对齐 czsc remove_include）
    → L2 分型识别（顶/底，强制交替，严格 >/<）
      → L3 笔生成（首分型→极端突破→包含检查→min_bi_len）
        → L4 中枢构建（3笔重叠 ZG=min(hi) ZD=max(lo)，支持扩展）
          → L5 动力学信号（MACD柱面积背驰 → 1买/2买/3买）
```

## 买点定义
- **2买**：笔向下离开中枢后，再向下笔不创新低 + MACD柱面积缩小（背驰）
- **3买**：笔向上突破中枢后，回拉笔不进入中枢上沿（ZG）

## 使用

```bash
# 分析单只股票
python3 scripts/chanlun_analyzer.py analyze --symbol sz002815 --days 250

# 输出缠论结构（笔、中枢、买卖点）
python3 scripts/chanlun_analyzer.py analyze --symbol sz002815 --days 250 --json

# 仅输出买卖点信号
python3 scripts/chanlun_analyzer.py signals --symbol sz002815
```

## 输出字段

| 字段 | 说明 |
|------|------|
| pens | 笔序列（方向、起止点） |
| zhongshus | 中枢列表（ZG、ZD、区间） |
| buy_points | 买点信号（类型1/2/3、位置、背驰信息） |
| sell_points | 卖点信号 |
| current_structure | 当前缠论状态描述 |

## 依赖

- Python 3.8+
- 标准库（urllib, json, dataclasses, enum）
- 无第三方依赖

## 数据源
- 腾讯K线接口：`web.ifzq.gtimg.cn/appstock/app/fqkline/get`
- 自动前复权处理
- symbol 格式：`sz002815` / `sh600540`

## 算法严格对齐

- L1 包含处理：严格对齐 czsc remove_include
- L2 分型识别：严格 >/<（非 >=/<=），强制顶底交替
- L3 笔生成：czsc check_bi 算法
- 中枢扩展：后续笔进入中枢区间时自动扩展
- 背驰：MACD柱面积对比法
