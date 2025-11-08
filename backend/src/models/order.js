const { getDatabase } = require('../config/database');

class Order {
  static create(orderData) {
    const db = getDatabase();
    const { phone_number, original_text, received_at } = orderData;
    
    const stmt = db.prepare(`
      INSERT INTO orders (phone_number, original_text, received_at, status)
      VALUES (?, ?, ?, 'received')
    `);
    
    const result = stmt.run(phone_number, original_text, received_at);
    
    return {
      id: result.lastInsertRowid,
      phone_number,
      original_text,
      received_at,
      status: 'received'
    };
  }
  
  static findById(id) {
    const db = getDatabase();
    const stmt = db.prepare('SELECT * FROM orders WHERE id = ?');
    return stmt.get(id);
  }
  
  static findByPhoneNumber(phoneNumber) {
    const db = getDatabase();
    const stmt = db.prepare('SELECT * FROM orders WHERE phone_number = ? ORDER BY received_at DESC');
    return stmt.all(phoneNumber);
  }
  
  static findAll(limit = 100) {
    const db = getDatabase();
    const stmt = db.prepare('SELECT * FROM orders ORDER BY received_at DESC LIMIT ?');
    return stmt.all(limit);
  }
}

module.exports = Order;

