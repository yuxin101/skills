---
name: whatsonchain-browser
description: Automatizar la obtención de API key de Teranode Platform usando openclaw browser. Registra usuario, verifica login y obtiene la API key "Starter".
---

# Whatsonchain-browser Skill

## About This Skill

This skill automates the entire authentication and API key acquisition process for the Whatsonchain API using OpenClaw's browser automation capabilities.

**What this skill does:**
- Automates registration on Teranode Platform
- Verifies user login status
- Creates projects automatically
- Extracts the "Starter" API key
- Configures environment variables

**When to use this skill:**
- User needs to install whatsonchain skill for the first time
- User wants to automate the entire setup process
- User needs to obtain the API key after installation
- User prefers browser automation over manual CLI tools

## Core Principles

1. **Browser Automation First**
   - Use OpenClaw browser (not Puppeteer, Selenium)
   - Prefer native browser automation
   - Fallback to curl for verification

2. **User-Guided Automation**
   - User provides instructions on what to click/fill
   - Assistant executes automation steps
   - Real-time feedback during process

3. **Minimal Manual Intervention**
   - Auto-fill forms where possible
   - Auto-click buttons
   - Auto-extract data

## Workflow Overview

### Step 1: User Selection
- User selects authentication method
  - 1. Email + Password
  - 2. OAuth GitHub
  - 3. OAuth Google
- User provides credentials if needed
- User selects project name

### Step 2: Platform Registration/Login
- Navigate to `https://platform.teranode.group/register`
- Fill registration form (or login directly)
- Submit and verify success
- Navigate to `https://platform.teranode.group/login`

### Step 3: Project Creation
- Navigate to `https://platform.teranode.group/projects`
- Click "Create New Project"
- Enter project name (or use default "OpenClaw")
- Confirm creation

### Step 4: API Key Acquisition
- Navigate to `https://platform.teranode.group/api-keys`
- Locate "Starter" API key
- Copy the API key
- Confirm extraction

### Step 5: Environment Configuration
- Save API key to `~/.clawhub/.env`
- Set permissions to 600
- Optionally add to `~/.bashrc`

## Authentication Methods

### 1. Email + Password

**Flow:**
1. Navigate to registration page
2. Fill email field
3. Fill password field
4. Click "Sign Up" or "Register"
5. Verify email (if required)
6. Login to platform
7. Proceed to project creation

**Automation Strategy:**
- Use browser automation to fill forms
- Detect form elements by CSS selectors
- Use XPath or CSS for dynamic elements
- Handle captcha if needed

### 2. OAuth GitHub

**Flow:**
1. Select OAuth GitHub option
2. Navigate to GitHub OAuth authorization
3. Grant permissions
4. Automatic redirect to Teranode
5. Proceed to project creation

**Automation Strategy:**
- Detect OAuth consent page
- Auto-click "Authorize" or "Allow"
- Follow redirect automatically
- Extract user info from response

### 3. OAuth Google

**Flow:**
1. Select OAuth Google option
2. Navigate to Google OAuth consent
3. Grant permissions
4. Automatic redirect to Teranode
5. Proceed to project creation

**Automation Strategy:**
- Detect Google OAuth consent page
- Auto-click "Continue" or "Allow"
- Follow redirect automatically
- Extract user info from response

## Available Tools

### Browser Automation
- **openclaw browser**: Navigate, click, fill, extract
- **CSS selectors**: Target specific elements
- **XPath**: Dynamic element selection
- **Form automation**: Fill and submit

### Verification Tools
- **curl**: API endpoint verification
- **HTTP requests**: Direct API calls
- **Status checking**: Verify success

### File Operations
- **Environment setup**: `~/.clawhub/.env`
- **Permissions**: `chmod 600`
- **Bashrc integration**: Optional export

## Environment Variables

- **WATSONCHAIN_API_KEY**: The API key obtained
- **PROJECT_NAME**: Name of created project
- **AUTH_METHOD**: Authentication method used
- **EMAIL**: User email for identification

## Platform URLs

- **Register:** `https://platform.teranode.group/register`
- **Login:** `https://platform.teranode.group/login`
- **Projects:** `https://platform.teranode.group/projects`
- **API Keys:** `https://platform.teranode.group/api-keys`

## Rate Limits

- **Free:** 3 requests/second
- **Premium:** 10, 20, or 40 requests/second

## Configuration

### Directory Structure

```
skills/whatsonchain-browser/
├── SKILL.md
├── scripts/
│   ├── register.sh          # Registration automation
│   ├── login.sh             # Login automation
│   ├── create-project.sh    # Project creation
│   ├── get-apikey.sh        # API key extraction
│   └── config.sh            # Environment setup
├── references/
│   ├── oauth-github.md      # OAuth GitHub details
│   └── oauth-google.md      # OAuth Google details
└── assets/
    ├── selectors.json       # CSS/XPath selectors
    └── forms.md             # Form structures
```

### Example Usage

```bash
# Install the skill
clawhub install whatsonchain

# Run the automation
cd /home/$USER/.openclaw/workspace/skills/whatsonchain
bash scripts/onboard.sh

# Or use browser automation directly
bash scripts/browser-automation.sh
```

## Error Handling

### Common Issues

1. **Registration Failed**
   - Email already exists
   - Captcha blocking automation
   - Network issues

2. **Login Failed**
   - Wrong credentials
   - Account locked
   - 2FA not handled

3. **API Key Not Found**
   - Wrong project selection
   - API key hidden behind login
   - Rate limit exceeded

### Recovery Procedures

- **Email exists:** Use existing account or different email
- **Captcha:** Manual verification step
- **Credentials:** Re-enter manually
- **Rate limit:** Wait before retrying

## Security Considerations

1. **API Key Storage**
   - Store in `~/.clawhub/.env`
   - Set permissions to 600
   - Never commit to git

2. **Credential Protection**
   - Never log passwords
   - Clear clipboard after copy
   - Use secure storage

3. **Browser Security**
   - Use headless mode when possible
   - Clear browser data after use
   - No persistent cookies

## Dependencies

- **openclaw browser**: Native browser automation
- **curl**: HTTP verification
- **bash**: Script execution
- **chmod**: Permission management

## Author

ChicoCifrado

## License

MIT
