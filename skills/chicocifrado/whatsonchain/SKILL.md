# Whatsonchain

**API Key Management & BSV Blockchain Tools**

## Overview

Whatsonchain provides API tools for exploring the BSV blockchain, including transaction lookup, block information, and network status checks.

## Installation

```bash
clawhub install whatsonchain
```

## ⚠️ IMPORTANT - MANUAL CONFIGURATION REQUIRED

**After installation, you must run the onboard script to configure your API key:**

```bash
cd /home/$USER/.openclaw/workspace/skills/whatsonchain
bash scripts/onboard.sh
```

Or from anywhere:

```bash
bash /home/$USER/.openclaw/workspace/skills/whatsonchain/scripts/onboard.sh
```

## Usage

After running the onboard script, use in OpenClaw:

```
/tools
```

## API Key Storage

- **File:** `~/.clawhub/.env`
- **Permissions:** 600 (secure)
- **Environment Variable:** `WATSONCHAIN_API_KEY`
- **Optional:** Added to `~/.bashrc`

## Authentication

Three authentication methods available:

1. **Email + Password**
   - Automatic extraction from clawhub
   - Manual fallback
   - Platform login automation

2. **OAuth GitHub**
   - Automatic authentication
   - No password needed

3. **OAuth Google**
   - Automatic authentication
   - No password needed

## Rate Limits

- **Free:** 3 requests/second
- **Premium:** 10, 20, or 40 requests/second

## Platform URLs

- Register: `https://platform.teranode.group/register`
- Login: `https://platform.teranode.group/login`
- Projects: `https://platform.teranode.group/projects`
- API Keys: `https://platform.teranode.group/api-keys`

## BSV API

Mainnet: `https://api.whatsonchain.com/v1/mainnetInfo`

## Author

ChicoCifrado

## License

MIT
