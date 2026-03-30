# Whatsonchain API

**Slug:** `whatsonchain`  
**Version:** `1.0.0`  
**Author:** ChicoCifrado

## ⚠️ IMPORTANT - MANUAL CONFIGURATION REQUIRED

**After installation, you must run the onboard script to configure your API key:**

```bash
cd /home/$USER/.openclaw/workspace/skills/whatsonchain
bash scripts/onboard.sh
```

## Installation

```bash
clawhub install whatsonchain
```

## Authentication

### Methods

1. **Email + Password**
   - Script attempts to extract email from clawhub settings
   - Falls back to manual input
   - Automates login to Teranode Platform

2. **OAuth GitHub**
   - Automatic authentication
   - No password required
   - Email optional

3. **OAuth Google**
   - Automatic authentication
   - No password required
   - Email optional

### Registration URL

After installation, visit:  
`https://platform.teranode.group/register`

For login:  
`https://platform.teranode.group/login`

## Setup Process

The onboard script will guide you through:

1. **Authentication Method Selection**
   - Choose one of the three methods above

2. **Authentication**
   - Register/login to Teranode Platform
   - For OAuth: automatic authentication

3. **Project Creation**
   - Creates a descriptive project name

4. **API Key Acquisition**
   - Generates or selects your API key

5. **Environment Setup**
   - Configures `WATSONCHAIN_API_KEY` environment variable
   - Adds to `~/.bashrc` (optional)

## Available Tools

After setup, these tools will be available in OpenClaw:

- **mainnetInfo**: Get BSV mainnet network status
- **testnetInfo**: Get BSV testnet network status
- **txHash**: Get transaction by hash
- **txIndex**: Get transaction by block height + index
- **txPropagation**: Check transaction propagation status
- **blockInfo**: Get block by height
- **txHex**: Get raw transaction hex
- **txBin**: Get raw transaction binary
- **decodeTx**: Decode raw transaction hex
- **broadcastTx**: Broadcast transaction to network

## API Endpoints

- Platform Register: `https://platform.teranode.group/register`
- Platform Login: `https://platform.teranode.group/login`
- Platform Projects: `https://platform.teranode.group/projects`
- Platform API Keys: `https://platform.teranode.group/api-keys`
- BSV API: `https://api.whatsonchain.com/v1/mainnetInfo`

## Rate Limits

- Free tier: 3 requests/second
- Premium: 10, 20, or 40 requests/second

## Documentation

Full documentation is available in `SKILL.md`.

## Support

- Telegram: WhatsonChain devs channel
- Platform: https://platform.teranode.group

## License

MIT
