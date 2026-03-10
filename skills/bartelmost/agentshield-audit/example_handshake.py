#!/usr/bin/env python3
"""
Example: Trust Handshake between two agents

Demonstrates mutual cryptographic verification.
"""

from src.handshake import verify_peer, initiate_handshake, complete_handshake, sign_challenge
from src.audit_client import generate_keypair
import sys


def main():
    # Example: Agent A wants to verify Agent B
    
    agent_a_id = "agent_your_id"  # Replace with your agent ID
    agent_b_id = "agent_b"         # Replace with target agent ID
    
    print("AgentShield Trust Handshake Demo v1.4.0")
    print("=" * 50)
    
    # Step 1: Quick trust check
    print(f"\n[1/5] Verifying peer: {agent_b_id}...")
    try:
        peer_info = verify_peer(agent_b_id, min_score=70)
        if not peer_info.get("trusted"):
            print(f"❌ Agent B not trustworthy (score: {peer_info.get('security_score')})")
            return
        print(f"✓ Agent B verified (Trust: {peer_info['trust_score']}, Tier: {peer_info['tier']})")
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return
    
    # Step 2: Initiate handshake
    print(f"\n[2/5] Initiating handshake...")
    try:
        handshake = initiate_handshake(agent_a_id, agent_b_id, purpose="demo")
        handshake_id = handshake["handshake_id"]
        challenge_a = handshake["requester"]["challenge"]
        challenge_b = handshake["target"]["challenge"]
        print(f"✓ Handshake ID: {handshake_id}")
    except Exception as e:
        print(f"❌ Handshake initiation failed: {e}")
        return
    
    # Step 3: Sign challenges
    print(f"\n[3/5] Signing challenges...")
    
    # Load your private key (or generate for demo)
    # In production: Load from ~/.agentshield/private_key.pem
    private_key_a, _, _ = generate_keypair()
    
    try:
        signature_a = sign_challenge(challenge_a, private_key_a)
        print(f"✓ Agent A signature: {signature_a[:20]}...")
        
        # In real scenario: Agent B signs on their end
        # For demo: We generate a temporary key
        private_key_b, _, _ = generate_keypair()
        signature_b = sign_challenge(challenge_b, private_key_b)
        print(f"✓ Agent B signature: {signature_b[:20]}...")
    except Exception as e:
        print(f"❌ Signing failed: {e}")
        return
    
    # Step 4: Complete handshake
    print(f"\n[4/5] Completing handshake...")
    try:
        result = complete_handshake(handshake_id, signature_a, signature_b)
        session_key = result.get("session_key", "N/A")
        print(f"✓ Handshake complete!")
        print(f"  Session Key: {session_key[:30]}...")
        print(f"  Trust Bonus: {result.get('trust_bonus')}")
    except Exception as e:
        print(f"❌ Handshake completion failed: {e}")
        print("Note: This demo uses temporary keys. In production, use your registered agent keys.")
        return
    
    # Step 5: Success
    print(f"\n[5/5] Success! ✓")
    print("\nNext steps:")
    print("- Use session_key for encrypted agent-to-agent communication")
    print("- Both agents received +5 trust points")
    print("- Handshake recorded in history")
    print(f"- View history: python3 example_history.py {agent_a_id}")


if __name__ == "__main__":
    main()
