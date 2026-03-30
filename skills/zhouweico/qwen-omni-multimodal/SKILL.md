---
name: qwen-omni-multimodal
description: |
  基于阿里云百炼 Qwen3-Omni-Flash 的全模态 skill。支持文本、图片、音频、视频理解，以及文本/语音输出。
  当用户需要分析图片、转写或理解音频、理解视频、进行跨模态问答，或直接生成语音回复时，使用此 skill。
homepage: https://help.aliyun.com/zh/model-studio/qwen-omni
metadata:
  openclaw:
    requires:
      env:
        - DASHSCOPE_API_KEY
      bins:
        - node
    primaryEnv: DASHSCOPE_API_KEY
---

# Qwen Omni Multimodal

通过阿里云百炼 OpenAI 兼容接口调用 Qwen Omni 模型，默认使用 `qwen3-omni-flash`，也支持显式切换到 `qwen-omni-turbo` 家族；支持文本、图片、音频、视频输入，并可返回文本或音频。

详细参数与约束见 `references/api.md`。

脚本支持单轮调用，也支持带本地会话历史的多轮对话。

## Setup

1. 配置 API Key：

```bash
export DASHSCOPE_API_KEY="sk-xxx"
```

也可以在 skill 目录下创建 `config.json`：

可先参考 `config.example.json` 再复制为 `config.json`。

```json
{
  "apiKey": "sk-xxx",
  "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "selectionPolicy": "auto",
  "defaultModel": "qwen3-omni-flash",
  "modelCandidates": [
    "qwen3-omni-flash",
    "qwen-omni-turbo"
  ],
  "voiceByModelFamily": {
    "qwen3-omni-flash": "Cherry",
    "qwen-omni-turbo": "Serena"
  },
  "voice": "Cherry"
}
```

2. 运行环境要求 `Node.js >= 18`

3. 可选：如果使用新加坡地域，覆盖 Base URL：

```bash
export DASHSCOPE_BASE_URL="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
```

配置优先级：

- CLI 参数
- 环境变量
- `config.json`
- 脚本默认值

具体覆盖规则：

- 模型选择：`CLI --model > DASHSCOPE_MODEL > selectionPolicy=auto > config.defaultModel > config.model > 内置默认`
- Base URL：`DASHSCOPE_BASE_URL > config.baseUrl > 内置默认`
- 音色选择：`CLI --voice > DASHSCOPE_VOICE > config.voiceByModelFamily[模型家族] > config.voice > 内置默认`
- API Key：`DASHSCOPE_API_KEY > config.apiKey`
- `selectionPolicy=fixed|auto`
  - `fixed`：按默认模型走，不自动切换
  - `auto`：音频输入或音频输出优先 `qwen3-omni-flash`，纯文本/图片/视频理解优先 `qwen-omni-turbo`
- `config.modelCandidates` 用于维护候选模型列表；`selectionPolicy=auto` 时会优先在候选列表里选模型
- `config.voiceByModelFamily` 用于给不同模型家族配置不同默认音色，避免切模型后沿用不兼容音色

## 何时使用

- 用户要看图说话、图像问答、图像对比
- 用户要识别、转写、总结音频
- 用户要理解视频内容，或同时利用视频中的视觉和音频信息
- 用户要求模型直接输出语音
- 用户明确提到 Qwen-Omni / Qwen3-Omni-Flash / 百炼全模态

## 关键限制

- Qwen-Omni 只支持流式调用，脚本默认强制 `stream=true`
- 一条 `user` 消息只允许包含文本和一种模态数据
- 输出音频时需要显式设置 `modalities=["text","audio"]`
- `qwen3-omni-flash` 开启思考模式时，不支持音频输出
- 图片列表形式的视频输入对 `qwen3-omni-flash` 要求 2 到 128 张图片
- 多轮模式下，脚本只保留当前活动话题；切到 `fresh` 时不会把旧话题继续注入给模型

## 支持模型与选择建议

- 默认模型：`qwen3-omni-flash`
- 也支持显式选择：`qwen-omni-turbo`
- 推荐在 `config.json` 中使用：
  - `selectionPolicy`：设置 `fixed` 或 `auto`
  - `defaultModel`：设置默认模型
  - `modelCandidates`：维护允许 Agent 自动优先考虑的模型列表
- 当前脚本已内置价格提醒的模型家族：
  - `qwen3-omni-flash`
  - `qwen3-omni-flash-2025-12-01`
  - `qwen3-omni-flash-2025-09-15`
  - `qwen-omni-turbo`
  - `qwen-omni-turbo-latest`
  - `qwen-omni-turbo-2025-03-26`
  - `qwen-omni-turbo-2025-01-19`
- 价格取舍基于你提供的中国内地价格表：
  - `qwen3-omni-flash`：音频输入更便宜，适合音频理解和语音相关任务
  - `qwen-omni-turbo`：文本、图片/视频输入和文本输出明显更便宜，适合以文本与视觉理解为主的任务
- 当前 skill 默认仍使用 `qwen3-omni-flash`
  - 原因是现有约束、示例和守卫规则主要按 `qwen3-omni-flash` 文档整理
  - 当 `selectionPolicy=auto` 时，会按任务类型在 `qwen3-omni-flash` 和 `qwen-omni-turbo` 之间自动二选一

## 音色选择建议

- 当前脚本已内置模型家族音色表，并会在 `--with-audio` 时校验音色是否合法
- 可用 `--list-voices --model <model>` 查看当前模型家族支持的音色
- 推荐把默认音色维护在 `config.voiceByModelFamily` 中，而不是只写一个全局 `voice`
- `qwen-omni-turbo` 当前内置音色：
  - `Cherry(辛悦)`
  - `Serena(苏瑶)`
  - `Ethan(晨煦)`
  - `Chelsie(千雪)`
- `qwen3-omni-flash` 当前内置音色：
  - `Cherry(辛悦)`、`Ethan(晨煦)`、`Nofish(不吃鱼)`、`Jennifer(詹妮弗)`、`Ryan(甜茶)`
  - `Katerina(卡捷琳娜)`、`Elias(墨讲师)`、`Jada(上海-阿珍)`、`Dylan(北京-晓东)`、`Sunny(四川-晴儿)`
  - `Li(南京-老李)`、`Marcus(陕西-秦川)`、`Roy(闽南-阿杰)`、`Peter(天津-李彼得)`、`Rocky(粤语-阿强)`、`Kiki(粤语-阿清)`、`Eric(四川-程川)`
- 经验建议：
  - 通用中文讲解默认优先 `Cherry`
  - 温柔女声可优先 `Serena`
  - 标准男声可优先 `Ethan`
  - 方言或角色化表达再按模型支持表显式选

## CLI

主要脚本：`node scripts/qwen-omni-chat.js`

### 文本

```bash
node scripts/qwen-omni-chat.js \
  --selection-policy="auto" \
  --prompt="用中文概括一下什么是全模态模型"
```

### 图片理解

```bash
node scripts/qwen-omni-chat.js \
  --prompt="描述这张图片，并指出最重要的三个细节" \
  --image="/absolute/path/image.jpg"
```

可重复 `--image` 传多张图。

### 音频理解

```bash
node scripts/qwen-omni-chat.js \
  --prompt="转写这段音频，并给出简短摘要" \
  --audio="/absolute/path/audio.mp3"
```

### 视频理解

```bash
node scripts/qwen-omni-chat.js \
  --prompt="概括这个视频的主要内容" \
  --video="/absolute/path/video.mp4"
```

### 图片列表形式的视频

```bash
node scripts/qwen-omni-chat.js \
  --prompt="描述这个动作序列发生了什么" \
  --video-frames="/abs/1.jpg,/abs/2.jpg,/abs/3.jpg"
```

### 文本加语音输出

```bash
node scripts/qwen-omni-chat.js \
  --prompt="请用中文做一个 20 秒以内的语音自我介绍" \
  --with-audio \
  --voice="Cherry" \
  --audio-out="/tmp/qwen-omni.wav"
```

### 查看某个模型支持的音色

```bash
node scripts/qwen-omni-chat.js --list-voices --model="qwen-omni-turbo"
```

### 仅做预检，不实际调用

```bash
node scripts/qwen-omni-chat.js \
  --prompt="描述这张图片，并指出最重要的三个细节" \
  --image="/absolute/path/image.jpg" \
  --dry-run
```

### 多轮对话

```bash
node scripts/qwen-omni-chat.js \
  --session="demo-chat" \
  --prompt="先分析这张图片" \
  --image="/abs/demo.jpg"
```

```bash
node scripts/qwen-omni-chat.js \
  --session="demo-chat" \
  --prompt="把刚才的结论总结成三点" \
  --mode="continue"
```

### 新话题切换

```bash
node scripts/qwen-omni-chat.js \
  --session="demo-chat" \
  --prompt="现在换个新问题，解释一下多模态模型训练难点" \
  --mode="fresh"
```

### 会话管理

```bash
node scripts/qwen-omni-chat.js --list-sessions
node scripts/qwen-omni-chat.js --show-session --session="demo-chat"
node scripts/qwen-omni-chat.js --clear-session --session="demo-chat"
```

## 工作流

1. 先判断输入属于图片、音频、视频中的哪一种。
2. 如果用户一次给了多种非文本模态，先拆成多次调用，或让用户明确优先级。
3. 默认模型为 `qwen3-omni-flash`。只有在用户明确要求或你确认更合适时再切换模型。
   - 纯文本/图片/视频理解且成本敏感时，可优先尝试 `qwen-omni-turbo`
   - 音频理解或语音相关任务，默认仍优先 `qwen3-omni-flash`
4. 需要语音回复时，关闭思考模式并保存脚本生成的 WAV 文件路径。
5. 需要延续当前话题时使用同一个 `--session`；需要切换新内容时使用 `--mode=fresh` 或直接新建 session。
6. 脚本会在调用前输出中国内地单价提醒；如果响应 `usage` 足够完整，还会输出本次费用估算。

## 多轮策略

- `--mode=auto`
  - 默认模式
  - 有新图片/音频/视频输入时，优先判为新话题
  - 纯文本追问时，优先判为继续当前话题
- `--mode=continue`
  - 强制延续当前 session 的活动话题
  - 会带最近几轮历史，以及更早历史的压缩摘要
- `--mode=fresh`
  - 强制开启新话题
  - 保留 session 文件，但重置活动上下文，避免模型被旧内容拖住

会话文件保存在 `sessions/` 目录。

## 会话与覆盖规则

- 会话模式：`CLI --mode > 默认 auto`
- 会话标识：`CLI --session` 或 `--new-session`
- 未指定 `--session` 时，只允许单轮调用；不能使用 `--mode=continue`
- `--reset-session` 会在当前请求前重置活动上下文
- `--mode=fresh` 会重置当前活动话题，但保留同一个 session 文件
- `--dry-run` 不会写入或删除任何 session 文件；如果同时传了 `--reset-session`，只打印将要发生的变化

## 参数约定

- `--prompt`：用户文本提示，必填
- `--session`：会话 ID，用于多轮对话
- `--selection-policy=fixed|auto`：模型选择策略，默认读配置，未配置时为 `fixed`
- `--new-session`：创建新 session；不传值时自动生成 ID
- `--mode=auto|continue|fresh`：会话路由模式，默认 `auto`
- `--history-window`：多轮模式下保留的最近轮数，默认 `6`
- `--reset-session`：在当前请求前重置活动上下文
- `--list-sessions`：列出已保存会话
- `--show-session`：查看某个会话摘要
- `--clear-session`：删除某个会话
- `--image`：图片路径、HTTP(S) URL 或 Data URL，可重复
- `--audio`：音频路径、HTTP(S) URL 或 Data URL
- `--video`：视频路径、HTTP(S) URL 或 Data URL
- `--video-frames`：逗号分隔的图片列表，按视频帧顺序传入
- `--with-audio`：启用音频输出
- `--voice`：输出音色，默认 `Cherry`
- `--list-voices`：查看当前模型家族支持的音色列表
- `--audio-out`：输出 WAV 文件路径，默认 `/tmp/qwen-omni-<timestamp>.wav`
- `--enable-thinking=true|false`：是否开启思考模式，默认 `false`
- `--system`：可选系统提示词
- `--dry-run`：只打印价格提醒和脱敏后的请求体，不实际调用 API，也不会落盘 session 变更

## 推荐的 Agent 调用方式

- 默认优先单轮调用；只有明确存在追问、延续分析或会话管理需求时再传 `--session`
- 日常优先把模型策略交给 `config.selectionPolicy + config.defaultModel + config.modelCandidates` 控制，不要反复改脚本
- 日常默认音色优先交给 `config.voiceByModelFamily` 控制；切模型家族时不要假设同一个音色参数总是可用
- 用户给了新的图片、音频或视频，且没有明确要求延续上下文时，优先用 `--mode=fresh` 或直接不带 session
- 用户明确说“继续”“基于刚才”“上一轮”时，优先复用原 session，并使用 `--mode=continue`
- 需要语音输出时，显式传 `--with-audio`，同时确保 `--enable-thinking=false`；不确定音色时先运行 `--list-voices`
- 正式调用前先跑一次 `--dry-run`，确认模型来源、模态判定、会话模式、请求体预览和价格提醒

## 成本提醒

- 脚本会先输出中国内地价格表对应的单价提醒
- 当前内置单价：
  - 输入文本：`1.8 元/百万Token`
  - 输入音频：`15.8 元/百万Token`
  - 输入图片/视频：`3.3 元/百万Token`
  - 输出文本（纯文本输入）：`6.9 元/百万Token`
  - 输出文本（多模态输入）：`12.7 元/百万Token`
  - 输出文本+音频：按音频 `62.6 元/百万Token` 计
- 如果响应里的 `usage` 带了足够的 token 明细，脚本会进一步输出本次费用估算
- 这不是实时价格查询；如果官方价格变化，需要同步更新脚本

## 失败时优先检查

- 是否缺少 `DASHSCOPE_API_KEY`
- `config.json` 是否是合法 JSON
- Node 版本是否低于 18
- 是否同时传入了多种非文本模态
- 是否在 `--with-audio` 时又开启了思考模式
- 多轮时是否忘记传 `--session`
- 是否错误地把新话题用了 `--mode=continue`
- 本地文件路径是否存在
- 视频帧数量是否满足要求
