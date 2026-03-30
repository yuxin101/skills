# clawhub-skill-packager

A ClawHub / OpenClaw skill for reviewing, repairing, packaging, and self-auditing other ClawHub/OpenClaw skills.

## Display Name
ClawHub Skill Packager

## Goal
Take any combination of:
- a user description
- existing skill files
- partial metadata
- draft naming
- invocation ideas
- packaging notes

and turn it into:
1. a publish-ready skill package
2. a separate plain-text review record
3. a publish/install handoff file

## Core philosophy
This skill is built for low-friction handoff.

The user should be able to hand over draft material and receive:
- a completed package
- a review record
- a clear summary of what was inferred, fixed, changed, or flagged
- a publish/install handoff

The skill should minimize question loops and favor best-effort packaging plus clear review notes.

## Runtime identity note
This package intentionally uses:
- `clawhub-pack` as the short runtime / slash identity
- `clawhub-skill-packager` as the fuller slug / skill key identity

## What it does

This skill:
- audits what is already present
- identifies what is missing
- fills gaps using safe defaults when needed
- repairs naming and frontmatter issues
- aligns slug, skill key, and package naming
- builds the final folder
- performs a second-pass self-review
- produces a plain-text change log / review file for the user
- produces a publish/install handoff file

## Deliverables
The skill should finish with:
- a zip-ready skill bundle
- a plain-text report for records and review
- a short completion summary for the user
- a publish/install handoff file

## Review emphasis
Important assumptions and risky guesses should be highlighted using:
- **⚠️ REQUIRED REVIEW**
- **🔶 INFERRED FIELD**
- **✅ FIXED AUTOMATICALLY**
- **📝 EDITED FOR ALIGNMENT**
- **🚀 READY TO PUBLISH**

## Publish fields
- Slug: `clawhub-skill-packager`
- Internal skill name / slash command: `clawhub-pack`
- Skill key: `clawhub-skill-packager`
- Version: `1.3.0`
- Tags: `latest, clawhub, openclaw, packaging, review, audit, skills`
