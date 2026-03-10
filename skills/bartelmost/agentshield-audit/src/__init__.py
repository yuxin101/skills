"""
AgentShield - Trust Infrastructure for AI Agents

v1.4.0 - Trust Handshake Protocol

Public API: https://agentshield.live/api
Documentation: https://agentshield.live/docs
"""

__version__ = "1.4.0"

from .handshake import (
    verify_peer,
    initiate_handshake,
    complete_handshake,
    get_handshake_status,
    get_handshake_history,
    sign_challenge
)

from .audit_client import (
    initiate_audit,
    submit_challenge_response,
    submit_audit_results,
    verify_certificate,
    generate_keypair
)

from .registry import (
    list_agents,
    search_agents,
    get_crl,
    check_revoked
)

__all__ = [
    # Handshake
    "verify_peer",
    "initiate_handshake",
    "complete_handshake", 
    "get_handshake_status",
    "get_handshake_history",
    
    # Audit
    "initiate_audit",
    "submit_challenge_response",
    "submit_audit_results",
    "verify_certificate",
    "generate_keypair",
    
    # Registry
    "list_agents",
    "search_agents",
    "get_crl",
    "check_revoked",
    
    # Utils
    "sign_challenge"
]
