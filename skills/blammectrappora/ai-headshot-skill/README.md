# AI Professional Headshot Generator

Generate polished, photorealistic professional headshots from a text description using AI. Powered by the Neta talesofai API — get a direct image URL back in seconds.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/ai-headshot-skill
```

**Via ClawHub:**
```bash
clawhub install ai-headshot-skill
```

---

## Usage

```bash
# Default prompt (studio headshot)
node aiheadshot.js

# Custom prompt
node aiheadshot.js "executive headshot, woman in blazer, blurred office background"

# With size option
node aiheadshot.js "confident professional headshot" --size landscape

# With a reference image UUID
node aiheadshot.js "same person, different background" --ref <picture_uuid>
```

The script prints a single image URL to stdout on success.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--token` | string | — | Neta API token (overrides env/file) |
| `--ref` | picture_uuid | — | Reference image UUID for style inheritance |

### Size dimensions

| Name | Width × Height |
|------|---------------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

---

## Token setup

The script resolves your `NETA_TOKEN` in this order:

1. `--token <value>` CLI flag
2. `NETA_TOKEN` environment variable

**Recommended:** add to your shell profile or `.env` file:
```bash
export NETA_TOKEN=your_token_here
```

---

## Examples

```bash
# Portrait headshot (default)
node aiheadshot.js "professional studio headshot, man in suit, neutral grey background"

# Square crop for profile pictures
node aiheadshot.js "friendly professional headshot, warm smile" --size square

# Landscape for LinkedIn banner
node aiheadshot.js "executive portrait, woman, modern office background" --size landscape
```

## Example Output

![Generated example](https://oss.talesofai.cn/picture/66f12b83-2349-4c05-ab43-16dfae9fb943.webp)
