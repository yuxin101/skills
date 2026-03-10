"""
AgentShield Security Audit Client v1.4.0

Cryptographic security audits for AI agents.
"""

import requests
import base64
from typing import Dict, Optional


API_BASE = "https://agentshield.live/api"


def initiate_audit(agent_name: str, platform: str, public_key_b64: str) -> Dict:
    """
    Start security audit and get challenge.
    
    Args:
        agent_name: Your agent's name
        platform: Platform (openclaw|autogpt|langchain|custom)
        public_key_b64: Base64-encoded Ed25519 public key
    
    Returns:
        {
            "audit_id": str,
            "agent_id": str,
            "challenge": str,
            "challenge_expires": str
        }
    """
    response = requests.post(
        f"{API_BASE}/agent-audit/initiate",
        json={
            "agent_name": agent_name,
            "platform": platform,
            "public_key": public_key_b64
        }
    )
    response.raise_for_status()
    return response.json()


def submit_challenge_response(audit_id: str, challenge_response: str) -> Dict:
    """
    Submit signed challenge to verify identity.
    
    Args:
        audit_id: Audit ID from initiate
        challenge_response: Base64-encoded Ed25519 signature
    
    Returns:
        {
            "audit_id": str,
            "status": "authenticated",
            "next_step": str
        }
    """
    response = requests.post(
        f"{API_BASE}/agent-audit/challenge",
        json={
            "audit_id": audit_id,
            "challenge_response": challenge_response
        }
    )
    response.raise_for_status()
    return response.json()


def submit_audit_results(audit_id: str, score: int, passed: int, total: int) -> Dict:
    """
    Submit audit results and receive certificate.
    
    Args:
        audit_id: Audit ID
        score: Security score (0-100)
        passed: Number of tests passed
        total: Total number of tests
    
    Returns:
        {
            "certificate": {...},
            "agent_id": str,
            "security_score": int,
            "tier": str,
            "trust_score": int,
            "verify_url": str
        }
    """
    response = requests.post(
        f"{API_BASE}/agent-audit/complete",
        json={
            "audit_id": audit_id,
            "score": score,
            "passed": passed,
            "total": total
        }
    )
    response.raise_for_status()
    return response.json()


def verify_certificate(agent_id: str) -> Dict:
    """
    Verify another agent's certificate.
    
    Args:
        agent_id: Agent ID to verify
    
    Returns:
        {
            "valid": bool,
            "agent_id": str,
            "agent_name": str,
            "security_score": int,
            "tier": str,
            "trust_score": int,
            "revoked": bool,
            "expires_at": str
        }
    """
    response = requests.get(f"{API_BASE}/verify/{agent_id}")
    response.raise_for_status()
    return response.json()


def generate_keypair():
    """
    Generate Ed25519 keypair for certificates.
    
    Returns:
        (private_key, public_key, public_key_b64)
    """
    from cryptography.hazmat.primitives.asymmetric import ed25519
    
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    public_key_b64 = base64.b64encode(
        public_key.public_bytes_raw()
    ).decode('utf-8')
    
    return private_key, public_key, public_key_b64


def sign_challenge(challenge: str, private_key) -> str:
    """
    Sign challenge with Ed25519 private key.
    
    Args:
        challenge: Challenge string
        private_key: Ed25519PrivateKey instance
    
    Returns:
        Base64-encoded signature
    """
    signature = private_key.sign(challenge.encode('utf-8'))
    return base64.b64encode(signature).decode('utf-8')
