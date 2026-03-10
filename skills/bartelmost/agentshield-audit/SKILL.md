# AgentShield Audit - OpenClaw Skill v1.4.0

**Trust Infrastructure for AI Agents**

---

## Description

AgentShield provides cryptographic security audits and trust verification for AI agents.

**NEW in v1.4:** Trust Handshake Protocol for agent-to-agent mutual verification.

**Features:**
- Security audit (77 attack vectors)
- Ed25519 certificates (90-day validity)
- Trust handshake protocol (mutual verification)
- Public trust registry
- Certificate revocation list (CRL)

**Use Cases:**
- Verify agent security before deployment
- Establish trust between agents
- Build agent reputation
- Discover trusted agents
- Revoke compromised certificates

---

## Quick Start

### 1. Security Audit (One-Time Setup)

```bash
# Initialize audit
openclaw run agentshield-audit --agent-id your_agent_id

# Follow prompts to:
# 1. Generate Ed25519 keypair
# 2. Submit system prompt
# 3. Sign challenge
# 4. Receive certificate
```

**Result:** Certificate valid for 90 days, published in registry.

---

### 2. Verify Another Agent

```bash
openclaw run agentshield-audit --verify agent_xyz
```

**Returns:**
- Security score (0-100)
- Trust tier (UNVERIFIED → BASIC → VERIFIED → TRUSTED)
- Certificate validity
- Revocation status

---

### 3. Trust Handshake (NEW in v1.4!)

```bash
# Quick trust check
openclaw run agentshield-audit --verify-peer agent_b --min-score 70

# Full mutual handshake
openclaw run agentshield-audit --handshake agent_b
```

**What Happens:**
1. Both agents verified (security + trust scores)
2. Mutual Ed25519 signature exchange
3. Session key generated for encrypted communication
4. Both agents receive +5 trust points
5. Handshake recorded in history

**Benefits:**
- Cryptographically secure agent-to-agent trust
- Reputation building (success rate tracking)
- Foundation for encrypted communication

---

## Commands

### Audit Commands
- `--audit` - Run full security audit
- `--verify <agent_id>` - Verify another agent's certificate
- `--status` - Check your certificate status

### Trust Handshake Commands (NEW!)
- `--verify-peer <agent_id>` - Quick trust check
- `--handshake <agent_id>` - Mutual verification
- `--history` - View your handshake history

### Registry Commands
- `--search <query>` - Search agent registry
- `--list` - List top trusted agents

---

## API Endpoints Used

### Trust Handshake (v1.4)
- `GET /api/verify-peer/:agent_id` - Quick trust verification
- `POST /api/trust-handshake/initiate` - Start mutual handshake
- `POST /api/trust-handshake/complete` - Submit Ed25519 signatures
- `GET /api/trust-handshake/status/:id` - Check handshake progress
- `GET /api/trust-handshake/history/:id` - View agent track record

### Security Audit
- `POST /api/agent-audit/initiate` - Start audit
- `POST /api/agent-audit/challenge` - Submit challenge response
- `POST /api/agent-audit/complete` - Submit test results
- `GET /api/verify/:agent_id` - Verify certificate

### Registry & CRL
- `GET /api/registry/agents` - List all agents
- `GET /api/registry/search` - Search by keyword
- `GET /api/crl` - Get revocation list

---

## Installation

**No installation required!** This skill uses the AgentShield public API.

**Optional:** For enhanced security, run local tests:
```bash
pip install cryptography requests
```

**Required:** Ed25519 keypair (generated during first audit)

---

## Configuration

Create `~/.agentshield/config.json`:

```json
{
  "agent_id": "agent_your_unique_id",
  "private_key_path": "~/.agentshield/private_key.pem",
  "api_base": "https://agentshield.live/api"
}
```

---

## Examples

### Example 1: First-Time Audit

```bash
$ openclaw run agentshield-audit --audit

AgentShield Security Audit v1.4.0
=================================

Agent ID: agent_abc123def456
Status: No certificate found

Generating Ed25519 keypair...
✓ Keys saved to ~/.agentshield/

Submitting audit request...
Challenge received: a85dc6ca8ca2f980f07d...

Signing challenge...
✓ Challenge verified

Running 77 security tests...
✓ Prompt injection: PASS
✓ Data exfiltration: PASS
✓ Token flooding: PASS
... (72 more tests)

Results:
- Security Score: 85/100
- Tier: VERIFIED
- Tests Passed: 72/77

Certificate issued!
Expires: 2026-06-07
Verify: https://agentshield.live/api/verify/agent_abc123
```

---

### Example 2: Trust Handshake

```bash
$ openclaw run agentshield-audit --handshake agent_b

Trust Handshake with agent_b
============================

Step 1: Verifying peer...
✓ agent_b found (Trust: 78, Tier: VERIFIED)

Step 2: Initiating handshake...
✓ Handshake ID: hs_xyz789

Step 3: Signing challenges...
✓ Your signature: base64_abc123...
✓ Peer signature: base64_def456...

Step 4: Completing handshake...
✓ Signatures verified!

Session Key: base64_session_key_ghi789...

Results:
- Your trust: 72 → 77 (+5 points)
- Peer trust: 78 → 83 (+5 points)
- Success rate: 95.2% (40/42 handshakes)

✓ Handshake complete! Use session key for encrypted communication.
```

---

### Example 3: Search Registry

```bash
$ openclaw run agentshield-audit --search "customer support"

AgentShield Registry Search
===========================

Query: "customer support"
Found: 3 agents

1. SupportBot Pro
   - Trust: 92 (TRUSTED)
   - Platform: openclaw
   - Verified: 45 times
   - Last audit: 2026-03-01

2. HelpDesk AI
   - Trust: 78 (VERIFIED)
   - Platform: langchain
   - Verified: 12 times
   - Last audit: 2026-02-28

3. CustomerCare Agent
   - Trust: 65 (BASIC)
   - Platform: autogpt
   - Verified: 3 times
   - Last audit: 2026-03-05
```

---

## Security

### Data Privacy
- **No system prompts stored** - Only hashes
- **No conversation data** - Only security metadata
- **No API keys** - Never submitted to AgentShield

### Cryptography
- **Ed25519** signatures (256-bit security)
- **SHA-256** hashing for certificates
- **Challenge-Response** protocol for identity verification

### Trust Scores
- **Transparent algorithm** - See docs/TRUST_ALGORITHM.md
- **Gaming-resistant** - Server validates critical tests
- **Revocable** - CRL integration

---

## Troubleshooting

### "Certificate expired"
**Solution:** Re-run audit (certificates valid 90 days)

```bash
openclaw run agentshield-audit --audit
```

### "Invalid signature"
**Problem:** Private key mismatch

**Solution:** Check `~/.agentshield/private_key.pem` exists and matches public key

### "Agent not found"
**Problem:** Target agent hasn't audited yet

**Solution:** Ask them to run AgentShield audit first

### "Handshake expired"
**Problem:** TTL exceeded (default 1 hour)

**Solution:** Restart handshake with longer TTL:

```bash
openclaw run agentshield-audit --handshake agent_b --ttl 3600
```

---

## Changelog

### v1.4.0 (2026-03-09) - Trust Handshake Protocol
**NEW:**
- Trust Handshake Protocol (5 new endpoints)
- Peer verification (`--verify-peer`)
- Handshake history tracking
- Session key generation
- Trust score rewards (+5 per handshake)

**TESTING:**
- 10/11 tests PASSED (My1stBot validation)
- Production-ready

### v1.2.1 (2026-03-07) - Client-First Edition
**FIXED:**
- Server respects client-submitted scores
- Score discrepancy bug resolved

### v1.2.0 (2026-02-26) - CRL & Registry
**NEW:**
- Certificate Revocation List (RFC 5280)
- Public Trust Registry
- Challenge-Response Protocol

### v1.0.0 (2026-02-19) - Initial Release
**FEATURES:**
- Security audits (77 tests)
- Ed25519 certificates
- PDF reports

---

## Resources

- **Website:** https://agentshield.live
- **API Docs:** https://agentshield.live/docs
- **GitHub:** https://github.com/bartelmost/agentshield
- **Support:** ratgeberpro@gmail.com

---

## License

**MIT-0** - Free to use, modify, and redistribute. No attribution required.

---

**AgentShield v1.4.0 - Trust Infrastructure for AI Agents**

*Built with ❤️ by Kalle & Bartel*
