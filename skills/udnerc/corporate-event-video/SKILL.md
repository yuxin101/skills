---
name: corporate-event-video
version: "1.0.1"
displayName: "Corporate Event Video Maker"
description: >
  Describe your event and NemoVideo creates the video. Annual conferences, product launches, team retreats, award ceremonies, company milestones — narrate the event and get corporate event content for internal communication, social media, and sponsor reporting.

  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM.
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
license: MIT-0
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> 📹 Welcome! I can corporate event video for you. Share a video file or tell me your idea!

**Try saying:**
- "help me create a short video"
- "add effects to this clip"
- "edit my video"

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


# Corporate Event Video Maker — Create Conference and Company Event Documentation

Describe your event and NemoVideo creates the video. Annual conferences, product launches, team retreats, award ceremonies, company milestones — narrate the event and get corporate event content for internal communication, social media, and sponsor reporting.

## When to Use This Skill

Use this skill for corporate and professional event content:
- Create conference and summit recap videos for attendee follow-up and marketing
- Film keynote and speaker highlight content for post-event distribution
- Build award ceremony and recognition event documentation
- Document company all-hands and milestone celebration content
- Create event promotional content for next year's registration campaign
- Produce sponsor deliverable videos showing brand exposure at events

## How to Describe Your Event

Be specific about the event type, scale, key speakers or moments, and what the video is meant to accomplish.

**Examples of good prompts:**
- "Annual user conference recap for a SaaS company: 800 attendees, 2 days, San Francisco. Day 1 highlights: CEO keynote (big product announcement — new AI features), the customer panel where a customer's case study went viral (standing ovation), networking happy hour on the rooftop. Day 2: 6 breakout sessions, the product demo hall, closing keynote. Overall feeling: this was the year the company stopped apologizing for ambition. Video is for post-event email to all attendees."
- "Company 10th anniversary gala: 200 employees, black tie, ballroom. The CEO and co-founder told the story of starting the company in a garage in 2015. Showed photos from year one alongside current office. The employee who has been there from day 1 gave a speech that made the CEO cry. Awards for the top performers. This video is for internal sharing and LinkedIn."
- "Product launch event for B2B software: 150 prospects and customers, intimate theater, Manhattan. The product reveal was a live demo where the software found a real customer error in real time (unscripted, the founder found it by accident and it was the best possible demo). Speakers: 3 customer testimonials and the founder. For LinkedIn and sales enablement."

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `event_type` | Event category | `"conference"`, `"summit"`, `"gala"`, `"product_launch"`, `"all_hands"`, `"retreat"` |
| `company_name` | Organization | `"Relay Inc."` |
| `event_name` | Event title | `"Forward Summit 2026"` |
| `attendee_count` | Scale | `"150"`, `"800"`, `"2000"` |
| `key_moments` | Highlights | `["product announcement", "customer case study", "founder speech"]` |
| `purpose` | Video use | `"attendee_followup"`, `"social_media"`, `"sponsor_report"`, `"internal"` |
| `show_speakers` | Speaker highlights | `true` |
| `show_audience` | Attendee reactions | `true` |
| `tone` | Production register | `"corporate_polished"`, `"energetic"`, `"intimate"`, `"documentary"` |
| `duration_minutes` | Video length | `2`, `3`, `5`, `8` |
| `platform` | Distribution | `"linkedin"`, `"youtube"`, `"email"`, `"internal_portal"` |

## Workflow

1. Describe the event, highlights, and video purpose
2. NemoVideo structures the corporate event narrative (arrival → keynote → peak moment → close)
3. Company name, event branding, speaker labels, and sponsor logos added automatically
4. Export in formats for the specific distribution channel

## API Usage

### Conference Recap Video

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "corporate-event-video",
    "input": {
      "prompt": "Annual design conference recap — Design Forward 2026: 600 attendees, 2 days, Chicago. Key moments: Opening keynote by the founder of a major design system (450 people silent for 45 minutes), the workshop session where designers worked on a real client brief live, the awards dinner where the best work of the year was recognized, and the candid hallway conversations where the real connections happened. The energy of this conference is 'serious people taking craft seriously' — not hype, not party, not startup energy. Thoughtful. Video is for post-event email and next year's registration campaign.",
      "event_type": "conference",
      "event_name": "Design Forward 2026",
      "attendee_count": "600",
      "key_moments": ["keynote silence", "live workshop", "awards dinner", "hallway networking"],
      "purpose": "attendee_followup",
      "show_speakers": true,
      "show_audience": true,
      "tone": "documentary",
      "duration_minutes": 3,
      "platform": "email",
      "hashtags": ["DesignForward", "DesignConference", "EventRecap", "B2B"]
    }
  }'
```

**Response:**
```json
{
  "job_id": "corp_def456",
  "status": "processing",
  "estimated_seconds": 110,
  "poll_url": "https://mega-api-prod.nemovideo.ai/v1/jobs/corp_def456"
}
```

### Company Milestone Gala Video

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "corporate-event-video",
    "input": {
      "prompt": "Company 15-year anniversary celebration: 180 employees, black tie dinner, Chicago rooftop. The highlight was a founder speech where she walked through the company history using actual photos and emails from year 1 — the first customer email (embarrassingly bad product pitch), the first hire (now the CTO), the moment they almost ran out of money (month 11, a wire transfer arrived with 4 hours to spare). Three employees who have been there 10+ years each gave 90-second toasts. For LinkedIn and internal sharing. Should feel proud, not corporate.",
      "event_type": "gala",
      "attendee_count": "180",
      "key_moments": ["founder history speech", "year-1 photos", "long-tenure toasts"],
      "purpose": "social_media",
      "tone": "intimate",
      "duration_minutes": 3,
      "platform": "linkedin"
    }
  }'
```

## Tips for Best Results

- **Purpose first**: "For post-event email to attendees" vs "for next year's registration campaign" vs "for sponsor report" — these are different videos with different content priorities, set `purpose` explicitly
- **The unscripted moment beats the planned one**: "The software found a real customer error in real time (unscripted)" is better than any planned demo — describe the unexpected moments that actually happened
- **Speaker names and titles matter**: Include speaker names and roles for keynotes and panels — attendees watch recap videos to share with colleagues who missed it
- **Sponsor placement is a deliverable**: If sponsors need footage of their logo/branding in the video, include `include_sponsors: true` and describe the placement context
- **Company culture shows in the event**: "Serious people taking craft seriously" or "stopped apologizing for ambition" — describe the company's energy and NemoVideo matches the editorial tone

## Output Formats

| Platform | Resolution | Duration |
|----------|------------|----------|
| LinkedIn | 1920×1080 | 2–3 min |
| Email embed | 1920×1080 | 2–3 min |
| YouTube | 1920×1080 | 3–8 min |
| Internal portal | 1920×1080 | 5–15 min |

## Related Skills

- `product-launch-video` — Product-focused launch event content
- `company-culture-video` — Culture content for recruiting and LinkedIn
- `startup-pitch-video` — Investor-facing company content
- `live-performance-video` — Entertainment documentation at corporate events

## Common Questions

**Can I create sponsor deliverable videos from the same footage as the recap?**
Yes — describe the sponsor's branding moments (logo placement, branded stage, sponsor booth) separately and NemoVideo creates a sponsor-specific cut alongside the general recap.

**What length works for LinkedIn video?**
2-3 minutes maximum. LinkedIn viewers want the energy and key moments — not a full documentary. Include the most impressive moment in the first 20 seconds.

**How do I include speaker content without filming a traditional talking-head interview?**
Describe the candid hallway conversations, the live workshop moments, or the Q&A exchanges — NemoVideo incorporates natural speaker content rather than staged interview clips.
