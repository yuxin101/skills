# Cost Control

## Where tokens actually go (OpenClaw reality)

Most spend is in **cacheWrite + cacheRead**, not raw input/output.
Cache tokens cost ~10% of input tokens — so high cache hit rate = low real cost.

### Healthy metrics
- Cache hit rate > 70%: ✅ costs well-controlled
- Cache hit rate 40-70%: 🟡 room to improve
- Cache hit rate < 40%: ⚠️ too many new sessions being created

### How to check
```python
# ~/.openclaw/agents/*/sessions/*.jsonl
# Look for: u.get('cacheRead') / (u.get('input') + u.get('cacheRead'))
```

## Model routing (tiered)

| Task | Tier | Notes |
|------|------|-------|
| Simple fetch, format, notify | Cheapest (e.g. qwen-plus) | Sports results, reminders, weather |
| Analysis, writing, reasoning | Mid (e.g. sonnet) | Self-improvement, strategy docs |
| Complex multi-step | High (e.g. opus) | Only when mid fails repeatedly |

**Rule:** Start with cheapest. Upgrade only when task repeatedly fails or quality matters critically.

## Session discipline

Each new session = new cache write = higher cost.

Reduce session sprawl:
- Don't create isolated sessions for simple tasks
- Reuse main session for interactive work
- Use `sessionTarget: isolated` only for true fire-and-forget cron jobs

## Context discipline

Large context = expensive heartbeats.

Keep these files lean:
- `HEARTBEAT.md`: < 30 lines of active rules only
- `AGENTS.md`: startup rules, not runbooks
- `SOUL.md`: personality, not procedures
- Move long docs to `references/` (loaded on demand)

## Cron cost profile

Cheapest cron pattern:
```
Script pre-computes → 0 tokens if no output
Script has output → ~500-1000 tokens total
```

Expensive cron anti-pattern:
```
Long prompt with embedded logic → 2000+ tokens setup
+ LLM reasons through it → 1000+ output tokens
+ Every run regardless of outcome
```

## Weekly token audit

Run `scripts/token_report.py` every Monday to:
- See per-day and per-model breakdown
- Catch anomalies (single-day spike > 3x average)
- Track cache hit rate trend

If single day > 3x recent average: investigate immediately (runaway cron? loop?).
