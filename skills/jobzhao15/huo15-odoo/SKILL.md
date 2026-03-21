---
name: huo15-odoo
description: |
  火一五欧度技能（辉火云企业套件 Odoo 接口访问指南）。提供 Odoo 系统访问的正确指导，包括项目（project.project）、
  任务（project.task）、工时（account.analytic.line）、销售（sale.order）、库存（stock.picking）等模型的正确查询方式。
  特别说明开放任务使用 active=True 过滤。
trigger:
  - patterns:
      - "odoo"
      - "辉火云"
      - "欧度"
      - "项目"
      - "任务"
      - "工时"
      - "库存"
      - "销售"
      - "project"
      - "task"
    type: fuzzy
---

# 火一五欧度技能

> 辉火云企业套件（Odoo）接口访问完整指南

> 基于 odoo-erp-connector 技能代码总结

---

## 🏢 系统信息

| 项目 | 值 |
|------|-----|
| **地址** | https://huihuoyun.huo15.com |
| **数据库** | huo15 |
| **模式** | 接口模式 |

### 账号规则

| 操作类型 | 账号 | 说明 |
|----------|------|------|
| **读取数据** | support@huo15.com | 默认使用，只读权限 |
| **写入操作** | 管理员账号 | 需授权 |

---

## 📋 Odoo 常用模型

### 项目管理

| 模型 | 说明 | 模型名 |
|------|------|--------|
| 项目 | 项目主数据 | `project.project` |
| 任务 | 项目任务 | `project.task` |
| 任务阶段 | 任务状态阶段 | `project.task.type` |
| 工时 | 时间记录 | `account.analytic.line` |

### 业务模块

| 模型 | 说明 | 模型名 |
|------|------|--------|
| 销售订单 | 销售订单 | `sale.order` |
| 发票 | 会计凭证 | `account.move` |
| 库存调拨 | 库存 | `stock.picking` |
| 联系人 | 客户/供应商 | `res.partner` |
| 产品 | 产品 | `product.product` |

---

## ⚠️ 核心查询规则

### 1. 任务查询 - 开放任务

**⚠️ 最重要规则**：搜索任务时，**必须**使用 `active=True` 过滤

```python
# ✅ 正确：只查询开放任务
domain = [["active", "=", True]]

# 查询某个项目下的开放任务
domain = [
    ("active", "=", True),
    ("project_id", "=", project_id),
]

# 查询某用户的开放任务
domain = [
    ("active", "=", True),
    ("user_ids", "in", [user_id]),
]
```

### 2. 项目查询 - 开放项目

```python
# ✅ 正确：只查询开放项目
domain = [["active", "=", True]]

# 按名称搜索项目
domain = [
    ("active", "=", True),
    ("name", "ilike", "项目名称"),
]

# 按客户搜索项目
domain = [
    ("active", "=", True),
    ("partner_id", "=", customer_id),
]
```

---

## 🔧 项目应用完整操作

### 项目（project.project）

#### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 项目ID |
| name | char | 项目名称 |
| user_id | many2one | 项目经理 |
| partner_id | many2one | 客户 |
| date_start | date | 开始日期 |
| date | date | 结束日期 |
| active | boolean | 是否启用 |
| task_count | integer | 任务数量 |
| company_id | many2one | 公司 |
| description | text | 描述 |
| allow_timesheets | boolean | 允许工时记录 |
| allow_billable | boolean | 允许计费 |
| tag_ids | many2many | 标签 |

#### 查询示例

```python
# 搜索项目
model = "project.project"
domain = [["active", "=", True]]
fields = ["id", "name", "user_id", "partner_id", "task_count", "active"]
result = client.search_read(model, domain, fields, limit=20, order="name asc")
```

---

### 任务（project.task）

#### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 任务ID |
| name | char | 任务名称 |
| project_id | many2one | 所属项目 |
| user_ids | many2many | 负责人员 |
| stage_id | many2one | 当前阶段 |
| priority | selection | 优先级 (0=普通, 1=紧急) |
| date_deadline | date | 截止日期 |
| active | boolean | 是否启用 |
| description | text | 任务描述 |
| parent_id | many2one | 父任务 |
| child_ids | one2many | 子任务 |
| date_assign | datetime | 分配时间 |
| create_date | datetime | 创建时间 |
| write_date | datetime | 更新时间 |
| partner_id | many2one | 相关联系人 |
| tag_ids | many2many | 标签 |

#### 查询示例

```python
# 搜索开放任务
model = "project.task"
domain = [["active", "=", True]]
fields = ["id", "name", "project_id", "user_ids", "stage_id", "priority", "date_deadline"]
result = client.search_read(model, domain, fields, limit=50, order="priority desc, date_deadline asc")

# 查询某项目的所有开放任务
domain = [
    ("active", "=", True),
    ("project_id", "=", project_id),
]

# 查询某用户负责的任务
domain = [
    ("active", "=", True),
    ("user_ids", "in", [user_id]),
]

# 查询某阶段的任务
domain = [
    ("active", "=", True),
    ("stage_id", "=", stage_id),
]
```

---

### 任务阶段（project.task.type）

#### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 阶段ID |
| name | char | 阶段名称 |
| sequence | integer | 排序 |
| fold | boolean | 是否折叠 |

#### 查询示例

```python
# 获取项目任务阶段
model = "project.task.type"
domain = []
fields = ["id", "name", "sequence", "fold"]
result = client.search_read(model, domain, fields, order="sequence asc")
```

---

### 工时记录（account.analytic.line）

#### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 工时ID |
| name | char | 描述 |
| project_id | many2one | 项目 |
| task_id | many2one | 任务 |
| unit_amount | float | 工时数（小时） |
| date | date | 日期 |
| user_id | many2one | 用户 |
| employee_id | many2one | 员工 |

#### 查询示例

```python
# 搜索工时记录
model = "account.analytic.line"
domain = [
    ("task_id", "=", task_id),
]
fields = ["id", "name", "unit_amount", "date", "user_id"]
result = client.search_read(model, domain, fields)
```

---

## 📊 业务模块查询

### 销售订单（sale.order）

```python
model = "sale.order"
domain = [
    ("state", "=", "sale"),  # 已确认
]
fields = ["name", "partner_id", "user_id", "amount_total", "date_order", "state"]
```

### 发票（account.move）

```python
model = "account.move"
domain = [
    ("move_type", "=", "out_invoice"),  # 销售发票
    ("state", "=", "posted"),  # 已过账
]
fields = ["name", "partner_id", "amount_total", "invoice_date", "payment_state"]
```

### 库存调拨（stock.picking）

```python
model = "stock.picking"
domain = [
    ("state", "not in", ["done", "cancel"]),
]
fields = ["name", "partner_id", "state", "scheduled_date", "picking_type_id"]
```

---

## 🎯 常用操作示例

### 创建项目

```python
values = {
    "name": "项目名称",
    "partner_id": customer_id,
    "description": "项目描述",
    "allow_timesheets": True,
}
project_id = client.create("project.project", values)
```

### 创建任务

```python
values = {
    "project_id": project_id,
    "name": "任务名称",
    "user_ids": [(6, 0, [user_id])],  # many2many 格式
    "description": "任务描述",
    "date_deadline": "2024-12-31",
    "priority": "0",  # 0=普通, 1=紧急
}
task_id = client.create("project.task", values)
```

### 分配任务

```python
client.write("project.task", task_id, {
    "user_ids": [(6, 0, [user_id1, user_id2])],
})
```

### 更改任务阶段

```python
client.write("project.task", task_id, {
    "stage_id": stage_id,
})
```

### 记录工时

```python
values = {
    "project_id": project_id,
    "task_id": task_id,
    "unit_amount": 3.0,  # 3小时
    "name": "工作描述",
    "date": "2024-03-19",
}
timesheet_id = client.create("account.analytic.line", values)
```

---

## ⚠️ 注意事项

1. **active 字段**：查询项目或任务时，**必须**使用 `active=True` 过滤，只返回开放的任务
2. **只读原则**：默认使用 support@huo15.com 进行读取操作
3. **多公司确认**：如果系统有多家公司，先确认使用哪个公司
4. **日期范围**：查询数据时先确认日期范围
5. **many2many 格式**：写入 user_ids 时使用 `[(6, 0, [ids])]` 格式

---

## 📁 Documents 文档应用操作

### 文档模型

| 模型 | 说明 | 模型名 |
|------|------|--------|
| 文档 | 文档主数据 | `documents.document` |
| 文件夹 | 文档分类 | `documents.folder` |
| 访问权限 | 文档成员权限 | `documents.access` |

### 文档字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 文档ID |
| name | char | 文档名称 |
| datas | binary | 文件内容(base64) |
| mimetype | char | 文件类型 |
| folder_id | many2one | 所属文件夹 |
| create_uid | many2one | 创建人 |
| owner_id | many2one | 所有者 |
| partner_id | many2one | 关联联系人 |
| access_token | char | 访问令牌 |
| access_url | char | 访问URL |
| access_via_link | selection | **链接访问权限** |
| access_internal | selection | **内部成员权限** |

### 文档权限字段说明

| 字段 | 说明 | 可用值 |
|------|------|--------|
| `access_via_link` | 链接访问权限（通过分享链接访问） | `view`(查看)、`edit`(编辑)、`none`(无权限) |
| `access_internal` | 内部成员权限（公司内部成员访问） | `view`(查看)、`edit`(编辑)、`none`(无权限) |

### 查询文档示例

```python
# 获取所有文档
model = "documents.document"
domain = []
fields = ["id", "name", "create_date", "mimetype", "access_token"]
result = client.search_read(model, domain, fields, limit=50)

# 搜索文档
model = "documents.document"
domain = [
    ("name", "ilike", "文档名称"),
]

# 获取文档详情
model = "documents.document"
result = client.read(doc_id, ["name", "datas", "access_token", "access_via_link", "access_internal"])
```

### 创建文档

```python
# 上传文档
import base64

model = "documents.document"
values = {
    "name": "文档名称.docx",
    "folder_id": folder_id,  # 文件夹ID
    "datas": base64.b64encode(file_content).decode('utf-8'),
    "mimetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
doc_id = client.create(model, values)
```

### 📤 文档分享链接

#### 分享链接机制

**关键发现**：Odoo 的 Documents 模块在上传时会自动生成 `access_token`，分享链接格式为：

```
https://huihuoyun.huo15.com/odoo/documents/{access_token}
```

#### 创建/设置分享链接

```python
# 只需要写入 access_via_link 字段即可启用分享
model = "documents.document"
client.write(doc_id, {
    "access_via_link": "edit"  # 启用链接访问，可编辑
})
```

#### 分享权限设置

| 值 | 说明 |
|---|------|
| `view` | 链接访问：仅查看 |
| `edit` | 链接访问：可编辑 |
| `none` | 关闭链接访问 |

```python
# 示例：设置文档为链接可编辑
model = "documents.document"
client.write(doc_id, {
    "access_via_link": "edit"
})

# 示例：设置文档为链接仅查看
client.write(doc_id, {
    "access_via_link": "view"
})

# 示例：关闭文档分享
client.write(doc_id, {
    "access_via_link": "none"
})
```

### 👥 内部成员权限设置

#### 权限字段

| 字段 | 说明 |
|------|------|
| `access_internal` | 内部成员权限 |

| 值 | 说明 |
|---|------|
| `view` | 内部成员：仅查看 |
| `edit` | 内部成员：可编辑 |
| `none` | 内部成员：无权限 |

#### 设置内部权限

```python
# 设置内部成员权限为可编辑
model = "documents.document"
client.write(doc_id, {
    "access_internal": "edit"
})

# 设置内部成员权限为仅查看
client.write(doc_id, {
    "access_internal": "view"
})

# 设置内部成员无权限
client.write(doc_id, {
    "access_internal": "none"
})
```

### 📋 完整权限组合示例

```python
# 同时设置内部和链接权限
model = "documents.document"
values = {
    "access_internal": "edit",  # 内部成员：可编辑
    "access_via_link": "view"   # 链接访问：仅查看
}
client.write(doc_id, values)

# 权限组合参考
combinations = [
    {"access_internal": "edit", "access_via_link": "edit", "desc": "完全公开编辑"},
    {"access_internal": "view", "access_via_link": "view", "desc": "公开仅查看"},
    {"access_internal": "edit", "access_via_link": "view", "desc": "内部可编辑，链接仅查看"},
    {"access_internal": "none", "access_via_link": "none", "desc": "完全私有"},
]
```

### 📄 获取文档分享链接

```python
# 读取文档的分享信息
model = "documents.document"
result = client.read(doc_id, ["name", "access_token", "access_url", "access_via_link"])

# 生成分享链接
access_token = result["access_token"]
share_url = f"https://huihuoyun.huo15.com/odoo/documents/{access_token}"
```

---

## 📁 文件夹操作

### 查询文件夹

```python
# 获取所有文件夹
model = "documents.folder"
domain = []
fields = ["id", "name", "owner_ids"]
result = client.search_read(model, domain, fields)

# 按名称搜索
model = "documents.folder"
domain = [("name", "ilike", "文件夹名称")]
```

### 创建文件夹

```python
# 创建文件夹
model = "documents.folder"
values = {
    "name": "文件夹名称",
    "owner_ids": [(6, 0, [user_id])],  # 所有者
}
folder_id = client.create(model, values)
```

---

## 🎯 Documents 完整操作示例

### 上传文档并设置分享

```python
import base64
from odoorpc import ODOO

# 连接系统
odoo = ODOO('https://huihuoyun.huo15.com', timeout=60)
odoo.login('huo15', 'admin@huo15.com', 'password')

# 1. 上传文档
doc_id = odoo.execute(
    'documents.document',
    'create',
    {
        'name': '报告.docx',
        'datas': base64.b64encode(file_content).decode('utf-8'),
        'mimetype': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    }
)

# 2. 设置分享权限（链接可编辑，内部可查看）
odoo.execute(
    'documents.document',
    'write',
    doc_id,
    {
        'access_via_link': 'edit',    # 链接可编辑
        'access_internal': 'view',     # 内部仅查看
    }
)

# 3. 获取分享链接
doc = odoo.execute('documents.document', 'read', doc_id, ['access_token'])
share_url = f"https://huihuoyun.huo15.com/odoo/documents/{doc['access_token']}"
print(f"分享链接: {share_url}")
```

---

## 🔗 相关技能

- **odoo-reporting**：财务报表查询
- **odoo-erp-connector**：ERP 连接器
- **huo15-doc-template**：文档生成
