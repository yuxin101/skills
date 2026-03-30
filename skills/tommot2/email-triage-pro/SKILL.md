---
name: email-triage-pro
description: "Intelligently categorize, prioritize, and draft replies for emails. Works with any Gmail-connected skill (e.g., GOG). AI-powered classification into urgent/important/newsletter/spam categories, generates contextual reply drafts, tracks unanswered emails, and This skill does NOT handle OAuth, credentials, or file I/O — it relies on other skills for Gmail access. Use when: (1) user wants email help or inbox management, (2) user asks to check inbox, triage emails, or find unread messages, (3) draft email replies with AI assistance, (4) find unanswered or forgotten emails, (5) set up automated email monitoring on schedule, (6) user says 'check my email', 'any urgent emails', 'draft a reply', 'email summary', 'inbox zero'. Homepage: https://clawhub.ai/skills/email-triage-pro"
---

# Email Triage Pro

Intelligent email triage, categorization, and reply drafting.

**This skill handles email analysis and reply drafting only.** It does NOT manage OAuth, credentials, or file storage. It requires a Gmail-connected skill (e.g., GOG) to be installed separately.

## Prerequisites

A Gmail-connected skill must be installed for email access. Recommended: **GOG** (`clawhub install gog`).

This skill has NO credential requirements — no OAuth tokens, no API keys, no config files. All email access is delegated to the connected Gmail skill.

## Workflow

### 1. Fetch Emails

Use the installed Gmail skill's tools/commands to fetch unread emails (typically 10-20 most recent). Do NOT use curl, exec, or direct API calls.

If no Gmail skill is installed, instruct the user:
```
Install a Gmail connector first: clawhub install gog
```

### 2. Categorize

Read each email's subject, sender, and snippet. Categorize:

| Category | Criteria | Action |
|----------|----------|--------|
| 🔴 Urgent | Time-sensitive, from boss/client, "ASAP" | Flag immediately |
| 🟡 Important | Work-related, requires response | Draft reply |
| 🟢 Newsletter | Mass email, marketing | Archive suggestion |
| ⚪ Spam/Low | Promotions, automated | Archive suggestion |

### 3. Draft Replies

For urgent and important emails, generate a reply draft following these rules:

- Match the sender's tone (formal if they're formal, casual if casual)
- Keep it concise - max 3 paragraphs
- End with a clear next step or question
- Do NOT send automatically — present draft for user review
- If sender's language is detected (e.g., Norwegian), reply in same language

Format the draft clearly:

```markdown
📧 Reply to: {sender} - "{subject}"

---
{draft text}

---
[Reply] [Edit] [Skip] [Send as-is]
```

### 4. Track Unanswered

For emails that need response, note the count and flag any waiting > 2 days as overdue. Do NOT write tracking state to files — use conversation context only.

## Privacy

- This skill processes email content in-session only — nothing is stored or persisted
- No credentials, tokens, or personal data are written to any files
- Email content is never forwarded to external services
- No file I/O of any kind

## Rate Limiting

Respect Gmail API rate limits imposed by the connected Gmail skill. Add 1s delay between batch fetches for safety.

## More by TommoT2

- **context-brief** — Optimize context window for longer conversations
- **setup-doctor** — Diagnose and fix OpenClaw setup issues
- **tommo-skill-guard** — Security scanner for all installed skills

Install the full starter pack:
```bash
clawhub install context-brief setup-doctor tommo-skill-guard
```
