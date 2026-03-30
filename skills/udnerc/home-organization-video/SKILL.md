---
name: home-organization-video
version: "1.0.1"
displayName: "Home Organization Video Maker"
description: >
  Describe your organization project and NemoVideo creates the video. Pantry overhauls, closet systems, garage transformations, whole-home declutters, container organization — narrate the chaos before, the decisions made, the systems built, and the calm after, and get home organization content that serves the massive audience looking for practical order in their living spaces.

  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM.
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
license: MIT-0
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> 🚀 Ready to home organization video! Just send me a video or describe your project.

**Try saying:**
- "edit my video"
- "help me create a short video"
- "add effects to this clip"

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


# Home Organization Video Maker — Create Declutter, Storage, and Systems Content

Describe your organization project and NemoVideo creates the video. Pantry overhauls, closet systems, garage transformations, whole-home declutters, container organization — narrate the chaos before, the decisions made, the systems built, and the calm after, and get home organization content that serves the massive audience looking for practical order in their living spaces.

## When to Use This Skill

Use this skill for home organization and decluttering content:
- Create room organization transformation videos showing before/after systems
- Film decluttering walkthroughs using specific methods (KonMari, Swedish death cleaning, 20/20 rule)
- Build pantry, closet, and cabinet organization tutorial content
- Document whole-home declutter projects over weeks or months
- Create "organize with me" real-time companion content
- Produce minimalism and intentional living content

## How to Describe Your Organization Project

Be specific about the space, the problem, the decision framework used, the products (if any), and the final system.

**Examples of good prompts:**
- "Pantry overhaul — from embarrassing to functional: Before: things falling out when you open the door, expired food from 2023, duplicates of things I didn't know I had (5 half-used bottles of soy sauce). The decision framework: everything out first (the chaos peak), sort by category, trash expired, donate unused unopened, then build zones (breakfast zone, baking zone, snacks, canned goods). Decant or not: honest take (decanting is beautiful but only worth it if you actually bake regularly). Products used: tiered lazy susans, pull-out drawers for cans, clear bins with labels. Total: $87 in organizers. Show the before chaos, the empty floor moment, and the finished labeled pantry."
- "Bedroom closet with too much stuff and not enough space: The real problem isn't the closet — it's that there are 40 items in the closet that I haven't worn in 18 months. Walk through the edit (the decision rule: worn in the last year AND would buy again today = keep), the math (removed 47 items, kept 31, the closet is now usable), and the simple organization (same hangers throughout, like with like, most-used at eye level). No products. No bins. No labels. Just editing."
- "Garage transformation from storage disaster to functional workshop: 2-car garage used for 0 cars and maximum chaos. Phase 1: sort and donate (7 donation runs, fill a 10-foot trailer with trash). Phase 2: overhead storage for seasonal items (racks installed into joists — show the structural consideration). Phase 3: wall system for tools (pegboard + french cleat sections). Phase 4: workbench build. Total: $340 in materials, 3 weekends. Show the before at its worst and the first car parked in it."

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `space_type` | Area being organized | `"pantry"`, `"closet"`, `"garage"`, `"kitchen"`, `"whole_home"`, `"bedroom"` |
| `method` | Organization approach | `"konmari"`, `"zone_based"`, `"edit_first"`, `"category_based"`, `"container_method"` |
| `products_used` | Organizers and containers | `["tiered lazy susan"`, `"pull-out can drawer"`, `"clear bins"]` |
| `budget` | Organizer spend | `"$0 edit only"`, `"$87"`, `"$340"` |
| `problem_statement` | The before state | `"things falling out"`, `"haven't opened boxes in 3 years"` |
| `key_decisions` | Organizing logic | `["worn in last year AND would buy again"`, `"most-used at eye level"]` |
| `tone` | Content style | `"motivating"`, `"realistic"`, `"minimalist"`, `"system_focused"` |
| `duration_minutes` | Video length | `5`, `8`, `12`, `15` |
| `platform` | Distribution | `"youtube"`, `"tiktok"`, `"instagram"` |

## Workflow

1. Describe the space, the problem, the decisions made, and the resulting system
2. NemoVideo structures the organization narrative (chaos before → empty reset → system building → calm after)
3. Zone labels, product callouts, decision rules, and cost overlays added automatically
4. Export with satisfying pacing matched to the transformation content

## API Usage

### Pantry Organization Transformation

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "home-organization-video",
    "input": {
      "prompt": "Deep pantry organization for a family of 5: The before state — 4-shelf pantry where the back shelves are invisible graveyards of forgotten food. The problem: no zones, no system, items pushed to the back and forgotten. The process: completely empty the pantry onto the kitchen table (show the table mountain — this is the chaos peak and it is important to show), trash everything expired (3 grocery bags), sort into categories (grains, canned, snacks, baking, sauces), then assign permanent zones. The zone rule: frequency of use determines shelf height (daily use = eye level, monthly baking supplies = bottom, backup inventory = top). Products: two sets of pull-out shelves for canned goods (the specific problem solver for deep shelves), matching food-safe bins for loose items. Total: $120. Show the empty pantry → zone assignment → final stocked and labeled system.",
      "space_type": "pantry",
      "method": "zone_based",
      "products_used": ["pull-out can drawers", "matching bins", "labels"],
      "budget": "$120",
      "problem_statement": "back shelves are invisible food graveyards",
      "key_decisions": ["frequency determines height", "zone before you contain"],
      "tone": "system_focused",
      "duration_minutes": 10,
      "platform": "youtube",
      "hashtags": ["PantryOrganization", "HomeOrganization", "PantryMakeover", "OrganizeWithMe", "PantryGoals"]
    }
  }'
```

**Response:**
```json
{
  "job_id": "organize_mno345",
  "status": "processing",
  "estimated_seconds": 100,
  "poll_url": "https://mega-api-prod.nemovideo.ai/v1/jobs/organize_mno345"
}
```

### Closet Edit (No Products) Video

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "home-organization-video",
    "input": {
      "prompt": "Capsule wardrobe edit — getting from 80 items to 33: Not a minimalism lecture, just what I actually did. The decision framework I used (not KonMari, not spark joy — just: would I buy this today for $50? If no, it goes). The math: started with 84 items, 31 immediate yes, 22 immediate no, 31 in the maybe pile. The maybe pile rule: comes out of the closet for 30 days and lives on a chair. Anything I didn't reach for once in 30 days was not a maybe. Ended with 38 items. What I kept and why. What surprised me (the expensive dress I never wore vs the $25 blouse I wear weekly). No bins, no containers, no organizing products. The closet is organized because there is less in it.",
      "space_type": "closet",
      "method": "edit_first",
      "budget": "$0 edit only",
      "tone": "minimalist",
      "duration_minutes": 8,
      "platform": "youtube"
    }
  }'
```

## Tips for Best Results

- **The chaos peak is essential**: "Completely empty the pantry onto the kitchen table — show the table mountain" — the worst moment of an organization project is motivating to viewers and makes the transformation meaningful
- **Decision frameworks beat instructions**: "Worn in the last year AND would buy again today" or "frequency of use determines shelf height" — the rule that drives the decision is more useful than "put like with like"
- **No products is its own angle**: "$0 edit only" — the permission to organize without buying containers is valuable content for audiences that feel they need to spend money to get organized
- **The math builds credibility**: "Started with 84 items, removed 47, kept 31" or "7 donation runs, fill a 10-foot trailer with trash" — specific quantities show the scale of the work and make the result believable
- **The before state needs to be specific and real**: "Things falling out when you open the door" or "5 half-used bottles of soy sauce" — the embarrassing specific detail is what viewers relate to and why they watch

## Output Formats

| Platform | Resolution | Duration |
|----------|------------|----------|
| YouTube | 1920×1080 | 8–15 min |
| TikTok | 1080×1920 | 60–180s |
| Instagram Reels | 1080×1920 | 60–90s |

## Related Skills

- `home-renovation-video` — Structural changes before organization
- `interior-design-video` — Styling after the organization system is built
- `declutter-video-maker` — Focused decluttering without organization systems

## Common Questions

**KonMari vs container method vs zone method — which should I use in my video?**
Choose based on what you actually did. Set `method` to match your approach. Viewers search for specific methods — "KonMari closet" and "zone pantry organization" are different audiences searching for different things.

**How long should a home organization video be?**
Match the complexity of the project. Closet edit: 8-10 minutes. Full pantry overhaul: 10-12 minutes. Garage transformation: 15-20 minutes. "Organize with me" real-time companion: 20-45 minutes (a different genre with a different audience).

**Can I create organization content without being a professional organizer?**
Absolutely. Personal organization journey content ("how I finally organized my disaster pantry") performs as well as professional organizer content. The relatable before state is more important than credentials.
