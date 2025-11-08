from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda, ECS
from diagrams.aws.integration import SNS, SQS, Eventbridge, StepFunctions
from diagrams.aws.ml import Comprehend, SagemakerModel
from diagrams.aws.database import DynamoDB, RDS
from diagrams.aws.network import APIGateway
from diagrams.aws.management import Cloudwatch
from diagrams.aws.mobile import APIGateway as MobileAPI
from diagrams.onprem.client import Users
from diagrams.saas.communication import Slack, Twilio
from diagrams.programming.framework import FastAPI

# Configuración del diagrama
graph_attr = {
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5",
    "splines": "ortho"
}

with Diagram("Sistema Multi-Agente de Procesamiento de Pedidos - AWS", 
             show=False, 
             direction="LR",
             graph_attr=graph_attr):
    
    # Usuarios y canales de entrada
    usuario = Users("Usuario")
    
    with Cluster("Canales de Entrada"):
        email = Slack("Email\n(SES)")
        whatsapp = Twilio("WhatsApp\n(Twilio)")
        sms = Twilio("SMS\n(SNS)")
    
    # API Gateway como punto de entrada
    api_gateway = APIGateway("API Gateway\n(Entrada)")
    
    with Cluster("Capa de Orquestación"):
        orquestador = StepFunctions("Step Functions\n(Orquestador)")
        event_bus = Eventbridge("EventBridge\n(Event Bus)")
        cola_mensajes = SQS("SQS Queue\n(Buffer)")
    
    with Cluster("Agentes de Procesamiento"):
        
        with Cluster("1. Interpretación NLP"):
            agente_nlp = Lambda("Lambda\nNLP Agent")
            comprehend = Comprehend("Amazon\nComprehend")
            bedrock_nlp = SagemakerModel("Bedrock/\nSageMaker\n(LLM)")
        
        with Cluster("2. Extracción de Entidades"):
            agente_extractor = Lambda("Lambda\nEntity Extractor")
            ner_model = SagemakerModel("SageMaker\n(NER Model)")
        
        with Cluster("3. Validación de Negocio"):
            agente_validador = Lambda("Lambda\nValidator")
        
        with Cluster("4. Formateo RPA"):
            agente_formateador = Lambda("Lambda\nRPA Formatter")
    
    with Cluster("Bases de Datos y Reglas"):
        dynamodb_reglas = DynamoDB("DynamoDB\nReglas de Negocio")
        rds_inventario = RDS("RDS/Aurora\nInventario")
        dynamodb_pedidos = DynamoDB("DynamoDB\nPedidos")
    
    with Cluster("Sistema RPA / Integración"):
        rpa_endpoint = APIGateway("API Gateway\n(Salida RPA)")
        ecs_rpa = ECS("ECS/Fargate\nSistema RPA")
    
    # Monitoreo
    monitoring = Cloudwatch("CloudWatch\n(Logs/Metrics)")
    
    # Flujo de datos - Entrada
    usuario >> Edge(label="envía mensaje") >> [email, whatsapp, sms]
    [email, whatsapp, sms] >> Edge(label="webhook") >> api_gateway
    api_gateway >> Edge(label="mensaje +\nmetadata") >> cola_mensajes
    
    # Orquestación
    cola_mensajes >> Edge(label="trigger") >> orquestador
    orquestador >> Edge(label="eventos") >> event_bus
    
    # Fase 1: Interpretación
    event_bus >> Edge(label="1. procesar\ntexto") >> agente_nlp
    agente_nlp >> Edge(label="analizar") >> comprehend
    agente_nlp >> Edge(label="LLM") >> bedrock_nlp
    agente_nlp >> Edge(label="intención") >> orquestador
    
    # Fase 2: Extracción
    orquestador >> Edge(label="2. extraer\nentidades") >> agente_extractor
    agente_extractor >> Edge(label="NER") >> ner_model
    agente_extractor >> Edge(label="entidades\nextraídas") >> orquestador
    
    # Fase 3: Validación
    orquestador >> Edge(label="3. validar") >> agente_validador
    agente_validador >> Edge(label="reglas") >> dynamodb_reglas
    agente_validador >> Edge(label="stock") >> rds_inventario
    agente_validador >> Edge(label="resultado\nvalidación") >> orquestador
    
    # Fase 4: Formateo
    orquestador >> Edge(label="4. formatear") >> agente_formateador
    agente_formateador >> Edge(label="guardar\npedido") >> dynamodb_pedidos
    agente_formateador >> Edge(label="payload\nRPA") >> orquestador
    
    # Salida a RPA
    orquestador >> Edge(label="orden\nestructurada") >> rpa_endpoint
    rpa_endpoint >> Edge(label="procesar") >> ecs_rpa
    
    # Confirmación al usuario
    ecs_rpa >> Edge(label="confirmación", style="dashed") >> api_gateway
    api_gateway >> Edge(label="notificación", style="dashed") >> [email, whatsapp, sms]
    [email, whatsapp, sms] >> Edge(label="mensaje", style="dashed") >> usuario
    
    # Monitoreo (conexiones implícitas)
    [agente_nlp, agente_extractor, agente_validador, agente_formateador] >> Edge(style="dotted", color="gray") >> monitoring
    orquestador >> Edge(style="dotted", color="gray") >> monitoring