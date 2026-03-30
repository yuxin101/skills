#!/usr/bin/env bash

# OAuth Device Code Flow Script
# Soporta GitHub y Google

set -e

# ==========================================================================
# CONFIGURACIÓN
# ==========================================================================

# Reemplaza con tus credenciales

# GitHub OAuth
GITHUB_CLIENT_ID="TU_GITHUB_CLIENT_ID"

# Google OAuth
GOOGLE_CLIENT_ID="TU_GOOGLE_CLIENT_ID.apps.googleusercontent.com"

# ==========================================================================
# FUNCIONES
# ==========================================================================

print_header() {
    echo ""
    echo "========================================"
    echo "  OAUTH DEVICE CODE FLOW"
    echo "========================================"
    echo ""
}

print_success() {
    echo -e "\033[0;32m✅ $1\033[0m"
}

print_info() {
    echo -e "\033[0;34m>>> $1\033[0m"
}

print_error() {
    echo -e "\033[0;31m❌ $1\033[0m"
}

print_warning() {
    echo -e "\033[1;33m⚠️  $1\033[0m"
}

# ==========================================================================
# SELECCIONAR PROVEEDOR
# ==========================================================================

select_provider() {
    print_info "Selecciona un proveedor OAuth:"
    echo ""
    echo "  1. GitHub"
    echo "  2. Google"
    echo ""
    
    read -p "Selecciona una opción (1-2): " PROVIDER_CHOICE
    echo ""
    
    case "$PROVIDER_CHOICE" in
        1)
            OAUTH_PROVIDER="github"
            ;;
        2)
            OAUTH_PROVIDER="google"
            ;;
        *)
            print_error "Opción inválida. Usando GitHub por defecto."
            OAUTH_PROVIDER="github"
            ;;
    esac
    
    echo ""
    echo "Proveedor seleccionado: $OAUTH_PROVIDER"
    echo ""
}

# ==========================================================================
# PASO 1: SOLICITAR DEVICE CODE
# ==========================================================================

request_device_code() {
    print_info "Solicitando device code para $OAUTH_PROVIDER..."
    echo ""
    
    if [ "$OAUTH_PROVIDER" == "github" ]; then
        response=$(curl -s "https://github.com/login/device/code" \
             -d "client_id=$GITHUB_CLIENT_ID" \
             -d "scope=repo" 2>/dev/null)
        
        if [ -z "$response" ]; then
            print_error "No se recibió respuesta."
            echo ""
            exit 1
        fi
        
        device_code=$(echo "$response" | jq -r '.device_code')
        user_code=$(echo "$response" | jq -r '.user_code')
        verification_uri=$(echo "$response" | jq -r '.verification_uri')
        
    elif [ "$OAUTH_PROVIDER" == "google" ]; then
        response=$(curl -s "https://oauth2.googleapis.com/device/code" \
             -d "client_id=$GOOGLE_CLIENT_ID" \
             -d "scope=https://www.googleapis.com/auth/userinfo.profile")
        
        if [ -z "$response" ]; then
            print_error "No se recibió respuesta."
            echo ""
            exit 1
        fi
        
        device_code=$(echo "$response" | jq -r '.device_code')
        user_code=$(echo "$response" | jq -r '.user_code')
        verification_url=$(echo "$response" | jq -r '.verification_url')
        
    fi
    
    if [ -z "$device_code" ] || [ -z "$user_code" ]; then
        print_error "La respuesta no contiene los campos esperados."
        echo "Respuesta completa:"
        echo "$response"
        echo ""
        exit 1
    fi
    
    print_success "Device code solicitado con éxito"
    echo ""
    
    # Mostrar instrucciones según proveedor
    case "$OAUTH_PROVIDER" in
        github)
            echo "👉 Abre: $verification_uri"
            echo "👉 Código: $user_code"
            ;;
        google)
            echo "👉 Ve a: $verification_url"
            echo "👉 Introduce el código: $user_code"
            ;;
    esac
    
    echo ""
    echo "Presiona ENTER cuando hayas iniciado sesión..."
    
    read
    
    echo ""
    echo ">>> Sesión iniciada"
    echo ""
}

# ==========================================================================
# PASO 2: POLLING PARA OBTENER TOKEN
# ==========================================================================

poll_for_token() {
    print_info "Comenzando polling para obtener token..."
    echo ""
    echo "Esperando confirmación de autenticación..."
    echo ""
    
    max_attempts=30
    attempt=0
    last_error=""
    
    while [ $attempt -lt $max_attempts ]; do
        attempt=$((attempt + 1))
        
        if [ "$OAUTH_PROVIDER" == "github" ]; then
            token_response=$(curl -s "https://github.com/login/oauth/access_token" \
                -H "Accept: application/json" \
                -d "client_id=$GITHUB_CLIENT_ID" \
                -d "device_code=$device_code" \
                -d "grant_type=urn:ietf:params:oauth:grant-type:device_code")
        elif [ "$OAUTH_PROVIDER" == "google" ]; then
            token_response=$(curl -s "https://oauth2.googleapis.com/token" \
                -d "client_id=$GOOGLE_CLIENT_ID" \
                -d "device_code=$device_code" \
                -d "grant_type=urn:ietf:params:oauth:grant-type:device_code")
        fi
        
        access_token=$(echo "$token_response" | jq -r '.access_token')
        error_description=$(echo "$token_response" | jq -r '.error_description' 2>/dev/null || echo "")
        
        # Verificar token
        if [ -n "$access_token" ] && [ "$access_token" != "null" ]; then
            print_success "Token obtenido con éxito!"
            echo ""
            
            # Mostrar token
            echo "Token: $access_token"
            echo ""
            
            # Guardar token en archivo
            TOKEN_FILE="$HOME/.clawhub/oauth-token.txt"
            echo "WATSONCHAIN_ACCESS_TOKEN=$access_token" > "$TOKEN_FILE"
            chmod 600 "$TOKEN_FILE"
            
            print_success "Token guardado en: $TOKEN_FILE"
            echo ""
            
            return 0
        fi
        
        # Verificar errores
        if [[ "$error_description" == *"access_denied"* ]] || [[ "$error_description" == *"authorization_denied"* ]]; then
            print_error "Autenticación denegada: $error_description"
            echo ""
            echo "Por favor, verifica que has iniciado sesión"
            echo "y presiona ENTER para continuar..."
            echo ""
            read
            echo ""
            continue
        fi
        
        # Verificar si el dispositivo ya completó el flujo
        if [[ "$error_description" == *"authorization_pending"* ]] || [[ "$error_description" == *"authorization_started"* ]]; then
            print_info "Pendiente de autorización..."
            echo ""
            echo "Por favor, completa el inicio de sesión en el navegador"
            echo ""
            read
            echo ""
            continue
        fi
        
        # Esperar 5 segundos
        sleep 5
    done
    
    # Si llegamos aquí, no obtuvimos token
    print_error "No se pudo obtener el token después de $max_attempts intentos"
    echo ""
    echo "Error final: $error_description"
    echo ""
    
    return 1
}

# ==========================================================================
# PASO 3: OBTENER API KEY
# ==========================================================================

get_api_key() {
    print_info "Obteniendo API key..."
    echo ""
    
    TOKEN_FILE="$HOME/.clawhub/oauth-token.txt"
    
    if [ ! -f "$TOKEN_FILE" ]; then
        print_error "Token no encontrado. Terminando..."
        echo ""
        exit 1
    fi
    
    ACCESS_TOKEN=$(cat "$TOKEN_FILE" | cut -d= -f2-)
    
    if [ -z "$ACCESS_TOKEN" ]; then
        print_error "Token vacío. Terminando..."
        echo ""
        exit 1
    fi
    
    # Solicitar API key al usuario
    echo "Instrucciones:"
    echo "  1. Ve a: https://platform.teranode.group/api-keys"
    echo "  2. Copia la API key"
    echo ""
    echo "Cuando tengas la API key, presiona ENTER y pégalos cuando te lo pida..."
    echo ""
    
    read
    
    read -s -p "API Key: " API_KEY
    echo ""
    echo ""
    
    if [ -z "$API_KEY" ]; then
        print_error "API key no puede estar vacía"
        echo ""
        exit 1
    fi
    
    # Guardar API key
    CONFIG_DIR="$HOME/.clawhub"
    CONFIG_FILE="$CONFIG_DIR/.env"
    
    echo "WATSONCHAIN_API_KEY=$API_KEY" > "$CONFIG_FILE"
    chmod 600 "$CONFIG_FILE"
    
    print_success "API key guardada en: $CONFIG_FILE"
    echo ""
    echo "API Key: ${API_KEY:0:20}..."
    echo ""
    
    # Verificar si es Starter
    if [[ "$API_KEY" == *"starter"* ]] || [[ "$API_KEY" == *"STARTER"* ]]; then
        print_warning "Atención: Esta parece ser la API key Starter"
        echo ""
        echo "Para obtener una nueva API key personal, debes ir a:"
        echo "https://platform.teranode.group/api-keys"
        echo ""
    fi
    
    return 0
}

# ==========================================================================
# PASO 4: VERIFICAR ACCESO A LA API
# ==========================================================================

verify_api_access() {
    print_info "Verificando acceso a la API BSV..."
    echo ""
    
    API_KEY=$(cat "$HOME/.clawhub/.env" | cut -d= -f2-)
    
    if [ -z "$API_KEY" ]; then
        print_error "API key no encontrada"
        echo ""
        return 1
    fi
    
    # Probar acceso a API
    response=$(curl -s -H "Authorization: Bearer $API_KEY" \
        "https://api.whatsonchain.com/v1/mainnetInfo")
    
    if [ $? -eq 0 ]; then
        print_success "Acceso a la API verificado"
        echo ""
        echo "Respuesta de la API:"
        echo "$response"
        echo ""
    else
        print_error "No se pudo acceder a la API"
        echo "Respuesta:"
        echo "$response"
        echo ""
        return 1
    fi
    
    return 0
}

# ==========================================================================
# PASO 5: USAR LA API
# ==========================================================================

use_api() {
    print_info "Uso de la API..."
    echo ""
    
    API_KEY=$(cat "$HOME/.clawhub/.env" | cut -d= -f2-)
    
    if [ -z "$API_KEY" ]; then
        print_error "API key no encontrada"
        echo ""
        return 1
    fi
    
    # Solicitar endpoint
    echo "Escribe el endpoint de la API o presiona ENTER para mainnetInfo:"
    read -r endpoint
    
    if [ -z "$endpoint" ]; then
        endpoint="https://api.whatsonchain.com/v1/mainnetInfo"
    fi
    
    echo ""
    echo "Obteniendo información..."
    echo ""
    
    response=$(curl -s -H "Authorization: Bearer $API_KEY" "$endpoint")
    
    if [ $? -eq 0 ]; then
        print_success "API llamada exitosa"
        echo ""
        echo "Respuesta:"
        echo "$response"
        echo ""
    else
        print_error "API llamada fallida"
        echo "Respuesta:"
        echo "$response"
        echo ""
    fi
    
    return $?
}

# ==========================================================================
# SCRIPT COMPLETO
# ==========================================================================

main() {
    print_header
    
    # Paso 1: Seleccionar proveedor
    select_provider
    
    # Paso 2: Solicitar device code
    request_device_code
    
    # Paso 3: Polling para obtener token
    poll_for_token
    
    # Paso 4: Obtener API key
    get_api_key
    
    # Paso 5: Verificar acceso
    verify_api_access
    
    # Paso 6: Usar API (opcional)
    use_api
    
    print_header
    print_success "COMPLETADO"
    echo ""
    echo "Resumen:"
    echo "  ✅ Device code solicitado"
    echo "  ✅ Token obtenido"
    echo "  ✅ API key obtenida"
    echo "  ✅ Acceso verificado"
    echo ""
    echo "Token guardado en: $HOME/.clawhub/oauth-token.txt"
    echo "API key guardada en: $HOME/.clawhub/.env"
    echo ""
    echo "Para usar la API:"
    echo "  export WATSONCHAIN_API_KEY=\$(cat ~/.clawhub/.env | cut -d= -f2-)"
    echo ""
    echo "========================================"
    echo ""
}

# Ejecutar
main
