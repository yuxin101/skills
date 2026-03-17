---
name: FTShare-etf-data
description: A 股 ETF 数据技能集（market.ft.tech）。覆盖单只 ETF 详情、ETF 分页列表（排序/筛选）、ETF K 线（日/周/月/年线）、ETF 分钟级分时、ETF PCF 列表与下载。用户询问某只 ETF 行情、ETF 列表、ETF K 线、分时或 PCF 申购赎回清单时使用。
---

# FT ETF 数据 Skills

本 skill 是 `FTShare-etf-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」或「询问方式与子 skill 对应表」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名。ETF 行情类子 skill（etf-detail、etf-list-paginated、etf-ohlcs、etf-prices）请求头已内置 `X-Client-Name: ft-web`；PCF 子 skill（etf-pcfs、etf-pcf-download）无需该请求头。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> etf-detail --etf 510050.XSHG
python <RUN_PY> etf-list-paginated --order_by "change_rate desc" --page_size 20 --page_no 1
python <RUN_PY> etf-ohlcs --etf 510050.XSHG --span DAY1 --limit 50
python <RUN_PY> etf-prices --etf 510050.XSHG --since TODAY
python <RUN_PY> etf-pcfs --date 20260309
python <RUN_PY> etf-pcf-download --filename pcf_159003_20260309.xml --output pcf_159003_20260309.xml
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## ETF — 询问方式与子 skill 对应表

| 询问方式（用户常说的词） | 子 skill |
|------------------------|----------|
| 某只 **ETF 详情**、**510050 行情**、**上证50ETF** 涨跌幅、ETF **跟踪指数/市值**、某只 ETF 名称/盘口 | `etf-detail` |
| **ETF 列表**、**全市场 ETF**、**按涨跌幅排序的 ETF**、**筛选某类 ETF** | `etf-list-paginated` |
| 某只 ETF 的 **K 线**、**510050 日线/周线/月线/年线**、ETF **开高低收**、**MA5/MA10/MA20** | `etf-ohlcs` |
| 某只 ETF **分时**、**510050 当日分时**、ETF **一分钟行情**、**多日分时走势** | `etf-prices` |
| **ETF PCF**、**申购赎回清单**、**指定日期 PCF 列表**、PCF 文件列表 | `etf-pcfs` |
| **下载 PCF**、**PCF 文件内容**、某只 ETF **申购赎回清单 XML**、pcf_xxx.xml | `etf-pcf-download` |

---

## 能力总览

- **`etf-detail`**：查询单只 ETF 详情（名称、行情、盘口、市值、涨跌幅、跟踪指数、投资类型等）。必填：`--etf`；可选 `--masks`。
- **`etf-list-paginated`**：ETF 分页列表，支持分页、排序、筛选。可选：`--order_by`/`--ob`、`--filter`、`--masks`、`--page_size`、`--page_no`、`--filter_index`。
- **`etf-ohlcs`**：查询单只 ETF OHLC K 线（开高低收、成交量、成交额），附带 MA5/MA10/MA20。必填：`--etf`、`--span`（DAY1/WEEK1/MONTH1/YEAR1）；可选 `--limit`、`--until_ts_ms`。
- **`etf-prices`**：查询单只 ETF 分钟级分时价格。必填：`--etf`；时间范围二选一：`--since`（TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(n)）或 `--since_ts_ms`。
- **`etf-pcfs`**：指定日期 ETF PCF 列表（申购赎回清单文件列表）。必填：`--date`（YYYYMMDD）；可选：`--page`、`--page_size`。
- **`etf-pcf-download`**：按文件名下载 PCF XML 文件。必填：`--filename`；可选：`--output`（保存到当前工作目录下路径）。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「询问方式与子 skill 对应表」或「能力总览」匹配子 skill 名称。
3. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解接口与参数。
4. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
5. **解析并输出**：以表格或要点形式展示给用户。
