# 数据统计模块

## 待办事项数据

### 功能描述

可以获取待发货订单数量、待处理售后订单数量、待付款订单数量、待补货商品数量、待审核会员数量

### 接口路由

GET /statistics/overview/to-do

### 请求参数说明

无

### 响应参数说明

| 字段                        | 类型     | 说明            | 示例   |
|---------------------------|--------|---------------|------|
| error                     | int    | 错误码 0:正常 非0错误 | 0    |
| data                      | object | 数据            |      |
| data.wait_delivery_order  | int    | 待发货订单数量       | 1737 |
| data.wait_pay_order       | int    | 待支付订单数量       | 943  |
| data.wait_replenish_goods | int    | 待补货商品数量       | 35   |
| data.wait_audit_member    | int    | 待审核会员数量       | 0    |

### 响应示例

``` json
{
    "error": 0,
    "data": {
        "wait_delivery_order": 1737,
        "wait_pay_order": 943,
        "wait_after_sale_order": 83,
        "wait_replenish_goods": 35,
        "wait_audit_member": 0
    }
}
```

## 运营数据

### 功能描述

可以获取指定时间段(今日\昨日\近7日\近30日)内的成交金额(元)、退款金额(元)、支付订单数

### 接口路由

GET /statistics/overview/operational

### 请求参数说明

| 字段     | 类型     | 是否必传 | 说明                                             | 示例    |
|--------|--------|------|------------------------------------------------|-------|
| period | string | 是    | 查询区间 today:今日 yesterday:昨日 week:近7日 month:近30日 | today |

### 响应参数说明

| 字段                                      | 类型     | 说明                         | 示例     |
|-----------------------------------------|--------|----------------------------|--------|
| error                                   | int    | 错误码 0:正常 非0错误              | 0      |
| data                                    | object | 数据                         |        |
| data.order_pay_price                    | float  | 成交金额(元)                    | 139    |
| data.order_refund_price                 | float  | 退款金额(元)                    | 120.25 |
| data.order_pay                          | int    | 支付订单数(笔)                   | 2      |
| data.unit_price                         | float  | 笔单价(元)                     | 0      |
| data.guest_unit_price                   | int    | 客单价(元)                     | 139    |
| data.order_pay_member                   | int    | 支付人数(人)                    | 1      |
| data.compare                            | int    | 与昨日对比(百分比)，period=today时返回 | 0      |
| data.compare.compare_order_pay_price    | int    | 较昨日对比成交金额的比例               | 100    |
| data.compare.compare_order_refund_price | int    | 较昨日对比退款金额的比例               | 100    |
| data.compare.compare_order_pay          | int    | 较昨日对比支付订单数的比例              | 100    |
| data.compare.compare_unit_price         | int    | 较昨日对比笔单价的比例                | 100    |
| data.compare.compare_guest_unit_price   | int    | 较昨日对比客单价的比例                | 100    |
| data.compare.compare_change             | int    | 较昨日对比支付人数的比例               | 100    |

### 响应示例

``` json
{
    "error": 0,
    "data": {
        "order_pay_price": 139,
        "order_refund_price": 120.25,
        "order_pay": 2,
        "unit_price": 69.5,
        "guest_unit_price": 139,
        "order_pay_member": 1,
        "new_member_count": 0,
        "compare": {
            "compare_order_pay_price": 100,
            "compare_order_refund_price": 100,
            "compare_order_pay": 100,
            "compare_unit_price": 100,
            "compare_guest_unit_price": 100,
            "compare_change": 0,
            "compare_new_member_count": 100
        }
    }
}
```

## 新增会员统计

### 功能描述

可以获取指定时间段(今日\昨日\近7日\近30日)内不同渠道的新增会员折线图

### 接口路由

GET /statistics/overview/new-member

### 请求参数说明

| 字段     | 类型     | 是否必传 | 说明                                             | 示例    |
|--------|--------|------|------------------------------------------------|-------|
| period | string | 是    | 查询区间 today:今日 yesterday:昨日 week:近7日 month:近30日 | today |

### 响应参数说明

| 字段                         | 类型     | 说明                 | 示例    |
|----------------------------|--------|--------------------|-------|
| error                      | int    | 错误码 0:正常 非0错误      | 0     |
| data                       | object | 数据                 |       |
| data.mall                  | array  | 综合商城业务的数据，必返       |       |
| data.mall[].period         | string | 时间                 | 00:00 |
| data.mall[].count          | int    | 数量                 | 0     |
| data.communityBuy          | array  | 社区团购业务的数据，有对应业务时返回 |       |
| data.communityBuy[].period | string | 时间                 | 00:00 |
| data.communityBuy[].count  | int    | 数量                 | 0     |
| data.siteApp               | array  | 智慧轻站业务的数据，有对应业务时返回 |       |
| data.siteApp[].period      | string | 时间                 | 00:00 |
| data.siteApp[].count       | int    | 数量                 | 0     |
| data.promoter              | array  | 推客带货业务的数据，有对应业务时返回 |       |
| data.promoter[].period     | string | 时间                 | 00:00 |
| data.promoter[].count      | int    | 数量                 | 0     |

### 响应示例

``` json
{
    "error": 0,
    "data": {
        "mall": [
            {
                "period": "00:00",
                "count": 0
            },
            ...
            {
                "period": "23:00",
                "count": 0
            }
        ],
        "communityBuy": [
            {
                "period": "00:00",
                "count": 0
            },
            ...
            {
                "period": "23:00",
                "count": 0
            }
        ],
        "siteApp": [
            {
                "period": "00:00",
                "count": 0
            },
            ...
            {
                "period": "23:00",
                "count": 0
            }
        ],
        "promoter": [
            {
                "period": "00:00",
                "count": 0
            },
            ...
            {
                "period": "23:00",
                "count": 0
            }
        ]
    }
}
```

## 新增订单统计

### 功能描述

可以获取指定时间段(今日\昨日\近7日\近30日)内不同渠道的的新增订单数折线图

### 接口路由

GET /statistics/overview/new-order

### 请求参数说明

| 字段     | 类型     | 是否必传 | 说明                                             | 示例    |
|--------|--------|------|------------------------------------------------|-------|
| period | string | 是    | 查询区间 today:今日 yesterday:昨日 week:近7日 month:近30日 | today |

### 响应参数说明

| 字段                         | 类型     | 说明                 | 示例    |
|----------------------------|--------|--------------------|-------|
| error                      | int    | 错误码 0:正常 非0错误      | 0     |
| data                       | object | 数据                 |       |
| data.mall                  | array  | 综合商城业务的数据，必返       |       |
| data.mall[].period         | string | 时间                 | 00:00 |
| data.mall[].count          | int    | 数量                 | 0     |
| data.communityBuy          | array  | 社区团购业务的数据，有对应业务时返回 |       |
| data.communityBuy[].period | string | 时间                 | 00:00 |
| data.communityBuy[].count  | int    | 数量                 | 0     |
| data.siteApp               | array  | 智慧轻站业务的数据，有对应业务时返回 |       |
| data.siteApp[].period      | string | 时间                 | 00:00 |
| data.siteApp[].count       | int    | 数量                 | 0     |
| data.promoter              | array  | 推客带货业务的数据，有对应业务时返回 |       |
| data.promoter[].period     | string | 时间                 | 00:00 |
| data.promoter[].count      | int    | 数量                 | 0     |

### 响应示例

``` json
{
    "error": 0,
    "data": {
        "mall": [
            {
                "period": "00:00",
                "count": 0
            },
            ...
            {
                "period": "23:00",
                "count": 0
            }
        ],
        "communityBuy": [
            {
                "period": "00:00",
                "count": 0
            },
            ...
            {
                "period": "23:00",
                "count": 0
            }
        ],
        "siteApp": [
            {
                "period": "00:00",
                "count": 0
            },
            ...
            {
                "period": "23:00",
                "count": 0
            }
        ],
        "promoter": [
            {
                "period": "00:00",
                "count": 0
            },
            ...
            {
                "period": "23:00",
                "count": 0
            }
        ]
    }
}
```

## 浏览量分析

### 功能描述

可以获取指定时间段(今日\昨日\近7日\近30日)内不同渠道访问浏览量数据(PV\VU)，同时可以获取折线图

### 接口路由

GET /statistics/overview/view-data

### 请求参数说明

| 字段     | 类型     | 是否必传 | 说明                                             | 示例    |
|--------|--------|------|------------------------------------------------|-------|
| period | string | 是    | 查询区间 today:今日 yesterday:昨日 week:近7日 month:近30日 | today |

### 响应参数说明

| 字段                            | 类型     | 说明                 | 示例 |
|-------------------------------|--------|--------------------|----|
| error                         | int    | 错误码 0:正常 非0错误      | 0  |
| data                          | object | 数据                 |    |
| data.mall                     | object | 综合商城业务的数据，必返       |    |
| data.mall.viewData            | object | 访问数据               |    |
| data.mall.viewData.pv         | int    | PV                 | 0  |
| data.mall.viewData.uv         | int    | UV                 | 0  |
| data.mall.detailData          | object | 详细时间段的数据           |    |
| data.communityBuy             | array  | 社区团购业务的数据，有对应业务时返回 |    |
| data.communityBuy.viewData    | object | 访问数据               |    |
| data.communityBuy.viewData.pv | int    | PV                 | 0  |
| data.communityBuy.viewData.uv | int    | UV                 | 0  |
| data.communityBuy.detailData  | object | 详细时间段的数据           |    |
| data.siteApp                  | array  | 智慧轻站业务的数据，有对应业务时返回 |    |
| data.siteApp.viewData         | object | 访问数据               |    |
| data.siteApp.viewData.pv      | int    | PV                 | 0  |
| data.siteApp.viewData.uv      | int    | UV                 | 0  |
| data.siteApp.detailData       | object | 详细时间段的数据           |    |
| data.promoter                 | array  | 推客带货业务的数据，有对应业务时返回 |    |
| data.promoter.viewData        | object | 访问数据               |    |
| data.promoter.viewData.pv     | int    | PV                 | 0  |
| data.promoter.viewData.uv     | int    | UV                 | 0  |
| data.promoter.detailData      | object | 详细时间段的数据           |    |

### 响应示例

``` json
{
    "error": 0,
    "data": {
        "mall": {
            "viewData": {
                "pv": 0,
                "uv": 0
            },
            "detailData": {
                "00:00": {
                    "pv": 0
                },
                ...
                "23:00": {
                    "pv": 0
                }
            }
        },
        "communityBuy": {
            "viewData": {
                "pv": 0,
                "uv": 0
            },
            "detailData": {
                "00:00": {
                    "pv": 0
                },
                ...
                "23:00": {
                    "pv": 0
                }
            }
        },
        "siteApp": {
            "viewData": {
                "pv": 0,
                "uv": 0
            },
            "detailData": {
                "00:00": {
                    "pv": 0
                },
                ...
                "23:00": {
                    "pv": 0
                }
            }
        },
        "promoter": {
            "viewData": {
                "pv": 0,
                "uv": 0
            },
            "detailData": {
                "00:00": {
                    "pv": 0
                },
                ...
                "23:00": {
                    "pv": 0
                }
            }
        }
    }
}
```

## 商品销量排行榜

### 功能描述

可以获取指定时间段(今日\昨日\近7日\近30日)内不同商品销量数量、商品销售额

### 接口路由

GET /statistics/overview/goods-rank

### 请求参数说明

| 字段     | 类型     | 是否必传 | 说明                                             | 示例    |
|--------|--------|------|------------------------------------------------|-------|
| period | string | 是    | 查询区间 today:今日 yesterday:昨日 week:近7日 month:近30日 | today |

### 响应参数说明

| 字段                        | 类型     | 说明                 | 示例      |
|---------------------------|--------|--------------------|---------|
| error                     | int    | 错误码 0:正常 非0错误      | 0       |
| data                      | object | 数据                 |         |
| data.mall                 | array  | 综合商城业务的数据，必返       |         |
| data.mall[].title         | string | 商品标题               | iphone  |
| data.mall[].total         | int    | 销售数量               | 123     |
| data.mall[].price         | float  | 销售额                | 9999.19 |
| data.communityBuy         | array  | 社区团购业务的数据，有对应业务时返回 |         |
| data.communityBuy[].title | string | 商品标题               | iphone  |
| data.communityBuy[].total | int    | 销售数量               | 123     |
| data.communityBuy[].price | float  | 销售额                | 9999.19 |
| data.promoter             | array  | 推客带货业务的数据，有对应业务时返回 |         |
| data.promoter[].title     | string | 商品标题               | iphone  |
| data.promoter[].total     | int    | 带货数量               | 123     |
| data.promoter[].price     | float  | 销售额                | 9999.19 |

### 响应示例

``` json
{
    "error": 0,
    "data": {
        "mall": [
            {
                "id": "3326",
                "title": "多规格-订单核销2",
                "thumb": "image/3/2026/01/7920f2b2b820e1b71d5fabbda1ec01e0.png",
                "has_option": "1",
                "status": "1",
                "stock": "592",
                "is_deleted": "0",
                "total": "8",
                "price": "75.00"
            }
        ],
        "communityBuy": [],
        "promoter": [
            {
                "title": "（1罐体验装）15头文山三七粉250克正宗云南文山三七粉超细三七粉特级野生纯三七头",
                "thumb": "https://wst.wxapp.tc.qq.com/161/20304/snscosdownload/SZ/reserved/67d5a39b000506340066ff5ea363bc1e000000a000004f50",
                "total": "0",
                "price": 0
            }
        ]
    }
}
```

## 会员消费排行榜

### 功能描述

可以获取指定时间段(今日\昨日\近7日\近30日)内不同会员消费数据

### 接口路由

GET /statistics/overview/member-rank

### 请求参数说明

| 字段     | 类型     | 是否必传 | 说明                                             | 示例    |
|--------|--------|------|------------------------------------------------|-------|
| period | string | 是    | 查询区间 today:今日 yesterday:昨日 week:近7日 month:近30日 | today |

### 响应参数说明

| 字段                              | 类型     | 说明                 | 示例      |
|---------------------------------|--------|--------------------|---------|
| error                           | int    | 错误码 0:正常 非0错误      | 0       |
| data                            | object | 数据                 |         |
| data.mall                       | array  | 综合商城业务的数据，必返       |         |
| data.mall[].id                  | int    | 会员ID               | 1       |
| data.mall[].nickname            | string | 会员昵称               | An      |
| data.mall[].order_money         | float  | 消费金额               | 9999.19 |
| data.communityBuy               | array  | 社区团购业务的数据，有对应业务时返回 |         |
| data.communityBuy[].id          | int    | 会员ID               | 1       |
| data.communityBuy[].nickname    | string | 会员昵称               | An      |
| data.communityBuy[].order_money | float  | 消费金额               | 9999.19 |
| data.promoter                   | array  | 推客带货业务的数据，有对应业务时返回 |         |
| data.promoter[].id              | int    | 会员ID               | 1       |
| data.promoter[].nickname        | string | 会员昵称               | An      |
| data.promoter[].total           | int    | 带货订单数量             | 9999.19 |
| data.promoter[].money           | float  | 带货订单金额             | 9999.19 |

### 响应示例

``` json
{
    "error": 0,
    "data": {
        "mall": [
            {
                "id": "317",
                "nickname": "An ⁵ᴳ1",
                "avatar": "https://xxx.jpg",
                "realname": "111111",
                "mobile": "15888888888",
                "source": "40",
                "order_money": 11
            }
            ...
        ],
        "communityBuy": [
            {
                "id": "317",
                "nickname": "An ⁵ᴳ1",
                "avatar": "https://xxx.jpg",
                "realname": "111111",
                "mobile": "15888888888",
                "source": "40",
                "order_money": 11
            }
            ...
        ],
        "promoter": [
            {
                "id": "9",
                "avatar": "https://xxx.jpg",
                "nickname": "som",
                "total": "0",
                "order_money": 0
            },
            ...
        ]
    }
}
```

## 获取商品基础数据统计

### 功能描述

可以获取指定时间段内被浏览商品数量、加购商品数量、购买商品数量

### 接口路由

GET /statistics/goods/basic

### 请求参数说明

| 字段         | 类型     | 是否必传 | 说明               | 示例                  |
|------------|--------|------|------------------|---------------------|
| start_time | string | 否    | 统计开始时间，不传默认为30天前 | 2026-01-01 00:00:00 |
| end_time   | string | 否    | 统计结束时间，不传默认为前一天  | 2026-02-01 00:00:00 |

### 响应参数说明

| 字段                    | 类型     | 说明            | 示例 |
|-----------------------|--------|---------------|----|
| error                 | int    | 错误码 0:正常 非0错误 | 0  |
| data                  | object | 数据            |    |
| data.goods_view_count | int    | 被浏览商品数量(件)    | 1  |
| data.cart_goods_count | int    | 加购商品数量(件)     | 2  |
| data.pay_goods_count  | int    | 购买商品数量(件)     | 3  |

### 响应示例

``` json
{
    "error": 0,
    "data": {
        "goods_view_count": 1,
        "cart_goods_count": 2,
        "pay_goods_count": 3
    }
}
```
