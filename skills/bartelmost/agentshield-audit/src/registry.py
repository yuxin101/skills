"""
AgentShield Public Registry Client v1.4.0

Discover and search trusted AI agents.
"""

import requests
from typing import Dict, List, Optional


API_BASE = "https://agentshield.live/api"


def list_agents(limit: int = 20, min_trust: int = 0) -> Dict:
    """
    List all registered agents.
    
    Args:
        limit: Max results (default 20)
        min_trust: Minimum trust score filter
    
    Returns:
        {
            "agents": [
                {
                    "agent_id": str,
                    "agent_name": str,
                    "tier": str,
                    "trust_score": int,
                    "platform": str
                }
            ],
            "count": int
        }
    """
    response = requests.get(
        f"{API_BASE}/registry/agents",
        params={"limit": limit, "min_trust": min_trust}
    )
    response.raise_for_status()
    return response.json()


def search_agents(query: str, min_trust: int = 50, limit: int = 20) -> Dict:
    """
    Search registry by keyword.
    
    Args:
        query: Search term (name, bio, platform)
        min_trust: Minimum trust score
        limit: Max results
    
    Returns:
        {
            "agents": [...],
            "count": int,
            "query": str
        }
    """
    response = requests.get(
        f"{API_BASE}/registry/search",
        params={
            "q": query,
            "min_trust": min_trust,
            "limit": limit
        }
    )
    response.raise_for_status()
    return response.json()


def get_crl() -> Dict:
    """
    Get Certificate Revocation List.
    
    Returns:
        {
            "revoked_certificates": [
                {
                    "agent_id": str,
                    "revoked_at": str,
                    "reason": str
                }
            ],
            "count": int
        }
    """
    response = requests.get(f"{API_BASE}/crl")
    response.raise_for_status()
    return response.json()


def check_revoked(agent_id: str) -> bool:
    """
    Check if agent certificate is revoked.
    
    Args:
        agent_id: Agent ID to check
    
    Returns:
        True if revoked, False otherwise
    """
    crl = get_crl()
    revoked_ids = [cert["agent_id"] for cert in crl["revoked_certificates"]]
    return agent_id in revoked_ids
