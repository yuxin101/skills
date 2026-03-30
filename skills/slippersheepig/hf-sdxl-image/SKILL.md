---
name: hf-sdxl-image
description: Generate an image from a text prompt through the Hugging Face Inference API using the HUGGINGFACE_TOKEN environment variable and an optional HF_IMAGE_MODEL override (default: stabilityai/stable-diffusion-xl-base-1.0). Use when the user asks to generate, draw, create, make, or render an image or illustration from text, especially when they mention Hugging Face, SDXL, Stable Diffusion, or want the result sent back directly into the current chat.
---

# HF SDXL Image

Generate a single image from a text prompt with the Hugging Face router endpoint. The skill defaults to `stabilityai/stable-diffusion-xl-base-1.0` and can be switched to another compatible Hugging Face Inference API model by setting `HF_IMAGE_MODEL`.

## Chat-oriented workflow

When the user asks for an image, illustration, cover image, wallpaper, poster, concept art, or similar visual generated from text:

1. Turn the user's request into a single prompt string.
2. Run `scripts/generate_hf_sdxl.py` with that prompt.
3. Save the image to a local file.
4. Send the generated image file back to the current conversation by default when media sending is available.
5. Do not reply with only a saved local path when you can send the image to chat.
6. Only fall back to returning the saved local file path if media upload is unavailable or fails.
7. If the API returns JSON or an HTTP error, surface the exact error instead of claiming success.

## Strong trigger examples

Use this skill for requests like:

- "生成一张图片：夕阳下的海边小镇"
- "画一张赛博朋克风格的城市夜景"
- "帮我做一张封面图，主题是 AI 和机器人"
- "用 Hugging Face 生成一张可爱的熊在图书馆读书"
- "用 SDXL 出一张未来感海报"
- "create an illustration of a scholar bear reading in a grand library"

## Command

```bash
python3 scripts/generate_hf_sdxl.py "a cozy cyberpunk alley at night, cinematic lighting" --output ./output --wait-for-model
```

With a model override:

```bash
HF_IMAGE_MODEL=stabilityai/stable-diffusion-3-medium-diffusers \
python3 scripts/generate_hf_sdxl.py "a cozy cyberpunk alley at night, cinematic lighting" --output ./output --wait-for-model
```

The script prints the saved file path on success.

## Behavior

- Sends `POST https://router.huggingface.co/hf-inference/models/<model-id>`
- Reads the bearer token from `HUGGINGFACE_TOKEN`
- Reads the model id from `HF_IMAGE_MODEL` when set; otherwise uses `stabilityai/stable-diffusion-xl-base-1.0`
- Sends JSON with `inputs` set to the prompt
- Requests image output with a single supported `Accept` header value
- Saves the returned image bytes to the requested path
- Fails loudly when the API returns JSON or an HTTP error

## Parameters

- Positional `prompt`: image prompt text
- `--output`: output file path or directory; defaults to `./output`
- `--timeout`: HTTP timeout in seconds; defaults to `180`
- `--wait-for-model`: set `options.wait_for_model=true` so cold starts wait instead of failing fast

## Troubleshooting

### Missing token

If the script says `Missing HUGGINGFACE_TOKEN environment variable.`, export the token before running it.

```bash
export HUGGINGFACE_TOKEN=hf_xxx
```

### Optional model override

To switch to another compatible Hugging Face Inference API model, set `HF_IMAGE_MODEL`.

```bash
export HF_IMAGE_MODEL=stabilityai/stable-diffusion-3-medium-diffusers
```

If `HF_IMAGE_MODEL` is unset, the script uses `stabilityai/stable-diffusion-xl-base-1.0`.

### 401 or 403

The token is missing, invalid, expired, or does not have permission for the endpoint.

### 503 or model loading errors

Retry with `--wait-for-model`.

### JSON instead of an image

Read the full JSON error body and surface it to the user. Do not pretend generation succeeded.

## Resource

### scripts/generate_hf_sdxl.py

Use this script for deterministic generation and repeatable testing.
