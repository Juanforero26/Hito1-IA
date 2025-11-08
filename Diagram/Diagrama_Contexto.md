@startuml Contexto_Sistema

!include <C4/C4_Context>

title Diagrama de Contexto - Sistema de Reconocimiento de Pedidos

Person(clienteReg, "Cliente Registrado", "Institución que realiza pedidos recurrentes")
Person(clienteNoReg, "Cliente No Registrado", "Nuevo cliente o pedido ocasional")
Person(empleado, "Empleado Panadería", "Valida y gestiona pedidos")

System(mvpSystem, "Sistema MVP\nReconocimiento y Estandarización", "Interpreta pedidos en texto libre,\nvalida reglas de negocio,\ngenera salidas estructuradas")

System_Ext(whatsapp, "WhatsApp Business API", "Canal de mensajería")
System_Ext(email, "Servidor Email", "Canal de correo")
System_Ext(sistDist, "Sistema de Distribución", "Gestión de entregas y logística")
System_Ext(notif, "Servicio Notificaciones", "Envío de confirmaciones")

Rel(clienteReg, whatsapp, "Envía pedido", "Texto libre")
Rel(clienteReg, email, "Envía pedido", "Texto libre")
Rel(clienteNoReg, whatsapp, "Envía pedido", "Texto libre")
Rel(clienteNoReg, email, "Envía pedido", "Texto libre")

Rel(whatsapp, mvpSystem, "Webhook", "JSON")
Rel(email, mvpSystem, "IMAP/API", "Email parsed")

Rel(empleado, mvpSystem, "Revisa y aprueba", "Web/App")

Rel(mvpSystem, sistDist, "Envía pedido validado", "REST API, JSON")
Rel(mvpSystem, notif, "Solicita envío", "REST API")

Rel(notif, clienteReg, "Confirmación", "WhatsApp/Email")
Rel(notif, clienteNoReg, "Confirmación", "WhatsApp/Email")

Rel(sistDist, mvpSystem, "Estado actualizado", "Webhook")

note right of mvpSystem
  **Componentes Core:**
  - Motor NLP/LLM
  - Motor de validación
  - Gestor de reglas
  - API REST
  - Dashboard web
end note

@enduml