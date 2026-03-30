---
name: ima-skill
description: |
  统一IMA OpenAPI技能，支持笔记管理和知识库操作。
  触发：知识库、资料库、笔记、上传文件、添加网页、搜索内容。
homepage: https://ima.qq.com
metadata:
  openclaw:
    emoji: '🔧'
    requires: { env: ['IMA_OPENAPI_CLIENTID', 'IMA_OPENAPI_APIKEY'] }
    primaryEnv: 'IMA_OPENAPI_CLIENTID'
  security:
    credentials_usage: 凭证仅发往ima.qq.com
    allowed_domains: [ima.qq.com]
---

# ima-skill

支持**笔记**和**知识库**两大模块。

## ⚠️ 开始前：检测环境

**先执行环境检测，确定调用方式：**

```bash
# 检测shell环境
echo $SHELL | grep -q bash && echo "Bash/Linux" || echo "Other"
command -v python3 >/dev/null 2>&1 && echo "Python: $(python3 --version)" || echo "No Python"
command -v node >/dev/null 2>&1 && echo "Node: $(node --version)" || echo "No Node"
```

### 环境对应调用方式

| 环境 | HTTP调用 | 文件处理 |
|------|----------|----------|
| **Bash + curl** | `curl -X POST https://ima.qq.com/...` | Python/Node脚本 |
| **Python** | `requests.post()` 或 `subprocess.run(['curl',...])` | Python直接处理 |
| **PowerShell** | `Invoke-RestMethod` | 需UTF-8字节处理 |
| **Node.js** | `fetch()` 或 `axios` | Node直接处理 |

### 各环境API调用模板

**Bash：**
```bash
curl -s -X POST "https://ima.qq.com/$path" \
  -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
  -H "ima-openapi-apikey: $IMA_API_KEY" \
  -H "Content-Type: application/json" -d "$body"
```

**Python：**
```python
import requests, os
resp = requests.post(f"https://ima.qq.com/{path}",
    headers={"ima-openapi-clientid": os.environ.get("IMA_OPENAPI_CLIENTID",""),
             "ima-openapi-apikey": os.environ.get("IMA_OPENAPI_APIKEY","")},
    json=body)
```

**PowerShell：**
```powershell
# 必须在发送前检测版本并处理UTF-8
$script:ima_utf8 = $PSVersionTable.PSVersion.Major -le 5
$body = @{...} | ConvertTo-Json -Depth 10
if ($ima_utf8) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    Invoke-RestMethod -Uri $u -Method Post -Body $bytes -ContentType "application/json; charset=utf-8" -Headers $h
} else { Invoke-RestMethod -Uri $u -Method Post -Body $body -ContentType "application/json; charset=utf-8" -Headers $h }
```

**Node.js：**
```javascript
const resp = await fetch(`https://ima.qq.com/${path}`, {
  method: 'POST',
  headers: {'ima-openapi-clientid': clientId, 'ima-openapi-apikey': apiKey},
  body: JSON.stringify(body)
});
```

## 凭证

**获取**：https://ima.qq.com/agent-interface 获取 Client ID 和 API Key

**配置（二选一）：**
```bash
# 配置文件（推荐）
mkdir -p ~/.config/ima
echo "id" > ~/.config/ima/client_id
echo "key" > ~/.config/ima/api_key

# 环境变量
export IMA_OPENAPI_CLIENTID="id"
export IMA_OPENAPI_APIKEY="key"
```

**加载函数（Bash）：**
```bash
ima_load_creds() {
  IMA_CLIENT_ID="${IMA_OPENAPI_CLIENTID:-$(cat ~/.config/ima/client_id 2>/dev/null)}"
  IMA_API_KEY="${IMA_OPENAPI_APIKEY:-$(cat ~/.config/ima/api_key 2>/dev/null)}"
  if [ -z "$IMA_CLIENT_ID" ] || [ -z "$IMA_API_KEY" ]; then
    echo "缺少IMA凭证，请先配置"; exit 1
  fi
}
```

## 实测经验

### search_note_book空标题会报错
`query_info.title`为空字符串时会返回错误`ListNoteBook param is error`。必须传入有效搜索词。

### import_urls根目录处理
`folder_id`省略=根目录，**不要传knowledge_base_id**作为folder_id。

### 笔记搜索必须带关键词
搜索笔记时`query_info`至少要有一个非空字段（title或content）。

### PowerShell显示乱码
PowerShell 5.1控制台用GBK编码显示UTF-8数据时会出现中文乱码，这是**显示问题**，不是实际数据编码问题。其他环境（bash/Python/Node）处理时中文正常。

## 模块路由

| 用户意图 | 模块 | 文档 |
|----------|------|------|
| 搜索/浏览/创建/编辑笔记、追加到笔记 | notes | `notes/SKILL.md` |
| 上传文件、添加网页、搜索/管理知识库 | knowledge-base | `knowledge-base/SKILL.md` |

### 意图判断

- **操作笔记内容** → notes
- **操作知识库条目** → knowledge-base
- 说"知识库里那篇笔记"但要操作笔记内容 → notes

### 易混淆场景

| 用户说的 | 实际意图 | 路由 |
|----------|----------|------|
| "添加到知识库XX的笔记YY" | 追加到笔记 | notes → `append_doc` |
| "写到XX笔记里" | 追加到笔记 | notes → `append_doc` |
| "把这篇笔记添加到知识库" | 关联笔记到知识库 | kb → `add_knowledge`(media_type=11) |
| "上传文件到知识库" | 上传文件 | kb → `create_media` → COS → `add_knowledge` |
| "新建一篇笔记" | 创建新笔记 | notes → `import_doc` |
| "帮我记一下" | 需确认 | notes → 先询问 |
| "从知识库搜内容记到笔记" | 多模块 | 先kb搜索，再notes创建 |

## 共享常量

### 错误码

**通用：**
| 码 | 含义 | 处理 |
|----|------|------|
| 0 | 成功 | — |
| 110001 | 参数非法 | 检查参数 |
| 110010 | 网络错误 | 可重试 |
| 110011 | 逻辑错误 | 不可重试 |
| 110021 | 频控 | 降低频率 |
| 110030 | 无权限 | 确认权限 |

**笔记专用：**
| 码 | 含义 | 处理 |
|----|------|------|
| 100001 | 参数错误 | 检查格式 |
| 100005 | 无权限 | 确认是用户自己的笔记 |
| 100006 | 笔记已删除 | 不存在 |
| 100009 | 超过大小限制 | 拆分append_doc |
| 20004 | apikey鉴权失败 | 检查凭证 |

> ⚠️ 实际响应字段为 `code`/`msg`，不是 `retcode`/`errmsg`

### 响应格式

```json
{ "code": 0, "msg": "...", "data": {...} }
```
- code=0：成功，从data提取字段
- code≠0：失败，直接展示msg

### 游标分页

适用于：get_knowledge_list、search_knowledge、search_knowledge_base、list_note_folder_by_cursor、list_note_by_folder_id

1. 首次：`cursor: ""`
2. 检查 `is_end`：`false`=还有更多
3. 用 `next_cursor` 继续
4. `is_end=true` 停止

## 编码规范

> 仅notes模块文本写入需要。knowledge-base文件上传必须保持原始二进制。

`import_doc`/`append_doc`前，所有字符串字段（content、title）必须确认UTF-8：

| 内容来源 | 方法 |
|----------|------|
| 文件读取 | 检测编码转UTF-8 |
| WebFetch | GBK/Latin-1需转码 |
| 用户输入/拼接 | 清洗非法UTF-8字节 |

```bash
# Python转码
content=$(python3 -c "import sys;data=open('f','rb').read()
for enc in ['utf-8','gbk','gb2312','big5','latin-1']:
    try: sys.stdout.write(data.decode(enc));break
    except: continue")
```
