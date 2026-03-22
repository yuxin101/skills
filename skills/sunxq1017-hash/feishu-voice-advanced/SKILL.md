---
name: feishu-voice-advanced
description: |
  🎙️ 飞书语音聊天神器 | Feishu Voice Chat for OpenClaw
  
  通过飞书直接与 OpenClaw 语音对话，AI 能听懂你的语气、感知你的情绪，并用 matching 的情绪语音回复。
  
  Talk to your AI agent via Feishu voice messages. It understands your tone, detects your emotion, and responds with emotionally-matched voice. Perfect for hands-free communication when typing is inconvenient.
  
  Use when: 发送飞书语音消息 / Sending Feishu voice messages · 语音识别 / Voice recognition · 情绪播报 / Emotional voice synthesis · 免提沟通 / Hands-free chat
---

# Feishu Voice Advanced 🎙️

> 让 OpenClaw 听懂你的声音，感受你的情绪  
> Let OpenClaw hear your voice, feel your emotion

飞书语音消息高级处理 Skill，支持接收语音、语音识别(ASR)、语音合成(TTS)发送语音消息，支持智能情绪播报。

## 功能特性

- 🎙️ **接收语音消息** - 自动接收飞书语音消息
- 🎯 **语音识别(ASR)** - 使用豆包极速版 ASR 将语音转为文字
- 🗣️ **语音合成(TTS)** - 使用豆包 TTS 2.0 生成语音
- 🎭 **智能情绪播报** - 使用 `context_texts` 让模型自动判断情绪

## 情绪控制规则 (V1.1)

### 核心原则
**默认使用引用上文**，让豆包模型从用户输入中自动感知情绪。

### 两层逻辑

| 条件 | 处理方式 | 说明 |
|------|---------|------|
| 用户输入以 `[#...]` 开头 | 原样使用，无 `context_texts` | 显式指令，如 `[#用激动的语气说]` |
| 其他情况 | `context_texts` = [用户输入] | 模型从用户输入中感知情绪 |

### 工作原理

- **`text`**: AI 生成的实际播报内容
- **`context_texts`**: 用户原始输入，作为情绪参考（不计费）

豆包模型从 `context_texts` 中理解语境情绪，用相应语气播报 `text`。

## 使用方法

### 1. 接收并识别语音

```python
from feishu_voice import FeishuVoice

voice = FeishuVoice()
text = voice.recognize_voice("/path/to/audio.ogg")
print(f"识别结果: {text}")
```

### 2. 发送语音消息（推荐方式）

```python
from feishu_voice import send

# 方式1：AI生成内容 + 用户输入（用 context_texts）
# 模型从 user_input 中感知情绪，用相应语气播报 text
send(
    text="对不起桥总，是我太笨了，我深刻检讨！",
    user_input="你怎么回事，这么笨，给我做个检讨"
)

# 方式2：显式指令（不用 context_texts）
send("[#用激动的语气说]我们成功了！")
```

### 3. 完整示例

```python
from feishu_voice import FeishuVoice

voice = FeishuVoice()

# 场景1：被批评后检讨
user_input = "你真笨，这么点事都做不好，用飞书语音给我发一段检讨"
ai_response = "桥总，对不起！我确实太笨了，连这么简单的事情都做不好。我深刻反省，一定改进！"
voice.send_voice(ai_response, user_input=user_input)

# 场景2：被表扬后汇报
user_input = "你真棒，汇报一下本周成果"
ai_response = "本周我们完成了三个重要项目，超额完成目标！"
voice.send_voice(ai_response, user_input=user_input)

# 场景3：显式指令
voice.send_voice("[#用低沉沙哑的语气说]高兄，你看这烛火，要灭了...")
```

## API 说明

### `send(text, receive_id, emotion, user_input)`

发送语音消息（便捷函数）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `text` | string | 是 | AI 生成的实际播报内容 |
| `receive_id` | string | 否 | 接收者 ID，默认当前用户 |
| `emotion` | string | 否 | 情绪类型，默认 `auto` |
| `user_input` | string | 否 | 用户原始输入，用于 `context_texts` |

### `FeishuVoice.send_voice(text, receive_id, emotion, user_input)`

类方法，功能同上。

### `FeishuVoice.generate_voice(text, emotion, context)`

生成语音文件，返回 Opus 文件路径。

| 参数 | 类型 | 说明 |
|------|------|------|
| `text` | string | AI 生成的播报内容 |
| `emotion` | string | 情绪类型 |
| `context` | string | 用户原始输入，用于 `context_texts` |

### `FeishuVoice.recognize_voice(audio_path)`

识别语音文件，返回文字。

## 技术细节

### TTS Payload 结构

```json
{
  "user": {"uid": "12345"},
  "event": 100,
  "req_params": {
    "text": "实际播报内容",
    "speaker": "zh_male_m191_uranus_bigtts",
    "audio_params": {
      "format": "mp3",
      "sample_rate": 24000
    },
    "additions": "{\"context_texts\": [\"用户原始输入\"]}"
  }
}
```

**注意：** `additions` 必须是 JSON 字符串，不是 object。

### 与 `[#...]` 语法的区别

| 方式 | 字段 | 说明 |
|------|------|------|
| `[#...]` | `text` | 直接拼接在 text 前，如 `[#用激动的语气说]内容` |
| `context_texts` | `additions` | 独立参数，让模型理解语境后自动选择情绪 |

推荐使用 `context_texts`，更灵活自然。

## 配置

在 `scripts/feishu_voice.py` 中配置以下参数：

```python
# 豆包 ASR 配置
ASR_APP_ID = "4391887839"
ASR_ACCESS_KEY = "your-access-key"
ASR_RESOURCE_ID = "volc.bigasr.auc_turbo"

# 豆包 TTS 配置
TTS_APP_ID = "4391887839"
TTS_ACCESS_KEY = "your-access-key"
TTS_RESOURCE_ID = "seed-tts-2.0"

# 飞书配置
FEISHU_APP_ID = "cli_xxx"
FEISHU_APP_SECRET = "xxx"
```

## 依赖

- ffmpeg（用于音频格式转换）
- Python 3.8+

## 安装 | Installation

```bash
cd scripts
chmod +x install.sh
./install.sh
```

**Dependencies:** ffmpeg, Python 3.8+

**Note:** Scripts are located in the `scripts/` directory.

## 更新日志

### V1.1 (2026-03-22)
- 新增 `context_texts` 支持，使用豆包引用上文功能
- 改进情绪控制逻辑：默认使用引用上文，让模型自动判断情绪
- 简化 API：`user_input` 参数替代复杂的情绪映射
- 修复 `additions` 格式问题（必须是 JSON 字符串）

### V1.0
- 基础语音收发功能
- ASR 语音识别
- TTS 语音合成
- 简单情绪映射

EOF
