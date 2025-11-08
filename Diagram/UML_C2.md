@startuml Arquitectura_Contenedores

!include <C4/C4_Container>

LAYOUT_WITH_LEGEND()

title Arquitectura de Contenedores - Sistema de Reconocimiento de Pedidos

Person(cliente, "Cliente Institucional", "Envía pedidos por diferentes canales")
Person(empleado, "Empleado Panadería", "Revisa y gestiona pedidos")

System_Boundary(mvp_system, "Sistema MVP") {
    
    Container(web_app, "Dashboard Web", "React/Next.js", "Interfaz para empleados. Revisión, aprobación y gestión de pedidos")
    
    Container(api_gateway, "API Gateway", "Node.js/Express", "Punto de entrada único. Autenticación, rate limiting, routing")
    
    Container(interpretacion_service, "Servicio de Interpretación", "Python/FastAPI", "Motor NLP/LLM para extraer entidades del texto libre")
    
    Container(validacion_service, "Servicio de Validación", "Node.js/TypeScript", "Aplica reglas de negocio, valida stock y ventanas de entrega")
    
    Container(normalizacion_service, "Servicio de Normalización", "Python", "Normaliza productos usando catálogo y fuzzy matching")
    
    Container(pedido_service, "Servicio de Pedidos", "Node.js/TypeScript", "Gestión del ciclo de vida de pedidos. CRUD y orquestación")
    
    Container(notificacion_service, "Servicio de Notificaciones", "Node.js", "Envío de confirmaciones y alertas")
    
    ContainerDb(main_db, "Base de Datos Principal", "PostgreSQL", "Almacena Pedidos, ItemPedido, Productos")
    
    ContainerDb(cache, "Cache", "Redis", "Cache de productos frecuentes, sesiones, rate limiting")
    
    Container(message_queue, "Cola de Mensajes", "RabbitMQ/SQS", "Procesamiento asíncrono de pedidos")
    
    Container(webhook_handler, "Manejador de Webhooks", "Node.js", "Recibe pedidos de WhatsApp y otros canales")
}

System_Ext(whatsapp_api, "WhatsApp Business API", "Canal de comunicación")
System_Ext(email_service, "Servicio Email", "SMTP/IMAP")
System_Ext(llm_provider, "Proveedor LLM", "OpenAI/Anthropic API")
System_Ext(sistema_distribucion, "Sistema de Distribución", "Sistema externo de logística")

' Relaciones Cliente
Rel(cliente, whatsapp_api, "Envía pedido", "Texto libre")
Rel(cliente, email_service, "Envía pedido", "Email")

' Relaciones Empleado
Rel(empleado, web_app, "Gestiona pedidos", "HTTPS")

' Relaciones Webhooks
Rel(whatsapp_api, webhook_handler, "Webhook", "HTTPS/JSON")
Rel(email_service, webhook_handler, "IMAP/Webhook", "JSON")

' Relaciones internas
Rel(webhook_handler, message_queue, "Publica mensaje", "AMQP")
Rel(message_queue, interpretacion_service, "Consume mensaje", "AMQP")

Rel(web_app, api_gateway, "Llamadas API", "HTTPS/REST")
Rel(api_gateway, pedido_service, "Enruta", "HTTP/gRPC")
Rel(api_gateway, validacion_service, "Enruta", "HTTP")

Rel(interpretacion_service, llm_provider, "Solicita análisis", "HTTPS/API")
Rel(interpretacion_service, normalizacion_service, "Normaliza productos", "HTTP")
Rel(interpretacion_service, pedido_service, "Crea pedido", "HTTP/Event")

Rel(normalizacion_service, main_db, "Lee catálogo", "SQL")
Rel(normalizacion_service, cache, "Cache productos", "Redis Protocol")

Rel(pedido_service, main_db, "Lee/Escribe", "SQL")
Rel(pedido_service, validacion_service, "Valida pedido", "HTTP")
Rel(pedido_service, notificacion_service, "Envía notificación", "Event/HTTP")

Rel(validacion_service, main_db, "Lee productos/stock", "SQL")
Rel(validacion_service, cache, "Cache reglas", "Redis Protocol")

Rel(notificacion_service, whatsapp_api, "Envía confirmación", "HTTPS/API")
Rel(notificacion_service, email_service, "Envía email", "SMTP")

Rel(pedido_service, sistema_distribucion, "Envía pedido aprobado", "REST API")

note right of interpretacion_service
  **Responsabilidades:**
  - Recibir texto libre
  - Extraer entidades (NLP/LLM)
  - Calcular confianza
  - Generar estructura JSON
end note

note right of validacion_service
  **Validaciones:**
  - Stock disponible
  - Ventana de entrega válida
  - Cantidades dentro de rango
  - Cliente autorizado
end note

note right of normalizacion_service
  **Técnicas:**
  - Fuzzy string matching
  - Búsqueda por sinónimos
  - Corrección ortográfica
  - Mapeo a catálogo
end note

@enduml