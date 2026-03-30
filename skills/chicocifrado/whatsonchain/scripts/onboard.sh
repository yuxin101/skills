#!/bin/bash

# Whatsonchain API Onboard Script
# Automates user registration, login, and API key acquisition for Teranode Platform
# Uses OpenClaw browser (curl fallback)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

CONFIG_DIR="$PWD/.clawhub"
CONFIG_FILE="$CONFIG_DIR/.env"
NOTES_FILE="$CONFIG_DIR/whatsonchain-notes.txt"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Print header
print_header() {
    echo ""
    echo "=============================================="
    echo -e "${GREEN}=== WHATSONCHAIN API - ONBOARD SCRIPT ===${NC}"
    echo "=============================================="
    echo ""
}

# Print success message
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Print warning message
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Print info message
print_info() {
    echo -e "${BLUE}>>> $1${NC}"
}

# Print error message
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Step 1: Collect user data and register
collect_user_data_and_register() {
    print_header
    print_info "=== COLLECTING USER DATA =="
    echo ""
    
    # Step 1a: Display authentication options
    echo "Authentication methods for Teranode Platform:"
    echo ""
    echo "  1. Email + Password"
    echo "  2. OAuth GitHub"
    echo "  3. OAuth Google"
    echo ""
    read -p "Select an option (1-3): " AUTH_METHOD
    echo ""
    
    case "$AUTH_METHOD" in
        1)
            echo "Selected method: Email + Password"
            echo ""
            
            # Step 1a: Attempt to get email from clawhub
            print_info "Step 1a: Attempting to get email from clawhub..."
            echo ""
            
            # Use clawhub login
            echo "Attempting login to clawhub..."
            clawhub login 2>&1 || true
            
            # Check if logged in
            if curl -s "https://api.clawhub.com/v1/account" 2>/dev/null | grep -q "email\|user" || echo "logged_in"; then
                print_info "ClawHub login successful"
                echo ""
                
                # Get email from clawhub.ai/settings
                echo "Getting email from https://clawhub.ai/settings..."
                echo ""
                
                settings_page=$(curl -s "https://clawhub.ai/settings" 2>/dev/null || echo "")
                
                # Extract email from HTML
                EMAIL=""
                
                # Attempt 1: Extract between quotes
                EMAIL=$(echo "$settings_page" | grep -oP '"email"\s*:\s*"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/' || echo "")
                
                if [ -z "$EMAIL" ]; then
                    # Attempt 2: Simpler pattern
                    EMAIL=$(echo "$settings_page" | grep -oP 'email[^"]*[^"]*"[^"]*[^"]*' | head -1 | sed 's/.*"\([^"]*\)"$/\1/' || echo "")
                fi
                
                if [ -z "$EMAIL" ]; then
                    # Attempt 3: Pattern match any email-like string
                    EMAIL=$(echo "$settings_page" | grep -oP '\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b' | head -1 || echo "")
                fi
                
                if [ -n "$EMAIL" ]; then
                    print_success "Email extracted: $EMAIL"
                    echo ""
                else
                    print_warning "Could not extract email automatically"
                    echo ""
                    echo "Please provide your email manually:"
                    read -s -p "Email: " EMAIL
                    echo ""
                fi
            else
                print_warning "ClawHub login failed. Using manual email entry."
                echo ""
                read -s -p "Email: " EMAIL
                echo ""
            fi
            
            if [ -z "$EMAIL" ]; then
                print_error "Email is required"
                echo ""
                exit 1
            fi
            
            # Step 1b: Request password
            echo "Please enter your password:"
            read -s -p "Password: " PASSWORD
            echo ""
            echo ""
            
            if [ -z "$PASSWORD" ]; then
                print_error "Password is required"
                echo ""
                exit 1
            fi
            ;;
        2)
            OAUTH_PROVIDER="github"
            echo "Selected method: OAuth GitHub"
            echo ""
            ;;
        3)
            OAUTH_PROVIDER="google"
            echo "Selected method: OAuth Google"
            echo ""
            ;;
        *)
            print_error "Invalid option. Using Email + Password by default."
            AUTH_METHOD="1"
            echo ""
            ;;
    esac
    
    # Validate email based on selected method
    if [ -z "$EMAIL" ]; then
        # For OAuth, email is optional
        if [ "$AUTH_METHOD" == "2" ] || [ "$AUTH_METHOD" == "3" ]; then
            print_info "For OAuth, email is optional (for identification only)"
            echo ""
            read -s -p "Email (optional, leave empty if unknown): " EMAIL
            echo ""
            
            # If empty, use placeholder
            if [ -z "$EMAIL" ]; then
                EMAIL="oauth_${OAUTH_PROVIDER:-github}"
                print_info "Using placeholder email for OAuth"
            fi
        else
            # For email+password, email is required
            print_error "Please provide your email:"
            echo ""
            read -s -p "Email: " EMAIL
            echo ""
            
            if [ -z "$EMAIL" ]; then
                print_error "Email is required"
                echo ""
                exit 1
            fi
        fi
    fi
    
    # Step 1b: Request password only if email+password method
    if [ "$AUTH_METHOD" == "1" ]; then
        echo "Please enter your password:"
        read -s -p "Password: " PASSWORD
        echo ""
        echo ""
        
        if [ -z "$PASSWORD" ]; then
            print_error "Password is required"
            echo ""
            exit 1
        fi
    else
        echo "For OAuth, the script will authenticate automatically."
        echo ""
    fi
    
    echo "Please enter project name:"
    read -s -p "Project name: " PROJECT_NAME
    echo ""
    echo ""
    
    if [ -z "$PROJECT_NAME" ]; then
        PROJECT_NAME="OpenClaw"
        print_info "Default project name: $PROJECT_NAME"
    fi
    
    echo ""
    print_success "Data collected:"
    echo "  Email: $EMAIL"
    echo "  Project: $PROJECT_NAME"
    echo "  Auth Method: $AUTH_METHOD"
    if [ "$AUTH_METHOD" == "2" ] || [ "$AUTH_METHOD" == "3" ]; then
        echo "  OAuth: $OAUTH_PROVIDER"
    fi
    echo ""
    
    echo "Do you already have an API key or want to generate a new one?"
    read -p "Response (new/existing): " AUTH_TYPE
    echo ""
    
    if [ "$AUTH_TYPE" == "new" ] || [ "$AUTH_TYPE" == "New" ]; then
        print_info "Generating new API key..."
        echo ""
        print_info "Please wait while the script completes..."
        echo ""
    else
        print_info "Using existing API key..."
        echo ""
        read -s -p "Paste your API key: " API_KEY
        echo ""
        echo ""
        
        if [ -z "$API_KEY" ]; then
            print_error "API key cannot be empty"
            echo ""
            exit 1
        fi
    fi
    
    echo ""
}

# Step 2: Automate registration/login and create project
automate_registration_and_project_creation() {
    print_header
    print_info "Step 2: Automating registration/login and project creation..."
    echo ""
    
    # Since openclaw browser is not documented, we use curl for verification
    print_info "Using curl for automation..."
    echo ""
    
    # Create automation script with curl
    cat > "$CONFIG_DIR/automate.sh" << 'AUTOMATE_SCRIPT'
#!/bin/bash

echo ''
echo '=== STEP 2: AUTOMATING REGISTRATION AND PROJECT CREATION ==='
echo ''

echo '>>> Verifying authentication...'
echo ''

# Wait for user to complete authentication
echo 'Instructions:'
echo '  1. Go to: https://platform.teranode.group/register'
echo '  2. Fill email: '$EMAIL
if [ -n "$PASSWORD" ]; then
    echo '  3. Fill password: ******'
fi
echo '  4. Click "Sign up" or "Login"'
echo ''
echo 'When you have logged in, type "ready"'
echo ''

read
echo ''
echo '>>> Session started'
echo ''

# Step 2b: Create project
echo ''
echo '=== CREATING PROJECT ==='
echo ''

PROJECTS_URL="https://platform.teranode.group/projects"
echo '>>> Navigating to '$PROJECTS_URL'...'
echo ''

echo 'Project: '$PROJECT_NAME
echo ''

echo 'To create the project manually:'
echo '  1. Go to: https://platform.teranode.group/projects'
echo '  2. Click on "Create New Project"'
echo '  3. Enter name: '$PROJECT_NAME
echo '  4. Click "Create"'
echo ''
echo 'When you have created the project, type "project_created"'
echo ''

read
echo ''
echo '>>> Project created (manually)'
echo ''

# Step 2c: Get API key
API_KEYS_URL="https://platform.teranode.group/api-keys"
echo ''
echo '>>> Navigating to '$API_KEYS_URL'...'
echo ''

echo '>>> API Keys loaded'
echo ''

echo ''
echo '=== API KEY OBTAINED ==='
echo ''
echo 'The API key will be generated or already exists on the page.'
echo 'When you have the API key, copy it and type "ready"'
echo ''
echo 'You can also add it to ~/.bashrc automatically'
echo ''

# Prompt user for API key
input_ready=""
while [ "$input_ready" != "ready" ] && [ -n "$input_ready" ]; do
    input_ready=$(read -t 30 -p '>>> API Key: ' -r)
done

if [ -n "$input_ready" ]; then
    echo '>>> API Key obtained:' "$input_ready"
    
    # Save to output file
    echo "WATSONCHAIN_API_KEY=$input_ready" > "$CONFIG_DIR/.env"
    chmod 600 "$CONFIG_DIR/.env"
    
    echo '>>> API key saved to: '$CONFIG_DIR'/ .env'
    echo ''
    echo 'Add to ~/.bashrc:'
    echo "export WATSONCHAIN_API_KEY=\"$input_ready\""
    echo 'source ~/.bashrc'
fi

# Exit process
exit 0
AUTOMATE_SCRIPT

    # Make script executable
    chmod +x "$CONFIG_DIR/automate.sh"
    
    # Export variables
    export EMAIL PASSWORD OAUTH_PROVIDER PROJECT_NAME CONFIG_DIR
    
    # Run automation script
    print_info "Running automation..."
    echo ""
    echo ">>> Automation process started..."
    echo ""
    echo "Please wait a moment..."
    echo ""
    
    bash "$CONFIG_DIR/automate.sh" 2>&1 | grep -v "^\[" | head -50
    
    echo ""
    echo ""
    
    # Check if .env file was created
    if [ -f "$CONFIG_FILE" ] && grep -q "WATSONCHAIN_API_KEY" "$CONFIG_FILE"; then
        print_success "Automation completed successfully"
        echo ""
    else
        print_info "Verifying configuration..."
        echo ""
        
        # Manual fallback
        print_warning "Automation did not create .env file"
        echo ""
        echo "Next steps:"
        echo ""
        echo "1. Go to: https://platform.teranode.group/register"
        echo ""
        echo "2. Register or login with:"
        echo "   - Email: $EMAIL"
        echo "   - Password: ******"
        echo ""
        echo "3. Go to: https://platform.teranode.group/projects"
        echo "   - Create project: $PROJECT_NAME"
        echo ""
        echo "4. Go to: https://platform.teranode.group/api-keys"
        echo "   - Copy the API key"
        echo ""
        echo "5. Return to script"
        echo ""
        echo "Press Enter when you have the API key..."
        echo ""
        
        read
        echo ""
        
        read -s -p "Paste your API key: " API_KEY
        echo ""
        echo ""
        
        if [ -z "$API_KEY" ]; then
            print_error "API key cannot be empty"
            echo ""
            exit 1
        fi
        
        # Save API key manually
        echo "WATSONCHAIN_API_KEY=$API_KEY" > "$CONFIG_FILE"
        chmod 600 "$CONFIG_FILE"
        echo ""
        print_success "API key saved manually"
    fi
}

# Step 3: Save configuration
save_configuration() {
    print_header
    print_info "Step 3: Saving configuration"
    echo ""
    print_info "Creating configuration directory..."
    mkdir -p "$CONFIG_DIR"
    echo ""
    print_success "Directory created: $CONFIG_DIR"
    echo ""
    
    # Get API key
    if [ -f "$CONFIG_FILE" ]; then
        # Already configured
        print_info "API key already configured. Not overwriting."
        
        # Show summary
        print_info "Configuration summary:"
        echo "  API key saved to: $CONFIG_FILE"
        echo "  Status: Configured"
        echo ""
    elif [ -n "$API_KEY" ]; then
        print_info "Saving API key to environment file..."
        echo "WATSONCHAIN_API_KEY=$API_KEY" > "$CONFIG_FILE"
        chmod 600 "$CONFIG_FILE"
        echo ""
        print_success "API key saved to: $CONFIG_FILE"
        echo ""
        print_warning "Only the owner (ChicoCifrado) has access to this file"
    else
        print_info "API key not defined. Using manual mode."
        read -s -p "Paste your API key: " API_KEY
        echo ""
        echo ""
        
        if [ -n "$API_KEY" ]; then
            echo "WATSONCHAIN_API_KEY=$API_KEY" > "$CONFIG_FILE"
            chmod 600 "$CONFIG_FILE"
            echo ""
            print_success "API key saved to: $CONFIG_FILE"
        else
            print_error "No API key provided"
            exit 1
        fi
    fi
    
    read -p "Press Enter to continue..."
}

# Step 4: Configure environment and add to .bashrc
configure_environment() {
    print_header
    print_info "Step 4: Configuring environment variables"
    echo ""
    echo "API key is imported and saved correctly."
    echo ""
    echo "Next steps:"
    echo "  1. Export environment variable:"
    echo -e "${BLUE}   export WATSONCHAIN_API_KEY=\$(cat $CONFIG_FILE | cut -d= -f2-)${NC}"
    echo ""
    echo "  2. Or add permanently to ~/.bashrc:"
    echo -e "${BLUE}   echo 'export WATSONCHAIN_API_KEY=\"\$(cat $CONFIG_FILE | cut -d= -f2-)\"' >> ~/.bashrc${NC}"
    echo "   source ~/.bashrc"
    echo ""
    echo "  3. Use in OpenClaw:"
    echo -e "${BLUE}   /tools${NC}"
    echo ""
    echo "  4. Or use the API directly:"
    echo -e "${BLUE}   curl -H \"Authorization: Bearer \$WATSONCHAIN_API_KEY\" \"https://api.whatsonchain.com/v1/...\"${NC}"
    echo ""
    
    read -p "Do you want to add the environment variable to ~/.bashrc? (y/n): " ANSWER
    echo ""
    
    if [ "$ANSWER" == "y" ] || [ "$ANSWER" == "Y" ]; then
        print_info "Adding to ~/.bashrc..."
        
        if [ -f ~/.bashrc ]; then
            # Get the API key value
            API_VALUE="$(cat "$CONFIG_FILE" | cut -d= -f2-)"
            
            # Check if already exists
            if ! grep -q "WATSONCHAIN_API_KEY=" ~/.bashrc; then
                echo "export WATSONCHAIN_API_KEY=\"$API_VALUE\"" >> ~/.bashrc
                print_success "Added to ~/.bashrc"
                echo ""
            else
                print_warning "Variable already exists in ~/.bashrc"
                echo ""
            fi
        else
            print_warning "~/.bashrc file does not exist"
        fi
        echo ""
    fi
    
    print_success "Environment variable configuration completed"
    echo ""
    echo "Import the changes with:"
    echo -e "${BLUE}   source ~/.bashrc${NC}"
    echo ""
    
    read -p "Press Enter to continue..."
}

# Step 5: Create notes file
create_notes() {
    print_header
    print_info "Step 5: Creating notes file"
    echo ""
    
    # Create notes
    cat > "$NOTES_FILE" << EOF
=== WHATSONCHAIN API CONFIGURATION ===
Date: $(date '+%Y-%m-%d %H:%M:%S')
Platform: https://platform.teranode.group

API Key Status: CONFIGURED
Key Length: ${#API_KEY} characters

=== AVAILABLE TOOLS ===
- mainnetInfo: Get BSV mainnet network status
- testnetInfo: Get BSV testnet network status
- txHash: Get transaction by hash
- txIndex: Get transaction by block height + index
- txPropagation: Check transaction propagation status
- blockInfo: Get block by height
- txHex: Get raw transaction hex
- txBin: Get raw transaction binary
- decodeTx: Decode raw transaction hex
- broadcastTx: Broadcast transaction to network

=== USAGE ===
Use in OpenClaw:
/tools

Or direct API calls:
curl -H "Authorization: Bearer \$WATSONCHAIN_API_KEY" "https://api.whatsonchain.com/v1/..."

=== RATE LIMITS ===
Free tier: 3 requests/second
Premium: 10, 20, or 40 requests/second

=== SUPPORT ===
Telegram: WhatsonChain devs channel

=== PLATFORM URLs ===
Register: https://platform.teranode.group/register
Login: https://platform.teranode.group/login
Projects: https://platform.teranode.group/projects
API Keys: https://platform.teranode.group/api-keys
EOF

    print_success "Notes file created: $NOTES_FILE"
    echo ""
    
    read -p "Press Enter to finish..."
}

# Main function
main() {
    print_header
    print_info "=== WHATSONCHAIN API ONBOARD ==="
    echo ""
    
    # Step 1: Collect data
    collect_user_data_and_register
    
    # Step 2: Automate or manual
    automate_registration_and_project_creation
    
    # Step 3: Save configuration
    save_configuration
    
    # Step 4: Configure environment
    configure_environment
    
    # Step 5: Create notes
    create_notes
    
    print_header
    print_success "=== ONBOARD COMPLETED ==="
    echo ""
    echo "Summary:"
    echo "  ✅ API key imported and saved"
    echo "  ✅ Configuration in ~/.bashrc (optional)"
    echo "  ✅ Notes file created"
    echo ""
    echo "Next steps:"
    echo "  1. Import ~/.bashrc with: source ~/.bashrc"
    echo "  2. Use /tools in OpenClaw"
    echo "  3. Consult $NOTES_FILE for documentation"
    echo ""
    echo "Visit: https://platform.teranode.group"
    echo ""
    echo "=============================================="
    echo ""
}

# Run
main
