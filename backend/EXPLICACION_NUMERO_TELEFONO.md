# 📱 Explicación: ¿De Dónde Viene el Número de Teléfono?

## 🔍 ¿Por Qué Usa el Número `573001234567`?

El sistema usa el número `573001234567` por **dos razones diferentes**:

---

## 1️⃣ En las Pruebas (Script test-webhook.js)

### ¿De dónde viene?

En el archivo `test-webhook.js`, el número está **hardcodeado** (escrito directamente en el código) como un número de ejemplo:

```javascript
// Línea 36 en test-webhook.js
from: '573001234567',
```

### ¿Por qué este número?

- **Es un número de ejemplo**: No es un número real, es solo para pruebas
- **Formato colombiano**: `57` es el código de país de Colombia, `3001234567` es un número de ejemplo
- **Número de prueba**: Se usa solo para simular un mensaje de WhatsApp

### ¿Puedo cambiarlo?

**¡Sí!** Puedes cambiar el número en el script de prueba a cualquier número que quieras usar para probar:

```javascript
// En test-webhook.js, línea 36
from: 'TU_NUMERO_AQUI',  // Cambia esto a tu número real
```

---

## 2️⃣ En Mensajes Reales de WhatsApp

### ¿De dónde viene?

Cuando recibes un mensaje **real** de WhatsApp, el número viene **directamente del mensaje** que WhatsApp envía a tu servidor.

### ¿Cómo se obtiene?

En el código (línea 68 de `webhookController.js`):

```javascript
const phoneNumber = message.from; // Número del remitente
```

WhatsApp envía el número del remitente en el campo `from` del mensaje. Este número es el número **real** de la persona que envió el mensaje.

### Ejemplo de Mensaje Real de WhatsApp:

```json
{
  "from": "573009876543",  // ← Este es el número REAL del remitente
  "id": "wamid.ABC123",
  "timestamp": "1234567890",
  "type": "text",
  "text": {
    "body": "Hola, necesito 50 panes"
  }
}
```

El sistema **automáticamente** extrae el número del campo `from` y lo usa para:
1. Guardar el pedido en la base de datos
2. Enviar la confirmación de vuelta a ese número

---

## 📊 Flujo del Número de Teléfono

### En Pruebas (test-webhook.js):
```
Script de prueba
    ↓
Número hardcodeado: '573001234567'
    ↓
Servidor recibe el mensaje
    ↓
Extrae: message.from = '573001234567'
    ↓
Guarda en base de datos
    ↓
Intenta enviar confirmación a '573001234567'
```

### En Mensajes Reales:
```
Cliente envía mensaje desde WhatsApp
    ↓
WhatsApp envía webhook a tu servidor
    ↓
Webhook incluye: message.from = 'NÚMERO_REAL_DEL_CLIENTE'
    ↓
Servidor extrae: const phoneNumber = message.from
    ↓
Guarda en base de datos con el número real
    ↓
Envía confirmación al número real del cliente
```

---

## 🔧 Cómo Cambiar el Número en las Pruebas

### Opción 1: Cambiar en test-webhook.js

Edita el archivo `backend/test-webhook.js`:

```javascript
// Línea 31 y 36
contacts: [
  {
    profile: {
      name: 'Cliente de Prueba'
    },
    wa_id: 'TU_NUMERO_AQUI'  // Cambia esto
  }
],
messages: [
  {
    from: 'TU_NUMERO_AQUI',  // Cambia esto también
    // ... resto del código
  }
]
```

### Opción 2: Usar Variables de Entorno

Puedes modificar el script para usar una variable de entorno:

```javascript
// En test-webhook.js
const TEST_PHONE_NUMBER = process.env.TEST_PHONE_NUMBER || '573001234567';

// Luego usa TEST_PHONE_NUMBER en lugar del número hardcodeado
from: TEST_PHONE_NUMBER,
```

Y ejecutar:
```bash
TEST_PHONE_NUMBER=573009876543 node test-webhook.js
```

---

## 💡 ¿Qué Número Debería Usar?

### Para Pruebas Locales:

Puedes usar cualquier número de ejemplo:
- `573001234567` (Colombia)
- `521234567890` (México)
- `34612345678` (España)
- Cualquier número en formato internacional sin espacios

### Para Pruebas con WhatsApp Real:

**Debes usar tu número real** (el número que tienes agregado en Meta for Developers):
- El número que agregaste a la lista de permitidos
- El número desde el que vas a enviar mensajes de prueba
- Debe estar en formato internacional sin espacios: `573009876543`

---

## ⚠️ Importante: Números en Modo de Prueba

### En Modo de Prueba (Sandbox):

- ✅ Puedes **recibir** mensajes de cualquier número
- ❌ Solo puedes **enviar** mensajes a números en tu lista de permitidos
- 🔒 El número debe estar agregado en Meta for Developers

### Si Quieres Probar con tu Número Real:

1. **Agrega tu número** en Meta for Developers
2. **Cambia el número** en `test-webhook.js` a tu número real
3. **Ejecuta el script** de prueba
4. **Verifica** que recibas la confirmación

---

## 🎯 Resumen

### ¿Por qué usa `573001234567`?

1. **En pruebas**: Es un número de ejemplo hardcodeado en `test-webhook.js`
2. **En producción**: El número viene del mensaje real de WhatsApp (campo `from`)

### ¿De dónde viene el número?

- **Pruebas**: Del código del script (`test-webhook.js`)
- **Real**: Del webhook de WhatsApp (campo `message.from`)

### ¿Puedo cambiarlo?

- **Sí**, puedes cambiar el número en `test-webhook.js`
- **No necesitas cambiarlo** para mensajes reales (se obtiene automáticamente)

### ¿Qué número debo usar?

- **Para pruebas**: Cualquier número de ejemplo (ej: `573001234567`)
- **Para pruebas reales**: Tu número real (debe estar en la lista de permitidos)

---

## 🔍 Verificar Qué Número se Está Usando

### Ver en los Logs del Servidor:

```
✅ Pedido almacenado - ID: 1, Teléfono: 573001234567
```

### Ver en la Base de Datos:

```bash
sqlite3 backend/data/orders.db "SELECT phone_number FROM orders;"
```

### Ver en el Código:

```javascript
// Línea 68 en webhookController.js
const phoneNumber = message.from; // Este es el número que se usa
```

---

## 📚 Archivos Relacionados

- **test-webhook.js**: Número hardcodeado para pruebas
- **webhookController.js**: Extrae el número del mensaje real
- **order.js**: Guarda el número en la base de datos

---

## ✅ Conclusión

El sistema usa el número `573001234567` porque:
1. Es el número de ejemplo en el script de prueba
2. Es fácil de reconocer como un número de prueba
3. Tiene el formato correcto (código de país + número)

**Para mensajes reales**, el sistema automáticamente usará el número real del cliente que envía el mensaje. No necesitas cambiar nada en el código para que funcione con números reales.

