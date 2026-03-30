---
name: web-collection
description: Browser plugin data collection via a local bridge, in strict synchronous closed-loop mode. Default bridge base URL is http://127.0.0.1:19820; always query task status on the same base URL used for collect, and do not reply to the user until the closed-loop script exits with a final result.
metadata: { "openclaw": { "emoji": "🕸️", "requires": { "bins": ["curl", "node"] } } }
---

# Web Collection

Use the bridge API plus browser extension to collect data from Douyin, TikTok, and Xiaohongshu.

## Browser Choice

This skill should use the user's usual browser environment, not the isolated OpenClaw-managed browser.

Hard rules:

1. Prefer the existing Chrome browser with the collection extension already installed and signed in.
2. Do not launch or rely on the isolated `openclaw` browser profile for this skill.
3. Prefer the local bridge plus browser extension flow over the generic OpenClaw browser tool.
4. If browser tool usage is absolutely required, explicitly use `profile="chrome"` and require an attached tab via the Chrome relay.
5. Never assume the isolated `openclaw` browser profile has the user's cookies, login sessions, or extension state.

## Account and Profile Guardrails

This skill must preserve the user's day-to-day Chrome account environment.

Hard rules:

1. Treat "Chrome" as the user's normal signed-in Chrome profile, including their usual Google account and website login state.
2. Do not silently fall back to another browser profile, another Chrome profile, or the isolated `openclaw` profile.
3. When switching platforms within the same conversation, do not assume the previous platform's browser attachment is still correct.
4. Before a Xiaohongshu, Douyin, or TikTok run after a platform switch, re-check that the active environment is still the user's normal Chrome environment.
5. If the run depends on an attached tab or relay state, require a fresh attached tab in Chrome for the target platform rather than reusing stale attachment assumptions.
6. If you cannot verify that the run is using the user's normal Chrome environment, stop and ask the user to re-attach the Chrome tab instead of continuing.

Practical interpretation:

- "Use the daily Google account" means "use the user's already signed-in normal Chrome session", not a fresh browser context.
- If Chrome relay or browser status was checked for another platform earlier in the thread, that check is stale after a platform change.
- For Xiaohongshu specifically, always prefer a fresh confirmation of the normal Chrome session before collecting.

## Fast Unified Entry (recommended)

When user intent is "采集 + 导出 + 返回链接", start with the bundled wrapper:

```bash
bash {baseDir}/scripts/run.sh \
  --keyword "小龙虾AI助手" \
  --max-items 10 \
  --ensure-bridge
```

Rules for speed:

1. Do not hand-write ad-hoc `curl` status checks before the first run.
2. Start with `scripts/run.sh` immediately.
3. Default to synchronous closed-loop execution. Do not split the task into `start -> running -> process poll -> final reply`.
4. Reply only after the script exits with a final result.
5. Reply result fields first: `表格链接`, `状态`, `导出状态`, `采集条数`.

`run.sh` uses the bundled closed-loop script and defaults to `http://127.0.0.1:19820`.
When available, it auto-detects the packaged macOS connector command under `/Library/Application Support/meixi-connector/...`.

## Closed-Loop Behavior

Use the bundled script:

```bash
{baseDir}/scripts/collect_and_export_loop.sh
```

It enforces the full loop:

1. Check `pluginConnected=true`
2. Wait idle (`running=0 && exporting=0`)
3. Start `POST /api/collect`
4. Handle `TASK_RUNNING` with `stop -> wait idle -> retry`
5. Poll by `taskId` until `completed` or `error`
6. If export is requested, require `export.status=completed` and `export.tableUrl`

If bridge is not already running, use `--ensure-bridge` plus `--bridge-cmd` to auto-start it.
Do not hand-write follow-up status polls against a different port. Reuse the same `--base-url` for collect, status, and stop. The default is `http://127.0.0.1:19820`.

## Strict Sync Mode

This skill should run in synchronous closed-loop mode by default.

Hard rules:

1. Do not reply to the user while the collection script is still running.
2. Do not switch to `process poll`, `sessionId`, or ad-hoc follow-up checks unless the user explicitly asks for progress-first behavior.
3. Do not send an intermediate "任务已发起" style answer by default.
4. Always wait for the closed-loop script to exit and return final JSON before replying.
5. If the execution environment requires an explicit tool timeout, set it high enough for the full loop. Prefer at least `1200` seconds, and use `1800` seconds for slower platforms.
6. When the task succeeds, the final reply must include the table link first when `export.tableUrl` exists, followed by a short analysis of the results.

If a command returns only a running handle instead of final JSON, treat that as the wrong execution mode and rerun with the direct closed-loop command.

## Final Reply Contract

When the task succeeds:

1. If `export.tableUrl` exists, include it in the final reply.
2. Include a short analysis after the link:
   - what the results mostly contain
   - whether the keyword meaning matches the user's likely intent
   - 1 to 3 notable examples
3. Keep the analysis short and useful.

When the task completes without `export.tableUrl`:

1. Explicitly say that the collection finished but no table link was exported.
2. Include the reason if `export.error` exists.
3. Do not imply export succeeded.

Recommended success structure:

- `表格链接`
- `状态`
- `导出状态`
- `采集条数`
- `简短分析`

## Prerequisites

1. Chrome is open and the collection extension is enabled.
2. Bridge server is running. On packaged macOS installs, prefer:

```bash
'/Library/Application Support/meixi-connector/runtime/node' \
  '/Library/Application Support/meixi-connector/connector/connector-server.js'
```

If you are running from a source checkout instead of the packaged connector, use your local checkout path, for example:

```bash
node /path/to/web_collection/bridge/bridge-server.js
```

## Quick Start

### Option A: payload file

```bash
cat >/tmp/web-collect.json <<'JSON'
{
  "platform": "douyin",
  "method": "videoKeyword",
  "keywords": ["美食探店"],
  "maxItems": 10,
  "feature": "video",
  "mode": "search",
  "interval": 300,
  "fetchDetail": true,
  "detailSpeed": "fast",
  "autoExport": true,
  "exportMode": "personal"
}
JSON

{baseDir}/scripts/collect_and_export_loop.sh \
  --payload-file /tmp/web-collect.json \
  --base-url http://127.0.0.1:19820 \
  --ensure-bridge \
  --bridge-cmd "'/Library/Application Support/meixi-connector/runtime/node' '/Library/Application Support/meixi-connector/connector/connector-server.js'" \
  --force-stop-before-start
```

### Option B: direct flags

```bash
{baseDir}/scripts/collect_and_export_loop.sh \
  --platform douyin \
  --method videoKeyword \
  --keyword "美食探店" \
  --max-items 10 \
  --feature video \
  --mode search \
  --interval 300 \
  --fetch-detail true \
  --detail-speed fast \
  --auto-export true \
  --export-mode personal \
  --base-url http://127.0.0.1:19820 \
  --ensure-bridge \
  --bridge-cmd "'/Library/Application Support/meixi-connector/runtime/node' '/Library/Application Support/meixi-connector/connector/connector-server.js'"
```

When invoking from an agent tool runner, use a blocking exec with a generous timeout.
Do not use a background session unless the user explicitly asks for incremental progress updates.

## Script Options

```bash
{baseDir}/scripts/collect_and_export_loop.sh --help
```

Common runtime flags:

- `--base-url` default `http://127.0.0.1:19820`
- `--poll-sec` default `3`
- `--timeout-sec` default `1200`
- `--start-retries` default `3`
- `--idle-timeout-sec` default `180`
- `--ensure-bridge` auto-start bridge if `/api/status` is unreachable
- `--bridge-cmd` bridge startup command, required with `--ensure-bridge` if auto-detection is not available
- `--bridge-ready-timeout-sec` default `30`
- `--bridge-log` default `/tmp/web-collection-bridge.log`
- `--force-stop-before-start`

## Platform Methods

### Douyin (`platform=douyin`)

- `videoKeyword` (keywords)
- `creatorKeyword` (keywords)
- `creatorLink` (links)
- `creatorVideo` (links)
- `videoComment` (links)
- `videoInfo` (links)
- `videoLink` (links)

### TikTok (`platform=tiktok`)

- `keywordSearch` (keywords)
- `userVideo` (links)
- `tiktokComment` (links)
- `tiktokCreatorKeyword` (keywords)
- `tiktokCreatorLink` (links)

### Xiaohongshu (`platform=xiaohongshu`)

- `keywordSearch` (keywords)
- `creatorNote` (links)
- `creatorLink` (links)
- `creatorKeyword` (keywords)
- `noteLink` (links)
- `noteComment` (links)

## Troubleshooting

### `pluginConnected=false`

- Check bridge process and port.
- Reload extension at `chrome://extensions`.
- Recheck `GET /api/status`.

### status query returns nothing

- Check that you are querying the same base URL used by the collect command.
- Default bridge URL is `http://127.0.0.1:19820`.
- Do not switch to ad-hoc ports for `/api/tasks/<taskId>` unless the run explicitly used that port.

### `TASK_RUNNING`

- The script auto-recovers with `POST /api/stop` and retry.
- If it still fails, run once with `--force-stop-before-start`.
- If `running` stays stuck after `POST /api/stop`, restart the connector and browser extension, then retry.

### the agent replied before the task finished

- That is the wrong execution mode for this skill.
- Rerun with the direct closed-loop script and wait for exit.
- Do not use split-phase `start + process poll + intermediate reply` unless the user explicitly asked for progress updates.

### stuck at `exporting`

- Verify Feishu export config and permissions in extension settings.
- Ensure extension build supports export callback.
- Inspect task detail `error` and `export` fields.

### task completed but the reply missed the table link

- Treat that as an invalid final response.
- Rerun the final formatting step from the completed JSON.
- If `export.tableUrl` exists, it must be included.

## Manual API Fallback

Use only when debugging. For normal runs, prefer the bundled script.

```bash
curl -s http://127.0.0.1:19820/api/status
curl -s -X POST http://127.0.0.1:19820/api/collect -H 'Content-Type: application/json' -d '{...}'
curl -s http://127.0.0.1:19820/api/tasks/<taskId>
curl -s -X POST http://127.0.0.1:19820/api/stop
```
