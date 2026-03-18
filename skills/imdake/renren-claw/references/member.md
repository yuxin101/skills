# 会员查询管理模块

## 获取会员列表

### 功能描述

根据会员昵称、真实姓名、手机号、会员ID搜索会员信息

### 接口路由

GET /member/list/get

### 请求参数说明

| 字段        | 类型     | 是否必传 | 说明                                | 示例 |
|-----------|--------|------|-----------------------------------|----|
| keywords  | string | 否    | 搜索关键字，可搜索会员昵称、真实姓名、手机号、会员ID搜索会员信息 | An |
| page      | int    | 否    | 页码，不传缺省为1                         | 1  |
| page_size | int    | 否    | 每页数量，不传缺省为6                       | 6  |

### 响应参数说明

| 字段                   | 类型     | 说明            | 示例                  |
|----------------------|--------|---------------|---------------------|
| error                | int    | 错误码 0:正常 非0错误 | 0                   |
| total                | int    | 当前搜索条件下总数量    | 1                   |
| page                 | int    | 当前页           | 1                   |
| page_size            | int    | 每页数量          | 6                   |
| list                 | array  | 会员列表          |                     |
| list[].id            | int    | 会员ID          | 9801                |
| list[].avatar        | string | 头像地址          | https://xx.jpg      |
| list[].nickname      | string | 昵称            | An                  |
| list[].realname      | string | 真实姓名          | 李可鑫                 |
| list[].mobile        | string | 手机号           | 15888888888         |
| list[].credit        | int    | 积分            | 9981290             |
| list[].balance       | float  | 余额            | 935276.97           |
| list[].level_id      | int    | 等级ID          | 447                 |
| list[].source        | int    | 来源            | 40                  |
| list[].create_time   | string | 创建时间          | 2021-12-13 10:10:35 |
| list[].remark        | string | 备注            | 无                   |
| list[].order_count   | int    | 订单数量          | 104                 |
| list[].money_count   | float  | 订单金额          | 65030.82            |
| list[].last_pay_time | string | 最后支付时间        | 026-03-04 21:01:02  |
| list[].is_black_name | string | 是否黑名单         | 是                   |
| list[].level_name    | string | 等级名称          | 市长                  |
| list[].group_name    | string | 标签名           | 简单明了,复杂繁琐           |
| list[].source_name   | string | 来源渠道          | APP                 |

### 响应示例

``` json
{
    "error": 0,
    "total": 1,
    "list": [
        {
            "id": "317",
            "avatar": "https://thirdwx.qlogo.cn/mmopen/vi_32/LLkzWr01KUK2szdujKcslIaWJrqLd9CFSX5B9NhYCcTiagf7szd3hECNUugt29ZwXb4guOmlibkZhhr6HhnVus7Q/132",
            "nickname": "An ⁵ᴳ1",
            "realname": "李可鑫",
            "mobile": "15888888888",
            "credit": "9981290",
            "balance": "935276.97",
            "is_black": 0,
            "level_id": "447",
            "source": "40",
            "create_time": "2021-12-13 10:10:35",
            "remark": "",
            "order_count": "104",
            "money_count": "65030.82",
            "last_pay_time": "2026-03-04 21:01:02",
            "is_black_name": "否",
            "level_name": "市长",
            "group_name": "简单明了,复杂繁琐",
            "source_name": "APP"
        }
    ],
    "page": 1,
    "page_size": 20
}
```

## 获取会员详情

### 功能描述

根据会员ID获取会员详情

### 接口路由

GET /member/list/get

### 请求参数说明

| 字段 | 类型  | 是否必传 | 说明   | 示例  |
|----|-----|------|------|-----|
| id | int | 是    | 会员ID | 184 |

### 响应参数说明

| 字段             | 类型     | 说明              | 示例                  |
|----------------|--------|-----------------|---------------------|
| error          | int    | 错误码 0:正常 非0错误   | 0                   |
| member         | array  | 会员信息            |                     |
| id             | int    | 会员ID            | 9801                |
| avatar         | string | 头像地址            | https://xxx.jpg     |
| nickname       | string | 昵称              | An                  |
| realname       | string | 真实姓名            | 李可鑫                 |
| mobile         | string | 手机号             | 15888888888         |
| credit         | int    | 积分              | 9981290             |
| balance        | float  | 余额              | 935276.97           |
| level_id       | int    | 等级ID            | 447                 |
| source         | int    | 来源              | 40                  |
| last_time      | string | 最后登录时间          | 2026-03-04 21:01:02 |
| is_deleted     | int    | 是否删除 0:否 1:是    | 0                   |
| create_time    | string | 注册时间            | 2026-03-04 21:01:02 |
| is_black       | int    | 是否黑名单 0:否 1:是   | 0                   |
| remark         | string | 备注              | 无                   |
| is_bind_mobile | int    | 是否绑定手机号 0:否 1:是 | 0                   |
| birthday       | string | 生日              | 2026-03-04          |
| level_name     | string | 等级名称            | 市长                  |
| password_set   | int    | 是否设置密码 0:否 1:是  | 1                   |
| group_name     | string | 标签名             | 简单明了,复杂繁琐           |
| is_black_name  | string | 是否黑名单           | 是                   |
| member_code    | string | 会员码             | 000000000000000317  |
| source_name    | string | 来源渠道            | APP                 |

### 响应示例

``` json
{
    "error": 0,
    "member": {
        "id": "317",
        "avatar": "https://xxx.jpg",
        "nickname": "An ⁵ᴳ1",
        "realname": "李可鑫",
        "level_id": "447",
        "mobile": "15888888888",
        "credit": "9981290",
        "balance": "935276.97",
        "source": "40",
        "last_time": "2026-03-05 17:28:12",
        "is_deleted": "0",
        "create_time": "2021-12-13 10:10:35",
        "is_black": 0,
        "remark": "-",
        "is_bind_mobile": "0",
        "birthday": "0000-00-00 00:00:00",
        "level_name": "市长",
        "password_set": 1,
        "group_name": "简单明了,复杂繁琐",
        "is_black_name": "否",
        "member_code": "000000000000000317",
        "source_name": "APP"
    }
}
```

## 通过手机号获取会员ID

### 功能描述

通过手机号获取会员ID

### 接口路由

GET /member/index/get-id-by-mobile

### 请求参数说明

| 字段     | 类型     | 是否必传 | 说明  | 示例          |
|--------|--------|------|-----|-------------|
| mobile | string | 是    | 手机号 | 15888888888 |

### 响应参数说明

| 字段        | 类型  | 说明            | 示例  |
|-----------|-----|---------------|-----|
| error     | int | 错误码 0:正常 非0错误 | 0   |
| member_id | int | 会员ID          | 317 |

### 响应示例

``` json
{
    "error": 0,
    "member_id": "317"
}
```
