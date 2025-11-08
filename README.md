# Sistema de Pedidos Institucionales - Panadería

Sistema de interpretación de texto libre para recibir pedidos institucionales de una panadería mediante WhatsApp.

## 📋 Descripción del Proyecto

Este proyecto permite recibir pedidos de clientes institucionales a través de WhatsApp en formato de texto libre, almacenarlos y procesarlos para generar un formato estandarizado que permite la conexión entre diferentes sistemas.

## 🏗️ Stack Tecnológico

- **Backend**: Node.js con Express
- **Frontend**: React (próximamente)
- **Base de Datos**: SQLite
- **API**: WhatsApp Business API

## 📦 Épica 1: MVP - Sistema de Reconocimiento y Estandarización de Pedidos

### US-001: Recibir pedido por WhatsApp

**Estado**: ✅ Implementado

#### Funcionalidades

- ✅ Recibe mensajes de WhatsApp mediante webhook
- ✅ Captura el número de teléfono del remitente
- ✅ Almacena el texto original completo
- ✅ Registra fecha y hora de recepción
- ✅ Responde confirmación de recepción en menos de 5 segundos

## 🚀 Instalación y Configuración

### Prerrequisitos

- Node.js (v16 o superior, recomendado v18+)
- npm o yarn
- Cuenta de WhatsApp Business API
- Herramienta para exponer el webhook localmente (ngrok recomendado)

### Instalación Rápida

1. **Instalar dependencias del backend**

```bash
cd backend
npm install
```

2. **Configurar variables de entorno**

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales de WhatsApp Business API.

3. **Configurar WhatsApp Business API**

Ver la guía completa en [INSTALLATION.md](backend/INSTALLATION.md)

### Configuración de WhatsApp Business API

Para una guía detallada paso a paso, consulta [backend/INSTALLATION.md](backend/INSTALLATION.md)

**Resumen rápido:**
1. Crear aplicación en [Meta for Developers](https://developers.facebook.com/)
2. Configurar WhatsApp Business API
3. Obtener credenciales (Access Token, Phone Number ID)
4. Configurar webhook con ngrok para desarrollo local

## 🏃 Ejecución

### Desarrollo

```bash
cd backend
npm run dev
```

El servidor estará corriendo en `http://localhost:3000`

### Producción

```bash
cd backend
npm start
```

## 📡 Endpoints

### GET /health
Verifica el estado del servidor

**Respuesta:**
```json
{
  "status": "ok",
  "message": "Servidor funcionando correctamente"
}
```

### GET /webhook/whatsapp
Verificación del webhook (requerido por WhatsApp)

**Query Parameters:**
- `hub.mode`: Debe ser "subscribe"
- `hub.verify_token`: Token de verificación
- `hub.challenge`: Challenge de WhatsApp

### POST /webhook/whatsapp
Recibe mensajes de WhatsApp

**Body:** Formato de webhook de WhatsApp Business API

## 🗄️ Estructura de Base de Datos

### Tabla: orders

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único del pedido |
| phone_number | TEXT | Número de teléfono del remitente |
| original_text | TEXT | Texto original del mensaje |
| received_at | DATETIME | Fecha y hora de recepción |
| created_at | DATETIME | Fecha de creación del registro |
| status | TEXT | Estado del pedido (default: 'received') |

## 📝 Ejemplo de Uso

1. El cliente envía un mensaje por WhatsApp:
   ```
   Hola, necesito 50 panes, 30 croissants y 20 donas para mañana a las 8am
   ```

2. El sistema:
   - Recibe el mensaje vía webhook
   - Almacena el pedido en la base de datos
   - Responde con confirmación en menos de 5 segundos:
     ```
     ✅ Pedido recibido correctamente.
     
     ID de pedido: #1
     
     Tu pedido ha sido registrado y está siendo procesado. Te notificaremos cuando esté listo.
     ```

## 🧪 Pruebas

### Probar el Webhook Localmente

Usa el script de prueba incluido:

```bash
cd backend
node test-webhook.js
```

Este script simula una petición de webhook de WhatsApp sin necesidad de configurar ngrok.

### Probar con WhatsApp Real

1. Usar ngrok para exponer el puerto 3000:
   ```bash
   ngrok http 3000
   ```
2. Configurar la URL de ngrok en WhatsApp Business API
3. Enviar un mensaje de prueba desde WhatsApp
4. Verificar que recibas la confirmación automática

## 📚 Próximos Pasos

- US-002: Procesamiento y extracción de información del pedido
- US-003: Validación de productos y cantidades
- US-004: Generación de formato estandarizado

## 🤝 Contribución

Este es un proyecto en desarrollo. Las contribuciones son bienvenidas.

## 📄 Licencia

ISC

