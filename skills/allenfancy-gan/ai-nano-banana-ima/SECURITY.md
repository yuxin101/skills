# Security Disclosure: ai-nano-banana-ima

## Purpose

This document explains network endpoints, credential flow, and local data usage for `ai-nano-banana-ima`.

## Network Endpoints

| Domain | Used For | Trigger |
|---|---|---|
| `api.imastudio.com` | Product list, task create, task detail polling | `text_to_image` and `image_to_image` |
| `imapi.liveme.com` | Local image upload token + file upload | `image_to_image` when input is local file path |

## Credential Flow

| Credential | Where Sent | Why |
|---|---|---|
| `IMA_API_KEY` | `api.imastudio.com` | Standard Open API auth (`Authorization: Bearer ...`) |
| `IMA_API_KEY` | `imapi.liveme.com` | Upload authentication (`appUid`, `cmimToken`) for OSS token flow |
| `APP_ID` / `APP_KEY` | `imapi.liveme.com` | Request signing for upload-token endpoint |

## Explicit Consent Gate

For local `image_to_image` uploads, the script requires:

```bash
--allow-secondary-upload-domain
```

Without this flag, execution fails fast with an explicit warning.

HTTPS input URLs do not require secondary upload and do not require this flag.

## Model Scope Enforcement

The script hard-limits exposed model IDs to:

- `gemini-3.1-flash-image`
- `gemini-3-pro-image`

Any other model ID is rejected locally.

## Local Data

| Path | Content | Retention |
|---|---|---|
| `~/.openclaw/memory/ima_prefs.json` | Per-user model preference cache | Until manually removed |
| `~/.openclaw/logs/ima_skills/` | Operational logs | Auto-cleaned by script after 7 days |

No secret is written into repository files.
