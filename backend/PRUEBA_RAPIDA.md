# ⚡ Prueba Rápida del Sistema

## ✅ ¡El Sistema Está Funcionando!

El script de prueba se ejecutó correctamente. Aquí tienes diferentes formas de probar el sistema:

---

## 🧪 Método 1: Prueba Local (Más Fácil) ⭐

### Ejecuta el script de prueba:

```bash
cd backend
node test-webhook.js
```

**✅ Resultado esperado:**
- Respuesta: `200 OK`
- Mensaje: "Prueba completada"
- El pedido se guarda en la base de datos

**📊 Verifica en los logs del servidor:**
```
✅ Pedido almacenado - ID: 1, Teléfono: 573001234567
📝 Texto: Hola, necesito 50 panes, 30 croissants y 20 donas para mañana a las 8am
```

---

## 📱 Método 2: Prueba con WhatsApp Real

### Paso 1: Verifica la Configuración

1. **Abre Meta for Developers**
2. **Verifica el webhook:**
   - Callback URL: `https://dissipative-firstly-emil.ngrok-free.dev/webhook/whatsapp`
   - Estado: ✅ Verificado

### Paso 2: Envía un Mensaje

1. **Abre WhatsApp** en tu teléfono
2. **Envía un mensaje** al número de WhatsApp Business:
   ```
   Hola, necesito 50 panes y 30 croissants para mañana
   ```

### Paso 3: Verifica la Recepción

**En la terminal del servidor:**
```
✅ Pedido almacenado - ID: 1, Teléfono: 573001234567
📝 Texto: Hola, necesito 50 panes y 30 croissants para mañana
✅ Mensaje de confirmación enviado a 573001234567
```

**En WhatsApp recibirás:**
```
✅ Pedido recibido correctamente.

ID de pedido: #1

Tu pedido ha sido registrado y está siendo procesado. Te notificaremos cuando esté listo.
```

---

## 📊 Verificar los Resultados

### Ver Pedidos en la Base de Datos

```bash
cd backend

# Ver todos los pedidos
sqlite3 data/orders.db "SELECT * FROM orders;"

# Ver el último pedido
sqlite3 data/orders.db "SELECT * FROM orders ORDER BY id DESC LIMIT 1;"

# Contar pedidos
sqlite3 data/orders.db "SELECT COUNT(*) FROM orders;"
```

### Ver Logs del Servidor

Revisa la terminal donde está corriendo `npm run dev`. Deberías ver:
- ✅ Mensajes de recepción
- ✅ Confirmaciones enviadas
- ✅ Tiempo de procesamiento

### Ver Peticiones en ngrok

Abre en tu navegador: `http://localhost:4040`

Aquí puedes ver:
- Todas las peticiones HTTP
- Contenido de peticiones y respuestas
- Logs en tiempo real

---

## ✅ Checklist de Prueba

### Prueba Básica
- [x] ✅ Script de prueba ejecutado
- [ ] Verificar que el pedido se guardó en la base de datos
- [ ] Verificar logs del servidor
- [ ] Verificar tiempo de respuesta (< 5 segundos)

### Prueba con WhatsApp Real
- [ ] Webhook configurado en Meta for Developers
- [ ] Enviar mensaje desde WhatsApp
- [ ] Verificar recepción en logs del servidor
- [ ] Verificar confirmación recibida en WhatsApp
- [ ] Verificar que el pedido se guardó

---

## 🎯 Qué Verificar

### 1. Recepción del Mensaje
- ✅ El servidor recibe el webhook
- ✅ Responde en menos de 5 segundos
- ✅ Procesa el mensaje correctamente

### 2. Almacenamiento
- ✅ Número de teléfono capturado
- ✅ Texto original almacenado completo
- ✅ Fecha y hora registradas
- ✅ Estado del pedido: "received"

### 3. Confirmación
- ✅ Mensaje de confirmación enviado
- ✅ Confirmación recibida en WhatsApp
- ✅ ID del pedido incluido en la confirmación

---

## 🐛 Si Algo No Funciona

### Problema: No recibo el mensaje en el servidor

**Solución:**
```bash
# 1. Verifica que el servidor esté corriendo
curl http://localhost:3000/health

# 2. Verifica que ngrok esté corriendo
curl http://localhost:4040/api/tunnels

# 3. Verifica la configuración en Meta for Developers
# 4. Prueba con el script local primero
node test-webhook.js
```

### Problema: No se envía la confirmación

**Solución:**
```bash
# 1. Verifica las variables de entorno
cat .env | grep WHATSAPP_ACCESS_TOKEN
cat .env | grep WHATSAPP_PHONE_NUMBER_ID

# 2. Verifica los logs del servidor
# 3. Verifica que el token sea válido
```

---

## 📈 Resultados Esperados

### Prueba Local (test-webhook.js)
```
✅ Respuesta: 200 OK
✅ Pedido almacenado en base de datos
✅ Tiempo de respuesta: < 100ms
```

### Prueba con WhatsApp Real
```
✅ Mensaje recibido en el servidor
✅ Pedido almacenado en base de datos
✅ Confirmación enviada en < 5 segundos
✅ Confirmación recibida en WhatsApp
```

---

## 🎉 ¡Todo Listo!

Si todo funciona correctamente:

1. ✅ El sistema recibe mensajes de WhatsApp
2. ✅ Los pedidos se almacenan correctamente
3. ✅ Las confirmaciones se envían automáticamente
4. ✅ El tiempo de respuesta es menor a 5 segundos

**¡El sistema está funcionando correctamente! 🚀**

---

## 📚 Más Información

- Guía completa de pruebas: [COMO_PROBAR.md](COMO_PROBAR.md)
- Configuración del webhook: [CONFIGURAR_WEBHOOK.md](CONFIGURAR_WEBHOOK.md)
- Solución de problemas: [SOLUCION_ERROR_NGROK.md](SOLUCION_ERROR_NGROK.md)

