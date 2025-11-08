@startuml Componentes_Interpretacion

!include <C4/C4_Component>

title Componentes - Servicio de Interpretación

Container_Boundary(interpretacion, "Servicio de Interpretación") {
    
    Component(api_endpoint, "API Endpoints", "FastAPI", "Expone endpoints REST para interpretación")
    
    Component(preprocessor, "Preprocesador de Texto", "Python", "Limpia y normaliza texto de entrada")
    
    Component(entity_extractor, "Extractor de Entidades", "Python/spaCy/LLM", "Identifica productos, cantidades, fechas")
    
    Component(product_matcher, "Matcher de Productos", "Python", "Busca coincidencias en catálogo")
    
    Component(quantity_parser, "Parser de Cantidades", "Python", "Interpreta números y unidades")
    
    Component(date_parser, "Parser de Fechas", "Python/dateparser", "Interpreta expresiones temporales")
    
    Component(confidence_calculator, "Calculador de Confianza", "Python", "Asigna nivel de confianza a cada entidad")
    
    Component(llm_client, "Cliente LLM", "Python/OpenAI SDK", "Interfaz con API de LLM")
    
    Component(result_builder, "Constructor de Resultados", "Python", "Ensambla JSON estructurado")
}

ComponentDb(products_cache, "Cache de Productos", "Redis", "Productos frecuentes")
ComponentDb(ml_models, "Modelos ML", "Filesystem/S3", "Modelos entrenados de NLP")

System_Ext(llm_api, "API LLM", "GPT-4/Claude")
System_Ext(normalization_svc, "Servicio Normalización")

' Flujo principal
Rel(api_endpoint, preprocessor, "1. Recibe texto", "JSON")
Rel(preprocessor, entity_extractor, "2. Texto limpio", "String")
Rel(entity_extractor, llm_client, "3. Solicita análisis", "Prompt")
Rel(llm_client, llm_api, "API Call", "HTTPS")

Rel(entity_extractor, product_matcher, "4a. Productos extraídos", "List")
Rel(entity_extractor, quantity_parser, "4b. Cantidades extraídas", "List")
Rel(entity_extractor, date_parser, "4c. Fechas extraídas", "List")

Rel(product_matcher, products_cache, "Lee", "Redis")
Rel(product_matcher, normalization_svc, "Normaliza", "HTTP")

Rel(quantity_parser, confidence_calculator, "Resultado", "Entity")
Rel(date_parser, confidence_calculator, "Resultado", "Entity")
Rel(product_matcher, confidence_calculator, "Resultado", "Entity")

Rel(confidence_calculator, result_builder, "Entidades + confianza", "Dict")
Rel(result_builder, api_endpoint, "JSON estructurado", "Response")

Rel(entity_extractor, ml_models, "Carga modelos", "File I/O")

note right of entity_extractor
  **Estrategia Híbrida:**
  1. Prompt engineering a LLM
  2. Named Entity Recognition (spaCy)
  3. Regex patterns para casos comunes
  4. Combinar resultados
end note

note bottom of confidence_calculator
  **Factores de confianza:**
  - Coincidencia exacta vs fuzzy
  - Contexto de oración
  - Coherencia con otros fields
  - Score del LLM
  --
  Formula: weighted average
  de factores individuales
end note

@enduml