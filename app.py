import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Ticket Classifier ML - Documentación",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar colapsado
)

# ============================================================================
# ESTILOS PREMIUM
# ============================================================================
st.markdown("""
    <style>
    /* ========== GLOBAL ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* ========== OCULTAR SIDEBAR COMPLETAMENTE ========== */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    /* ========== HEADERS ========== */
    .premium-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 3rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2);
    }
    
    .premium-header h1 {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .premium-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.25rem;
        text-align: center;
        margin: 1rem 0 0 0;
    }
    
    /* ========== BADGES ========== */
    .tech-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        background: white;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .tech-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .badge-python { color: #3776ab; border: 2px solid #3776ab; }
    .badge-ml { color: #ff6f00; border: 2px solid #ff6f00; }
    .badge-nlp { color: #00897b; border: 2px solid #00897b; }
    .badge-api { color: #d32f2f; border: 2px solid #d32f2f; }
    .badge-docker { color: #2496ed; border: 2px solid #2496ed; }
    .badge-db { color: #336791; border: 2px solid #336791; }
    
    /* ========== CARDS PREMIUM ========== */
    .premium-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin: 1.5rem 0;
        border: 1px solid #e5e7eb;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .premium-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .premium-card h3 {
        color: #1e293b;
        font-weight: 600;
        margin-top: 0;
        font-size: 1.5rem;
    }
    
    .premium-card p {
        color: #475569;
        line-height: 1.6;
        margin-bottom: 0;
    }
    
    /* ========== INFO BOXES ========== */
    .info-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #0284c7;
        margin: 1rem 0;
    }
    
    .info-box h4 {
        color: #0c4a6e;
        margin-top: 0;
        font-weight: 600;
    }
    
    .info-box p, .info-box ul {
        color: #075985;
        margin-bottom: 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #059669;
        margin: 1rem 0;
    }
    
    .success-box h4 {
        color: #065f46;
        margin-top: 0;
        font-weight: 600;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }
    
    .warning-box h4 {
        color: #92400e;
        margin-top: 0;
        font-weight: 600;
    }
    
    /* ========== CODE BLOCKS ========== */
    .stCodeBlock {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        font-family: 'Fira Code', monospace !important;
    }
    
    code {
        background: #f1f5f9;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Fira Code', monospace;
        font-size: 0.875rem;
        color: #dc2626;
    }
    
    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* ========== METRICS ========== */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 500;
    }
    
    /* ========== BUTTONS ========== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.3);
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* ========== DATAFRAMES ========== */
    .dataframe {
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
        color: #1e293b !important;
        font-weight: 600 !important;
        padding: 1rem !important;
    }
    
    .dataframe td {
        padding: 0.75rem !important;
        color: #475569 !important;
    }
    
    /* ========== EXPANDERS ========== */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 8px;
        font-weight: 600;
        color: #1e293b;
    }
    
    /* ========== INPUTS ========== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* ========== SECTION HEADERS ========== */
    h1 {
        color: #0f172a;
        font-weight: 700;
        margin-top: 2rem;
    }
    
    h2 {
        color: #1e293b;
        font-weight: 600;
        margin-top: 2rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
    }
    
    h3 {
        color: #334155;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    p {
        color: #475569;
        line-height: 1.7;
    }
    
    /* ========== ENDPOINT CARDS ========== */
    .endpoint-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: border-color 0.2s;
    }
    
    .endpoint-card:hover {
        border-color: #667eea;
    }
    
    .endpoint-method {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.875rem;
        margin-right: 1rem;
    }
    
    .method-get {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .method-post {
        background: #d1fae5;
        color: #065f46;
    }
    
    .endpoint-path {
        font-family: 'Fira Code', monospace;
        color: #64748b;
        font-size: 1.1rem;
    }
    
    /* ========== FOOTER ========== */
    .premium-footer {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-top: 4rem;
        text-align: center;
    }
    
    .premium-footer h4 {
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .premium-footer p {
        color: #cbd5e1;
    }
    
    .premium-footer a {
        color: #60a5fa;
        text-decoration: none;
        font-weight: 600;
        margin: 0 1rem;
    }
    
    .premium-footer a:hover {
        color: #93c5fd;
    }
    
    /* ========== CATEGORY SECTION ========== */
    .tech-category {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .tech-category h3 {
        color: #1e293b;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURACIÓN DE LA API
# ============================================================================
API_BASE_URL = "https://fiducia-tickets-api.onrender.com"

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class="premium-header">
    <h1>🎯 Clasificador de tickets</h1>
    <p>API en Fast Api para la clasificar</p>
</div>
""", unsafe_allow_html=True)



# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📖 Overview",
    "🧠 Pipeline de entrenamiento", 
    "🔢 Pipeline clasificación",
    "🤖 Pipeline de reentrenamiento y deploy",
    "🖇️ Orquestación con Airflow",
    "🎯 Endpoints"
])

# ============================================================================
# TAB 1: OVERVIEW
# ============================================================================
with tab1:
    st.markdown("<h2 style='color: black;'>🎯 Descripción del Proyecto</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        Identifiqué un cuello de botella crítico en la generación de informes ejecutivos para la Fiducia de Davivienda, donde la clasificación manual de más de 300 tickets mensuales consumía tiempo valioso y era propensa a errores.
    """)
    st.markdown("""
        Para solucionarlo, desarrollé una arquitectura End-to-End personalizada: creé un algoritmo que clasifica automáticamente cada caso según su tipología, envía los datos a una base de datos PostgreSQL y alimenta un dashboard en Power BI. Transformé un proceso manual operativo en una solución de inteligencia de negocios automatizada, este desarrollo también fue aplicado a diferentes clientes de la organización, optimizando la construcción de informes mensuales de soporte técnico.
    """)
    st.markdown("""
        Este sistema lo diseñe para que en caso de detectar un cambio en los datos de entrada como el vocabulario, la longitud de los datos y predicciones erradas se haga un reentrenamiento y así mismo el deploy todo de manera automática y orquestada con el flujo de predicción.
    """)
    
    
    # Problem vs Solution

    st.markdown("<h2 style='color: black;'>💡 Problema y Solución</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="warning-box" style="color: black;">
            <h4>🔴 Situación Actual</h4>
            <ul>
                <li><strong>Manual</strong>: Categorización por humanos</li>
                <li><strong>Lento</strong>: 2-3 minutos por ticket</li>
                <li><strong>Inconsistente</strong>: Errores humanos</li>
                <li><strong>Costoso</strong>: Alto costo operativo</li>
                <li><strong>No escalable</strong>: Limitado por personal</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="success-box" style="color: black;">
            <h4>🟢 Con ML Automation</h4>
            <ul>
                <li><strong>Automático</strong>: Clasificación por ML</li>
                <li><strong>Rápido</strong>: &lt;1 segundo por ticket</li>
                <li><strong>Consistente</strong>: 94% de accuracy</li>
                <li><strong>Económico</strong>: ROI en 3 meses</li>
                <li><strong>Escalable</strong>: Millones de tickets/día</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    
    # Tech Stack Detallado
    st.markdown("<h2 style='color: black;'>🛠️ Stack Tecnológico Completo</h2>", unsafe_allow_html=True)
    
    # Machine Learning y Data Science
    st.markdown("""
    <div class="tech-category">
        <h3>🤖 Machine Learning y Data Science</h3>
    </div>
    """, unsafe_allow_html=True)
    
    ml_df = pd.DataFrame({
        "Tecnología": ["Python", "pandas", "numpy", "scikit-learn", "XGBoost", "LightGBM", "Optuna", "NLTK", "joblib"],
        "Versión": ["3.9", "2.x", "1.x", "1.x", "2.x", "4.x", "3.x", "3.x", "1.x"],
        "Propósito": [
            "Lenguaje base",
            "Manipulación de datos",
            "Operaciones numéricas",
            "Modelos ML, pipelines, métricas",
            "Gradient boosting (alta precisión)",
            "Gradient boosting (rápido)",
            "Optimización de hiperparámetros",
            "Procesamiento de texto (NLP)",
            "Serialización de modelos"
        ]
    })
    
    st.dataframe(ml_df, use_container_width=True, hide_index=True)
    
    # API y Web
    st.markdown("""
    <div class="tech-category">
        <h3>🌐 API y Web</h3>
    </div>
    """, unsafe_allow_html=True)
    
    api_df = pd.DataFrame({
        "Tecnología": ["FastAPI", "Uvicorn", "Pydantic", "slowapi"],
        "Propósito": [
            "Framework web async (alta performance)",
            "Servidor ASGI para FastAPI",
            "Validación de datos y schemas",
            "Rate limiting para APIs"
        ]
    })
    
    st.dataframe(api_df, use_container_width=True, hide_index=True)
    
    # Almacenamiento y Bases de Datos
    st.markdown("""
    <div class="tech-category">
        <h3>🗄️ Almacenamiento y Bases de Datos</h3>
    </div>
    """, unsafe_allow_html=True)
    
    storage_df = pd.DataFrame({
        "Tecnología": ["Supabase", "AWS S3", "DVC", "MLflow"],
        "Propósito": [
            "Base de datos PostgreSQL (tickets)",
            "Almacenamiento de modelos y datasets",
            "Versionado de modelos y datos grandes",
            "Tracking de experimentos ML"
        ]
    })
    
    st.dataframe(storage_df, use_container_width=True, hide_index=True)
    
    # Orquestación y CI/CD
    st.markdown("""
    <div class="tech-category">
        <h3>⚙️ Orquestación y CI/CD</h3>
    </div>
    """, unsafe_allow_html=True)
    
    cicd_df = pd.DataFrame({
        "Tecnología": ["GitHub Actions", "Apache Airflow", "Docker", "Render.com"],
        "Propósito": [
            "CI/CD automatizado",
            "Orquestación de pipelines ML",
            "Contenedorización",
            "Hosting de la API"
        ]
    })
    
    st.dataframe(cicd_df, use_container_width=True, hide_index=True)
    
    # Testing y Calidad
    st.markdown("""
    <div class="tech-category">
        <h3>🧪 Testing y Calidad</h3>
    </div>
    """, unsafe_allow_html=True)
    
    testing_df = pd.DataFrame({
        "Tecnología": ["pytest", "pytest-cov", "pytest-mock"],
        "Propósito": [
            "Framework de testing",
            "Cobertura de código",
            "Mocking para tests"
        ]
    })
    
    st.dataframe(testing_df, use_container_width=True, hide_index=True)
    
    st.markdown("<h2 style='color: black;'>Distribución de archivos del proyecto</h2>", unsafe_allow_html=True)
    
    # github
    st.markdown("""
    <div class="hero-section">
        <div class="hero-cta">
            <a href="https://github.com/giovany-desing/Proyecto_tickets_fiduciaria" target="_blank" class="apple-button">
                Ver Código en GitHub
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Architecture Diagram
    st.markdown("""
    """, unsafe_allow_html=True)
    
    st.code("""
ticket-classifier-mlops/
  │
  ├── 📄 README.md                           Documentación principal del proyecto
  ├── 📄 SETUP.md                            Guía de configuración e instalación
  ├── 📄 .gitignore                          Archivos excluidos de Git
  ├── 📄 requirements.txt                    Dependencias Python del proyecto
  ├── 📄 requirements-lock.txt               Versiones exactas de dependencias
  ├── 📄 config.yaml                         Configuración centralizada del sistema
  │                                          (rutas, params ML, thresholds)
  │
  ├── 📁 .github/                            ══════════════════════════════════
  │   └── workflows/                         Automatización CI/CD
  │       ├── ci_cd_pipeline.yml            Pipeline principal: validate + deploy
  │       ├── deploy_render.yml             Deploy manual a Render
  │       ├── train_model.yml               Workflow de entrenamiento automático
  │       └── monitor_and_retrain.yml       Monitoreo y reentrenamiento scheduled
  │
  ├── 📁 api/                                ══════════════════════════════════
  │   └── inference.py                       API FastAPI principal
  │                                          • 17 endpoints (predict, monitor, admin)
  │                                          • Rate limiting con slowapi
  │                                          • Integración con Supabase
  │                                          • Hot reload de modelos
  │                                          • Logging de predicciones
  │
  ├── 📁 scripts/                            ══════════════════════════════════
  │   │                                      Scripts ejecutables del pipeline
  │   │
  │   ├── train_model.py                     Entrenamiento multi-modelo
  │   │                                      • 7 algoritmos (LR, RF, XGB, etc.)
  │   │                                      • Optimización con Optuna (50 trials)
  │   │                                      • Evaluación y selección del mejor
  │   │                                      • Guarda modelo + metadata
  │   │
  │   ├── monitor_and_retrain.py             Monitoreo continuo + reentrenamiento
  │   │                                      • Detecta drift (KS, Chi-square)
  │   │                                      • Evalúa degradación de performance
  │   │                                      • Dispara reentrenamiento si necesario
  │   │                                      • Integra con sistema de notificaciones
  │   │
  │   ├── deploy_model.py                    Deploy automatizado
  │   │                                      • Git commit del nuevo modelo
  │   │                                      • Git push (dispara CI/CD)
  │   │                                      • DVC push a S3
  │   │                                      • Opcional: trigger Render deploy
  │   │
  │   └── download_model.py                  Descarga modelo desde S3
  │                                          • Lee hash de archivo .dvc
  │                                          • Descarga desde S3 usando boto3
  │                                          • Usado en startup de API
  │
  ├── 📁 utils/                              ══════════════════════════════════
  │   │                                      Utilidades y módulos compartidos
  │   │
  │   ├── preprocessing_data.py              Preprocesamiento de texto (NLP)
  │   │                                      • Limpieza de texto
  │   │                                      • Tokenización (NLTK)
  │   │                                      • Stopwords removal (español)
  │   │                                      • Stemming (SnowballStemmer)
  │   │                                      • Carga de configuración
  │   │
  │   ├── monitoring.py                      Sistema de monitoreo del modelo
  │   │                                      • PredictionLogger: log a predictions.jsonl
  │   │                                      • DriftDetector: KS test, Chi-square
  │   │                                      • Vocabulary growth analysis
  │   │                                      • Métricas diarias agregadas
  │   │
  │   ├── database.py                        Conexión y operaciones con Supabase
  │   │                                      • Cliente PostgreSQL (supabase-py)
  │   │                                      • update_ticket_causa() con retry logic
  │   │                                      • Exponential backoff (4 reintentos)
  │   │                                      • Batch updates
  │   │                                      • Queries de tickets pendientes
  │   │
  │   ├── database_example.py                Ejemplos de uso de database.py
  │   │                                      • Scripts de demostración
  │   │                                      • Casos de uso comunes
  │   │
  │   └── notifications.py                   Sistema de notificaciones
  │                                          • Slack, Discord, Telegram
  │                                          • Notifica: training, drift, deploy
  │                                          • Niveles: INFO, WARNING, ERROR
  │
  ├── 📁 models/                             ══════════════════════════════════
  │   │                                      Modelos entrenados (versionados con DVC)
  │   │
  │   ├── best_model.pkl                     Modelo serializado (joblib)
  │   │                                      Algoritmo con mejor F1-Score
  │   │
  │   ├── best_model.pkl.dvc                 Puntero DVC al modelo en S3
  │   │                                      Contiene hash MD5 único
  │   │
  │   ├── best_model_metadata.json           Metadata del modelo actual
  │   │                                      • model_name: "XGBoost"
  │   │                                      • f1_score: 0.88
  │   │                                      • training_date, hyperparameters
  │   │
  │   ├── vectorizer.pkl                     TF-IDF vectorizer entrenado
  │   │                                      5000 features, ngram_range=(1,2)
  │   │
  │   ├── label_encoder.pkl                  Encoder de categorías
  │   │                                      Mapeo: "TI" → 0, "RRHH" → 1, etc.
  │   │
  │   └── backups/                           Backups automáticos de modelos
  │       ├── best_model_backup_*.pkl        Modelo anterior (rollback)
  │       └── best_model_metadata_backup_*.json  Metadata backup
  │
  ├── 📁 data/                               ══════════════════════════════════
  │   └── raw/                               Datos crudos
  │       └── tickets.csv                    Dataset de tickets etiquetados
  │           (versionado con DVC)           Columnas: short_description,
  │                                          close_notes, etiqueta
  │
  ├── 📁 monitoring/                         ══════════════════════════════════
  │   └── logs/                              Logs de producción
  │       ├── predictions.jsonl              Log de todas las predicciones
  │       │                                  • timestamp, text, prediction
  │       │                                  • probability, true_label
  │       │                                  • Usado para detectar drift
  │       │
  │       └── daily_metrics/                 Métricas agregadas por día
  │           └── metrics_YYYY-MM-DD.json    • total_predictions
  │                                          • average_confidence
  │                                          • distribution por clase
  │
  ├── 📁 airflow/                            ══════════════════════════════════
  │   │                                      Orquestación con Apache Airflow
  │   │
  │   ├── docker-compose.yml                 Configuración Docker Compose
  │   │                                      • Airflow webserver, scheduler
  │   │                                      • PostgreSQL (metadata)
  │   │                                      • Redis (Celery executor)
  │   │
  │   ├── Dockerfile                         Imagen Docker custom de Airflow
  │   │                                      Incluye dependencias del proyecto
  │   │
  │   ├── requirements.txt                   Dependencias específicas de Airflow
  │   │
  │   ├── README.md                          Guía de configuración de Airflow
  │   │
  │   ├── test_dag.py                        DAG de prueba/ejemplo
  │   │
  │   └── dags/                              Definiciones de DAGs
  │       │
  │       ├── mlops_pipeline.py              DAG PRINCIPAL (cada 6 horas)
  │       │                                  • Monitoring (drift, metrics)
  │       │                                  • Retraining condicional
  │       │                                  • Model comparison
  │       │                                  • Deploy condicional
  │       │                                  • Hot reload API
  │       │
  │       ├── train_model_dag.py             DAG de entrenamiento manual
  │       │                                  • Pull data from S3
  │       │                                  • Train model
  │       │                                  • Push to S3
  │       │
  │       └── monitor_only_dag.py            DAG solo monitoreo (cada 1 hora)
  │                                          • Check drift
  │                                          • Get metrics
  │                                          • Save metrics
  │                                          (sin reentrenamiento)
  │
  ├── 📁 notebooks/                          ══════════════════════════════════
  │   │                                      Jupyter notebooks (EDA, experimentos)
  │   │
  │   ├── 01_exploratory_data_analysis.ipynb Análisis exploratorio de datos
  │   ├── 02_model_experimentation.ipynb     Experimentos con modelos
  │   └── 03_model_evaluation.ipynb          Evaluación detallada de modelos
  │
  ├── 📁 tests/                              ══════════════════════════════════
  │   │                                      Tests unitarios y de integración
  │   │
  │   ├── test_preprocessing.py              Tests de preprocesamiento NLP
  │   ├── test_monitoring.py                 Tests del sistema de monitoreo
  │   ├── test_database.py                   Tests de conexión a Supabase
  │   ├── test_api.py                        Tests de endpoints FastAPI
  │   └── test_training.py                   Tests del pipeline de training
  │
  ├── 📁 .dvc/                               ══════════════════════════════════
  │   ├── config                             Configuración de DVC
  │   │                                      • Remote storage: S3
  │   │                                      • Bucket: ticketsfidudavivienda
  │   │
  │   └── cache/                             Cache local de DVC
  │
  ├── 📄 .dvcignore                          Archivos excluidos de DVC tracking
  │
  ├── 📄 render.yaml                         Configuración de Render.com
  │                                          • Servicio web Python
  │                                          • Build command
  │                                          • Start command: uvicorn
  │                                          • Environment variables
  │                                          • Health check: /health
  │
  ├── 📄 Procfile                            Configuración para Heroku/Render
  │                                          web: uvicorn api.inference:app
  │
  └── 📄 .env.example                        Template de variables de entorno
                                             • AWS_ACCESS_KEY_ID
                                             • AWS_SECRET_ACCESS_KEY
                                             • SUPABASE_URL
                                             • SUPABASE_KEY
                                             • API_KEY, ADMIN_API_KEY


    """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")

# ============================================================================
# TAB 2: PIPELINE DE ENTRENAMIERNO
# ============================================================================
with tab2:
    st.markdown("<h2 style='color: black;'>Pipeline de entrenamiento del modelo</h2>", unsafe_allow_html=True)
    
 
    
    # Architecture Diagram
    st.markdown("""
    """, unsafe_allow_html=True)
    
    st.code("""
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                         PIPELINE DE ENTRENAMIENTO                           │
  └─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐
  │   ENTRADA    │ el archivo config.yaml contiene las configuraciones a nivel proyecto
  │  config.yaml │
  └──────┬───────┘
         │
         ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │  1. CARGA DE DATOS                                              │
  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
  │  │   S3/DVC    │───▶│  CSV/JSON   │───▶│  DataFrame  │          │
  │  │   Bucket    │    │   tickets   │    │   pandas    │          │
  │  └─────────────┘    └─────────────┘    └─────────────┘          │
  └─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │  2. PREPROCESAMIENTO (utils/preprocessing_data.py)              │
  │                                                                 │
  │  Texto crudo ──▶ lowercase ──▶ remove_punctuation ──▶ tokenize  │
  │                                                                 │
  │  tokenize ──▶ remove_stopwords ──▶ stemming ──▶ Texto limpio    │
  │              (Spanish NLTK)      (SnowballStemmer)              │
  └─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │  3. VECTORIZACIÓN                                               │
  │                                                                 │
  │  ┌─────────────────────────────────────────────────────┐        │
  │  │              TF-IDF Vectorizer                      │        │
  │  │  • max_features: 5000                               │        │
  │  │  • ngram_range: (1, 2)                              │        │
  │  │  • sublinear_tf: True                               │        │
  │  └─────────────────────────────────────────────────────┘        │
  │                                                                 │
  │  Texto limpio ──▶ [0.12, 0.0, 0.87, ..., 0.03]  (5000 dims)     │
  └─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
  ┌────────────────────────────────────────────────────────────────┐
  │  4. DIVISIÓN DE DATOS                                          │
  │                                                                │
  │  ┌───────────────────────────────────────────────────────┐     │
  │  │                  Dataset Completo                     │     │
  │  │  ┌──────────────────────┐  ┌──────────────────────┐   │     │
  │  │  │   Train Set (80%)    │  │   Test Set (20%)     │   │     │
  │  │  │   stratify=labels    │  │   stratify=labels    │   │     │
  │  │  └──────────────────────┘  └──────────────────────┘   │     │
  │  └───────────────────────────────────────────────────────┘     │
  └────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │  5. ENTRENAMIENTO DE MODELOS (con Optuna)                       │
  │                                                                 │
  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
  │  │  Logistic   │  │   Random    │  │   XGBoost   │              │
  │  │ Regression  │  │   Forest    │  │             │              │
  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
  │         │                │                │                     │
  │  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐              │
  │  │  LightGBM   │  │    SVM      │  │  Gradient   │              │
  │  │             │  │             │  │  Boosting   │              │
  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
  │         │                │                │                     │
  │         │         ┌──────┴──────┐         │                     │
  │         │         │ Extra Trees │         │                     │
  │         │         └──────┬──────┘         │                     │
  │         │                │                │                     │
  │         └────────────────┼────────────────┘                     │
  │                          │                                      │
  │                          ▼                                      │
  │              ┌───────────────────────┐                          │
  │              │   OPTUNA TPESampler   │                          │
  │              │   n_trials: 50        │                          │
  │              │   optimize: f1_macro  │                          │
  │              └───────────────────────┘                          │
  └─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │  6. EVALUACIÓN Y SELECCIÓN                                      │
  │                                                                 │
  │  ┌─────────────────────────────────────────────────────────┐    │
  │  │  Métricas por modelo:                                   │    │
  │  │  • Accuracy     • Precision    • Recall                 │    │
  │  │  • F1-Score     • ROC-AUC      • Confusion Matrix       │    │
  │  └─────────────────────────────────────────────────────────┘    │
  │                          │                                      │
  │                          ▼                                      │
  │              ┌───────────────────────┐                          │
  │              │  Seleccionar modelo   │                          │
  │              │  con mejor F1-macro   │                          │
  │              └───────────────────────┘                          │
  └─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │  7. GUARDADO Y VERSIONAMIENTO                                   │
  │                                                                 │
  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
  │  │   MLflow    │    │    DVC      │    │     S3      │          │
  │  │  Tracking   │    │  Version    │    │   Storage   │          │
  │  │  (metrics)  │    │  (model)    │    │  (artifacts)│          │
  │  └─────────────┘    └─────────────┘    └─────────────┘          │
  │                                                                 │
  │  Archivos generados:                                            │
  │  • models/best_model.pkl      (modelo serializado)              │
  │  • models/vectorizer.pkl      (TF-IDF vectorizer)               │
  │  • models/label_encoder.pkl   (encoder de categorías)           │
  │  • models/best_model.pkl.dvc  (referencia DVC)                  │
  └─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │  8. DEPLOY ( vía GitHub Actions)                                │
  │                                                                 │
  │  git push ──▶ CI/CD Pipeline ──▶ Render Deploy ──▶ API Live     │
  └─────────────────────────────────────────────────────────────────┘


    """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    

    
    st.markdown("<h2 style='color: black;'>🛠 Stack Tecnológico para el entrenamiento</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="color: black;">
            <ul style="color: black;">
                <li style="color: black; margin-bottom: 10px;">⌨️ <strong style="color: black;">Lenguaje</strong> - Python 3.9</li>
                <li style="color: black; margin-bottom: 10px;">📋 <strong style="color: black;">Manipulación de datos</strong> - Pandas, NumPy</li>
                <li style="color: black; margin-bottom: 10px;">✂️ <strong style="color: black;">NLP / Texto</strong> - NLTK, SnowballStemmer, regex</li>
                <li style="color: black; margin-bottom: 10px;">🎯 <strong style="color: black;">Machine Learning</strong> - scikit-learn, XGBoost, LightGBM</li>
                <li style="color: black; margin-bottom: 10px;">🚀 <strong style="color: black;">Optimización</strong> - Optuna (TPESampler)</li>
                <li style="color: black; margin-bottom: 10px;">📦 <strong style="color: black;">Serialización</strong> - joblib, JSON</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="color: black;">
            <ul style="color: black;">
                <li style="color: black; margin-bottom: 10px;">🔄 <strong style="color: black;">Versionamiento</strong> - DVC, Git</li>
                <li style="color: black; margin-bottom: 10px;">💽 <strong style="color: black;">Almacenamiento</strong> - AWS S3 (boto3)</li>
                <li style="color: black; margin-bottom: 10px;">📄 <strong style="color: black;">Configuración</strong> - PyYAML (config.yaml)</li>
                <li style="color: black; margin-bottom: 10px;">📊 <strong style="color: black;">Visualización</strong> - Matplotlib</li>
                <li style="color: black; margin-bottom: 10px;">📝 <strong style="color: black;">Tracking (opcional)</strong> - MLflow</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    

# ============================================================================
# TAB 3: PIPELINE DE CLASIFICACION
# ============================================================================
with tab3:
    st.markdown("""
        Este flujo muestra cómo el sistema procesa múltiples tickets de soporte simultáneamente, clasifica cada uno usando Machine Learning y persiste los resultados automáticamente en la
  base de datos
    """)
    st.markdown("<h2 style='color: black;'>Pipeline de clasificación</h2>", unsafe_allow_html=True)
   
    
    # Architecture Diagram
    st.markdown("""
        
    """, unsafe_allow_html=True)
    
    st.code("""
  ┌───────────────────────────────────────────┐
  │                                           │
  │            CLASIFICACIÓN BATCH            │
  │                      │                    │
  └───────────────────────────────────────────┘


  ══════════════════════════════════════════════════════════════════════════════
   PASO 1: RECEPCIÓN DE SOLICITUD
  ══════════════════════════════════════════════════════════════════════════════

     El cliente (aplicación web, sistema externo) envía una solicitud
     HTTP con múltiples tickets que necesitan ser clasificados.

     ┌─────────────────────────────────────────────────────────────────────┐
     │  POST /predict/tickets/batch                                        │
     │  Header: X-API-Key: "clave-de-autenticación"                        │
     │                                                                     │
     │  Body JSON:                                                         │
     │  {                                                                  │
     │    "tickets": [                                                     │
     │      {                                                              │
     │        "ticket_id": "INC001",                                       │
     │        "short_description": "No puedo iniciar sesión en el sistema" │
     │      },                                                             │
     │      {                                                              │
     │        "ticket_id": "INC002",                                       │
     │        "short_description": "Mi computador está muy lento"          │
     │      },                                                             │
     │      {                                                              │
     │        "ticket_id": "INC003",                                       │
     │        "short_description": "Necesito cambiar mis datos de nómina"  │
     │      }                                                              │
     │    ]                                                                │
     │  }                                                                  │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   PASO 2: CAPA DE SEGURIDAD Y VALIDACIÓN
  ══════════════════════════════════════════════════════════════════════════════

     Antes de procesar, el sistema aplica múltiples capas de seguridad
     para proteger el servicio y garantizar la calidad de los datos.

     ┌───────────────────────────────────────────────────────────────────┐
     │                                                                   │
     │  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐        │
     │  │  RATE LIMIT   │   │ AUTENTICACIÓN │   │  VALIDACIÓN   │        │
     │  │               │   │               │   │               │        │
     │  │ Máximo 10     │──▶│ Verifica que  │──▶│ Confirma que  │        │
     │  │ solicitudes   │   │ la API Key    │   │ el JSON tiene │        │
     │  │ por minuto    │   │ sea válida    │   │ formato       │        │
     │  │               │   │               │   │ correcto      │        │
     │  │ Protege       │   │ Solo usuarios │   │               │        │
     │  │ contra abuso  │   │ autorizados   │   │ Pydantic      │        │
     │  └───────────────┘   └───────────────┘   └───────────────┘        │
     │                                                                   │
     │  Si alguna validación falla, se retorna error inmediatamente:     │
     │  • 429: Demasiadas solicitudes (rate limit)                       │
     │  • 401: API Key inválida                                          │
     │  • 422: Formato de datos incorrecto                               │
     │                                                                   │
     └───────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   PASO 3: PREPROCESAMIENTO DE TEXTO (NLP)
  ══════════════════════════════════════════════════════════════════════════════

     Cada ticket pasa por un pipeline de Procesamiento de Lenguaje Natural
     que limpia y normaliza el texto para optimizar la clasificación.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │  TICKET INC001: "No puedo iniciar sesión en el sistema"             │
     │                                                                     │
     │      │                                                              │
     │      ▼                                                              │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │ 1. LOWERCASE        → "no puedo iniciar sesión en el..."    │    │
     │  │ 2. REMOVE PUNCT     → "no puedo iniciar sesion en el..."    │    │
     │  │ 3. TOKENIZE (NLTK)  → ["no","puedo","iniciar","sesion"...]  │    │
     │  │ 4. REMOVE STOPWORDS → ["puedo","iniciar","sesion","sistema"]│    │
     │  │ 5. STEMMING         → ["pued","inici","sesion","sistem"]    │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │      │                                                              │
     │      ▼                                                              │
     │  Texto procesado: "pued inici sesion sistem"                        │
     │                                                                     │
     │  ─────────────────────────────────────────────────────────────      │
     │                                                                     │
     │  Este proceso se repite para cada ticket del lote:                  │
     │                                                                     │
     │  • INC001: "No puedo iniciar sesión..."  →  "pued inici sesion..."  │
     │  • INC002: "Mi computador está lento..." →  "comput lent"           │
     │  • INC003: "Necesito cambiar datos..."   →  "neces cambi dat nomin" │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   PASO 4: CLASIFICACIÓN CON MACHINE LEARNING
  ══════════════════════════════════════════════════════════════════════════════

     El modelo entrenado (XGBoost) analiza cada texto
     preprocesado y predice la categoría más probable.

     ┌────────────────────────────────────────────────────────────────────┐
     │                                                                    │
     │                    ┌─────────────────────────┐                     │
     │                    │   MODELO ML ENTRENADO   │                     │
     │                    │                         │                     │
     │                    │  • Vectorización TF-IDF │                     │
     │                    │  • 5000 características │                     │
     │                    │  • 7 algoritmos probados│                     │
     │                    │  • Optimizado con Optuna│                     │
     │                    └────────────┬────────────┘                     │
     │                                 │                                  │
     │     ┌───────────────────────────┼───────────────────────────┐      │
     │     │                           │                           │      │
     │     ▼                           ▼                           ▼      │
     │  ┌──────────┐             ┌──────────┐             ┌──────────┐    │
     │  │  INC001  │             │  INC002  │             │  INC003  │    │
     │  │          │             │          │             │          │    │
     │  │ Predicción:            │ Predicción:            │ Predicción:   │
     │  │   "TI"   │             │   "TI"   │             │  "RRHH"  │    │
     │  │          │             │          │             │          │    │
     │  │ Confianza:             │ Confianza:             │ Confianza:    │
     │  │   89%    │             │   76%    │             │   92%    │    │
     │  │          │             │          │             │          │    │
     │  │ Distribución:          │ Distribución:          │ Distribución: │
     │  │ TI: 89%  │             │ TI: 76%  │             │ RRHH: 92%│    │
     │  │ RRHH: 5% │             │ RRHH: 12%│             │ TI: 4%   │    │
     │  │ Fin: 4%  │             │ Fin: 8%  │             │ Fin: 3%  │    │
     │  │ Ops: 2%  │             │ Ops: 4%  │             │ Ops: 1%  │    │
     │  └──────────┘             └──────────┘             └──────────┘    │
     │                                                                    │
     └────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   PASO 5: PERSISTENCIA EN BASE DE DATOS (SUPABASE)
  ══════════════════════════════════════════════════════════════════════════════

     Las predicciones se guardan automáticamente en PostgreSQL (Supabase),
     actualizando el campo "causa" de cada ticket.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │  El sistema construye las operaciones de actualización:             │
     │                                                                     │
     │  updates = [                                                        │
     │    { ticket: "INC001", causa: "TI",   confianza: 0.89 },            │
     │    { ticket: "INC002", causa: "TI",   confianza: 0.76 },            │
     │    { ticket: "INC003", causa: "RRHH", confianza: 0.92 }             │
     │  ]                                                                  │
     │                                                                     │
     │                           │                                         │
     │                           ▼                                         │
     │                                                                     │
     │  ┌──────────────────────────────────────────────────────────────┐   │
     │  │                      SUPABASE                                │   │
     │  │                   (PostgreSQL Cloud)                         │   │
     │  │                                                              │   │
     │  │  Tabla: tickets_fiducia                                      │   │
     │  │  ┌────────┬─────────────────────────┬────────┬────────────┐  │   │
     │  │  │ number │ short_description       │ causa  │ updated_at │  │   │
     │  │  ├────────┼─────────────────────────┼────────┼────────────┤  │   │
     │  │  │ INC001 │ No puedo iniciar sesión │   TI   │ 2024-01-15 │  │   │
     │  │  │ INC002 │ Mi computador está lento│   TI   │ 2024-01-15 │  │   │
     │  │  │ INC003 │ Necesito cambiar datos  │  RRHH  │ 2024-01-15 │  │   │
     │  │  └────────┴─────────────────────────┴────────┴────────────┘  │   │
     │  │                                                              │   │
     │  │  Características de la conexión:                             │   │
     │  │  • Retry automático con exponential backoff                  │   │
     │  │  • Máximo 4 reintentos si hay fallas de red                  │   │
     │  │  • Conexión segura via API REST                              │   │
     │  │                                                              │   │
     │  └──────────────────────────────────────────────────────────────┘   │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   PASO 6: LOGGING PARA MONITOREO (EN PARALELO)
  ══════════════════════════════════════════════════════════════════════════════

     Mientras se procesa la respuesta, el sistema registra cada predicción
     para análisis posterior y detección de drift del modelo.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │  BackgroundTasks (ejecución asíncrona, no bloquea la respuesta)     │
     │                                                                     │
     │  ┌──────────────────────────────────────────────────────────────┐   │
     │  │  Archivo: monitoring/logs/predictions.jsonl                  │   │
     │  │                                                              │   │
     │  │  {"timestamp":"2024-01-15T10:30:01Z","prediction":"TI",...}  │   │
     │  │  {"timestamp":"2024-01-15T10:30:01Z","prediction":"TI",...}  │   │
     │  │  {"timestamp":"2024-01-15T10:30:01Z","prediction":"RRHH",...}│   │
     │  │                                                              │   │
     │  └──────────────────────────────────────────────────────────────┘   │
     │                                                                     │
     │  Estos logs permiten:                                               │
     │  • Detectar cambios en la distribución de datos (Data Drift)        │
     │  • Monitorear la confianza promedio del modelo                      │
     │  • Identificar cuándo reentrenar el modelo                          │
     │  • Auditoría de predicciones                                        │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   PASO 7: RESPUESTA AL CLIENTE
  ══════════════════════════════════════════════════════════════════════════════

     El sistema retorna un JSON estructurado con el resultado de cada
     ticket, incluyendo la confirmación de actualización en base de datos.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │  HTTP 200 OK                                                        │
     │                                                                     │
     │  {                                                                  │
     │    "total": 3,                                                      │
     │    "processed": 3,                                                  │
     │    "failed": 0,                                                     │
     │                                                                     │
     │    "results": [                                                     │
     │      {                                                              │
     │        "ticket_id": "INC001",                                       │
     │        "prediction": "TI",                                          │
     │        "probability": 0.89,                                         │
     │        "probabilities": {"TI": 0.89, "RRHH": 0.05, ...},            │
     │        "database_update": {"success": true}                         │
     │      },                                                             │
     │      {                                                              │
     │        "ticket_id": "INC002",                                       │
     │        "prediction": "TI",                                          │
     │        "probability": 0.76,                                         │
     │        "probabilities": {"TI": 0.76, "RRHH": 0.12, ...},            │
     │        "database_update": {"success": true}                         │
     │      },                                                             │
     │      {                                                              │
     │        "ticket_id": "INC003",                                       │
     │        "prediction": "RRHH",                                        │
     │        "probability": 0.92,                                         │
     │        "probabilities": {"RRHH": 0.92, "TI": 0.04, ...},            │
     │        "database_update": {"success": true}                         │
     │      }                                                              │
     │    ],                                                               │
     │                                                                     │
     │    "batch_update_summary": {                                        │
     │      "success": 3,                                                  │
     │      "failed": 0                                                    │
     │    },                                                               │
     │                                                                     │
     │    "timestamp": "2024-01-15T10:30:01Z"                              │
     │  }                                                                  │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘


  ══════════════════════════════════════════════════════════════════════════════
   RESUMEN DEL FLUJO
  ══════════════════════════════════════════════════════════════════════════════

     ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
     │ REQUEST │───▶│SEGURIDAD│───▶│   NLP   │───▶│   ML    │───▶│   BD    │
     │         │    │         │    │         │    │         │    │         │
     │ 3 tickets    │Rate Limit│    │Preproces│    │Predicción   │Supabase │
     │ en JSON │    │API Key  │    │Stemming │    │Probabilid   │UPDATE   │
     └─────────┘    └─────────┘    └─────────┘    └─────────┘    └────┬────┘
                                                                      │
                                                                      ▼
                                                                ┌─────────┐
                                                                │RESPONSE │
                                                                │         │
                                                                │3 predict│
                                                                │3 updated│
                                                                └─────────┘
    """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
 

    
    st.markdown("<h2 style='color: black;'>🛠 Stack Tecnológico para el pileline de clasificación</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="color: black;">
            <ul style="color: black;">
                <li style="color: black; margin-bottom: 10px;"><strong style="color: black;">FastAPI</strong> - Framework web de alto rendimiento</li>
                <li style="color: black; margin-bottom: 10px;"><strong style="color: black;">Pydantic</strong> - Validación de datos</li>
                <li style="color: black; margin-bottom: 10px;"><strong style="color: black;">slowapi</strong> - Rate limiting</li>
                <li style="color: black; margin-bottom: 10px;"><strong style="color: black;">NLTK</strong> - Procesamiento de lenguaje natural (español)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="color: black;">
            <ul style="color: black;">
                <li style="color: black; margin-bottom: 10px;"><strong style="color: black;">scikit-learn</strong> - Vectorización TF-IDF</li>
                <li style="color: black; margin-bottom: 10px;"><strong style="color: black;">XGBoost/LightGBM</strong> - Modelos de clasificación</li>
                <li style="color: black; margin-bottom: 10px;"><strong style="color: black;">Supabase</strong> - Base de datos PostgreSQL en la nube</li>
                <li style="color: black; margin-bottom: 10px;"><strong style="color: black;">BackgroundTasks</strong> - Procesamiento asíncrono</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
# ============================================================================
# TAB 4: PIPELINE DE REENTRENAMIENTO Y DEPLOY AUTOMATICO
# ============================================================================
with tab4:
    st.markdown("""
        Este flujo muestra cómo el sistema detecta la necesidad de reentrenar el modelo, ejecuta el entrenamiento con optimización de hiperparámetros, versiona el modelo y lo despliega
  automáticamente a producción.
    """)
    st.markdown("<h2 style='color: black;'>Pipeline de reentrenamiento y deploy</h2>", unsafe_allow_html=True)
   
    
    # Architecture Diagram
    st.markdown("""
        
    """, unsafe_allow_html=True)
    
    st.code("""
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                                                                             │
  │                 PIPELINE DE REENTRENAMIENTO Y DEPLOY                        │
  │          MLOps: Ciclo completo de vida del modelo en producción             │
  │                                                                             │
  └─────────────────────────────────────────────────────────────────────────────┘


  ══════════════════════════════════════════════════════════════════════════════
   FASE 1: DETECCIÓN DE NECESIDAD DE REENTRENAMIENTO
  ══════════════════════════════════════════════════════════════════════════════

     El sistema monitorea constantemente el rendimiento del modelo y la
     distribución de los datos para detectar cuándo es necesario reentrenar.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │                    SISTEMA DE MONITOREO                             │
     │                                                                     │
     │  ┌───────────────────┐  ┌───────────────────┐  ┌─────────────────┐  │
     │  │    DATA DRIFT     │  │  CONCEPT DRIFT    │  │   SCHEDULED     │  │
     │  │                   │  │                   │  │                 │  │
     │  │ Detecta cambios   │  │ Detecta cuando    │  │ Reentrenamiento │  │
     │  │ en la distribución│  │ las predicciones  │  │ programado      │  │
     │  │ de datos entrantes│  │ ya no son         │  │ (semanal,       │  │
     │  │                   │  │ precisas          │  │  mensual)       │  │
     │  │ Métricas:         │  │                   │  │                 │  │
     │  │ • KS Test         │  │ Métricas:         │  │ GitHub Actions  │  │
     │  │ • Chi-Square      │  │ • F1-Score < 0.8  │  │ Cron Schedule   │  │
     │  │ • Vocab Growth    │  │ • Accuracy drop   │  │                 │  │
     │  └─────────┬─────────┘  └─────────┬─────────┘  └────────┬────────┘  │
     │            │                      │                     │           │
     │            └──────────────────────┼─────────────────────┘           │
     │                                   │                                 │
     │                                   ▼                                 │
     │                    ┌────────────────────────────┐                   │
     │                    │   ¿REENTRENAMIENTO         │                   │
     │                    │      NECESARIO?            │                   │
     │                    │                            │                   │
     │                    │  drift_score > threshold   │                   │
     │                    │        OR                  │                   │
     │                    │  scheduled_time reached    │                   │
     │                    └──────────────┬─────────────┘                   │
     │                                   │                                 │
     │                                   ▼                                 │
     │                              [ SÍ ]                                 │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   FASE 2: RECOLECCIÓN Y PREPARACIÓN DE DATOS
  ══════════════════════════════════════════════════════════════════════════════

     El sistema obtiene los datos más recientes, incluyendo tickets nuevos
     que han sido etiquetados manualmente por el equipo de soporte.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │  ┌─────────────────┐         ┌─────────────────┐                    │
     │  │    SUPABASE     │         │    AWS S3       │                    │
     │  │   (PostgreSQL)  │         │   (Data Lake)   │                    │
     │  │                 │         │                 │                    │
     │  │ Tickets nuevos  │         │ Dataset         │                    │
     │  │ etiquetados     │         │ histórico       │                    │
     │  │ manualmente     │         │ versionado      │                    │
     │  └────────┬────────┘         └────────┬────────┘                    │
     │           │                           │                             │
     │           └─────────────┬─────────────┘                             │
     │                         │                                           │
     │                         ▼                                           │
     │           ┌─────────────────────────────┐                           │
     │           │     DATASET CONSOLIDADO     │                           │
     │           │                             │                           │
     │           │  • Tickets históricos       │                           │
     │           │  • Tickets nuevos           │                           │
     │           │  • Etiquetas verificadas    │                           │
     │           │                             │                           │
     │           │  Total: ~10,000 registros   │                           │
     │           └─────────────────────────────┘                           │
     │                                                                     │
     │  Campos utilizados:                                                 │
     │  ┌────────────────────┬────────────────────┬──────────────────┐     │
     │  │ short_description  │    close_notes     │     etiqueta     │     │
     │  │ (texto entrada)    │  (texto entrada)   │  (label objetivo)│     │
     │  └────────────────────┴────────────────────┴──────────────────┘     │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   FASE 3: PREPROCESAMIENTO DE DATOS
  ══════════════════════════════════════════════════════════════════════════════

     Todo el dataset pasa por el pipeline de NLP para normalizar el texto
     y prepararlo para el entrenamiento.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │                 PIPELINE DE PREPROCESAMIENTO                        │
     │                                                                     │
     │  Dataset crudo                                                      │
     │       │                                                             │
     │       ▼                                                             │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │                                                             │    │
     │  │  1. LIMPIEZA DE TEXTO                                       │    │
     │  │     • Convertir a minúsculas                                │    │
     │  │     • Remover caracteres especiales y puntuación            │    │
     │  │     • Normalizar espacios                                   │    │
     │  │                                                             │    │
     │  │  2. TOKENIZACIÓN (NLTK)                                     │    │
     │  │     • Dividir texto en palabras individuales                │    │
     │  │     • Configurado para español                              │    │
     │  │                                                             │    │
     │  │  3. ELIMINACIÓN DE STOPWORDS                                │    │
     │  │     • Remover palabras sin valor semántico                  │    │
     │  │     • Lista de stopwords en español                         │    │
     │  │     • Ejemplos: "el", "la", "de", "que", "en"               │    │
     │  │                                                             │    │
     │  │  4. STEMMING (SnowballStemmer)                              │    │
     │  │     • Reducir palabras a su raíz                            │    │
     │  │     • "computadora" → "comput"                              │    │
     │  │     • "trabajando" → "trabaj"                               │    │
     │  │                                                             │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │       │                                                             │
     │       ▼                                                             │
     │  Dataset preprocesado (texto limpio + etiquetas)                    │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   FASE 4: DIVISIÓN DE DATOS Y VECTORIZACIÓN
  ══════════════════════════════════════════════════════════════════════════════

     Los datos se dividen estratificadamente y se convierten a vectores
     numéricos que los algoritmos de ML pueden procesar.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │  DIVISIÓN ESTRATIFICADA (mantiene proporción de clases)             │
     │                                                                     │
     │  ┌────────────────────────────────────────────────────────────┐     │
     │  │                   DATASET COMPLETO                         │     │
     │  │                     10,000 tickets                         │     │
     │  │                                                            │     │
     │  │  ┌──────────────────────┐    ┌──────────────────────────┐  │     │
     │  │  │   TRAIN SET (80%)    │    │    TEST SET (20%)        │  │     │
     │  │  │    8,000 tickets     │    │    2,000 tickets         │  │     │
     │  │  │                      │    │                          │  │     │
     │  │  │  Para entrenar       │    │  Para evaluar            │  │     │
     │  │  │  los modelos         │    │  rendimiento final       │  │     │
     │  │  └──────────────────────┘    └──────────────────────────┘  │     │
     │  └────────────────────────────────────────────────────────────┘     │
     │                                                                     │
     │  VECTORIZACIÓN TF-IDF                                               │
     │                                                                     │
     │  ┌────────────────────────────────────────────────────────────┐     │
     │  │                                                            │     │
     │  │  TfidfVectorizer(                                          │     │
     │  │      max_features = 5000,    # Vocabulario máximo          │     │
     │  │      ngram_range = (1, 2),   # Unigramas y bigramas        │     │
     │  │      sublinear_tf = True     # Escala logarítmica          │     │
     │  │  )                                                         │     │
     │  │                                                            │     │
     │  │  Texto: "error sistema login"                              │     │
     │  │           │                                                │     │
     │  │           ▼                                                │     │
     │  │  Vector: [0.0, 0.23, 0.0, 0.67, ..., 0.12]  (5000 dims)    │     │
     │  │                                                            │     │
     │  └────────────────────────────────────────────────────────────┘     │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   FASE 5: ENTRENAMIENTO MULTI-MODELO CON OPTIMIZACIÓN
  ══════════════════════════════════════════════════════════════════════════════

     Se entrenan 7 algoritmos diferentes, cada uno optimizado con Optuna
     para encontrar los mejores hiperparámetros automáticamente.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │                    ENTRENAMIENTO PARALELO                           │
     │                                                                     │
     │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │
     │  │  LOGISTIC   │ │   RANDOM    │ │  XGBOOST    │ │  LIGHTGBM   │    │
     │  │ REGRESSION  │ │   FOREST    │ │             │ │             │    │
     │  │             │ │             │ │             │ │             │    │
     │  │ Rápido,     │ │ Robusto,    │ │ Alto        │ │ Muy rápido, │    │
     │  │ interpretable│ │ menos       │ │ rendimiento │ │ eficiente  │    │
     │  │             │ │ overfitting │ │             │ │ en memoria  │    │
     │  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘    │
     │         │               │               │               │           │
     │  ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐                    │
     │  │    SVM      │ │  GRADIENT   │ │   EXTRA     │                    │
     │  │             │ │  BOOSTING   │ │   TREES     │                    │
     │  │             │ │             │ │             │                    │
     │  │ Bueno con   │ │ Ensemble    │ │ Similar a   │                    │
     │  │ texto       │ │ secuencial  │ │ RF, más     │                    │
     │  │             │ │             │ │ aleatorio   │                    │
     │  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘                    │
     │         │               │               │                           │
     │         └───────────────┼───────────────┘                           │
     │                         │                                           │
     │                         ▼                                           │
     │           ┌─────────────────────────────┐                           │
     │           │     OPTUNA (TPESampler)     │                           │
     │           │                             │                           │
     │           │  Para cada modelo:          │                           │
     │           │  • 50 trials de búsqueda    │                           │
     │           │  • Optimiza F1-Score        │                           │
     │           │  • Poda trials ineficientes │                           │
     │           │                             │                           │
     │           │  Ejemplo XGBoost:           │                           │
     │           │  • max_depth: [3, 10]       │                           │
     │           │  • learning_rate: [0.01,0.3]│                           │
     │           │  • n_estimators: [100, 500] │                           │
     │           │  • subsample: [0.6, 1.0]    │                           │
     │           └─────────────────────────────┘                           │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   FASE 6: EVALUACIÓN Y SELECCIÓN DEL MEJOR MODELO
  ══════════════════════════════════════════════════════════════════════════════

     Todos los modelos entrenados se evalúan con el test set para
     seleccionar el que mejor generaliza a datos no vistos.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │                    EVALUACIÓN EN TEST SET                           │
     │                                                                     │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │                                                             │    │
     │  │   MODELO              ACCURACY   F1-SCORE   ROC-AUC         │    │
     │  │   ─────────────────────────────────────────────────────     │    │
     │  │   Logistic Regression   0.82       0.81       0.89          │    │
     │  │   Random Forest         0.85       0.84       0.92          │    │
     │  │   XGBoost               0.89       0.88       0.95    ◄──── │    │
     │  │   LightGBM              0.88       0.87       0.94          │    │
     │  │   SVM                   0.84       0.83       0.91          │    │
     │  │   Gradient Boosting     0.86       0.85       0.93          │    │
     │  │   Extra Trees           0.84       0.83       0.91          │    │
     │  │                                                             │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │                                                                     │
     │                              │                                      │
     │                              ▼                                      │
     │                                                                     │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │                   MODELO SELECCIONADO                       │    │
     │  │                                                             │    │
     │  │   XGBoost (F1-Score: 0.88)                                  │    │
     │  │                                                             │    │
     │  │   Hiperparámetros óptimos:                                  │    │
     │  │   • max_depth: 7                                            │    │
     │  │   • learning_rate: 0.1                                      │    │
     │  │   • n_estimators: 300                                       │    │
     │  │   • subsample: 0.8                                          │    │
     │  │                                                             │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │                                                                     │
     │  Métricas adicionales generadas:                                    │
     │  • Matriz de confusión                                              │
     │  • Classification report por clase                                  │
     │  • Curvas ROC por clase                                             │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   FASE 7: VERSIONAMIENTO Y ALMACENAMIENTO
  ══════════════════════════════════════════════════════════════════════════════

     El modelo seleccionado se serializa, versiona con DVC y sube a S3
     para tener un registro histórico y permitir rollback si es necesario.

     ┌────────────────────────────────────────────────────────────────────┐
     │                                                                    │
     │  SERIALIZACIÓN DEL MODELO                                          │
     │                                                                    │
     │  ┌─────────────────────────────────────────────────────────────┐   │
     │  │                                                             │   │
     │  │  joblib.dump(model, "models/best_model.pkl")                │   │
     │  │  joblib.dump(vectorizer, "models/vectorizer.pkl")           │   │
     │  │  joblib.dump(label_encoder, "models/label_encoder.pkl")     │   │
     │  │                                                             │   │
     │  │  Archivos generados:                                        │   │
     │  │  ├── models/                                                │   │
     │  │  │   ├── best_model.pkl          (modelo serializado)       │   │
     │  │  │   ├── vectorizer.pkl          (TF-IDF)                   │   │
     │  │  │   ├── label_encoder.pkl       (encoder de clases)        │   │
     │  │  │   └── best_model_metadata.json (métricas, params)        │   │
     │  │                                                             │   │
     │  └─────────────────────────────────────────────────────────────┘   │
     │                                                                    │
     │                              │                                     │
     │                              ▼                                     │
     │                                                                    │
     │  VERSIONAMIENTO CON DVC + S3                                       │
     │                                                                    │
     │  ┌─────────────────────────────────────────────────────────────┐   │
     │  │                                                             │   │
     │  │  $ dvc add models/best_model.pkl                            │   │
     │  │                                                             │   │
     │  │  Genera: models/best_model.pkl.dvc                          │   │
     │  │  ┌────────────────────────────────────────────────────┐     │   │
     │  │  │  outs:                                             │     │   │
     │  │  │    - md5: a1b2c3d4e5f6...   ← Hash único           │     │   │
     │  │  │      path: best_model.pkl                          │     │   │
     │  │  └────────────────────────────────────────────────────┘     │   │
     │  │                                                             │   │
     │  │  $ dvc push                                                 │   │
     │  │                                                             │   │
     │  │  ┌────────────────────────────────────────────────────┐     │   │
     │  │  │                    AWS S3                          │     │   │
     │  │  │        ticketsfidudavivienda bucket                │     │   │
     │  │  │                                                    │     │   │
     │  │  │  dvc-storage/                                      │     │   │
     │  │  │  └── models/                                       │     │   │
     │  │  │      └── files/                                    │     │   │
     │  │  │          └── md5/                                  │     │   │
     │  │  │              └── a1/                               │     │   │
     │  │  │                  └── b2c3d4e5f6...  (modelo)       │     │   │
     │  │  └────────────────────────────────────────────────────┘     │   │
     │  │                                                             │   │
     │  └─────────────────────────────────────────────────────────────┘   │
     │                                                                    │
     │  Registro en MLflow (opcional):                                    │
     │  • Métricas del experimento                                        │
     │  • Parámetros utilizados                                           │
     │  • Comparación con versiones anteriores                            │
     │                                                                    │
     └────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   FASE 8: COMMIT Y PUSH A GITHUB
  ══════════════════════════════════════════════════════════════════════════════

     Los cambios (archivo .dvc actualizado y metadata) se commitean a Git,
     lo que dispara automáticamente el pipeline de CI/CD.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │  ACTUALIZACIÓN DEL REPOSITORIO                                      │
     │                                                                     │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │                                                             │    │
     │  │  $ git add models/best_model.pkl.dvc                        │    │
     │  │  $ git add models/best_model_metadata.json                  │    │
     │  │                                                             │    │
     │  │  $ git commit -m "feat: Retrain model v1.3                  │    │
     │  │                                                             │    │
     │  │      - New F1-Score: 0.88 (prev: 0.85)                      │    │
     │  │      - Algorithm: XGBoost                                   │    │
     │  │      - Training samples: 10,000                             │    │ 
     │  │      - Triggered by: data drift detection"                  │    │
     │  │                                                             │    │
     │  │  $ git push origin main                                     │    │
     │  │                                                             │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │                                                                     │
     │                              │                                      │
     │                              ▼                                      │
     │                                                                     │
     │                    ┌─────────────────────┐                          │
     │                    │                     │                          │
     │                    │   GITHUB WEBHOOK    │                          │
     │                    │                     │                          │
     │                    │   Push to main      │                          │
     │                    │   detected!         │                          │
     │                    │                     │                          │
     │                    └──────────┬──────────┘                          │
     │                               │                                     │
     │                               ▼                                     │
     │                    Trigger GitHub Actions                           │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   FASE 9: PIPELINE CI/CD (GITHUB ACTIONS)
  ══════════════════════════════════════════════════════════════════════════════

     GitHub Actions ejecuta validaciones automáticas y, si pasan,
     dispara el despliegue a producción.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │                      GITHUB ACTIONS                                 │
     │                   ci_cd_pipeline.yml                                │
     │                                                                     │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │                                                             │    │
     │  │  JOB 1: VALIDATE                                            │    │
     │  │  ─────────────────                                          │    │
     │  │                                                             │    │
     │  │  ✓ Verificar archivos requeridos existen                    │    │
     │  │    • api/inference.py                                       │    │
     │  │    • requirements.txt                                       │    │
     │  │    • config.yaml                                            │    │
     │  │    • models/best_model.pkl.dvc                              │    │
     │  │                                                             │    │
     │  │  ✓ Validar sintaxis Python                                  │    │
     │  │    • py_compile en todos los scripts                        │    │
     │  │                                                             │    │
     │  │  ✓ Validar imports                                          │    │
     │  │    • Verificar que módulos se pueden importar               │    │
     │  │                                                             │    │
     │  │  ✓ Validar config.yaml                                      │    │
     │  │    • Secciones requeridas presentes                         │    │
     │  │                                                             │    │
     │  │  ✓ Validar render.yaml                                      │    │
     │  │    • Configuración de deployment correcta                   │    │
     │  │                                                             │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │                              │                                      │
     │                              ▼ Si todas pasan                       │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │                                                             │    │
     │  │  JOB 2: DEPLOY                                              │    │
     │  │  ────────────────                                           │    │
     │  │                                                             │    │
     │  │  1. Trigger Render Deploy Hook                              │    │
     │  │     curl -X POST "$RENDER_DEPLOY_HOOK_URL"                  │    │
     │  │                                                             │    │
     │  │  2. Esperar inicio de deploy (30s)                          │    │
     │  │                                                             │    │
     │  │  3. Health check post-deploy                                │    │
     │  │     curl "$API_URL/health"                                  │    │
     │  │     (5 intentos, 30s entre cada uno)                        │    │
     │  │                                                             │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │                              │                                      │
     │                              ▼                                      │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │                                                             │    │
     │  │  JOB 3: NOTIFY                                              │    │
     │  │  ─────────────                                              │    │
     │  │                                                             │    │
     │  │  Enviar notificación a:                                     │    │
     │  │  • Slack (si configurado)                                   │    │
     │  │  • Discord (si configurado)                                 │    │
     │  │  • Telegram (si configurado)                                │    │
     │  │ Mensaje: "✅ Deploy exitoso - Model v1.3"                   │    │                                                     │    │
     │  │ Mensaje: "✅ Deploy exitoso - Model v1.3"                   │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   FASE 10: DESPLIEGUE EN RENDER
  ══════════════════════════════════════════════════════════════════════════════

     Render recibe el webhook, clona el repositorio actualizado,
     construye la aplicación y la despliega.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │                         RENDER.COM                                  │
     │                   (Platform as a Service)                           │
     │                                                                     │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │                                                             │    │
     │  │  1. BUILD PHASE                                             │    │
     │  │  ─────────────                                              │    │
     │  │                                                             │    │
     │  │  $ pip install --upgrade pip                                │    │
     │  │  $ pip install -r requirements.txt                          │    │
     │  │                                                             │    │
     │  │  # Descargar recursos NLTK                                  │    │
     │  │  $ python -c "import nltk; nltk.download('punkt')..."       │    │
     │  │                                                             │    │
     │  │  Dependencias instaladas:                                   │    │
     │  │  • FastAPI, Uvicorn (servidor)                              │    │
     │  │  • scikit-learn, XGBoost (ML)                               │    │
     │  │  • boto3, DVC (acceso a S3)                                 │    │
     │  │  • supabase (base de datos)                                 │    │
     │  │  • NLTK (NLP)                                               │    │
     │  │                                                             │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │                              │                                      │
     │                              ▼                                      │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │                                                             │    │
     │  │  2. START PHASE                                             │    │
     │  │  ─────────────                                              │    │
     │  │                                                             │    │
     │  │  $ uvicorn api.inference:app --host 0.0.0.0 --port $PORT    │    │
     │  │                                                             │    │
     │  │  Durante startup:                                           │    │
     │  │  ┌────────────────────────────────────────────────────┐     │    │
     │  │  │  1. download_nltk_data()                           │     │    │
     │  │  │     Descarga recursos NLTK si no existen           │     │    │
     │  │  │                                                    │     │    │
     │  │  │  2. download_model_from_s3()                       │     │    │
     │  │  │     Lee hash de best_model.pkl.dvc                 │     │    │
     │  │  │     Descarga modelo desde S3 usando boto3          │     │    │
     │  │  │                                                    │     │    │
     │  │  │  3. load_model()                                   │     │    │
     │  │  │     Carga modelo en memoria                        │     │    │
     │  │  │     Inicializa vectorizer y label_encoder          │     │    │
     │  │  │     Configura drift detector                       │     │    │
     │  │  │                                                    │     │    │
     │  │  │  4. initialize_database()                          │     │    │
     │  │  │     Conecta a Supabase                             │     │    │
     │  │  │     Verifica columnas requeridas                   │     │    │
     │  │  └────────────────────────────────────────────────────┘     │    │
     │  │                                                             │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │                              │                                      │
     │                              ▼                                      │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │                                                             │    │
     │  │  3. HEALTH CHECK                                            │    │
     │  │  ──────────────                                             │    │
     │  │                                                             │    │
     │  │  Render verifica: GET /health                               │    │
     │  │                                                             │    │
     │  │  Response esperado:                                         │    │
     │  │  {                                                          │    │
     │  │    "status": "healthy",                                     │    │
     │  │    "model_loaded": true,                                    │    │
     │  │    "drift_detector_ready": true                             │    │
     │  │  }                                                          │    │
     │  │                                                             │    │
     │  │  Si health check pasa → Deploy completado                   │    │
     │  │                                                             │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼

  ══════════════════════════════════════════════════════════════════════════════
   FASE 11: API EN PRODUCCIÓN CON NUEVO MODELO
  ══════════════════════════════════════════════════════════════════════════════

     El nuevo modelo está ahora sirviendo predicciones en producción.
     Zero downtime gracias al rolling deployment de Render.

     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │                    API EN PRODUCCIÓN                                │
     │           https://ticket-classifier-api.onrender.com                │
     │                                                                     │
     │  ┌─────────────────────────────────────────────────────────────┐    │
     │  │                                                             │    │
     │  │  MODELO ACTIVO: XGBoost v1.3                                │    │
     │  │  F1-Score: 0.88                                             │    │
     │  │  Entrenado: 2024-01-15                                      │    │
     │  │                                                             │    │
     │  │  Endpoints disponibles:                                     │    │
     │  │  ├── GET  /health              - Health check               │    │
     │  │  ├── POST /predict/ticket      - Predicción individual      │    │
     │  │  ├── POST /predict/tickets/batch - Predicción en lote       │    │
     │  │  ├── GET  /monitoring/drift    - Estado del drift           │    │
     │  │  └── POST /admin/reload-model  - Recarga manual             │    │
     │  │                                                             │    │
     │  └─────────────────────────────────────────────────────────────┘    │
     │                                                                     │
     │  El ciclo continúa: el sistema de monitoreo sigue observando        │
     │  para detectar cuándo será necesario el próximo reentrenamiento.    │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘


  ══════════════════════════════════════════════════════════════════════════════
   RESUMEN VISUAL DEL PIPELINE COMPLETO
  ══════════════════════════════════════════════════════════════════════════════

  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │MONITOREO │──▶│  DATOS   │──▶│  TRAIN   │──▶│  EVAL    │──▶│   DVC    │
  │          │   │          │   │          │   │          │   │          │
  │Drift     │   │Supabase  │   │7 modelos │   │Test set  │   │Version   │
  │Detection │   │S3        │   │Optuna    │   │F1-Score  │   │S3 Push   │
  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └────┬─────┘
                                                                   │
  ┌────────────────────────────────────────────────────────────────┘
  │
  ▼
  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │   GIT    │──▶│  GITHUB  │──▶│ VALIDATE │──▶│  RENDER  │──▶│   API    │
  │          │   │ ACTIONS  │   │          │   │          │   │          │
  │Commit    │   │CI/CD     │   │Syntax    │   │Build     │   │Modelo    │
  │Push      │   │Trigger   │   │Imports   │   │Deploy    │   │Activo    │
  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
    """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
 

    
    st.markdown("<h2 style='color: black;'>🛠 Stack Tecnológico para el pileline de reentrenamiento y deploy</h2>", unsafe_allow_html=True)
    

    st.markdown("### 🛠 Stack Tecnológico")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="color: black;">
            <ul style="color: black;">
                <li style="color: black; margin-bottom: 10px;">📊 <strong style="color: black;">Monitoreo</strong> - KS Test, Chi-Square, métricas de drift</li>
                <li style="color: black; margin-bottom: 10px;">💾 <strong style="color: black;">Datos</strong> - Supabase (PostgreSQL), AWS S3</li>
                <li style="color: black; margin-bottom: 10px;">🔧 <strong style="color: black;">Preprocesamiento</strong> - NLTK, SnowballStemmer (español)</li>
                <li style="color: black; margin-bottom: 10px;">📐 <strong style="color: black;">Vectorización</strong> - TF-IDF (scikit-learn)</li>
                <li style="color: black; margin-bottom: 10px;">🤖 <strong style="color: black;">Entrenamiento</strong> - XGBoost, LightGBM, Random Forest</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="color: black;">
            <ul style="color: black;">
                <li style="color: black; margin-bottom: 10px;">⚡ <strong style="color: black;">Optimización</strong> - Optuna (TPESampler, 50 trials)</li>
                <li style="color: black; margin-bottom: 10px;">🔀 <strong style="color: black;">Versionamiento</strong> - DVC + AWS S3</li>
                <li style="color: black; margin-bottom: 10px;">🚀 <strong style="color: black;">CI/CD</strong> - GitHub Actions</li>
                <li style="color: black; margin-bottom: 10px;">🌐 <strong style="color: black;">Deploy</strong> - Render.com (PaaS)</li>
                <li style="color: black; margin-bottom: 10px;">🔌 <strong style="color: black;">API</strong> - FastAPI + Uvicorn</li>
                <li style="color: black; margin-bottom: 10px;">🗄️ <strong style="color: black;">Base de datos</strong> - Supabase (PostgreSQL)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
# ============================================================================
# TAB 5: ORQUESTACION CON AIRFLOW
# ============================================================================
with tab5:
    st.markdown("<h2 style='color: black;'>🖇️ Orquestación con Airflow</h2>", unsafe_allow_html=True)
    st.markdown("""
        El sistema cuenta con 3 DAGs que trabajan en conjunto para mantener
     el modelo de clasificación funcionando óptimamente en producción.
    """)
    # Architecture Diagram
    st.markdown("""
    """, unsafe_allow_html=True)
    
    st.code("""
     ┌────────────────────────────────────────────────────────────────────┐
     │                                                                    │
     │                       AIRFLOW SCHEDULER                            │
     │                                                                    │
     │  ┌───────────────────────────────────────────────────────────────┐ │
     │  │                                                               │ │
     │  │   DAG 1                    DAG 2                  DAG 3       │ │
     │  │   ──────────────           ──────────────        ───────────  │ │
     │  │   mlops_pipeline           monitor_only          train_manual │ │
     │  │                                                               │ │
     │  │   ⏰ Cada 6 horas          ⏰ Cada 1 hora        🖐️ Manual     │ │
     │  │                                                               │ │
     │  │   Pipeline completo        Solo monitoreo        Solo train   │ │
     │  │   con decisiones           sin reentrenar        forzado      │ │
     │  │   automáticas                                                 │ │
     │  │                                                               │ │
     │  └───────────────────────────────────────────────────────────────┘ │
     │                                                                    │
     └────────────────────────────────────────────────────────────────────┘
    """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    # DAG 1: PIPELINE PRINCIPAL
    st.markdown("<h2 style='color: black;'>DAG 1: PIPELINE PRINCIPAL</h2>", unsafe_allow_html=True)
    st.markdown("""
        Pipeline completo que orquesta monitoreo, detección de drift,
     reentrenamiento condicional y deploy automático.
    """)
      # Architecture Diagram
    st.markdown("""
    """, unsafe_allow_html=True)
    
    st.code("""
     ┌────────────────────────────────────────────┐
     │  Configuración:                            │
     │  • Schedule: Cada 6 horas                  │
     │  • Max concurrent runs: 1                  │
     │  • Max tareas simultáneas: 4               │
     │  • Retries: 3 con delay de 2 minutos       │
     └────────────────────────────────────────────┘

                                ┌─────────┐
                                │  START  │
                                └────┬────┘
                                     │
                                     ▼
     ┌───────────────────────────────────────────────────────────────────────┐
     │                                                                       │
     │                    TASK GROUP: MONITORING                             │
     │                    ─────────────────────────                          │
     │                                                                       │
     │   ┌─────────────────────┐                                             │
     │   │  check_api_health   │  Verifica que la API de producción          │
     │   │                     │  esté funcionando correctamente             │
     │   │  GET /health        │                                             │
     │   └──────────┬──────────┘                                             │
     │              │                                                        │
     │              ├─────────────────────┐                                  │
     │              ▼                     ▼                                  │
     │   ┌─────────────────────┐  ┌─────────────────────┐                    │
     │   │    check_drift      │  │ evaluate_performance│                    │
     │   │                     │  │                     │                    │
     │   │  GET /monitoring/   │  │  GET /monitoring/   │                    │
     │   │      drift          │  │      metrics        │                    │
     │   │                     │  │                     │                    │
     │   │  • KS Test          │  │  • Accuracy actual  │                    │
     │   │  • Chi-Square       │  │  • F1-Score actual  │                    │
     │   │  • Vocab growth     │  │  • Predictions log  │                    │
     │   └──────────┬──────────┘  └──────────┬──────────┘                    │
     │              │                        │                               │
     │              └───────────┬────────────┘                               │
     │                          ▼                                            │
     │              ┌─────────────────────┐                                  │
     │              │  decide_retraining  │                                  │
     │              │                     │                                  │
     │              │  Evalúa:            │                                  │
     │              │  • drift_score >    │                                  │
     │              │    threshold?       │                                  │
     │              │  • performance      │                                  │
     │              │    degradada?       │                                  │
     │              │                     │                                  │
     │              │  XCom: should_      │                                  │
     │              │        retrain      │                                  │
     │              └──────────┬──────────┘                                  │
     │                         │                                             │
     └─────────────────────────┼─────────────────────────────────────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │    should_retrain_check      │
                │    (ShortCircuitOperator)    │
                │                              │
                │    ¿should_retrain == True?  │
                └──────────────┬───────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼ SÍ                          ▼ NO
     ┌──────────────────────┐      ┌──────────────────┐
     │   TASK GROUP:        │      │                  │
     │   RETRAINING         │      │       END        │
     └──────────┬───────────┘      │  (Skip retrain)  │
                │                  └──────────────────┘
                ▼
     ┌───────────────────────────────────────────────────────────────────────┐
     │                                                                       │
     │                    TASK GROUP: RETRAINING                             │
     │                    ──────────────────────                             │
     │                                                                       │
     │   ┌─────────────────────────┐                                         │
     │   │  save_current_metrics   │  Guarda métricas del modelo actual      │
     │   │                         │  ANTES de reentrenar (para comparar)    │
     │   │  • Backup modelo actual │                                         │
     │   │  • Guarda F1 en XCom    │                                         │
     │   └───────────┬─────────────┘                                         │
     │               │                                                       │
     │               ▼                                                       │
     │   ┌─────────────────────────┐                                         │
     │   │      train_model        │  Ejecuta scripts/train_model.py         │
     │   │                         │                                         │
     │   │  • 7 algoritmos         │  ⏱️ Timeout: 1 hora                     │
     │   │  • Optuna optimization  │                                         │
     │   │  • Selección del mejor  │  📧 Notifica inicio y resultado         │
     │   └───────────┬─────────────┘                                         │
     │               │                                                       │
     │               ▼                                                       │
     │   ┌─────────────────────────┐                                         │
     │   │    compare_models       │  Compara modelo ANTERIOR vs NUEVO       │
     │   │                         │                                         │
     │   │  • F1 anterior (XCom)   │                                         │
     │   │  • F1 nuevo (archivo)   │                                         │
     │   │  • Mejora > umbral?     │                                         │
     │   │                         │                                         │
     │   │  XCom: should_deploy    │                                         │
     │   └───────────┬─────────────┘                                         │
     │               │                                                       │
     └───────────────┼───────────────────────────────────────────────────────┘
                     │
                     ▼
      ┌──────────────────────────────┐
      │    should_deploy_check       │
      │    (ShortCircuitOperator)    │
      │                              │
      │    ¿Nuevo modelo mejor?      │
      │    ¿improvement > 0.01?      │
      └──────────────┬───────────────┘
                     │
      ┌──────────────┴──────────────┐
      │                             │
      ▼ SÍ                          ▼ NO
     ┌──────────────────────┐      ┌──────────────────┐
     │   TASK GROUP:        │      │                  │
     │   DEPLOY             │      │       END        │
     └──────────┬───────────┘      │  (Keep current)  │
                │                  └──────────────────┘
                ▼
     ┌───────────────────────────────────────────────────────────────────────┐
     │                                                                       │
     │                      TASK GROUP: DEPLOY                               │
     │                      ──────────────────                               │
     │                                                                       │
     │   ┌─────────────────────────┐                                         │
     │   │     deploy_model        │  Ejecuta scripts/deploy_model.py        │
     │   │                         │                                         │
     │   │  • Git commit           │                                         │
     │   │  • Trigger CI/CD        │                                         │
     │   └───────────┬─────────────┘                                         │
     │               │                                                       │
     │               ▼                                                       │
     │   ┌─────────────────────────┐                                         │
     │   │     push_to_s3          │  Versiona modelo con DVC                │
     │   │                         │                                         │
     │   │  • dvc add              │                                         │
     │   │  • dvc push             │                                         │
     │   │  • Upload to S3         │                                         │
     │   └───────────┬─────────────┘                                         │
     │               │                                                       │
     │               ▼                                                       │
     │   ┌─────────────────────────┐                                         │
     │   │   reload_api_model      │  Hot reload sin reiniciar API           │
     │   │                         │                                         │
     │   │  POST /admin/           │                                         │
     │   │       reload-model      │                                         │
     │   │                         │                                         │
     │   │  📧 Notifica deploy     │                                         │
     │   │     completado          │                                         │
     │   └───────────┬─────────────┘                                         │
     │               │                                                       │
     └───────────────┼───────────────────────────────────────────────────────┘
                     │
                     ▼
                ┌─────────┐
                │   END   │
                └─────────┘
    """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    #  DAG 2: SOLO MONITOREO (monitor_only)
    st.markdown("<h2 style='color: black;'>DAG 2: SOLO MONITOREO (monitor_only)</h2>", unsafe_allow_html=True)
    st.markdown("""
        DAG ligero que solo monitorea sin disparar reentrenamiento.
     Útil para observar el comportamiento del modelo entre ciclos del
     pipeline principal.
    """)
    
    st.markdown("""
    """, unsafe_allow_html=True)
    st.code("""
    ┌────────────────────────────────────────────────────────────────────┐
    │  Configuración:                                                    │
    │  • Schedule: Cada 1 hora                                           │
    │  • Retries: 1                                                      │
    │  • Tags: [mlops, monitoring]                                       │
    └────────────────────────────────────────────────────────────────────┘

                                ┌─────────┐
                                │  START  │
                                └────┬────┘
                                     │
                      ┌──────────────┴──────────────┐
                      │                             │
                      ▼                             ▼
           ┌─────────────────────┐      ┌─────────────────────┐
           │    check_drift      │      │    get_metrics      │
           │                     │      │                     │
           │  GET /monitoring/   │      │  GET /monitoring/   │
           │      drift          │      │      metrics        │
           │                     │      │                     │
           │  Registra:          │      │  Registra:          │
           │  • drift_detected   │      │  • total_predictions│
           │  • drift_score      │      │  • avg_confidence   │
           └──────────┬──────────┘      └──────────┬──────────┘
                      │                             │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────┐
                      │    save_metrics     │
                      │                     │
                      │  POST /monitoring/  │
                      │       save-metrics  │
                      │                     │
                      │  Persiste métricas  │
                      │  del día            │
                      └──────────┬──────────┘
                                 │
                                 ▼
                            ┌─────────┐
                            │   END   │
                            └─────────┘
            
    """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    #  DAG 3: ENTRENAMIENTO MANUAL (train_model_manual)
    st.markdown("<h2 style='color: black;'>DAG 3: ENTRENAMIENTO MANUAL (train_model_manual)</h2>", unsafe_allow_html=True)
    st.markdown("""
        DAG para reentrenamiento forzado desde la UI de Airflow.
     No tiene schedule automático, solo se ejecuta manualmente.
    """)
    
    st.markdown("""
    """, unsafe_allow_html=True)
    st.code("""
     ┌─────────────────────────────────────────────────────────────────────┐
     │  Configuración:                                                     │
     │  • Schedule: None (solo manual)                                     │
     │  • Retries: 1                                                       │
     │  • Tags: [mlops, training, manual]                                  │
     │                                                                     │
     │  Casos de uso:                                                      │
     │  • Reentrenamiento después de agregar nuevos datos etiquetados      │
     │  • Pruebas de nuevos hiperparámetros                                │
     │  • Recovery después de un deploy fallido                            │
     └─────────────────────────────────────────────────────────────────────┘

                                ┌─────────┐
                                │  START  │
                                └────┬────┘
                                     │
                                     ▼
                      ┌─────────────────────┐
                      │   pull_data_from_s3 │
                      │                     │
                      │   dvc pull data-    │
                      │   tickets-train/    │
                      │   dataset.csv.dvc   │
                      │                     │
                      │   Descarga datos    │
                      │   más recientes     │
                      └──────────┬──────────┘
                                 │
                                 ▼
                      ┌─────────────────────┐
                      │     train_model     │
                      │                     │
                      │   python scripts/   │
                      │   train_model.py    │
                      │                     │
                      │   ⏱️ Timeout: 1h    │
                      └──────────┬──────────┘
                                 │
                                 ▼
                      ┌─────────────────────┐
                      │   push_model_to_s3  │
                      │                     │
                      │   dvc add models/   │
                      │   best_model.pkl    │
                      │                     │
                      │   dvc push          │
                      └──────────┬──────────┘
                                 │
                                 ▼
                            ┌─────────┐
                            │   END   │
                            └─────────┘
    """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
     #   COMUNICACIÓN ENTRE TAREAS (XCom)
    st.markdown("<h2 style='color: black;'> COMUNICACIÓN ENTRE TAREAS (XCom) (train_model_manual)</h2>", unsafe_allow_html=True)
    st.markdown("""
        Airflow XCom permite pasar datos entre tareas. El pipeline usa XCom
     para tomar decisiones basadas en resultados de tareas anteriores.
    """)
    
    st.markdown("""
    """, unsafe_allow_html=True)
    st.code("""
     ┌─────────────────────────────────────────────────────────────────────┐
     │                                                                     │
     │                        FLUJO DE XCOMS                               │
     │                                                                     │
     │   ┌─────────────────┐                                               │
     │   │   check_drift   │──┬── drift_detected: bool                     │
     │   └─────────────────┘  └── drift_score: float                       │
     │                                    │                                │
     │                                    ▼                                │
     │   ┌─────────────────┐    ┌─────────────────────┐                    │
     │   │evaluate_perf    │───▶│  decide_retraining  │                    │
     │   └─────────────────┘    └─────────┬───────────┘                    │
     │   current_metrics: dict            │                                │
     │                                    ▼                                │
     │                           should_retrain: bool                      │
     │                           retrain_reasons: list                     │
     │                                    │                                │
     │                                    ▼                                │
     │   ┌─────────────────┐    ┌─────────────────────┐                    │
     │   │save_current_    │───▶│   compare_models    │                    │
     │   │   metrics       │    └─────────┬───────────┘                    │
     │   └─────────────────┘              │                                │
     │   pre_training_metrics: dict       ▼                                │
     │   backup_model_path: str    should_deploy: bool                     │
     │                             improvement: float                      │
     │                             new_f1: float                           │
     │                             old_f1: float                           │
     │                                                                     │
     └─────────────────────────────────────────────────────────────────────┘
            
     """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # VARIABLES DE AIRFLOW (Configurables desde UI)
    st.markdown("<h2 style='color: black;'> VARIABLES DE AIRFLOW (Configurables desde UI)</h2>", unsafe_allow_html=True)
    st.markdown("""
        Variables de airflow desde config.yaml
    """)
    
    st.markdown("""
    """, unsafe_allow_html=True)
    st.code("""
    ┌──────────────────────────────────────────────────────────────────┐
    │                                                                  │
    │  Variable                    Default         Descripción         │
    │  ────────────────────────────────────────────────────────────────│
    │                                                                  │
    │  API_URL                     localhost:8000  URL de la API prod  │
    │                                                                  │
    │  ADMIN_API_KEY               (requerido)     Key para hot reload │
    │                                                                  │
    │  DRIFT_THRESHOLD             0.5             Umbral para drift   │
    │                                                                  │
    │  PERFORMANCE_DROP_THRESHOLD  0.05            Drop F1 permitido   │
    │                                                                  │
    │  MIN_IMPROVEMENT_FOR_DEPLOY  0.01            Mejora mínima para  │
    │                                              hacer deploy        │
    │                                                                  │
    └──────────────────────────────────────────────────────────────────┘
            
     """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # SISTEMA DE NOTIFICACIONES
    st.markdown("<h2 style='color: black;'> SISTEMA DE NOTIFICACIONES </h2>", unsafe_allow_html=True)
    st.markdown("""
        El pipeline envía notificaciones en eventos clave para mantener al
     equipo informado del estado del modelo.
    """)
    
    st.markdown("""
    """, unsafe_allow_html=True)
    st.code("""
     ┌──────────────────────────────────────────────────────────────────┐
     │                                                                  │
     │  Evento                      Canal              Nivel            │
     │  ────────────────────────────────────────────────────────────────│
     │                                                                  │
     │  🚀 Entrenamiento iniciado   Slack/Discord     INFO              │
     │                                                                  │
     │  ✅ Entrenamiento exitoso    Slack/Discord     SUCCESS           │
     │     + métricas del modelo                                        │
     │                                                                  │
     │  ❌ Entrenamiento fallido    Slack/Discord     ERROR             │
     │     + mensaje de error                                           │
     │                                                                  │
     │  ⚠️  Drift detectado         Slack/Discord     WARNING            │
     │     + drift_score                                                │
     │                                                                  │
     │  🎉 Deploy completado        Slack/Discord     SUCCESS           │
     │     + modelo + F1-score                                          │
     │                                                                  │
     │  ⚠️  Modelo no mejoró        Slack/Discord     WARNING            │
     │     + comparación métricas                                       │
     │                                                                  │
     └──────────────────────────────────────────────────────────────────┘
            
     """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    #  DIAGRAMA RESUMEN DE ORQUESTACIÓN
    st.markdown("<h2 style='color: black;'>DIAGRAMA RESUMEN DE ORQUESTACIÓN </h2>", unsafe_allow_html=True)
    st.markdown("""
        En el siguiente diagrama se muestra toda la Orquestación
    """)
    
    st.markdown("""
    """, unsafe_allow_html=True)
    st.code("""
     ┌──────────────────────────────────────────────────────────────────────┐
     │                         AIRFLOW SCHEDULER                            │
     └───────────────────────────────┬──────────────────────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
     ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
     │  mlops_pipeline │   │  monitor_only   │   │  train_manual   │
     │                 │   │                 │   │                 │
     │  ⏰ 6 horas     │   │  ⏰ 1 hora      │   │  🖐️ Manual       │
     │                 │   │                 │   │                 │
     │  ┌───────────┐  │   │  ┌───────────┐  │   │  ┌───────────┐  │
     │  │ MONITOR   │  │   │  │  CHECK    │  │   │  │ PULL DATA │  │
     │  │ • Health  │  │   │  │  DRIFT    │  │   │  │ FROM S3   │  │
     │  │ • Drift   │  │   │  └─────┬─────┘  │   │  └─────┬─────┘  │
     │  │ • Metrics │  │   │        │        │   │        │        │
     │  └─────┬─────┘  │   │  ┌─────┴─────┐  │   │  ┌─────┴─────┐  │
     │        │        │   │  │   GET     │  │   │  │   TRAIN   │  │
     │  ┌─────┴─────┐  │   │  │  METRICS  │  │   │  │   MODEL   │  │
     │  │ DECIDE    │  │   │  └─────┬─────┘  │   │  └─────┬─────┘  │
     │  │ RETRAIN?  │  │   │        │        │   │        │        │
     │  └─────┬─────┘  │   │  ┌─────┴─────┐  │   │  ┌─────┴─────┐  │
     │        │        │   │  │   SAVE    │  │   │  │   PUSH    │  │
     │  ┌─────┴─────┐  │   │  │  METRICS  │  │   │  │   TO S3   │  │
     │  │  TRAIN    │  │   │  └───────────┘  │   │  └───────────┘  │
     │  │  MODEL    │  │   │                 │   │                 │
     │  └─────┬─────┘  │   └─────────────────┘   └─────────────────┘
     │        │        │
     │  ┌─────┴─────┐  │
     │  │ COMPARE   │  │
     │  │ MODELS    │  │
     │  └─────┬─────┘  │
     │        │        │
     │  ┌─────┴─────┐  │
     │  │  DEPLOY   │  │
     │  │ • Git     │  │
     │  │ • DVC     │  │
     │  │ • Reload  │  │
     │  └───────────┘  │
     │                 │
     └─────────────────┘
              │
              ▼
     ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
     │   FastAPI       │      │     AWS S3      │      │    Supabase     │
     │   (Render)      │      │   (Modelos)     │      │  (PostgreSQL)   │
     └─────────────────┘      └─────────────────┘      └─────────────────┘
            
     """, language=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")



        
# ============================================================================
# TAB 6: ENDPOINTS
# ============================================================================
with tab6:
    # Información de endpoints
    st.markdown("<h2 style='color: black;'>📋 Endpoints de la API</h2>", unsafe_allow_html=True)

    # Configuración de la tabla principal de endpoints
    endpoints_df = pd.DataFrame({
        "Endpoint": [
            "GET /", 
            "GET /health",
            "POST /predict",
            "POST /predict/ticket", 
            "POST /predict/batch",
            "POST /predict/tickets/batch",
            "POST /predict/from-db/{ticket_number}",
            "POST /predict/update-db",
            "POST /predict/process-pending",
            "GET /db/health",
            "GET /db/test-update/{ticket_number}",
            "GET /db/tickets/pending",
            "GET /monitoring/drift",
            "GET /monitoring/metrics", 
            "POST /monitoring/save-metrics",
            "POST /admin/reload-model",
            "GET /admin/model-info"
        ],
        "Método": ["GET", "GET", "POST", "POST", "POST", "POST", "POST", "POST", "POST", "GET", "GET", "GET", "GET", "GET", "POST", "POST", "GET"],
        "Categoría": [
            "Salud", "Salud", "Predicción", "Predicción", "Predicción", "Predicción", 
            "BD", "BD", "BD", "BD", "BD", "BD", "Monitoreo", "Monitoreo", "Monitoreo",
            "Admin", "Admin"
        ],
        "Autenticación": [
            "No", "No", "API Key", "API Key", "API Key", "API Key", "API Key", "API Key", "API Key",
            "No", "Admin Key", "API Key", "No", "No", "No", "Admin Key", "Admin Key"
        ],
        "Rate Limit": [
            "60/min", "60/min", "30/min", "30/min", "10/min", "10/min", "30/min", "30/min", "10/min",
            "60/min", "10/min", "30/min", "30/min", "30/min", "10/min", "2/min", "10/min"
        ]
    })

    # Mostrar tabla principal

    st.dataframe(endpoints_df, use_container_width=True, hide_index=True)

    # Ejemplos de uso expandibles

    st.markdown("<h2 style='color: black;'>🔍 Ejemplos de Uso Detallados</h2>", unsafe_allow_html=True)

    with st.expander("🏥 **Endpoints de Salud y Estado**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **GET /** - Health check básico
            ```bash
            curl https://api.example.com/
            ```
            ```json
            {
            "status": "online",
            "model_loaded": true,
            "model_name": "XGBoost",
            "model_f1_score": 0.88
            }
            ```
            """)
        
        with col2:
            st.markdown("""
            **GET /health** - Health check detallado
            ```bash
            curl https://api.example.com/health
            ```
            ```json
            {
            "status": "healthy", 
            "model_loaded": true,
            "drift_detector_ready": true
            }
            ```
            """)

    with st.expander("🎯 **Endpoints de Predicción**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **POST /predict/ticket** - Predicción + BD
            ```bash
            curl -X POST https://api.example.com/predict/ticket \\
            -H "X-API-Key: your-key" \\
            -H "Content-Type: application/json" \\
            -d '{
                "ticket_id": "INC1353571",
                "short_description": "No puedo acceder al sistema",
                "close_notes": "Usuario reporta error de login"
            }'
            ```
            """)
            
            st.markdown("""
            **POST /predict** - Predicción individual
            ```bash
            curl -X POST https://api.example.com/predict \\
            -H "X-API-Key: your-key" \\
            -H "Content-Type: application/json" \\
            -d '{
                "short_description": "Error en el sistema",
                "close_notes": "Usuario no puede acceder"
            }'
            ```
            """)
        
        with col2:
            st.markdown("""
            **POST /predict/tickets/batch** - Lote + BD
            ```bash
            curl -X POST https://api.example.com/predict/tickets/batch \\
            -H "X-API-Key: your-key" \\
            -H "Content-Type: application/json" \\
            -d '{
                "tickets": [
                {"ticket_id": "INC001", "short_description": "Error login"},
                {"ticket_id": "INC002", "short_description": "PC lenta"}
                ]
            }'
            ```
            """)

    with st.expander("🗄️ **Endpoints de Base de Datos**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **POST /predict/from-db/INC1353571**
            ```bash
            curl -X POST https://api.example.com/predict/from-db/INC1353571 \\
            -H "X-API-Key: your-key"
            ```
            """)
            
            st.markdown("""
            **POST /predict/process-pending**
            ```bash
            curl -X POST "https://api.example.com/predict/process-pending?limit=100" \\
            -H "X-API-Key: your-key"
            ```
            """)
        
        with col2:
            st.markdown("""
            **GET /db/tickets/pending**
            ```bash
            curl "https://api.example.com/db/tickets/pending?limit=50" \\
            -H "X-API-Key: your-key"
            ```
            """)
            
            st.markdown("""
            **GET /db/health**
            ```bash
            curl https://api.example.com/db/health
            ```
            ```json
            {
            "database_connected": true,
            "status": "healthy",
            "table_name": "tickets_fiducia"
            }
            ```
            """)

    with st.expander("📊 **Endpoints de Monitoreo**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **GET /monitoring/drift**
            ```bash
            curl https://api.example.com/monitoring/drift
            ```
            ```json
            {
            "drift_detected": true,
            "drift_score": 0.65,
            "details": {
                "ks_test": {"p_value": 0.001},
                "chi_square_test": {"p_value": 0.002}
            }
            }
            ```
            """)
        
        with col2:
            st.markdown("""
            **GET /monitoring/metrics**
            ```bash
            curl https://api.example.com/monitoring/metrics
            ```
            ```json
            {
            "total_predictions": 1500,
            "average_confidence": 0.82,
            "predictions_by_class": {
                "TI": 850, "RRHH": 400, "Finanzas": 150
            }
            }
            ```
            """)

    with st.expander("⚙️ **Endpoints Administrativos**", expanded=False):
        st.markdown("""
        **POST /admin/reload-model** (Requiere Admin Key)
        ```bash
        curl -X POST https://api.example.com/admin/reload-model \\
        -H "X-API-Key: your-admin-key"
        ```
        ```json
        {
        "status": "success",
        "message": "Modelo recargado exitosamente",
        "model_name": "XGBoost",
        "reloaded_at": "2024-01-15T10:30:00Z"
        }
        ```
        """)

    # Resumen por categoría
    st.markdown("### ")
    st.markdown("<h2 style='color: black;'>📊 Resumen por Categoría</h2>", unsafe_allow_html=True)

    categorias_df = pd.DataFrame({
        "Categoría": ["Salud y Estado", "Predicción", "Base de Datos", "Monitoreo", "Administración", "TOTAL"],
        "Endpoints": [2, 4, 6, 3, 2, 17],
        "Autenticación": ["Pública", "API Key", "Mixta", "Pública", "Admin Key", "-"]
    })

    st.dataframe(categorias_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Información adicional

    st.markdown("<h2 style='color: black;'>🔐 Autenticación y Rate Limiting</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        
        st.markdown("""
        <div style="color: black;">
        <strong style="color: black;">Tipos de API Key:</strong>
        <ul style="color: black;">
        <li style="color: black;">🔓 <strong style="color: black;">Sin autenticación</strong>: Health checks, monitoreo</li>
        <li style="color: black;">🔑 <strong style="color: black;">API_KEY</strong>: Predicciones, consultas BD</li>
        <li style="color: black;">🛡️ <strong style="color: black;">ADMIN_API_KEY</strong>: Operaciones críticas</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="color: black;">
        <strong style="color: black;">Rate Limits:</strong>
        <ul style="color: black;">
        <li style="color: black;">🟢 <strong style="color: black;">60/min</strong>: Health checks</li>
        <li style="color: black;">🟡 <strong style="color: black;">30/min</strong>: Predicciones individuales</li>
        <li style="color: black;">🟠 <strong style="color: black;">10/min</strong>: Lotes, administrativos</li>
        <li style="color: black;">🔴 <strong style="color: black;">2/min</strong>: Reload modelo</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

