---
name: clawhub-pack
description: "Review, repair, package, and self-audit ClawHub/OpenClaw skill bundles into a publish-ready zip plus a plain-text review record using an inference-first, low-friction packaging workflow."
version: "1.3.0"
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"📦","skillKey":"clawhub-skill-packager"}}
---

# ClawHub Skill Packager

Use this skill when the user wants to create, repair, review, rename, repackage, or republish a ClawHub / OpenClaw skill bundle.

## Identity note

This skill intentionally uses:
- `name: clawhub-pack` as the short runtime / slash identity
- `metadata.openclaw.skillKey: clawhub-skill-packager` as the fuller registry / config identity

Treat this split as deliberate, not as drift.

## Core job

This skill turns user input, existing skill files, or partial drafts into a **publish-ready ClawHub skill bundle**.

It is designed to:
- inspect what is present
- infer what is missing when reasonable
- repair inconsistencies
- build the package anyway when a safe best-effort package is possible
- self-audit the result
- return both the package and clear review artifacts

## Operating stance

This skill is designed for **low-friction handoff**.

When the user provides material:
- inspect what is there
- infer what is missing when reasonable
- choose the best safe course based on current knowledge
- avoid unnecessary clarification loops
- return a concrete package plus a review statement

Prefer **statements** over **questions**.

If something is missing but inferable:
- infer it
- note the inference
- keep moving

If something is risky, ambiguous, or likely to affect publishing:
- still produce the package
- highlight the issue clearly in the review record
- mark it for user review

Do not stop at “more info needed” when a reasonable package can still be built.

## Required outputs

Always produce both primary deliverables:

### A. Publish bundle
A zip-ready skill folder containing the files needed for ClawHub / OpenClaw publishing.

Minimum expected files:
- `SKILL.md`
- `README.md`
- `CHANGELOG.md`

Optional files when useful:
- `NOTES.txt`
- `EXAMPLES.md`

### B. Plain-text review record
A simple file that any user or system can open without special software.

Preferred format:
- `.txt`

This review record should say:
- what inputs were provided
- what information was missing
- what assumptions were made
- what was added
- what was edited
- what was removed
- what was inferred
- what still deserves human review
- whether the package appears publish-ready

## Standard support artifacts

This packager also maintains reusable support files.

Use them like this:

- `REVIEW-CHECKLIST.txt` = the permanent self-audit standard
- `REVIEW-RECORD-TEMPLATE.txt` = the base for the generated per-run review record
- `DELIVERY-SUMMARY-TEMPLATE.txt` = the short user-facing completion summary
- `PUBLISH-HANDOFF.txt` = the final publish/install handoff format

## Packaging promise

Always finish by producing the intended package, even if some fields required inference.

If information is missing:
- determine the best safe default
- state the assumption clearly in the review record
- highlight the assumption for user review

If information is sufficient:
- package the skill cleanly
- audit it
- report what was done

## Operating modes

Use one of these modes based on the user's request and the material provided:

### 1. Package-from-scratch
Use when the user provides a concept, rough notes, or minimal package material.

### 2. Repair-existing-skill
Use when the user provides an existing skill package that needs cleanup, fixes, or modernization.

### 3. Audit-only
Use when the user wants analysis and recommendations without generating a new package.

### 4. Republish / update
Use when the user already has a package and wants version, naming, positioning, or packaging updates for republishing.

### 5. Rename / rebrand
Use when identity surfaces need changing while preserving intended behavior.

## Two-pass workflow by mode

The packager always works in two passes, but the shape of those passes depends on the mode.

### Package-from-scratch
Pass 1:
- assemble identity
- infer missing metadata
- define package surfaces
- identify major assumptions

Pass 2:
- build files
- self-audit
- generate review record and handoff artifacts

### Repair-existing-skill
Pass 1:
- inspect existing files
- identify drift, breakage, or parser-risky structure
- determine what should be preserved

Pass 2:
- repair and normalize
- self-audit
- generate review record and handoff artifacts

### Audit-only
Pass 1:
- inspect the provided package or concept
- identify strengths, issues, risks, and missing information

Pass 2:
- generate the review record and user-facing summary
- do not build a replacement package unless the user also asked for packaging

### Republish / update
Pass 1:
- inspect the current package
- identify what changed since the prior release
- align versioning, naming, and publish surfaces

Pass 2:
- update files
- self-audit
- generate review record and handoff artifacts

### Rename / rebrand
Pass 1:
- inspect current identity surfaces
- preserve intended behavior
- determine which naming surfaces change and which remain stable

Pass 2:
- rewrite aligned identity surfaces
- self-audit
- generate review record and handoff artifacts

## Packaging workflow

### Step 1 — Inspect
Look at all provided material:
- text prompts
- existing `SKILL.md`
- existing `README.md`
- existing `CHANGELOG.md`
- file names
- intended display name
- intended slug
- invocation ideas
- notes about platform behavior
- prior package artifacts if relevant

### Step 2 — Determine completeness
Check whether the package has enough information for:
- display name
- slug
- internal skill name
- version
- description
- tags
- invocation behavior
- public positioning
- file set
- frontmatter format
- compatibility with current OpenClaw parser expectations

### Step 3 — Infer or repair
If something is missing or inconsistent:
- choose the best safe default
- repair mismatched naming
- align slug, skill key, package folder name, and README publish fields
- correct parser-risky frontmatter
- normalize versioning
- remove obvious contradictions
- preserve intended behavior whenever possible

### Step 4 — Build the package
Create the full package folder and final file contents.

### Step 5 — Self-audit
Run a second-pass review using `REVIEW-CHECKLIST.txt`.

### Step 6 — Deliver
Deliver:
- the final zip/package
- the plain-text review record built from `REVIEW-RECORD-TEMPLATE.txt`
- the short user-facing summary built from `DELIVERY-SUMMARY-TEMPLATE.txt`
- the publish/install handoff built from `PUBLISH-HANDOFF.txt`
- any highlighted assumptions or issues needing user review

## Skill type awareness

When packaging a skill, classify it before building.

Possible classes include:
- instruction-only skill
- formatting / style skill
- workflow / orchestration skill
- code or script-backed skill
- API-dependent skill
- environment-variable-dependent skill
- binary / external-tool-dependent skill
- mixed package

Use the class to decide:
- what files are needed
- what install notes are needed
- what security notes are needed
- what review flags matter most

## Runtime and security declarations

Inspect for:
- environment variable requirements
- secrets or credentials
- external API dependencies
- script or binary execution assumptions
- file system expectations
- privilege or escalation requirements
- background or always-on behavior

If these exist:
- package the skill anyway when safe
- state them clearly in the review record
- highlight them for review

## Frontmatter rules

For OpenClaw compatibility, prefer:
- single-line frontmatter keys
- `metadata` as a single-line JSON object
- quoted `version`
- quoted long `description` strings when helpful

Preferred base frontmatter pattern:

```yaml
---
name: skill-name
description: "Short clear skill description."
version: "1.0.0"
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"📦","skillKey":"skill-slug"}}
---
```

## Naming rules

Align these surfaces unless the user explicitly wants them different:
- public display name
- package folder name
- slug
- `metadata.openclaw.skillKey`
- README publish fields
- changelog package identity

Use:
- human-readable title for display name
- lowercase hyphenated form for slug
- concise internal command name when user invocation is intended

## Review checklist

A package should be checked for all of the following:

### Identity alignment
- display name matches intent
- slug is lowercase and hyphenated
- folder name matches slug
- skill key matches slug
- README publish fields match final identity
- changelog reflects the current version and identity

### Frontmatter health
- `SKILL.md` exists
- frontmatter is present
- `name` exists
- `description` exists
- `version` exists
- `metadata` uses single-line JSON
- invocation flags are present when useful
- emoji is present if desired
- parser-risky nested metadata is repaired

### Behavioral clarity
- purpose is clear
- scope is clear
- activation behavior is clear
- explicit invocation is defined if needed
- output behavior is described
- risky ambiguity is reduced

### Public positioning
- branding is reasonable
- wording is accurate
- descriptions do not overclaim capabilities
- external affiliation wording is safe when relevant

### Runtime / security awareness
- skill type is correctly classified
- env var requirements are documented
- API dependencies are documented
- binaries / scripts are documented
- privilege assumptions are documented
- risky surfaces are highlighted

### Deliverables
- package files were generated
- review record was generated
- changes are summarized
- assumptions are highlighted
- publish-readiness is stated

## Severity markers

Use these markers consistently:

- **✅ FIXED AUTOMATICALLY** = safe automatic repair completed
- **🔶 INFERRED FIELD** = best-effort inferred value that should remain visible
- **⚠️ REQUIRED REVIEW** = likely publish-affecting issue that deserves human confirmation
- **📝 EDITED FOR ALIGNMENT** = consistency edit across identity or package surfaces
- **🚀 READY TO PUBLISH** = no major blocker detected in the final package

## Final response contract

At completion, report in this order:
1. brief status line
2. link or handoff to the publish-ready package
3. link or handoff to the review record
4. link or handoff to the publish/install handoff
5. short bullet summary of:
   - what was created
   - what was changed
   - what assumptions were made
   - what should be reviewed
6. publish-readiness statement

The response should tell the user, in plain terms:
- here is what you gave me
- here is what I inferred
- here is what I fixed
- here is what I packaged
- here is what I think you may want to adjust

## Second-pass workflow

If the user returns with edits or clarifications:
- re-run the same inspection and package workflow
- preserve the accepted identity and structure unless the new instructions change them
- reduce the number of inferred fields
- keep the second-pass output cleaner and closer to final
- aim for a near-zero-friction publish handoff

## Operating note

This skill is a packager and self-auditor for ClawHub / OpenClaw skills. Its job is to turn incomplete or inconsistent skill drafts into coherent publish-ready bundles while preserving the user's intended behavior whenever possible and minimizing decision friction for the user.
