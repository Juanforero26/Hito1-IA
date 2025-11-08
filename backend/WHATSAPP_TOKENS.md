# 🔐 Tokens de WhatsApp - Explicación

## ❓ ¿Son lo mismo los dos tokens?

**NO**, son completamente diferentes y tienen propósitos distintos:

## 1. WHATSAPP_VERIFY_TOKEN (Token de Verificación)

### ¿Qué es?
- **Token personalizado** que **TÚ CREAS** para verificar el webhook
- Es una **contraseña secreta** que solo tú conoces
- Se usa **solo una vez** durante la configuración inicial del webhook

### ¿Dónde se obtiene?
- **TÚ LO CREAS** - puede ser cualquier string que elijas
- Ejemplos: `"mi_token_secreto_123"`, `"panaderia_2024"`, `"webhook_verify_token"`
- No viene de Meta/WhatsApp, lo inventas tú

### ¿Para qué se usa?
- **Verificación inicial del webhook** cuando WhatsApp intenta conectarse a tu servidor
- WhatsApp envía una petición GET con este token para verificar que eres el dueño del webhook
- Si el token coincide, WhatsApp confía en tu servidor y empieza a enviar mensajes

### ¿Dónde se configura?
1. **En tu archivo `.env`**: 
   ```env
   WHATSAPP_VERIFY_TOKEN=mi_token_secreto_123
   ```

2. **En Meta for Developers** (cuando configuras el webhook):
   - En el campo "Token de verificación" pegas el mismo valor
   - Ejemplo: `mi_token_secreto_123`

### Ejemplo en el código:
```javascript
// Línea 11 en webhookController.js
const verifyToken = process.env.WHATSAPP_VERIFY_TOKEN;

// Línea 13 - Compara el token que envía WhatsApp con el tuyo
if (mode === 'subscribe' && token === verifyToken) {
  // ✅ Webhook verificado
}
```

---

## 2. WHATSAPP_ACCESS_TOKEN (Token de Acceso)

### ¿Qué es?
- **Token de autenticación** que te da **Meta/WhatsApp**
- Es una **credencial oficial** para usar la API de WhatsApp Business
- Se usa **cada vez** que quieres enviar mensajes o hacer llamadas a la API

### ¿Dónde se obtiene?
- **DE META FOR DEVELOPERS** - no lo creas tú, lo genera Meta
- Debes ir a: https://developers.facebook.com/
- En tu aplicación → Configuración → Tokens de acceso
- Generas un token temporal (24 horas) o permanente (producción)

### ¿Para qué se usa?
- **Autenticación** en las peticiones a la API de WhatsApp
- Enviar mensajes de confirmación a los clientes
- Hacer cualquier operación con la API de WhatsApp Business

### ¿Dónde se configura?
1. **En tu archivo `.env`**:
   ```env
   WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxx
   ```
   (Este token es mucho más largo, tipo: `EAAa1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

2. **NO se configura en Meta** - solo lo obtienes de ahí y lo guardas en tu `.env`

### Ejemplo en el código:
```javascript
// Línea 118 en webhookController.js
const accessToken = process.env.WHATSAPP_ACCESS_TOKEN;

// Línea 133 - Se usa en el header de autorización
headers: {
  'Authorization': `Bearer ${accessToken}`,
  'Content-Type': 'application/json'
}
```

---

## 📊 Tabla Comparativa

| Característica | WHATSAPP_VERIFY_TOKEN | WHATSAPP_ACCESS_TOKEN |
|----------------|----------------------|----------------------|
| **¿Quién lo crea?** | TÚ | Meta/WhatsApp |
| **¿Dónde se obtiene?** | Lo inventas | Meta for Developers |
| **Formato** | String simple (ej: "mi_token_123") | String largo (ej: "EAAa1b2c3...") |
| **Uso** | Solo una vez (verificación) | Cada vez (API calls) |
| **Cuándo se usa** | Al configurar el webhook | Al enviar mensajes |
| **Expira** | Nunca (es permanente) | Sí (24h temporal, o permanente) |
| **Secreto** | Sí (solo tú lo conoces) | Sí (muy importante) |

---

## 🔄 Flujo de Uso

### 1. Configuración Inicial (VERIFY_TOKEN)
```
1. Tú creas: WHATSAPP_VERIFY_TOKEN="mi_secreto_123"
2. Lo pones en tu .env
3. Lo pones en Meta for Developers (configuración del webhook)
4. WhatsApp envía GET /webhook/whatsapp?hub.verify_token=mi_secreto_123
5. Tu servidor compara: ¿coinciden? ✅
6. WhatsApp confía en tu servidor
```

### 2. Envío de Mensajes (ACCESS_TOKEN)
```
1. Obtienes ACCESS_TOKEN de Meta for Developers
2. Lo pones en tu .env
3. Cliente envía mensaje → WhatsApp → Tu servidor
4. Tu servidor procesa el mensaje
5. Tu servidor envía confirmación usando ACCESS_TOKEN
6. WhatsApp API verifica el token → ✅ Mensaje enviado
```

---

## ⚠️ Importante

### Seguridad de VERIFY_TOKEN
- Puede ser cualquier string que elijas
- Debe ser difícil de adivinar (no uses "123" o "test")
- Úsalo solo durante la configuración del webhook
- Una vez configurado, WhatsApp no lo vuelve a pedir (solo si reconfiguras)

### Seguridad de ACCESS_TOKEN
- **MUY SENSIBLE** - nunca lo compartas
- Si alguien lo obtiene, puede enviar mensajes en tu nombre
- Los tokens temporales expiran en 24 horas
- Para producción, configura tokens permanentes con permisos limitados
- **NUNCA** lo subas a Git (ya está en .gitignore)

---

## 📝 Ejemplo de Configuración

### Archivo `.env`:
```env
# Token que TÚ CREAS (puede ser cualquier string)
WHATSAPP_VERIFY_TOKEN=panaderia_secreto_2024_xyz

# Token que OBTIENES de Meta for Developers
WHATSAPP_ACCESS_TOKEN=EAAa1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0

# ID del número de teléfono (también de Meta)
WHATSAPP_PHONE_NUMBER_ID=123456789012345
```

### En Meta for Developers:
```
Configuración del Webhook:
- URL: https://tu-dominio.com/webhook/whatsapp
- Token de verificación: panaderia_secreto_2024_xyz  ← El mismo que en .env
```

---

## 🆘 Problemas Comunes

### Error: "Webhook verification failed"
- **Causa**: El `WHATSAPP_VERIFY_TOKEN` en tu `.env` NO coincide con el que pusiste en Meta
- **Solución**: Asegúrate de que sean exactamente iguales (mayúsculas, minúsculas, espacios)

### Error: "Access token invalid"
- **Causa**: El `WHATSAPP_ACCESS_TOKEN` es inválido o expiró
- **Solución**: Ve a Meta for Developers y genera un nuevo token

### Error: "Unauthorized"
- **Causa**: El `WHATSAPP_ACCESS_TOKEN` no tiene permisos o es incorrecto
- **Solución**: Verifica que el token tenga permisos de `whatsapp_business_messaging`

---

## ✅ Resumen

- **VERIFY_TOKEN**: Lo creas tú, string simple, solo para verificación inicial
- **ACCESS_TOKEN**: Lo obtienes de Meta, string largo, para todas las operaciones de API
- **Son diferentes** y ambos son necesarios
- **Ambos deben ser secretos** y no compartirse

