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