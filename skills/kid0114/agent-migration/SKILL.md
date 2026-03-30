---
name: agent-migration
description: Rename or migrate an OpenClaw agent by updating config and naming, migrating prior session content, fixing session display metadata, restarting, verifying, and only then asking whether to delete the old agent.
input: old agent id、new agent id、new workspace（optional model）
output: 新 agent 生效；旧会话内容已迁到新 agent；旧 agent 是否删除由用户最终确认
---

# Agent Migration

## What this skill does
This skill standardizes OpenClaw agent rename/migration work:
- rename the agent id
- rename the workspace path
- migrate prior session content to the new agent
- update session display metadata (`sessions.json` and related paths)
- restart and verify the new agent
- ask separately before deleting the old agent

## Typical ownership / permission level
- This skill is typically used by the **`master`** agent.
- It usually requires **higher local permissions** because it can modify:
  - `~/.openclaw/openclaw.json`
  - `~/.openclaw/agents/<id>/...`
  - `/home/yln/claw-workspace/<name>`
  - session metadata such as `sessions.json`
- It should be used carefully and should not silently delete old agents.

## Core rules
- Confirm old id, new id, new workspace, and whether model also changes.
- Update agent id, workspace, related config, and naming consistently.
- **Session content migration is required by default**, unless the user explicitly says not to migrate it.
- Do not use “active vs inactive session” as a reason to skip migration.
- Do not hard-edit active lock files or forcibly rewrite the live session shell.
- **Session display-layer metadata** (for example `sessions.json` fields such as `sessionKey`, `sessionFile`, `workspaceDir`, and related paths) must also be renamed.
- Restart is required after migration.
- **Deleting the old agent must always be asked separately.**

## Standard flow
1. Confirm names and target paths
2. Update config and naming
3. Migrate old session content to the new agent
4. Update session display metadata
5. Restart Gateway / OpenClaw
6. Verify UI, agent id, workspace, model, tools/skills, and migrated content
7. Ask separately whether to delete the old agent

## Included files
- `references/checklist.md`
- `references/cleanup.md`
- `scripts/inspect_agent_migration.sh`
- `scripts/copy_session_content.sh`
- `scripts/verify_agent_migration.sh`

## Recommended commands
```bash
bash skills/agent-migration/scripts/inspect_agent_migration.sh <old-id> <new-id>
bash skills/agent-migration/scripts/copy_session_content.sh <old-id> <new-id>
bash skills/agent-migration/scripts/verify_agent_migration.sh <old-id> <new-id>
```

## Do not
- Do not directly hard-rename a running agent and assume the UI will follow.
- Do not hard-migrate the active session shell.
- Do not skip content migration because a session “doesn’t look active”.
- Do not delete the old agent before asking again.
