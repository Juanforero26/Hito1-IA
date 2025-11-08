# 🔧 Guía: Cómo Configurar el Webhook en Meta for Developers

## 📋 Pasos para Completar la Configuración del Webhook

### Paso 1: Preparar tu Servidor Backend

1. **Asegúrate de que tu archivo `.env` está configurado:**

```bash
cd backend
# Si no tienes el archivo .env, créalo copiando el ejemplo
cp .env.example .env
```

2. **Edita el archivo `.env` y configura el VERIFY_TOKEN:**
```env
WHATSAPP_VERIFY_TOKEN=mi_token_secreto_de_verificacion
```

> ⚠️ **Importante**: Elige un token seguro y guárdalo. Lo necesitarás para el paso 4.

3. **Inicia tu servidor backend:**
```bash
npm start
# o para desarrollo con auto-recarga:
npm run dev
```

Deberías ver un mensaje como:
```
🚀 Servidor corriendo en el puerto 3000
📱 Webhook de WhatsApp: http://localhost:3000/webhook/whatsapp
```

---

### Paso 2: Exponer tu Servidor Local con ngrok

Para desarrollo local, necesitas exponer tu servidor a internet usando ngrok.

1. **Instala ngrok** (si no lo tienes):
```bash
# Opción 1: Con npm
npm install -g ngrok

# Opción 2: Con Homebrew (macOS)
brew install ngrok

# Opción 3: Descarga desde https://ngrok.com/download
```

2. **Inicia ngrok en una nueva terminal:**
```bash
ngrok http 3000
```

3. **Copia la URL HTTPS que ngrok te proporciona:**
```
Forwarding: https://abc123def456.ngrok-free.app -> http://localhost:3000
```

> 📝 **Nota**: La URL será algo como `https://abc123def456.ngrok-free.app`

---

### Paso 3: Completar el Campo "Callback URL"

En la interfaz de Meta for Developers:

1. **En el campo "Callback URL"**, pega la URL de ngrok y añade `/webhook/whatsapp`:

```
https://abc123def456.ngrok-free.app/webhook/whatsapp
```

> ⚠️ **Importante**: 
> - Usa la URL **HTTPS** (no HTTP)
> - Añade `/webhook/whatsapp` al final
> - Asegúrate de que tu servidor esté corriendo antes de verificar

**Ejemplo completo:**
- Si ngrok te da: `https://abc123def456.ngrok-free.app`
- Tu Callback URL será: `https://abc123def456.ngrok-free.app/webhook/whatsapp`

---

### Paso 4: Completar el Campo "Verify token"

En el campo "Verify token":

1. **Pega el valor exacto** que configuraste en tu archivo `.env`:

```
mi_token_secreto_de_verificacion
```

> ⚠️ **MUY IMPORTANTE**: 
> - El valor debe ser **exactamente igual** al que pusiste en tu `.env`
> - Respeta mayúsculas, minúsculas, espacios y caracteres especiales
> - Si no coinciden, la verificación fallará

**Para verificar qué token tienes configurado:**
```bash
# En el directorio backend
cat .env | grep WHATSAPP_VERIFY_TOKEN
```

---

### Paso 5: Configurar el Certificado (Opcional)

- **"Attach a client certificate"**: Déjalo **desactivado** (toggle en gris/off)
- Esto solo es necesario para configuraciones avanzadas de seguridad
- Para esta implementación, no es necesario

---

### Paso 6: Verificar y Guardar

1. **Haz clic en el botón azul "Verify and save"**

2. **¿Qué sucede?**
   - Meta/WhatsApp enviará una petición GET a tu Callback URL
   - Tu servidor verificará que el token coincida
   - Si todo está correcto, verás un mensaje de éxito

3. **Verifica en la terminal de tu servidor:**
   ```
   ✅ Webhook verificado correctamente
   ```

4. **Si hay un error:**
   - Revisa que tu servidor esté corriendo
   - Verifica que ngrok esté activo
   - Confirma que el VERIFY_TOKEN coincida exactamente
   - Revisa los logs de tu servidor para más detalles

---

## 🔍 Verificación de que Todo Funciona

### 1. Verificar que el Webhook está Activo

Después de hacer clic en "Verify and save", deberías ver:
- ✅ Un mensaje de éxito en Meta for Developers
- ✅ El webhook marcado como "Activo" o "Verificado"
- ✅ En tu servidor: `✅ Webhook verificado correctamente`

### 2. Probar el Webhook

1. **Envía un mensaje de prueba** al número de WhatsApp Business configurado
2. **Verifica en la terminal de tu servidor** que recibas el mensaje:
   ```
   ✅ Pedido almacenado - ID: 1, Teléfono: 573001234567
   📝 Texto: Hola, necesito 50 panes...
   ✅ Mensaje de confirmación enviado a 573001234567
   ```

### 3. Verificar en la Base de Datos

```bash
# Ver los pedidos almacenados
sqlite3 data/orders.db "SELECT * FROM orders;"
```

---

## 🐛 Solución de Problemas

### Error: "Webhook verification failed"

**Causas posibles:**
1. ❌ El servidor no está corriendo
2. ❌ ngrok no está activo o la URL cambió
3. ❌ El VERIFY_TOKEN no coincide exactamente
4. ❌ La Callback URL está mal formada

**Solución:**
```bash
# 1. Verifica que el servidor esté corriendo
# Deberías ver: "🚀 Servidor corriendo en el puerto 3000"

# 2. Verifica que ngrok esté activo
# Deberías ver la URL HTTPS en la terminal de ngrok

# 3. Verifica el token en tu .env
cat .env | grep WHATSAPP_VERIFY_TOKEN

# 4. Asegúrate de que la Callback URL sea exactamente:
# https://TU_URL_NGROK.ngrok-free.app/webhook/whatsapp
```

### Error: "Cannot reach callback URL"

**Causas posibles:**
1. ❌ ngrok no está corriendo
2. ❌ El servidor backend no está activo
3. ❌ La URL de ngrok cambió (ngrok genera una nueva URL cada vez que se reinicia)

**Solución:**
```bash
# 1. Reinicia ngrok
ngrok http 3000

# 2. Copia la NUEVA URL
# 3. Actualiza la Callback URL en Meta for Developers
# 4. Haz clic en "Verify and save" nuevamente
```

### El webhook se verificó pero no recibo mensajes

**Causas posibles:**
1. ❌ No estás suscrito a los eventos correctos
2. ❌ El número de teléfono no está configurado correctamente
3. ❌ El ACCESS_TOKEN no está configurado

**Solución:**
1. En Meta for Developers, verifica que estés suscrito a los eventos:
   - ✅ `messages` (mensajes recibidos)
   - ✅ `message_status` (estado de mensajes, opcional)
2. Verifica que el `WHATSAPP_ACCESS_TOKEN` esté en tu `.env`
3. Verifica que el `WHATSAPP_PHONE_NUMBER_ID` esté configurado

---

## 📝 Resumen Rápido

1. ✅ Servidor corriendo en puerto 3000
2. ✅ ngrok activo: `ngrok http 3000`
3. ✅ Callback URL: `https://TU_URL_NGROK.ngrok-free.app/webhook/whatsapp`
4. ✅ Verify token: El mismo que en tu `.env` (ej: `mi_token_secreto_de_verificacion`)
5. ✅ Certificado: Desactivado
6. ✅ Clic en "Verify and save"
7. ✅ Verificar que aparezca: `✅ Webhook verificado correctamente`

---

## 🎯 Ejemplo Completo

```bash
# Terminal 1: Servidor
cd backend
npm run dev

# Terminal 2: ngrok
ngrok http 3000
# Copia: https://abc123def456.ngrok-free.app

# En Meta for Developers:
# Callback URL: https://abc123def456.ngrok-free.app/webhook/whatsapp
# Verify token: mi_token_secreto_de_verificacion
# Clic en: "Verify and save"

# ✅ Listo! El webhook está configurado
```

---

## 💡 Consejos

1. **Para desarrollo**: ngrok es perfecto, pero la URL cambia cada vez que lo reinicias
2. **Para producción**: Usa un dominio propio y configura SSL
3. **Token seguro**: Usa un token difícil de adivinar (no uses "123" o "test")
4. **Mantén ngrok activo**: Si cierras ngrok, el webhook dejará de funcionar
5. **Monitorea los logs**: Revisa la terminal del servidor para ver los mensajes recibidos

---

## 📚 Recursos Adicionales

- [WHATSAPP_TOKENS.md](WHATSAPP_TOKENS.md) - Explicación de los tokens
- [INSTALLATION.md](INSTALLATION.md) - Guía completa de instalación
- [Documentación oficial de WhatsApp Webhooks](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks)

