---
name: logicx-skill
description: Call LogicX frontend proxy APIs from OpenClaw for health checks, browser binding, password login, user info, orders, payments, and account actions.
---

# LogicX Skill

Use the LogicX frontend proxy as the only API surface.

## Rules

- Call `/api/proxy/*`, not backend `/v1/*`.
- Prefer `scripts/logicx_api.sh` over ad-hoc `curl`.
- Default to browser binding. Only ask for email and password if the user explicitly chooses password login.
- Ask before mutating calls such as `payment/create`, `payment/cancel`, `auth/change-password`, or `agent/unlink`.
- Treat `LOGICX_AGENT_SERVICE_KEY` and `LOGICX_USER_TOKEN` as secrets. Never echo them in full.
- The official skill uses built-in `openclaw-public` key. Never ask the end user for any key.
- Never infer binding, membership, order, or payment state. Report API responses only.

## Runtime Config

**Official skill: users need no config.** The script uses built-in defaults:

- `LOGICX_BASE_URL` — defaults to `https://logicx.ai`; override for custom deployment
- `LOGICX_AGENT_SERVICE_KEY` — defaults to `openclaw-public` (LogicX backend accepts this for the official OpenClaw skill)

User-scoped calls also need:

- `LOGICX_USER_TOKEN` — obtained after binding or password login (script auto-loads from state file)

**Optional override (e.g. for self-hosted LogicX):**

```json5
{
  "LOGICX_BASE_URL": "http://your-logicx-host:8070"
}
```

**Fallback state file (when OpenClaw does not persist per-user state):**

- `logicx_api.sh` auto-saves `link_code` and `install_id` after `agent/link/start`, and `user_token` after `agent/link/status` or `agent/auth/login` succeeds
- When `LOGICX_USER_TOKEN` is not set, the script reads it from the state file
- When the user says "我登录好了", run `scripts/check_link_status.sh` — it reads from the state file and calls `agent/link/status`
- Default path: `~/.config/logicx/skill-state.json`. Override with `LOGICX_STATE_FILE`

## Responsibilities

This integration works only if all three layers do their part:

- Platform: optional override of `LOGICX_BASE_URL` (default: `https://logicx.ai`)
- Skill: decide the next API call and the correct user-facing reply
- OpenClaw runtime: persist per-user auth state such as `install_id`, `link_code`, and `user_token`

Do not rely on the model to remember auth state across turns. Persist it in runtime state.

## Auth Model

No user token required:

- `GET /api/health`
- `POST /api/proxy/agent/link/start`
- `POST /api/proxy/agent/link/status`
- `POST /api/proxy/agent/auth/login`

User-scoped calls require both headers:

- `Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>`
- `X-LogicX-User-Token: <LOGICX_USER_TOKEN>`

Do not call `agent/link/confirm` from the agent. It is part of the browser-side flow after the user opens the login link.

## Default Operating Flow

1. If connectivity is uncertain, run `GET /api/health`.
2. If the request needs a user token and no token is available, first ensure `LOGICX_AGENT_SERVICE_KEY` is present and valid, then offer two login paths:
   - default: browser binding with user confirmation
   - fallback: agent password login
3. When `agent/link/start` succeeds, persist the pending bind state for the current OpenClaw user:
   - `install_id`
   - `link_code`
   - `status=pending`
4. After obtaining a token, persist it as the current user's LogicX login state, then verify it with `GET user`.
5. Run the requested user action.
6. Summarize the result in natural language unless the user asks for raw JSON.

If the API returns `Agent service key required` or `Unauthorized`, the LogicX backend may not accept the public key yet. Ask the user to try again later or contact LogicX support.

## Login Path 1: Browser Binding with User Confirmation

Preferred path. No password needed in chat.

Start binding:

```bash
{baseDir}/scripts/logicx_api.sh POST agent/link/start '{"install_id":"openclaw-main"}'
```

The script auto-saves `link_code` and `install_id` to the state file so they persist across turns.
Reply to the user with the returned `login_url` and clearly offer both login options.

Preferred reply style:

```text
你可以点击以下链接登录并完成授权：

<login_url>

登录完成后请回来告诉我一声，比如直接回复“我登录好了”。

如果你不想跳转浏览器，也可以直接把用户名和密码告诉我，我可以直接帮你登录。
```

After the user says they have finished logging in, run `check_link_status.sh`. It reads `link_code` and `install_id` from the state file and calls `agent/link/status`:

```bash
{baseDir}/scripts/check_link_status.sh
```

If the script fails with "No bind state found", the user must restart with `agent/link/start`.

Interpretation:

- `pending`: tell the user the browser-side confirmation may not be complete yet and ask them to confirm they finished authorization, then let them reply again when ready
- `expired`: stop and ask the user whether to restart binding
- `confirmed`: persist the returned `user_token` for the current OpenClaw user and continue

After `confirmed`, verify the token:

```bash
{baseDir}/scripts/logicx_api.sh GET user
```

## Login Path 2: Agent Password Login

Use only when the user explicitly chooses not to use the browser flow.

```bash
{baseDir}/scripts/logicx_api.sh POST agent/auth/login \
  '{"email":"user@example.com","password":"secret","install_id":"openclaw-main"}'
```

On success, store the returned `user_token` for the current runtime, then verify it:

```bash
{baseDir}/scripts/logicx_api.sh GET user
```

Limits: 5 attempts per 15 minutes per IP + email. If the API returns `429`, tell the user to wait before retrying.

## Runtime State Contract

OpenClaw should keep per-user auth state outside the markdown skill. Recommended fields:

```json
{
  "install_id": "openclaw-main",
  "link_code": "lc_xxx",
  "user_token": "at_xxx",
  "status": "pending | confirmed"
}
```

Rules:

- Save `install_id` and `link_code` immediately after `agent/link/start`
- Replace pending state with `user_token` after `agent/link/status` returns `confirmed`
- Reuse the saved `user_token` for later user-scoped requests
- If later user-scoped calls return auth failure, clear the saved `user_token` and restart binding

## Common Calls

```bash
{baseDir}/scripts/logicx_api.sh GET /api/health
{baseDir}/scripts/logicx_api.sh GET user
{baseDir}/scripts/logicx_api.sh GET payment/orders
{baseDir}/scripts/logicx_api.sh POST payment/create '{"plan":"pro_monthly","gateway":"mock"}'
{baseDir}/scripts/logicx_api.sh GET payment/orders/ORDER_NO
{baseDir}/scripts/logicx_api.sh POST payment/cancel '{"orderNo":"ORDER_NO"}'
{baseDir}/scripts/logicx_api.sh POST auth/change-password '{"currentPassword":"old-password","newPassword":"new-password-min-8-chars"}'
{baseDir}/scripts/logicx_api.sh POST agent/unlink '{"install_id":"INSTALL_ID"}'
```

## Connectivity

```bash
{baseDir}/scripts/logicx_api.sh GET /api/health
```

If health works but user calls fail, check `LOGICX_USER_TOKEN`. If auth fails globally (e.g. `Agent service key required`), the LogicX backend may need to enable the public key.

## References

- `references/api-reference.md`
- `examples.md`

## Constraints

- Browser login is cookie-based. Do not try to recreate it in chat.
- Email change is not a confirmed skill capability. Do not promise it.
- The confirmed account mutation is password change.
- Do not persist user tokens in this skill folder. The fallback state file (`~/.config/logicx/skill-state.json`) is outside the skill and is acceptable.
