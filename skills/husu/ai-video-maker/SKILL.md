---
name: aivideo-api-executor
description: Executes AIVideoMaker API workflows for text-to-video and image-to-video generation, including task creation, status polling, task details retrieval, and cancellation. Use when users ask to generate videos via API, monitor generation progress, cancel tasks, or automate AIVideoMaker API operations.
---




# AIVideoMaker API Executor

## Purpose
Provide a production-ready execution workflow for AIVideoMaker API v1:
- Create generation task
- Poll task status safely
- Fetch task details
- Cancel submitted task

## When To Use
- User asks to call `aivideomaker.ai` API directly
- User wants a scriptable generation workflow
- User needs robust retry/429 handling for task queries

## Required Environment
- `AIVIDEO_API_KEY` (required) Get an API Key from [https://aivideomaker.ai](https://aivideomaker.ai) .
- `AIVIDEO_BASE_URL` (optional, default `https://aivideomaker.ai`)
- `AIVIDEO_TIMEOUT_MS` (optional, default `30000`)
- `AIVIDEO_MAX_RETRIES` (optional, default `3`)

## Supported Actions
1. `createGeneration`
2. `getTask`
3. `getStatus`
4. `cancelTask`

## Model Whitelist
- `t2v`
- `i2v`
- `lv`
- `t2v_v3`
- `i2v_v3`

## Standard Workflow
1. Validate model and payload by contract.
2. Call `createGeneration`.
3. Poll `getStatus` with backoff until terminal status.
4. If `COMPLETED`, call `getTask` and return output.
5. If `FAILED`, return failure with actionable next steps.

## Error Policy
- Normalize all responses to:
  - `ok`, `status`, `taskId`, `data`, `errorCode`, `errorMessage`, `retryAfter`
- Map API/runtime errors into stable error codes:
  - `INVALID_MODEL`
  - `INVALID_PAYLOAD`
  - `AUTH_FAILED`
  - `RATE_LIMITED`
  - `INSUFFICIENT_CREDITS`
  - `TASK_NOT_FOUND`
  - `NETWORK_ERROR`
  - `UNKNOWN_ERROR`

## Execution Commands
- Run full workflow:
  - `node scripts/run-workflow.mjs --model t2v --input ./examples/t2v-input.json`
- Query status:
  - `node scripts/run-workflow.mjs --action getStatus --taskId <taskId>`
- Cancel task:
  - `node scripts/run-workflow.mjs --action cancelTask --taskId <taskId>`

## Additional Resources
- Full API matrix: [reference.md](reference.md)
- Usage and failure scenarios: [examples.md](examples.md)
