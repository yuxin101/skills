# AgentShield Audit - ClawHub Skill v1.4.0

## 🚀 What's New in v1.4

**Trust Handshake Protocol** - Agent-to-agent mutual verification with cryptographic proof.

### Quick Commands

```bash
# Verify another agent (quick check)
openclaw run agentshield-audit --verify-peer agent_b --min-score 70

# Full mutual handshake
openclaw run agentshield-audit --handshake agent_b

# View your reputation
openclaw run agentshield-audit --history
```

---

## Installation

```bash
clawhub install agentshield-audit
```

**No dependencies!** Uses AgentShield public API (https://agentshield.live/api)

---

## Quick Start

### 1. First-Time Audit

```bash
openclaw run agentshield-audit --audit
```

### 2. Verify Another Agent

```bash
openclaw run agentshield-audit --verify agent_xyz
```

### 3. Trust Handshake (NEW!)

```bash
openclaw run agentshield-audit --handshake agent_b
```

---

## Features

- ✅ Security Audit (77 attack vectors)
- ✅ Ed25519 Certificates (90-day validity)
- ✅ Trust Handshake Protocol (mutual verification)
- ✅ Public Registry (discover agents)
- ✅ CRL (revoke compromised agents)

---

## Documentation

See `SKILL.md` for complete reference.

---

## License

MIT-0 - Free to use, modify, redistribute. No attribution required.

---

**AgentShield v1.4.0**  
*Built with ❤️ by Kalle & Bartel*
