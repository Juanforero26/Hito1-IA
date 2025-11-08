const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const DB_PATH = process.env.DB_PATH || path.join(__dirname, '../../data/orders.db');

// Asegurar que el directorio data existe
const dataDir = path.dirname(DB_PATH);
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

let db = null;

function initializeDatabase() {
  try {
    db = new Database(DB_PATH);
    
    // Crear tabla de pedidos
    db.exec(`
      CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT NOT NULL,
        original_text TEXT NOT NULL,
        received_at DATETIME NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'received'
      );
      
      CREATE INDEX IF NOT EXISTS idx_phone_number ON orders(phone_number);
      CREATE INDEX IF NOT EXISTS idx_received_at ON orders(received_at);
    `);
    
    console.log('✅ Base de datos inicializada correctamente');
    return db;
  } catch (error) {
    console.error('❌ Error al inicializar la base de datos:', error);
    throw error;
  }
}

function getDatabase() {
  if (!db) {
    db = initializeDatabase();
  }
  return db;
}

module.exports = {
  initializeDatabase,
  getDatabase
};

