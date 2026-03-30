---
name: byted-las-asr-pro
description: |
  Transcribe audio files to text using speech recognition.
  Use this skill when user needs to:
  - Convert audio/video to text (speech-to-text)
  - Transcribe recordings, meetings, or voice files
  - Extract text from audio with speaker diarization
  Supports multiple audio formats (wav/mp3/m4a/aac/flac), language detection, and speaker identification.
  Requires LAS_API_KEY for authentication.
---

# LAS-ASR-PRO（las_asr_pro）

本 Skill 用于把「LAS-ASR-PRO 接口文档」里的 `submit/poll` 异步调用流程，封装成可重复使用的脚本化工作流：

- `POST https://operator.las.cn-beijing.volces.com/api/v1/submit` 提交转写任务
- `POST https://operator.las.cn-beijing.volces.com/api/v1/poll` 轮询任务状态并获取识别结果

## 快速开始

在本 skill 目录执行：

```bash
python3 scripts/skill.py --help
```

### 提交并等待

```bash
python3 scripts/skill.py submit \
  --audio-url "https://example.com/audio.wav" \
  --audio-format wav \
  --model-name bigmodel \
  --region cn-beijing \
  --out result.json
```

### 仅提交（返回 task_id）

```bash
python3 scripts/skill.py submit \
  --audio-url "https://example.com/audio.wav" \
  --audio-format wav \
  --no-wait
```

### 轮询 / 等待

```bash
python3 scripts/skill.py poll <task_id>
python3 scripts/skill.py wait <task_id> --timeout 1800 --out result.json
```

## 参数与返回字段

详见 `references/api.md`。

## 常见问题

- API Key 未找到：设置环境变量 `LAS_API_KEY` 或提供 `env.sh`。
- Parameter.Invalid：检查字段结构/枚举值是否符合文档（推荐先最小化 payload，再逐项加字段）。
- `audio_format` 不正确：请确保容器格式与真实音频一致（以服务端支持为准）。
