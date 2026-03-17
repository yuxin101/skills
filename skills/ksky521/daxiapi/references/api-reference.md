# Coze API 详细参考文档

**Base URL:** `https://daxiapi.com/coze`

---

## GET 接口

### get_index_k
获取上证指数的K线数据（最近30天）

**请求方式:** `GET`

**请求示例:**
```javascript
fetch('/coze/get_index_k', {
    headers: { 'X-API-Token': 'your_token' }
})
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| name | 指数名称 |
| klines[].date | 日期 |
| klines[].open | 开盘价 |
| klines[].close | 收盘价 |
| klines[].high | 最高价 |
| klines[].low | 最低价 |
| klines[].vol | 成交量 |

---

### get_market_data
获取A股市场主流指数信息，包括名称、涨跌幅、市场宽度等

**请求方式:** `GET`

**响应字段:**
| 字段 | 说明 |
|------|------|
| above_ma200_ratio | 全市场股票在200日均线之上的占比 |
| index[] | 主流指数列表 |
| index[].name | 指数名称 |
| index[].cs | 短期动量CS |
| index[].zdf | 当日涨跌幅(%) |
| index[].zdf5/zdf10/zdf20/zdf30 | 5/10/20/30日涨跌幅 |
| zdfRange | 涨跌幅区间分布 |

---

### get_market_degree
获取A股市场温度，判断市场冷热程度

**请求方式:** `GET`

**用途:** 市场冷清时考虑抄底，过热时考虑卖出

**响应内容:** 包含市场温度、估值指标、抄底信号等综合分析文本

---

### get_market_style
获取大小盘风格数据

**请求方式:** `GET`

**响应字段:**
| 字段 | 说明 |
|------|------|
| 日期 | 交易日期 |
| 大小盘波动差值 | 正值大盘强，负值小盘强 |

---

### get_market_end_news
获取收盘新闻信息

**请求方式:** `GET`

**响应字段:**
| 字段 | 说明 |
|------|------|
| title | 新闻标题 |
| summary | 新闻摘要 |
| content | 新闻内容 |
| showTime | 发布时间 |
| uniqueUrl | 新闻链接 |

---

### get_market_value_data
获取市场主流指数估值数据（PE/PB/温度）

**请求方式:** `GET`

**用途:** 评估指数估值水平，指导定投和止盈

**投资建议:**
- 买入：20°C以下慢慢定投，10°C以下加量，5°C以下提升额度
- 卖出：60°C以上关注止盈，80°C以上分批止盈

**响应字段:**
| 字段 | 说明 |
|------|------|
| name | 指数名称 |
| PE | 市盈率 |
| PEPercentile | PE历史分位值 |
| PB | 市净率 |
| PBPercentile | PB历史分位值 |
| wendu | 综合温度（最重要指标） |

---

### get_zdt_pool
获取市场涨跌停股票表格

**请求方式:** `POST`

**响应:** Markdown格式的涨跌停股票表格

---

### get_gn_table
获取概念板块数据（资金流入、涨跌幅、涨幅7%股票个数）

**请求方式:** `POST`

---

### get_jsl_topics
获取集思录热门话题

**请求方式:** `GET`

---

## POST 接口

### get_stock_data
获取A股个股详细信息

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 股票代码，多个用逗号分隔，最多20个 |

**请求示例:**
```javascript
fetch('/coze/get_stock_data', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ code: '000001,600031' })
})
```

**响应字段（重要）:**
| 字段 | 说明 |
|------|------|
| code/stockId | 股票代码 |
| name | 股票名称 |
| close/price | 收盘价 |
| zdf | 当日涨跌幅(%) |
| zdf_5d/zdf_10d/zdf_20d/zdf_30d | 5/10/20/30日涨跌幅 |
| cs | 短期动量（Close与EMA20乖离率） |
| sm | 中期动量（EMA20与EMA60乖离率） |
| ml | 长期动量（EMA60与EMA120乖离率） |
| rps_score | RPS相对强度（>80为强势股） |
| sctr | 技术排名百分比 |
| ma20/ma50/ma150/ma200 | 各期均线 |
| ema20 | 20日EMA |
| isVCP | 是否VCP形态（1=是） |
| isSOS | 是否SOS强势走势（1=是） |
| isLPS | 是否LPS支撑点（1=是） |
| isSpring | 是否弹簧形态（1=是） |
| isCrossoverBox | 是否突破箱体（1=是） |
| isIB | 是否Inside Bar（1=是） |
| isNR4/isNR7 | 是否振幅收窄4/7天（1=是） |
| tags[] | 标签（Good/LPS/↑TR/H2/Sp） |
| vol/vol1 | 当日/昨日成交量 |
| vcs | 成交量动量（>0为放量） |
| vma5 | 5日均量 |
| high_52w/low_52w | 52周高低点 |
| pe_ttm | 市盈率TTM |
| shizhi_lt | 流通市值 |
| bkId/bkName | 所属板块代码/名称 |
| gainian | 所属概念 |

---

### get_sector_data
获取行业板块热力图

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| orderBy | string | 否 | cs | 排序指标：cs/zdf/zdf5/zdf10/zdf20/cs_avg/stock_cs_avg |
| lmt | integer | 否 | 5 | 返回天数 |

**请求示例:**
```javascript
fetch('/coze/get_sector_data', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ orderBy: 'zdf', lmt: 5 })
})
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| csHeatmap | CS动量热力图（Markdown表格） |
| zdfHeatmap | 当日涨跌幅热力图 |
| crossover | 箱体突破板块信息 |
| topStocksTable | 龙头股表格 |
| cs_gt_ma20_names | CS>CS_MA20的板块名称 |
| cs_gt_5_names | CS>5的板块名称 |

---

### get_sector_rank_stock
获取特定行业的股票排名

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| sectorCode | string | 是 | - | 行业代码（以BK开头） |
| orderBy | string | 否 | cs | 排序指标 |

**orderBy 可选值:**
- `cs` - 短期动量
- `sm` - 中期动量
- `zdf/zdf_5d/zdf_10d/zdf_20d/zdf_30d` - 涨跌幅
- `sctr` - 技术排名
- `cg/cr/cb` - 鳄鱼线乖离率

**请求示例:**
```javascript
fetch('/coze/get_sector_rank_stock', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ sectorCode: 'BK0477', orderBy: 'cs' })
})
```

---

### get_gainian_stock
根据概念获取股票信息

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| gnId | string | 是 | 概念代码 |

**请求示例:**
```javascript
fetch('/coze/get_gainian_stock', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ gnId: 'GN1234' })
})
```

---

### query_stock_data
根据关键字查询股票/行业代码

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| q | string | 是 | - | 关键字/拼音/代码，多个用逗号分隔，最多10个 |
| type | string | 是 | stock | 类型：stock（个股）/ hy（行业） |

**请求示例:**
```javascript
// 查询个股
fetch('/coze/query_stock_data', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ q: '三一重工', type: 'stock' })
})

// 查询行业
fetch('/coze/query_stock_data', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ q: '机械', type: 'hy' })
})
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| code | 股票/行业代码 |
| name | 名称 |
| pinyin | 拼音缩写 |
| type | 类型（stock/hy） |

---

## 错误处理

### 统一响应格式
```json
{
    "errCode": 0,
    "errMsg": "OK",
    "data": { ... }
}
```

### 错误码说明
| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 0 | 成功 | - |
| 401 | Token无效或非VIP | 提示用户检查Token或申请VIP |
| 404 | API不存在 | 检查请求路径和方法 |
| 429 | 请求频率超限 | 等待后重试，每分钟限10次，每日限1000次 |
| 500 | 服务器错误 | 联系管理员 |

---

## 使用场景示例

### 场景1：分析市场整体情况
1. 调用 `get_market_data` 获取市场宽度
2. 调用 `get_market_degree` 获取市场温度
3. 调用 `get_market_style` 判断大小盘风格

### 场景2：自下向上选股
1. 调用 `get_sector_data` 找出强势行业
2. 调用 `get_sector_rank_stock` 获取行业内龙头股
3. 调用 `get_stock_data` 分析个股详细指标

### 场景3：查询特定股票
1. 调用 `query_stock_data` 搜索股票代码
2. 调用 `get_stock_data` 获取详细信息

### 场景4：定投决策
1. 调用 `get_market_value_data` 获取指数估值
2. 根据温度值决定定投金额
