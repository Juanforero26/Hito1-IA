const Order = require('../models/order');

/**
 * Verifica el webhook de WhatsApp (para la configuración inicial)
 */
function verifyWebhook(req, res) {
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];
  
  const verifyToken = process.env.WHATSAPP_VERIFY_TOKEN;
  
  if (mode === 'subscribe' && token === verifyToken) {
    console.log('✅ Webhook verificado correctamente');
    res.status(200).send(challenge);
  } else {
    console.error('❌ Error al verificar el webhook');
    res.status(403).send('Forbidden');
  }
}

/**
 * Procesa los mensajes entrantes de WhatsApp
 */
async function handleWebhook(req, res) {
  const startTime = Date.now();
  
  try {
    // Responder inmediatamente a WhatsApp (requisito: <5 segundos)
    res.status(200).send('OK');
    
    const body = req.body;
    
    // Verificar que es un webhook válido de WhatsApp
    if (body.object === 'whatsapp_business_account') {
      const entries = body.entry || [];
      
      for (const entry of entries) {
        const changes = entry.changes || [];
        
        for (const change of changes) {
          if (change.value?.messages) {
            const messages = change.value.messages;
            
            for (const message of messages) {
              await processMessage(message, change.value);
            }
          }
        }
      }
    }
    
    const processingTime = Date.now() - startTime;
    console.log(`⏱️  Tiempo de procesamiento: ${processingTime}ms`);
    
  } catch (error) {
    console.error('❌ Error al procesar el webhook:', error);
    // Ya respondimos, así que solo registramos el error
  }
}

/**
 * Procesa un mensaje individual de WhatsApp
 */
async function processMessage(message, value) {
  try {
    // Extraer información del mensaje
    const phoneNumber = message.from; // Número del remitente
    const messageId = message.id;
    const timestamp = message.timestamp;
    const messageType = message.type;
    
    // Extraer el texto del mensaje según el tipo
    let originalText = '';
    
    if (messageType === 'text') {
      originalText = message.text?.body || '';
    } else if (messageType === 'button') {
      originalText = message.button?.text || '';
    } else {
      // Para otros tipos de mensaje (imagen, audio, etc.), usar el tipo como referencia
      originalText = `[${messageType.toUpperCase()}] - Mensaje no textual`;
    }
    
    // Convertir timestamp a fecha
    const receivedAt = new Date(parseInt(timestamp) * 1000).toISOString();
    
    // Validar que tenemos los datos necesarios
    if (!phoneNumber || !originalText) {
      console.warn('⚠️  Mensaje sin número de teléfono o texto:', message);
      return;
    }
    
    // Almacenar el pedido en la base de datos
    const order = Order.create({
      phone_number: phoneNumber,
      original_text: originalText,
      received_at: receivedAt
    });
    
    console.log(`✅ Pedido almacenado - ID: ${order.id}, Teléfono: ${phoneNumber}`);
    console.log(`📝 Texto: ${originalText.substring(0, 100)}${originalText.length > 100 ? '...' : ''}`);
    
    // Enviar confirmación de recepción
    await sendConfirmationMessage(phoneNumber, order.id);
    
  } catch (error) {
    console.error('❌ Error al procesar el mensaje:', error);
    throw error;
  }
}

/**
 * Envía un mensaje de confirmación al cliente
 */
async function sendConfirmationMessage(phoneNumber, orderId) {
  try {
    const accessToken = process.env.WHATSAPP_ACCESS_TOKEN;
    const phoneNumberId = process.env.WHATSAPP_PHONE_NUMBER_ID;
    
    if (!accessToken || !phoneNumberId) {
      console.warn('⚠️  Credenciales de WhatsApp no configuradas. Mensaje de confirmación no enviado.');
      return;
    }
    
    const message = `✅ Pedido recibido correctamente.\n\nID de pedido: #${orderId}\n\nTu pedido ha sido registrado y está siendo procesado. Te notificaremos cuando esté listo.`;
    
    const url = `https://graph.facebook.com/v18.0/${phoneNumberId}/messages`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        messaging_product: 'whatsapp',
        to: phoneNumber,
        type: 'text',
        text: {
          body: message
        }
      })
    });
    
    if (response.ok) {
      console.log(`✅ Mensaje de confirmación enviado a ${phoneNumber}`);
    } else {
      const errorText = await response.text();
      let errorData;
      try {
        errorData = JSON.parse(errorText);
      } catch (e) {
        errorData = { error: { message: errorText } };
      }
      
      // Manejar errores específicos
      if (errorData.error?.code === 131030) {
        console.error(`❌ Error al enviar confirmación: El número ${phoneNumber} no está en la lista de permitidos.`);
        console.error(`💡 Solución: Agrega el número a tu lista de permitidos en Meta for Developers.`);
        console.error(`   Ve a: WhatsApp → Getting Started → Agrega el número: ${phoneNumber}`);
        console.error(`   Más información: backend/SOLUCION_ERROR_NUMERO_PERMITIDO.md`);
      } else {
        console.error(`❌ Error al enviar confirmación: ${errorText}`);
      }
    }
    
  } catch (error) {
    console.error('❌ Error al enviar mensaje de confirmación:', error);
  }
}

module.exports = {
  verifyWebhook,
  handleWebhook,
  processMessage,
  sendConfirmationMessage
};

