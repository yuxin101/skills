---
name: lovelybots-video
description: Generate avatar videos from a script and image using the LovelyBots API. Queue a video, poll for completion, and retrieve a download URL — all in one workflow. Built for marketing teams, ecommerce brands, and agent pipelines that need consistent avatar video at scale.
metadata: { "openclaw": { "requires": { "env": ["LOVELYBOTS_API_KEY"], "bins": ["curl"] }, "primaryEnv": "LOVELYBOTS_API_KEY", "emoji": "🎬", "homepage": "https://lovelybots.com/openclaw" } }
---

# LovelyBots Video Generation

Generate avatar videos programmatically using the LovelyBots API. This skill lets you queue a video from a script and avatar image, poll until it's ready, and return the final video URL.

Get your API key at: https://lovelybots.com/developer/api_tokens

---

## What This Skill Does

- Submits a video generation job (script + avatar image → queued video)
- Polls the job status until complete (or failed)
- Returns the final video URL
- Reports credits used per request
- Works with any avatar image URL or previously used avatar

---

## Setup

Set your LovelyBots API key as an environment variable:

```bash
export LOVELYBOTS_API_KEY=your_api_key_here
```

Or add it to your openclaw.json:

```json
{
  "skills": {
    "entries": {
      "lovelybots-video": {
        "env": {
          "LOVELYBOTS_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

---

## Example Prompts

- "Generate a 30-second product ad video using my avatar at https://example.com/avatar.jpg with this script: Welcome to our summer sale..."
- "Make a video with the LovelyBots skill — use avatar URL [url] and script: [text]"
- "Queue a video generation job and give me the download link when it's done"
- "Create an avatar video for my TikTok ad using LovelyBots"

---

## How to Generate a Video

### Step 1 — Submit the job

```bash
curl -X POST https://lovelybots.com/api/create \
  -H "Authorization: Bearer $LOVELYBOTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "script": "Welcome to our summer sale. Use code SAVE20 for 20% off everything this week only.",
    "avatar_url": "https://example.com/your-avatar.jpg"
  }'
```

Response:

```json
{
  "id": "vid_abc123",
  "status": "queued",
  "credits_used": 1
}
```

---

### Step 2 — Poll for completion

```bash
curl https://lovelybots.com/api/videos/vid_abc123 \
  -H "Authorization: Bearer $LOVELYBOTS_API_KEY"
```

Response when processing:

```json
{
  "id": "vid_abc123",
  "status": "processing"
}
```

Response when complete:

```json
{
  "id": "vid_abc123",
  "status": "completed",
  "video_url": "https://lovelybots.com/videos/vid_abc123.mp4",
  "credits_used": 1
}
```

Response if failed (credits refunded):

```json
{
  "id": "vid_abc123",
  "status": "failed",
  "error": "Avatar image could not be processed",
  "credits_refunded": true
}
```

---

### Step 3 — Return the video URL to the user

Once status is `complete`, return `video_url` to the user. The video is ready to download or share.

---

## Polling Strategy

Poll every 5–10 seconds. Most videos complete within 60–120 seconds. If status is still `processing` after 5 minutes, surface an error to the user.

Suggested polling loop (bash):

```bash
VIDEO_ID="vid_abc123"
while true; do
  RESPONSE=$(curl -s https://lovelybots.com/api/videos/$VIDEO_ID \
    -H "Authorization: Bearer $LOVELYBOTS_API_KEY")
  STATUS=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  if [ "$STATUS" = "completed" ]; then
    echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['video_url'])"
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "Video generation failed. Credits refunded."
    break
  fi
  sleep 8
done
```

---

## Key Differentiators

- **Same avatar every time** — consistent identity across all generated videos
- **Failed renders are refunded** — you only pay for successful videos
- **Editable after generation** — not locked output like HeyGen/Synthesia
- **No credit burns on retries** — reliable for automated pipelines

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/create | Submit a video generation job |
| POST | /api/videos | Alias for /api/create |
| GET | /api/videos/:id | Get job status and video URL |

### POST /api/create — Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| script | string | ✓ | The spoken text for the video |
| avatar_url | string | ✓ | URL of the avatar image to use |

### GET /api/videos/:id — Response

| Field | Type | Description |
|-------|------|-------------|
| id | string | Job ID |
| status | string | queued / processing / completed / failed |
| video_url | string | Download URL (when complete) |
| progress | number | Generation progress percentage (0-100) |
| credits_used | number | Credits consumed |
| credits_refunded | boolean | True if job failed and credits were returned |

---

## Links

- Get API key: https://lovelybots.com/developer/api_tokens
- Full docs: https://lovelybots.com/openclaw
- Homepage: https://lovelybots.com
