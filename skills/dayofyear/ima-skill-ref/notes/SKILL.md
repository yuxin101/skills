# Notes

前置：根SKILL.md凭证、`ima_api`函数。API路径: `openapi/note/v1`

支持：搜索笔记、浏览笔记本、读取正文、新建笔记、追加内容。

> 群聊中只展示标题和摘要，禁止展示正文。

## 接口决策

| 意图 | 接口 | 关键参数 |
|------|------|----------|
| 搜索笔记（标题） | `search_note_book` | search_type=0、query_info.title |
| 搜索笔记（正文） | `search_note_book` | search_type=1、query_info.content |
| 列出笔记本 | `list_note_folder_by_cursor` | cursor="0"、limit |
| 浏览笔记本里的笔记 | `list_note_by_folder_id` | folder_id（空=全部笔记）、cursor="" |
| 读取正文 | `get_doc_content` | doc_id、target_content_format（推荐0） |
| 新建笔记 | `import_doc` | content_format=1、content |
| 追加到已有笔记 | `append_doc` | doc_id、content_format=1、content |

## 新建 vs 追加

### 直接新建
"**新建**笔记"、"**创建**笔记"、"**写一篇**笔记" → `import_doc`

### 直接追加
"**追加到**《XX》"、"在那篇笔记**末尾加上**" → `append_doc`

### 必须先询问
意图不明确时，**必须先确认**：
- "帮我记一下"、"保存为笔记"
- "添加到笔记里"

询问示例："您是想**创建新笔记**还是**追加到已有笔记**？"

## 追加是敏感操作

追加会**不可撤销修改**用户笔记：

| 情况 | 处理 |
|------|------|
| 用户明确指定目标笔记 | 直接追加 |
| 用户未明确指定 | 必须先询问确认 |

## 常用流程

### 搜索并读取
```bash
# 搜索（⚠️query_info.title不能为空，否则报错）
ima_api "openapi/note/v1/search_note_book" '{"search_type":0,"query_info":{"title":"关键词"},"start":0,"end":20}'
# 从 docs[].doc.basic_info.docid 取ID

# 读取（纯文本）
ima_api "openapi/note/v1/get_doc_content" '{"doc_id":"<id>","target_content_format":0}'
```

### 浏览笔记本
```bash
# 列出笔记本
ima_api "openapi/note/v1/list_note_folder_by_cursor" '{"cursor":"0","limit":20}'

# 浏览某笔记本（空folder_id=全部笔记）
ima_api "openapi/note/v1/list_note_by_folder_id" '{"folder_id":"","cursor":"","limit":20}'
```

### 新建笔记
```bash
ima_api "openapi/note/v1/import_doc" '{"content_format":1,"content":"# 标题\n\n正文"}'
# 返回 doc_id
```

### 追加内容
```bash
ima_api "openapi/note/v1/append_doc" '{"doc_id":"<id>","content_format":1,"content":"\n## 补充\n\n内容"}'
```

## 核心响应字段

| 结构 | 路径 | 关键字段 |
|------|------|----------|
| 搜索结果 | docs[].doc.basic_info | docid、title、summary、folder_id |
| 笔记本 | note_book_folders[].folder.basic_info | folder_id、name、folder_type |
| 笔记列表 | note_book_list[].basic_info.basic_info | docid、title、summary |

时间字段为Unix毫秒，展示时转可读格式。

## 枚举值

| 枚举 | 值 | 说明 |
|------|-----|------|
| content_format | 0 | 纯文本 |
| content_format | 1 | Markdown（写入必须用1） |
| search_type | 0 | 按标题（默认） |
| search_type | 1 | 按正文 |
| folder_type | 0 | 用户自建 |
| folder_type | 1 | 全部笔记（根目录） |
| folder_type | 2 | 未分类 |

## 注意事项

- `folder_id`不可为"0"。根目录ID格式`user_list_{userid}`，从folder_type=1获取
- 笔记有大小上限，超限返回100009，拆分多次`append_doc`
- **本地图片不支持**：过滤`![](file:///...)`等路径，告知用户
