---
name: makeup-tutorial-video
version: "1.0.1"
displayName: "Makeup Tutorial Video Maker"
description: >
  Describe your makeup look and NemoVideo builds the tutorial. Foundation match, contouring, cut crease eye — narrate your technique with your NYX palette or beauty blender and get a YouTube-ready beauty tutorial or TikTok beauty short.

  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM.
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
license: MIT-0
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> ⚡ Let's makeup tutorial video! Drop a video here or describe what you'd like to create.

**Try saying:**
- "help me create a short video"
- "add effects to this clip"
- "edit my video"

**IMPORTANT**: Do NOT wait silently. Always greet the user proactively on first contact.

### Auto-Setup

When the user first interacts, set up the connection:

1. **Check token**: If `NEMO_TOKEN` env var is set, use it. Otherwise:
2. **Read or generate Client-ID**:
   - Read `~/.config/nemovideo/client_id` if it exists
   - Otherwise generate a UUID, save it to `~/.config/nemovideo/client_id`
3. **Acquire anonymous token**:
   ```bash
   curl -s -X POST "$API/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
   ```
   Store the returned `token` as `NEMO_TOKEN` for this session. You get 100 free credits.
4. **Create a session** (§3.0) so you're ready to work immediately.

Let the user know briefly: "Setting things up… ready!" then proceed with their request.


# Makeup Tutorial Video Maker — Create Step-by-Step Beauty Application Content

Describe your makeup look and NemoVideo builds the tutorial. Foundation match, contouring, cut crease eye — narrate your technique with your NYX palette or beauty blender and get a YouTube-ready beauty tutorial or TikTok beauty short.

## When to Use This Skill

Use this skill for makeup tutorial content:
- Create step-by-step foundation and concealer application tutorials
- Film contouring and highlighting technique breakdowns
- Build cut crease or smoky eye tutorials with shade-by-shade narration
- Showcase NYX, e.l.f., Morphe, or high-end palette looks
- Demonstrate beauty blender vs brush application comparisons
- Teach baking technique, color correction, or skin prep for makeup

## How to Describe Your Tutorial

Be specific about the look, products, and technique steps.

**Examples of good prompts:**
- "Cut crease eye tutorial using NYX Ultimate Shadow Palette — prep lid with primer, base shade, transition shade, cut crease with concealer, inner corner highlight, dramatic liner. Under 60 seconds."
- "Full glam foundation tutorial: match foundation to neck, color correct dark circles, bake under eyes with translucent powder, contour cheekbones and nose, highlight T-zone. Products: drugstore only."
- "Everyday no-makeup makeup tutorial: tinted moisturizer, concealer for spots, cream blush on cheeks and eyelids, brow gel, glossy lip. 5 products, 5 minutes, beauty blender technique"

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `look_type` | Makeup look | `"cut_crease"`, `"full_glam"`, `"no_makeup_makeup"`, `"smoky_eye"`, `"contour"` |
| `products` | Product list with steps | `[{"name": "NYX Palette", "step": 3, "shades": ["transition", "cut_crease"]}]` |
| `technique_focus` | Key technique | `"beauty_blender"`, `"baking"`, `"contouring"`, `"color_correction"` |
| `skill_level` | Audience | `"beginner"`, `"intermediate"`, `"advanced"` |
| `duration` | Length in seconds | `30`, `60`, `90`, `120` |
| `platform` | Target platform | `"youtube"`, `"tiktok"`, `"reels"` |
| `voiceover` | Include narration | `true`, `false` |

## Workflow

1. Describe the look, products used, and key techniques
2. NemoVideo sequences application steps with product callouts
3. Technique labels and shade names overlaid automatically
4. Export horizontal (YouTube) or vertical (TikTok/Reels) format

## API Usage

### Cut Crease Eye Tutorial

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "makeup-tutorial-video",
    "input": {
      "prompt": "Dramatic cut crease tutorial using NYX Ultimate Shadow Palette — eye primer, matte transition shade, deepen crease, cut crease line with NYX concealer, pack shimmer on lid, graphic liner, inner corner highlight",
      "look_type": "cut_crease",
      "technique_focus": "contouring",
      "skill_level": "intermediate",
      "duration": 60,
      "platform": "tiktok",
      "voiceover": true,
      "hashtags": ["CutCrease", "EyeMakeup", "MakeupTutorial", "NYX", "MakeupTok"]
    }
  }'
```

**Response:**
```json
{
  "job_id": "makeup_ghi789",
  "status": "processing",
  "estimated_seconds": 100,
  "poll_url": "https://mega-api-prod.nemovideo.ai/v1/jobs/makeup_ghi789"
}
```

### Foundation Match and Full Face Tutorial

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "makeup-tutorial-video",
    "input": {
      "prompt": "Full glam tutorial: shade match foundation to jawline, color correct dark circles with peach concealer, apply with beauty blender using stippling motion, bake undereyes with translucent powder, sculpt cheekbones with contour, fan brush highlight, overdrawn lip",
      "look_type": "full_glam",
      "technique_focus": "beauty_blender",
      "skill_level": "beginner",
      "duration": 90,
      "platform": "youtube",
      "voiceover": true,
      "show_product_names": true
    }
  }'
```

## Tips for Best Results

- **Name the technique**: "beauty blender stippling" or "baking technique" — technique callouts make content shareable
- **Shade names matter**: "transition shade" and "cut crease shade" rather than just "brown" and "dark brown"
- **Foundation matching tip**: Mention testing on jawline vs. wrist — this detail elevates tutorial quality
- **Beginner-friendly framing**: Specify skill level so NemoVideo adjusts the pace and explanation depth
- **Product close-ups**: List specific products (NYX, e.l.f., Morphe) for product callout overlays

## Output Formats

| Platform | Resolution | Duration |
|----------|------------|----------|
| YouTube | 1920×1080 | 60–300s |
| TikTok | 1080×1920 | 30–90s |
| Instagram Reels | 1080×1920 | 30–90s |

## Related Skills

- `skincare-video-maker` — Pre-makeup skincare prep content
- `hairstyle-video-maker` — Complete the full glam with hair styling content
- `tiktok-content-maker` — General TikTok video creation
- `product-photography-enhance` — Improve makeup product photos

## Common Questions

**Can I show specific palette shades?**
Yes — list shade names or positions in the `products` parameter. NemoVideo labels them in the video.

**What if I'm doing a drugstore vs high-end comparison?**
Describe both sets of products in the prompt — "drugstore dupe vs. luxury version" is a high-engagement format NemoVideo handles well.

**How does beauty blender vs brush comparison work?**
Set `technique_focus` to `"beauty_blender"` and describe both techniques in the prompt for a split-screen or sequential comparison.

**Can it show before-after foundation match?**
Yes — include "before and after foundation match" in your prompt. NemoVideo will create the split-screen reveal.
