# AI Album Cover Generator

Generate stunning album cover art from a text description using AI. Powered by the Neta talesofai API — get back a direct image URL in seconds.

---

## Install

**Via npx skills:**
```bash
npx skills add omactiengartelle/album-cover-skill
```

**Via ClawHub:**
```bash
clawhub install album-cover-skill
```

---

## Usage

```bash
# Basic — uses the built-in default prompt
node albumcover.js

# Custom prompt
node albumcover.js "dark synthwave aesthetic, neon purple cityscape, retro 80s vibes"

# Square cover (default)
node albumcover.js "jazz trio, warm tones, vintage vinyl feel" --size square

# Portrait format
node albumcover.js "epic orchestral album, stormy sky, dramatic" --size portrait

# With a reference image UUID
node albumcover.js "same style but winter theme" --ref abc123-uuid-here

# Pass token explicitly
node albumcover.js "lo-fi beats cover art" --token YOUR_TOKEN_HERE
```

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `square` | Output image dimensions |
| `--style` | `anime`, `cinematic`, `realistic` | `cinematic` | Visual style (informational) |
| `--ref` | `<picture_uuid>` | — | Reference image UUID for style inheritance |
| `--token` | `<token>` | — | Override token resolution |

### Size dimensions

| Size | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

---

## About Neta

[Neta](https://www.neta.art/) (by TalesofAI) is an AI image and video generation platform with a powerful open API. It uses a **credit-based system (AP — Action Points)** where each image generation costs a small number of credits. Subscriptions are available for heavier usage.

### Register & Get Token

| Region | Sign up | Get API token |
|--------|---------|---------------|
| Global | [neta.art](https://www.neta.art/) | [neta.art/open](https://www.neta.art/open/) |
| China  | [nieta.art](https://app.nieta.art/) | [nieta.art/security](https://app.nieta.art/security) |

New accounts receive free credits to get started. No credit card required to try.

### Pricing

Neta uses a pay-per-generation credit model. View current plans on the [pricing page](https://www.neta.art/pricing).

- **Free tier:** limited credits on signup — enough to test
- **Subscription:** monthly AP allowance via Stripe
- **Credit packs:** one-time top-up as needed

### Set up your token

```bash
# Step 1 — get your token:
#   Global: https://www.neta.art/open/
#   China:  https://app.nieta.art/security

# Step 2 — set it
export NETA_TOKEN=your_token_here

# Step 3 — run
node albumcover.js "your prompt"
```

Or pass it inline:
```bash
node albumcover.js "your prompt" --token your_token_here
```

> **API endpoint:** defaults to `api.talesofai.com` (Open Platform tokens).  
> China users: set `NETA_API_BASE_URL=https://api.talesofai.com` to use the China endpoint.


---

## Output

The script prints a single direct image URL to stdout on success, making it easy to pipe into other tools:

```bash
node albumcover.js "cyberpunk album cover, rain, neon" | pbcopy   # copy URL
node albumcover.js "jazz" | xargs curl -o cover.jpg               # download
```

---

## Default Prompt

When no prompt is provided, the script uses:

> professional album cover art, dramatic lighting, bold composition, music album aesthetic, high contrast, visually striking, suitable for streaming platforms

---

Built with [Claude Code](https://claude.ai/claude-code) · Powered by [Neta](https://www.neta.art/) · [Open Portal](https://www.neta.art/open/)