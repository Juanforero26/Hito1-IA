# 🔧 Solución: Error "Recipient phone number not in allowed list"

## ❌ Error Detectado

```
Error al enviar confirmación:
{
  "error": {
    "message": "(#131030) Recipient phone number not in allowed list",
    "type": "OAuthException",
    "code": 131030,
    "error_data": {
      "messaging_product": "whatsapp",
      "details": "Recipient phone number not in allowed list: Add recipient phone number to recipient list and try again."
    }
  }
}
```

---

## 🔍 ¿Qué Significa Este Error?

Este error ocurre porque **estás usando WhatsApp Business API en modo de prueba (sandbox)** y el número de teléfono al que intentas enviar el mensaje **no está en tu lista de números permitidos**.

### ¿Por qué pasa esto?

En el **modo de prueba** de WhatsApp Business API:
- ✅ Puedes **recibir** mensajes de cualquier número
- ❌ Solo puedes **enviar** mensajes a números que hayas agregado a tu lista de permitidos
- 🔒 Esto es una restricción de seguridad para prevenir spam

---

## ✅ Solución: Agregar Número a la Lista de Permitidos

### Paso 1: Ve a Meta for Developers

1. **Abre tu navegador** y ve a: https://developers.facebook.com/
2. **Inicia sesión** con tu cuenta
3. **Selecciona tu aplicación** de WhatsApp Business

### Paso 2: Accede a la Configuración de WhatsApp

1. En el menú lateral, busca **"WhatsApp"**
2. Haz clic en **"WhatsApp"** → **"API Setup"** o **"Getting Started"**
3. Busca la sección **"To"** o **"Phone numbers"** o **"Recipient phone numbers"**

### Paso 3: Agrega el Número de Teléfono

1. **Busca el campo** donde puedes agregar números de teléfono
2. **Agrega el número** al que quieres enviar mensajes
   - Formato: Solo el número sin espacios, guiones o símbolos
   - Ejemplo: `573001234567` (sin el +)
   - Debe incluir el código de país
3. **Haz clic en "Agregar"** o "Add"

### Paso 4: Verifica el Número

1. **WhatsApp enviará un código de verificación** al número
2. **Ingresa el código** para verificar el número
3. **El número quedará agregado** a tu lista de permitidos

---

## 📋 Paso a Paso Detallado

### Opción A: Desde "Getting Started"

1. Ve a: **WhatsApp** → **Getting Started**
2. Busca la sección **"Step 2: Send a test message"** o similar
3. Verás un campo **"To"** o **"Phone number"**
4. Ingresa el número de teléfono (formato: `573001234567`)
5. Haz clic en **"Send Message"** o **"Verify"**
6. Recibirás un código de verificación en WhatsApp
7. Ingresa el código para verificar

### Opción B: Desde "API Setup"

1. Ve a: **WhatsApp** → **API Setup**
2. Busca la sección **"Recipient phone numbers"** o **"To"**
3. Haz clic en **"Add phone number"** o **"Manage phone numbers"**
4. Ingresa el número de teléfono
5. Verifica el número con el código que recibes

### Opción C: Desde la Interfaz de Prueba

1. Ve a: **WhatsApp** → **API Setup** → **"Send and receive messages"**
2. Busca la sección **"To"** (destinatario)
3. Ingresa el número de teléfono
4. Haz clic en **"Send Message"**
5. Verifica el número

---

## 🔢 Formato del Número de Teléfono

### Formato Correcto:
- ✅ `573001234567` (código de país + número, sin espacios, sin +, sin guiones)
- ✅ `521234567890` (México)
- ✅ `34612345678` (España)

### Formatos Incorrectos:
- ❌ `+57 300 123 4567` (con espacios y símbolos)
- ❌ `300-123-4567` (sin código de país)
- ❌ `(57) 300 123 4567` (con paréntesis y espacios)

### Cómo Obtener el Formato Correcto:

1. **Toma el número completo** con código de país
2. **Elimina todos los espacios, guiones, paréntesis y símbolos**
3. **Elimina el símbolo +** si lo tiene
4. **Solo deja los dígitos**

**Ejemplo:**
- Número original: `+57 300 123 4567`
- Formato correcto: `573001234567`

---

## 🧪 Verificar que Funciona

### Paso 1: Verifica que el Número Esté Agregado

1. Ve a Meta for Developers
2. Verifica que el número aparezca en tu lista de permitidos
3. Asegúrate de que esté **verificado** (no solo agregado)

### Paso 2: Prueba Enviar un Mensaje

1. **Desde tu servidor**, envía un mensaje de prueba
2. **O desde Meta for Developers**, usa la interfaz de prueba
3. **Verifica que el mensaje se envíe correctamente**

### Paso 3: Prueba el Flujo Completo

1. **Envía un mensaje desde WhatsApp** al número de WhatsApp Business
2. **Verifica en los logs del servidor** que se reciba el mensaje
3. **Verifica que se envíe la confirmación** sin errores
4. **Verifica que recibas la confirmación** en WhatsApp

---

## 🐛 Solución de Problemas

### Problema: No encuentro dónde agregar números

**Solución:**
1. Asegúrate de estar en el modo de **prueba/sandbox**
2. Busca en: **WhatsApp** → **Getting Started** o **API Setup**
3. Busca la sección **"To"** o **"Recipient phone numbers"**
4. Si no encuentras la opción, verifica que tengas permisos de administrador

### Problema: El número no se verifica

**Solución:**
1. Verifica que el número esté correcto (formato sin espacios)
2. Asegúrate de recibir el código de verificación en WhatsApp
3. Verifica que el código no haya expirado (tiene tiempo limitado)
4. Intenta agregar el número nuevamente

### Problema: Sigo viendo el error después de agregar el número

**Solución:**
1. Verifica que el número esté en el formato correcto (sin espacios, sin +)
2. Verifica que el número esté **verificado** (no solo agregado)
3. Espera unos minutos y vuelve a intentar (puede tomar tiempo en propagarse)
4. Verifica que estés usando el número correcto en tu código

### Problema: No recibo el código de verificación

**Solución:**
1. Verifica que el número de teléfono sea correcto
2. Asegúrate de tener WhatsApp instalado en ese número
3. Verifica que el número tenga conexión a internet
4. Intenta agregar el número nuevamente
5. Revisa si hay restricciones en tu cuenta de WhatsApp Business

---

## 📱 Números Múltiples

### Agregar Múltiples Números:

1. **Repite el proceso** para cada número que quieras agregar
2. **Cada número debe ser verificado** individualmente
3. **Puedes agregar hasta 5 números** en el modo de prueba (depende de tu plan)

### Formato para Múltiples Números:

Cada número debe estar en una línea separada o en campos separados:
```
573001234567
573009876543
521234567890
```

---

## 🚀 Para Producción

### Modo de Prueba vs Producción:

- **Modo de Prueba (Sandbox)**:
  - ✅ Gratuito
  - ❌ Solo puedes enviar a números permitidos
  - ❌ Limitado a 5 números (generalmente)
  - ✅ Perfecto para desarrollo y pruebas

- **Modo de Producción**:
  - ✅ Puedes enviar a cualquier número
  - ✅ Sin restricciones de números permitidos
  - ⚠️ Requiere verificación de negocio
  - ⚠️ Puede tener costos

### Migrar a Producción:

1. **Verifica tu negocio** en Meta Business
2. **Completa el proceso de verificación**
3. **Solicita acceso a producción**
4. **Configura tu número de producción**
5. **Actualiza tus credenciales** (Access Token, Phone Number ID)

---

## ✅ Resumen

### El Error:
```
Recipient phone number not in allowed list
```

### La Causa:
- Estás en modo de prueba de WhatsApp Business API
- El número no está en tu lista de permitidos

### La Solución:
1. Ve a Meta for Developers
2. Agrega el número a tu lista de permitidos
3. Verifica el número con el código que recibes
4. Prueba enviar un mensaje

### Pasos Rápidos:
1. ✅ Meta for Developers → WhatsApp → Getting Started
2. ✅ Agrega el número (formato: `573001234567`)
3. ✅ Verifica con el código de WhatsApp
4. ✅ Prueba el sistema nuevamente

---

## 🎯 Siguiente Paso

Una vez que agregues el número a la lista de permitidos:

1. **Verifica que el número esté agregado** en Meta for Developers
2. **Envía un mensaje de prueba** desde WhatsApp
3. **Verifica que recibas la confirmación** sin errores
4. **Revisa los logs del servidor** para confirmar que todo funciona

---

## 📚 Recursos Adicionales

- [Documentación de WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Guía de números permitidos](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/manage-phone-numbers)
- [Solución de problemas comunes](https://developers.facebook.com/docs/whatsapp/cloud-api/support)

---

## 💡 Consejos

1. **Agrega todos los números de prueba** antes de empezar a probar
2. **Verifica el formato** del número (sin espacios, sin +)
3. **Guarda los números permitidos** en un lugar seguro
4. **Para producción**, considera migrar a un plan que permita enviar a cualquier número
5. **Monitorea los errores** para identificar números que necesitan ser agregados

---

## ✅ Checklist

- [ ] Identificar el número que causa el error
- [ ] Ir a Meta for Developers
- [ ] Agregar el número a la lista de permitidos
- [ ] Verificar el número con el código
- [ ] Probar el sistema nuevamente
- [ ] Verificar que no haya más errores
- [ ] Confirmar que la confirmación se envía correctamente

