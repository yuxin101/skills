---
name: explainer-video-maker
version: "1.0.0"
displayName: "Explainer Video Maker — Create Animated Explainer Videos with AI from Script"
description: >
  Create animated explainer videos using AI — turn scripts, product descriptions, and complex ideas into clear, engaging animated videos with voiceover narration, visual metaphors, animated diagrams, character animations, and professional motion graphics. NemoVideo produces the explainer videos that startups use on landing pages, SaaS companies use for onboarding, educators use for lesson delivery, and marketers use for product launches — all generated from text without animation software, designers, or production budgets.
metadata: {"openclaw": {"emoji": "💡", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Explainer Video Maker — Animated Explainers from Script to Screen

Explainer videos are the most effective content format for converting confusion into understanding — and understanding into action. A 90-second animated explainer on a landing page increases conversion rates by 20-80% (depending on the product's complexity). A 3-minute explainer in an onboarding flow reduces support tickets by 40%. A 5-minute educational explainer gets shared 3x more than a text article covering the same topic. The reason is cognitive: animation can show abstract concepts that cameras cannot film. How does cloud computing work? You can't film "the cloud." But you can animate data flowing between servers, scaling up during traffic spikes, and distributing across regions — making the invisible visible. The barrier to explainer videos has always been production cost. A professional 90-second animated explainer costs $5,000-$15,000: scriptwriting ($500-1,000), storyboarding ($500-1,500), animation ($3,000-8,000), voiceover ($200-500), and music/sound design ($300-500). Timeline: 3-6 weeks. NemoVideo generates explainer videos from a script in minutes. Write what you want explained, describe the visual approach, and the AI produces: animated scenes matching each concept, voiceover narration with appropriate tone, visual metaphors for abstract ideas, smooth transitions between topics, and professional motion graphics — at a fraction of the cost and time.

## Use Cases

1. **SaaS Product — Landing Page Explainer (60-90s)** — A project management tool needs a landing page video. NemoVideo produces: Problem scene (overwhelmed team, missed deadlines, scattered communication — animated with frustrated character and flying notifications), Solution scene (clean dashboard, organized tasks, team collaboration — animated with smooth UI mockup transitions), Benefits (3 key benefits as animated icons with counter statistics: "Save 5 hours/week"), and CTA ("Start free at teamflow.ai"). Voiceover: confident, friendly female. Music: upbeat corporate at -18dB. Animation style: modern flat design with brand colors.
2. **Educational — Complex Concept (3-8 min)** — "How does photosynthesis work?" for middle school students. NemoVideo creates: animated plant cross-section showing sunlight entering leaves, chlorophyll molecules animated as green energy collectors, water molecules traveling up from roots, CO2 entering through stomata, glucose molecules being assembled step-by-step, and oxygen released as bubbles. Narration: friendly, patient voice with age-appropriate vocabulary. Each concept builds on the previous one with smooth transitions and recap checkpoints.
3. **Startup Pitch — Investor Deck Companion (2-3 min)** — A startup's pitch deck needs a video version for async investor review. NemoVideo produces: market problem (animated market size charts, frustrated user personas), solution (product demo animation with key features), traction (animated growth chart, customer logos), team (brief animated bios), and ask (investment terms, use of funds as animated pie chart). Narration: authoritative yet passionate founder voice. The pitch deck becomes a standalone watchable narrative.
4. **Internal Training — Process Explanation (3-5 min)** — A new employee onboarding module explaining the expense reporting process. NemoVideo creates: step-by-step animated workflow (submit receipt → manager approval → finance review → reimbursement), decision trees animated at approval/rejection points, timeline expectations animated on a calendar, and common mistakes shown with animated "wrong way / right way" comparisons. Clear, patient narration with no jargon.
5. **Healthcare — Patient Education (2-4 min)** — A hospital needs to explain a surgical procedure to patients. NemoVideo generates: simplified animated anatomy showing the relevant area, step-by-step procedure animation (gentle, non-graphic), recovery timeline with animated milestones, expected outcomes shown as before/after animations, and a FAQ section addressing common concerns. Narration: calm, reassuring medical professional voice. Animations: clean, medical-illustration style — informative without being alarming.

## How It Works

### Step 1 — Provide Script or Topic
Write the full script or describe the topic. NemoVideo develops the visual concept, scene breakdown, and animation approach based on the content.

### Step 2 — Choose Animation Style
Select: modern flat design, whiteboard animation, 3D isometric, character-driven, infographic, or custom. Set brand colors, voiceover character, and music mood.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "explainer-video-maker",
    "prompt": "Create a 90-second explainer video for a SaaS project management tool. Structure: Problem (teams drowning in notifications, missed deadlines, scattered tools) → Solution (one dashboard, smart task prioritization, integrated communication) → Benefits (save 5 hours/week, 40%% fewer meetings, 92%% team satisfaction) → CTA (Start free at teamflow.ai). Animation: modern flat design, brand colors blue (#2563EB) and white. Voice: friendly confident female. Music: upbeat corporate at -18dB. Include animated UI mockups and counter statistics.",
    "animation_style": "modern-flat",
    "brand_colors": ["#2563EB", "#FFFFFF"],
    "voice": "friendly-confident-female",
    "music": "upbeat-corporate",
    "music_volume": "-18dB",
    "duration": "90 sec",
    "format": "16:9"
  }'
```

### Step 4 — Review Scenes and Export
Preview each scene. Adjust animations, voiceover timing, or color palette. Export for landing page, social media, or presentation.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Script/topic and visual requirements |
| `animation_style` | string | | "modern-flat", "whiteboard", "3d-isometric", "character-driven", "infographic" |
| `brand_colors` | array | | Hex colors for brand consistency |
| `voice` | string | | "friendly-female", "authoritative-male", "warm", "energetic" |
| `music` | string | | "upbeat-corporate", "cinematic", "playful", "minimal" |
| `music_volume` | string | | "-14dB" to "-22dB" (default: "-18dB") |
| `duration` | string | | "60 sec", "90 sec", "3 min", "5 min" |
| `characters` | boolean | | Include animated character personas (default: true) |
| `subtitles` | string | | "burned-in", "srt", "none" |
| `format` | string | | "16:9", "9:16", "1:1" |

## Output Example

```json
{
  "job_id": "evm-20260328-001",
  "status": "completed",
  "duration_seconds": 88,
  "scenes": 4,
  "format": "mp4",
  "resolution": "1920x1080",
  "file_size_mb": 22.6,
  "output_url": "https://mega-api-prod.nemovideo.ai/output/evm-20260328-001.mp4",
  "production": {
    "animation_style": "modern-flat (blue #2563EB + white)",
    "voice": "friendly-confident-female (en)",
    "music": "upbeat-corporate at -18dB",
    "scenes": ["Problem (0:00-0:25)", "Solution (0:25-0:50)", "Benefits (0:50-1:12)", "CTA (1:12-1:28)"],
    "animations": "UI mockups, counter statistics, character personas, icon transitions"
  }
}
```

## Tips

1. **90 seconds is the landing page sweet spot** — Shorter than 60 seconds feels incomplete for a product explanation. Longer than 2 minutes loses website visitor attention. 75-90 seconds delivers the full Problem → Solution → Benefit → CTA arc.
2. **Problem-first structure builds empathy** — Start with the pain the viewer feels before introducing the solution. "Drowning in notifications?" creates emotional agreement before "Our dashboard fixes this" offers relief.
3. **Animated statistics are more believable** — A counter animating from 0 to "40% fewer meetings" is more credible and memorable than static text. Animation implies data; static text implies claims.
4. **Brand colors in animation create subliminal recognition** — Using exact brand hex colors throughout the explainer means every frame reinforces brand identity. The viewer associates the positive explainer experience with the brand's visual language.
5. **Voiceover pace should match content complexity** — Simple benefits: 160 wpm. Technical explanation: 130 wpm. The voice should slow down when the concept is hard and speed up when it's intuitive.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | Landing page / YouTube / presentation |
| MP4 9:16 | 1080x1920 | Social media / TikTok ad |
| MP4 1:1 | 1080x1080 | Instagram / LinkedIn feed |
| GIF | 720p | Email embed / preview |

## Related Skills

- [youtube-shorts-maker](/skills/youtube-shorts-maker) — YouTube Shorts
- [youtube-script-writer](/skills/youtube-script-writer) — Script writing
- [talking-head-video](/skills/talking-head-video) — Talking head editing
