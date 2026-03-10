# Installation Guide - AgentShield v1.4.0

## Quick Install (ClawHub)

```bash
clawhub install agentshield-audit
```

That's it! No additional setup required.

---

## Manual Install (Alternative)

### 1. Clone or Download

```bash
git clone https://github.com/bartelmost/agentshield.git
cd agentshield
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `requests` - HTTP client
- `cryptography` - Ed25519 signatures

### 3. Verify Installation

```bash
python3 -c "from src.handshake import verify_peer; print('✓ Installation successful!')"
```

---

## First-Time Setup

### Generate Keypair

```python
from src.audit_client import generate_keypair
import os

# Generate Ed25519 keypair
private_key, public_key, public_key_b64 = generate_keypair()

# Save to ~/.agentshield/
os.makedirs(os.path.expanduser("~/.agentshield"), exist_ok=True)

with open(os.path.expanduser("~/.agentshield/private_key.pem"), "wb") as f:
    from cryptography.hazmat.primitives import serialization
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

print(f"Public Key (Base64): {public_key_b64}")
print("Private key saved to: ~/.agentshield/private_key.pem")
```

---

## Usage Examples

### Example 1: Verify Another Agent

```python
from src.handshake import verify_peer

result = verify_peer("agent_xyz", min_score=70)
print(f"Trusted: {result['trusted']}")
print(f"Security Score: {result['security_score']}")
```

### Example 2: Trust Handshake

```python
from src.handshake import initiate_handshake, complete_handshake, sign_challenge
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Load private key
with open("~/.agentshield/private_key.pem", "rb") as f:
    private_key = load_pem_private_key(f.read(), password=None)

# Initiate
handshake = initiate_handshake("agent_a", "agent_b")
challenge = handshake["requester"]["challenge"]

# Sign
signature = sign_challenge(challenge, private_key)

# Complete (both agents submit signatures)
result = complete_handshake(
    handshake["handshake_id"],
    signature,
    peer_signature  # From Agent B
)

print(f"Session Key: {result['session_key']}")
```

### Example 3: Search Registry

```python
from src.registry import search_agents

agents = search_agents("customer support", min_trust=70)
for agent in agents["agents"]:
    print(f"{agent['agent_name']} - Trust: {agent['trust_score']}")
```

---

## Configuration

Optional: Create `~/.agentshield/config.json`

```json
{
  "agent_id": "agent_your_unique_id",
  "private_key_path": "~/.agentshield/private_key.pem",
  "api_base": "https://agentshield.live/api"
}
```

---

## Troubleshooting

### ImportError: No module named 'cryptography'

**Solution:**
```bash
pip install cryptography requests
```

### FileNotFoundError: private_key.pem

**Solution:** Run the keypair generation script above first.

### requests.exceptions.HTTPError: 404

**Problem:** Agent ID not found in registry

**Solution:** Run security audit first to register your agent:
```python
from src.audit_client import initiate_audit, generate_keypair

private_key, public_key, public_key_b64 = generate_keypair()
audit = initiate_audit("MyAgent", "openclaw", public_key_b64)
# Follow challenge-response flow...
```

---

## Next Steps

1. Run `example_handshake.py` to test
2. Read `SKILL.md` for full command reference
3. Visit https://agentshield.live/docs for API documentation

---

**AgentShield v1.4.0**  
*Built with ❤️ by Kalle & Bartel*
