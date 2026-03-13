---
name: ai-compliance
description: >
  AI compliance analysis for EU AI Act, ISO 42001, NIST AI RMF, GDPR, OECD, and other frameworks.
  Use when asked to generate a compliance checklist for an AI tool or use case, determine if a risk
  assessment is required, identify where an AI tool or use case could run afoul of regulatory
  requirements, perform a gap analysis against AI compliance frameworks, or recommend solutions to
  compliance issues. Triggers on phrases like "compliance checklist", "risk assessment", "does this
  comply", "EU AI Act", "ISO 42001", "NIST AI RMF", "AI governance", "gap analysis", or any request
  to evaluate an AI tool or use case for regulatory compliance.
---

# AI Compliance Skill

## Reference Files
Load only what's needed based on the frameworks relevant to the request:

- **EU AI Act** → `references/eu-ai-act.md` (risk tiers, prohibited uses, high-risk obligations)
- **ISO 42001** → `references/iso-42001.md` (clauses, Annex A controls)
- **NIST AI RMF** → `references/nist-ai-rmf.md` (GOVERN/MAP/MEASURE/MANAGE)
- **GDPR, OECD, IEEE, UK, Singapore** → `references/other-frameworks.md`
- **Checklist/gap analysis templates** → `references/checklist-templates.md`

When in doubt, load all four reference files — the frameworks overlap significantly.

## Workflow

### 1. Understand the AI Tool/Use Case
Gather (or ask for) the following before assessing:
- What does the AI system do? (intended purpose)
- Who uses it and how? (internal staff, customers, automated pipeline)
- What data does it process? (personal data, financial, sensitive)
- Where is it deployed? (EU context? affecting EU residents?)
- Is it a third-party tool (e.g., ChatGPT, Copilot) or internally built?

### 2. Classify Risk
Determine tier across frameworks:
- **EU AI Act**: Prohibited → High Risk → Limited → Minimal
- **NIST AI RMF**: Categorize by impact level (high/medium/low)
- **ISO 42001**: Confirm in scope of AIMS; classify per A.5.1
- **GDPR**: Triggers if personal data of EU residents is processed

Flag immediately if any prohibited use indicators are present.

### 3. Generate Output

#### For "compliance checklist" requests:
Use `references/checklist-templates.md` Template 1. Customize sections based on the tool's risk tier and applicable frameworks.

#### For "does this require a risk assessment?" requests:
Use Template 2 from `references/checklist-templates.md`. Walk through each step and provide a clear YES/NO determination with rationale.

#### For "gap analysis" or "where could this go wrong?" requests:
1. Assess against each applicable framework
2. Identify specific gaps (missing controls, missing documentation, missing processes)
3. Use Template 3 from `references/checklist-templates.md`
4. Rate each gap: HIGH / MEDIUM / LOW severity
5. Provide concrete remediation recommendations

### 4. Output Structure
Always structure output as:

```
## AI Compliance Assessment: [Tool/Use Case Name]
### Risk Classification
### Applicable Frameworks
### Compliance Checklist (or Gap Analysis)
### Issues Found
### Recommendations
### Priority Actions
```

## Key Principles
- Be specific: reference exact articles, clauses, and controls (e.g., "EU AI Act Article 14", "ISO 42001 Annex A.6.1", "NIST GOVERN 1.2")
- Flag HIGH severity issues prominently — these are blockers
- Always include remediation steps, not just gaps
- Cross-reference frameworks where they overlap (shows compliance efficiency)
- When uncertain about risk tier, err on the side of higher risk classification
