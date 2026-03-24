# Proxy Gateway

> 🚀 **Secure HTTP Proxy for AI Agents** — Unrestricted internet access with pay-per-use pricing. Start with 10 free requests, then only $0.001 per API call.

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](https://proxy.easky.cn)
[![Security](https://img.shields.io/badge/security-audited-green.svg)](SECURITY.md)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Network](https://img.shields.io/badge/network-Polygon-purple.svg)](https://polygon.technology)

## ⚠️ Security & Privacy Notice

**Please read carefully before using this service:**

### 🔒 Privacy Risks

**All requests transit through the proxy server**, including:
- Full request URLs
- All HTTP headers
- Request bodies
- Response content

**DO NOT use this proxy for:**
- API keys or access tokens
- Private keys or passwords
- Personal or sensitive data
- Internal/private network endpoints
- Banking or financial credentials

### 💰 Trust Model

This service operates on a **custodial model**:
- You deposit USDC to a platform-controlled address
- The platform maintains your balance and authorizes access
- This requires trust in the platform operator

### 🏠 Self-Hosting Option

For maximum privacy and control, **self-host this service**:
- Full source code available (MIT License)
- Complete data sovereignty
- No third-party visibility
- Easy deployment with Docker or pip

---

## ✨ Why Proxy Gateway?

| Feature | Benefit |
|---------|---------|
| 🎁 **10 Free Requests** | Start instantly, no credit card required |
| ⚡ **Zero Configuration** | No local proxy setup, just call the API |
| 💵 **Pay-Per-Use** | Only $0.001 per request, no subscriptions |
| 🔐 **Security Audited** | 6 security audits, 13 P0 vulnerabilities fixed |
| 📖 **Open Source** | MIT licensed, fully auditable code |
| 🌍 **Multi-Region** | US, EU, Asia proxy nodes |
| 🔗 **Web3 Native** | Polygon blockchain, USDC payments |
| 🏠 **Self-Host Ready** | Deploy your own instance in minutes |

---

## 🚀 Quick Start

### 1. Start with Free Trial (10 Requests)

```python
import requests

response = requests.post(
    "https://proxy.easky.cn/api/v1/fetch",
    headers={"X-Client-ID": "my_agent_001"},
    json={
        "url": "https://api.github.com/users/github",
        "method": "GET"
    }
)

data = response.json()
print(data["content"])  # Response content
print(f"Remaining free calls: {data['remaining_calls']}")
```

### 2. Continue with Paid Mode

After free trial, deposit USDC to continue:

```python
# Use your user_id as API Key after deposit
response = requests.post(
    "https://proxy.easky.cn/api/v1/fetch",
    headers={"X-API-Key": "my_agent_001"},
    json={
        "url": "https://api.example.com/data",
        "method": "GET"
    }
)
```

---

## 💰 Pricing

| Tier | Price | Features |
|------|-------|----------|
| **Free Trial** | **FREE** | 10 requests, no registration |
| **Pay-Per-Use** | **$0.001/request** | Unlimited calls, pay as you go |
| **Self-Hosted** | **FREE** | Run your own server |

- **Currency**: USDC on Polygon
- **Minimum Deposit**: None (top up any amount)
- **Network Fees**: Paid by user for deposits

---

## 🌐 API Endpoints

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/` | GET | Service info | None |
| `/health` | GET | Health check | None |
| `/network-info` | GET | Network configuration | None |
| `/api/v1/regions` | GET | Available proxy regions | None |
| `/api/v1/fetch` | POST | Fetch any URL via proxy | Client ID or API Key |
| `/deposit-info` | GET | Get deposit address | None |
| `/balance` | GET | Check balance | Client ID |

---

## 🏠 Self-Hosting Guide

### Why Self-Host?

| Aspect | Hosted Service | Self-Hosted |
|--------|---------------|-------------|
| **Privacy** | Server sees all requests | Complete privacy |
| **Control** | Platform managed | Full control |
| **Cost** | Per-request fees | Server costs only |
| **Trust** | Requires trust | Trustless |
| **Setup** | Instant | 5-minute setup |

### Quick Deploy

```bash
# 1. Clone repository
git clone https://github.com/openclaw/proxy-gateway.git
cd proxy-gateway

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings:
# - HOSTED_WALLET: Your Polygon wallet address
# - ADMIN_TOKEN: Secure random string (16+ chars)

# 5. Start server
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Docker Deploy

```bash
# Build image
docker build -t proxy-gateway .

# Run container
docker run -d \
  -p 8080:8080 \
  -e NETWORK=mainnet \
  -e HOSTED_WALLET=0x... \
  -e ADMIN_TOKEN=... \
  proxy-gateway
```

---

## 🔒 Security Features

- ✅ **6 Security Audits** Completed by independent reviewers
- ✅ **13 P0 Vulnerabilities Fixed** All critical issues resolved
- ✅ **Input Validation** Strict validation on all inputs
- ✅ **Anti-Replay Protection** Transaction replay attack prevention
- ✅ **Atomic Deduction** Balance updates are atomic
- ✅ **HTTPS/TLS** All communications encrypted
- ✅ **Open Source** Full code transparency

**Security Policy**: See [SECURITY.md](SECURITY.md) for detailed security information and vulnerability reporting.

---

## 🛡️ Best Practices

### ✅ DO
- Use for public API access
- Use for web scraping public data
- Use for research automation
- Use for content aggregation
- Self-host for sensitive operations

### ❌ DON'T
- Send API keys through the proxy
- Send passwords or credentials
- Access private/internal networks
- Send personal information
- Send financial data

---

## 📝 Environment Variables

### Required (for self-hosting)

| Variable | Description | Example |
|----------|-------------|---------|
| `HOSTED_WALLET` | Polygon address for USDC deposits | `0x1234...abcd` |
| `ADMIN_TOKEN` | Admin authentication token | `random_string_16+` |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `NETWORK` | `testnet` | Network mode (mainnet/testnet) |
| `REDIS_HOST` | `localhost` | Redis server host |
| `REDIS_PORT` | `6379` | Redis server port |
| `FREE_TRIAL_LIMIT` | `10` | Free trial request limit |
| `COST_PER_REQUEST` | `0.001` | Price per request (USDC) |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |

See [.env.example](.env.example) for complete configuration template.

---

## 🤝 Contributing

Contributions are welcome! Please see our contributing guidelines and submit PRs.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🆘 Support

- **Documentation**: https://proxy.easky.cn
- **Issues**: GitHub Issues
- **Email**: support@proxy.easky.cn

---

**Built with ❤️ for the AI Agent ecosystem**
