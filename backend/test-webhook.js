/**
 * Script de prueba para verificar el webhook de WhatsApp
 * Este script simula una petición de webhook de WhatsApp para pruebas
 */

const http = require('http');

// Configuración
const PORT = process.env.PORT || 3000;
const HOST = 'localhost';

// Datos de prueba simulando un webhook de WhatsApp
const testWebhookData = {
  object: 'whatsapp_business_account',
  entry: [
    {
      id: 'WHATSAPP_BUSINESS_ACCOUNT_ID',
      changes: [
        {
          value: {
            messaging_product: 'whatsapp',
            metadata: {
              display_phone_number: '1234567890',
              phone_number_id: 'PHONE_NUMBER_ID'
            },
            contacts: [
              {
                profile: {
                  name: 'Cliente de Prueba'
                },
                wa_id: '573182217109'
              }
            ],
            messages: [
              {
                from: '573182217109',
                id: 'wamid.test123',
                timestamp: Math.floor(Date.now() / 1000).toString(),
                type: 'text',
                text: {
                  body: 'Hola, necesito 50 panes, 30 croissants y 20 donas para mañana a las 8am'
                }
              }
            ]
          },
          field: 'messages'
        }
      ]
    }
  ]
};

// Función para enviar la petición de prueba
function testWebhook() {
  const postData = JSON.stringify(testWebhookData);

  const options = {
    hostname: HOST,
    port: PORT,
    path: '/webhook/whatsapp',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData)
    }
  };

  const req = http.request(options, (res) => {
    console.log(`\n📡 Estado de respuesta: ${res.statusCode}`);
    console.log(`📋 Headers:`, res.headers);

    let data = '';

    res.on('data', (chunk) => {
      data += chunk;
    });

    res.on('end', () => {
      console.log(`\n✅ Respuesta del servidor:`, data || '(sin cuerpo)');
      console.log('\n✨ Prueba completada. Verifica los logs del servidor para más detalles.\n');
    });
  });

  req.on('error', (error) => {
    console.error(`\n❌ Error al enviar la petición:`, error.message);
    console.log('\n💡 Asegúrate de que el servidor esté corriendo en el puerto', PORT);
    console.log('   Ejecuta: npm run dev\n');
  });

  req.write(postData);
  req.end();
}

// Ejecutar la prueba
console.log('🧪 Iniciando prueba del webhook de WhatsApp...');
console.log(`📍 Enviando petición a http://${HOST}:${PORT}/webhook/whatsapp`);
console.log(`📝 Mensaje de prueba: "${testWebhookData.entry[0].changes[0].value.messages[0].text.body}"\n`);

testWebhook();

