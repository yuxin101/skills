# SoundAI TTS Provider

This provider integrates OpenClaw with SoundAI's cloud-based TTS (Text-to-Speech) API, enabling high-quality voice synthesis for your agent's responses.

## Installation & Configuration

After installing this plugin, you need to configure your SoundAI API Key in your environment variables:

```bash
export SOUNDAI_API_KEY="your_api_key_here"
```

## Features
This plugin implements the `generateAudio` method of the `MediaGenerationProvider` interface. The core logic sends text data via HTTP requests to SoundAI's TTS service and returns the synthesized audio buffer to OpenClaw.