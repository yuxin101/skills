---
name: makepost-app-growth
version: 1.0.1
title: App Growth Toolkit (via makepost.com)
description: Manage social media across 9 platforms, track App Store analytics, monitor ASO keywords, analyze competitors, and control subscription pricing — all through conversation.
license: MIT
author: William Engbjerg
homepage: https://makepost.com/openclaw
keywords: social-media, app-store, aso, analytics, subscription-pricing, ios, app-growth
metadata:
  openclaw:
    requires:
      env:
        - MAKEPOST_API_KEY
      bins:
        - npx
    primaryEnv: MAKEPOST_API_KEY
---

# App Growth Toolkit (via makepost.com)

MakePost is a growth platform for iOS app developers. Publish to 9 social platforms, track downloads and revenue via App Store Connect, monitor ASO keyword rankings, watch competitor apps, and manage subscription pricing — from one place or from your AI agent.

## Setup

1. Create a MakePost account at [makepost.com](https://makepost.com)
2. Connect your social accounts (TikTok, Instagram, YouTube, etc.)
3. Add your iOS apps and connect App Store Connect credentials
4. Generate an API key from Settings
5. Store your API key:
   ```
   MAKEPOST_API_KEY=sk_live_your_key_here
   ```

## Auth

All requests use Bearer token:
```
Authorization: Bearer <MAKEPOST_API_KEY>
```

MCP endpoint: `https://makepost.com/api/mcp/`

## Available Tools

### Publishing

**list_videos** — List uploaded videos ready for posting.
- `limit` (int, default 50) — Max videos to return.
- Returns: video ID, title, duration (seconds), source ("upload" or "creatify"), linked app name.
- Only completed videos included (processing/errored excluded). Sorted newest first.

**upload_video** — Upload a video from a public URL into MakePost.
- `video_url` (string, required) — Public URL to .mp4, .mov, .webm, or .m4v. Max 500MB, max 10 minutes.
- `title` (string, required) — Video title.
- `caption` (string) — Default caption for publishing. Falls back to title if empty.
- `app_id` (string) — App to link to. Accepts app ID, name, or bundle ID. Auto-selects if you have one app.
- Returns: video_id, url, title, duration, file_size, is_short_eligible.
- Runs content moderation automatically. Rejected content is deleted.

**list_accounts** — List connected social media accounts.
- Returns: account ID, platform, username, provider.
- Only active (connected) accounts returned. Disconnected accounts excluded.
- Platforms: tiktok, instagram, youtube, facebook, x, linkedin, threads, pinterest, bluesky.

**schedule_post** — Schedule a video to one or more social media accounts at a specific time.
- `video_id` (string, required) — Video ID from list_videos.
- `account_ids` (list of strings, required) — Account IDs from list_accounts.
- `scheduled_at` (string, required) — ISO 8601 datetime (e.g. "2026-03-22T15:00:00").
- `timezone` (string) — IANA timezone (e.g. "America/New_York"). Defaults to your account timezone.
- `caption` (string) — Post caption. Falls back to video script, then title.
- Inactive accounts in the list are silently skipped. Response times are always UTC.

**list_posts** — List your posts, optionally filtered by status.
- `status` (string) — Filter: "scheduled", "published", "failed", "pending", or "processing".
- `limit` (int, default 50) — Max posts to return (1-100).
- Status lifecycle: scheduled → pending → processing → published or failed.
- All timestamps in UTC. Sorted by scheduled_at (newest first).

**cancel_scheduled_post** — Cancel a scheduled post before it publishes.
- `post_id` (string, required) — Post ID to cancel.
- Only works on posts with status "scheduled". The post is permanently deleted.

**reschedule_scheduled_post** — Change when a scheduled post will be published.
- `post_id` (string, required) — Post ID to reschedule.
- `scheduled_at` (string, required) — New publish time in ISO 8601.
- `timezone` (string) — IANA timezone. Defaults to your account timezone.
- Only works on "scheduled" posts. New time must be at least 5 minutes in the future.

**get_publishing_results** — Check publishing results for a post.
- `post_id` (string, required) — Post ID to check.
- Returns: status, platform_url (null while pending), stats (views, likes, comments, shares — null until synced), error_message (only for failed posts).

### App Analytics

**list_apps** — List your connected iOS apps with App Store metadata.
- Returns: app ID, name, bundle ID, rating (1-5), rating_count.
- Rating is null if the app has no ratings yet. Sorted newest first.

**get_app_analytics** — Get download and revenue stats for an app over a period.
- `app_id` (string) — App ID, name, or bundle ID. Auto-selects if you have one app.
- `days` (int, default 7) — Days of data to return (1-90).
- Key fields:
  - `net_revenue` — Your actual earnings after Apple's 15-30% commission. Use this for "total revenue" or "earnings" questions.
  - `gross_revenue` — What customers paid before Apple's cut. Only use when specifically asked about gross amounts.
  - `active_subscriptions` — Peak concurrent subscribers (max across the period, NOT a sum).
  - `new_trials` — Free trial starts, summed across the period.
  - `revenue_currency` — ISO 4217 code. Null on days with no data.

### ASO (App Store Optimization)

**get_aso_keywords_tool** — Get tracked ASO keywords with latest rankings, difficulty, popularity, and 7-day rank change.
- `app_id` (string) — App ID, name, or bundle ID. Auto-selects if you have one app.
- `country` (string) — 2-letter country code to filter (e.g. "us", "gb", "de").
- Key fields:
  - `rank` — App Store search position. Lower is better. Null means no rank data.
  - `rank_change` — Positive = improved (e.g. moved from #10 to #5 = +5). Negative = worsened.
  - `difficulty` — How hard to rank (0-100).
  - `popularity` — Search volume indicator (0-100).

**get_keyword_history** — Get full ranking history for a specific tracked keyword over time.
- `keyword_id` (string, required) — Keyword ID from get_aso_keywords_tool.
- `app_id` (string) — App ID, name, or bundle ID. Auto-selects if you have one app.
- Returns daily snapshots ordered chronologically (oldest first).
- Null rank means data was unavailable that day, not that the app was unranked.

**get_aso_competitors_tool** — Get tracked competitor apps with App Store metadata.
- `app_id` (string) — App ID, name, or bundle ID. Auto-selects if you have one app.
- Returns: competitor name, rating, rating_count, category, icon URL, last_refreshed_at.

**search_keyword** — Search for an ASO keyword and get cached analysis.
- `keyword` (string, required) — Keyword or phrase to search.
- `country` (string, default "us") — 2-letter country code.
- `app_id` (string) — App ID, name, or bundle ID. Auto-selects if you have one app.
- Cached lookup only (24h cache). If no cached data exists, search via the MakePost web UI first, then retry here.

**get_aso_score_tool** — Check the ASO metadata optimization score for an app.
- `app_id` (string) — App ID, name, or bundle ID. Auto-selects if you have one app.
- Returns: score (0-100 based on title, subtitle, keywords, description completeness), scored_at.

### Subscription Pricing

**list_subscriptions** — List Apple App Store subscription products for an app.
- `app_id` (string) — App ID, name, or bundle ID. Auto-selects if you have one app.
- CRITICAL: Two ID fields exist:
  - `id` — Internal database ID. Do NOT use with other subscription tools.
  - `apple_subscription_id` — Apple's numeric ID (e.g. "6757696252"). Use THIS for all pricing tools.
- Returns: name, duration (ISO 8601, e.g. "P1M" = 1 month), state.

**get_subscription_prices** — Get subscription prices by territory with currency and pending changes.
- `subscription_id` (string, required) — Apple's numeric subscription ID from list_subscriptions (the apple_subscription_id field).
- `territory_code` (string) — ISO 3166-1 alpha-3 (e.g. "USA", "GBR", "JPN").
- `app_id` (string) — App ID, name, or bundle ID. Auto-selects if you have one app.
- Key fields: current_price, current_price_usd, pending_price (null if none), pending_source ("manual" or "automatic").

**stage_price_change_tool** — Stage a pending price change for a subscription in a specific territory.
- `subscription_id` (string, required) — Apple's numeric subscription ID.
- `territory_code` (string, required) — Territory code (e.g. "USA", "GBR").
- `new_price` (float, required) — New price in the territory's local currency.
- `app_id` (string) — App ID, name, or bundle ID. Auto-selects if you have one app.
- This only stages locally — does NOT push to Apple. Use push_price_changes to submit.
- If new_price matches current price (within $0.01), the pending change is removed instead.

**push_price_changes** — Push all staged price changes to App Store Connect.
- `subscription_id` (string, required) — Apple's numeric subscription ID.
- `app_id` (string) — App ID, name, or bundle ID. Auto-selects if you have one app.
- Asynchronous — returns immediately with status "started". Only one push per subscription at a time.
- WARNING: Changes may take effect immediately once pushed. Review with get_subscription_prices first.
- Requires App Store Connect credentials to be configured.

## Example Workflows

- "Upload https://example.com/my-video.mp4 and schedule it to all my accounts tomorrow at noon" — Downloads the video, runs moderation, and schedules across all connected platforms.
- "Post my latest video to TikTok and Instagram tomorrow at 3pm" — Finds your most recent video, picks the right accounts, and schedules it.
- "How are my app downloads this week compared to last week?" — Pulls analytics for all your apps and compares the two periods.
- "What keywords did my app gain or lose rankings on?" — Checks ASO keyword history and highlights changes.
- "Lower my Pro subscription price to $4.99 in Brazil and push it live" — Stages the price change and pushes to App Store Connect after your confirmation.

## Tips

- **App auto-selection**: If you have only one app, you can omit app_id from any tool — it auto-selects.
- **Flexible app lookup**: Pass an app name (case-insensitive) or bundle ID instead of the internal ID.
- **Timezone handling**: schedule_post and reschedule default to your account timezone if you don't specify one.
- **Caption fallbacks**: If no caption is provided, publishing uses the video's script, then its title.
- **Revenue fields**: Use net_revenue for earnings questions (after Apple's cut). Use gross_revenue only when specifically asked.
- **Subscription IDs**: Always use apple_subscription_id (not id) when calling pricing tools.
- **Price push safety**: Always confirm with the user before calling push_price_changes — changes can take effect immediately.
- Post to multiple platforms simultaneously by including multiple account IDs in schedule_post.

## Supported Platforms

TikTok, Instagram, YouTube, Facebook, X, LinkedIn, Threads, Pinterest, Bluesky
