---
name: tradesman-verify
version: 2.1.0
description: Verify contractor credentials via OpenCorporates business entity lookup (140+ jurisdictions) and Accumulate blockchain ADI verification. Issues and verifies W3C Verifiable Credentials for KYC, contractor license, insurance, and business entity. ACME Foundation reference implementation.
homepage: https://gitlab.com/lv8rlabs/tradesman-verify
metadata:
  openclaw:
    emoji: "🔐"
    primaryEnv: OPENCORPORATES_API_KEY
    requires:
      env:
        - OPENCORPORATES_API_KEY
    install:
      - kind: node
        package: tradesman-verify
        bins:
          - tradesman-verify
---

# Tradesman Verify Skill

**Proof-of-Credential infrastructure for contractor verification** combining OpenCorporates business entity verification, state licensing board checks, and blockchain-compatible credential attestation. Similar to Centrifuge's Proof-of-Index (SPXA) but designed specifically for service provider credentials in the construction and trades industry.

## Overview

BIMPassport's Proof-of-Credential system establishes verifiable trust for contractors, tradesmen, and service providers through multi-layer verification:

- **Layer 1**: Business entity verification (OpenCorporates, 140+ jurisdictions)
- **Layer 2**: Professional license validation (state licensing boards)
- **Layer 3**: Risk assessment and compliance screening (optional)
- **Layer 4**: Blockchain attestation (deRWA-compatible credentials)

This skill provides the foundational verification layer that feeds into tradesman-validate for credential issuance.

## Features

### Proof-of-Credential Infrastructure

**What is Proof-of-Credential?**

Similar to how Centrifuge's Proof-of-Index (SPXA) verifies the existence and characteristics of real-world assets for DeFi lending, BIMPassport's Proof-of-Credential verifies the existence and legitimacy of service provider credentials for decentralized workforce coordination.

**Key Capabilities:**
- Multi-jurisdictional business entity verification (140+ countries via OpenCorporates)
- Professional license validation across all US states
- Real-time status monitoring (active, suspended, expired)
- Historical verification audit trail
- deRWA-compatible output format for on-chain attestation

### OpenCorporates Integration

**Business Entity Verification:**
- Legal business entity exists and is registered
- Company status (Active, Dissolved, Liquidated)
- Incorporation date (business longevity indicator)
- Registered officers and ownership structure
- Business address verification

**Jurisdictions Supported:**
- United States (all 50 states + DC)
- United Kingdom
- Canada
- Australia
- 140+ additional countries

### State Licensing Board Validation

**Professional License Checks:**
- Contractor license active status
- License number and business name matching
- Specialty certifications (electrical, plumbing, HVAC, roofing, etc.)
- License expiration date and renewal status
- Disciplinary action history

**US State Coverage:**
- All 50 states supported
- Automated checks where state APIs available
- Manual verification workflow for states without APIs

### BMLS Framework Integration

This skill implements the **Build-Measure-Learn-Share (BMLS)** framework:

**Build:** Verification infrastructure for contractor credentials
**Measure:** Verification success rates, API response times, license expiration tracking
**Learn:** Identify high-risk jurisdictions, optimize verification workflows
**Share:** Anonymized verification metrics published quarterly (via BIMHero DAO)

See [BMLS-FRAMEWORK.md](../../BMLS-FRAMEWORK.md) for detailed framework documentation.

## Usage

### Free Tier

**Limits:**
- 50 verifications per month
- OpenCorporates free tier (200 API calls/month)
- Manual state licensing board checks
- Basic verification reports (JSON format)

**Suitable for:**
- Small contractors verifying occasional subcontractors
- Testing and development
- Individual property managers

### CLI Usage

```bash
# Basic verification
npx tradesman-verify \
  --business-name "ABC Roofing LLC" \
  --jurisdiction "us_tx" \
  --license-number "123456" \
  --state "TX"

# Output
✅ Business Entity Verified
   Company: ABC ROOFING LLC
   Status: Active
   Incorporated: 2020-05-15
   Jurisdiction: us_tx

✅ Professional License Verified
   License: 123456
   Status: Active
   Expires: 2026-12-31
   Type: General Contractor

✅ VERIFICATION PASSED
   Recommendation: APPROVED
   Valid Until: 2027-02-13
```

### API Usage

```javascript
const { verifyContractor } = require('tradesman-verify');

const result = await verifyContractor({
  businessName: "ABC Roofing LLC",
  jurisdiction: "us_tx",
  licenseNumber: "123456",
  state: "TX"
});

// Output
{
  "contractorId": "abc_roofing_llc",
  "verificationStatus": "VERIFIED",
  "verificationDate": "2026-02-18T14:00:00Z",
  "businessVerification": {
    "isRegistered": true,
    "isActive": true,
    "incorporationDate": "2020-05-15",
    "businessAge": "5.75 years",
    "jurisdiction": "us_tx",
    "companyNumber": "0803456789"
  },
  "licenseVerification": {
    "isValid": true,
    "licenseNumber": "123456",
    "licenseType": "General Contractor",
    "expirationDate": "2026-12-31",
    "status": "Active"
  },
  "recommendation": "APPROVED"
}
```

### Batch Processing

```bash
# Verify multiple contractors from CSV
npx tradesman-verify --batch --input contractors.csv --output verification-report.json

# Output
Processing 15 contractors...
✅ 12 verified successfully
⚠️  2 require manual review
❌ 1 failed verification

Details saved to: verification-report.json
```

## Output Format

### deRWA-Compatible Credential Format

Verification results can be output in deRWA-compatible format for blockchain attestation:

```json
{
  "credentialType": "ProofOfCredential",
  "credentialSubtype": "ContractorVerification",
  "subject": {
    "businessName": "ABC Roofing LLC",
    "jurisdiction": "us_tx",
    "licenseNumber": "123456"
  },
  "verification": {
    "businessEntity": {
      "verified": true,
      "source": "OpenCorporates",
      "verifiedAt": "2026-02-18T14:00:00Z",
      "status": "Active"
    },
    "professionalLicense": {
      "verified": true,
      "source": "Texas Dept. of Licensing",
      "verifiedAt": "2026-02-18T14:00:00Z",
      "status": "Active",
      "expiresAt": "2026-12-31T23:59:59Z"
    }
  },
  "attestation": {
    "attestedBy": "BIMPassport-ProofOfCredential-v1",
    "attestedAt": "2026-02-18T14:00:00Z",
    "validUntil": "2027-02-18T14:00:00Z",
    "checksumSHA256": "a3f5b8c..."
  }
}
```

This format is compatible with:
- Accumulate ADI credential issuance (via tradesman-validate)
- Circle ARC attestation infrastructure
- Centrifuge Proof-of-X framework
- W3C Verifiable Credentials

## Upgrade Paths

### Premium Tiers

**PPCS Pro** (ppcs.pro)
- 500 verifications/month
- Automated state license checks (premium tier)
- Real-time status monitoring webhooks
- Priority support
- Pricing: $99/month

**Enterprise** (lv8rlabs.com)
- Unlimited verifications
- Dedicated API endpoint
- Custom integrations
- Risk assessment layer (premium providers)
- White-label branding
- SLA guarantees
- Pricing: Contact sales

### Premium Features

**Real-Time Monitoring:**
```javascript
// Webhook notification when contractor license status changes
POST https://your-app.com/webhooks/license-status
{
  "event": "license_status_changed",
  "contractorId": "abc_roofing_llc",
  "licenseNumber": "123456",
  "previousStatus": "Active",
  "newStatus": "Expired",
  "changedAt": "2026-06-30T23:59:59Z"
}
```

**Risk Assessment:**
- Sanctions and watchlist screening
- Adverse media monitoring
- Litigation history
- Financial stability indicators
- Overall risk score (0-100)

**Advanced Analytics:**
- Verification success rate trends
- Geographic risk heatmaps
- License expiration forecasting
- Compliance dashboard

## Integration with BIMPassport Ecosystem

### tradesman-validate Integration

After verification via `tradesman-verify`, credentials can be issued on-chain via `tradesman-validate`:

```bash
# Step 1: Verify contractor
npx tradesman-verify --business-name "ABC Roofing LLC" --jurisdiction "us_tx" --license-number "123456" --state "TX"

# Step 2: Issue blockchain credential (requires tradesman-validate)
npx tradesman-validate --contractor-id "abc_roofing_llc" --adi-url "abc.acme/contractor" --credential-type "contractor-license"
```

### deRWA Compatibility

BIMPassport credentials are compatible with decentralized Real-World Asset (deRWA) protocols:

- **Centrifuge**: Can be used as proof documents for service provider financing
- **Circle ARC**: Attestation-ready format for institutional compliance
- **Accumulate**: Native ADI credential issuance
- **Chainlink Functions**: Off-chain verification oracle integration

### BIMHero DAO Governance

Verification metrics and standards are governed by BIMHero DAO (details in BMLS-FRAMEWORK.md):

- Quarterly publication of anonymized verification metrics
- Community-driven threshold adjustments (e.g., code similarity for IP violations)
- Transparent policy evolution
- Open-source verification algorithms (premium risk models proprietary)

## Environment Variables

### Required (Free Tier)

```bash
# OpenCorporates API (Free tier: 200/month)
OPENCORPORATES_API_KEY="your-opencorporates-api-key"
```

### Optional (Premium Tiers)

```bash
# PPCS Premium API (license automation + risk assessment)
PPCS_API_KEY="your-ppcs-api-key"
```

## API Rate Limits

| Tier | Verifications/Month | API Calls/Month | Real-Time Monitoring |
|------|---------------------|-----------------|---------------------|
| **Free** | 50 | 200 (OpenCorporates) | No |
| **PPCS Pro** | 500 | Unlimited | Yes |
| **Enterprise** | Unlimited | Unlimited | Yes + SLA |

## Error Handling

### OpenCorporates Errors

**Rate Limit Exceeded (429):**
```javascript
{
  "error": "rate_limit_exceeded",
  "message": "Daily limit of 50 requests exceeded",
  "action": "Upgrade to paid plan or retry after 24 hours"
}
```

**Company Not Found (404):**
```javascript
{
  "error": "business_entity_not_found",
  "message": "No registered business found for 'ABC Roofing LLC' in us_tx",
  "action": "Verify business name spelling, check jurisdiction, request incorporation docs"
}
```

### License Verification Errors

**License Expired:**
```javascript
{
  "error": "license_expired",
  "licenseNumber": "123456",
  "expirationDate": "2025-12-31",
  "action": "Request updated license documentation from contractor"
}
```

**License Suspended:**
```javascript
{
  "error": "license_suspended",
  "licenseNumber": "123456",
  "suspensionDate": "2026-01-15",
  "reason": "Non-payment of renewal fee",
  "action": "CRITICAL - Block contractor from new jobs, escalate to compliance team"
}
```

## Success Criteria

### Verification Passed
```javascript
{
  "status": "VERIFIED",
  "confidence": "HIGH",
  "checks": {
    "businessEntity": "PASSED",
    "professionalLicense": "PASSED"
  },
  "recommendation": "APPROVED",
  "validUntil": "2027-02-18T14:00:00Z"
}
```

### Verification Failed
```javascript
{
  "status": "FAILED",
  "confidence": "N/A",
  "checks": {
    "businessEntity": "FAILED",
    "professionalLicense": "NOT_FOUND"
  },
  "recommendation": "REJECT",
  "reason": "Business entity dissolved, license not found"
}
```

### Manual Review Required
```javascript
{
  "status": "PENDING",
  "confidence": "MEDIUM",
  "checks": {
    "businessEntity": "PASSED",
    "professionalLicense": "MANUAL_CHECK_REQUIRED"
  },
  "recommendation": "MANUAL_REVIEW",
  "reason": "State licensing board has no API, manual verification required"
}
```

## Testing

### Test with OpenCorporates Free Tier

```bash
# Set test API key
export OPENCORPORATES_API_KEY="test_key_xxxxx"

# Test company search
curl --header "X-API-TOKEN:$OPENCORPORATES_API_KEY" \
  "https://api.opencorporates.com/v0.4/companies/search?q=test&jurisdiction_code=us_tx"

# Verify API quota
curl --header "X-API-TOKEN:$OPENCORPORATES_API_KEY" \
  "https://api.opencorporates.com/v0.4/account_status"
```

### Mock Data for Development

```javascript
const mockVerificationResult = {
  status: "VERIFIED",
  businessEntity: {
    isActive: true,
    incorporationDate: "2020-01-01",
    jurisdiction: "us_tx"
  },
  license: {
    isValid: true,
    expirationDate: "2026-12-31",
    status: "Active"
  },
  recommendation: "APPROVED"
};
```

## Roadmap

### Phase 1: Core Verification (Current)
- ✅ OpenCorporates business entity verification
- ✅ Manual state licensing board checks
- ✅ deRWA-compatible output format
- ✅ Free tier implementation

### Phase 2: Enhanced Automation (Q2 2026)
- 🔄 Automated license check integration (premium tier)
- 🔄 Automated state license checks (all 50 states)
- 🔄 Real-time status change webhooks
- 🔄 Premium tier launch

### Phase 3: Blockchain Attestation (Q3 2026)
- 📋 Native Accumulate ADI integration
- 📋 Circle ARC attestation support
- 📋 Centrifuge proof document formatting
- 📋 Chainlink oracle integration

### Phase 4: Advanced Risk (Q4 2026)
- 📋 Advanced risk assessment layer
- 📋 Sanctions screening
- 📋 Litigation monitoring
- 📋 Financial stability indicators

## Support

### Documentation
- [tradesman-verify npm library](https://gitlab.com/lv8rlabs/tradesman-verify)
- [BMLS Framework](../../BMLS-FRAMEWORK.md)
- [OpenCorporates API Docs](https://api.opencorporates.com/documentation/API-Reference)

### State Licensing Resources
- [Texas TDLR](https://www.tdlr.texas.gov/LicenseSearch/)
- [California CSLB](https://www.cslb.ca.gov/onlineservices/checklicenseII/checklicense.aspx)
- [Washington L&I](https://secure.lni.wa.gov/verify/)
- [License Lookup Directory](https://licenselookup.org/)

### Upgrade & Pricing
- **PPCS Pro**: https://ppcs.pro/pricing
- **Enterprise**: https://lv8rlabs.com/contact
- **Community Support**: https://gitlab.com/lv8rlabs/tradesman-verify/-/issues

## License

MIT License - See [LICENSE](../../LICENSE) file for details.

**Open Source Tier**: Free forever for up to 50 verifications/month
**Commercial Tiers**: PPCS Pro and Enterprise require paid subscription

---

**Skill Version**: 2.1.0
**Last Updated**: 2026-02-28
**Maintainer**: TradesmanTools / BIMPassport
**Status**: Production-Ready
**ClawHub Submission**: Ready
