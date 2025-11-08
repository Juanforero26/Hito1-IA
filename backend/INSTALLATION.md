# Guía de Instalación - Backend

## 📋 Prerrequisitos

- Node.js v16 o superior (recomendado v18+)
- npm o yarn
- Cuenta de WhatsApp Business API
- Herramienta para exponer el webhook localmente (ngrok recomendado)

## 🚀 Instalación Paso a Paso

### 1. Instalar Dependencias

```bash
cd backend
npm install
```

### 2. Configurar Variables de Entorno

Copia el archivo de ejemplo y configura tus credenciales:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales de WhatsApp Business API:

```env
PORT=3000
WHATSAPP_VERIFY_TOKEN=mi_token_secreto_de_verificacion
WHATSAPP_ACCESS_TOKEN=tu_access_token_aqui
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id_aqui
DB_PATH=./data/orders.db
```

### 3. Configurar WhatsApp Business API

#### Paso 1: Crear una Aplicación en Meta for Developers

1. Ve a https://developers.facebook.com/
2. Inicia sesión con tu cuenta de Facebook
3. Haz clic en "Mis Aplicaciones" → "Crear Aplicación"
4. Selecciona "Empresa" como tipo de aplicación
5. Completa la información de la aplicación

#### Paso 2: Configurar WhatsApp Business API

1. En el panel de tu aplicación, busca "WhatsApp" en el menú
2. Haz clic en "Configurar" en la sección de WhatsApp
3. Sigue las instrucciones para configurar WhatsApp Business API
4. Obtén tu número de teléfono de prueba (para desarrollo) o configura tu número de producción

#### Paso 3: Obtener Credenciales

> 💡 **Nota Importante**: Hay DOS tokens diferentes. Ver [WHATSAPP_TOKENS.md](WHATSAPP_TOKENS.md) para una explicación detallada.

1. **Access Token (WHATSAPP_ACCESS_TOKEN)**:
   - ⚠️ **Este token lo OBTIENES de Meta/WhatsApp** (no lo creas tú)
   - Ve a "Configuración" → "Básica" en tu aplicación
   - En la sección "Tokens de acceso", genera un token temporal (para pruebas) o un token permanente (para producción)
   - El token es un string largo (ej: `EAAa1b2c3d4e5f6g7h8...`)
   - Copia el token y pégalo en tu archivo `.env`
   - **Se usa para enviar mensajes** a través de la API

2. **Phone Number ID (WHATSAPP_PHONE_NUMBER_ID)**:
   - ⚠️ **Este ID lo OBTIENES de Meta/WhatsApp**
   - Ve a la sección de WhatsApp en tu aplicación
   - Encuentra el ID de tu número de teléfono (formato: números)
   - Copia el ID y pégalo en tu archivo `.env`

3. **Verify Token (WHATSAPP_VERIFY_TOKEN)**:
   - ✅ **Este token LO CREAS TÚ** (no viene de Meta)
   - Es un token personalizado que tú eliges
   - Puede ser cualquier string (ej: `"mi_token_secreto_2024"`)
   - **Debe ser el mismo** en tu archivo `.env` y en la configuración del webhook en Meta
   - **Solo se usa una vez** durante la verificación inicial del webhook

#### Paso 4: Configurar el Webhook

1. **Para desarrollo local con ngrok**:
   ```bash
   # Instala ngrok si no lo tienes
   npm install -g ngrok
   
   # Inicia tu servidor
   npm run dev
   
   # En otra terminal, expone el puerto 3000
   ngrok http 3000
   ```

2. **Configurar el webhook en Meta**:
   - Ve a la sección de WhatsApp en tu aplicación
   - Haz clic en "Configurar webhooks"
   - URL de callback: `https://tu-url-ngrok.ngrok.io/webhook/whatsapp`
   - Token de verificación: El mismo que configuraste en `WHATSAPP_VERIFY_TOKEN`
   - Suscríbete a los eventos: `messages`

3. **Verificar el webhook**:
   - WhatsApp enviará una petición GET a tu URL para verificar
   - Si la verificación es exitosa, verás un mensaje de confirmación

### 4. Iniciar el Servidor

#### Modo Desarrollo (con auto-recarga)

```bash
npm run dev
```

#### Modo Producción

```bash
npm start
```

El servidor estará corriendo en `http://localhost:3000`

### 5. Verificar que Todo Funciona

1. **Verificar salud del servidor**:
   ```bash
   curl http://localhost:3000/health
   ```

2. **Probar el webhook localmente**:
   ```bash
   node test-webhook.js
   ```

3. **Enviar un mensaje de prueba desde WhatsApp**:
   - Envía un mensaje al número de WhatsApp Business configurado
   - Verifica que recibas una confirmación automática
   - Revisa los logs del servidor para confirmar que el mensaje fue procesado

## 🧪 Pruebas

### Probar el Webhook Localmente

Usa el script de prueba incluido:

```bash
node test-webhook.js
```

Este script simula una petición de webhook de WhatsApp y te permite verificar que todo funciona correctamente sin necesidad de configurar ngrok.

### Verificar la Base de Datos

Los pedidos se almacenan en `./data/orders.db`. Puedes usar cualquier cliente de SQLite para verificar los datos:

```bash
# Instalar sqlite3 si no lo tienes
npm install -g sqlite3

# Ver los pedidos
sqlite3 data/orders.db "SELECT * FROM orders;"
```

## 📝 Notas Importantes

1. **Tokens Temporales**: Los tokens de acceso temporales expiran después de 24 horas. Para producción, necesitarás configurar tokens permanentes.

2. **Número de Prueba**: En modo de prueba, puedes usar el número de teléfono de prueba proporcionado por Meta. Para producción, necesitarás verificar tu número de teléfono empresarial.

3. **Webhook Público**: WhatsApp requiere que el webhook sea accesible públicamente. Para desarrollo local, usa ngrok o una herramienta similar.

4. **Seguridad**: Nunca compartas tus tokens de acceso. Mantén el archivo `.env` fuera del control de versiones (ya está en `.gitignore`).

## 🐛 Solución de Problemas

### Error: "Webhook verification failed"

- Verifica que el `WHATSAPP_VERIFY_TOKEN` en tu `.env` coincida con el configurado en Meta
- Asegúrate de que el servidor esté corriendo cuando WhatsApp intente verificar

### Error: "Access token invalid"

- Verifica que el `WHATSAPP_ACCESS_TOKEN` sea válido
- Los tokens temporales expiran después de 24 horas
- Regenera el token en el panel de Meta for Developers

### Error: "Phone number ID not found"

- Verifica que el `WHATSAPP_PHONE_NUMBER_ID` sea correcto
- Puedes encontrarlo en la sección de WhatsApp de tu aplicación en Meta

### Los mensajes no se reciben

- Verifica que el webhook esté correctamente configurado en Meta
- Asegúrate de que ngrok esté corriendo y la URL sea accesible
- Revisa los logs del servidor para ver errores

## 📚 Recursos Adicionales

- [WHATSAPP_TOKENS.md](WHATSAPP_TOKENS.md) - Explicación detallada de la diferencia entre los tokens
- [Documentación de WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Guía de ngrok](https://ngrok.com/docs)
- [Documentación de Meta for Developers](https://developers.facebook.com/docs)

