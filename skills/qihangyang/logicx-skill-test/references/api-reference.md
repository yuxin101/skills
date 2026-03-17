## API Surface

LogicX exposes a frontend proxy. Use:

- Health: `/api/health`
- Business APIs: `/api/proxy/*`

Do not call backend `/v1/*` endpoints directly from this skill.

## Auth Rules

The official skill uses `openclaw-public` as the default agent key. LogicX backend accepts it for the public OpenClaw integration.

### Health

```http
GET /api/health
```

No auth required.

### Agent bind start

```http
POST /api/proxy/agent/link/start
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
Content-Type: application/json

{"install_id":"openclaw-main"}
```

Response:

```json
{
  "link_code": "lc_xxx",
  "login_url": "https://logicx.ai/agent/link?code=lc_xxx"
}
```

### Agent bind status (poll)

```http
POST /api/proxy/agent/link/status
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
Content-Type: application/json

{"link_code":"lc_xxx","install_id":"openclaw-main"}
```

Responses:

```json
{"status":"pending"}
{"status":"expired"}
{"status":"confirmed","user_token":"at_xxx"}
```

This endpoint supports polling, but this skill should not background-poll by default. Instead, ask the user to finish browser authorization and reply when ready, then check status. If `confirmed`, persist the returned `user_token` for that OpenClaw user. Link codes expire after 10 minutes.
Use the same `install_id` for `agent/link/start` and `agent/link/status`.

### Agent password login

```http
POST /api/proxy/agent/auth/login
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
Content-Type: application/json

{"email":"user@example.com","password":"secret","install_id":"openclaw-main"}
```

Response:

```json
{"ok":true,"user_token":"at_xxx"}
```

Rate limited: 5 attempts per 15 minutes per IP + email. Returns `429` if exceeded.

### User-scoped calls

Use both headers:

```http
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
X-LogicX-User-Token: <LOGICX_USER_TOKEN>
```

## Confirmed Calls

### Current user

```http
GET /api/proxy/user
```

Response:

```json
{
  "id": "user_xxx",
  "email": "user@example.com",
  "createdAt": "2026-01-01T00:00:00.000Z",
  "role": "user",
  "plan": "free",
  "proExpiresAt": null,
  "maxExpiresAt": null
}
```

Use `GET /api/proxy/user` as the canonical read endpoint. Avoid the trailing-slash form in this skill.

`PATCH /api/proxy/user/` is listed in the frontend README, but this skill should not invent a profile patch schema. Treat email as immutable unless the backend contract is explicitly confirmed.

### Orders and payment

```http
POST /api/proxy/payment/create
GET /api/proxy/payment/orders
GET /api/proxy/payment/orders/:orderNo
POST /api/proxy/payment/mock-confirm
POST /api/proxy/payment/cancel
```

`POST /payment/create` request:

```json
{"plan":"pro_monthly","gateway":"mock"}
```

Order shape:

```json
{
  "id": "ord_xxx",
  "orderNo": "202603160001",
  "plan": "pro_monthly",
  "amount": 2900,
  "gateway": "mock",
  "status": "pending",
  "expiresAt": "2026-03-16T12:00:00.000Z",
  "confirmedAt": null,
  "cancelledAt": null,
  "createdAt": "2026-03-16T11:58:00.000Z"
}
```

Allowed status values: `pending`, `confirmed`, `cancelled`, `expired`

### Password change

```http
POST /api/proxy/auth/change-password
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
X-LogicX-User-Token: <LOGICX_USER_TOKEN>
Content-Type: application/json
```

Request:

```json
{"currentPassword":"old-password","newPassword":"new-password-min-8-chars"}
```

### Agent unlink

```http
POST /api/proxy/agent/unlink
Authorization: Bearer <LOGICX_AGENT_SERVICE_KEY>
X-LogicX-User-Token: <LOGICX_USER_TOKEN>
Content-Type: application/json

{"install_id":"openclaw-main"}
```

## Notes

- Browser login is cookie-based; use agent binding or password login instead.
- Recommended binding flow: `agent/link/start` -> save `install_id` + `link_code` -> user opens browser and confirms -> user replies "我登录好了" -> agent checks `agent/link/status` -> save `user_token`.
- After either login path succeeds, verify the token with `GET /api/proxy/user`.
- `400` on `agent/link/confirm` usually means the `link_code` expired or was already consumed.
- `429` on `agent/auth/login` means rate limit exceeded; wait 15 minutes.
- Auth failures usually mean a bad service key or missing/invalid user token.
