# Hopola (ClawHub Release)

## Overview

Hopola is an end-to-end skill pipeline for:

- web research
- image generation
- video generation
- 3D model generation
- logo design
- product image generation
- asset upload
- Markdown report delivery

## Architecture

- Main orchestrator: `SKILL.md`
- Version file: `VERSION.txt`
- Subskills: 8 focused units under `subskills/`
- Design intake playbook: `playbooks/design-intake.md`
- Scripts: release validation and packaging under `scripts/`
- Assets: logo, cover, flow chart under `assets/`

## Secure Key Design

- Users must provide `OPENCLOW_KEY` via environment variable.
- `config.template.json` keeps only `key_env_name` and an empty `key_value`.
- Release validation blocks packaging if plaintext keys are detected.

## Quick Start

```bash
cd .trae/skills/Hopola
python3 scripts/check_tools_mapping.py
python3 scripts/validate_release.py
python3 scripts/build_release_zip.py
```

## Routing Policy

- Generation tasks use preferred fixed tool first.
- If unavailable, fallback discovery uses `/api/gateway/mcp/tools`.

## Release Deliverables

- `Hopola-Skills/hopola-clawhub-v<version>-*.zip`
- `README.zh-CN.md`
- `README.en.md`
- `RELEASE.md`
