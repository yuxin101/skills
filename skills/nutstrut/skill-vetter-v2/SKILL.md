---

name: skill-vetter-v2
description: "Analyze and classify agent skills for safety using local evaluation. Optionally produce a signed attestation of the vetting result."
--------------------------------------------------------------------------------------------------------------------------------------------------

# Skill Vetter v2

**Evaluate agent skills for safety using local analysis. Optionally produce verifiable attestations of the result.**

---

## What this does

Skill Vetter v2 analyzes a skill’s instructions, structure, and behavior to determine:

* What the skill does
* What permissions or capabilities it uses
* Whether it introduces security or trust risks

All analysis and decisions are performed **locally**.

---

## Core principle

**Never delegate safety decisions to external systems.**

Skill Vetter v2:

* Performs all classification and risk assessment locally
* Does not rely on external services to determine safety
* Produces a structured vetting report that can be reviewed or shared

---

## Evaluation categories

Each skill is evaluated across three dimensions:

### 1. Install-time risk

* Does the skill write files?
* Does it fetch packages or execute code?
* Does it modify system configuration?

### 2. Runtime behavior

* Does it call external endpoints?
* Does it process user data?
* Does it request credentials or secrets?

### 3. Trust dependency

* Does it rely on an external authority?
* Is that authority transparent and auditable?
* Can outputs be independently verified?

---

## External service classification

External services are not automatically unsafe. They are classified as:

### Opaque external service (higher risk)

* Unknown operator or provenance
* No public documentation or spec
* No independent verification method
* Requires arbitrary or sensitive data

### Transparent verification service (lower risk)

* Clearly defined purpose
* Accepts structured, minimal inputs
* Explicitly prohibits secrets
* Provides public verification material (e.g. keys, spec)
* Outputs can be independently verified

---

## Output format

Skill Vetter produces a structured report:

```json
{
  "purpose": "...",
  "capabilities": [...],
  "install_risk": "low | medium | high",
  "runtime_risk": "low | medium | high",
  "trust_dependency": "none | transparent | opaque",
  "warnings": [...],
  "recommendations": [...],
  "verdict": "safe | caution | unsafe"
}
```

---

## Optional attestation (SAR)

After producing a vetting report, you may optionally generate a signed attestation.

This step is:

* **Optional**
* Performed only on the final report
* Used to create a verifiable record of the vetting outcome

Example:

```javascript
settlement_witness({
  task_id: "skill-vetting-001",
  spec: { expected: "valid vetting report structure" },
  output: vetting_report
})
```

Important:

* The attestation does **not determine the verdict**
* It only provides a signed proof that the evaluation was performed

---

## Safety guidelines

* Never include secrets, credentials, or private data in analysis
* Treat all external calls as potential data exposure points
* Prefer skills that operate locally or use transparent verification services
* Validate claims made by any external system before trusting outputs

---

## What this skill is not

* Not a code execution tool
* Not an installer
* Not a network client
* Not a decision authority outside local analysis

---

## What it is

* Local safety evaluator
* Risk classification tool
* Trust dependency analyzer
* Optional attestation generator

---

## Summary

Skill Vetter v2 enables agents to:

* Understand what a skill does
* Identify risks before installation or execution
* Classify trust dependencies clearly
* Optionally produce a signed, portable record of the evaluation

All safety decisions remain local and under agent control.
