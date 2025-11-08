# 🧪 Guía: Cómo Probar el Sistema

## ✅ Verificación Inicial

Antes de probar, verifica que todo esté funcionando:

### 1. Servidor Backend
```bash
# Verifica que el servidor esté corriendo
curl http://localhost:3000/health
```

**Debes ver:**
```json
{"status":"ok","message":"Servidor funcionando correctamente"}
```

### 2. ngrok
```bash
# Verifica que ngrok esté corriendo
curl http://localhost:4040/api/tunnels
```

**O abre en tu navegador:** `http://localhost:4040`

### 3. URL Pública
Obtén la URL de ngrok y prueba:
```bash
# Reemplaza TU_URL con tu URL de ngrok
curl https://TU_URL.ngrok-free.dev/health
```

---

## 🧪 Métodos de Prueba

### Método 1: Prueba Local con Script (Más Fácil)

Usa el script de prueba incluido que simula un mensaje de WhatsApp:

```bash
cd backend
node test-webhook.js
```

**¿Qué hace este script?**
- Simula una petición de webhook de WhatsApp
- Envía un mensaje de prueba al servidor
- Verifica que el servidor responda correctamente

**Resultado esperado:**
```
🧪 Iniciando prueba del webhook de WhatsApp...
📍 Enviando petición a http://localhost:3000/webhook/whatsapp
📝 Mensaje de prueba: "Hola, necesito 50 panes, 30 croissants y 20 donas para mañana a las 8am"

📡 Estado de respuesta: 200
✅ Respuesta del servidor: OK

✨ Prueba completada. Verifica los logs del servidor para más detalles.
```

**En la terminal del servidor deberías ver:**
```
✅ Pedido almacenado - ID: 1, Teléfono: 573001234567
📝 Texto: Hola, necesito 50 panes, 30 croissants y 20 donas para mañana a las 8am
✅ Mensaje de confirmación enviado a 573001234567
```

---

### Método 2: Prueba con WhatsApp Real

#### Paso 1: Verifica la Configuración del Webhook

1. **Ve a Meta for Developers**
2. **Verifica que el webhook esté configurado:**
   - Callback URL: `https://TU_URL.ngrok-free.dev/webhook/whatsapp`
   - Verify token: El mismo que en tu `.env`
   - Estado: ✅ Verificado

#### Paso 2: Envía un Mensaje de Prueba

1. **Abre WhatsApp** en tu teléfono
2. **Envía un mensaje** al número de WhatsApp Business configurado
   - Ejemplo: "Hola, necesito 50 panes y 30 croissants para mañana"

#### Paso 3: Verifica la Recepción

**En la terminal del servidor deberías ver:**
```
✅ Pedido almacenado - ID: 1, Teléfono: 573001234567
📝 Texto: Hola, necesito 50 panes y 30 croissants para mañana
✅ Mensaje de confirmación enviado a 573001234567
```

**En WhatsApp deberías recibir:**
```
✅ Pedido recibido correctamente.

ID de pedido: #1

Tu pedido ha sido registrado y está siendo procesado. Te notificaremos cuando esté listo.
```

---

### Método 3: Prueba con cURL (Avanzado)

Puedes simular un webhook de WhatsApp manualmente:

```bash
curl -X POST http://localhost:3000/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{
    "object": "whatsapp_business_account",
    "entry": [{
      "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
      "changes": [{
        "value": {
          "messaging_product": "whatsapp",
          "metadata": {
            "display_phone_number": "1234567890",
            "phone_number_id": "PHONE_NUMBER_ID"
          },
          "contacts": [{
            "profile": {
              "name": "Cliente de Prueba"
            },
            "wa_id": "573001234567"
          }],
          "messages": [{
            "from": "573001234567",
            "id": "wamid.test123",
            "timestamp": "'$(date +%s)'",
            "type": "text",
            "text": {
              "body": "Hola, necesito 50 panes para mañana"
            }
          }]
        },
        "field": "messages"
      }]
    }]
  }'
```

---

## 📊 Verificar los Resultados

### 1. Verificar en la Base de Datos

```bash
# Ver todos los pedidos
sqlite3 backend/data/orders.db "SELECT * FROM orders;"

# Ver el último pedido
sqlite3 backend/data/orders.db "SELECT * FROM orders ORDER BY id DESC LIMIT 1;"

# Ver pedidos por número de teléfono
sqlite3 backend/data/orders.db "SELECT * FROM orders WHERE phone_number = '573001234567';"
```

### 2. Verificar los Logs del Servidor

Revisa la terminal donde está corriendo el servidor. Deberías ver:
- ✅ Mensajes de recepción de pedidos
- ✅ Confirmaciones enviadas
- ✅ Errores (si los hay)

### 3. Verificar la Interfaz Web de ngrok

Abre en tu navegador: `http://localhost:4040`

Aquí puedes ver:
- Todas las peticiones HTTP que llegan a tu servidor
- El contenido de las peticiones y respuestas
- Logs en tiempo real
- Útil para depurar problemas

---

## ✅ Checklist de Prueba

### Prueba Básica (Script)
- [ ] Ejecutar `node test-webhook.js`
- [ ] Verificar respuesta 200 OK
- [ ] Verificar logs del servidor
- [ ] Verificar que el pedido se guardó en la base de datos

### Prueba con WhatsApp Real
- [ ] Webhook configurado en Meta for Developers
- [ ] ngrok corriendo y accesible
- [ ] Enviar mensaje desde WhatsApp
- [ ] Verificar recepción en logs del servidor
- [ ] Verificar confirmación recibida en WhatsApp
- [ ] Verificar que el pedido se guardó en la base de datos

### Verificación de Funcionalidades
- [ ] Número de teléfono capturado correctamente
- [ ] Texto original almacenado completo
- [ ] Fecha y hora registradas
- [ ] Confirmación enviada en menos de 5 segundos
- [ ] Pedido guardado en base de datos

---

## 🎯 Escenarios de Prueba

### Escenario 1: Mensaje de Texto Simple
```
Mensaje: "Hola, necesito 50 panes"
Resultado esperado:
- ✅ Pedido almacenado
- ✅ Confirmación enviada
- ✅ Texto completo guardado
```

### Escenario 2: Mensaje Largo
```
Mensaje: "Hola, necesito 50 panes, 30 croissants, 20 donas, 10 pasteles y 5 tortas para mañana a las 8am. Gracias!"
Resultado esperado:
- ✅ Pedido almacenado con texto completo
- ✅ Confirmación enviada
```

### Escenario 3: Múltiples Mensajes
```
Enviar 3 mensajes diferentes desde el mismo número
Resultado esperado:
- ✅ 3 pedidos almacenados
- ✅ 3 confirmaciones enviadas
- ✅ Cada pedido con ID único
```

### Escenario 4: Diferentes Números
```
Enviar mensajes desde números diferentes
Resultado esperado:
- ✅ Cada pedido asociado al número correcto
- ✅ Confirmaciones enviadas a cada número
```

---

## 🐛 Solución de Problemas

### Problema: No recibo el mensaje en el servidor

**Posibles causas:**
1. ❌ El webhook no está configurado correctamente
2. ❌ ngrok no está corriendo
3. ❌ El servidor no está corriendo
4. ❌ La URL del webhook está incorrecta

**Solución:**
```bash
# 1. Verifica que el servidor esté corriendo
curl http://localhost:3000/health

# 2. Verifica que ngrok esté corriendo
curl http://localhost:4040/api/tunnels

# 3. Verifica la configuración en Meta for Developers
# 4. Prueba con el script de prueba local
node test-webhook.js
```

### Problema: Recibo el mensaje pero no se guarda

**Posibles causas:**
1. ❌ Error en la base de datos
2. ❌ Problema con el modelo de datos
3. ❌ Error en el procesamiento del mensaje

**Solución:**
```bash
# 1. Verifica los logs del servidor
# 2. Verifica que la base de datos exista
ls -la backend/data/orders.db

# 3. Verifica los permisos de la base de datos
# 4. Revisa los errores en la terminal del servidor
```

### Problema: No se envía la confirmación

**Posibles causas:**
1. ❌ WHATSAPP_ACCESS_TOKEN no configurado
2. ❌ WHATSAPP_PHONE_NUMBER_ID no configurado
3. ❌ Token inválido o expirado
4. ❌ Error en la API de WhatsApp

**Solución:**
```bash
# 1. Verifica las variables de entorno
cat backend/.env | grep WHATSAPP_ACCESS_TOKEN
cat backend/.env | grep WHATSAPP_PHONE_NUMBER_ID

# 2. Verifica los logs del servidor para errores
# 3. Verifica que el token sea válido en Meta for Developers
# 4. Regenera el token si es necesario
```

---

## 📈 Métricas de Rendimiento

### Verificar Tiempo de Respuesta

El sistema debe responder en menos de 5 segundos. Puedes verificar en los logs:

```
⏱️  Tiempo de procesamiento: 150ms
```

### Verificar Almacenamiento

```bash
# Ver cuántos pedidos hay
sqlite3 backend/data/orders.db "SELECT COUNT(*) FROM orders;"

# Ver el último pedido
sqlite3 backend/data/orders.db "SELECT * FROM orders ORDER BY id DESC LIMIT 1;"
```

---

## 🎉 Prueba Exitosa

Si todo funciona correctamente, deberías ver:

1. ✅ El script de prueba se ejecuta sin errores
2. ✅ Los pedidos se almacenan en la base de datos
3. ✅ Las confirmaciones se envían correctamente
4. ✅ Los logs muestran toda la información correcta
5. ✅ El tiempo de respuesta es menor a 5 segundos

---

## 📚 Próximos Pasos

Una vez que las pruebas básicas funcionen:

1. **Prueba con mensajes reales** desde WhatsApp
2. **Verifica diferentes tipos de mensajes** (texto, botones, etc.)
3. **Prueba con múltiples clientes** simultáneamente
4. **Monitorea el rendimiento** del sistema
5. **Revisa los logs** regularmente

---

## ✅ Resumen

**Para probar rápidamente:**
```bash
cd backend
node test-webhook.js
```

**Para probar con WhatsApp real:**
1. Verifica la configuración del webhook
2. Envía un mensaje desde WhatsApp
3. Verifica los logs del servidor
4. Verifica la confirmación recibida

**Para verificar los resultados:**
```bash
# Ver pedidos en la base de datos
sqlite3 backend/data/orders.db "SELECT * FROM orders;"

# Ver logs del servidor
# (en la terminal donde corre npm run dev)

# Ver peticiones en ngrok
# (abre http://localhost:4040 en tu navegador)
```

