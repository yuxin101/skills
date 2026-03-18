# 商品查询管理模块

## 获取商品列表

### 功能描述

根据商品标题、商品编码、商品条码搜索商品信息

### 接口路由

GET /goods/list/get

### 请求参数说明

| 字段        | 类型     | 是否必传 | 说明                                                                                      | 示例          |
|-----------|--------|------|-----------------------------------------------------------------------------------------|-------------|
| keywords  | string | 否    | 搜索关键字，可搜索商品标题、商品编码、商品条码                                                                 | iPhone      |
| type      | int    | 否    | 商品类型 0:实体商品 1:虚拟商品 2:虚拟卡密 3:预约到店 5:计次时商品 8:批发商品 9:智慧药房 13:海淘商品 20:社区团购 21:期刊商品 22:供应链商品 | 0           |
| status    | int    | 否    | 商品状态 空:上架下架和售罄 1: 上架销售 2:售罄 3:下架 4:已删除                                                  | 1           |
| sort      | string | 否    | 排序字段 real_sales:真实销量 create_time:创建时间                                                   | create_time |
| by        | string | 否    | 排序方式 asc:升序 desc:降序                                                                     | desc        |
| page      | int    | 否    | 页码，不传缺省为1                                                                               | 1           |
| page_size | int    | 否    | 每页数量，不传缺省为6                                                                             | 6           |

### 响应参数说明

| 字段                    | 类型     | 说明              | 示例                |
|-----------------------|--------|-----------------|-------------------|
| error                 | int    | 错误码 0:正常 非0错误   | 0                 |
| total                 | int    | 当前搜索条件下总数量      | 1                 |
| page                  | int    | 当前页             | 1                 |
| page_size             | int    | 每页数量            | 6                 |
| list                  | array  | 商品列表            |                   |
| list[].id             | int    | 商品ID            | 9801              |
| list[].title          | string | 商品标题            | iPhone 17 Pro Max |
| list[].sub_title      | string | 商品副标题           | 新品上线              |
| list[].unit           | string | 单位              | 件                 |
| list[].goods_code     | string | 编码              | SJ0001            |
| list[].bar_code       | string | 条码              | 690100102121      |
| list[].stock          | int    | 库存              | 120               |
| list[].real_sales     | int    | 真实销量            | 99                |
| list[].price          | float  | 商品价格            | 8999.00           |
| list[].min_price      | float  | 多规格区间价最低价       | 8999.00           |
| list[].max_price      | float  | 多规格区间价最高价       | 8999.00           |
| list[].cost_price     | float  | 成本价             | 7000              |
| list[].original_price | float  | 划线价             | 12000.00          |
| list[].has_option     | int    | 是否多规格商品 0:否 1:是 | 0                 |
| list[].type_text      | string | 商品类型文字          | 实体商品              |
| list[].status_text    | string | 商品状态文字          | 上架                |

### 响应示例

``` json
{
    "error": 0,
    "total": 1307,
    "list": [
        {
            "id": "9842",
            "title": "按订单-一次性核销完成",
            "sub_title": "",
            "type": "5",
            "thumb": "image/25/2025/11/8500f5ed069c49cfc194f2dc03efe7cb.jpg",
            "unit": "件",
            "goods_code": "",
            "bar_code": "",
            "stock": "3316",
            "stock_warning": "20",
            "real_sales": "16",
            "price": "10.00",
            "min_price": "10.00",
            "max_price": "12.00",
            "cost_price": "0.00",
            "original_price": "0.00",
            "has_option": "1",
            "status": "1",
            "sales": "16",
            "type_text": "计次时商品",
            "status_text": "上架"
        },
        ...
    ],
    "page": 1,
    "page_size": 6
}
```

## 获取商品详情

### 功能描述

根据商品ID获取商品详情

### 接口路由

GET /goods/detail/get

### 请求参数说明

| 字段 | 类型  | 是否必传 | 说明   | 示例  |
|----|-----|------|------|-----|
| id | int | 是    | 商品ID | 184 |

### 响应参数说明

### 响应示例

| 字段                   | 类型     | 说明              | 示例                |
|----------------------|--------|-----------------|-------------------|
| error                | int    | 错误码 0:正常 非0错误   | 0                 |
| goods                | object | 商品数据            |                   |
| goods.id             | int    | 商品ID            | 9801              |
| goods.title          | string | 商品标题            | iPhone 17 Pro Max |
| goods.sub_title      | string | 商品副标题           | 新品上线              |
| goods.unit           | string | 单位              | 件                 |
| goods.goods_code     | string | 编码              | SJ0001            |
| goods.bar_code       | string | 条码              | 690100102121      |
| goods.stock          | int    | 库存              | 120               |
| goods.real_sales     | int    | 真实销量            | 99                |
| goods.price          | float  | 商品价格            | 8999.00           |
| goods.min_price      | float  | 多规格区间价最低价       | 8999.00           |
| goods.max_price      | float  | 多规格区间价最高价       | 8999.00           |
| goods.cost_price     | float  | 成本价             | 7000              |
| goods.original_price | float  | 划线价             | 12000.00          |
| goods.has_option     | int    | 是否多规格商品 0:否 1:是 | 0                 |
| goods.type_text      | string | 商品类型文字          | 实体商品              |
| goods.status_text    | string | 商品状态文字          | 上架                |

``` json
{
    "error": 0,
    "goods": {
        "id": "9842",
        "type": "5",
        "status": "1",
        "is_deleted": "0",
        "title": "按订单-一次性核销完成",
        "sub_title": "",
        "price": "10.00",
        "max_price": "12.00",
        "min_price": "10.00",
        "original_price": "0.00",
        "stock": "3316",
        "display_order": "9999",
        "has_option": "1",
        "view_count": "27",
        "sales": "0",
        "thumb": "https://likexin-shop.v5dev.getpkg.cn/data/attachment/image/25/2025/11/8500f5ed069c49cfc194f2dc03efe7cb.jpg",
        "goods_unit": "袋",
        "status_text": "上架",
        "type_text": "计次时商品"
    }
}
```

## 下架商品

### 功能描述

通过商品ID进行下架操作

### 接口路由

POST /goods/operation/put-store

### 请求参数说明

| 字段 | 类型  | 是否必传 | 说明   | 示例  |
|----|-----|------|------|-----|
| id | int | 是    | 商品ID | 184 |

### 响应参数说明

| 字段      | 类型     | 说明              | 示例    |
|---------|--------|-----------------|-------|
| error   | int    | 错误码 0:正常 非0错误   | 0     |
| message | string | 错误信息 error非0时返回 | 商品不存在 |

### 响应示例

``` json
{
    "error": 0
}
```
