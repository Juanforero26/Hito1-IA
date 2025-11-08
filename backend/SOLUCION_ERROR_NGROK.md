# 🔧 Solución: Error ERR_NGROK_3200

## ❌ Error: "The endpoint is offline"

Este error significa que **ngrok no está conectado** o **tu servidor no está corriendo**.

---

## 🔍 Diagnóstico Rápido

### ¿Qué significa este error?

El error `ERR_NGROK_3200` indica que:
- ❌ ngrok no está corriendo, O
- ❌ Tu servidor backend no está corriendo en el puerto 3000, O
- ❌ ngrok perdió la conexión con tu servidor

---

## ✅ Solución Paso a Paso

### Paso 1: Verifica que tu servidor backend esté corriendo

Abre una terminal y ejecuta:

```bash
cd backend
npm run dev
```

**Debes ver:**
```
🚀 Servidor corriendo en el puerto 3000
📱 Webhook de WhatsApp: http://localhost:3000/webhook/whatsapp
```

✅ **Si ves esto**: Tu servidor está funcionando  
❌ **Si NO ves esto**: Tu servidor no está corriendo → Inícialo primero

---

### Paso 2: Verifica que ngrok esté corriendo

Abre **otra terminal** (deja la del servidor corriendo) y ejecuta:

```bash
ngrok http 3000
```

**Debes ver algo como:**
```
Session Status                online
Account                       (Plan: Free)
Version                       3.31.0
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123def456.ngrok-free.app -> http://localhost:3000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

✅ **Si ves "Session Status: online"**: ngrok está funcionando  
❌ **Si NO ves esto**: ngrok no está corriendo → Inícialo

---

### Paso 3: Verifica la conexión

1. **Copia la URL HTTPS** que ngrok te muestra (ej: `https://abc123def456.ngrok-free.app`)

2. **Prueba acceder** en tu navegador a:
   ```
   https://TU_URL_NGROK.ngrok-free.app/health
   ```

3. **Debes ver:**
   ```json
   {
     "status": "ok",
     "message": "Servidor funcionando correctamente"
   }
   ```

✅ **Si ves esto**: Todo está funcionando correctamente  
❌ **Si ves el error ERR_NGROK_3200**: Sigue con el Paso 4

---

### Paso 4: Si el error persiste

#### Opción A: Reinicia todo

1. **Detén el servidor** (Ctrl+C en la terminal del servidor)
2. **Detén ngrok** (Ctrl+C en la terminal de ngrok)
3. **Reinicia el servidor**:
   ```bash
   cd backend
   npm run dev
   ```
4. **Reinicia ngrok** (en otra terminal):
   ```bash
   ngrok http 3000
   ```
5. **Copia la NUEVA URL** de ngrok (puede cambiar)
6. **Actualiza la URL en Meta for Developers** si cambió

#### Opción B: Verifica que el puerto 3000 esté libre

```bash
# Verifica qué está usando el puerto 3000
lsof -i :3000

# Si hay algo usando el puerto, detén el proceso
# O usa otro puerto (ej: 3001) y actualiza ngrok: ngrok http 3001
```

#### Opción C: Verifica la configuración de ngrok

```bash
# Verifica que ngrok esté correctamente instalado
ngrok version

# Si hay problemas, reinstala ngrok
brew install ngrok/ngrok/ngrok
```

---

## 🎯 Checklist de Verificación

Antes de usar el webhook, asegúrate de:

- [ ] ✅ Servidor backend corriendo (`npm run dev`)
- [ ] ✅ ngrok corriendo (`ngrok http 3000`)
- [ ] ✅ Sesión de ngrok muestra "Status: online"
- [ ] ✅ Puedes acceder a `https://TU_URL.ngrok-free.app/health`
- [ ] ✅ La URL de ngrok está configurada en Meta for Developers
- [ ] ✅ El verify token está configurado correctamente

---

## 🔄 Flujo Correcto

```bash
# Terminal 1: Servidor Backend
cd backend
npm run dev
# ✅ Debes ver: "🚀 Servidor corriendo en el puerto 3000"

# Terminal 2: ngrok
ngrok http 3000
# ✅ Debes ver: "Session Status: online"
# ✅ Copia la URL: https://abc123.ngrok-free.app

# Navegador: Prueba la conexión
# Ve a: https://abc123.ngrok-free.app/health
# ✅ Debes ver: {"status":"ok","message":"Servidor funcionando correctamente"}

# Meta for Developers:
# Callback URL: https://abc123.ngrok-free.app/webhook/whatsapp
# Verify token: tu_token_aqui
# ✅ Haz clic en "Verify and save"
```

---

## 🐛 Problemas Comunes

### Problema 1: "ngrok: command not found"
```bash
# Reinstala ngrok
brew install ngrok/ngrok/ngrok
```

### Problema 2: "Port 3000 is already in use"
```bash
# Encuentra qué está usando el puerto 3000
lsof -i :3000

# Mata el proceso o usa otro puerto
# Ejemplo: usa puerto 3001
# En backend: cambia PORT=3001 en .env
# En ngrok: ngrok http 3001
```

### Problema 3: "Session expired" en ngrok
```bash
# Simplemente reinicia ngrok
ngrok http 3000
```

### Problema 4: La URL de ngrok cambia cada vez
- Esto es normal con la cuenta gratuita de ngrok
- Cada vez que reinicias ngrok, obtienes una URL diferente
- Debes actualizar la URL en Meta for Developers cada vez

### Problema 5: "Cannot reach callback URL" en Meta
- Verifica que ngrok esté corriendo
- Verifica que el servidor esté corriendo
- Verifica que uses la URL HTTPS (no HTTP)
- Verifica que añadiste `/webhook/whatsapp` al final

---

## 💡 Consejos

1. **Mantén ambas terminales abiertas**:
   - Terminal 1: Servidor backend
   - Terminal 2: ngrok

2. **Usa la interfaz web de ngrok**:
   - Abre `http://localhost:4040` en tu navegador
   - Puedes ver todas las peticiones en tiempo real
   - Útil para depurar problemas

3. **Verifica la conexión regularmente**:
   - Si no usas ngrok por un tiempo, la sesión puede expirar
   - Reinicia ngrok si es necesario

4. **Para desarrollo continuo**:
   - Considera crear una cuenta gratuita de ngrok
   - Con cuenta puedes tener URLs estables (no cambian)

---

## ✅ Resumen

**El error ERR_NGROK_3200 significa que:**
- ngrok no está corriendo, O
- Tu servidor no está corriendo, O
- Perdieron la conexión entre sí

**Para resolverlo:**
1. ✅ Asegúrate de que el servidor esté corriendo
2. ✅ Asegúrate de que ngrok esté corriendo
3. ✅ Verifica que puedas acceder a la URL de ngrok
4. ✅ Actualiza la configuración en Meta for Developers si es necesario

---

## 🆘 Si nada funciona

1. **Reinicia todo desde cero**:
   ```bash
   # Terminal 1
   cd backend
   npm run dev
   
   # Terminal 2
   ngrok http 3000
   ```

2. **Verifica los logs**:
   - Revisa la terminal del servidor para ver errores
   - Revisa la interfaz web de ngrok (`http://localhost:4040`)

3. **Prueba con curl**:
   ```bash
   curl https://TU_URL_NGROK.ngrok-free.app/health
   ```

4. **Verifica la configuración**:
   - Revisa que el `.env` esté correcto
   - Revisa que el servidor esté en el puerto correcto
   - Revisa que ngrok esté apuntando al puerto correcto

