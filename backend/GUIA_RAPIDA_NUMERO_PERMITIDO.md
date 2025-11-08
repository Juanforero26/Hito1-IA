# ⚡ Guía Rápida: Agregar Número a Lista de Permitidos

## ❌ Error que Estás Viendo

```
Error al enviar confirmación: El número 573001234567 no está en la lista de permitidos.
```

---

## ✅ Solución Rápida (3 Pasos)

### Paso 1: Ve a Meta for Developers

1. Abre: https://developers.facebook.com/
2. Inicia sesión
3. Selecciona tu aplicación de WhatsApp Business

### Paso 2: Agrega el Número

1. Ve a: **WhatsApp** → **Getting Started**
2. Busca la sección **"To"** o **"Phone number"**
3. Ingresa el número (formato: `573001234567` - sin espacios, sin +)
4. Haz clic en **"Send Message"** o **"Verify"**

### Paso 3: Verifica el Número

1. Recibirás un código en WhatsApp
2. Ingresa el código en Meta for Developers
3. El número quedará agregado ✅

---

## 🔢 Formato del Número

### ✅ Correcto:
```
573001234567
```

### ❌ Incorrecto:
```
+57 300 123 4567
300-123-4567
(57) 300 123 4567
```

**Regla**: Solo dígitos, sin espacios, sin símbolos, con código de país.

---

## 📍 Dónde Encontrar la Opción

### Opción 1: Getting Started
1. **WhatsApp** → **Getting Started**
2. Busca **"Step 2: Send a test message"**
3. Campo **"To"**

### Opción 2: API Setup
1. **WhatsApp** → **API Setup**
2. Busca **"Recipient phone numbers"**
3. Haz clic en **"Add phone number"**

### Opción 3: Send and Receive Messages
1. **WhatsApp** → **API Setup** → **"Send and receive messages"**
2. Busca la sección **"To"**

---

## 🧪 Verificar que Funciona

1. **Agrega el número** en Meta for Developers
2. **Verifica el número** con el código
3. **Envía un mensaje de prueba** desde WhatsApp
4. **Verifica que recibas la confirmación** sin errores

---

## ⚠️ Importante

- **El pedido SÍ se guarda** en la base de datos (esto funciona correctamente)
- **Solo falla el envío de la confirmación** (porque el número no está permitido)
- **Una vez agregues el número**, la confirmación se enviará correctamente

---

## 🎯 Pasos Completos

```bash
# 1. Identifica el número que causa el error
# (Aparece en el log del servidor)

# 2. Ve a Meta for Developers
# https://developers.facebook.com/

# 3. Agrega el número
# WhatsApp → Getting Started → Campo "To"

# 4. Verifica el número
# Ingresa el código que recibes en WhatsApp

# 5. Prueba nuevamente
# Envía un mensaje desde WhatsApp y verifica que funcione
```

---

## ✅ Checklist

- [ ] Identificar el número del error (aparece en los logs)
- [ ] Ir a Meta for Developers
- [ ] Agregar el número (formato correcto: `573001234567`)
- [ ] Verificar el número con el código
- [ ] Probar el sistema nuevamente
- [ ] Verificar que la confirmación se envíe correctamente

---

## 📚 Más Información

Guía completa: [SOLUCION_ERROR_NUMERO_PERMITIDO.md](SOLUCION_ERROR_NUMERO_PERMITIDO.md)

---

## 💡 Nota

Este error es **normal en el modo de prueba**. En producción, puedes enviar a cualquier número sin restricciones.

