# TikTok Video Maker — OpenClaw Skill

Generate avatar videos from any script using the [LovelyBots API](https://lovelybots.com/openclaw).

POST a script and avatar image → GET a finished video URL. Token-authenticated, poll-based, works in any agent pipeline.

## What It Does

- Queues video generation jobs via the LovelyBots API
- Polls for completion automatically
- Returns a direct video download URL
- Reports credit usage per video
- Refunds credits on failed renders

## Requirements

- A LovelyBots API key — get one at [lovelybots.com/api](https://lovelybots.com/api)
- `curl` available in your environment

## Install

```bash
openclaw skills install tiktok-video-maker
```

Then add your API key to openclaw.json:

```json
{
  "skills": {
    "entries": {
      "tiktok-video-maker": {
        "env": {
          "LOVELYBOTS_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

## Example Usage

> "Generate a TikTok ad video using avatar at [url] with this script: [text]"

> "Create a video with my avatar and queue it for me — I'll give you the script"

> "Make a 30-second product video using LovelyBots"

## Why LovelyBots

Most AI video tools burn credits on failed renders and produce inconsistent avatars. LovelyBots refunds failed jobs and uses the same avatar every time — which matters when you're generating at scale inside an agent pipeline.

## Links

- [Get API Key](https://lovelybots.com/api)
- [Full API Docs](https://lovelybots.com/openclaw)
- [LovelyBots Homepage](https://lovelybots.com)
