# 百度智能云 BOS 操作参考

本文档记录三种操作方式的详细参数定义，供执行操作时查阅。

**环境设置**：首次使用请运行 `scripts/setup.sh`，详见 `SKILL.md` 首次使用章节。

**官方文档链接：**
- BOS Node.js SDK: https://cloud.baidu.com/doc/BOS/s/Djwvyrhiw
- BOS Python SDK: https://cloud.baidu.com/doc/BOS/s/Vjwvyrfs3
- bcecmd 工具: https://cloud.baidu.com/doc/BOS/s/kmcn3zrup

---

## 方式一：scripts/bos_node.mjs 命令参考

脚本位于 `scripts/bos_node.mjs`，依赖 `@baiducloud/sdk`（`npm install @baiducloud/sdk`）。
所有凭证通过环境变量读取。输出 JSON 格式。

### 环境变量

| 变量 | 必需 | 说明 |
|------|:----:|------|
| `BCE_ACCESS_KEY_ID` | ✅ | 百度云 Access Key ID |
| `BCE_SECRET_ACCESS_KEY` | ✅ | 百度云 Secret Access Key |
| `BCE_BOS_ENDPOINT` | ✅ | BOS 服务端点（如 `bj.bcebos.com`） |
| `BCE_BOS_BUCKET` | ✅ | 存储桶名称 |
| `BCE_STS_TOKEN` | ❌ | 临时安全凭证 SessionToken |

### 可用操作

| 操作 | 命令 | 说明 |
|------|------|------|
| upload | `node bos_node.mjs upload --file <path> --key <key>` | 上传本地文件 |
| put-string | `node bos_node.mjs put-string --content <text> --key <key> [--content-type <mime>]` | 上传字符串内容 |
| download | `node bos_node.mjs download --key <key> --output <path>` | 下载文件到本地 |
| list | `node bos_node.mjs list [--prefix <prefix>] [--max-keys <n>] [--marker <m>]` | 列出文件 |
| sign-url | `node bos_node.mjs sign-url --key <key> [--expires <seconds>]` | 获取签名下载链接 |
| head | `node bos_node.mjs head --key <key>` | 查看文件元信息 |
| delete | `node bos_node.mjs delete --key <key>` | 删除文件 |
| copy | `node bos_node.mjs copy --source-key <key> --key <dest-key> [--source-bucket <bucket>]` | 复制文件 |
| list-buckets | `node bos_node.mjs list-buckets` | 列出所有 Bucket |

### 操作详细参数

#### upload
上传本地文件到存储桶。
- `--file` (string, **必需**): 本地文件路径
- `--key` (string, 可选): 存储桶中的目标路径，默认取文件名

#### put-string
上传字符串内容到存储桶。
- `--content` (string, **必需**): 要上传的字符串内容
- `--key` (string, **必需**): 存储桶中的目标路径
- `--content-type` (string, 可选): MIME 类型，默认 `text/plain`

#### download
下载存储桶中的文件到本地。
- `--key` (string, **必需**): 文件在存储桶中的路径
- `--output` (string, 可选): 本地保存路径，默认取文件名

#### list
列出存储桶中的文件。
- `--prefix` (string, 可选): 路径前缀过滤
- `--max-keys` (number, 可选): 最大返回数量，默认 100
- `--marker` (string, 可选): 分页标记，用于获取下一页

#### sign-url
获取文件的预签名下载链接。
- `--key` (string, **必需**): 文件在存储桶中的路径
- `--expires` (number, 可选): 链接有效期（秒），默认 3600

#### head
获取文件的元信息。
- `--key` (string, **必需**): 文件在存储桶中的路径

#### delete
删除存储桶中的文件。
- `--key` (string, **必需**): 文件在存储桶中的路径

#### copy
复制文件（同桶或跨桶）。
- `--source-key` (string, **必需**): 源文件路径
- `--key` (string, **必需**): 目标文件路径
- `--source-bucket` (string, 可选): 源 Bucket，默认当前 Bucket

#### list-buckets
列出账号下的所有 Bucket。
- 无参数

### 返回格式

成功时 `success: true`，退出码 0；失败时 `success: false`，退出码 1。

---

## 方式二：scripts/bos_python.py 命令参考

脚本位于 `scripts/bos_python.py`，依赖 `bce-python-sdk`（`pip install bce-python-sdk`）。
环境变量和操作与方式一完全一致。

### 可用操作

| 操作 | 命令 | 说明 |
|------|------|------|
| upload | `python3 bos_python.py upload --file <path> --key <key>` | 上传本地文件 |
| put-string | `python3 bos_python.py put-string --content <text> --key <key> [--content-type <mime>]` | 上传字符串内容 |
| download | `python3 bos_python.py download --key <key> --output <path>` | 下载文件到本地 |
| list | `python3 bos_python.py list [--prefix <prefix>] [--max-keys <n>] [--marker <m>]` | 列出文件 |
| sign-url | `python3 bos_python.py sign-url --key <key> [--expires <seconds>]` | 获取签名下载链接 |
| head | `python3 bos_python.py head --key <key>` | 查看文件元信息 |
| delete | `python3 bos_python.py delete --key <key>` | 删除文件 |
| copy | `python3 bos_python.py copy --source-key <key> --key <dest-key> [--source-bucket <bucket>]` | 复制文件 |
| list-buckets | `python3 bos_python.py list-buckets` | 列出所有 Bucket |

参数与方式一完全一致，输出 JSON 格式。

---

## 方式三：bcecmd 命令参考

依赖百度云 bcecmd 工具，需手动安装。

安装参考: https://cloud.baidu.com/doc/BOS/s/kmcn3zrup

### 首次配置

```bash
bcecmd --conf-path ~/.bcecmd configure \
  --access-key <AK> \
  --secret-key <SK> \
  --domain <Endpoint>
```

### 常用命令

| 操作 | 命令 | 说明 |
|------|------|------|
| 上传文件 | `bcecmd bos cp <localpath> bos:/<bucket>/<bospath>` | 上传单个文件 |
| 递归上传目录 | `bcecmd bos cp <localdir> bos:/<bucket>/<bosdir>/ --recursive` | 上传整个目录 |
| 下载文件 | `bcecmd bos cp bos:/<bucket>/<bospath> <localpath>` | 下载单个文件 |
| 递归下载目录 | `bcecmd bos cp bos:/<bucket>/<bosdir>/ <localdir> --recursive` | 下载整个目录 |
| 列出文件 | `bcecmd bos ls bos:/<bucket>/[prefix]` | 列出文件 |
| 删除文件 | `bcecmd bos rm bos:/<bucket>/<bospath>` | 删除单个文件 |
| 递归删除 | `bcecmd bos rm bos:/<bucket>/<bosdir>/ --recursive --yes` | 强制递归删除 |
| 同步到 BOS | `bcecmd bos sync <localdir> bos:/<bucket>/<dir>/ [--delete]` | 增量同步本地到远端 |
| 同步到本地 | `bcecmd bos sync bos:/<bucket>/<dir>/ <localdir> [--delete]` | 增量同步远端到本地 |
| 文件信息 | `bcecmd bos head bos:/<bucket>/<bospath>` | 查看文件元信息 |
| 签名 URL | `bcecmd bos gen_signed_url bos:/<bucket>/<bospath> [-e<seconds>]` | 获取签名下载链接 |
| 列出 Bucket | `bcecmd bos ls` | 列出所有 Bucket |
| 创建 Bucket | `bcecmd bos mb bos:/<bucket>` | 创建存储桶 |
| 删除 Bucket | `bcecmd bos rb bos:/<bucket>` | 删除存储桶（必须为空） |

### 全局参数

- `--conf-path <PATH>`：指定配置目录（默认 `~/.bcecmd`）
- `--recursive` / `-r`：递归操作
- `--yes` / `-y`：跳过确认
- `--delete`：同步时删除目标端多余文件
- `--exclude <PATTERN>`：排除匹配的文件
- `--include <PATTERN>`：仅包含匹配的文件
- `-e<seconds>`：`gen_signed_url` 专用，指定 URL 有效期（秒），`-1` 为永久有效，默认 1800 秒；注意 `-e` 与数字之间无空格

---

## BOS Endpoint 对照表

| 区域 | Endpoint | 位置 |
|------|----------|------|
| 北京 | `bj.bcebos.com` | 华北 |
| 广州 | `gz.bcebos.com` | 华南 |
| 苏州 | `su.bcebos.com` | 华东 |
| 保定 | `bd.bcebos.com` | 华北 |
| 香港 | `hkg.bcebos.com` | 港澳台 |
