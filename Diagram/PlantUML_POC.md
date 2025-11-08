@startuml
!theme plain
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true

title Sistema Multi-Agente de Procesamiento de Pedidos desde Múltiples Canales

actor Usuario as user
participant "Canal de Entrada\n(Email/WhatsApp/SMS)" as canal
participant "Orquestador" as orq
participant "Agente de\nInterpretación NLP" as nlp
participant "Agente de\nExtracción de Entidades" as extractor
participant "Agente de\nValidación de Negocio" as validador
database "Reglas de Negocio" as reglas
database "Sistema de Inventario" as inventario
participant "Agente de\nFormateo RPA" as formateador

== Recepción del Mensaje ==
user -> canal: Envía mensaje de texto libre\n"Necesito 50 cajas de producto X\npara el cliente ABC en Calle 123\npara mañana antes de las 3pm"
canal -> orq: Mensaje recibido\n+ Metadata (fuente, timestamp)
orq -> orq: Registra solicitud\nID: REQ-001

== Fase 1: Interpretación y Extracción ==
orq -> nlp: Procesar texto libre
activate nlp
nlp -> nlp: Analizar intención\n(tipo: pedido)
nlp -> nlp: Detectar idioma\ny contexto
nlp --> orq: Intención identificada:\nCrear nuevo pedido
deactivate nlp

orq -> extractor: Extraer entidades del texto
activate extractor
extractor -> extractor: Aplicar NER\n(Named Entity Recognition)
extractor -> extractor: Extraer:\n- Producto: "Producto X"\n- Cantidad: 50\n- Unidad: "cajas"\n- Cliente: "ABC"\n- Dirección: "Calle 123"\n- Fecha: "mañana"\n- Hora: "15:00"
extractor --> orq: Entidades extraídas
deactivate extractor

orq -> orq: Normalizar datos:\n- Fecha relativa → Fecha absoluta\n- Cliente → ID Cliente

== Fase 2: Validación de Reglas de Negocio ==
orq -> validador: Validar entidades extraídas
activate validador

validador -> inventario: Consultar disponibilidad\nProducto X, Cantidad: 50
activate inventario
inventario --> validador: Stock disponible: 75 unidades\nEstado: OK
deactivate inventario

validador -> reglas: Verificar ventana de entrega\nFecha: 2025-11-06, Hora: 15:00
activate reglas
reglas --> validador: Ventana válida: 08:00 - 18:00\nEstado: OK
deactivate reglas

validador -> reglas: Validar dirección de entrega\nDirección: "Calle 123"
activate reglas
reglas -> reglas: Geocodificar dirección
reglas -> reglas: Verificar zona de cobertura
reglas --> validador: Dirección válida\nZona: Norte\nEstado: OK
deactivate reglas

validador -> reglas: Calcular tiempo de entrega\nOrigen → Destino
activate reglas
reglas --> validador: Tiempo estimado: 4 horas\nCompatible con solicitud: SÍ
deactivate reglas

validador -> validador: Consolidar validaciones:\n✓ Stock disponible\n✓ Ventana de entrega OK\n✓ Dirección válida\n✓ Tiempo suficiente

validador --> orq: Validación completa:\nEstado: APROBADO\nConfianza: 95%
deactivate validador

== Fase 3: Generación de Salida Estructurada ==
orq -> formateador: Generar payload RPA
activate formateador

formateador -> formateador: Construir JSON estructurado:\n{\n  "order_id": "ORD-2025-001",\n  "source": "whatsapp",\n  "customer": {...},\n  "items": [...],\n  "delivery": {...},\n  "validations": {...}\n}

formateador --> orq: Payload RPA generado
deactivate formateador


orq -> canal: Enviar confirmación al usuario
canal -> user: "✓ Pedido confirmado\nID: ORD-2025-001\nEntrega: 06/11/2025 15:00\nProducto X: 50 cajas\nCliente ABC - Calle 123"

@enduml