---
name: theta-edgecloud-skill
description: Theta EdgeCloud API-key-first runtime scaffold with secure command-scoped auth and dry-run safety.
metadata:
  openclaw:
    homepage: https://docs.thetatoken.org/docs/edgecloud-api-keys
    primaryEnv: THETA_EC_API_KEY
    requires:
      env:
        - THETA_EC_API_KEY
        - THETA_EC_PROJECT_ID
---

# Theta EdgeCloud Skill (Cloud API Runtime)

## Credential scope model (important)
This skill is command-scoped: only provide the credentials needed for the command family you use.

- Controller/deployment/project commands: `THETA_EC_API_KEY`, `THETA_EC_PROJECT_ID`
- Balance command: add `THETA_ORG_ID`
- On-demand inference commands: `THETA_ONDEMAND_API_TOKEN` or `THETA_ONDEMAND_API_KEY`
- Inference endpoint commands: `THETA_INFERENCE_ENDPOINT` + auth (`THETA_INFERENCE_AUTH_TOKEN` or user/pass)

Credentials above are not globally required all at once.

## Quick setup (new users)
1) Log in at `https://www.thetaedgecloud.com/`.
2) Go to **Account -> Projects** and select your project.
3) Click **Create API Key** and copy the key.
4) Provide these on install/setup prompt:
   - `THETA_EC_API_KEY`
   - `THETA_EC_PROJECT_ID`
5) (Optional for on-demand image/video generation) create On-demand API key/token and set:
   - `THETA_ONDEMAND_API_KEY` (or `THETA_ONDEMAND_API_TOKEN`)

If a command says a key is missing, run `theta.auth.capabilities` to see exactly what to configure.

This runtime artifact is scoped to cloud API operations only.

## Security behavior (explicit)
- Runtime command handlers do not execute local shell commands.
- Runtime does not read local files for upload operations.
- Runtime does not call localhost/default local RPC endpoints.
- Runtime secret resolution uses OpenClaw secret provider first, then env fallback for:
  - `THETA_ONDEMAND_API_TOKEN`
  - `THETA_INFERENCE_AUTH_TOKEN`
  - `THETA_INFERENCE_AUTH_USER` / `THETA_INFERENCE_AUTH_PASS`
- Paid/mutating operations are user-triggered and can be gated by `THETA_DRY_RUN=1`.

## Credential model (what users actually need)
Users need a Theta EdgeCloud account with billing/credits enabled for paid operations.

Use only credentials required for the feature set you plan to call:

- Deployments API:
  - `THETA_EC_API_KEY`
  - `THETA_EC_PROJECT_ID`
- Dedicated inference endpoint:
  - `THETA_INFERENCE_ENDPOINT`
  - EITHER basic auth:
    - `THETA_INFERENCE_AUTH_USER`
    - `THETA_INFERENCE_AUTH_PASS`
  - OR bearer token auth:
    - `THETA_INFERENCE_AUTH_TOKEN`
- On-demand model API:
  - `THETA_ONDEMAND_API_TOKEN`
- Theta Video API:
  - `THETA_VIDEO_SA_ID`
  - `THETA_VIDEO_SA_SECRET`

## Runtime-only package
This ClawHub artifact is a dist/docs bundle intended for transparent inspection and low scanner surface.

## Env knobs (selected)
- `THETA_DRY_RUN`
- `THETA_EC_API_KEY`
- `THETA_EC_PROJECT_ID`
- `THETA_INFERENCE_ENDPOINT`
- `THETA_INFERENCE_AUTH_USER`
- `THETA_INFERENCE_AUTH_PASS`
- `THETA_INFERENCE_AUTH_TOKEN`
- `THETA_ONDEMAND_API_TOKEN`
- `THETA_HTTP_TIMEOUT_MS`
- `THETA_HTTP_MAX_RETRIES`
- `THETA_HTTP_RETRY_BACKOFF_MS`


## AI Services coverage
- On-demand model APIs: live discovery + infer/status/poll
- Dedicated deployments and template listing
- Jupyter notebook listing
- GPU node and GPU cluster listing
- Persistent storage listing
- Agentic AI (chatbot) listing

## Organization & Project scope
- Theta dashboard uses Organization + Project context.
- Runtime commands are project-scoped and require explicit `projectId` where relevant.
- Org membership/invite/session management endpoints are web-dashboard auth flows and not included in this skill runtime.


## API key vs user/password auth (validated)
- API key (`THETA_EC_API_KEY`) + project/org IDs can access project-scoped controller APIs and org balance.
- API key is sufficient for key runtime operations; dashboard username/password is not required for these flows.
- Username/password session auth is still required for account-management endpoints (org/project membership, invite, charge usage history APIs).


## On-demand API key alias
The runtime accepts either `THETA_ONDEMAND_API_TOKEN` or `THETA_ONDEMAND_API_KEY` for on-demand model API auth.


## Auth diagnostics
Use `theta.auth.capabilities` to quickly see which command families are available with the current credential set and which env vars are missing.


## First-run setup command
Use `theta.setup` to get a one-screen checklist for new users, including where to create API keys and which env vars to set.
