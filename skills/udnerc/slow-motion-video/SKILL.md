---
name: slow-motion-video
version: 1.0.4
displayName: "Slow Motion Video — Create Slow Motion and Speed Ramp Effects with AI"
description: >
  Slow Motion Video — Create Slow Motion and Speed Ramp Effects with AI.
  Frame-accurate speed control through conversation. Upload your video and describe where you want time to slow down or ramp: 'slow down to 0.25x right when the ball hits' or 'speed ramp from normal to 50% at the 8-second mark.' The AI handles precise frame-level speed adjustments, smooth velocity curves, and multi-point ramping in a single clip. Works for sports highlight reels, dance videos, action sequences, product reveals, and any footage where timing is part of the story. Combine speed effects with color grading, music, and text overlays in the same session. No keyframe animation knowledge needed — describe the effect, get the output. Preserves original resolution. Export as MP4. Supports mp4, mov, avi, webm, mkv.
  
  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM. Free trial available.
metadata: {"openclaw": {"emoji": "🎬"}}
license: MIT-0
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
metadata:
  requires:
    env: []
    configPaths:
      - "~/.config/nemovideo/"
  primaryEnv: NEMO_TOKEN
---

# Slow Motion Video — Create Slow Motion and Speed Ramp Effects with AI

Create slow-motion and speed effects. Add dramatic slow-mo and speed ramps through chat.

## Quick Start
Ask the agent to apply slow motion or speed effects to your video.

## What You Can Do
- Create smooth slow-motion effects from regular footage
- Add speed ramp transitions (fast to slow, slow to fast)
- Apply variable speed effects to specific sections
- Generate freeze frame moments
- Combine multiple speed effects in one video

## API
Uses NemoVideo API (mega-api-prod.nemovideo.ai) for all video processing.
