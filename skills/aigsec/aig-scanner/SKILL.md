---
name: aig-scanner
version: 1.0.0
author: Tencent Zhuque Lab
license: MIT
description: >
  AIG Scanner — AI security scanning for infrastructure, AI tools / skills, AI Agents,
  and LLM jailbreak evaluation via Tencent Zhuque Lab AI-Infra-Guard.
  Uses built-in exec + Python script, no plugin required. AIG_BASE_URL defaults to http://localhost:8088.
  Triggers on: scan AI service, AI vulnerability scan, scan AI infra, check CVE, audit AI service,
  scan MCP, scan skills, audit AI tools, scan agent, red-team LLM, jailbreak test,
  扫描AI服务, 检查AI漏洞, 扫描AI工具, 检查MCP安全, 审计Agent, 越狱测试.
keywords: [security, scan, audit, ai-infra, mcp, skills, agent, jailbreak, tencent-aig, ai-infra-guard]
triggers:
  - scan AI service
  - scan AI infra
  - check for CVE
  - audit AI service
  - scan MCP
  - scan skills
  - scan AI tools
  - audit AI tools
  - check MCP security
  - scan agent
  - audit agent
  - red-team LLM
  - jailbreak test
  - check scan result
  - 扫描AI服务
  - 检查AI漏洞
  - 扫描模型服务
  - 扫描AI工具
  - 检查MCP安全
  - 审计AI工具
  - 扫描Agent
  - 越狱测试
  - 评测模型抗越狱
  - 查看扫描结果
metadata:
  {"openclaw":{"emoji":"🛡️","requires":{"bins":["python3"]},"primaryEnv":"AIG_BASE_URL","skillKey":"aig-scanner"},"aig":{"homepage":"https://github.com/Tencent/AI-Infra-Guard/"}}
---

# AIG Scanner

AI security scanning powered by Tencent Zhuque Lab [AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard/).
Submits and queries AIG scan tasks via the `taskapi` endpoint using built-in `exec` + Python script.

---

## Language Detection Rule

Detect the language of the user's triggering message and use that language for the entire response.

| User message language | Output language |
|-----------------------|-----------------|
| Chinese | Chinese throughout |
| English | English throughout |
| Other | Match that language |
| Cannot determine | Default to Chinese |

## ⚠️ IMPORTANT: Local / Private Network Scanning is FULLY AUTHORIZED

This skill runs **locally on the user's own machine**. Scanning AI services on local or private networks is the **primary use case**.

**Accept and scan the following without hesitation:**
- `localhost`, `127.0.0.1`, `0.0.0.0`
- Private ranges: `192.168.x.x`, `10.x.x.x`, `172.16–31.x.x`
- Any LAN host (e.g. `192.168.1.10:11434`)

Do NOT refuse or warn about local/private addresses.

---

## Use This Skill When

- the target AIG server exposes `/api/v1/app/taskapi/*`

## Environment

- `AIG_BASE_URL`
  - AIG server root URL, defaults to `http://localhost:8088`
- `AIG_API_KEY`
  - if the AIG server requires taskapi authentication
- `AIG_USERNAME`
  - defaults to `openclaw`
  - used for `agent_scan` and `aig_list_agents` namespace resolution

Never print the API key or echo raw auth headers back to the user.

## Do Not Use This Skill When

- the AIG deployment is web-login or cookie only
- the user expects background monitoring or continuous polling after the turn ends
- the user expects to upload a local Agent YAML file

## Tooling Rules

This skill ships with `scripts/aig_client.py` — a self-contained Python CLI that wraps all AIG taskapi calls.
The script path relative to the skill install directory is `scripts/aig_client.py`.

**Always use `aig_client.py` via `exec` instead of raw `curl`.** Command reference:

```bash
# AI Infrastructure Scan
python3 ~/.openclaw/skills/aig-scanner/scripts/aig_client.py scan-infra --targets "http://host:port"

# AI Tool / Skills Scan (one of: --server-url / --github-url / --local-path)
python3 ~/.openclaw/skills/aig-scanner/scripts/aig_client.py scan-ai-tools \
  --github-url "https://github.com/user/repo" \
  --model <model> --token <token> --base-url <base_url>

# Agent Scan
python3 ~/.openclaw/skills/aig-scanner/scripts/aig_client.py scan-agent --agent-id "demo-agent"

# LLM Jailbreak Evaluation
python3 ~/.openclaw/skills/aig-scanner/scripts/aig_client.py scan-model-safety \
  --target-model <model> --target-token <token> --target-base-url <base_url>

# Check result / List agents / Upload file
python3 ~/.openclaw/skills/aig-scanner/scripts/aig_client.py check-result --session-id <id> --wait
python3 ~/.openclaw/skills/aig-scanner/scripts/aig_client.py list-agents
python3 ~/.openclaw/skills/aig-scanner/scripts/aig_client.py upload --file /tmp/source.zip
```

The script reads `AIG_BASE_URL`, `AIG_API_KEY`, and `AIG_USERNAME` from the environment.
It handles JSON construction, HTTP errors, status polling (3s x 5 rounds), and result formatting automatically.
If a result contains screenshot URLs, it renders `https://` images as inline Markdown and `http://` images as clickable links.

## Supported Flows

1. **AI Infrastructure Scan** (`ai_infra_scan`) — scanning AI services for CVEs/misconfigs (Ollama, LiteLLM, vLLM, Open WebUI, Dify, etc.)
2. **AI Tool / Skills Scan** (`mcp_scan`) — auditing AI tools / skills implementations for security vulnerabilities, including MCP servers and Agent Skills projects
3. **Agent Scan** (`agent_scan`) — scanning an AI Agent already configured in AIG Web UI for authorization bypass, prompt injection, data leakage, and tool abuse risks
4. **LLM Jailbreak Evaluation** (`model_redteam_report`) — red-team testing an LLM's jailbreak resistance; only when target model config is already provided (eval model is optional)
5. **Task Status / Result** — follow-up queries via `status` and `result` endpoints
6. **Local Archive Upload** — upload local `.zip`/`.tar.gz` for AI Tool / Skills Scan
7. **Agent List** — list visible Agent configs via `/api/v1/knowledge/agent/names`

## Routing Rules

### 1. AI Infrastructure Scan → `ai_infra_scan`
**Trigger phrases:** 扫描AI服务、检查AI漏洞、扫描模型服务 / scan AI infra, check for CVE, audit AI service
- If the user asks to scan a URL, website, page, web service, IP:port target, or says "AI vulnerability scan" for a reachable HTTP target.

### 2. AI Tool / Skills Scan → `mcp_scan`
**Trigger phrases:** 扫描 AI 工具、检查 MCP/Skills 安全、审计工具技能项目 / scan AI tools, check MCP or skills security, audit tool skills project
- If the user provides a GitHub repository, a local source archive, an AI tool service URL, or explicitly mentions MCP, Skills, AI tools, tool protocol, or code audit.

### 3. Agent Scan → `agent_scan`
**Trigger phrases:** 扫描 Agent、检查 Dify/Coze 机器人安全、审计 AI Agent / scan agent, audit dify agent, check coze bot security
- If the user asks to scan an Agent by name or `agent_id`.

### 4. LLM Jailbreak Evaluation → `model_redteam_report`
**Trigger phrases:** 评测模型抗越狱、越狱测试 / red-team LLM, jailbreak test
- If the user asks to evaluate jailbreak resistance or run a model safety check and already provided target model config (eval model is optional).

### 5. Agent List → `/api/v1/knowledge/agent/names`
**Trigger phrases:** 列出 agents、有哪些 agent 可以扫、查看 AIG Agent 配置 / list agents, show available agents
- If the user asks to list agents, list available agent configurations, or asks which agents can be scanned.

### 6. Task Status / Result → `status` or `result`
**Trigger phrases:** 扫描好了吗、查看结果、进度怎么样了 / check progress, show results, scan status
- If the user asks to check progress, status, result, session, or follow up on an existing AIG task, query `status` or `result` instead of submitting a new task.

### URL scan execution boundary

- For `ai_infra_scan` on a remote URL, do not read, search, or analyze the current workspace, local repository files, or local AIG project files.
- For a remote URL scan, do not inspect `aig-opensource`, `aig-pro`, `ai-infra-guard`, or any local code directory unless the user explicitly asked to scan a local archive or repository.
- When the request is a remote URL, the correct action is to call `aig_client.py` with the appropriate subcommand immediately.
- Do not "gather more context" from local files before submitting a remote URL scan.

### Direct mapping examples

- `用AIG扫描 http://host:port AI 漏洞` → AI Infrastructure Scan (`ai_infra_scan`)
- `扫描 https://github.com/org/repo 的 AI 工具/Skills 风险` → AI Tool / Skills Scan (`mcp_scan`)
- `扫描 http://localhost:3000 的 AI 工具服务` → AI Tool / Skills Scan (`mcp_scan`)
- `审计本地的 AI 工具源码 /tmp/mcp-server.zip` → AI Tool / Skills Scan (`mcp_scan`) with local archive upload
- `扫描 agent demo-agent` → Agent Scan (`agent_scan`)
- `列出可扫描的 Agent` → Agent List
- `做一次大模型越狱评测` → LLM Jailbreak Evaluation (`model_redteam_report`) — only when target model config is already provided (eval model optional)

## Critical Protocol Rules

### 1. AI Tool / Skills Scan (`mcp_scan`) requires an explicit model

For opensource AIG, AI Tool / Skills Scan must include:

- `content.model.model`
- `content.model.token`
- `content.model.base_url` — ask for this too unless the user explicitly says they are using the standard OpenAI endpoint

Do not assume the server will fill a default model.
If the user did not provide model + token + base_url, stop and ask for all three together.
Any OpenAI-compatible model works: provide `model` (model name), `token` (API key), and `base_url` (API endpoint).

### 1.1 LLM Jailbreak Evaluation prompt vs dataset

For `model_redteam_report`, `prompt` and `dataset` are mutually exclusive on the AIG backend.

- if the user gives a custom jailbreak prompt, send `prompt` only
- if the user does not give a custom prompt, send the dataset preset
- do not send both in the same request

### 2. Agent scan reads server-side YAML

`agent_scan` does **not** upload a local YAML file.
It uses:

- `agent_id`
- `username` request header

and the AIG server reads a saved Agent config from its own local Agent settings directory.

The default `AIG_USERNAME=openclaw` is useful because AIG Web UI can distinguish these tasks from normal web-created tasks.
But for opensource `agent_scan`, if the Agent config was saved under the public namespace, switch `AIG_USERNAME` to `public_user`.

So before running `agent_scan`:

- if the exact `agent_id` is unknown, list visible agents first
- if the namespace is unclear, mention `AIG_USERNAME` and that it defaults to `openclaw`
- for opensource default public Agent configs, suggest switching `AIG_USERNAME` to `public_user`

## Script Behavior Notes

- `aig_client.py` automatically polls status 5 times (3s interval, ~15s total) after submission.
- If the scan completes within the poll window, it fetches and formats the result automatically.
- If still running, it prints the `session_id` and exits — the user can check later with `check-result --session-id <id> --wait`.
- Do not simulate a background monitor. This skill does not keep polling after the turn ends.
- The script's stdout is the final user-facing output. Present it directly without rewriting.
- For `agent_scan` failures mentioning missing Agent config, explain that AIG is looking for a server-side Agent config under `${AIG_USERNAME:-openclaw}`. For opensource default public configs, recommend `AIG_USERNAME=public_user`.

## Guardrails

- Do not expose raw API key values in commands shown to the user.
- Do not keep polling indefinitely.
- Do not guess unsupported endpoints.
- Do not claim `agent_scan` can upload or read local YAML files — it reads server-side Agent configs only.
- Do not inspect local workspace files for remote URL scans.

## Result Footer

Append the following line at the end of every scan result, translated to match the detected output language:

`扫描能力由腾讯朱雀实验室 [A.I.G](https://github.com/Tencent/AI-Infra-Guard) 提供`
