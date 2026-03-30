# Knowledge Base

前置：根SKILL.md凭证、`ima_api`函数。API路径: `openapi/wiki/v1`

支持：上传文件、添加网页、搜索知识库、管理知识库。

## 接口决策

| 意图 | 接口 |
|------|------|
| 上传文件 | `check_repeated_names` → `create_media` → COS上传 → `add_knowledge` |
| 添加网页/微信文章 | `import_urls` |
| 将笔记关联到知识库 | `add_knowledge` (media_type=11) |
| 检查文件名重复 | `check_repeated_names` |
| 获取知识库信息 | `get_knowledge_base` |
| 浏览知识库内容 | `get_knowledge_list` |
| 在知识库中搜索 | `search_knowledge` |
| 搜索知识库 | `search_knowledge_base` (空query=返回所有) |
| 添加但未指定知识库 | `get_addable_knowledge_base_list` |

### search_knowledge_base vs get_addable_knowledge_base_list

| 场景 | 接口 |
|------|------|
| 用户说了知识库名称 | `search_knowledge_base` |
| 查看自己有哪些知识库 | `search_knowledge_base` (query="") |
| 要添加但没说哪个知识库 | `get_addable_knowledge_base_list` |

## 前置检查（必须）

### 1. 类型支持

| 检查项 | 条件 | 处理 |
|--------|------|------|
| 扩展名 | 不在支持列表 | 告知不支持 |
| 视频文件 | .mp4/.avi/.mov等 | 告知仅桌面端支持 |
| 视频URL | bilibili.com/video/、youtube.com | 告知仅桌面端支持 |
| 本地HTML | file:// | 告知仅桌面端支持 |

### 2. 文件大小

| 类型 | media_type | 限制 |
|------|-----------|------|
| Excel/TXT/Xmind/MD | 5/13/14/7 | 10MB |
| 图片 | 9 | 30MB |
| PDF/Word/PPT/音频 | 1/3/4/15等 | 200MB |

### 3. 重名检查（仅文件类型）

`is_repeated=true`时询问用户处理方式。

## 文件检测脚本

```bash
node scripts/preflight-check.cjs --file "/path/file.pdf"
# 输出JSON: pass=true(含file_name/size/media_type/content_type) 或 pass=false(含reason)
```

### 扩展名映射

| 扩展名 | media_type | content_type |
|--------|-----------|--------------|
| .pdf | 1 | application/pdf |
| .doc/.docx | 3 | application/msword |
| .ppt/.pptx | 4 | application/vnd.ms-powerpoint |
| .xls/.xlsx/.csv | 5 | application/vnd.ms-excel |
| .md | 7 | text/markdown |
| .png/.jpg/.webp | 9 | image/png/jpeg/webp |
| .txt | 13 | text/plain |
| .xmind | 14 | application/x-xmind |
| .mp3/.m4a/.wav/.aac | 15 | audio/mpeg等 |

## 上传文件流程

```
1. 前置检查 → preflight-check.cjs
2. 重名检查 → check_repeated_names（如需要）
3. 创建媒体 → create_media → 获取media_id和COS凭证
4. 上传COS → cos-upload.cjs
5. 添加知识 → add_knowledge
```

## 添加网页

```bash
# 根目录（省略folder_id）
ima_api "openapi/wiki/v1/import_urls" '{"knowledge_base_id":"<id>","urls":["url"]}'

# 指定文件夹(folder_id以folder_开头)
ima_api "openapi/wiki/v1/import_urls" '{"knowledge_base_id":"<id>","folder_id":"<fid>","urls":["url"]}'

# 返回: results{url: {ret_code, media_id}}，ret_code=0成功
```

## 添加笔记到知识库

```bash
ima_api "openapi/wiki/v1/add_knowledge" '{"media_type":11,"note_info":{"content_id":"<doc_id>"},"title":"标题","knowledge_base_id":"<id>"}'
```

## URL类型检测

用户提供URL时判断类型：

1. **URL含文件扩展名**（.pdf/.docx）→ 文件型，下载后走上传流程
2. **HEAD请求**检查Content-Type：
   - `text/html` → 检查微信/普通网页
   - `application/pdf`等 → 文件型
3. **已知模式**：arxiv.org/pdf/* → PDF

### html页面判断

| URL模式 | 类型 | 处理 |
|---------|------|------|
| mp.weixin.qq.com/s/ | 微信公众号 | `import_urls` |
| bilibili.com/video/ | 视频 | 不支持 |
| youtube.com/watch | 视频 | 不支持 |
| file:// | 本地HTML | 不支持 |
| 其他 | 普通网页 | `import_urls` |

## 文件夹操作

定位文件夹（用户只给名称时）：
```bash
# 搜索（推荐）
ima_api "openapi/wiki/v1/search_knowledge" '{"query":"文件夹名","knowledge_base_id":"<id>","cursor":""}'
# 从results取media_id作为folder_id（以folder_开头）

# 或浏览列表逐级查找
ima_api "openapi/wiki/v1/get_knowledge_list" '{"knowledge_base_id":"<id>","cursor":"","limit":50}'
```

规则：
- 根目录时：**省略folder_id字段**
- folder_id以`folder_`开头
- 不要将knowledge_base_id作为folder_id传入

## 核心响应字段

| 结构 | 关键字段 |
|------|----------|
| KnowledgeInfo | media_id、title、parent_folder_id |
| SearchedKnowledgeInfo | media_id、title、highlight_content |
| KnowledgeBaseInfo | id、name、description |
| FolderInfo | folder_id、name、file_number |

## 展示格式

```
📚 知识库列表（共3个）：
1. 产品文档库 — 存放产品文档
2. 技术方案库
---
📂 产品文档库：
📁 设计文档/  (3个文件)
📄 产品需求.pdf
---
🔍 搜索「排期」：
1. 📄 Q1排期表.xlsx
   > ...包含**排期**计划...
```

## 用户体验

- **隐藏内部ID**：展示时用名称
- **精简进度**：只报告结果
  - ✅ "已添加到「产品文档库」✓"
  - ❌ "正在创建媒体…正在上传…"
- **批量汇总**："3个已添加，1个失败（data.xlsx: 大小超限）"
