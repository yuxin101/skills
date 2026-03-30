---
name: video-splitter
version: "1.0.0"
displayName: "Video Splitter — Split Long Videos into Clips Scenes and Segments Automatically"
description: >
  Split long videos into clips, scenes, and segments automatically with AI — detect scene changes, topic shifts, silence gaps, and speaker turns to divide any video into individual files. NemoVideo analyzes video structure and splits intelligently: podcast episodes into topic clips, lectures into lesson modules, meetings into agenda items, streams into highlight segments, and interviews into individual Q&A pairs. Upload one long video and download multiple ready-to-use segments. Split video online, divide video into parts, cut video into clips, scene detection, video chapter splitter, segment video automatically.
metadata: {"openclaw": {"emoji": "✂️", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Video Splitter — One Long Video Becomes Twenty Pieces of Content

Every long video is a container holding multiple shorter videos. A 60-minute podcast contains 8-12 standalone topic discussions — each one a potential clip for social media, a blog post, or a newsletter segment. A 90-minute lecture contains 6-10 teaching modules — each one a lesson in an online course. A 3-hour live stream contains dozens of highlight moments — each one a TikTok, a Shorts, or a Twitch clip. The content already exists inside the long video. The work is extraction. Manual extraction means: watching the entire video start to finish, writing down every timestamp where a new segment begins, opening editing software, setting in-points and out-points for each segment, exporting each one individually, and naming and organizing the files. For a 60-minute video split into 10 segments, this process takes 2-3 hours. For a library of 50 videos, it takes a week. NemoVideo automates the entire extraction pipeline. The AI watches the video once, identifies every natural split point — topic changes in conversation, scene transitions in footage, silence gaps between sections, speaker turns in interviews — and exports each segment as a separate file with automatic titles, consistent formatting, and clean transitions at every cut point.

## Use Cases

1. **Podcast Repurposing — Topics to Clips (any length)** — A weekly podcast runs 45-75 minutes per episode. The host wants each topic discussed as a standalone clip for YouTube, LinkedIn, and TikTok. NemoVideo: transcribes the full episode, identifies 8-10 topic transitions from conversational cues ("Speaking of...", "Let's talk about...", natural subject shifts), splits at each transition with 0.5-second audio crossfade, titles each segment from the topic discussed ("Why Remote Work Is Failing — with Sarah Chen"), exports full-length segments (3-8 min each) for YouTube AND extracts the single best 45-second moment from each segment as a vertical TikTok clip. One episode becomes 8 YouTube videos and 8 TikTok clips.
2. **Online Course — Lectures to Modules (30-120 min)** — A professor recorded a 90-minute lecture for an online learning platform that requires videos under 15 minutes. NemoVideo: detects the lecture's natural structure (introduction → concept 1 → example → concept 2 → example → summary), identifies slide transitions and verbal cues ("Next, we will examine..."), splits into 7 modules aligned with the pedagogical structure, adds title cards to each module ("Module 4: Market Equilibrium — 11:42"), numbers them sequentially, and exports with consistent formatting. A single recording becomes a structured course.
3. **Meeting Recording — Agenda Items (30-90 min)** — A 60-minute team meeting was recorded and stakeholders only care about specific agenda items. NemoVideo: identifies speaker transitions and topic shifts, maps the recording to the meeting agenda (provided as text or detected from conversation), splits into individual agenda segments ("Q3 Budget Review — 12:34", "Product Launch Timeline — 08:22", "Open Discussion — 15:48"), and exports each as a separate file. Stakeholders watch only their relevant segment instead of scrubbing through the full recording.
4. **YouTube Chapters — Auto-Generated Timestamps (any length)** — A 25-minute YouTube video needs chapter timestamps for the description. NemoVideo: analyzes the video for topic structure, generates chapter markers at each transition, provides the timestamp list formatted for YouTube description copy-paste, AND optionally splits the video at chapter boundaries for individual segment downloads. Even without splitting, the chapter detection alone saves 30 minutes of manual timestamp creation.
5. **Content Library — Batch Processing (multiple videos)** — A media company has 200 hours of interview footage archived without segmentation. NemoVideo: batch-processes the entire library, splits each interview into individual Q&A segments, titles each with the question asked, tags with speaker names, and organizes into a searchable catalog. Two hundred hours of unsearchable footage becomes a categorized content database of 2,000+ individual clips.

## How It Works

### Step 1 — Upload Video
Any long video: podcast, lecture, meeting, stream, interview, event recording. Any length — NemoVideo handles multi-hour files.

### Step 2 — Choose Split Method
Topic-based (AI detects subject changes), scene-based (visual transitions), silence-based (pauses between sections), speaker-based (who is talking), duration-based (equal chunks), or custom timestamps.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "video-splitter",
    "prompt": "Split a 55-minute podcast into individual topic segments. Detect topic transitions from conversation flow. Title each segment with the topic discussed. Add 0.5s audio crossfade at each split. Also extract the best 45-second moment from each segment as a 9:16 TikTok clip with word-by-word captions (white text, #FF6B6B highlight, dark pill bg). Export all segments as MP4.",
    "split_method": "topic",
    "crossfade": 0.5,
    "auto_title": true,
    "short_clips": {
      "per_segment": 1,
      "duration": "45 sec",
      "format": "9:16",
      "captions": {"style": "word-highlight", "text": "#FFFFFF", "highlight": "#FF6B6B", "bg": "pill-dark"}
    },
    "output_format": "mp4",
    "naming": "sequential-with-title"
  }'
```

### Step 4 — Review and Distribute
Preview each segment: verify split points land on natural pauses, titles match content, no audio cut mid-sentence. Download all segments and clips. Distribute across platforms.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Video description and split requirements |
| `split_method` | string | | "topic", "scene", "silence", "speaker", "duration", "timestamps" |
| `split_duration` | string | | For duration method: "5 min", "10 min", "15 min" |
| `timestamps` | array | | Manual split points: ["5:30", "12:15", "28:00"] |
| `crossfade` | float | | Seconds of crossfade at cuts (default: 0) |
| `auto_title` | boolean | | AI-generated titles per segment |
| `short_clips` | object | | {per_segment, duration, format, captions} |
| `output_format` | string | | "mp4", "mov", "mkv" |
| `naming` | string | | "sequential", "sequential-with-title", "title-only" |
| `chapters_only` | boolean | | Output timestamps without splitting |
| `batch` | array | | Multiple videos for batch splitting |

## Output Example

```json
{
  "job_id": "vs-20260328-002",
  "status": "completed",
  "source_duration": "55:08",
  "split_method": "topic",
  "segments": [
    {"file": "01-intro-and-background.mp4", "duration": "3:44", "start": "0:00"},
    {"file": "02-why-ai-wont-replace-developers.mp4", "duration": "8:12", "start": "3:44"},
    {"file": "03-the-real-threat-to-junior-devs.mp4", "duration": "7:55", "start": "11:56"},
    {"file": "04-how-to-stay-relevant.mp4", "duration": "9:18", "start": "19:51"},
    {"file": "05-building-a-personal-brand.mp4", "duration": "6:42", "start": "29:09"},
    {"file": "06-freelance-vs-employment-2026.mp4", "duration": "8:30", "start": "35:51"},
    {"file": "07-rapid-fire-predictions.mp4", "duration": "5:22", "start": "44:21"},
    {"file": "08-closing-and-resources.mp4", "duration": "5:25", "start": "49:43"}
  ],
  "tiktok_clips": 8,
  "total_segments": 8
}
```

## Tips

1. **Topic-based splitting produces the highest-value segments** — Each segment stands alone as a complete discussion. Viewers can find and watch exactly the topic they care about. Individual topic clips consistently outperform timestamped full-length videos for engagement.
2. **Always use crossfade at split points** — Even when the AI picks a perfect split point on a silence gap, a 0.3-0.5 second crossfade ensures the audio transition is inaudible. Hard cuts at split points can create audible pops or jarring transitions.
3. **Extract short clips from each segment for 2x content output** — Splitting a podcast into 8 topic segments is valuable. Extracting a 45-second TikTok clip from each segment doubles the output to 16 pieces of content from one recording.
4. **Auto-titling makes segments immediately usable** — Manually titling 8-10 segments requires re-listening to each one. AI titles based on transcript analysis produce accurate, descriptive titles in zero time — ready for YouTube or file organization.
5. **Batch processing unlocks catalog-scale repurposing** — 100 podcast episodes × 8 segments = 800 topic clips + 800 TikTok shorts = 1,600 pieces of content from existing recordings. The content already exists; splitting unlocks it.

## Output Formats

| Format | Content | Use Case |
|--------|---------|----------|
| MP4 16:9 | Individual segments | YouTube / website |
| MP4 9:16 | Short clips per segment | TikTok / Reels / Shorts |
| JSON | Segment metadata + timestamps | CMS integration / YouTube chapters |
| SRT | Per-segment subtitles | Accessibility |

## Related Skills

- [video-reverser](/skills/video-reverser) — Reverse video effects
- [instagram-reels-editor](/skills/instagram-reels-editor) — Reels editing
- [reels-creator](/skills/reels-creator) — Reels creation
