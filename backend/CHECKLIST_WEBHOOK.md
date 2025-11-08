# ✅ Checklist Rápido: Configurar Webhook

## 📋 Pasos en Orden

### 1️⃣ Prepara tu Backend
```bash
cd backend
# Verifica que tienes el archivo .env
cat .env | grep WHATSAPP_VERIFY_TOKEN

# Si no existe, créalo:
cp .env.example .env
# Edita .env y configura el VERIFY_TOKEN
```

### 2️⃣ Inicia tu Servidor
```bash
npm run dev
```
✅ **Verifica**: Debes ver `🚀 Servidor corriendo en el puerto 3000`

### 3️⃣ Inicia ngrok (Nueva Terminal)
```bash
ngrok http 3000
```
✅ **Copia la URL HTTPS**: `https://abc123.ngrok-free.app`

### 4️⃣ Completa los Campos en Meta for Developers

#### Campo 1: Callback URL
```
https://TU_URL_NGROK.ngrok-free.app/webhook/whatsapp
```
Ejemplo:
```
https://abc123def456.ngrok-free.app/webhook/whatsapp
```

#### Campo 2: Verify token
```
mi_token_secreto_de_verificacion
```
⚠️ **DEBE SER EXACTAMENTE IGUAL** al que tienes en tu `.env`

#### Campo 3: Attach a client certificate
🔘 **Déjalo DESACTIVADO** (toggle en gris)

### 5️⃣ Verifica
1. Haz clic en **"Verify and save"**
2. ✅ Deberías ver un mensaje de éxito
3. ✅ En tu terminal del servidor deberías ver: `✅ Webhook verificado correctamente`

---

## 🎯 Valores de Ejemplo

### En tu archivo `.env`:
```env
WHATSAPP_VERIFY_TOKEN=mi_token_secreto_de_verificacion
```

### En Meta for Developers:

**Callback URL:**
```
https://abc123def456.ngrok-free.app/webhook/whatsapp
```

**Verify token:**
```
mi_token_secreto_de_verificacion
```

---

## ❌ Si Algo Sale Mal

### Error: "Webhook verification failed"
- ✅ Verifica que el servidor esté corriendo
- ✅ Verifica que ngrok esté activo
- ✅ Verifica que el token sea EXACTAMENTE igual en `.env` y en Meta

### Error: "Cannot reach callback URL"
- ✅ Verifica que ngrok esté corriendo
- ✅ Verifica que la URL de ngrok sea HTTPS (no HTTP)
- ✅ Verifica que añadiste `/webhook/whatsapp` al final

### No recibes mensajes después de verificar
- ✅ Verifica que estés suscrito a los eventos `messages`
- ✅ Verifica que el `WHATSAPP_ACCESS_TOKEN` esté configurado
- ✅ Verifica que el `WHATSAPP_PHONE_NUMBER_ID` esté configurado

---

## 🧪 Prueba Rápida

1. Envía un mensaje de WhatsApp al número configurado
2. Verifica en la terminal del servidor que recibas:
   ```
   ✅ Pedido almacenado - ID: 1, Teléfono: 573001234567
   ✅ Mensaje de confirmación enviado
   ```

---

## 📚 Más Ayuda

- Guía completa: [CONFIGURAR_WEBHOOK.md](CONFIGURAR_WEBHOOK.md)
- Explicación de tokens: [WHATSAPP_TOKENS.md](WHATSAPP_TOKENS.md)
- Instalación: [INSTALLATION.md](INSTALLATION.md)

