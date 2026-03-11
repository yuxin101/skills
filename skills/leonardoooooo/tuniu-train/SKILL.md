---
name: tuniu-train
description: 途牛火车票助手 - 通过 exec + curl 调用 MCP 实现车次列表搜索、查询车次详情、预订下单。适用于用户查询车次列表、查询车次详情或提交火车票订单时使用。
version: 1.0.0
metadata: {"openclaw": {"emoji": "✈️", "category": "travel", "tags": ["途牛", "火车票", "车次详情", "下单"], "requires": {"bins": ["curl"]}, "env": {"TUNIU_API_KEY": {"type": "string", "description": "途牛开放平台 API key，用于 apiKey 请求头", "required": true}}}}
---

# 途牛火车票票助手

当用户查询车次列表、查询具体车次详情或火车票预订时，使用此 skill 通过 exec 执行 curl 调用途牛火车票票 MCP 服务。

## 运行环境要求

本 skill 通过 **shell exec** 执行 **curl** 向 MCP endpoint 发起 HTTP POST 请求，使用 JSON-RPC 2.0 / `tools/call` 协议。**运行环境必须提供 curl 或等效的 HTTP 调用能力**（如 wget、fetch 等可发起 POST 的客户端），否则无法调用 MCP 服务。

## 隐私与个人信息（PII）说明

预订功能会将用户提供的**个人信息**（联系人姓名、手机号、乘机人姓名、证件号等）通过 HTTP POST 发送至途牛火车票票 MCP 远端服务（`https://openapi.tuniu.cn/mcp/train`） ，以完成火车票预订。使用本 skill 即表示用户知晓并同意上述 PII 被发送到外部服务。请勿在日志或回复中暴露用户个人信息。

## 适用场景

- 按出发站、到达站、出发日期查询车次列表（第一页、翻页）
- 查看指定车次的坐等价格信息
- 用户确认后创建火车票票预订订单

## 配置要求

### 必需配置

- **TUNIU_API_KEY**：途牛开放平台 API key，用于 `apiKey` 请求头

用户需在[途牛开放平台](https://open.tuniu.com/mcp)注册并获取上述密钥。

### 可选配置

- **TRAIN_MCP_URL**：MCP 服务地址，默认 `https://openapi.tuniu.cn/mcp/train`

## 调用方式

**直接调用工具**：使用以下请求头调用 `tools/call` 即可：

- `apiKey: $TUNIU_API_KEY`
- `Content-Type: application/json`
- `Accept: application/json, text/event-stream`

## 可用工具

**重要**：下方示例中的参数均为占位，调用时需**根据用户当前需求**填入实际值（出发站、出发日期、车次号、乘机人、联系方式等），勿直接照抄示例值。

### 1. 查询车次列表 (searchLowestPriceTrain)

**第一页**：必填 `departureCityName`、`arrivalCityName`、`departureDate`（格式 yyyy-MM-dd）。

**翻页**：传入首次查询返回的快照id(queryId)和 `pageNum`（2=第二页，3=第三页…）。用户说「还有吗」「翻页」「下一页」时用queryId + pageNum 再次调用即可。

**触发词**：查询某日出发某站到某站的火车票

```bash
# 第一页：出发城市、到达城市、日期按用户需求填写（日期格式 YYYY-MM-DD）
curl -s -X POST "${TRAIN_MCP_URL:-https://openapi.tuniu.cn/mcp/train}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "apiKey: $TUNIU_API_KEY" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"searchLowestPriceTrain","arguments":{"departureCityName":"<用户指定的出发站>","arrivalCityName":"<用户指定的到达站>","departureDate":"<用户指定的出发日期 yyyy-MM-dd>"}}}'
```

```bash
# 翻页：传相同的城市日期 + pageNum
curl -s -X POST "${TRAIN_MCP_URL:-https://openapi.tuniu.cn/mcp/train}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "apiKey: $TUNIU_API_KEY" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"searchLowestPriceTrain","arguments":{"queryId":"<快照id>","pageNum":2}}}'
```

### 2. 查询车次详情 (queryTrainDetail)

**入参**：`departureStationName`、`arrivalStationName`、`departureDate`（yyyy-MM-dd）、`trainNum`（车次号，从搜索结果获取）均为必填。

**返回**：`trainInfo`（车次详情）、`seatInfo`（坐等信息，含 resId、price等）。**resId、price、departsDate 为下单必填，需保留供 bookTrain 使用。**

**触发词**：车次详情、看一下这个车次、这个车次有什么坐等

```bash
# departureStationName、arrivalStationName、departureDate 从搜索结果或用户需求取，trainNum 从搜索结果取
curl -s -X POST "${TRAIN_MCP_URL:-https://openapi.tuniu.cn/mcp/train}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "apiKey: $TUNIU_API_KEY" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"queryTrainDetail","arguments":{"departureStationName":"<出发站>","arrivalStationName":"<到达站>","departureDate":"<出发日期 yyyy-MM-dd>","trainNum":"<车次号>"}}}'
```

### 3. 预定订单 (bookTrain)

**前置条件**：
- 必须先调用 `searchLowestPriceTrain` 获取车次列表信息
- 必须调用 `queryTrainDetail` 获取车次详情；从返回的 `seatInfo` 中选取坐等，拿到 `resId`、`price`、，从`trainInfo`中获取`departureDate`

**必填参数**：resources(资源信息)、adultTourists（乘客信息）、contact（联系人信息）、acceptStandingTicket(是否接受无座)。

**resources 格式**：
| 字段 | 类型 | 说明 |
|------|------|------|
| resourceId | long | 资源id |
| departsDate | string | 出发日期 |
| adultPrice | BigDecimal | 价格 |


**adultTourists 格式**：

| 字段 | 类型 | 说明                 |
|------|------|--------------------|
| name | string | 姓名                 |
| psptType | number | 证件类型;1:身份证,;2:护照   |
| psptId | string | 证件号码               |
| isStuDisabledArmyPolice| number | 乘客类型;0:成人 |
| tel | string | 手机号                |

**contact 格式**：

| 字段 | 类型 | 说明 |
|------|------|------|
| tel | string | 联系人手机号 |

**触发词**：预订、下单、订火车票

```bash
# resId、price、departureDate 从最近一次 queryTrainDetail 结果取；乘客信息、联系人按用户需求填
curl -s -X POST "${TRAIN_MCP_URL:-https://openapi.tuniu.cn/mcp/train}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "apiKey: $TUNIU_API_KEY" \
  -d '{
    "jsonrpc": "2.0",
    "id": 6,
    "method": "tools/call",
    "params": {
      "name": "bookTrain",
      "arguments": {
        "acceptStandingTicket": false,
        "adultTourists": [
          {
              "isStuDisabledArmyPolice": 0,
              "name": "张宁",
              "psptId": "110101199001014534",
              "psptType": 1,
              "tel": "18888888888"
          }
        ],
        "contact": {
          "tel": "18888888888"
        },
        "resources": [
          {
              "adultPrice": 100.5,
              "departsDate": "2026-03-20",
              "resourceId": 355371385,
              "resourceType": 8
          }
        ]
      }
    }
  }'
```


## 响应处理

### 成功响应

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "..."}]
  },
  "id": 2
}
```

- **本项目中** 工具结果统一放在 **`result.content[0].text`** 中。`text` 为 **JSON 字符串**，需先 `JSON.parse(result.content[0].text)` 再使用。
- 解析后为业务对象，各工具结构不同：
  - **车次列表**（searchLowestPriceTrain）：`successCode`、`data`（车次列表，含 trainNum、departStationName、destStationName、price、seatAvailable 等）。
  - **车次详情**（queryTrainDetail）：`successCode`、`trainInfo`、`seatInfo`（含 resId、price等）。
  - **预定下单**（bookTrain）：`successCode`、`orderId`、`orderDetailUrl`。
- 错误时 `text` 解析后为 `{ "successCode": false, "errorMessage": "错误信息" }`，可从 `errorMessage` 字段取提示文案。

### 错误响应

本项目中错误分两类，需分别处理：

**1. 传输/会话层错误**（无 `result`，仅有顶层 `error`，通常伴随 HTTP 4xx/5xx）：

```json
{
  "jsonrpc": "2.0",
  "error": {"code": -32000, "message": "..."},
  "id": null
}
```
- **Method Not Allowed**：GET 等非 POST 请求
- **Internal server error**（code -32603）：服务内部异常

**2. 工具层错误**（HTTP 仍为 200，有 `result`）：与成功响应结构相同，但 `result.content[0].text` 解析后为 `{ "successCode": false, "errorMessage": "错误信息" }`。例如参数校验失败、舱位信息失效、下单失败等，从 `errorMessage` 字段取文案提示用户或重试。

## 输出格式建议

- **车次列表**：以表格或清单展示车次号、出发/到达站、时间、价格、坐等、剩余座位；可提示「可以说翻页/下一页」
- **车次详情**：分块展示坐等、价格；提示用户可预订
- **预订成功**：明确写出订单号、订单详情链接

## 使用示例

以下示例中，所有参数均从**用户表述或上一轮结果**中解析并填入，勿用固定值。

**用户**：查询2026年3月20日南京到上海的火车票

**AI 执行**：按用户意图填参：departureCityName=南京、arrivalCityName=上海、departureDate=2026-03-20，调用 searchLowestPriceTrain（请求头需带 apiKey、Content-Type、Accept）。解析 result.content[0].text，整理车次列表回复。

**用户**：还有吗？/ 下一页

**AI 执行**：用首次查询返回的快照id(queryId) + pageNum=2（或 3、4…）再次调用 searchLowestPriceTrain。

**用户**：查一下南京南到上海虹桥G203车次详情

**AI 执行**：从上一轮列表确认出发站南京南，到达站上海虹桥，出发日期2026-03-20，车次号G203，调用 queryTrainDetail；解析坐等后展示价格、余票信息，并提示可预订。

**用户**：预定二等座，乘客姓名张宁，乘客身份证号 310101199001011234，乘客手机号 13564789999，联系人手机号 13800138000

**AI 执行**：从最近一次 queryTrainDetail 结果取 resId、price、departsDate；按用户提供的乘客信息填 adultTourists（name=张宁、psptType=1、psptId=310101199001011234、tel=13564789999），contact（tel=13800138000）。成功后回复订单号、订单详情url，并提醒用户完成支付。

## 注意事项

1. **密钥安全**：不要在回复或日志中暴露 TUNIU_API_KEY
2. **PII 安全**：联系人手机号、乘客姓名、证件号等仅在预订时发送至 MCP 服务，勿在日志或回复中暴露
3. **认证**：若遇协议或认证错误，可重试或检查 TUNIU_API_KEY
4. **日期格式**：所有日期均为 yyyy-MM-dd
5. **下单前**：bookTrain 的 resId、price、departsDate 必须来自最近一次 queryTrainDetail 的返回
6. **翻页**：用户要「更多」「下一页」时用快照id(queryId) + pageNum（≥2）调用即可
7. **支付提醒**：下单成功后必须提示用户点击 orderDetailUrl 完成支付