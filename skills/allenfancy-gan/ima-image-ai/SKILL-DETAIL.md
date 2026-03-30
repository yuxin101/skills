---
name: IMA Studio Image Generation
version: 1.0.8
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, image generation, text to image, 图像生成, AI绘画, 文生图, 图生图, IMA, 画图, SeeDream, Nano Banana, Midjourney
argument-hint: "[text prompt or image URL]"
description: >
  Complete API documentation for IMA Image Generator. Includes detailed model parameters,
  attribute_id references, error handling, UX protocol, and Python examples.
---

# IMA Image AI — Complete Documentation

## Supported Models

⚠️ **Production Environment**: **4 image models** are currently available (as of 2026-02-28).

### text_to_image (4 models)

| Name | model_id | version_id | Cost | attribute_id | Size Options |
|------|----------|------------|------|--------------|--------------|
| **SeeDream 4.5** 🌟 | `doubao-seedream-4.5` | `doubao-seedream-4-5-251128` | 5 pts | 2341 | Default (adaptive 4k) |
| **Nano Banana2** 💚 | `gemini-3.1-flash-image` | `gemini-3.1-flash-image-preview` | 4/6/10/13 pts | 4400/4401/4402/4403 | 512px/1K/2K/4K |
| **Nano Banana Pro** | `gemini-3-pro-image` | `gemini-3-pro-image-preview` | 10/10/18 pts | 2399/2400/2401 | 1K/2K/4K |
| **Midjourney** 🎨 | `midjourney` | `v6` | 8/10 pts | 5451/5452 | 480p/720p |

### image_to_image (4 models)

| Name | model_id | version_id | Cost | attribute_id | Size Options |
|------|----------|------------|------|--------------|--------------|
| **SeeDream 4.5** 🌟 | `doubao-seedream-4.5` | `doubao-seedream-4-5-251128` | 5 pts | 1611 | Default (adaptive 4k) |
| **Nano Banana2** 💚 | `gemini-3.1-flash-image` | `gemini-3.1-flash-image-preview` | 4/6/10/13 pts | 4404/4405/4406/4407 | 512px/1K/2K/4K |
| **Nano Banana Pro** | `gemini-3-pro-image` | `gemini-3-pro-image-preview` | 10 pts | 2402/2403/2404 | 1K/2K/4K |
| **Midjourney** 🎨 | `midjourney` | `v6` | 8/10 pts | 5453/5454 | 480p/720p |

---

## Estimated Generation Time per Model

| Model | Estimated Time | Poll Every | Send Progress Every |
|-------|---------------|------------|---------------------|
| **SeeDream 4.5** 🌟 | 30~60s | 5s | 20s |
| **Nano Banana2** 💚 | 20~40s | 5s | 15s |
| **Nano Banana Pro** | 60~120s | 5s | 30s |
| **Midjourney** 🎨 | 40~90s | 8s | 25s |

---

## 💬 User Experience Protocol (IM / Feishu / Discord)

### 🚫 Never Say to Users

| ❌ Never say | ✅ What users care about |
|-------------|--------------------------|
| `ima_image_create.py` / 脚本 / script | — |
| attribute_id / model_version / form_config | — |
| API 调用 / HTTP 请求 / 任何技术参数名 | — |

Only tell users: **model name · estimated time · credits · result (image/media) · plain-language status**.

### UX Flow

1. **Pre-generation:** "🎨 开始生成图片… 模型：[Name]，预计[X~Y]秒，消耗[N]积分"
2. **Progress:** Every 15-30s: "⏳ 正在生成中… [P]%" (cap at 95%)
3. **Success:** Send image via `media=image_url` + caption with link
4. **Failure:** Natural language error + suggest alternatives

---

## ⚠️ Error Message Translation

**NEVER show technical error messages to users.**

| Technical Error | ✅ Say Instead (Chinese) | ✅ Say Instead (English) |
|----------------|------------------------|------------------------|
| `401 Unauthorized` | ❌ API密钥无效或未授权<br>💡 **生成新密钥**: https://www.imaclaw.ai/imaclaw/apikey | ❌ API key is invalid<br>💡 **Generate API Key**: https://www.imaclaw.ai/imaclaw/apikey |
| `4008 Insufficient points` | ❌ 积分不足<br>💡 **购买积分**: https://www.imaclaw.ai/imaclaw/subscription | ❌ Insufficient points<br>💡 **Buy Credits**: https://www.imaclaw.ai/imaclaw/subscription |
| `Error 6006` | 积分计算异常，系统正在修复 | Points calculation error |
| `Error 6010` | 模型参数不匹配，请尝试其他模型 | Model parameters incompatible |
| `error 400` | 图片参数设置有误，请调整尺寸或比例 | Image parameter error |
| `timeout` | 生成时间过长已超时，建议用更快的模型 | Generation took too long |

**Failure fallback table:**

| Failed Model | First Alt | Second Alt |
|-------------|-----------|------------|
| SeeDream 4.5 | Nano Banana2（4pts） | Nano Banana Pro（10-18pts） |
| Nano Banana2 | SeeDream 4.5（5pts） | Nano Banana Pro（10-18pts） |
| Nano Banana Pro | SeeDream 4.5（5pts） | Nano Banana2（4pts） |
| Midjourney | SeeDream 4.5（5pts） | Nano Banana2（4pts） |

---

## 🌐 Network Endpoints

| Domain | Purpose | What's Sent |
|--------|---------|-------------|
| `api.imastudio.com` | Main API | Prompts, model params, task IDs |
| `imapi.liveme.com` | Image upload (i2i only) | Image files, IMA API key |

Both domains are **owned by IMA Studio**.

---

## Quick Reference: attribute_ids

⚠️ Always call `/open/v1/product/list` at runtime; values change frequently.

**text_to_image**:

| Model | model_id | attribute_id | credit | Size |
|-------|----------|-------------|--------|------|
| SeeDream 4.5 | `doubao-seedream-4.5` | **2341** | 5 pts | adaptive 4k |
| Nano Banana2 (512px) | `gemini-3.1-flash-image` | **4400** | 4 pts | 512×512 |
| Nano Banana2 (1K) | `gemini-3.1-flash-image` | **4401** | 6 pts | 1024×1024 |
| Nano Banana2 (2K) | `gemini-3.1-flash-image` | **4402** | 10 pts | 2048×2048 |
| Nano Banana2 (4K) | `gemini-3.1-flash-image` | **4403** | 13 pts | 4096×4096 |
| Nano Banana Pro (1K) | `gemini-3-pro-image` | **2399** | 10 pts | 1024×1024 |
| Nano Banana Pro (2K) | `gemini-3-pro-image` | **2400** | 10 pts | 2048×2048 |
| Nano Banana Pro (4K) | `gemini-3-pro-image` | **2401** | 18 pts | 4096×4096 |

**image_to_image**:

| Model | model_id | attribute_id | credit | Size |
|-------|----------|-------------|--------|------|
| SeeDream 4.5 | `doubao-seedream-4.5` | **1611** | 5 pts | adaptive 4k |
| Nano Banana2 (512px) | `gemini-3.1-flash-image` | **4404** | 4 pts | 512×512 |
| Nano Banana2 (1K) | `gemini-3.1-flash-image` | **4405** | 6 pts | 1024×1024 |
| Nano Banana2 (2K) | `gemini-3.1-flash-image` | **4406** | 10 pts | 2048×2048 |
| Nano Banana2 (4K) | `gemini-3.1-flash-image` | **4407** | 13 pts | 4096×4096 |

---

## Aspect Ratio Support

| Model | Supported Ratios | Notes |
|-------|------------------|-------|
| SeeDream 4.5 | 1:1, 16:9, 9:16, 4:3, 3:4, 2:3, 3:2, 21:9 | Via virtual params |
| Nano Banana2 | 1:1, 16:9, 9:16, 4:3, 3:4 | Native support |
| Nano Banana Pro | 1:1, 16:9, 9:16, 4:3, 3:4 | Native support |
| Midjourney | 1:1 only | Fixed 1024×1024 |

**SeeDream 4.5 aspect_ratio → size mapping:**
- `1:1` → 2048×2048
- `16:9` → 2560×1440
- `9:16` → 1440×2560
- `4:3` → 2304×1728
- `3:4` → 1728×2304
- `2:3` → 1664×2496
- `3:2` → 2496×1664
- `21:9` → 3024×1296

---

## API Reference

### Core Flow

```
1. GET /open/v1/product/list?app=ima&platform=web&category=<type>
   → Get attribute_id, credit, model_version, form_config

2. [image_to_image only] Upload input image → get HTTPS URL

3. POST /open/v1/tasks/create → get task_id

4. POST /open/v1/tasks/detail → poll every 3-5s until resource_status==1
```

### API 1: Product List

```
GET /open/v1/product/list?app=ima&platform=web&category=text_to_image
```

### API 2: Create Task

**text_to_image:**
```json
{
  "task_type": "text_to_image",
  "enable_multi_model": false,
  "src_img_url": [],
  "parameters": [{
    "attribute_id": 2341,
    "model_id": "doubao-seedream-4.5",
    "model_name": "SeeDream 4.5",
    "model_version": "doubao-seedream-4-5-251128",
    "app": "ima",
    "platform": "web",
    "category": "text_to_image",
    "credit": 5,
    "parameters": {
      "prompt": "a beautiful mountain sunset",
      "size": "4k",
      "n": 1,
      "input_images": [],
      "cast": {"points": 5, "attribute_id": 2341}
    }
  }]
}
```

**image_to_image:**
```json
{
  "task_type": "image_to_image",
  "enable_multi_model": false,
  "src_img_url": ["https://example.com/input.jpg"],
  "parameters": [{
    "attribute_id": 1611,
    "model_id": "doubao-seedream-4.5",
    "model_name": "SeeDream 4.5",
    "model_version": "doubao-seedream-4-5-251128",
    "app": "ima",
    "platform": "web",
    "category": "image_to_image",
    "credit": 5,
    "parameters": {
      "prompt": "turn into oil painting style",
      "size": "4k",
      "n": 1,
      "input_images": ["https://example.com/input.jpg"],
      "cast": {"points": 5, "attribute_id": 1611}
    }
  }]
}
```

### API 3: Task Detail (Poll)

```
POST /open/v1/tasks/detail
{"task_id": "<id>"}
```

| resource_status | status | Action |
|-----------------|--------|--------|
| 0 or null | pending/processing | Keep polling |
| 1 | success | Done, read `url` |
| 2/3 | any | Failed |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `attribute_id` is 0 or missing | Always query product list first |
| `prompt` at outer level | Must be inside `parameters[].parameters` |
| Wrong `credit` value | Must match `credit_rules[].points` |
| `size: "adaptive"` for SeeDream i2i | Use values from `form_config` only |

---

## Python Example

```python
import time, requests

BASE_URL = "https://api.imastudio.com"
API_KEY = "ima_your_key_here"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "x-app-source": "ima_skills",
    "x_app_language": "en",
}

def get_products(category):
    r = requests.get(f"{BASE_URL}/open/v1/product/list",
                     headers=HEADERS,
                     params={"app": "ima", "platform": "web", "category": category})
    r.raise_for_status()
    versions = []
    for node in r.json()["data"]:
        for child in node.get("children") or []:
            if child.get("type") == "3":
                versions.append(child)
    return versions

def create_task(task_type, prompt, product, input_images=None):
    input_images = input_images or []
    rule = product["credit_rules"][0]
    body = {
        "task_type": task_type,
        "enable_multi_model": False,
        "src_img_url": input_images,
        "parameters": [{
            "attribute_id": rule["attribute_id"],
            "model_id": product["model_id"],
            "model_name": product["name"],
            "model_version": product["id"],
            "app": "ima", "platform": "web",
            "category": task_type,
            "credit": rule["points"],
            "parameters": {
                "prompt": prompt, "n": 1,
                "input_images": input_images,
                "cast": {"points": rule["points"], "attribute_id": rule["attribute_id"]}
            }
        }]
    }
    r = requests.post(f"{BASE_URL}/open/v1/tasks/create", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]["id"]

def poll(task_id, interval=3, timeout=300):
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.post(f"{BASE_URL}/open/v1/tasks/detail",
                          headers=HEADERS, json={"task_id": task_id})
        r.raise_for_status()
        task = r.json()["data"]
        medias = task.get("medias", [])
        if medias and all(m.get("resource_status") == 1 for m in medias):
            return task
        time.sleep(interval)
    raise TimeoutError(f"Task timed out: {task_id}")

# Example: text_to_image
products = get_products("text_to_image")
seedream = next(p for p in products if p["model_id"] == "doubao-seedream-4.5")
task_id = create_task("text_to_image", "mountain sunset", seedream)
result = poll(task_id)
print(result["medias"][0]["url"])
```
