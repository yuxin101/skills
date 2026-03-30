---

name: settlement-witness
description: "Verify structured agent task outputs with signed receipts and optional TrustScore attribution."
-------------------------------------------------------------------------------------------------------------

# SettlementWitness

**Verify structured agent task outputs and return signed proof of outcome.**

---

## What this does

**Did the agent deliver what was specified?**

SettlementWitness evaluates **structured task inputs you choose to submit** (spec + output) and returns:

* A deterministic verdict: **PASS / FAIL / INDETERMINATE**
* A signed **Settlement Attestation Receipt (SAR)**
* An optional **TrustScore update** when an `agent_id` is provided

Every agent can claim success. SettlementWitness makes selected outcomes **provable**.

Verification is optional and should be applied only to tasks where independent proof is required.

---

## Why verify?

Every receipt:

* Builds a verifiable history of agent performance
* Provides **objective evidence of task outcomes**
* Creates an auditable record for downstream systems

Receipts are signed and portable — they can be verified independently.

---

## Quickstart

```javascript
settlement_witness({
  task_id: "task-001",
  agent_id: "0xYourWallet:my-agent",
  spec: { expected: "report generated" },
  output: { expected: "report generated" }
})
```

Returns:

```json
{
  "receipt_v0_1": {
    "verdict": "PASS",
    "confidence": 1.0,
    "reason_code": "SPEC_MATCH",
    "receipt_id": "sha256:...",
    "verifier_kid": "sar-prod-ed25519-02",
    "sig": "base64url:..."
  },
  "counterparty": "0xCounterpartyWallet",
  "_ext": {
    "agent_id": "0xYourWallet:my-agent"
  },
  "trustscore_update": {
    "score": 54,
    "tier": "bronze"
  }
}
```

---

## Where it fits

Insumer → x402 → SettlementWitness → TrustScore

Attestation → Payment signal → Delivery verification → Reputation layer

---

## Endpoints

Production:
POST https://defaultverifier.com/settlement-witness

x402 Base:
POST https://defaultverifier.com/x402/settlement-witness

x402 Solana:
POST https://defaultverifier.com/x402/settlement-witness-solana

Public keys:
https://defaultverifier.com/.well-known/sar-keys.json

---

## Agent identity (optional)

`agent_id: "0xYourWallet:your-agent-name"`

* A wallet address enables persistent attribution across sessions
* The agent name distinguishes multiple agents under one wallet
* TrustScore is computed per `agent_id` when provided

If no identity is provided, verification still functions without attribution.

---

## Provenance

SettlementWitness is operated via:
https://defaultverifier.com

For transparency:

* Public verification keys:
  https://defaultverifier.com/.well-known/sar-keys.json

* Protocol specification:
  https://defaultverifier.com/spec/sar-v0.1/

Users should independently validate the service before relying on verification results.

---

## Verifier model

SettlementWitness is a **stateless verification service**:

* Verification is performed on submitted structured inputs only
* Receipts are generated deterministically from inputs
* Signatures use Ed25519 and can be independently verified
* No persistent agent state is required for validation

Trust in verification depends on validating the service origin and public keys.

---

## Data handling

SettlementWitness processes **only structured task evaluation data** (spec and output).

Guidelines:

* Submit only the minimum data required for evaluation
* Do NOT include secrets, API keys, credentials, or private data
* Inputs are used solely for verification and receipt generation

SettlementWitness does not require full application context or arbitrary data.

---

## What SettlementWitness is not

* Not a payment processor
* Not a fund custodian
* Not an enforcement layer
* Not a data storage system

---

## What it is

* Deterministic verifier
* Signed receipt issuer
* Verifiable proof system
* Reputation input layer

---

Spec: https://defaultverifier.com/spec/sar-v0.1/
