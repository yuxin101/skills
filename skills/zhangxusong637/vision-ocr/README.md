# vision-ocr

vision-ocr 是一个面向 OpenClaw 的文档识别技能，支持图片和 PDF 的 OCR 提取、多模态整合，以及 Markdown 结果输出。

它适合处理截图、扫描件、表格、技术文档、票据和常见 PDF 文档。识别完成后，结果默认发送到飞书，也可以按需关闭。

## 核心能力

- 图片识别：支持常见图片格式，默认按文档识别流程处理。
- PDF 识别：支持逐页处理，适合长文档和多页材料。
- Markdown 输出：尽量保留标题、列表、表格和代码块结构。
- 多模态整合：OCR 有效时，结合原图输出更完整的最终 Markdown。
- 手写优化：检测到手写文档、手写便条或手写批注相关指令时，会自动启用手写优先识别策略。
- 飞书发送：默认发送识别结果到飞书，可通过配置或命令行关闭。

## 安装要求

必需环境：

- Node.js 18+
- Python 3.8+
- PyMuPDF

安装 PyMuPDF：

```bash
pip install pymupdf
```

如需默认发送到飞书，建议同时安装 `feishu-send-files` 技能。

## 快速开始

1. 安装技能并进入目录。
2. 准备 OCR 和多模态配置。
3. 运行命令或直接在 OpenClaw 中调用。

自动同步多模态配置：

```bash
cd ~/.openclaw/workspace/skills/vision-ocr
node index.js --update-config
```

图片识别示例：

```bash
node index.js --image /path/to/image.jpg --confirm=true
```

PDF 识别示例：

```bash
node index.js --image /path/to/file.pdf --pdf-option=ocr_full --confirm=true
```

关闭飞书发送：

```bash
node index.js --image /path/to/image.jpg --confirm=true --no-send-to-feishu
```

## 配置

支持以下配置来源，优先级从高到低：

1. 环境变量
2. 技能目录配置 `~/.openclaw/workspace/skills/vision-ocr/config.json`
3. Workspace 配置 `~/.openclaw/workspace/config.json`
4. OpenClaw 主配置 `~/.openclaw/openclaw.json`

推荐配置示例：

```json
{
  "ocr": {
    "imageocr": {
      "token": "你的 ImageOCR Token",
      "endpoint": "你的 ImageOCR 端点"
    },
    "multimodal": {
      "baseUrl": "你的多模态 API 地址",
      "token": "你的多模态 Token",
      "model": "你的模型名称"
    }
  },
  "autoSendToFeishu": true
}
```

机器人模式下，如果 OpenClaw 提供当前会话上下文，识别结果会优先发送到当前群聊或当前私聊。若要发送给其他对象，可直接在对话里明确指定，例如：`发给 open_id:ou_xxx` 或 `发给 chat:oc_xxx`。

OpenClaw 集成时，若希望自动发送到当前会话，必须以机器人模式调用导出的 `run(context)`，不能只走命令行：

```js
const visionOcr = require('/home/node/.openclaw/workspace/skills/vision-ocr');

await visionOcr.run({
  session: {
    chatId: 'chat_xxx',
    openId: 'ou_xxx',
    isGroup: false
  },
  message: {
    text: '识别图片 /path/to/image.jpg'
  },
  replyText: async (msg) => {
    console.log(msg);
  }
});
```

如果 OpenClaw 只执行 `node index.js --image ...` 这类命令行调用，技能仍可完成识别，但不会拿到 `context.session`，因此无法自动发送到当前飞书会话。

常用环境变量：

```bash
export VISION_IMAGEOCR_TOKEN="你的 Token"
export VISION_IMAGEOCR_ENDPOINT="你的端点"
export VISION_BASE_URL="你的多模态 API 地址"
export VISION_MULTIMODAL_TOKEN="你的多模态 Token"
export VISION_MODEL="你的模型名称"
export VISION_AUTO_SEND_TO_FEISHU="true"
```

## 使用方式

OpenClaw 对话示例：

```text
识别图片 /path/to/image.jpg
识别 PDF /path/to/file.pdf --pdf-option=ocr_full
OCR 这个截图
```

常用参数：

| 参数 | 说明 |
| ---- | ---- |
| `--image` | 输入图片或 PDF 路径 |
| `--pdf-option` | PDF 处理方式 |
| `--prompt` | 自定义补充指令 |
| `--prompt-type` | 预设模板类型 |
| `--confirm` | 跳过交互确认 |
| `--progress` | 显示处理进度 |
| `--no-send-to-feishu` | 关闭自动发送到飞书 |

PDF 处理选项：

| 选项 | 说明 |
| ---- | ---- |
| `ocr_full` | 逐页识别全部内容 |
| `ocr_table` | 逐页提取表格内容 |
| `ocr_plain` | 逐页提取纯文字 |
| `save_images` | 将 PDF 保存为图片 |
| `info` | 查看 PDF 基本信息 |

## 结果与隐私

- 默认会发送识别结果到飞书。
- 在 OpenClaw 机器人会话中，默认优先发送到当前会话；没有当前会话上下文时不会自动发送。
- 如处理敏感文档，建议显式使用 `--no-send-to-feishu`。
- 发送关闭或发送失败时，结果会保留在临时目录 `/tmp/vision-ocr-<PID>/result.md`。
- 仓库和发布包中不应包含真实 `config.json`、Token 或 API Key。

## 常见问题

### 未找到 imageocr 配置

请检查以下任一位置是否已配置：

1. `~/.openclaw/workspace/skills/vision-ocr/config.json`
2. `~/.openclaw/workspace/config.json`
3. 环境变量 `VISION_IMAGEOCR_TOKEN` 与 `VISION_IMAGEOCR_ENDPOINT`

### 未自动发送到飞书

如果当前运行环境没有提供会话上下文，技能会保留结果文件而不自动发送。OpenClaw 集成时，这通常表示当前仍在使用命令行模式而不是机器人模式。此时可改为调用导出的 `run(context)`，或在对话中显式指定接收者，或手动发送生成的 Markdown 文件。

### PDF 转图片失败

通常是未安装 PyMuPDF：

```bash
pip install pymupdf
```

### 需要查看详细日志

```bash
DEBUG=1 node index.js --image /path/to/file.jpg --confirm=true
```

## 发布页

Clawhub 页面：<https://clawhub.ai/zhangxusong637/vision-ocr>
