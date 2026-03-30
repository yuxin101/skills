---
name: coding-prompt
version: "1.0.2"
description: AI coding prompt optimizer and coach. This skill should be used whenever the user is writing programming prompts or instructions to an AI during active coding sessions— including when starting new features, correcting AI's direction, reviewing code, or requesting tests. Trigger when: explicit request to optimize/improve/refine a prompt, the user activates this skill (激活编程提示词), or during coding tasks where instructions to AI are vague, missing constraints, missing acceptance criteria, or could benefit from prompt engineering best practices. Also trigger when the user says "更新技能" or "update skill" to evolve this skill's knowledge base. Do NOT trigger for non-coding prompts or general chat.
---

# Coding Prompt — AI 编程提示词最佳实践

> Activate: 激活编程提示词 | 优化提示词 | improve my prompt

## Purpose

This skill improves the quality of coding prompts sent to AI by diagnosing weaknesses,
applying proven principles, and proactively detecting common AI failure patterns during
active coding sessions.

## Table of Contents

| Section | Content | Location |
|---------|---------|----------|
| 1 | Prompt Diagnosis Checklist | `references/checklist.md` |
| 2 | Core Principles | `references/principles.md` |
| 3 | Communication Patterns | `references/patterns.md` |
| 4 | Workflow Templates | `references/templates.md` |
| 5 | Anti-Pattern Quick Reference | `references/anti-patterns.md` |
| 6 | Structural Wisdom | `references/structure.md` |
| 7 | Evolution Protocol | Below (this file) |

## How This Skill Works

This skill operates in **two modes**. Detailed rules are stored in `references/` files — load them **only when needed** per the instructions below.

### Mode 1: Explicit Optimization (100% reliable)

When explicit prompt optimization is requested — via trigger phrases, pasting a prompt for review, or prefacing an instruction with "优化提示词" — perform a **full diagnosis** and return a rewritten/improved version of the prompt.

**Trigger phrases**:
- `优化提示词: <your prompt>` — Rewrite the prompt following all principles
- `激活编程提示词` / `activate coding-prompt` — Enter active mode
- `improve my prompt` / `优化提示词` / `check my prompt`
- `prompt review` / `提示词审查`

**Before starting diagnosis, load all reference files**:
```
read_file(references/checklist.md)
read_file(references/principles.md)
read_file(references/patterns.md)
read_file(references/templates.md)
read_file(references/anti-patterns.md)
read_file(references/structure.md)
```
Then run through the checklist and apply principles to rewrite the prompt.

**Output format for optimization**:
```
## 原始提示词
<user's original prompt>

## 诊断结果
- D2 缺少约束: <what's missing>
- D4 缺少场景: <what's missing>

## 优化后的提示词
<rewritten prompt with improvements applied>
```

### Mode 2: Active Monitoring (high-priority signals only)

Once activated (Mode 1 triggered), the skill remains active for the rest of the session. In this mode, **proactively alert** when **only these high-priority signals** are detected:

| Alert | Signal | Response |
|-------|--------|----------|
| 🚨 **Fake completion** | D12 | AI claims "done" but code contains stubs/TODOs/placeholder returns/sample data. Append: `[coding-prompt] ⚠️ 检测到假完成：代码包含 <具体问题>，请替换为真实实现。` |
| 🚨 **Rule-based bias** | D11 | AI chooses hardcoded rules/regex/scoring when LLM-native would be better. Append: `[coding-prompt] ⚠️ 检测到规则匹配偏见：建议使用 LLM 原生能力替代硬编码 <具体规则>。` |

**For all other signals (D1-D10)**: Do NOT proactively interrupt. Only mention them if explicitly asked for a prompt review.

**Do NOT load reference files in Mode 2.** The rules above are sufficient for proactive monitoring.

**Session persistence note**: Mode 2 relies on conversation context. If context degradation is suspected (~10+ turns without explicit reference to active monitoring), re-confirm active status before issuing alerts.

**Golden rule**: The user's original instruction always takes priority. Alerts and suggestions are additive, never overriding.

**Evolution on demand**: When the user says "更新技能" / "update skill", follow Section 7 below.

---

## 7. Evolution Protocol / 进化协议

> Trigger: 更新技能 / update skill

### Step 1: Review

Analyze the current coding session for patterns, mistakes, or insights that could become new rules or improve existing ones.

### Step 2: Propose

Present a structured proposal with three sections:

```
## Proposed Changes

### Add (新增)
- [rule summary] — <brief reason>

### Modify (修改)
- [existing rule name]: <what to change> — <reason>

### Remove (删除)
- [existing rule name]: <reason for removal>
```

### Step 3: Confirm (MANDATORY)

**Wait for explicit user confirmation before making ANY changes.** This is the highest priority rule in this skill.

### Step 4: Output Change Proposal

After confirmation, output a **complete change proposal** — full file content with changes applied, clearly marked (e.g., `+` for added lines, `-` for removed lines). **Do NOT directly modify skill files at runtime.** The skill bundle is read-only during execution; changes must be applied by the user or the hosting platform.

1. Output the complete revised file content for each affected file (SKILL.md or references/)
2. Estimate the new total line count and issue a **warning** if it exceeds 500 lines (SKILL.md + all reference files combined)
3. If over 500 lines: include a consolidation suggestion (merge similar rules, remove redundancy) in the proposal
4. Indicate the new `version` value for SKILL.md frontmatter
5. Report: estimated new line count, files changed, and recommended version bump

### Anti-Bloat Guidelines

- **Soft limit**: ~500 lines total (SKILL.md + all references/ files combined). Exceeding this triggers a warning and consolidation suggestion, but does NOT block changes.
- **Prefer updating** existing rules over adding new ones
- **When adding**: evaluate if any existing rule can be merged or removed to make room
- **Example scope**: principles.md and anti-patterns.md may include Weak → Strong examples. Do NOT add verbose case studies or multi-paragraph narratives.
- **Periodic audit**: recommend reviewing all rules for relevance every 6 months
