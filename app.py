import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
import time

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Clasificador de Tickets ML - Fiducia",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS PERSONALIZADOS
# ============================================================================
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .tech-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .badge-mlops { background-color: #e8f4f8; color: #0066cc; }
    .badge-nlp { background-color: #fff4e6; color: #d97706; }
    .badge-sql { background-color: #f0fdf4; color: #059669; }
    .badge-docker { background-color: #eff6ff; color: #2563eb; }
    .badge-fastapi { background-color: #fef2f2; color: #dc2626; }
    
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURACIÓN DE LA API
# ============================================================================
# 🔧 CAMBIA ESTA URL POR TU URL DE RENDER
API_BASE_URL = "https://fiducia-tickets-api.onrender.com"  # ⬅️ ACTUALIZA ESTO

# ============================================================================
# HEADER Y PRESENTACIÓN
# ============================================================================
st.markdown('<h1 class="main-header">🎫 Sistema de Clasificación de Tickets ML</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Predicción automática de causas usando NLP y Machine Learning</p>', unsafe_allow_html=True)

# Badges de tecnologías
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <span class="tech-badge badge-mlops">MLOps</span>
    <span class="tech-badge badge-nlp">NLP</span>
    <span class="tech-badge badge-nlp">NLTK</span>
    <span class="tech-badge badge-sql">PostgreSQL</span>
    <span class="tech-badge badge-docker">Docker</span>
    <span class="tech-badge badge-fastapi">Flask API</span>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - INFORMACIÓN DEL PROYECTO
# ============================================================================
with st.sidebar:
    st.title("🧠")
    st.title("📊 Información del Proyecto")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Objetivo")
    st.info("""
    Sistema automatizado para clasificar tickets de soporte 
    usando Machine Learning y NLP, reduciendo tiempo de 
    categorización manual.
    """)
    
    st.markdown("### 🔧 Stack Tecnológico")
    st.markdown("""
    - **ML/NLP**: scikit-learn, NLTK
    - **API**: Flask + Gunicorn
    - **Base de Datos**: PostgreSQL
    - **Deployment**: Docker
    - **MLOps**: MLflow, Git, CI/CD
    """)
    
    st.markdown("### 📈 Métricas del Modelo")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("F1-Score", "0.92", "5%")
    with col2:
        st.metric("Accuracy", "0.94", "3%")
    
    st.markdown("---")
    
    st.markdown("### 🔗 Enlaces")
    st.markdown(f"""
    - [📡 API Health Check]({API_BASE_URL}/health)
    - [💻 Repositorio del proyecto](https://github.com/giovany-desing/fiducia_tickets_sorter)
    """)
    
    st.markdown("---")
    st.caption("Desarrollado por: Edgar Yovany Samaca Acuña")

# ============================================================================
# TABS PRINCIPALES
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 Predicción Individual", 
    "📦 Predicción en Batch", 
    "📊 Arquitectura del Sistema",
    "🧪 Test de API"
])

# ============================================================================
# TAB 1: PREDICCIÓN INDIVIDUAL
# ============================================================================
with tab1:
    st.header("🔮 Predicción Individual de Tickets")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Ingresa los datos del ticket")
        
        ticket_id = st.text_input(
            "🎫 ID del Ticket",
            value="INC1363654",
            help="Identificador único del ticket"
        )
        
        short_description = st.text_area(
            "📋 Descripción Corta",
            value="Se solicita reenviar documentos al correo del cliente",
            height=100,
            help="Descripción breve del problema reportado"
        )
        
        close_notes = st.text_area(
            "📝 Notas de Cierre",
            value="Se realiza reenvío de documentos solicitados por el cliente al correo registrado",
            height=100,
            help="Notas sobre cómo se resolvió el ticket"
        )
        
        predict_button = st.button("Clasificar ticket", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Categorías Posibles")
        st.info("""
        **0**: Davibox sin documentos
        
        **1**: Reenvío de documentos
        
        **2**: Errores generales
        """)
        
        st.markdown("### ℹ️ Información")
        st.markdown("""
        El modelo analiza:
        - Texto de descripción
        - Notas de cierre
        - Patrones lingüísticos
        - Palabras clave
        """)
    
    if predict_button:
        if not ticket_id or not short_description or not close_notes:
            st.error("⚠️ Por favor completa todos los campos")
        else:
            with st.spinner("🔄 Procesando predicción..."):
                try:
                    # Hacer petición a la API
                    payload = {
                        "ticket_id": ticket_id,
                        "short_description": short_description,
                        "close_notes": close_notes
                    }
                    
                    response = requests.post(
                        f"{API_BASE_URL}/predict",
                        json=payload,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("✅ Predicción completada exitosamente")
                        
                        # Mostrar resultados
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "🎯 Predicción",
                                result['prediction'],
                                delta=None
                            )
                        
                        with col2:
                            st.metric(
                                "📌 Causa Asignada",
                                result['causa_asignada'],
                                delta=None
                            )
                        
                        with col3:
                            bd_status = "✅ Éxito" if result['actualizacion_bd']['success'] else "❌ Error"
                            st.metric(
                                "💾 Actualización BD",
                                bd_status,
                                delta=None
                            )
                        
                        # Detalles expandibles
                        with st.expander("📊 Ver detalles completos"):
                            st.json(result)
                        
                        # Información de procesamiento
                        st.markdown("### 🔍 Análisis del Texto")
                        st.code(result['input']['processed_text'], language=None)
                        
                    else:
                        st.error(f"❌ Error en la API: {response.status_code}")
                        st.json(response.json())
                
                except requests.exceptions.ConnectionError:
                    st.error("🔌 No se pudo conectar con la API. Verifica que esté corriendo.")
                except requests.exceptions.Timeout:
                    st.warning("⏱️ La petición tomó demasiado tiempo. La API puede estar 'despertando' (Render free tier).")
                except Exception as e:
                    st.error(f"💥 Error inesperado: {str(e)}")

# ============================================================================
# TAB 2: PREDICCIÓN EN BATCH
# ============================================================================
with tab2:
    st.header("📦 Predicción en Batch (Múltiples Tickets)")
    
    st.markdown("""
    ### 📋 Opciones de carga
    Puedes cargar múltiples tickets de dos formas:
    """)
    
    option = st.radio(
        "Selecciona el método de entrada:",
        ["📝 Entrada Manual (JSON)", "📁 Cargar archivo CSV"]
    )
    
    if option == "📝 Entrada Manual (JSON)":
        st.markdown("### ✏️ Ingresa los tickets en formato JSON")
        
        default_json = json.dumps({
            "tickets": [
                {
                    "ticket_id": "BATCH_001",
                    "short_description": "Se solicita reenviar documentos",
                    "close_notes": "Se realiza reenvío de documentos"
                },
                {
                    "ticket_id": "BATCH_002",
                    "short_description": "Error al cargar davibox",
                    "close_notes": "Se soluciona problema con davibox"
                },
                {
                    "ticket_id": "BATCH_003",
                    "short_description": "Problema general con el sistema",
                    "close_notes": "Se corrige error del sistema"
                }
            ]
        }, indent=2)
        
        json_input = st.text_area(
            "JSON de tickets:",
            value=default_json,
            height=300
        )
        
        batch_button = st.button("Clasificar tickets en Batch", type="primary")
        
        if batch_button:
            try:
                tickets_data = json.loads(json_input)
                
                with st.spinner("🔄 Procesando batch de tickets..."):
                    response = requests.post(
                        f"{API_BASE_URL}/predict/batch",
                        json=tickets_data,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("✅ Batch procesado exitosamente")
                        
                        # Resumen
                        summary = result['summary']
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("📊 Total", summary['total_tickets'])
                        with col2:
                            st.metric("✅ Exitosos", summary['procesados_exitosamente'])
                        with col3:
                            st.metric("❌ Con Errores", summary['con_errores'])
                        with col4:
                            st.metric("💾 BD Actualizados", summary['actualizaciones_exitosas'])
                        
                        # Tabla de resultados
                        st.markdown("### 📋 Resultados Detallados")
                        
                        predictions_df = pd.DataFrame(result['predictions'])
                        st.dataframe(predictions_df, use_container_width=True)
                        
                        # Descargar resultados
                        csv = predictions_df.to_csv(index=False)
                        st.download_button(
                            "📥 Descargar resultados CSV",
                            csv,
                            "predicciones_batch.csv",
                            "text/csv"
                        )
                        
                        # JSON completo
                        with st.expander("🔍 Ver JSON completo"):
                            st.json(result)
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                        st.json(response.json())
            
            except json.JSONDecodeError:
                st.error("❌ JSON inválido. Verifica el formato.")
            except Exception as e:
                st.error(f"💥 Error: {str(e)}")
    
    else:  # Cargar CSV
        st.markdown("### 📁 Carga un archivo CSV")
        
        st.info("""
        **Formato esperado del CSV:**
        - `ticket_id`: ID único del ticket
        - `short_description`: Descripción corta
        - `close_notes`: Notas de cierre
        """)
        
        uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                st.markdown("### 👀 Vista previa de los datos")
                st.dataframe(df.head(), use_container_width=True)
                
                # Validar columnas
                required_cols = ['ticket_id', 'short_description', 'close_notes']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.error(f"❌ Faltan columnas: {missing_cols}")
                else:
                    process_csv_button = st.button("🚀 Procesar CSV", type="primary")
                    
                    if process_csv_button:
                        # Convertir a formato JSON
                        tickets_list = df.to_dict('records')
                        payload = {"tickets": tickets_list}
                        
                        with st.spinner(f"🔄 Procesando {len(tickets_list)} tickets..."):
                            response = requests.post(
                                f"{API_BASE_URL}/predict/batch",
                                json=payload,
                                timeout=120
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                
                                st.success("✅ Procesamiento completado")
                                
                                # Mostrar resumen igual que arriba
                                summary = result['summary']
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.metric("📊 Total", summary['total_tickets'])
                                with col2:
                                    st.metric("✅ Exitosos", summary['procesados_exitosamente'])
                                with col3:
                                    st.metric("❌ Con Errores", summary['con_errores'])
                                with col4:
                                    st.metric("💾 BD Actualizados", summary['actualizaciones_exitosas'])
                                
                                predictions_df = pd.DataFrame(result['predictions'])
                                st.dataframe(predictions_df, use_container_width=True)
                                
                                csv_result = predictions_df.to_csv(index=False)
                                st.download_button(
                                    "📥 Descargar resultados",
                                    csv_result,
                                    "resultados_predicciones.csv",
                                    "text/csv"
                                )
                            else:
                                st.error(f"❌ Error: {response.status_code}")
            
            except Exception as e:
                st.error(f"💥 Error procesando CSV: {str(e)}")

# ============================================================================
# TAB 3: ARQUITECTURA DEL SISTEMA
# ============================================================================
with tab3:
    st.header("🏗️ Arquitectura del Sistema MLOps")
    
    st.markdown("""
    ## 🎯 Pipeline End-to-End
    
    Este proyecto implementa un pipeline completo de procesamiento de texto para hace la clsificacion 
    """)
    
    # Diagrama de arquitectura (texto ASCII)
    st.code("""
    ┌─────────────────┐
    │  app de tickets │
    │(Recibe el json) │        
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Data Processing │
    │   & Cleaning    │
    │  (NLP Pipeline) │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ carga el modelo │
    │    con mlflow   │
    │  (Artifacts)    │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  Fast API       │
    │  (Endpoint de   │
    │   clasificacion)│
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │   inserta la    │
    │    Prediccion   │
    │  (Postgresql)   │
    └─────────────────┘
    """, language=None)
    
    # Componentes principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 Componentes Backend")
        st.markdown("""
        1. **Preprocessing Pipeline**
           - Limpieza de texto
           - Stemming con NLTK
           - Vectorización TF-IDF
        
        2. **Model Training**
           - Algoritmos: XGBoost
           - Tracking con MLflow
           - Cross-validation
        
        3. **API REST**
           - Flask + Gunicorn
           - Endpoints: `/predict`, `/predict/batch`
           - Health checks
        """)
    
    with col2:
        st.markdown("### 🚀 Infrastructure")
        st.markdown("""
        1. **Containerization**
           - Docker multi-stage builds
           - Optimización de imágenes
        
        2. **Database**
           - PostgreSQL para persistencia
           - Actualización automática de causas
        
        3. **Deployment**
           - Cloud Run
        """)
    
    st.markdown("---")
    
    # Flujo de predicción
    st.markdown("### 🔄 Flujo de Predicción")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Input
        - ticket_id
        - short_description
        - close_notes
        """)
    
    with col2:
        st.markdown("""
        #### 2️⃣ Processing
        - Text cleaning
        - Stemming
        - Model prediction
        """)
    
    with col3:
        st.markdown("""
        #### 3️⃣ Output
        - Categoría predicha
        - BD actualizada
        """)
    
    st.markdown("---")
    
    # Tecnologías
    st.markdown("### 💻 Stack Tecnológico Detallado")
    
    tech_df = pd.DataFrame({
        "Categoría": ["ML/NLP", "Backend", "Database", "DevOps", "Frontend", "Monitoring"],
        "Tecnologías": [
            "scikit-learn, NLTK, pandas, joblib",
            "Flask, Gunicorn, Python 3.11",
            "PostgreSQL",
            "Docker, Git",
            "App corporativa",
            "MLflow, Logging, Health Checks"
        ],
        "Propósito": [
            "Training y predicción de modelos",
            "API REST para servir predicciones",
            "Persistencia y actualización de datos",
            "Codigo reproducible en cualquier sistema operativo",
            "Interfaz web para demos",
            "Tracking de experimentos y métricas"
        ]
    })
    
    st.dataframe(tech_df, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 4: TEST DE API
# ============================================================================
with tab4:
    st.header("🧪 Pruebas de Conectividad con la API")
    
    st.markdown(f"""
    ### 🔗 URL Base de la API
    `{API_BASE_URL}`
    """)
    
    # Test de health
    if st.button("🏥 Test Health Check", type="primary"):
        with st.spinner("Conectando..."):
            try:
                response = requests.get(f"{API_BASE_URL}/health", timeout=10)
                
                if response.status_code == 200:
                    st.success("✅ API está funcionando correctamente")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error: {response.status_code}")
            
            except requests.exceptions.ConnectionError:
                st.error("🔌 No se pudo conectar. Verifica que la URL sea correcta y la API esté corriendo.")
            except requests.exceptions.Timeout:
                st.warning("⏱️ Timeout. La API puede estar 'despertando' (Render free tier tarda ~30-40s).")
            except Exception as e:
                st.error(f"💥 Error: {str(e)}")
    
    st.markdown("---")
    
    # Información de endpoints
    st.markdown("### 📡 Endpoints Disponibles")
    
    endpoints_df = pd.DataFrame({
        "Endpoint": ["/health", "/predict", "/predict/batch", "/"],
        "Método": ["GET", "POST", "POST", "GET"],
        "Descripción": [
            "Verificar estado de la API",
            "Predicción individual",
            "Predicción en lote",
            "Información general"
        ],
        "Autenticación": ["No", "No", "No", "No"]
    })
    
    st.dataframe(endpoints_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Ejemplos de cURL
    st.markdown("### 💻 Ejemplos de Uso (cURL)")
    
    st.code(f"""
# Health Check
curl {API_BASE_URL}/health

# Predicción Individual
curl -X POST {API_BASE_URL}/predict \\
  -H "Content-Type: application/json" \\
  -d '{{
    "ticket_id": "TEST001",
    "short_description": "Se solicita reenviar documentos",
    "close_notes": "Se realiza reenvío"
  }}'

# Predicción Batch
curl -X POST {API_BASE_URL}/predict/batch \\
  -H "Content-Type: application/json" \\
  -d '{{
    "tickets": [
      {{
        "ticket_id": "TEST001",
        "short_description": "Problema con documentos",
        "close_notes": "Resuelto"
      }}
    ]
  }}'
    """, language="bash")
    
    st.markdown("---")
    
    # Configuración
    st.markdown("### ⚙️ Configuración de la URL")
    
    new_url = st.text_input(
        "Actualizar URL base de la API:",
        value=API_BASE_URL,
        help="Cambia esto si desplegaste en una URL diferente"
    )
    
    if st.button("💾 Actualizar URL"):
        st.info(f"ℹ️ Para cambiar permanentemente, actualiza la variable `API_BASE_URL` en el código (línea ~70)")
        st.code(f'API_BASE_URL = "{new_url}"', language="python")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong> Sistema de Clasificación de Tickets ML</strong></p>
    <p>Desarrollado con Python, Flask, Docker, PostgreSQL</p>
    <p>MLOps • NLP • API REST • Cloud Deployment</p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">
        © 2023 - Proyecto de demostración de habilidades en Machine Learning y MLOps
    </p>
</div>
""", unsafe_allow_html=True)