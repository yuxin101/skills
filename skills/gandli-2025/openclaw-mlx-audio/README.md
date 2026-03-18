# OpenClaw mlx-audio Plugin

🎙️ **OpenClaw integration for mlx-audio - Local TTS & STT on Apple Silicon**

Zero API keys. Zero cloud dependency. Powered by [Blaizzy/mlx-audio](https://github.com/Blaizzy/mlx-audio).

---

## What This Is

This plugin integrates **mlx-audio** into OpenClaw, providing:

- 🗣️ **TTS Tools** - Text-to-Speech via `mlx_tts` tool and `/mlx-tts` command
- 🎧 **STT Tools** - Speech-to-Text via `mlx_stt` tool and `/mlx-stt` command
- 📚 **Skills** - Documentation that teaches OpenClaw agents how to use these tools

**Not a re-implementation** - This is an integration layer that wraps the official mlx-audio library.

---

## Architecture

```
OpenClaw Agent
     │
     │ (learns from skills/mlx-tts/SKILL.md)
     ▼
Tool Call: mlx_tts
     │
     ▼
Plugin (src/index.ts)
     │
     ▼
HTTP API → Python Server (python-runtime/)
     │
     ▼
mlx-audio Library (Blaizzy/mlx-audio)
     │
     ▼
Generate Audio
```

---

## Prerequisites

### 1. Install mlx-audio (required)

```bash
# Using uv (recommended)
uv tool install mlx-audio --prerelease=allow

# Or using pip
pip install mlx-audio
```

### 2. Verify Installation

```bash
# Test TTS
mlx_audio.tts.generate --model mlx-community/Kokoro-82M-bf16 --text "Hello!" --lang_code a

# Test STT
mlx_audio.stt.transcribe --model mlx-community/whisper-large-v3-turbo-asr-fp16 --audio test.wav
```

---

## Installation

### Build the Plugin

```bash
cd ~/.openclaw/workspace/projects/openclaw-mlx-audio
bun install
bun run build
```

### Enable in OpenClaw

Add to your `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "openclaw-mlx-audio": {
        "enabled": true,
        "config": {
          "tts": {
            "enabled": true,
            "model": "mlx-community/Kokoro-82M-bf16",
            "port": 19280,
            "langCode": "a"
          },
          "stt": {
            "enabled": true,
            "model": "mlx-community/whisper-large-v3-turbo-asr-fp16",
            "port": 19290,
            "language": "en"
          }
        }
      }
    }
  }
}
```

### Restart OpenClaw

```bash
openclaw gateway restart
```

---

## Usage

### Via Tools (Agent)

Agents will automatically learn to use these tools from the Skills documentation.

**TTS Example:**
```json
{
  "tool": "mlx_tts",
  "parameters": {
    "action": "generate",
    "text": "Hello from OpenClaw!",
    "outputPath": "/tmp/speech.mp3"
  }
}
```

**STT Example:**
```json
{
  "tool": "mlx_stt",
  "parameters": {
    "action": "transcribe",
    "audioPath": "/tmp/recording.m4a",
    "language": "en"
  }
}
```

### Via Commands (User)

```bash
# TTS commands
/mlx-tts status
/mlx-tts test "Hello World"
/mlx-tts models
/mlx-tts reload

# STT commands
/mlx-stt status
/mlx-stt transcribe /tmp/audio.mp3
/mlx-stt models
/mlx-stt reload
```

---

## Supported Models

### TTS Models

| Model | Languages | Description |
|-------|-----------|-------------|
| **Kokoro-82M** ⭐ | 8 | Fast, 54 preset voices |
| **Qwen3-TTS-0.6B** | ZH, EN, JA, KO | Excellent Chinese quality |
| **Qwen3-TTS-1.7B** | ZH, EN, JA, KO | Voice design from text |
| **CSM-1B** | EN | Conversational, voice cloning |
| **Chatterbox** | 16 | Widest language coverage |

### STT Models

| Model | Languages | Description |
|-------|-----------|-------------|
| **Whisper-large-v3-turbo** ⭐ | 99+ | Fast & accurate |
| **Whisper-large-v3** | 99+ | Highest accuracy |
| **Qwen3-ASR** | ZH, EN, JA, KO | Alibaba multilingual |
| **VibeVoice-ASR-9B** | Multiple | Diarization, long-form |

See [MODELS.md](./MODELS.md) for complete list.

---

## Project Structure

```
openclaw-mlx-audio/
├── src/                        # TypeScript plugin code
│   ├── index.ts                # Main entry
│   ├── tts-server.ts           # TTS server management
│   └── stt-server.ts           # STT server management
│
├── python-runtime/             # Python wrapper (mlx-audio)
│   ├── tts_server.py           # TTS HTTP server
│   └── stt_server.py           # STT HTTP server
│
├── skills/                     # OpenClaw Skills
│   ├── mlx-tts/SKILL.md        # TTS usage guide
│   └── mlx-stt/SKILL.md        # STT usage guide
│
├── README.md                   # This file
├── README.zh-CN.md             # Chinese documentation
├── PROJECT_STRUCTURE.md        # Architecture details
├── MODELS.md                   # Supported models
└── QUICK_REFERENCE.md          # Quick model selection guide
```

---

## Development

```bash
# Install dependencies
bun install

# Build
bun run build

# Watch mode
bun run dev

# Test
bun test
```

---

## Configuration

### TTS Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable TTS |
| `model` | string | `Kokoro-82M` | Model to use |
| `port` | number | `19280` | Server port |
| `langCode` | string | `"a"` | Language code (Kokoro) |
| `pythonEnvMode` | string | `"managed"` | `managed` or `external` |

### STT Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable STT |
| `model` | string | `whisper-large-v3-turbo` | Model to use |
| `port` | number | `19290` | Server port |
| `language` | string | `"en"` | Language code |
| `pythonEnvMode` | string | `"managed"` | `managed` or `external` |

---

## Troubleshooting

### Server Not Starting

```bash
# Check if mlx-audio is installed
which mlx_audio

# Test mlx-audio directly
mlx_audio.tts.generate --text "Test" --lang_code a
```

### Model Download Issues

Models are cached at `~/.cache/huggingface/hub/`. Clear cache and retry:

```bash
rm -rf ~/.cache/huggingface/hub/models--mlx-community--*
```

### Check Status

```bash
/mlx-tts status
/mlx-stt status
```

---

## License

MIT

## Acknowledgments

- **[mlx-audio](https://github.com/Blaizzy/mlx-audio)** by Blaizzy - Core TTS/STT engine
- **[OpenClaw](https://github.com/openclaw/openclaw)** - Plugin framework

---

## Links

- GitHub: https://github.com/openclaw/openclaw-mlx-audio
- mlx-audio: https://github.com/Blaizzy/mlx-audio
- Documentation: [MODELS.md](./MODELS.md), [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
