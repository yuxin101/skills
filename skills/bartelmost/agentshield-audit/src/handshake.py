"""
AgentShield Trust Handshake Client v1.4.0

Mutual cryptographic verification between AI agents.
Like SSL/TLS for agent-to-agent communication.
"""

import requests
import base64
from typing import Dict, Optional


API_BASE = "https://agentshield.live/api"


def verify_peer(agent_id: str, min_score: int = 70, min_tier: str = "VERIFIED") -> Dict:
    """
    Quick trust check before handshake.
    
    Args:
        agent_id: Target agent ID
        min_score: Minimum security score (0-100)
        min_tier: Minimum tier (UNVERIFIED|BASIC|VERIFIED|TRUSTED)
    
    Returns:
        {
            "trusted": bool,
            "security_score": int,
            "trust_score": int,
            "tier": str,
            "revoked": bool,
            "certificate_valid": bool
        }
    """
    response = requests.get(
        f"{API_BASE}/verify-peer/{agent_id}",
        params={"min_score": min_score, "min_tier": min_tier}
    )
    response.raise_for_status()
    return response.json()


def initiate_handshake(requester_id: str, target_id: str, purpose: str = "mutual_verification", ttl: int = 3600) -> Dict:
    """
    Start mutual trust handshake.
    
    Args:
        requester_id: Your agent ID
        target_id: Agent to verify with
        purpose: Reason for handshake (optional)
        ttl: Time-to-live in seconds (60-86400)
    
    Returns:
        {
            "handshake_id": str,
            "requester": {"agent_id": str, "challenge": str},
            "target": {"agent_id": str, "challenge": str},
            "expires_at": str
        }
    """
    response = requests.post(
        f"{API_BASE}/trust-handshake/initiate",
        json={
            "requester_id": requester_id,
            "target_id": target_id,
            "purpose": purpose,
            "ttl": ttl
        }
    )
    response.raise_for_status()
    return response.json()


def complete_handshake(handshake_id: str, requester_signature: str, target_signature: str) -> Dict:
    """
    Submit Ed25519 signatures to complete handshake.
    
    Args:
        handshake_id: Handshake ID from initiate
        requester_signature: Base64-encoded Ed25519 signature (requester)
        target_signature: Base64-encoded Ed25519 signature (target)
    
    Returns:
        {
            "handshake_id": str,
            "status": "completed",
            "session_key": str,
            "trust_bonus": "+5 points for both agents"
        }
    """
    response = requests.post(
        f"{API_BASE}/trust-handshake/complete",
        json={
            "handshake_id": handshake_id,
            "requester_signature": requester_signature,
            "target_signature": target_signature
        }
    )
    response.raise_for_status()
    return response.json()


def get_handshake_status(handshake_id: str) -> Dict:
    """
    Check handshake progress.
    
    Args:
        handshake_id: Handshake ID
    
    Returns:
        {
            "handshake_id": str,
            "status": str,
            "requester": {"signature_submitted": bool},
            "target": {"signature_submitted": bool},
            "expired": bool
        }
    """
    response = requests.get(f"{API_BASE}/trust-handshake/status/{handshake_id}")
    response.raise_for_status()
    return response.json()


def get_handshake_history(agent_id: str, limit: int = 20, status: Optional[str] = None) -> Dict:
    """
    View agent's handshake track record.
    
    Args:
        agent_id: Agent ID
        limit: Max results (1-100)
        status: Filter by status (pending|completed|expired)
    
    Returns:
        {
            "agent_id": str,
            "statistics": {
                "total_handshakes": int,
                "completed": int,
                "success_rate": float
            },
            "handshakes": [...]
        }
    """
    params = {"limit": limit}
    if status:
        params["status"] = status
    
    response = requests.get(
        f"{API_BASE}/trust-handshake/history/{agent_id}",
        params=params
    )
    response.raise_for_status()
    return response.json()


def sign_challenge(challenge: str, private_key) -> str:
    """
    Sign challenge with Ed25519 private key.
    
    Args:
        challenge: Challenge string from handshake
        private_key: Ed25519PrivateKey instance (from cryptography library)
    
    Returns:
        Base64-encoded signature
    """
    signature = private_key.sign(challenge.encode('utf-8'))
    return base64.b64encode(signature).decode('utf-8')
