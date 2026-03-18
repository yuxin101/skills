# OpenClaw mlx-audio - 本地语音合成与识别

基于 mlx-audio 的 OpenClaw 本地 TTS & STT 集成 - 无需 API 密钥，无需云服务，完全在 Apple Silicon 上运行。

## 功能

- **mlx-tts**: 文本转语音 (TTS) - 支持多种模型和语言
- **mlx-stt**: 语音转文本 (STT) - 使用 Whisper 模型进行语音识别

## 触发条件

当用户请求以下操作时使用此技能：
- "朗读这段文字" / "把这段话转成语音" - 使用 TTS
- "转录这个音频" / "听写这段语音" - 使用 STT
- "检查语音服务状态" - 查看 TTS/STT 服务器状态

## 工具

### mlx_tts (文本转语音)

```json
{
  "action": "generate",
  "text": "要合成的文本",
  "outputPath": "/tmp/output.mp3",
  "model": "可选：指定模型",
  "langCode": "可选：语言代码",
  "speed": "可选：语速倍数"
}
```

### mlx_stt (语音转文本)

```json
{
  "action": "transcribe",
  "audioPath": "/path/to/audio.wav",
  "model": "可选：指定模型",
  "language": "可选：语言代码"
}
```

### mlx_audio_status (状态检查)

```json
{
  "action": "status"
}
```

返回 TTS 和 STT 服务器的运行状态、加载的模型等信息。

## 可用模型

### TTS 模型
| 模型 | 语言 | 描述 |
|------|------|------|
| Kokoro-82M | 多语言 | 快速轻量，54 种预设声音 |
| Qwen3-TTS-0.6B | 中英日韩 | 中文质量优秀 |
| Qwen3-TTS-1.7B | 中英日韩 | 声音设计功能 |

### STT 模型
| 模型 | 描述 |
|------|------|
| whisper-large-v3-turbo | 快速准确的语音识别 |

## CLI 命令

| 命令 | 描述 |
|------|------|
| `/mlx-tts status` | 查看 TTS 服务器状态 |
| `/mlx-tts test <文本>` | 测试生成语音 |
| `/mlx-stt status` | 查看 STT 服务器状态 |
| `/mlx-stt transcribe <音频>` | 转录音频 |

## 配置

在 `openclaw.json` 中配置：

```json
{
  "plugins": {
    "entries": {
      "openclaw-mlx-audio": {
        "config": {
          "tts": {
            "enabled": true,
            "model": "mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16",
            "port": 19280,
            "langCode": "zh"
          },
          "stt": {
            "enabled": true,
            "model": "mlx-community/whisper-large-v3-turbo",
            "port": 19290,
            "language": "zh"
          }
        }
      }
    }
  }
}
```

## 注意事项

- **完全本地**: 所有处理在本地完成，数据不出机器
- **首次运行较慢**: 模型需要预热和下载
- **内存需求**: 根据选择的模型，可能需要 2-16GB 内存
