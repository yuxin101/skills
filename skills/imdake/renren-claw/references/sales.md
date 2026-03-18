# 营销活动查询管理模块

## 获取优惠券概览

### 功能描述

获取优惠券发放中数量(张)、已过期数量(张)、已领完数量(张)、已使用数量(张)、已领取数量(张)

### 接口路由

GET /sales/coupon/overview

### 请求参数说明

无

### 响应参数说明

| 字段                | 类型     | 说明            | 示例    |
|-------------------|--------|---------------|-------|
| error             | int    | 错误码 0:正常 非0错误 | 0     |
| data              | object | 数据            |       |
| data.sending      | int    | 发放中优惠券数量      | 29    |
| data.expired      | int    | 已过期优惠券数量      | 66    |
| data.out_of_stock | int    | 已领完优惠券数量      | 6     |
| data.used         | int    | 已使用优惠券数量      | 523   |
| data.received     | int    | 已领取优惠券数量      | 18417 |

### 响应示例

``` json
{
    "error": 0,
    "data": {
        "sending": 29,
        "expired": 66,
        "out_of_stock": 6,
        "used": 523,
        "received": 18417
    }
}

```

## 获取优惠券列表

### 功能描述

根据优惠券名称、状态、领取方式搜索优惠券信息

### 接口路由

GET /sales/coupon/list

### 请求参数说明

| 字段               | 类型     | 是否必传 | 说明                                               | 示例 |
|------------------|--------|------|--------------------------------------------------|----|
| keywords         | string | 否    | 搜索关键字，搜索优惠券名称                                    | 0  |
| coupon_sale_type | int    | 否    | 优惠券优惠类型 1:立减 2:折扣，不传为全部                          | 1  |
| status           | int    | 否    | 优惠券状态 1:发放中 2:未发放 3:已领完 4:已过期，不传为全部              | 1  |
| pick_way         | int    | 否    | 领取方式 1:免费领取 2:付费领取 3:通过链接领取 4:活动领取 5:领券中心 6:直播领取 | 1  |
| page             | int    | 否    | 页码，不传缺省为1                                        | 1  |
| page_size        | int    | 否    | 每页数量，不传缺省为6                                      | 6  |

### 响应参数说明

| 字段                   | 类型     | 说明            | 示例                  |
|----------------------|--------|---------------|---------------------|
| error                | int    | 错误码 0:正常 非0错误 | 0                   |
| total                | int    | 当前搜索条件下总数量    | 1                   |
| page                 | int    | 当前页           | 1                   |
| page_size            | int    | 每页数量          | 6                   |
| list                 | array  | 优惠券列表         |                     |
| list[].id            | int    | 优惠券ID         | 9801                |
| list[].coupon_name   | string | 优惠券名称         | 满1减0.1              |
| list[].stock         | int    | 优惠券库存         | 120                 |
| list[].create_time   | string | 添加时间          | 2025-11-25 15:24:33 |
| list[].content       | string | 优惠内容          | 满1减0.1              |
| list[].pick_way_text | string | 领取类型文字        | 付费领取                |
| list[].status_text   | string | 状态文字          | 已过期                 |

### 响应示例

``` json
{
    "error": 0,
    "total": 1,
    "list": [
        {
            "id": "218",
            "coupon_name": "计次时",
            "coupon_sale_type": "1",
            "stock": "0",
            "stock_type": "0",
            "get_total": "1111",
            "create_time": "2025-11-25 15:24:33",
            "use_num": "0.0216",
            "content": "满1减0.1",
            "pick_way": 2,
            "pick_way_text": "付费领取",
            "status": "4",
            "status_text": "已过期"
        }
    ],
    "page": 1,
    "page_size": 20
}

```

## 手动停止发放优惠券

### 功能描述

根据优惠券ID停止发放指定的优惠券

### 接口路由

POST /sales/coupon/manual-stop

### 请求参数说明

| 字段 | 类型  | 是否必传 | 说明    | 示例  |
|----|-----|------|-------|-----|
| id | int | 是    | 优惠券ID | 184 |

### 响应参数说明

| 字段      | 类型     | 说明              | 示例     |
|---------|--------|-----------------|--------|
| error   | int    | 错误码 0:正常 非0错误   | 0      |
| message | string | 错误信息 error非0时返回 | 优惠券不存在 |

### 响应示例

``` json
{
    "error": 0
}
```

## 获取满额包邮设置

### 功能描述

获取满额包邮设置

### 接口路由

GET /sales/full-free/get

### 请求参数说明

无

### 响应参数说明

| 字段                      | 类型     | 说明                             | 示例       |
|-------------------------|--------|--------------------------------|----------|
| error                   | int    | 错误码 0:正常 非0错误                  | 0        |
| settings                | object | 设置项                            |          |
| settings.state          | int    | 开启状态 0:关闭 1:开启                 | 1        |
| settings.is_participate | string | 指定商品 0:以下商品不参与 1: 以下商品参与 2:不限制 | 1        |
| settings.goods_ids      | array  | 指定商品的ID合集                      | ["9801"] |
| settings.order_enough   | string | 单笔订单包邮金额                       | 2000     |
| goods_list              | array  | 指定商品的列表                        |          |
| goods_list[].id         | int    | 商品ID                           | 9801     |
| goods_list[].title      | string | 商品标题                           | iphone   |
| goods_list[].price      | float  | 商品价格                           | 120.00   |
| no_support_areas        | string | 不参加包邮地区，为空则不限制                 | 北京市      |

### 响应示例

``` json
{
    "error": 0,
    "settings": {
        "state": 0,
        "is_participate": "0",
        "goods_ids": [
            "9801"
        ],
        "order_enough": "3000.00"
    },
    "goods_list": [
        {
            "id": "9801",
            "thumb": "image/25/2025/07/5653ba2ab5df7e5d6386f27acc6be96b.jpg",
            "title": "xzj多规格",
            "price": "120.00",
            "type": "0",
            "has_option": "1"
        }
    ],
    "no_support_areas": "北京市，山东省【青岛市(黄岛区)】"
}

```

## 关闭满额包邮设置

### 功能描述

关闭满额包邮设置

### 接口路由

POST /sales/full-free/close

### 请求参数说明

无

### 响应参数说明

| 字段      | 类型     | 说明              | 示例        |
|---------|--------|-----------------|-----------|
| error   | int    | 错误码 0:正常 非0错误   | 0         |
| message | string | 错误信息 error非0时返回 | 当前已经是关闭状态 |

### 响应参数说明

### 响应示例

``` json
{
    "error": 0
}
```
