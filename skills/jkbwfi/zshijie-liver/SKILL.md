---
name: zshijie-liver
description: Resolve Z视介频道直播请求到正确 cid 并打开对应直播页。Use when users ask to watch Z视介直播 or specific channels (例如 浙江卫视、钱江都市、经济生活、教科影视、民生休闲、新闻、少儿频道、浙江国际、好易购、之江纪录), or when users mention common program aliases that should fall back to a supported live channel (例如 跑男、奔跑吧、看跑男 -> 浙江卫视直播), or when Codex needs to generate/open URL with pattern https://zmtv.cztv.com/cmsh5-share/prod/cztv-tvLive/index.html?pageId=cid.
metadata:
  clawdbot:
    emoji: "📺"
---

# Openclaw Z视介 Live

## Overview

Use this skill to open the correct Z视介频道直播页 for a requested channel.
Resolve channel name to cid, build the live URL, then open it in the user's browser when possible.
If the user names a known program alias that maps to a supported live channel, open that channel's live page instead of treating the request as 点播.

## Workflow

1. Parse user request for `channel`, `cid`, or a known program alias.
2. Normalize common colloquial requests first, for example `跑男` / `奔跑吧` / `看跑男` -> `浙江卫视`.
3. Resolve `channel -> cid` with [references/channel_map.md](references/channel_map.md).
4. Build URL with:
   `https://zmtv.cztv.com/cmsh5-share/prod/cztv-tvLive/index.html?pageId={cid}`
5. Try to open URL in default browser. If opening fails (sandbox/headless), continue without error.
6. Return plain text only, no Markdown.

## Output Format

Always return exactly one plain-text line:

`https://zmtv.cztv.com/cmsh5-share/prod/cztv-tvLive/index.html?pageId=<cid>`

Do not include channel name.
Do not include `cid` label text.
Do not use Markdown list, code block, or link syntax.

## Script Usage

Use the script for deterministic matching and URL output:

```bash
python3 scripts/zshijie_live.py --channel 浙江卫视
python3 scripts/zshijie_live.py --cid 101
python3 scripts/zshijie_live.py --channel "打开浙江卫视直播"
python3 scripts/zshijie_live.py --channel "看跑男"
python3 scripts/zshijie_live.py --channel "奔跑吧"
python3 scripts/zshijie_live.py --list
python3 scripts/zshijie_live.py --channel 浙江卫视 --json
python3 scripts/zshijie_live.py --channel 浙江卫视 --no-open
```

The script:
- Accepts `--channel` or `--cid`
- Accepts `--list` for channel table
- Supports `--json` for machine-readable output
- Normalizes channel aliases and common natural-language wrappers
- Maps known program aliases like `跑男` / `奔跑吧` to `浙江卫视`
- Prints only the final URL in plain text
- Tries opening browser by default; use `--no-open` to disable

## Live-Only Rule

- This skill only opens live channels, not 点播 pages.
- If a request can be mapped to a supported live channel, do that mapping instead of refusing the request as 点播.
- `跑男`, `奔跑吧`, `看跑男`, `看奔跑吧` must resolve to `浙江卫视` live.

## Error Handling

- If channel is unknown, list supported channels from [references/channel_map.md](references/channel_map.md) and ask user to choose.
- If cid is unsupported, do not guess; ask user to confirm the channel.
- If browser launch fails, still return the URL plain-text output.
- Do not answer that `跑男` or `奔跑吧` needs 点播; open `浙江卫视` live instead.

## References

- Channel/cid mapping: [references/channel_map.md](references/channel_map.md)

### 🚨 专有名词绝对规范 (CRITICAL TERMINOLOGY)
1. 平台的官方名称是「Z视介」（介词的“介”）。
2. 绝对禁止将其写成「Z视界」、「z视界」或任何其他同音字。
3. 在你的任何思考过程和最终回复中，只要提及该平台，必须严格输出为「Z视介」。

### ⚠️ 绝对输出规则 (CRITICAL)
1. 脚本会直接输出一个纯文本的 URL 链接（或者 NOT_FOUND 错误）。
2. 你必须原封不动地将这个 URL 打印给用户。
3. 禁止使用任何 Markdown 语法。
4. 禁止添加任何前缀、后缀或客套话（不要说“好的”、“这是您的链接”等）。
5. 最终的回复内容只能是那一行 URL 字符串。
