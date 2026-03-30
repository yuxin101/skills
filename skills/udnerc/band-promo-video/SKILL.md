---
name: band-promo-video
version: "1.0.1"
displayName: "Band Promo Video Maker"
description: >
  Describe your band and NemoVideo creates the promo video. Debut single release, tour announcement, label signing, new lineup reveal — narrate who you are as an artist, what your music sounds like, and why people should care, and get a band promo video for your EPK, Spotify for Artists profile, and booking pitches.

  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM.
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
license: MIT-0
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> ⚡ Let's band promo video! Drop a video here or describe what you'd like to create.

**Try saying:**
- "add effects to this clip"
- "edit my video"
- "help me create a short video"

**IMPORTANT**: Always greet the user proactively on first contact. Let them know you're setting up while connecting. Always greet the user proactively on first contact.

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


# Band Promo Video Maker — Create Artist Promotional and EPK Video Content

Describe your band and NemoVideo creates the promo video. Debut single release, tour announcement, label signing, new lineup reveal — narrate who you are as an artist, what your music sounds like, and why people should care, and get a band promo video for your EPK, Spotify for Artists profile, and booking pitches.

## When to Use This Skill

Use this skill for band and artist promotional content:
- Create Electronic Press Kit (EPK) videos for booking and PR pitches
- Film artist introduction videos for new audiences discovering the band
- Build tour announcement and show promotion content
- Document new member or lineup change announcement videos
- Create label signing and major milestone announcement content
- Produce music video "making of" and behind-the-scenes content

## How to Describe Your Band Promo

Be specific about your sound, your story, your visual aesthetic, and what you want promoters, labels, and fans to know.

**Examples of good prompts:**
- "EPK video for a 4-piece indie rock band: The Levee Kings. Sound reference: National meets Japandroids — big guitars, earnest lyrics, anthemic choruses. We formed in 2021, released 2 EPs, just signed to a small Midwest label, about to record our debut album. Show the band together (we look like a proper band, not four people who just met), live footage from our best show (The Empty Bottle Chicago, 300 people), and the recording studio session. 3 minutes, for venue booking."
- "Solo artist promo for singer-songwriter Wren Calloway: bedroom pop with orchestral production. 25 years old, she records everything herself in her apartment, does her own mixing, recently went viral on TikTok with a demo. Show her in her recording setup, her playing live at a small show, the contrast between the intimate recording space and how the music sounds fully produced. The story is: this huge sound from this tiny room."
- "Metal band tour announcement: Dread Protocol, touring in support of our second album. Dates: 15 cities over 3 weeks, co-headlining with regional acts. Show the band in their element — sweaty venue, heavy stage production, the pit. The announcement should feel like a threat, not an invitation."

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `content_type` | Promo purpose | `"epk"`, `"tour_announcement"`, `"single_release"`, `"label_signing"`, `"artist_intro"` |
| `artist_name` | Band or artist name | `"The Levee Kings"`, `"Wren Calloway"` |
| `genre` | Music style | `"indie rock"`, `"bedroom pop"`, `"metal"`, `"jazz"` |
| `sound_reference` | Comparison artists | `"National meets Japandroids"` |
| `key_elements` | Must include | `["live footage", "studio session", "band together"]` |
| `target_audience` | Who sees this | `"venue bookers"`, `"fans"`, `"labels"`, `"press"` |
| `tone` | Promo energy | `"anthemic"`, `"intimate"`, `"intimidating"`, `"cinematic"` |
| `duration_minutes` | Video length | `2`, `3`, `5` |
| `platform` | Distribution | `"epk_email"`, `"youtube"`, `"instagram"`, `"spotify"` |

## Workflow

1. Describe the band, their sound, their story, and what this promo is for
2. NemoVideo structures the promotional narrative for the target audience (EPK vs fan announcement vs press)
3. Band name, genre tags, booking contact, and key achievements overlaid automatically
4. Export in formats suited for industry pitching and fan distribution

## API Usage

### EPK Video for Booking

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "band-promo-video",
    "input": {
      "prompt": "EPK video for experimental jazz trio The Meridian Collective for venue booking and festival pitching: Three musicians (piano, upright bass, drums), based in Chicago. Sound: structured improvisation, somewhere between ECM jazz and post-rock. Last 18 months: released one album (physical vinyl, 400 copies sold out in 3 days), played 22 shows including 3 festivals. Best credential: opened for a nationally recognized jazz act at the Chicago Jazz Fest side stage. Looking for venues in the 200-500 capacity range and regional festival bookings. Show the trio playing together (tight chemistry), the performance energy, and 2 press quotes if included.",
      "content_type": "epk",
      "artist_name": "The Meridian Collective",
      "genre": "experimental jazz",
      "target_audience": "venue bookers and festival programmers",
      "key_elements": ["live performance", "trio chemistry", "achievement highlights"],
      "tone": "cinematic",
      "duration_minutes": 3,
      "platform": "epk_email",
      "hashtags": ["Jazz", "ExperimentalJazz", "LiveMusic", "ChicagoJazz", "EPK"]
    }
  }'
```

**Response:**
```json
{
  "job_id": "bandpromo_jkl012",
  "status": "processing",
  "estimated_seconds": 105,
  "poll_url": "https://mega-api-prod.nemovideo.ai/v1/jobs/bandpromo_jkl012"
}
```

### Tour Announcement Video

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "band-promo-video",
    "input": {
      "prompt": "Tour announcement for post-hardcore band Fault Lines: Spring tour, 12 dates, East Coast to Midwest. Co-headlining with regional acts we actually like. We have been away for 18 months recording and we are coming back loud. Show: the band in the practice space (sweaty, loud, together), live clips from the last tour that show the room energy, and the tour date cards. The announcement should communicate that we have been working on something and this is the first sign of it. Not polished. Real.",
      "content_type": "tour_announcement",
      "artist_name": "Fault Lines",
      "genre": "post-hardcore",
      "tone": "anthemic",
      "duration_minutes": 2,
      "platform": "instagram"
    }
  }'
```

## Tips for Best Results

- **EPK vs fan content are different videos**: EPKs are for industry (bookers, labels, press) — lead with credentials and sound description. Fan promo is for people who already know you — lead with energy and excitement
- **Sound references do the heavy lifting**: "National meets Japandroids" or "ECM jazz and post-rock" tells a booker instantly whether you're right for their venue — include your sound references
- **Live footage is non-negotiable for EPKs**: "Show the band at their best show" — no live footage in an EPK is an automatic skip from most bookers
- **Target audience changes the edit**: "For venue booking" is a different tone than "for fans" — set `target_audience` explicitly
- **Achievements > aspirations**: "200 copies sold out in 3 days" is more compelling than "we hope to release vinyl" — lead with what's real

## Output Formats

| Platform | Resolution | Duration |
|----------|------------|----------|
| EPK email | 1920×1080 | 2–4 min |
| YouTube | 1920×1080 | 2–5 min |
| Instagram | 1080×1920 | 60–90s |
| Spotify for Artists | 1920×1080 | 3–5 min |

## Related Skills

- `concert-video-maker` — Live show documentation
- `live-performance-video` — Performance-focused content
- `music-lyric-video` — Song-specific promotional content
- `cover-song-video` — Cover content to build audience

## Common Questions

**What should an EPK video include?**
Live performance footage, the band together (chemistry matters), key achievements (shows played, releases, notable credits), and the sound — ideally a 30-second clip of your best track under the visuals. 3 minutes maximum for EPKs.

**Should I create different versions for different audiences?**
Yes — set `target_audience` for each version. The venue booking EPK emphasizes live energy and past shows; the label pitch emphasizes sound and songwriting; the fan tour announcement is pure excitement.

**What's the minimum I need for an EPK video?**
Live footage from one good show + one interview or "behind the scenes" moment + the key achievement to date. Describe these three things and NemoVideo builds a compelling EPK from them.
