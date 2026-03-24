---
name: aivideo-api-executor
description: Executes AIVideoMaker API workflows for text-to-video and image-to-video generation, including task creation, status polling, task detail retrieval, and cancellation. Use when users ask to generate videos via API, monitor generation progress, cancel tasks, or automate AIVideoMaker API operations.
---

# AIVideoMaker API Executor

Run production-grade AIVideoMaker API v1 workflows with input validation, retry handling, and stable output shape.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Create a new generation and wait for completion | Run `scripts/run-workflow.mjs` with `--model` and `--input` |
| Check task progress only | Use `--action getStatus --taskId <taskId>` |
| Retrieve final task details | Use `--action getTask --taskId <taskId>` |
| Cancel a queued task | Use `--action cancelTask --taskId <taskId>` |
| Upstream returns `429` | Honor `Retry-After`, then retry idempotent reads |
| Upstream returns credits error | Map to `INSUFFICIENT_CREDITS` and return suggestions |

## Capabilities
- Create generation task via `POST /api/v1/generate/{model}`
- Poll status via `GET /api/v1/tasks/{taskId}/status`
- Get task details via `GET /api/v1/tasks/{taskId}`
- Cancel task via `PUT /api/v1/tasks/{taskId}/cancel`
- Normalize output for all actions

## Required Environment
- `AIVIDEO_API_KEY` (required) Get an API Key from [https://aivideomaker.ai](https://aivideomaker.ai) .
- `AIVIDEO_TIMEOUT_MS` (optional, default `30000`)
- `AIVIDEO_MAX_RETRIES` (optional, default `3`)

## Model Whitelist
- `t2v`
- `i2v`
- `lv`
- `t2v_v3`
- `i2v_v3`

## Standard Workflow
1. Validate model and payload using `scripts/contract.mjs`.
2. Submit generation task.
3. Poll task status with bounded backoff.
4. On `COMPLETED`, fetch final details and return.
5. On `FAILED`/`CANCEL`, return actionable suggestions.

## Error Policy
- Standard response fields: `ok`, `status`, `taskId`, `data`, `errorCode`, `errorMessage`, `retryAfter`, `httpStatus`, `timestamp`
- Stable error codes:
  - `INVALID_MODEL`
  - `INVALID_PAYLOAD`
  - `AUTH_FAILED`
  - `RATE_LIMITED`
  - `INSUFFICIENT_CREDITS`
  - `TASK_NOT_FOUND`
  - `NETWORK_ERROR`
  - `UNKNOWN_ERROR`
  - `POLL_TIMEOUT`

## Security Notes
- API key is read from environment, never hardcoded.
- Request logs redact API key.
- URL query parameters are removed from debug logs.
- Retry logic applies to idempotent read operations only.

## Execution Commands

Run create-and-poll flow:
```bash
node scripts/run-workflow.mjs --model t2v --input ./examples/t2v-input.json
```

Read-only status check:
```bash
node scripts/run-workflow.mjs --action getStatus --taskId <taskId>
```

Cancel task:
```bash
node scripts/run-workflow.mjs --action cancelTask --taskId <taskId>
```

## Additional Resources
- API details: [references/api-reference.md](references/api-reference.md)
- Usage scenarios: [references/examples.md](references/examples.md)