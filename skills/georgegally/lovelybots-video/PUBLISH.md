# How to Publish to ClawHub

## Before You Publish

1. Verify the API endpoints in SKILL.md match your actual production routes
2. Confirm the request/response schema is accurate
3. Make sure lovelybots.com/developer/api_tokens is live and self-serve
4. Test the skill locally with a real API key

## One-time Setup

```bash
# Install the ClawHub CLI
npm install -g clawhub

# Authenticate with GitHub
clawhub login
```

Your GitHub account must be at least 1 week old to publish.

## Publish

```bash
# From the parent directory of lovelybots-video/
clawhub publish ./lovelybots-video --slug lovelybots-video --name "LovelyBots Video" --version 1.0.0 --changelog "Initial release — avatar video generation for OpenClaw agents"
```

Your skill will be live at:
**https://clawhub.ai/[your-github-username]/lovelybots-video**

Users install it with:
```bash
openclaw skills install lovelybots-video
```

## After Publishing

Post in the OpenClaw GitHub Discussions or Discord:

> "Just published a video generation skill to ClawHub — lets your agent generate avatar videos from a script. Built on LovelyBots API. Install with `npx clawhub add lovelybots-video`"

That's it. The community does the rest.

## Updating the Skill

```bash
clawhub publish . --slug lovelybots-video --version 1.0.1 --changelog "Updated polling docs and added aspect ratio support"
```

## Schema Check

Before publishing, verify these assumptions in SKILL.md are correct:

- [ ] POST /api/create takes `script` and `avatar_url` as the primary fields
- [ ] Response includes `id`, `status`, `video_url`, `credits_used`
- [ ] Polling endpoint is GET /api/videos/:id
- [ ] Failed renders return `credits_refunded: true`
- [ ] Production base URL is https://lovelybots.com/api (not the ngrok URL)

If any fields differ, update SKILL.md before publishing.
