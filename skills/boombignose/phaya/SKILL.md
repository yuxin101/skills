---
name: phaya
description: Use the Phaya SaaS backend to generate images, videos, audio, music, and run LLM chat completions via simple REST API calls. Use when the user wants to generate media, call AI models, or use the Phaya API for image/video/audio/text generation.
metadata: {"clawdbot":{"emoji":"🎬","requires":{"anyBins":["curl","python3"]},"os":["linux","darwin","win32"]}}
---

# Phaya Media API

Phaya is a FastAPI backend that brokers AI media generation across KIE.ai (Sora 2, Veo 3.1, Seedance, Kling, Seedream, Suno), Google Gemini TTS, and OpenRouter LLMs.

## Auth

All endpoints require a Bearer token or API key:

```
Authorization: Bearer <your_api_key>
```

Get your profile and credit balance:
- `GET /api/v1/user/profile` — full profile
- `GET /api/v1/user/credits` → `{ "credits_balance": 84.90, ... }`

**Rate limit:** 60 requests/minute per API key.

## Credit System

Every generation costs credits deducted on job creation; auto-refunded on failure.

| Credits | Service |
|---------|---------|
| 0.5 | image-to-video (FFmpeg local), Sora 2 character creation |
| 1.0 | text-to-image (Z-Image) |
| 1.5 | Seedream 5.0 |
| 2–4 | Nano Banana 2 (1K/2K/4K resolution) |
| 3.0 | Text-to-music (Suno) |
| 2–35 | Seedance 1.5 Pro (resolution × duration × audio) |
| 8.0 | Sora 2 video |
| 1.21–1.82/sec | Kling 2.6 motion control (720p/1080p) |
| 15.0 | Veo 3.1 fast (`veo3_fast`) |
| 50.0 | Veo 3.1 quality (`veo3`) |

## Job / Polling Pattern

Every generation is async. Create endpoints return `job_id` immediately; poll the status endpoint.

```
POST /api/v1/<service>/create   →  { "job_id": "uuid" }
GET  /api/v1/<service>/status/{job_id}  →  { "status": "...", "<media>_url": "..." }
```

**Status values:**
- Image/music endpoints: `PENDING`, `QUEUED`, `PROCESSING`, `COMPLETED`, `FAILED`
- Speech/subtitle endpoints: `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`
- Video/download endpoints: `processing`, `completed`, `failed`, `cancelled`

**Response URL field by media type:**

| Media type | Response field |
|------------|---------------|
| Images | `image_url` |
| Videos | `video_url` |
| Audio / music | `audio_url` (music also returns `audio_urls[]`) |
| Sora 2 character | `character_id` (a string ID, not a URL) |

Poll every 3–5 seconds until the terminal status is reached.

## Quick Start

### 1. Generate an image (text-to-image)

```python
import httpx, time

BASE = "https://your-api-host/api/v1"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY"}

r = httpx.post(f"{BASE}/text-to-image/generate", headers=HEADERS, json={
    "prompt": "A futuristic city at sunset, ultra-detailed",
    "aspect_ratio": "16:9"
})
job_id = r.json()["job_id"]

while True:
    s = httpx.get(f"{BASE}/text-to-image/status/{job_id}", headers=HEADERS).json()
    if s["status"] == "COMPLETED":
        print("Image URL:", s["image_url"])
        break
    if s["status"] == "FAILED":
        raise RuntimeError("Job failed")
    time.sleep(4)
```

### 2. Generate a video (Sora 2 text-to-video)

```python
r = httpx.post(f"{BASE}/sora2-text-to-video/create", headers=HEADERS, json={
    "prompt": "A dragon flying over mountains at dawn",
    "aspect_ratio": "landscape",
    "n_frames": "10"          # "10" or "15" as a string
})
job_id = r.json()["job_id"]
# Poll /sora2-text-to-video/status/{job_id} → s["video_url"]
```

### 3. Chat with Phaya-GPT

```python
r = httpx.post(f"{BASE}/phaya-gpt/chat/completions", headers=HEADERS, json={
    "messages": [{"role": "user", "content": "Hello, what can you do?"}],
    "stream": False
})
print(r.json()["message"]["content"])   # flat dict — NOT choices[0].message.content
```

## Additional Resources

- Full endpoint reference: [endpoints.md](endpoints.md)
- Curl & Python examples for every category: [examples.md](examples.md)
