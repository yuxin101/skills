# 订单查询管理模块

## 获取订单列表

### 功能描述

根据会员ID、订单状态、下单时间、订单编号搜索订单信息

### 接口路由

GET /order/list/get

### 请求参数说明

| 字段                | 类型     | 是否必传 | 说明                                                    | 示例                     |
|-------------------|--------|------|-------------------------------------------------------|------------------------|
| order_no          | string | 否    | 搜索订单编号                                                | 1010260204182752364533 |
| create_time_start | string | 否    | 下单时间搜索-开始值                                            | 2026-02-02 00:00:00    |
| create_time_end   | string | 否    | 下单时间搜索-结束值                                            | 2026-02-04 23:59:59    | 
| member_id         | int    | 否    | 指定会员ID                                                | 317                    |
| status            | int    | 否    | 订单状态 -1:已关闭 0:待支付 10:待发货 11:部分发货 20:待收货 21:待自提 30:已完成 | 0                      |
| page              | int    | 否    | 页码，不传缺省为1                                             | 1                      |
| page_size         | int    | 否    | 每页数量，不传缺省为6                                           | 6                      |

### 响应参数说明

| 字段                        | 类型     | 说明            | 示例                     |
|---------------------------|--------|---------------|------------------------|
| error                     | int    | 错误码 0:正常 非0错误 | 0                      |
| total                     | int    | 当前搜索条件下总数量    | 1                      |
| page                      | int    | 当前页           | 1                      |
| page_size                 | int    | 每页数量          | 6                      |
| list                      | array  | 订单列表          |                        |
| list[].id                 | int    | 订单ID          | 29057                  |
| list[].order_no           | string | 订单编号          | 1010260204182752364533 |
| list[].pay_price          | float  | 实付金额          | 1898.80                |
| list[].order_type         | int    | 订单类型码         | 10                     |
| list[].activity_type      | int    | 活动类型码         | 22                     |
| list[].status             | int    | 订单状态码         | 11                     |
| list[].create_time        | string | 下单时间          | 2021-12-13 10:10:35    |
| list[].dispatch_type      | int    | 配送方式          | 10                     |
| list[].buyer_name         | string | 收件人姓名         | 收件人姓名                  |
| list[].buyer_mobile       | string | 收件人手机号        | 15888888888            |
| list[].member_id          | int    | 会员ID          | 447                    |
| list[].member_nickname    | string | 会员昵称          | An                     |
| list[].member_realname    | string | 会员真实姓名        | 李可鑫                    |
| list[].member_mobile      | string | 会员手机号         | 15888888888            |
| list[].address            | string | 收货地址          | 浙江省 杭州市 淳安县 啦啦啦        |
| list[].status_text        | string | 订单状态文字        | 部分发货                   |
| list[].order_type_text    | string | 订单类型文字        | 普通订单                   |
| list[].activity_type_text | string | 订单活动类型文字      | 秒杀                     |

### 响应示例

``` json
{
    "error": 0,
    "total": 1,
    "list": [
        {
            "id": "29057",
            "order_no": "1010260204182752364533",
            "pay_price": "1898.80",
            "order_type": "10",
            "activity_type": "22",
            "status": "11",
            "create_time": "2026-02-04 18:27:52",
            "goods_info": [
                {
                    "title": "大疆 DJI Pocket 2 全能套装灵眸云台vlog全景相机 小型户外数码摄像机高清防抖运动相机 大疆口袋相机",
                    "type": "0",
                    "sub_title": "",
                    "option_title": "",
                    "thumb": "https://likexin-shop.v5dev.getpkg.cn/data/attachment/image/25/2024/07/0af3a10324dacd6796695b02a4db63cf.jpg",
                    "goods_id": "8588",
                    "option_id": "0",
                    "total": "1",
                    "price": 1726.95,
                    "price_unit": "1788.00",
                    "price_original": 1726.95,
                    "price_discount": 61.05
                },
                {
                    "title": "大疆 DJI OM 磁吸手机夹 3 Osmo Mobile 6/Osmo Mobile SE/OM 5/OM 4 SE 配件 大疆云台稳定器配件",
                    "type": "0",
                    "sub_title": "",
                    "option_title": "",
                    "thumb": "https://likexin-shop.v5dev.getpkg.cn/data/attachment/image/25/2024/07/f85eacce1c57bb33690870355dd7a05a.jpg",
                    "goods_id": "8590",
                    "option_id": "0",
                    "total": "2",
                    "price": 171.85,
                    "price_unit": "89.00",
                    "price_original": 171.85,
                    "price_discount": 6.15
                }
            ],
            "dispatch_type": "10",
            "buyer_name": "收件人姓名",
            "buyer_mobile": "15888888888",
            "buyer_remark": "",
            "member_id": "317",
            "member_nickname": "An ⁵ᴳ1",
            "member_realname": "李可鑫",
            "member_mobile": "15888888888",
            "address": "浙江省 杭州市 淳安县 啦啦啦",
            "status_text": "部分发货",
            "order_type_text": "普通订单",
            "activity_type_text": null
        }
    ],
    "page": 1,
    "page_size": 20
}
```

## 通过订单编号获取订单ID

### 功能描述

通过订单编号获取订单ID

### 接口路由

GET /order/index/get-id-by-no

### 请求参数说明

| 字段       | 类型     | 是否必传 | 说明   | 示例                 |
|----------|--------|------|------|--------------------|
| order_no | string | 是    | 订单编号 | 101011010101110101 |

### 响应参数说明

| 字段       | 类型  | 说明            | 示例    |
|----------|-----|---------------|-------|
| error    | int | 错误码 0:正常 非0错误 | 0     |
| order_id | int | 订单ID          | 31711 |

### 响应示例

``` json
{
    "error": 0,
    "order_id": "31711"
}
```

## 获取订单状态

### 功能描述

根据订单编号、订单ID查询订单当前状态

### 接口路由

GET /order/index/get-status

### 请求参数说明

| 字段       | 类型  | 是否必传 | 说明                  | 示例  |
|----------|-----|------|---------------------|-----|
| order_no | int | 否    | 订单编号或者订单ID(后端会自动查询) | 184 |

### 响应参数说明

| 字段          | 类型     | 说明            | 示例  |
|-------------|--------|---------------|-----|
| error       | int    | 错误码 0:正常 非0错误 | 0   |
| status      | int    | 订单状态码         | 30  |
| status_text | string | 订单状态文字        | 已完成 |

### 响应示例

``` json
{
    "error": 0,
    "status": "30",
    "status_text": "已完成"
}
```

## 获取订单物流信息

### 功能描述

根据订单编号、订单ID查询订单当前物流信息

### 接口路由

GET /order/index/get-express

### 请求参数说明

| 字段       | 类型  | 是否必传 | 说明                  | 示例  |
|----------|-----|------|---------------------|-----|
| order_no | int | 否    | 订单编号或者订单ID(后端会自动查询) | 184 |

### 响应参数说明

| 字段                            | 类型     | 说明            | 示例                  |
|-------------------------------|--------|---------------|---------------------|
| error                         | int    | 错误码 0:正常 非0错误 | 0                   |
| data                          | object | 物流数据          |                     |
| data.express                  | object | 物流信息          |                     |
| data.express.staus            | int    | 状态码           | 2                   |
| data.express.state_text       | string | 状态文字          | 疑难                  |
| data.express.data             | array  | 物流轨迹          |                     |
| data.express.data[].date_time | string | 日期            | 2026-03-12 11:52:29 |
| data.express.data[].step      | string | 位置            | 已离开 山东济南分拨交付中心      |
| data.express_com              | string | 物流公司名称        | 韵达快运                |
| data.express_sn               | string | 物流单号          | 315070238346274     |
| data.address_detail           | int    | 收货地址          | 啦啦啦                 |

### 响应示例

``` json
{
    "error": 0,
    "data": {
        "express": {
            "state": "2",
            "data": [
                {
                    "time": "11:52",
                    "step": "【济南市】已离开 山东济南分拨交付中心；发往 山东潍坊分拨交付中心。（如遇物流问题无需找商家/平台，拨打专属电话：0531-75643530为您解决，或关注“韵达快递”官方微信公众号获取实时物流信息）",
                    "date_time": "2026-03-12 11:52:29",
                    "short_date": "03-12"
                },
                ...
                {
                    "time": "16:18",
                    "step": "【南京市】江苏南京浦口区新城公司-余小花（17721565294） 已揽收（如遇物流问题无需找商家/平台，拨打专属电话：025-66971817为您解决，或关注“韵达快递”官方微信公众号获取实时物流信息）",
                    "date_time": "2026-03-11 16:18:16",
                    "short_date": "03-11"
                }
            ],
            "state_text": "疑难"
        },
        "express_com": "韵达快运",
        "express_sn": "315070238346274",
        "address_detail": "啦啦啦"
    }
}
```

## 关闭待支付订单

### 功能描述

通过订单ID关闭待支付的订单

### 接口路由

POST /order/operation/close

| 字段 | 类型  | 是否必传 | 说明   | 示例  |
|----|-----|------|------|-----|
| id | int | 是    | 订单ID | 184 |

### 响应参数说明

| 字段      | 类型     | 说明              | 示例    |
|---------|--------|-----------------|-------|
| error   | int    | 错误码 0:正常 非0错误   | 0     |
| message | string | 错误信息 error非0时返回 | 订单不存在 |

### 响应示例

``` json
{
    "error": 0
}
```
