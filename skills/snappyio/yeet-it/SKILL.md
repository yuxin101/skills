---
name: yeetit-publish
description: Publish HTML as a live website instantly. POST HTML, get a shareable URL. No account needed. Sites go live in under a second.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    homepage: https://yeetit.site
    emoji: 🚀
---

# YeetIt — Instant Web Publishing

Publish any HTML content as a live, shareable website in one API call. No account, no authentication, no setup required.

## When to Use This Skill

Use this skill when the user wants to:
- Share HTML, a report, dashboard, or document as a live website
- Deploy a landing page, portfolio, or event page instantly
- Publish any web content and get a shareable URL
- Create a temporary or permanent website from generated content

## How to Publish

Make a POST request to the YeetIt API:

```bash
curl -X POST https://yeetit.site/v1/publish \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><body><h1>Hello World</h1></body></html>",
    "title": "My Page"
  }'
```

The response includes:
- `url` — the live, shareable URL (e.g. https://yeetit.site/hello-world-k3m)
- `edit_key` — key for future updates (save this)
- `claim_url` — link for the user to claim permanent ownership

## Updating a Published Site

```bash
curl -X PUT https://yeetit.site/v1/sites/{slug} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {edit_key}" \
  -d '{"html": "<html><body><h1>Updated</h1></body></html>"}'
```

## Including Assets (CSS, JS, images)

Pass an `assets` map alongside the HTML:

```json
{
  "html": "<html><head><link rel='stylesheet' href='./style.css'></head><body>Hello</body></html>",
  "assets": {
    "style.css": "body { font-family: sans-serif; color: #333; }"
  }
}
```

## Limits (Free Tier)

- Max site size: 5 MB (HTML + assets)
- Max assets: 10 per site
- Expiry: 24 hours (claim via email to extend to 7 days; Pro plan for permanent)
- Max active sites: 5

## Important Notes

- Always show the user the published URL after publishing
- Save the `edit_key` from the response if the user may want to update the site later
- Suggest the user visit the `claim_url` to take permanent ownership
- For sites that need to persist, suggest the Pro plan ($8/mo)
