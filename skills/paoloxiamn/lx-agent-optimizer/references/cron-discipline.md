# Cron Discipline

## The Golden Rule
> If the cron prompt needs > 200 tokens to explain, convert it to a script.

## Script-first pattern

### Structure
```
skills/my-skill/
├── SKILL.md
└── scripts/
    └── my_job.py    ← all logic here
```

### Cron payload (short)
```json
{
  "message": "Run script via nodes.run:\n[\"/usr/bin/python3\", \"/path/to/scripts/my_job.py\"]\n\nIf output: send to user.\nIf no output: end silently.",
  "timeoutSeconds": 60,
  "model": "qwen-plus"
}
```

## Script design rules

### Silent on success
```python
# Good: no output when nothing to report
if not new_events:
    exit(0)

# Good: output only when something happened
print(f"⚽ AC Milan won 3-2")
```

### Validate data sources first
Before embedding any URL in a cron job:
```bash
curl -s "https://api.example.com/data" | head -5
# Confirm: returns real data, not HTML shell, not 403
```

### State file for idempotency
```python
# Track what was last sent to avoid duplicates
state_path = "/tmp/my_job_state.json"
state = json.load(open(state_path)) if os.path.exists(state_path) else {}
last_sent = state.get("last_id", "")

if new_id == last_sent:
    exit(0)  # already sent this

# ... send ...
json.dump({"last_id": new_id}, open(state_path, "w"))
```

## Pre-ship checklist
- [ ] Logic is in `.py` script, not in prompt
- [ ] Script tested locally: `python3 script.py`
- [ ] Silent on no-op (exit 0, no output)
- [ ] Output < 300 chars for routine cases
- [ ] Model: cheapest tier that works
- [ ] Timeout: 60s for simple, 120s for web fetch, never > 180s
- [ ] File writes in main session, not work agent
- [ ] Data source validated with curl

## Common timeout guide
| Task | Timeout |
|------|---------|
| Local script (no network) | 30s |
| Single API call | 60s |
| Web fetch + parse | 120s |
| Multi-step with LLM reasoning | 120s |
| Never | > 180s |

## Delivery rules
- `NO_REPLY` / no output = no message sent ✅
- Alert only on: new data, errors, anomalies
- Never send "everything is fine" messages
- Success = silence
