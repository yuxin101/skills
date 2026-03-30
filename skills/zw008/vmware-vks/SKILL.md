---
name: vmware-vks
description: >
  AI-powered VMware vSphere with Tanzu (VKS) management.
  Manage Supervisor Namespaces and TanzuKubernetesCluster lifecycle via AI.
  20 MCP tools: compatibility checks, Namespace CRUD with quota management,
  TKC lifecycle (create/scale/upgrade/delete), kubeconfig retrieval, Harbor registry.
  Use when user asks to "create a namespace", "deploy a TKC cluster",
  "scale Kubernetes workers", "get kubeconfig", "check supervisor status",
  "list Tanzu clusters", or mentions VKS, Tanzu, TKC, Supervisor, or
  vSphere Kubernetes. For VM operations use vmware-aiops, for monitoring
  use vmware-monitor, for storage use vmware-storage.
installer:
  kind: uv
  package: vmware-vks
metadata: {"openclaw":{"requires":{"env":["VMWARE_VKS_CONFIG"],"bins":["vmware-vks"],"config":["~/.vmware-vks/config.yaml"]},"primaryEnv":"VMWARE_VKS_CONFIG","homepage":"https://github.com/zw008/VMware-VKS","emoji":"☸️","os":["macos","linux"]}}
---

# VMware VKS

AI-powered VMware vSphere with Tanzu (VKS) management — 20 MCP tools.

> Requires vSphere 8.x+ with Workload Management enabled.
> **Companion skills**: [vmware-aiops](https://github.com/zw008/VMware-AIops) (VM lifecycle), [vmware-monitor](https://github.com/zw008/VMware-Monitor) (monitoring), [vmware-storage](https://github.com/zw008/VMware-Storage) (storage).

## What This Skill Does

| Category | Capabilities | Count |
|----------|-------------|:-----:|
| **Supervisor** | Compatibility check, status, storage policies | 3 |
| **Namespace** | List, get, create with quotas, update, delete with TKC guard, VM classes | 6 |
| **TKC Clusters** | List, get, versions, create, scale, upgrade, delete with workload guard | 7 |
| **Access** | Supervisor kubeconfig, TKC kubeconfig, Harbor registry, storage usage | 4 |

## Quick Install

```bash
uv tool install vmware-vks
vmware-vks doctor
```

## When to Use This Skill

- Check if vSphere environment supports VKS/Tanzu
- Create, update, or delete Supervisor Namespaces with resource quotas
- Deploy, scale, upgrade, or delete TKC (TanzuKubernetesCluster) clusters
- Get kubeconfig for Supervisor or TKC clusters
- Check Harbor registry info or storage usage

**Use companion skills for**:
- VM lifecycle, deployment → `vmware-aiops`
- Inventory, health, alarms → `vmware-monitor`
- iSCSI, vSAN, datastore → `vmware-storage`

## Related Skills — Skill Routing

| User Intent | Recommended Skill |
|-------------|------------------|
| Read-only monitoring | **vmware-monitor** |
| Storage: iSCSI, vSAN | **vmware-storage** |
| VM lifecycle, deployment | **vmware-aiops** |
| Tanzu Kubernetes (vSphere 8.x+) | **vmware-vks** ← this skill |

## Common Workflows

### Deploy a New TKC Cluster

1. Check compatibility → `vmware-vks supervisor check --target prod`
2. List available K8s versions → `vmware-vks tkc versions -n dev`
3. Create namespace (if needed) → `vmware-vks namespace create dev --cluster domain-c1 --storage-policy vSAN --cpu 16000 --memory 32768 --apply`
4. Create TKC cluster → `vmware-vks tkc create dev-cluster -n dev --version v1.28.4+vmware.1 --control-plane 1 --workers 3 --vm-class best-effort-large --apply`
5. Get kubeconfig → `vmware-vks kubeconfig get dev-cluster -n dev`

### Scale Workers for Load Testing

1. Check current state → `vmware-vks tkc get dev-cluster -n dev`
2. Scale up → `vmware-vks tkc scale dev-cluster -n dev --workers 6`
3. Monitor progress → `vmware-vks tkc get dev-cluster -n dev` (watch phase)
4. Scale back down after test

### Namespace Resource Management

1. List namespaces → `vmware-vks namespace list`
2. Check usage → `vmware-vks storage -n dev`
3. Update quota → `vmware-vks namespace update dev --cpu 32000 --memory 65536`

## Architecture

```
User (Natural Language)
  ↓
AI Agent (Claude Code / Goose / Cursor)
  ↓ reads SKILL.md
  ↓
vmware-vks CLI  ─── or ───  vmware-vks MCP Server (stdio)
  │
  ├─ Layer 1: pyVmomi → vCenter REST API
  │   Supervisor status, storage policies, Namespace CRUD, VM classes, Harbor
  │
  └─ Layer 2: kubernetes client → Supervisor K8s API endpoint
      TKC CR apply / get / delete  (cluster.x-k8s.io/v1beta1)
      Kubeconfig built from Layer 1 session token
  ↓
vCenter Server 8.x+ (Workload Management enabled)
  ↓
Supervisor Cluster → vSphere Namespaces → TanzuKubernetesCluster
```

## MCP Tools (20)

All accept optional `target` parameter to specify a named vCenter.

| Category | Tool | Type |
|----------|------|:----:|
| **Supervisor** | `check_vks_compatibility` | Read |
| | `get_supervisor_status` | Read |
| | `list_supervisor_storage_policies` | Read |
| **Namespace** | `list_namespaces` | Read |
| | `get_namespace` | Read |
| | `create_namespace` | Write |
| | `update_namespace` | Write |
| | `delete_namespace` | Write |
| | `list_vm_classes` | Read |
| **TKC** | `list_tkc_clusters` | Read |
| | `get_tkc_cluster` | Read |
| | `get_tkc_available_versions` | Read |
| | `create_tkc_cluster` | Write |
| | `scale_tkc_cluster` | Write |
| | `upgrade_tkc_cluster` | Write |
| | `delete_tkc_cluster` | Write |
| **Access** | `get_supervisor_kubeconfig` | Read |
| | `get_tkc_kubeconfig` | Read |
| | `get_harbor_info` | Read |
| | `list_namespace_storage_usage` | Read |

`create_namespace` / `create_tkc_cluster` — defaults to `dry_run=True`, returns a YAML plan for review. Pass `dry_run=False` to apply.

`delete_namespace` — requires `confirmed=True` and rejects if TKC clusters still exist (prevents orphaned clusters).

`delete_tkc_cluster` — requires `confirmed=True` and checks for running workloads. Rejects if found unless `force=True`.

> Full capability details and safety features: see `references/capabilities.md`

## CLI Quick Reference

```bash
# Supervisor
vmware-vks check [--target <name>]
vmware-vks supervisor status <cluster-id> [--target <name>]
vmware-vks supervisor storage-policies [--target <name>]

# Namespace
vmware-vks namespace list [--target <name>]
vmware-vks namespace get <name> [--target <name>]
vmware-vks namespace create <name> --cluster <id> [--cpu <n>] [--memory <mb>] [--storage-policy <name>] [--apply]
vmware-vks namespace update <name> [--cpu <n>] [--memory <mb>] [--target <name>]
vmware-vks namespace delete <name> [--target <name>]

# TKC Clusters
vmware-vks tkc list [-n <namespace>] [--target <name>]
vmware-vks tkc create <name> -n <ns> [--version <v>] [--workers <n>] [--vm-class <name>] [--apply]
vmware-vks tkc scale <name> -n <ns> --workers <n> [--target <name>]
vmware-vks tkc upgrade <name> -n <ns> --version <v> [--target <name>]
vmware-vks tkc delete <name> -n <ns> [--force] [--target <name>]

# Kubeconfig
vmware-vks kubeconfig supervisor -n <namespace> [--target <name>]
vmware-vks kubeconfig get <cluster-name> -n <namespace> [-o <path>] [--target <name>]

# Harbor & Storage
vmware-vks harbor [--target <name>]
vmware-vks storage -n <namespace> [--target <name>]
```

> Full CLI reference with all flags and interactive creation: see `references/cli-reference.md`

## Troubleshooting

### "VKS not compatible" error

Workload Management must be enabled in vCenter. Check: vCenter UI → Workload Management. Requires vSphere 8.x+ with Enterprise Plus or VCF license.

### Namespace creation fails with "storage policy not found"

List available policies first: `vmware-vks supervisor storage-policies`. Policy names are case-sensitive.

### TKC cluster stuck in "Creating" phase

Check Supervisor events in vCenter. Common causes: insufficient resources on ESXi hosts, network issues with NSX-T, or storage policy not available on target datastore.

### Kubeconfig retrieval fails

Supervisor API endpoint must be reachable from the machine running vmware-vks. Check firewall rules for port 6443.

### Scale operation has no effect

Verify the cluster is in "Running" phase before scaling. Clusters in "Creating" or "Updating" phase reject scale operations.

### Delete namespace rejected unexpectedly

The namespace delete guard prevents deletion when TKC clusters exist inside. Delete all TKC clusters in the namespace first, then retry.

## Prerequisites

- vSphere 8.x+ with Workload Management enabled
- Enterprise Plus or VCF license
- NSX-T (recommended) or VDS + HAProxy networking
- Supervisor Cluster configured and running

## Setup

```bash
uv tool install vmware-vks
mkdir -p ~/.vmware-vks
vmware-vks init
```

> Full setup guide, security details, and AI platform compatibility: see `references/setup-guide.md`

## License

MIT — [github.com/zw008/VMware-VKS](https://github.com/zw008/VMware-VKS)
