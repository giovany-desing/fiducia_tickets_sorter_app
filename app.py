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
background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
padding: 3rem 2rem;
border-radius: 16px;
margin-bottom: 3rem;
box-shadow: 0 10px 40px rgba(30, 41, 59, 0.3);
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
background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
padding: 2.5rem 1.5rem;
border-radius: 10px;
border-left: 4px solid #1e3a8a;
margin: 1rem 0;
color: #ffffff;
}

.warning-box h4 {
color: #ffffff;
margin-top: 0;
font-weight: 600;
}

.warning-box p {
color: #ffffff;
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
/* ========== TABS PREMIUM ========== */
.stTabs [data-baseweb="tab-list"] {
gap: 12px;
background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
padding: 1rem;
border-radius: 16px;
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.08);
border: 1px solid rgba(226, 232, 240, 0.8);
margin-bottom: 2rem;
}

.stTabs [data-baseweb="tab"] {
height: 56px;
padding: 0 28px;
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border-radius: 12px;
color: #64748b;
font-weight: 600;
font-size: 0.95rem;
border: 2px solid transparent;
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
position: relative;
overflow: hidden;
}

.stTabs [data-baseweb="tab"]::before {
content: '';
position: absolute;
top: 0;
left: -100%;
width: 100%;
height: 100%;
background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
transition: left 0.5s;
}

.stTabs [data-baseweb="tab"]:hover::before {
left: 100%;
}

.stTabs [data-baseweb="tab"]:hover {
background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
color: #1e293b;
transform: translateY(-2px);
box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
border-color: #cbd5e1;
}

.stTabs [aria-selected="true"] {
background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1e40af 100%) !important;
color: white !important;
box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4), 0 4px 12px rgba(59, 130, 246, 0.3) !important;
border: 2px solid rgba(255, 255, 255, 0.3) !important;
transform: translateY(-2px);
font-weight: 700;
position: relative;
}

.stTabs [aria-selected="true"]::after {
content: '';
position: absolute;
bottom: 0;
left: 0;
right: 0;
height: 3px;
background: linear-gradient(90deg, #60a5fa, #3b82f6, #2563eb);
border-radius: 0 0 12px 12px;
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
background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
color: white;
border: none;
padding: 0.75rem 2rem;
font-weight: 600;
border-radius: 8px;
box-shadow: 0 4px 14px rgba(30, 41, 59, 0.3);
transition: all 0.2s;
}

.stButton > button:hover {
transform: translateY(-2px);
box-shadow: 0 6px 20px rgba(30, 41, 59, 0.4);
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
border-color: #334155;
box-shadow: 0 0 0 3px rgba(30, 41, 59, 0.1);
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
border-color: #334155;
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
border-left: 4px solid #334155;
box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.tech-category h3 {
color: #1e293b;
margin-top: 0;
margin-bottom: 1rem;
}

/* ========== FLOW PIPELINE ========== */
.flow-container {
background: #f8fafc;
padding: 2rem;
border-radius: 12px;
margin: 2rem 0;
border: 1px solid #e2e8f0;
}

.flow-pipeline {
display: flex;
flex-wrap: wrap;
align-items: center;
justify-content: center;
gap: 0.75rem;
margin: 1.5rem 0;
}

.flow-step {
background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
border: 2px solid #334155;
border-radius: 10px;
padding: 1rem 1.25rem;
font-size: 0.875rem;
font-weight: 600;
color: #475569;
box-shadow: 0 2px 8px rgba(30, 41, 59, 0.1);
transition: all 0.3s ease;
text-align: center;
min-width: 140px;
flex: 0 1 auto;
}

.flow-step small {
color: #64748b;
font-size: 0.75rem;
display: block;
margin-top: 0.25rem;
}

.flow-step:hover {
transform: translateY(-3px);
box-shadow: 0 4px 12px rgba(30, 41, 59, 0.2);
border-color: #1e40af;
}

.flow-arrow {
color: #475569;
font-size: 1.25rem;
font-weight: bold;
margin: 0 0.25rem;
}

.flow-time {
background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
color: white;
padding: 0.75rem 1.5rem;
border-radius: 8px;
font-weight: 700;
text-align: center;
margin-top: 1.5rem;
display: inline-block;
box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
}

@media (max-width: 768px) {
.flow-pipeline {
flex-direction: column;
}
.flow-arrow {
transform: rotate(90deg);
margin: 0.5rem 0;
}
}

/* ========== VERTICAL PIPELINE ========== */
.vertical-pipeline {
display: flex;
flex-direction: column;
gap: 1.5rem;
margin: 2rem 0;
}

.pipeline-step {
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border: 2px solid #334155;
border-left: 5px solid #1e40af;
border-radius: 12px;
padding: 1.5rem;
box-shadow: 0 4px 12px rgba(30, 41, 59, 0.1);
transition: all 0.3s ease;
}

.pipeline-step:hover {
transform: translateX(5px);
box-shadow: 0 6px 16px rgba(30, 41, 59, 0.15);
border-left-color: #2563eb;
}

.pipeline-step-header {
color: #1e293b;
font-size: 1.25rem;
font-weight: 700;
margin-bottom: 1rem;
display: flex;
align-items: center;
gap: 0.75rem;
}

.pipeline-step-content {
color: #475569;
line-height: 1.8;
margin-top: 0.75rem;
}

.pipeline-step-content ul {
margin: 0.5rem 0;
padding-left: 1.5rem;
}

.pipeline-step-content li {
margin: 0.5rem 0;
color: #64748b;
}

.pipeline-step-content code {
background: #f1f5f9;
padding: 0.2rem 0.5rem;
border-radius: 4px;
font-family: 'Fira Code', monospace;
color: #1e40af;
font-size: 0.875rem;
}

.pipeline-arrow-down {
text-align: center;
color: #475569;
font-size: 1.5rem;
font-weight: bold;
margin: -0.5rem 0;
}

.pipeline-substeps {
display: flex;
gap: 1rem;
margin-top: 1rem;
flex-wrap: wrap;
}

.pipeline-substep {
background: #f8fafc;
border: 1px solid #e2e8f0;
border-radius: 8px;
padding: 0.75rem 1rem;
font-size: 0.875rem;
color: #475569;
flex: 1;
min-width: 150px;
}

/* ========== ROAD PIPELINE (Carretera sinuosa) ========== */
.road-pipeline {
position: relative;
padding: 4rem 2rem;
margin: 2rem 0;
background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
border-radius: 20px;
min-height: 2000px;
}


.road-step {
position: relative;
z-index: 2;
margin: 3rem 0;
display: flex;
align-items: center;
min-height: 120px;
}

.road-step.step-left {
flex-direction: row;
justify-content: flex-start;
padding-right: 50%;
}

.road-step.step-right {
flex-direction: row-reverse;
justify-content: flex-end;
padding-left: 50%;
}

.road-step-number {
width: 70px;
height: 70px;
border-radius: 50%;
display: flex;
align-items: center;
justify-content: center;
font-weight: 700;
font-size: 1.5rem;
color: white;
box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25), 0 0 0 4px rgba(255, 255, 255, 0.8);
margin: 0 2rem;
flex-shrink: 0;
position: relative;
z-index: 3;
border: 3px solid white;
}

.road-step:nth-child(1) .road-step-number { background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); }
.road-step:nth-child(2) .road-step-number { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
.road-step:nth-child(3) .road-step-number { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }
.road-step:nth-child(4) .road-step-number { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.road-step:nth-child(5) .road-step-number { background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); }
.road-step:nth-child(6) .road-step-number { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
.road-step:nth-child(7) .road-step-number { background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); }
.road-step:nth-child(8) .road-step-number { background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); }
.road-step:nth-child(9) .road-step-number { background: linear-gradient(135deg, #84cc16 0%, #65a30d 100%); }
.road-step:nth-child(10) .road-step-number { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); }
.road-step:nth-child(11) .road-step-number { background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); }
.road-step:nth-child(12) .road-step-number { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
.road-step:nth-child(13) .road-step-number { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }
.road-step:nth-child(14) .road-step-number { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.road-step:nth-child(15) .road-step-number { background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); }
.road-step:nth-child(16) .road-step-number { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
.road-step:nth-child(17) .road-step-number { background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); }
.road-step:nth-child(18) .road-step-number { background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); }
.road-step:nth-child(19) .road-step-number { background: linear-gradient(135deg, #84cc16 0%, #65a30d 100%); }
.road-step:nth-child(20) .road-step-number { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); }

.road-step-box {
flex: 1;
max-width: 500px;
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border: 2px solid #334155;
border-left: 5px solid #1e40af;
border-radius: 12px;
padding: 1.5rem;
box-shadow: 0 4px 16px rgba(30, 41, 59, 0.12);
transition: all 0.3s ease;
}

.road-step-box:hover {
transform: translateY(-4px) translateX(5px);
box-shadow: 0 8px 24px rgba(30, 41, 59, 0.18);
border-left-color: #2563eb;
}

.road-step-header {
color: #1e293b;
font-size: 1.15rem;
font-weight: 700;
margin-bottom: 0.75rem;
display: flex;
align-items: center;
gap: 0.5rem;
}

.road-step-content {
color: #475569;
line-height: 1.7;
font-size: 0.9rem;
}

.road-step-content ul {
margin: 0.5rem 0;
padding-left: 1.25rem;
}

.road-step-content li {
margin: 0.4rem 0;
color: #64748b;
}

.road-step-content code {
background: #f1f5f9;
padding: 0.2rem 0.4rem;
border-radius: 4px;
font-family: 'Fira Code', monospace;
color: #1e40af;
font-size: 0.85rem;
}

@media (max-width: 768px) {
.road-step {
flex-direction: column !important;
padding: 0 !important;
}

.road-step-number {
margin: 1rem 0;
}

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
<h1>🎯 Sistema MLOps de Clasificación Inteligente de Tickets</h1>
</div>
""", unsafe_allow_html=True)



# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
"📖 Overview",
"🧠 Pipeline de entrenamiento", 
"🔢 Pipeline clasificación",
"🔄 Monitoreo con Apache Airflow",
"🎯 Endpoints",
"💻 Ver software"
])

# ============================================================================
# TAB 1: OVERVIEW
# ============================================================================
with tab1:
    st.markdown("<h2 style='color: black;'>Introducción</h2>", unsafe_allow_html=True)

    st.markdown("""
Sistema de producción enterprise que revoluciona la gestión de tickets de soporte mediante Deep NLP en español y MLOps automático, alcanzando un 98.35% de precisión en clasificación multiclase.

Implementa un pipeline completo de **Procesamiento de Lenguaje Natural** con tokenización avanzada, stemming Snowball optimizado para español, eliminación inteligente de stopwords y vectorización
TF-IDF de 5000 dimensiones, transformando texto no estructurado en insights accionables en menos de 500ms. El sistema no solo predice — aprende, se adapta y se auto-optimiza mediante drift
detection tri-dimensional que monitorea cambios en distribución de datos, conceptos y vocabulario.

A diferencia de soluciones tradicionales que requieren intervención manual constante, este proyecto implementa auto-healing inteligente: detecta degradación de rendimiento mediante análisis
estadístico (KS-test, Chi-square), se retrain automáticamente cada 6 horas solo cuando es necesario, y despliega nuevas versiones sin downtime. La arquitectura dual de orquestación **(Apache
Airflow + GitHub Actions)** garantiza operación continua tanto en entornos cloud como on-premise, mientras que el versionamiento completo con DVC + MLflow asegura reproducibilidad y trazabilidad de
cada decisión del modelo — cumpliendo estándares de model governance para industrias reguladas.

**Valor de Mercado:** Elimina el 100% del trabajo manual de clasificación de tickets, reduciendo tiempo de respuesta de horas a milisegundos y **costos operativos en un 70-80%**. La capacidad de procesar
lenguaje natural en español con técnicas de NLP state-of-the-art (comparable a soluciones comerciales como AWS Comprehend o Google Cloud NLP, pero customizado y auto-recuperable) posiciona este
sistema como solución enterprise-ready para cualquier organización que maneje 10K+ tickets mensuales en mercados hispanohablantes.

""")

    st.markdown("<h2 style='color: black; margin-top: 2rem; margin-bottom: 1.5rem;'>Flujo de Clasificación</h2>", unsafe_allow_html=True)

    st.markdown("""
<div class="flow-container">
<div class="flow-pipeline">
<div class="flow-step">📝 Ticket</div>
<span class="flow-arrow">→</span>
<div class="flow-step">🔐 Auth API Key</div>
<span class="flow-arrow">→</span>
<div class="flow-step">🧹 NLP Preprocessing<br/><small>Tokenización + Lowercase<br/>+ Stopwords + Stemming</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step">🔢 TF-IDF<br/><small>Vectorization (5000D)</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step">🤖 Gradient Boosting<br/><small>Prediction</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step">✅ Clasificación<br/><small>TI/RRHH/Finanzas/Ops</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step">💾 Logging +<br/><small>PostgreSQL insert result clasitication</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step">📤 Response JSON</div>
</div>
<div style="text-align: center;">
<div class="flow-time">⚡ Tiempo total: &lt;500ms</div>
</div>
</div>
    """, unsafe_allow_html=True)
    
    # Nota sobre procesamiento batch
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                border: 2px solid #f59e0b; 
                border-radius: 10px; 
                padding: 1.25rem; 
                margin: 1.5rem 0;
                box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);">
    <p style="color: #92400e; 
               font-weight: 600; 
               margin: 0; 
               font-size: 1rem;
               line-height: 1.6;">
    <strong>📌 NOTA:</strong> El proyecto está diseñado para procesar tickets en batch.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    
    # Problem vs Solution

    st.markdown("<h2 style='color: black;'>💡 Problema y Solución</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
<div class="warning-box">
<h4>🔴 Situación Actual</h4>
<p>Una de mis tareas era clasificar tickets de soporte manualmente, para luego ser analizados en looker studio y entregarle a los clientes a final de mes un informe general del comportamiento de soporte de las aplicaciones que la organización tenía a cargo, generando cuellos de botella operativos críticos, yo tardaba 60-70% de mi tiempo solo clasificando tickets de manera manual.</p>
<p>Este proceso manual no escalaba y representaba costos operativos masivos no solo en la empresa en la que colaboraba sino en empresas con 10K+ tickets mensuales. Además, los sistemas
tradicionales de clasificación se degradan silenciosamente con el tiempo — nadie detecta cuándo el modelo deja de funcionar hasta que ya es tarde.</p>
</div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="success-box">
<h4>🟢 La Solución</h4>
<p>Construí un sistema MLOps que elimina completamente la clasificación manual mediante NLP avanzado en español, alcanzando 98.35% de precisión en tiempo real (&lt;500ms). Va más allá de la predicción básica:
implementa auto-healing inteligente con drift detection tri-dimensional que monitorea 24/7 cambios en datos, vocabulario y conceptos, retrenándose automáticamente cada 6 horas solo cuando detecta
degradación estadísticamente significativa. El pipeline completo de NLP (tokenización + stemming Snowball + TF-IDF 5000D) procesa lenguaje natural desestructurado y lo transforma en
clasificaciones accionables, actualizando automáticamente la base de datos y enrutando tickets al departamento correcto sin intervención humana. Con arquitectura enterprise-grade (FastAPI +
Airflow + DVC + MLflow), despliega nuevas versiones sin downtime, versiona cada decisión para auditoría, y garantiza reproducibilidad total — cumpliendo estándares de producción que sistemas
comerciales como AWS Comprehend no ofrecen en español con esta personalización y auto-recuperación.</p>
<p>Impacto: Reduce tiempo de clasificación de horas a milisegundos, elimina errores de enrutamiento en 98%, libera 70% del tiempo de agentes para resolver problemas reales, y disminuye costos
operativos en 70-80% — todo mientras se auto-mantiene y mejora continuamente sin supervisión humana.</p>
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
    
    

# ============================================================================
# TAB 2: PIPELINE DE ENTRENAMIERNO
# ============================================================================
with tab2:
    st.markdown("""
El sistema se auto-mantiene mediante un ciclo continuo cada 6 horas donde GitHub Actions ejecuta monitoreo automático que usa SciPy para detectar drift estadístico (KS-test, Chi-square) y scikit-learn para evaluar performance real con datos de Supabase; cuando detecta problemas (drift > 0.5 o F1 cae > 5%), se auto-retrain descargando dataset actualizado vía DVC desde S3, re-optimiza hiperparámetros con Optuna considerando patrones emergentes en datos nuevos, entrena 7 modelos y selecciona el mejor; si la mejora es ≥ 1%, despliega automáticamente sin downtime haciendo hot-reload en FastAPI, versiona con DVC+MLflow para trazabilidad completa, y notifica al equipo — todo sin intervención humana, logrando que el modelo se adapte a cambios en vocabulario, distribución de datos y conceptos emergentes (como nuevas herramientas tipo "Teams" o "Zoom" que no existían en entrenamiento original), previniendo degradación silenciosa y manteniendo F1-score > 0.98 en producción de forma perpetua.
""")
    
    st.markdown("""<div class="flow-container">
<div class="flow-pipeline">
<div class="flow-step">📅 DÍA 1<br/><small>F1=0.9835 funciona perfectamente</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step">📅 DÍA 15<br/><small>Empresa adopta "Microsoft Teams"</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step">👥 Usuarios reportan<br/><small>"Teams", "reunión virtual", "compartir pantalla" (vocabulario nuevo)</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step">⏰ HORA 360<br/><small>GitHub Actions CRON activa monitoreo</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step" style="border-color: #ef4444; background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);">📊 Detección<br/><small>Vocabulary Drift 12% + F1=0.9280 (-5.6%)</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step" style="border-color: #10b981; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);">🔄 AUTO-RETRAIN<br/><small>DVC descarga dataset + Optuna re-optimiza + Entrena 7 modelos</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step" style="border-color: #8b5cf6; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);">🏆 Mejor resultado<br/><small>F1=0.9890 (+0.55% mejora)</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step" style="border-color: #8b5cf6; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);">✅ Deploy autorizado<br/><small>Mejora ≥1% → DVC push a S3</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step" style="border-color: #8b5cf6; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);">🔄 API hot-reload<br/><small>Sin downtime</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step">📊 MLflow<br/><small>Registra todo</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step">🔔 Notificación<br/><small>"Sistema auto-recuperado, F1=0.9890"</small></div>
<span class="flow-arrow">→</span>
<div class="flow-step" style="border-color: #8b5cf6; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);">🎯 Modelo actualizado<br/><small>Entiende términos nuevos, performance restaurada</small></div>
</div>
<div style="text-align: center; margin-top: 1.5rem;">
<div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border: 2px solid #3b82f6; border-radius: 12px; padding: 1.5rem; display: inline-block; max-width: 900px;">
<div style="color: #1e40af; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">🏆 Resultado</div>
<div style="color: #1e293b; font-size: 0.95rem; line-height: 1.6;">Modelo entrenado y desplegado automáticamente (<strong>NOTA: el usuario de este producto garantiza una muestra de la data de entrenamiento con los nuevos parámetros subiéndola al bucket de S3 para hacer el reentrenamiento, este sistema está diseñado con alertas que le indican al usuario cuando hay cambios en los vocabularios</strong>)</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: black;'>🔄 Pipeline de Reentrenamiento Automático</h2>", unsafe_allow_html=True)
    
    st.markdown("""<div class="road-pipeline">
<div class="road-step step-left">
<div class="road-step-number">01</div>
<div class="road-step-box">
<div class="road-step-header">🚀 GitHub Actions (Orquestador)</div>
<div class="road-step-content">
<p><strong>⏰ CRON Schedule:</strong> Cada 6 horas (0 */6 * * *)</p>
<p>Workflow: <code>monitor_and_retrain.yml</code> se activa automáticamente</p>
<p><strong>Rol:</strong> Orquesta todo el proceso de monitoreo y reentrenamiento sin intervención humana.</p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">02</div>
<div class="road-step-box">
<div class="road-step-header">🏥 FastAPI (API de Producción)</div>
<div class="road-step-content">
<p><strong>Health Check:</strong> GET <code>/health</code></p>
<ul>
<li>Verifica que API esté disponible</li>
<li>Response: <code>{"status": "healthy", "model_version": "...", "f1_score": 0.9835}</code></li>
</ul>
<p><strong>Rol:</strong> Expone endpoints para verificar estado del sistema y obtener métricas.</p>
</div>
</div>
</div>
<div class="road-step step-left">
<div class="road-step-number">03</div>
<div class="road-step-box">
<div class="road-step-header">📊 Supabase (Base de Datos PostgreSQL)</div>
<div class="road-step-content">
<p><strong>Query últimas predicciones:</strong></p>
<pre><code>SELECT ticket_id, texto, prediction, label_real, probability, timestamp
FROM tickets_fiducia
WHERE timestamp > NOW() - INTERVAL '48 hours'
AND label_real IS NOT NULL
LIMIT 500</code></pre>
<p><strong>Rol:</strong> Almacena todas las predicciones históricas con sus labels reales. Permite evaluar performance real del modelo en producción.</p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">04</div>
<div class="road-step-box">
<div class="road-step-header">🧹 NLTK + Custom Preprocessing (NLP)</div>
<div class="road-step-content">
<p><strong>Procesa textos nuevos igual que en entrenamiento:</strong></p>
<p>Ejemplo: "Mi computadora no funciona"</p>
<p>→ Tokenización → Lowercase → Stopwords → Stemming</p>
<p>→ "comput funcion"</p>
<p><strong>Rol:</strong> Mantiene consistencia en el preprocesamiento. Los textos nuevos pasan por el mismo pipeline NLP que el entrenamiento original.</p>
</div>
</div>
</div>
<div class="road-step step-left">
<div class="road-step-number">05</div>
<div class="road-step-box">
<div class="road-step-header">📈 Python SciPy + NumPy (Análisis Estadístico)</div>
<div class="road-step-content">
<p><strong>Drift Detection (3 dimensiones):</strong></p>
<ul>
<li><strong>A) Data Drift - KS Test:</strong> Compara distribución de longitud de texto (producción vs entrenamiento). <code>scipy.stats.ks_2samp()</code> p-value < 0.05 → DRIFT detectado</li>
<li><strong>B) Concept Drift - Chi-Square Test:</strong> Compara distribución de clases predichas. <code>scipy.stats.chisquare()</code> p-value < 0.05 → CONCEPT DRIFT</li>
<li><strong>C) Vocabulary Drift:</strong> Detecta términos nuevos no vistos. Growth rate > 10% → VOCAB DRIFT</li>
</ul>
<p><strong>Rol:</strong> Herramientas estadísticas que detectan cuándo los datos de producción divergen significativamente del entrenamiento.</p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">06</div>
<div class="road-step-box">
<div class="road-step-header">📉 scikit-learn (Evaluación de Performance)</div>
<div class="road-step-content">
<p><strong>Calcula F1-score actual en producción:</strong></p>
<ul>
<li>Usa predicciones con labels reales (datos etiquetados manualmente post-predicción)</li>
<li><code>from sklearn.metrics import f1_score</code></li>
<li><code>f1_actual = f1_score(y_true=labels_reales, y_pred=predicciones, average='macro')</code></li>
<li>Compara: f1_actual (ej: 0.9300) vs f1_baseline (0.9835)</li>
<li>Drop = (0.9835 - 0.9300) / 0.9835 = 5.4% → DEGRADACIÓN detectada</li>
</ul>
<p><strong>Rol:</strong> Mide qué tan bien está funcionando el modelo en datos reales. Detecta cuando performance cae.</p>
</div>
</div>
</div>
<div class="road-step step-left">
<div class="road-step-number">07</div>
<div class="road-step-box">
<div class="road-step-header">⚖️ Python (Lógica de Decisión)</div>
<div class="road-step-content">
<p><strong>Evaluación:</strong></p>
<p><code>drift_score = (data_drift_weight × 0.4) + (concept_drift_weight × 0.4) + (vocab_drift_weight × 0.2)</code></p>
<p><strong>¿Reentrenar?</strong></p>
<ul>
<li><strong>SI</strong> (drift_score > 0.5) <strong>O</strong> (f1_drop > 5%): → <strong>REENTRENAR ✅</strong></li>
<li><strong>ELSE:</strong> → MANTENER modelo actual, seguir monitoreando ❌</li>
</ul>
<p><strong>Rol:</strong> Lógica inteligente que previene reentrenamiento innecesario. Solo entrena cuando hay evidencia estadística de problemas.</p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">08</div>
<div class="road-step-box">
<div class="road-step-header">📦 DVC (Data Version Control)</div>
<div class="road-step-content">
<p><strong>Obtiene datos actualizados:</strong></p>
<ul>
<li><code>dvc pull data-tickets-train/dataset_tickets.csv</code></li>
<li>Descarga desde S3 la última versión del dataset</li>
<li>Dataset ahora incluye: datos originales + nuevos tickets etiquetados de producción</li>
</ul>
<p><strong>Rol:</strong> Versionamiento de datos. Garantiza que usamos dataset actualizado y que podemos volver a cualquier versión anterior.</p>
</div>
</div>
</div>
<div class="road-step step-left">
<div class="road-step-number">09</div>
<div class="road-step-box">
<div class="road-step-header">🔬 Optuna (Optimización de Hiperparámetros)</div>
<div class="road-step-content">
<p><strong>Re-optimiza hiperparámetros con datos nuevos:</strong></p>
<ul>
<li>10 trials × 2-fold CV</li>
<li>Busca: mejores n_estimators, max_depth, learning_rate, etc.</li>
<li>Considera datos nuevos que pueden requerir hiperparámetros diferentes</li>
</ul>
<p><strong>Rol:</strong> Encuentra la mejor configuración para el modelo considerando los datos actualizados. No asume que hiperparámetros antiguos siguen siendo óptimos.</p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">10</div>
<div class="road-step-box">
<div class="road-step-header">🤖 scikit-learn + XGBoost + LightGBM (Entrenamiento)</div>
<div class="road-step-content">
<p><strong>Entrena 7 modelos nuevamente:</strong></p>
<ul>
<li>Mismo proceso que entrenamiento inicial</li>
<li>Usa dataset expandido (original + datos nuevos)</li>
<li>Selecciona mejor modelo (puede o no ser el mismo algoritmo)</li>
</ul>
<p><strong>Rol:</strong> Bibliotecas de ML que ejecutan el entrenamiento. Aprenden patrones de datos actualizados.</p>
</div>
</div>
</div>
<div class="road-step step-left">
<div class="road-step-number">11</div>
<div class="road-step-box">
<div class="road-step-header">🆚 Python (Comparación de Modelos)</div>
<div class="road-step-content">
<p><strong>Compara modelo_nuevo vs modelo_actual:</strong></p>
<ul>
<li>f1_nuevo = 0.9870 (entrenado con datos actualizados)</li>
<li>f1_actual = 0.9835 (modelo en producción)</li>
<li>Mejora = 0.9870 - 0.9835 = 0.0035 = +0.35%</li>
</ul>
<p><strong>¿Desplegar?</strong></p>
<ul>
<li><strong>SI</strong> mejora >= 1% (threshold): → <strong>DEPLOY nuevo modelo ✅</strong></li>
<li><strong>ELSE:</strong> → MANTENER modelo actual ❌</li>
</ul>
<p><strong>Rol:</strong> Protección contra deploys que no mejoran significativamente. Previene cambios innecesarios.</p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">12</div>
<div class="road-step-box">
<div class="road-step-header">📤 DVC + AWS S3 (Almacenamiento)</div>
<div class="road-step-content">
<p><strong>Versiona y sube nuevo modelo:</strong></p>
<ul>
<li><code>joblib.dump(modelo_nuevo, 'models/best_model.pkl')</code></li>
<li><code>dvc add models/best_model.pkl</code> → genera hash MD5 nuevo</li>
<li><code>dvc push</code> → sube a S3: <code>s3://bucket/models/b4c7e9f1...</code></li>
<li>Git commit del .dvc file → historial completo de versiones</li>
</ul>
<p><strong>Rol:</strong> S3 almacena modelos (objetos grandes), DVC trackea versiones (lightweight pointers).</p>
</div>
</div>
</div>
<div class="road-step step-left">
<div class="road-step-number">13</div>
<div class="road-step-box">
<div class="road-step-header">📊 MLflow (Registro de Experimentos)</div>
<div class="road-step-content">
<p><strong>Registra experimento de reentrenamiento:</strong></p>
<ul>
<li><code>mlflow.log_params({'retrain_reason': 'drift_detected', 'drift_score': 0.62})</code></li>
<li><code>mlflow.log_metrics({'f1_new': 0.9870, 'f1_old': 0.9835, 'improvement': 0.35})</code></li>
<li><code>mlflow.sklearn.log_model(modelo_nuevo, "model")</code></li>
<li>Version: v2.3 (auto-incrementa)</li>
</ul>
<p><strong>Rol:</strong> Auditoría completa. Permite saber POR QUÉ se reentrenó, CUÁNDO, y CUÁL fue el resultado. Trazabilidad para regulación/compliance.</p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">14</div>
<div class="road-step-box">
<div class="road-step-header">🔄 FastAPI (Hot Reload)</div>
<div class="road-step-content">
<p><strong>Recarga modelo sin downtime:</strong></p>
<ul>
<li>Endpoint: POST <code>/admin/reload-model</code> (autenticado con ADMIN_API_KEY)</li>
<li>API ejecuta: <code>dvc pull models/best_model.pkl</code> → descarga desde S3</li>
<li><code>new_model = joblib.load('models/best_model.pkl')</code></li>
<li><code>global model_pipeline; model_pipeline = new_model</code> (swap atómico)</li>
<li>Uvicorn NO reinicia → requests continúan sin interrupción</li>
</ul>
<p><strong>Rol:</strong> Zero-downtime deployment. API actualiza modelo en memoria sin afectar disponibilidad del servicio.</p>
</div>
</div>
</div>
<div class="road-step step-left">
<div class="road-step-number">15</div>
<div class="road-step-box">
<div class="road-step-header">🔔 Webhooks (Slack, Discord, Telegram)</div>
<div class="road-step-content">
<p><strong>Notifica resultado:</strong></p>
<p>"✅ Auto-retrain completado: Drift detectado (score: 0.62)<br>
Nuevo modelo: Gradient Boosting v2.3<br>
F1-score: 0.9870 (+0.35% mejora)<br>
Deployed automáticamente a producción"</p>
<p><strong>Rol:</strong> Mantiene al equipo informado de cambios automáticos. Transparencia en operaciones MLOps.</p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">16</div>
<div class="road-step-box">
<div class="road-step-header">📄 GitHub Actions (Reporte)</div>
<div class="road-step-content">
<p><strong>Genera summary en UI de GitHub:</strong></p>
<ul>
<li>Tabla: drift scores, performance metrics, decisión tomada</li>
<li>Link a MLflow run</li>
<li>Confusion matrix del modelo nuevo</li>
<li>Comparativa antes/después</li>
</ul>
<p><strong>Rol:</strong> Documentación automática de cada ciclo de reentrenamiento. Útil para debugging y análisis histórico.</p>
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("<h2 style='color: black;'>📊 Resumen por Herramienta</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .stack-table {
        width: 100%;
        border-collapse: collapse;
        margin: 2rem 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stack-table thead {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
    }
    
    .stack-table th {
        padding: 1rem 1.25rem;
        text-align: left;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.5px;
        border-bottom: 3px solid #1e3a8a;
    }
    
    .stack-table tbody tr {
        background: #ffffff;
        transition: all 0.2s ease;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .stack-table tbody tr:nth-child(even) {
        background: #f8fafc;
    }
    
    .stack-table tbody tr:hover {
        background: #eff6ff;
        transform: translateX(4px);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
    }
    
    .stack-table td {
        padding: 1rem 1.25rem;
        color: #1e293b;
        font-size: 0.95rem;
        line-height: 1.6;
        vertical-align: top;
    }
    
    .stack-table td:first-child {
        font-weight: 600;
        color: #1e40af;
        width: 20%;
    }
    
    .stack-table td:nth-child(2) {
        width: 25%;
        color: #475569;
    }
    
    .stack-table td:nth-child(3) {
        width: 55%;
        color: #64748b;
    }
    
    .stack-table tbody tr:last-child {
        border-bottom: none;
    }
    </style>
    
    <table class="stack-table">
        <thead>
            <tr>
                <th>Stack</th>
                <th>Rol en Reentrenamiento</th>
                <th>Acción Específica</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>GitHub Actions</td>
                <td>Orquestador</td>
                <td>CRON cada 6h → ejecuta workflow completo</td>
            </tr>
            <tr>
                <td>FastAPI</td>
                <td>API Producción</td>
                <td>Expone /health, /metrics, /reload-model</td>
            </tr>
            <tr>
                <td>Supabase</td>
                <td>Almacén de Datos</td>
                <td>Query predicciones históricas con labels</td>
            </tr>
            <tr>
                <td>NLTK</td>
                <td>Preprocessing NLP</td>
                <td>Procesa textos nuevos (consistencia)</td>
            </tr>
            <tr>
                <td>SciPy/NumPy</td>
                <td>Análisis Estadístico</td>
                <td>KS-test, Chi-square, detección drift</td>
            </tr>
            <tr>
                <td>scikit-learn</td>
                <td>Evaluación + Training</td>
                <td>F1-score producción + entrenamiento modelos</td>
            </tr>
            <tr>
                <td>DVC</td>
                <td>Versionamiento Datos/Modelos</td>
                <td>Pull dataset, push modelo nuevo, tracking</td>
            </tr>
            <tr>
                <td>AWS S3</td>
                <td>Storage</td>
                <td>Almacena datasets y modelos versionados</td>
            </tr>
            <tr>
                <td>Optuna</td>
                <td>Optimización</td>
                <td>Re-optimiza hiperparámetros con datos nuevos</td>
            </tr>
            <tr>
                <td>XGBoost/LightGBM</td>
                <td>Algoritmos ML</td>
                <td>Entrenamiento de modelos boosting</td>
            </tr>
            <tr>
                <td>MLflow</td>
                <td>Experiment Tracking</td>
                <td>Registra por qué/cuándo/resultado reentrenamiento</td>
            </tr>
            <tr>
                <td>Webhooks</td>
                <td>Notificaciones</td>
                <td>Alerta equipo de cambios automáticos</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)


# ============================================================================
# TAB 3: PIPELINE DE CLASIFICACION
# ============================================================================
with tab3:
    st.markdown("""
        <h3 style='color: #2563eb; font-size: 1rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem;'>Capacidad de Procesamiento Masivo</h3>
        <p style='color: #1e293b; line-height: 1.7; margin-bottom: 1.5rem;'>
        Además de clasificar tickets individuales en tiempo real, el sistema implementa un endpoint especializado para procesamiento batch que permite clasificar hasta 100 tickets simultáneamente en una sola request, optimizado para escenarios de migración de datos históricos, procesamiento nocturno de backlogs, o integración con sistemas legacy que acumulan tickets antes de enviarlos.
        </p>
        
        <h3 style='color: #2563eb; font-size: 1rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem;'>Funcionamiento del Batch Processing</h3>
        <p style='color: #1e293b; line-height: 1.7; margin-bottom: 1.5rem;'>
        Cuando una empresa tiene un backlog de 500 tickets sin clasificar o recibe un dump masivo de tickets desde otro sistema, en lugar de hacer 500 requests individuales (consumiendo rate limit y tiempo), puede usar el endpoint <code>POST /predict/tickets/batch</code> enviando un array de tickets. El sistema aprovecha la vectorización paralela de scikit-learn y NumPy broadcasting para procesar todos los textos en un solo pipeline: NLTK preprocesa los 100 textos en paralelo, TfidfVectorizer los transforma en una matriz sparse (100, 5000) de una sola vez, y el modelo Gradient Boosting ejecuta predicción matricial sobre todo el batch, retornando las 100 clasificaciones con sus probabilidades en menos de 5 segundos — 100x más rápido que 100 requests individuales.
        </p>
        
        <h3 style='color: #2563eb; font-size: 1rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem;'>Características Técnicas del Batch</h3>
        <p style='color: #1e293b; line-height: 1.7; margin-bottom: 1.5rem;'>
        El procesamiento batch mantiene las mismas garantías de calidad que la inferencia individual: mismo preprocessing NLP (tokenización, stemming, stopwords), misma extracción de features TF-IDF, mismo modelo versionado, y logging completo de todas las predicciones para drift detection. La diferencia está en la eficiencia computacional: FastAPI procesa el batch en una única transacción, Supabase ejecuta un bulk UPDATE con todas las clasificaciones en una sola query, y el rate limiting se ajusta a 10 req/min (vs 30 individual) para balancear recursos del servidor. Esto permite a empresas clasificar miles de tickets históricos en minutos durante migraciones, reprocesar tickets cuando se deploya un modelo mejorado, o integrar con pipelines de ETL que extraen tickets desde múltiples fuentes y los envían agrupados.
        </p>
        
        <h3 style='color: #2563eb; font-size: 1rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem;'>Caso de Uso Real</h3>
        <p style='color: #1e293b; line-height: 1.7; margin-bottom: 1.5rem;'>
        Una empresa migra 5,000 tickets históricos de un sistema legacy: en lugar de 5,000 requests individuales que tomarían ~3 horas (con rate limit de 30/min), hace 50 requests batch de 100 tickets cada uno (permitidos a 10/min), completando la clasificación completa en 5 minutos — reducción de tiempo del 97% mientras mantiene la misma precisión F1=0.9835 y actualiza automáticamente la base de datos Supabase con todas las clasificaciones.
        </p>
    """, unsafe_allow_html=True)
    st.markdown("<h2 style='color: black;'>🔄 Flujo de Clasificación Completo</h2>", unsafe_allow_html=True)
    
    st.markdown("""<div class="road-pipeline">
<div class="road-step step-left">
<div class="road-step-number">01</div>
<div class="road-step-box">
<div class="road-step-header">📝 Cliente envía ticket</div>
<div class="road-step-content">
<p><strong>POST</strong> <code>https://api.com/predict/ticket</code></p>
<p><strong>Body:</strong> <code>{"ticket_id": "INC001", "texto": "Mi computadora no funciona correctamente"}</code></p>
<p><strong>Headers:</strong> <code>{"X-API-Key": "abc123..."}</code></p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">02</div>
<div class="road-step-box">
<div class="road-step-header">🔐 FastAPI - Autenticación y Rate Limiting</div>
<div class="road-step-content">
<p><strong>Rol:</strong> Gateway de seguridad</p>
<p><strong>Acción:</strong> Valida API Key en header → Verifica rate limit (30 req/min) → Si pasa, continúa</p>
</div>
</div>
</div>
<div class="road-step step-left">
<div class="road-step-number">03</div>
<div class="road-step-box">
<div class="road-step-header">🧹 NLTK - Preprocessing NLP</div>
<div class="road-step-content">
<p><strong>Rol:</strong> Limpieza y normalización de texto</p>
<p><strong>Acción:</strong></p>
<ul>
<li>Tokenización: "Mi computadora no funciona" → ['Mi', 'computadora', 'no', 'funciona']</li>
<li>Lowercase: ['mi', 'computadora', 'no', 'funciona']</li>
<li>Stopwords removal (español): ['computadora', 'funciona']</li>
<li>Stemming Snowball: ['comput', 'funcion']</li>
</ul>
<p><strong>Output:</strong> "comput funcion"</p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">04</div>
<div class="road-step-box">
<div class="road-step-header">🔢 scikit-learn TfidfVectorizer - Feature Extraction</div>
<div class="road-step-content">
<p><strong>Rol:</strong> Convierte texto en números</p>
<p><strong>Acción:</strong> Transforma "comput funcion" → vector [0.0, 0.0, 0.87, 0.0, 0.45, ...] (5000 dimensiones)</p>
<p><strong>Cómo:</strong> Usa vocabulario aprendido en entrenamiento, calcula TF-IDF scores</p>
</div>
</div>
</div>
<div class="road-step step-left">
<div class="road-step-number">05</div>
<div class="road-step-box">
<div class="road-step-header">🤖 Gradient Boosting Classifier - Predicción</div>
<div class="road-step-content">
<p><strong>Rol:</strong> Modelo ML que clasifica</p>
<p><strong>Acción:</strong> Recibe vector [5000 dims] → Pasa por 400 árboles de decisión → Calcula probabilidades para cada clase</p>
<p><strong>Output:</strong> <code>{"TI": 0.95, "RRHH": 0.02, "Finanzas": 0.01, "Operaciones": 0.02}</code></p>
<p><strong>Decisión:</strong> Clase con mayor probabilidad = TI (95%)</p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">06</div>
<div class="road-step-box">
<div class="road-step-header">📝 Python - Logging de Predicción</div>
<div class="road-step-content">
<p><strong>Rol:</strong> Registro para auditoría y monitoreo</p>
<p><strong>Acción:</strong> Guarda en <code>monitoring/logs/predictions.jsonl</code>:</p>
<pre><code>{"ticket_id": "INC001", "prediction": "TI", "probability": 0.95,
 "timestamp": "2025-12-14T10:30:00Z", "prediction_id": "uuid-123"}</code></pre>
</div>
</div>
</div>
<div class="road-step step-left">
<div class="road-step-number">07</div>
<div class="road-step-box">
<div class="road-step-header">💾 Supabase (PostgreSQL) - Actualización Base de Datos</div>
<div class="road-step-content">
<p><strong>Rol:</strong> Persistencia de datos</p>
<p><strong>Acción:</strong></p>
<pre><code>UPDATE tickets_fiducia
SET prediction = 'TI',
    probability = 0.95,
    classified_at = NOW()
WHERE ticket_id = 'INC001'</code></pre>
<p><strong>Por qué:</strong> Enruta ticket automáticamente al departamento correcto</p>
</div>
</div>
</div>
<div class="road-step step-right">
<div class="road-step-number">08</div>
<div class="road-step-box">
<div class="road-step-header">📤 FastAPI - Response al Cliente</div>
<div class="road-step-content">
<p><strong>Rol:</strong> Comunicación de resultado</p>
<p><strong>Acción:</strong> Retorna JSON:</p>
<pre><code>{
  "ticket_id": "INC001",
  "prediction": "TI",
  "probability": 0.95,
  "database_update": {"success": true},
  "timestamp": "2025-12-14T10:30:00Z"
}</code></pre>
</div>
</div>
</div>
<div class="road-step step-left">
<div class="road-step-number">09</div>
<div class="road-step-box">
<div class="road-step-header">🔄 Background: Drift Detection (cada 6h)</div>
<div class="road-step-content">
<p><strong>Rol:</strong> Monitoreo continuo de calidad</p>
<ul>
<li><strong>GitHub Actions:</strong> Activa CRON cada 6 horas</li>
<li><strong>SciPy:</strong> Analiza logs acumulados → detecta drift estadístico</li>
<li><strong>scikit-learn:</strong> Evalúa F1-score en predicciones con labels reales</li>
<li><strong>Si problema:</strong> Activa auto-reentrenamiento (flujo anterior)</li>
</ul>
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("<h2 style='color: black;'>📊 Stack Tecnológico - Resumen Completo</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: black; margin-top: 1rem; margin-bottom: 1rem;'>Pipeline de Clasificación (Inferencia)</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .classification-table {
        width: 100%;
        border-collapse: collapse;
        margin: 2rem 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .classification-table thead {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
    }
    
    .classification-table th {
        padding: 1rem 1.25rem;
        text-align: left;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.5px;
        border-bottom: 3px solid #1e3a8a;
    }
    
    .classification-table tbody tr {
        background: #ffffff;
        transition: all 0.2s ease;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .classification-table tbody tr:nth-child(even) {
        background: #f8fafc;
    }
    
    .classification-table tbody tr:hover {
        background: #eff6ff;
        transform: translateX(4px);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
    }
    
    .classification-table td {
        padding: 1rem 1.25rem;
        color: #1e293b;
        font-size: 0.95rem;
        line-height: 1.6;
        vertical-align: top;
    }
    
    .classification-table td:first-child {
        font-weight: 600;
        color: #1e40af;
        width: 22%;
    }
    
    .classification-table td:nth-child(2) {
        width: 20%;
        color: #475569;
    }
    
    .classification-table td:nth-child(3) {
        width: 58%;
        color: #64748b;
    }
    
    .classification-table tbody tr:last-child {
        border-bottom: none;
    }
    </style>
    
    <table class="classification-table">
        <thead>
            <tr>
                <th>Stack Tecnológico</th>
                <th>Rol en el Flujo</th>
                <th>Acción Específica</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>FastAPI</td>
                <td>Gateway API & Seguridad</td>
                <td>Recibe request → Valida API Key → Rate limiting (30 req/min) → Retorna response JSON</td>
            </tr>
            <tr>
                <td>NLTK</td>
                <td>Preprocessing NLP</td>
                <td>Tokenización → Lowercase → Stopwords removal (español) → Stemming Snowball ('computadora'→'comput')</td>
            </tr>
            <tr>
                <td>scikit-learn TfidfVectorizer</td>
                <td>Feature Extraction</td>
                <td>Transforma texto limpio → vector numérico sparse [5000 dimensiones] con TF-IDF scores</td>
            </tr>
            <tr>
                <td>Gradient Boosting (scikit-learn)</td>
                <td>Modelo de Clasificación</td>
                <td>Recibe vector → Pasa por 400 árboles → Calcula probabilidades → Retorna clase (TI/RRHH/Finanzas/Ops)</td>
            </tr>
            <tr>
                <td>Python (joblib)</td>
                <td>Serialización de Modelos</td>
                <td>Carga modelo desde best_model.pkl al iniciar API → Mantiene en memoria para inferencia rápida</td>
            </tr>
            <tr>
                <td>Python (logging)</td>
                <td>Auditoría</td>
                <td>Guarda predicción en predictions.jsonl (ticket_id, predicción, probabilidad, timestamp)</td>
            </tr>
            <tr>
                <td>Supabase (PostgreSQL)</td>
                <td>Persistencia de Datos</td>
                <td>UPDATE ticket con predicción + probabilidad → Enruta a departamento correcto automáticamente</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
# ============================================================================
# TAB 5: ORQUESTACION CON AIRFLOW
# ============================================================================
with tab4:
    st.markdown("<h2 style='color: black;'>🔄 Monitoreo con Apache Airflow</h2>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style='color: #475569; font-size: 1.2rem; font-weight: 700; margin-top: 1.5rem; margin-bottom: 1rem;'>¿Qué es Apache Airflow y por qué está en el proyecto?</h3>
        <p style='color: #1e293b; line-height: 1.7; margin-bottom: 1.5rem;'>
        Apache Airflow es una plataforma de orquestación de workflows que permite programar, ejecutar y monitorear pipelines de datos complejos mediante DAGs (Directed Acyclic Graphs - Grafos Acíclicos Dirigidos). En este proyecto, Airflow actúa como una alternativa local y on-premise a GitHub Actions, permitiendo a empresas que no pueden usar servicios cloud públicos ejecutar el mismo sistema de monitoreo y reentrenamiento automático en su propia infraestructura, con la ventaja adicional de tener una interfaz web visual para monitorear el estado de cada tarea en tiempo real.
        </p>
        
        <hr style='border: none; border-top: 2px solid #e2e8f0; margin: 2rem 0;' />
        
        <h3 style='color: #475569; font-size: 1.2rem; font-weight: 700; margin-top: 1.5rem; margin-bottom: 1rem;'>Arquitectura de Airflow en el Proyecto</h3>
        <h4 style='color: #475569; font-size: 1rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.75rem;'>El sistema incluye un Docker Compose stack completo que levanta cuatro componentes:</h4>
        <ol style='color: #1e293b; line-height: 1.8; margin-bottom: 1.5rem; padding-left: 1.5rem;'>
        <li style='margin-bottom: 0.75rem;'><strong>PostgreSQL:</strong> Base de datos que almacena metadata de Airflow (estado de DAGs, ejecuciones históricas, logs de tareas)</li>
        <li style='margin-bottom: 0.75rem;'><strong>Airflow Webserver:</strong> Interfaz web en puerto 8080 donde se visualizan DAGs, se monitorean ejecuciones, se ven logs en tiempo real</li>
        <li style='margin-bottom: 0.75rem;'><strong>Airflow Scheduler:</strong> Motor que ejecuta DAGs según su schedule, maneja dependencias entre tareas, retry logic</li>
        <li style='margin-bottom: 0.75rem;'><strong>Volúmenes compartidos:</strong> Montan airflow/dags/ (código de DAGs), models/ (modelos versionados), data-tickets-train/ (datasets)</li>
        </ol>
        
        <hr style='border: none; border-top: 2px solid #e2e8f0; margin: 2rem 0;' />
        
        <h3 style='color: #475569; font-size: 1.2rem; font-weight: 700; margin-top: 1.5rem; margin-bottom: 1rem;'>Los 3 DAGs Implementados</h3>
        <h4 style='color: #475569; font-size: 1.1rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 1rem;'>1. DAG Principal: mlops_ticket_classifier_pipeline</h4>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin: 1rem 0; text-align: center;">
    <strong style="color: #475569;">⏰ Schedule: Cada 6 horas</strong> <span style="color: #64748b;">(equivalente al CRON de GitHub Actions)</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="flow-container">
    <div class="flow-pipeline">
    <div class="flow-step">🔍 check_api_health<br/><small>BashOperator</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step">📊 check_drift<br/><small>PythonOperator<br/>utils/monitoring.py</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step">📉 evaluate_performance<br/><small>PythonOperator<br/>Calcula F1 en producción</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step" style="border-color: #f59e0b; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);">⚖️ decide_retraining<br/><small>ShortCircuitOperator<br/>DECISIÓN INTELIGENTE<br/>drift > 0.5 OR f1_drop > 5%</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step" style="border-color: #10b981; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);">🤖 train_model<br/><small>BashOperator<br/>scripts/train_model.py</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step" style="border-color: #10b981; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);">🆚 compare_models<br/><small>PythonOperator<br/>f1_nuevo vs f1_actual</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step" style="border-color: #f59e0b; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);">✅ decide_deploy<br/><small>ShortCircuitOperator<br/>VALIDACIÓN<br/>mejora >= 1%</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step" style="border-color: #8b5cf6; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);">🚀 deploy_model<br/><small>PythonOperator<br/>hot reload API</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step" style="border-color: #8b5cf6; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);">📦 push_to_s3<br/><small>BashOperator<br/>dvc push</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step" style="border-color: #8b5cf6; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);">🔔 notify_completion<br/><small>PythonOperator<br/>Slack/Discord/Telegram</small></div>
    </div>
    <div style="text-align: center; margin-top: 1.5rem;">
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 2px solid #f59e0b; border-radius: 8px; padding: 0.75rem 1.5rem; display: inline-block; margin: 0.5rem;">
    <span style="color: #92400e; font-weight: 600; font-size: 0.9rem;">⚠️ Puntos de Decisión: Si NO cumple condición → FIN (skip tareas siguientes)</span>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <hr style='border: none; border-top: 2px solid #e2e8f0; margin: 2rem 0;' />
    <h4 style='color: #475569; font-size: 1.1rem; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem;'>2. DAG Manual: train_model_manual</h4>
    <p style='color: #1e293b; line-height: 1.7; margin-bottom: 1.5rem;'><strong>Schedule: None (solo manual)</strong></p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="flow-container">
    <div class="flow-pipeline">
    <div class="flow-step">👤 Data Scientist<br/><small>Entra a Airflow UI<br/>localhost:8080</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step">📋 Selecciona<br/><small>train_model_manual</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step" style="border-color: #3b82f6; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);">🖱️ Click<br/><small>"Trigger DAG"</small></div>
    <span class="flow-arrow">→</span>
    <div class="flow-step" style="border-color: #10b981; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);">🚀 Ejecuta<br/><small>Entrenamiento completo<br/>inmediatamente sin esperar CRON</small></div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <hr style='border: none; border-top: 2px solid #e2e8f0; margin: 2rem 0;' />
    <h4 style='color: #475569; font-size: 1.1rem; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem;'>3. DAG de Monitoreo Ligero: monitor_only</h4>
    <p style='color: #1e293b; line-height: 1.7; margin-bottom: 1.5rem;'><strong>Schedule: Cada hora</strong></p>
    <p style='color: #1e293b; line-height: 1.7; margin-bottom: 1.5rem;'>Uso: Monitoreo frecuente sin reentrenamiento (solo observación).</p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin: 1.5rem 0;">
    <strong style="color: #475569; font-size: 1rem;">Tareas:</strong>
    </div>
    <div class="flow-container">
    <div class="flow-pipeline">
    <div class="flow-step">🔍 check_api_health</div>
    <span class="flow-arrow">→</span>
    <div class="flow-step">📊 check_drift</div>
    <span class="flow-arrow">→</span>
    <div class="flow-step">📝 log_metrics</div>
    <span class="flow-arrow">→</span>
    <div class="flow-step" style="border-color: #ef4444; background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);">🚨 alert_if_threshold_exceeded</div>
    </div>
    </div>
    <p style='color: #1e293b; line-height: 1.7; margin-top: 1.5rem; margin-bottom: 1.5rem;'>Si detecta drift, envía alerta pero NO retrain — útil para tener visibilidad sin costo computacional de entrenar.</p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <h3 style='color: #475569; font-size: 1.3rem; font-weight: 700; margin-top: 2.5rem; margin-bottom: 1.5rem;'>Ejemplo de Ejecución en Airflow</h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border: 2px solid #3b82f6; border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0;">
    <div style="color: #1e40af; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">⏰ Día 1, 00:00: Scheduler activa mlops_ticket_classifier_pipeline</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin: 2rem 0;">
    <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #10b981; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem;">
    <div style="color: #065f46; font-weight: 700; margin-bottom: 0.75rem;">1. check_api_health (30 seg): <span style="color: #10b981;">✅ Verde → API respondiendo</span></div>
    </div>
    
    <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #10b981; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem;">
    <div style="color: #065f46; font-weight: 700; margin-bottom: 0.75rem;">2. check_drift (2 min):</div>
    <ul style="color: #047857; margin-left: 1.5rem; line-height: 1.8;">
    <li>KS-test p-value: 0.12 (>0.05) → No data drift</li>
    <li>Chi-square p-value: 0.03 (<0.05) → <strong>Concept drift detectado</strong></li>
    <li>Vocab growth: 8% (<10%) → No vocab drift</li>
    <li><strong>drift_score = 0.55 → Almacena en XCom</strong></li>
    </ul>
    </div>
    
    <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #10b981; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem;">
    <div style="color: #065f46; font-weight: 700; margin-bottom: 0.75rem;">3. evaluate_performance (1 min):</div>
    <ul style="color: #047857; margin-left: 1.5rem; line-height: 1.8;">
    <li>Query Supabase: 150 predicciones con labels</li>
    <li>F1 actual: 0.9300</li>
    <li>F1 baseline: 0.9835</li>
    <li><strong>Drop: 5.4% (>5% threshold) → Almacena en XCom</strong></li>
    </ul>
    </div>
    
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 2px solid #f59e0b; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem;">
    <div style="color: #92400e; font-weight: 700; margin-bottom: 0.75rem;">4. decide_retraining (5 seg):</div>
    <ul style="color: #78350f; margin-left: 1.5rem; line-height: 1.8;">
    <li>Lee XCom: drift_score=0.55, f1_drop=5.4%</li>
    <li>Condición: (0.55 > 0.5) OR (5.4% > 5%) = <strong>TRUE</strong></li>
    <li><strong>Resultado: CONTINUAR ✅</strong></li>
    </ul>
    </div>
    
    <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #10b981; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem;">
    <div style="color: #065f46; font-weight: 700; margin-bottom: 0.75rem;">5. train_model (60 min): Ejecuta entrenamiento completo → <span style="color: #10b981;">✅ Verde</span></div>
    </div>
    
    <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #10b981; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem;">
    <div style="color: #065f46; font-weight: 700; margin-bottom: 0.75rem;">6. compare_models (1 min):</div>
    <ul style="color: #047857; margin-left: 1.5rem; line-height: 1.8;">
    <li>F1 nuevo: 0.9880</li>
    <li>F1 actual: 0.9835</li>
    <li><strong>Mejora: +0.45% → Almacena en XCom</strong></li>
    </ul>
    </div>
    
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 2px solid #f59e0b; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem;">
    <div style="color: #92400e; font-weight: 700; margin-bottom: 0.75rem;">7. decide_deploy (5 seg):</div>
    <ul style="color: #78350f; margin-left: 1.5rem; line-height: 1.8;">
    <li>Lee XCom: mejora=0.45%</li>
    <li>Condición: 0.45% >= 1% = <strong>FALSE</strong></li>
    <li><strong>Resultado: SKIP ⚠️ (modelo no mejora suficiente)</strong></li>
    </ul>
    </div>
    
    <div style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border: 2px solid #f59e0b; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem;">
    <div style="color: #991b1b; font-weight: 700; margin-bottom: 0.75rem;">8. deploy_model, push_to_s3, notify_completion: <span style="color: #f59e0b;">⚠️ Marcadas como "skipped" (naranja en UI)</span></div>
    </div>
    
    <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border: 2px solid #3b82f6; border-radius: 12px; padding: 1.5rem; margin-top: 2rem;">
    <div style="color: #1e40af; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">📊 Resultado visible en Airflow UI</div>
    <div style="color: #1e293b; line-height: 1.7;">DAG completado en 63 minutos, 7 tareas exitosas <span style="color: #10b981; font-weight: 600;">(verde)</span>, 3 skipped <span style="color: #f59e0b; font-weight: 600;">(naranja)</span>. Usuario ve que se entrenó pero no deployó por mejora insuficiente.</div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
<div style="margin-top: 3rem;">
<h3 style='color: #475569; font-size: 1.2rem; font-weight: 700; margin-top: 2rem; margin-bottom: 1.5rem;'>Monitoreo en Tiempo Real desde la UI</h3>
<p style='color: #1e293b; line-height: 1.7; margin-bottom: 1rem;'>En <strong>http://localhost:8080</strong>:</p>
<ul style='color: #1e293b; line-height: 1.8; margin-left: 1.5rem; margin-bottom: 2rem;'>
<li><strong>Grid View:</strong> Calendario con estado de cada ejecución (verde=éxito, rojo=fallo, naranja=skipped)</li>
<li><strong>Graph View:</strong> DAG visual con colores por estado, click en tarea → ver logs en vivo</li>
<li><strong>Gantt Chart:</strong> Timeline de cuánto tardó cada tarea (útil para optimizar)</li>
<li><strong>Task Duration:</strong> Histograma de duración de tareas (detecta si train_model está tardando más con el tiempo)</li>
<li><strong>Task Logs:</strong> stdout/stderr en tiempo real (ve progreso de Optuna trial por trial)</li>
</ul>

<h3 style='color: #475569; font-size: 1.2rem; font-weight: 700; margin-top: 2rem; margin-bottom: 1.5rem;'>Alertas y Notificaciones</h3>
<p style='color: #1e293b; line-height: 1.7; margin-bottom: 1rem;'>En el código de cada DAG, se configuran callbacks:</p>
<div style="background: #1e293b; color: #e2e8f0; padding: 1.25rem; border-radius: 8px; margin: 1rem 0; font-family: 'Courier New', monospace; font-size: 0.9rem; overflow-x: auto;">
<pre style="margin: 0; white-space: pre-wrap;">default_args = {
    'on_failure_callback': slack_alert,  # Si falla, envía a Slack
    'on_retry_callback': log_retry,      # Log cada retry
    'retries': 3,                        # Intenta 3 veces antes de fallar
    'retry_delay': timedelta(minutes=5), # Espera 5 min entre retries
}</pre>
</div>
<p style='color: #1e293b; line-height: 1.7; margin-top: 1rem; margin-bottom: 1rem;'><strong>Ejemplo:</strong> Si train_model falla (ej: DVC no puede conectar a S3), Airflow:</p>
<ol style='color: #1e293b; line-height: 1.8; margin-left: 1.5rem; margin-bottom: 2rem;'>
<li>Espera 5 minutos</li>
<li>Reintenta (retry 1/3)</li>
<li>Si falla de nuevo → espera 5 min → retry 2/3</li>
<li>Si falla 3 veces → envía Slack alert: "⚠️ DAG mlops_pipeline FAILED en train_model"</li>
</ol>

<h3 style='color: #475569; font-size: 1.2rem; font-weight: 700; margin-top: 2rem; margin-bottom: 1.5rem;'>Dual Orchestration: GitHub Actions + Airflow</h3>
<p style='color: #1e293b; line-height: 1.7; margin-bottom: 1rem;'>El proyecto usa ambos en paralelo:</p>
<ul style='color: #1e293b; line-height: 1.8; margin-left: 1.5rem; margin-bottom: 1rem;'>
<li><strong>GitHub Actions (Cloud):</strong> Para equipos distribuidos, CI/CD automático en push, ideal para startups/cloud-first</li>
<li><strong>Airflow (On-Premise):</strong> Para empresas con compliance estricto, necesidad de infraestructura local, o equipos que prefieren UI visual</li>
</ul>
<p style='color: #1e293b; line-height: 1.7; margin-top: 1rem; margin-bottom: 1rem;'>Ambos ejecutan exactamente el mismo código (scripts/train_model.py, utils/monitoring.py), garantizando consistencia. Un Data Scientist puede:</p>
<ul style='color: #1e293b; line-height: 1.8; margin-left: 1.5rem; margin-bottom: 1rem;'>
<li>Ver ejecución en GitHub Actions summary (markdown estático)</li>
<li>O abrir Airflow UI (interfaz gráfica interactiva)</li>
</ul>
<div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border: 2px solid #3b82f6; border-radius: 12px; padding: 1.25rem; margin-top: 1.5rem;">
<p style='color: #1e40af; font-weight: 600; margin: 0;'>Resultado: Flexibilidad máxima para diferentes contextos empresariales sin duplicar lógica de negocio.</p>
</div>
</div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 5: ENDPOINTS
# ============================================================================
with tab5:
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

# ============================================================================
# TAB 6: DISTRIBUCIÓN DE ARCHIVOS DEL PROYECTO
# ============================================================================
with tab6:
    st.markdown("<h2 style='color: black;'>💻 Ver software</h2>", unsafe_allow_html=True)
    
    # Botón para ver repositorio en GitHub
    st.markdown("""
    <div style="margin: 1.5rem 0; text-align: center;">
    <a href="https://github.com/giovany-desing/Proyecto_tickets_fiduciaria" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #24292e 0%, #1a1e22 100%); color: white; padding: 0.75rem 2rem; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 1.05rem; box-shadow: 0 4px 15px rgba(36, 41, 46, 0.3); transition: transform 0.2s, box-shadow 0.2s;">
    🔗 Ver repositorio en Github
    </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.code("""
 Proyecto_tickets_fiduciaria/
  │
  ├── 📁 api/
  │   ├── __init__.py                            # Inicialización módulo API
  │   └── inference.py                           # API REST con endpoints de predicción y autenticación
  │
  ├── 📁 scripts/
  │   ├── train_model.py                         # Entrena 7 modelos ML + Optuna + DVC versionamiento
  │   ├── monitor_and_retrain.py                 # Drift detection + auto-retrain + hot reload API
  │   ├── download_model.py                      # Descarga modelos desde S3 via DVC
  │   └── deploy_model.py                        # Deploy modelo a producción + trigger reload
  │
  ├── 📁 utils/
  │   ├── __init__.py                            # Inicialización módulo utils
  │   ├── preprocessing_data.py                  # Pipeline NLP: tokenización, stemming, stopwords
  │   ├── monitoring.py                          # Drift detection (KS-test, Chi², vocab)
  │   ├── database.py                            # Cliente Supabase: queries, updates, retry logic
  │   ├── notifications.py                       # Webhooks: Slack, Discord, Telegram
  │   └── config_schema.py                       # Validación de config.yaml con Pydantic
  │
  ├── 📁 airflow/
  │   ├── 📁 dags/
  │   │   ├── mlops_pipeline.py                  # DAG principal: monitoring + retrain cada 6h
  │   │   ├── train_model_dag.py                 # DAG manual: entrenamiento on-demand
  │   │   └── monitor_only_dag.py                # DAG ligero: solo monitoreo cada 1h
  │   ├── docker-compose.yml                     # Stack Airflow: webserver, scheduler, postgres
  │   ├── Dockerfile                             # Imagen custom Airflow + deps proyecto
  │   ├── requirements.txt                       # Dependencias Airflow + ML stack
  │   └── README.md                              # Guía setup Airflow local
  │
  ├── 📁 models/
  │   ├── best_model.pkl                         # Modelo en producción (Gradient Boosting)
  │   ├── best_model.pkl.dvc                     # DVC pointer (hash MD5 + path S3)
  │   ├── best_model_metadata.json               # Metadata: F1, hiperparámetros, timestamp
  │   └── 📁 backups/                            # Backups automáticos con timestamp
  │
  ├── 📁 data-tickets-train/
  │   ├── dataset_tickets.csv                    # Dataset entrenamiento: 1,213 tickets
  │   └── dataset_tickets.csv.dvc                # DVC pointer dataset versionado en S3
  │
  ├── 📁 tests/
  │   ├── conftest.py                            # Fixtures pytest: sample data, mocks
  │   ├── test_api.py                            # Tests endpoints API + auth + rate limit
  │   ├── test_preprocessing.py                  # Tests pipeline NLP + edge cases
  │   ├── test_monitoring.py                     # Tests drift detection + performance eval
  │   ├── test_database.py                       # Tests Supabase client + retry logic
  │   └── README.md                              # Guía ejecución tests + coverage
  │
  ├── 📁 .github/workflows/
  │   ├── ci_cd_pipeline.yml                     # Validación + deploy Render + notificaciones
  │   ├── train_model.yml                        # Entrenamiento automático en push
  │   ├── monitor_and_retrain.yml                # CRON 6h: drift + auto-retrain
  │   ├── validate.yml                           # Pre-commit validations + linting
  │   └── deploy_render.yml                      # Deploy manual directo a Render
  │
  ├── 📁 .dvc/
  │   ├── config                                 # Configuración remote S3
  │   └── .gitignore                             # Ignora cache DVC local
  │
  ├── 📁 monitoring/
  │   └── 📁 logs/
  │       └── predictions.jsonl                  # Log predicciones: drift + performance eval
  │
  ├── 📄 config.yaml                             # Configuración centralizada: thresholds, paths
  ├── 📄 render.yaml                             # Config deployment Render.com
  ├── 📄 requirements.txt                        # Dependencias flexibles (189 paquetes)
  ├── 📄 requirements-lock.txt                   # Dependencias pinneadas (reproducibilidad)
  ├── 📄 runtime.txt                             # Versión Python: 3.9.18
  ├── 📄 pytest.ini                              # Configuración pytest: markers, coverage
  ├── 📄 setup_supabase_columns.sql              # DDL tabla tickets_fiducia
  ├── 📄 README.md                               # Documentación principal del proyecto
  ├── 📄 SETUP.md                                # Guía setup: env vars, AWS, Supabase
  ├── 📄 .gitignore                              # Archivos ignorados por Git
  ├── 📄 .dvcignore                              # Archivos ignorados por DVC
  └── 📄 .python-version                         # Versión Python local (pyenv)
""", language=None)