---
name: soundai-asr
description: SoundAI ASR Provider API integration for OpenClaw. Transcribes audio to text with high accuracy.
author: SoundAI
tags: [asr, audio, speech-to-text, soundai]
version: 1.0.0
---

# SoundAI ASR Provider

This provider integrates OpenClaw with SoundAI's cloud-based ASR (Automatic Speech Recognition) API, enabling highly accurate speech-to-text functionality for audio recorded on edge devices.

## Installation & Configuration

After installing this plugin, you need to configure your SoundAI API Key in your environment variables:

```bash
export SOUNDAI_API_KEY="your_api_key_here"
```

## Features
This plugin implements the `transcribeAudio` method of the `MediaUnderstandingProvider` interface. The core logic sends audio data via HTTP requests to SoundAI's ASR service and returns the transcribed text to OpenClaw.