# Whatsonchain API Playbooks

**Fuente:** https://docs.whatsonchain.com  
**Fecha:** 2026-03-26

## ⚠️ Nota Importante

No fue posible acceder completamente a la documentación de la API debido a limitaciones de acceso (404, 403). Esta lista contiene la información disponible de la página principal.

---

## 📋 Endpoints Principales (Disponible)

### 1. BSV Mainnet Network Info

```bash
curl -H 'Authorization: mainnet_xx...' \
  "https://api.whatsonchain.com/v1/bsv/main/chain/info"
```

**Descripción:** Información del nodo principal de BSV.

---

### 2. Authentication & Rate Limits

**No se requiere autenticación para rate limit free:**
- Up to 3 requests/sec is free
- Para más: https://platform.teranode.group/pricing?plan=woc

**API Key Authentication:**
```bash
curl -H 'Authorization: mainnet_xx...' \
  "https://api.whatsonchain.com/v1/bsv/main/chain/info"
```

**Rate Limits:**
- Free: 3 requests/sec
- Premium: 10, 20, or 40 requests/sec
- Enterprise: Custom

---

### 3. Networks Available

- **Mainnet** - BSV Mainnet
- **Testnet** - BSV Testnet (BSV-only)

**Nota:** BTC networks no están disponibles (solo BSV).

---

## 🌐 Platform URLs (No son API Endpoints)

Estas URLs se usan durante el setup, no son endpoints de la API:

1. **Registro del usuario:** `https://platform.teranode.group/register`
   - Para obtener la API key para Whatsonchain

2. **Comprobación de cuenta:** `https://platform.teranode.group/login`
   - Comprobación de cuenta del usuario

3. **Gestión de proyectos:** `https://platform.teranode.group/projects`
   - Opcional: Crear un proyecto

4. **Obtener API "Starter":** `https://platform.teranode.group/api-keys`
   - Requerido: Obtener la API "Starter"

---

## 📊 API Capabilities (Basado en Documentación Principal)

### Funcionalidades Confirmadas

✅ **Blockchain Explorer Services**
- Blocks
- Transactions
- Address activity
- On-chain data
- Stats
- Insights

✅ **Network Support**
- BSV Mainnet
- BSV Testnet (BSV-only)

✅ **Transaction Broadcasting**
- Broadcast transactions to BSV network

✅ **REST API**
- Simple REST API endpoints
- JSON responses

---

## 🔧 Authentication

**Free Tier:**
- No authentication required
- Up to 3 requests/sec

**Premium/Enterprise:**
```bash
curl -H 'Authorization: mainnet_xx...' \
  "https://api.whatsonchain.com/v1/..."
```

**API Key Format:**
- `mainnet_xx...` (mainnet)
- `testnet_xx...` (testnet)

---

## 📞 Support

**Telegram:** https://t.me/joinchat/FfE6-EjZhoTHwhDhZH6F-w

**Pricing:** https://platform.teranode.group/pricing?plan=woc

**Powered by Whatsonchain:** https://whatsonchain.com/assets#powered-by-whatsonchain

---

## 📝 Limitaciones Encontradas

No fue posible acceder a:
- API Reference (404)
- Networks documentation (404)
- Transactions documentation (404)
- Blocks documentation (403 - Just a moment)

**Se recomienda visitar:** https://docs.whatsonchain.com directamente para ver todos los endpoints disponibles.

---

## 🚀 Próximos Pasos

1. ✅ Registrar cuenta en Teranode Platform
2. ✅ Obtener API key (Starter o premium)
3. ✅ Visitar documentación completa
4. ✅ Recopilar todos los endpoints disponibles
5. ✅ Documentar cada playbook con HTTP Request y Example

---

**Author:** Whatsonchain API Team  
**License:** MIT
