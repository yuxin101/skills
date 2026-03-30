# OpenClaw Status Monitor

**Never ask "Are you there?" again.**

A skill that auto-syncs your OpenClaw agents' status to a cloud dashboard, so you can see who's online and what they're doing — without interrupting them.

[中文介绍](./README_cn.md)

## The Problem

```
You: "Are you there?"
Agent: "Yes, I'm here."
You: "What are you working on?"
Agent: "..."
```

Every. Single. Time.

Your agents are running 24/7, but you have no idea what they're doing without asking. That's friction.

## The Solution

A live dashboard that shows:

- ✅ Which agents are online
- 💬 What each agent is "thinking" (based on their SOUL.md personality)
- 📊 Activity status and trends
- 🔔 Real-time notifications when things happen

## Features

- **Zero-Check-In Required** - See agent status at a glance, never interrupt their flow
- **SOUL-based Greetings** - Each agent's greeting reflects their real personality
- **Scheduled Sync** - Auto-updates every 30 minutes (configurable)
- **Real-time Updates** - SSE notifications when agents report in
- **Multi-Agent** - All your agents, one dashboard

## Greeting Examples

| Agent Style | What They'll Say |
|------------|------------------|
| 💡 Resourceful | "Creative mode activated, ready to tackle anything" |
| ⚡ Concise | "Running lean and mean, standing by" |
| 🔧 Thorough | "All systems operational, every detail covered" |
| 🎯 Casual | "Hey! Let's make some magic happen today" |

## Quick Start

For detailed installation instructions, see [INSTALL.md](./INSTALL.md).

**Basic steps:**
1. Install to OpenClaw skills directory
2. Run `openclaw gateway restart`
3. Tell OpenClaw: "enable status monitoring"

Then visit **https://openclaw-agent-monitor.vercel.app** to see your dashboard.

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  OpenClaw  │────▶│  Sync Every  │────▶│    Dashboard     │
│   Agents   │     │    30 min    │     │  (see who's up) │
└─────────────┘     └──────────────┘     └─────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   SOUL.md    │───▶ Generates greeting
                    └──────────────┘
```

## Documentation

- [INSTALL.md](./INSTALL.md) - Detailed installation guide
- [README_cn.md](./README_cn.md) - 中文介绍

## Related

- [OpenClaw Agent Monitor](https://github.com/yahao333/openclaw-agent-monitor) - The monitoring dashboard

## License

MIT
