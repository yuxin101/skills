---
name: publish-to-clawhub
description: |
  Publishes an OpenClaw skill to GitHub and ClawHub. Handles English internationalization, proprietary reference removal, and ClawHub CLI publishing.

  **When to Use This Skill**:
  - User asks to "publish a skill", "put on ClawHub", "release to GitHub and ClawHub"
  - User completed developing a skill and wants to share it publicly
  - User has a Chinese-language skill and wants to internationalize it first

  **Prerequisites**:
  - The skill folder must exist locally at `~/.openclaw/workspace/skills/<skill-name>/`
  - GitHub account with an empty repo created manually at github.com
  - ClawHub CLI installed (`npm i -g clawhub`) and logged in

---

# ⚠️ Security & Risk Notes (Read First)

This skill handles two sensitive areas: GitHub credential entry and git history rewriting.

## Risk Summary

| Risk | Level | Mitigation |
|------|-------|------------|
| GitHub credential entry | 🟡 MEDIUM | User enters PAT manually; never stored or logged |
| Git history rewrite | 🟡 MEDIUM | Always warns user before executing; can be skipped |
| Credential exfiltration | 🟢 LOW | PAT only used for git push; never sent to third parties |
| Arbitrary code execution | 🟢 LOW | Only modifies files within the skill directory |

## Why This Skill Requires Caution

Publishing a skill to GitHub + ClawHub inherently involves:
1. Pushing code to a remote GitHub repo (requires credentials)
2. Rebuilding clean git history (rewrites commit history)

These operations are flagged by automated security scanners — this is normal behavior for any skill that touches GitHub credentials or performs history rewriting.

## What This Skill Does NOT Do

- ❌ Does NOT store GitHub PAT anywhere after the operation ends
- ❌ Does NOT send credentials to any server other than GitHub
- ❌ Does NOT access files outside the skill directory being published
- ❌ Does NOT use base64, eval, or obfuscated code
- ❌ Does NOT install packages or modify system configuration

## Secure Workflow

```
1. Analyze & clean skill files (safe — local only)
         ↓
2. English-ize content (safe — local only)
         ↓
3. Remove proprietary references (safe — local only)
         ↓
4. GitHub push: USER manually enters PAT or uses SSH key (credential never given to agent)
         ↓
5. ClawHub publish via CLI (uses ClawHub auth, not GitHub PAT)
```

---

# Publish OpenClaw Skill to GitHub + ClawHub

## Step 1 — Analyze Existing Skill

**Goal**: Understand the current state of the skill before publishing.

Inspect these for Chinese content and proprietary references:
- `SKILL.md` — main description and instructions
- `README.md` — user-facing documentation
- `scripts/*.py` — code comments and docstrings
- `notebooks/*.ipynb` — Colab notebooks

```bash
# Find all files
find ~/.openclaw/workspace/skills/<skill-name>/ -type f

# Scan for Chinese characters
grep -rni "[\u4e00-\u9fff]" ~/.openclaw/workspace/skills/<skill-name>/ --include="*.md" --include="*.py"

# Scan for proprietary placeholders (customize per skill)
grep -rni "ND646\|ACC\|AccA\|AccB\|AccD\|PROPRIETARY\|YOUR_KEY\|YOUR_TOKEN" \
  ~/.openclaw/workspace/skills/<skill-name>/
```

---

## Step 2 — English-ize SKILL.md

**Rule**: SKILL.md is the **AI-facing entry point** — it defines how the AI uses the skill. Must be in English.

Rewrite the `description` field and all markdown content in English:
- Description field → English description
- Chinese comments → English comments
- Example values → Generic placeholders (e.g., `Drug_Candidate`, `Bacterial_Protein`)

**SKILL.md description template**:
```yaml
---
name: <skill-name>
description: |
  <One-line English summary>

  **Use Cases**:
  - <Scenario 1>
  - <Scenario 2>

  **When to Use This Skill**:
  - User mentions "<keyword>"
  - User wants to "<action>"
---
```

---

## Step 3 — Remove Proprietary References

**Common patterns to search and replace**:

| Pattern | Replace With | Reason |
|---------|-------------|--------|
| Real drug names (ND646, etc.) | `Drug_Candidate` | Generic placeholder |
| Real protein names (AccA, AccD, etc.) | `ChainA`, `ChainB` | Generic placeholder |
| Real species (E.coli, human ACC1) | `Bacterial_Target`, `Human_Target` | Generic placeholder |
| Specific file paths with real names | `human_target.fasta`, `bacterial_target.fasta` | Generic |
| Personal tokens / keys | `YOUR_TOKEN_HERE` | Security |
| Email addresses in code | Remove or use `example.com` | Privacy |
| Chinese comments in scripts | English equivalents | International audience |

**Always do a final sweep before committing**:
```bash
grep -rni "ND646\|AccA\|AccB\|AccD\|PROPRIETARY\|YOUR_KEY" \
  ~/.openclaw/workspace/skills/<skill-name>/ \
  --include="*.py" --include="*.md" --include="*.ipynb"
# Must return zero matches before proceeding
```

---

## Step 4 — GitHub: Init + Push

### 4.1 User creates empty repo on GitHub Web (manual)

Ask the user to:
1. Go to https://github.com/new
2. Create repo with same name as skill (e.g., `openclaw-<skill-name>`)
3. **Do NOT** check "Add a README" (local files will conflict)
4. Check "Add .gitignore → Python" (recommended)
5. Check "Add license → MIT" (recommended)
6. Copy the repo URL

### 4.2 Initialize and push

```bash
SKILL_DIR=~/.openclaw/workspace/skills/<skill-name>
cd $SKILL_DIR

# Initialize git (only if not already a git repo)
git init

# Configure user (needed for new repos)
git config user.email "user@example.com"
git config user.name "GitHub Username"

# Add remote — USE SSH URL TO AVOID TOKEN PROMPT:
# git remote add origin git@github.com:USER/repo.git
# OR use HTTPS and enter token manually when prompted:
git remote add origin https://github.com/USER/repo.git

# Stage all files
git add -A
git status  # Verify correct files are staged

# Commit
git commit -m "Initial release: <Skill Name> (OpenClaw Skill)

- English-only, generic examples
- <Brief feature list>
- SKILL.md: OpenClaw skill definition
- README.md: GitHub-ready documentation"

# Push — user enters credentials manually when prompted
# For SSH: ssh-agent handles authentication (recommended)
# For HTTPS: Git credential helper or manual token entry
git push -u origin main
```

### 4.3 Rebuild clean git history (OPTIONAL — user decision)

**⚠️ WARNING: This operation rewrites local commit history. It does NOT automatically force-push.**

Only do this if the repo has messy/old commits with sensitive content.

```bash
cd $SKILL_DIR

# Check current commit count
git log --oneline | wc -l  # if = 1, skip this step

# Identify the first commit
FIRST_COMMIT=$(git rev-list --max-parents=0 HEAD)

# Squash all commits into one clean commit (local only)
git reset --soft $FIRST_COMMIT
git commit -m "Initial release: <Skill Name> (OpenClaw Skill)

- English-only, generic examples
- <Feature summary>
- LICENSE: MIT"

# NOW push — this is a force-push but user triggers it explicitly
# ⚠️  Ask user to confirm before running this:
git push -f origin main
```

**Rule**: Always ask the user explicitly before running `git push -f`. Never automate it.

---

## Step 5 — ClawHub Publish

### 5.1 Check prerequisites

```bash
# Verify clawhub CLI is installed
which clawhub

# Check if logged in (will prompt if not)
clawhub whoami
```

### 5.2 Publish

```bash
cd $SKILL_DIR

clawhub publish $SKILL_DIR \
  --slug <skill-name> \
  --name "<Human-Readable Skill Name>" \
  --version 1.0.0 \
  --changelog "Initial release: English, generic, <brief description>"
```

### 5.3 Post-publish verification

```bash
# Verify it appears on ClawHub
clawhub search <skill-name>

# Or visit: https://clawhub.com/skills/<skill-name>
```

---

## Common Issues

### "SKILL.md required" error from clawhub publish
- The skill directory must contain a valid `SKILL.md` file
- Use absolute path to the skill directory

### GitHub API rate limit exceeded
- Wait 1–2 minutes and retry
- Avoid running `git push` + `clawhub publish` in rapid succession
- Consider setting a separate GitHub token for clawhub

### Push rejected: "Updates were rejected because the remote contains work"
- The remote repo was initialized with a README or LICENSE
- Fix: `git pull origin main --allow-unrelated-histories`, resolve conflicts, then push

---

## Quality Checklist (Before Publishing)

- [ ] SKILL.md is 100% English
- [ ] README.md is 100% English with generic examples only
- [ ] All scripts have English comments/docstrings
- [ ] Zero proprietary references (drug names, protein names, tokens, emails)
- [ ] `git push` succeeded without errors
- [ ] `clawhub publish` succeeded and returned a package ID
- [ ] ClawHub page is accessible at `https://clawhub.com/skills/<skill-name>`

---

*Skill: publish-to-clawhub | For publishing OpenClaw skills to GitHub and ClawHub*
