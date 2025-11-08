# 🚀 Guía Rápida de ngrok

## ✅ ngrok está instalado

ngrok ya está instalado en tu sistema. Ahora puedes usarlo para exponer tu servidor local a internet.

---

## 🎯 ¿Para qué sirve ngrok?

ngrok crea un **túnel seguro** entre internet y tu servidor local, permitiendo que WhatsApp pueda enviar webhooks a tu aplicación que está corriendo en `localhost:3000`.

**Sin ngrok**: WhatsApp no puede acceder a `http://localhost:3000` (solo tú puedes)  
**Con ngrok**: WhatsApp puede acceder a `https://tu-url.ngrok-free.app` → tu servidor local

---

## 📋 Cómo Usar ngrok

### Paso 1: Inicia tu servidor backend

```bash
cd backend
npm run dev
```

Deberías ver:
```
🚀 Servidor corriendo en el puerto 3000
```

### Paso 2: En otra terminal, inicia ngrok

```bash
ngrok http 3000
```

### Paso 3: Copia la URL HTTPS

ngrok mostrará algo como:

```
Forwarding: https://abc123def456.ngrok-free.app -> http://localhost:3000
```

Copia la URL `https://abc123def456.ngrok-free.app`

### Paso 4: Usa esta URL en Meta for Developers

En el campo "Callback URL", pega:
```
https://abc123def456.ngrok-free.app/webhook/whatsapp
```

---

## ⚠️ Importante

### 1. ngrok debe estar activo
- Si cierras ngrok, el webhook dejará de funcionar
- Cada vez que reinicias ngrok, obtienes una URL diferente
- Si la URL cambia, debes actualizar la configuración en Meta for Developers

### 2. URLs temporales
- Las URLs gratuitas de ngrok cambian cada vez que lo reinicias
- Para desarrollo está bien, pero para producción necesitarás un dominio propio

### 3. Mantén ambas terminales abiertas
- Terminal 1: Servidor backend (`npm run dev`)
- Terminal 2: ngrok (`ngrok http 3000`)

---

## 🔧 Comandos Útiles de ngrok

### Iniciar ngrok en puerto 3000
```bash
ngrok http 3000
```

### Ver la interfaz web de ngrok
Cuando ngrok está corriendo, abre en tu navegador:
```
http://localhost:4040
```

Aquí puedes ver:
- Todas las peticiones que llegan a tu servidor
- El contenido de las peticiones y respuestas
- Logs en tiempo real

### Verificar que ngrok está funcionando
```bash
# En otra terminal, prueba hacer una petición a tu servidor
curl https://TU_URL_NGROK.ngrok-free.app/health
```

Deberías recibir:
```json
{"status":"ok","message":"Servidor funcionando correctamente"}
```

---

## 🆓 Cuenta Gratuita de ngrok

### Con cuenta gratuita:
- ✅ Funciona perfecto para desarrollo
- ✅ URLs HTTPS seguras
- ✅ Túnel básico (suficiente para webhooks)
- ⚠️ URLs cambian cada vez que reinicias
- ⚠️ Límite de conexiones simultáneas

### Crear cuenta (opcional):
```bash
# 1. Regístrate en https://ngrok.com/signup
# 2. Obtén tu authtoken
# 3. Configura ngrok:
ngrok config add-authtoken TU_AUTHTOKEN
```

Con cuenta gratuita puedes:
- URLs estables (no cambian)
- Más funciones
- Mejor para desarrollo a largo plazo

---

## 🐛 Solución de Problemas

### Error: "ngrok: command not found"
```bash
# Reinstalar ngrok
brew install ngrok/ngrok/ngrok
```

### Error: "Session expired"
- Esto pasa si ngrok se queda inactivo mucho tiempo
- Simplemente reinicia ngrok: `ngrok http 3000`

### La URL de ngrok cambió
1. Copia la nueva URL de ngrok
2. Ve a Meta for Developers
3. Actualiza la "Callback URL" con la nueva URL
4. Haz clic en "Verify and save"

### No puedo acceder a la URL de ngrok
1. Verifica que ngrok esté corriendo: `ngrok http 3000`
2. Verifica que tu servidor esté corriendo: `npm run dev`
3. Verifica que uses la URL HTTPS (no HTTP)
4. Prueba acceder desde otro dispositivo/navegador

---

## 🎯 Flujo Completo

```bash
# Terminal 1: Servidor
cd backend
npm run dev

# Terminal 2: ngrok
ngrok http 3000
# Copia la URL: https://abc123.ngrok-free.app

# En Meta for Developers:
# Callback URL: https://abc123.ngrok-free.app/webhook/whatsapp
# Verify token: mi_token_secreto_de_verificacion
# Clic en: "Verify and save"

# ✅ Listo! Ahora puedes recibir mensajes de WhatsApp
```

---

## 📚 Alternativas a ngrok

Si no quieres usar ngrok, puedes usar:

1. **localtunnel** (gratuito, similar a ngrok):
   ```bash
   npm install -g localtunnel
   lt --port 3000
   ```

2. **serveo** (gratuito, sin instalación):
   ```bash
   ssh -R 80:localhost:3000 serveo.net
   ```

3. **Deploy en producción** (Heroku, Railway, Render, etc.):
   - No necesitas ngrok
   - Usas tu dominio propio
   - Mejor para producción

---

## ✅ Resumen

- ✅ ngrok está instalado
- ✅ Usa `ngrok http 3000` para exponer tu servidor
- ✅ Copia la URL HTTPS para usar en Meta for Developers
- ✅ Mantén ngrok corriendo mientras desarrollas
- ✅ Usa `http://localhost:4040` para ver las peticiones en tiempo real

---

## 🚀 Siguiente Paso

Ahora que ngrok está instalado:

1. Inicia tu servidor: `npm run dev`
2. Inicia ngrok: `ngrok http 3000`
3. Completa la configuración del webhook en Meta for Developers
4. ¡Listo para recibir mensajes de WhatsApp!

