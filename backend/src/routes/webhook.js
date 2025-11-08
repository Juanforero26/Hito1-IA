const express = require('express');
const router = express.Router();
const { verifyWebhook, handleWebhook } = require('../controllers/webhookController');

// Ruta GET para verificación del webhook (requerido por WhatsApp)
router.get('/whatsapp', verifyWebhook);

// Ruta POST para recibir mensajes de WhatsApp
router.post('/whatsapp', handleWebhook);

module.exports = router;

