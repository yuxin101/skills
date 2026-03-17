---
name: tronscan-sr-governance
description: |
  Query TRON Super Representatives (SRs), witnesses, candidates, voting info, chain parameters, and governance proposals.
  Use when user asks "SR list", "super representatives", "witness ranking", "my votes", "chain parameters", "energy/bandwidth price", "governance proposals", or "TRON voting".
  Do NOT use for: account asset profiling (tronscan-account-profiler). For "who voted for SR X" use getVoteList (Account API).
metadata:
  author: tronscan-mcp
  version: "1.0"
  mcp-server: https://mcp.tronscan.org/mcp
---

# SR / Witness (Super Representative)

## Overview

| Tool | Function | Use Case |
|------|----------|----------|
| getWitnessList | Witness/SR list | SRs, partners, candidates by type |
| getAccountVotes | Account vote record | Which SRs an address voted for and amounts |
| getChainParameters | Chain parameters | Tx fees, energy/bandwidth price, config |
| getProposals | Governance proposals | Proposal content, votes, participants |
| getWitnessVoteInfo | SR vote metrics | Vote count, ranking history for a witness |
| getWitnessGeneralInfo | Network aggregate | Total votes, block stats, witness count |

## Workflow: SR & Voting Queries

> User: "Who are the top SRs? What are the chain parameters?"

1. **tronscan-sr-governance** — `getWitnessList` → SR/partner/candidate list; optionally filter by type.
2. **tronscan-sr-governance** — `getWitnessGeneralInfo` → total votes, block stats, witness count.
3. For **chain config** (fees, energy/bandwidth price): `getChainParameters`.

> User: "Which SRs did this address vote for?"

1. **tronscan-sr-governance** — `getAccountVotes` with address → vote targets and amounts.

> User: "What is the vote/ranking history of SR X?"

1. **tronscan-sr-governance** — `getWitnessVoteInfo` with witness address → vote metrics and history.

> User: "Who voted for SR X?" or "List voters of SR X"

1. **tronscan-account-profiler** — `getVoteList` (Account API) with SR address → voter list.

## MCP Server

- **Prerequisite**: [TronScan MCP Guide](https://mcpdoc.tronscan.org)


## Troubleshooting

- **MCP connection failed**: If you see "Connection refused", verify TronScan MCP is connected in Settings > Extensions.
- **API rate limit / 429**: Apply for an API key at [TronScan Developer API](https://tronscan.org/#/developer/api) and add it to MCP config.

### Invalid witness address
Ensure the address is a valid TRON base58 format (starts with T). For voter list of an SR, use `getVoteList` (Account API) with the SR address.
