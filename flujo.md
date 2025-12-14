 🔄 Flujo Completo Paso a Paso

  FASE 1: Preparación del Entorno ⚙️

  1. GitHub Actions Trigger
     ├─ Detecta: git push a main
     ├─ Verifica: cambios en data-tickets-train/** o scripts/**
     └─ Inicia: Runner Ubuntu-latest

  2. Setup Inicial
     ├─ Checkout código (actions/checkout@v3)
     ├─ Setup Python 3.9 (actions/setup-python@v4)
     ├─ Cache pip dependencies
     └─ Install requirements.txt (189 paquetes)

  3. NLTK Resources Download
     ├─ punkt (tokenizador)
     ├─ stopwords (español)
     ├─ wordnet (lematización)
     └─ omw-1.4 (Open Multilingual Wordnet)

  4. DVC Configuration
     ├─ Configure AWS credentials:
     │  ├─ AWS_ACCESS_KEY_ID (secrets)
     │  ├─ AWS_SECRET_ACCESS_KEY (secrets)
     │  └─ AWS_DEFAULT_REGION
     ├─ DVC remote: s3://tu-bucket/path
     └─ DVC pull dataset_tickets.csv desde S3

  ---
  FASE 2: Carga y Preprocesamiento de Datos 📊

  5. Load Dataset
     ├─ Lectura: data-tickets-train/dataset_tickets.csv
     ├─ Validación: columnas requeridas ['texto', 'etiqueta']
     ├─ Shape: ~1,213 tickets × 2 columnas
     └─ Distribución de clases:
        ├─ TI: ~300 tickets
        ├─ RRHH: ~300 tickets
        ├─ Finanzas: ~300 tickets
        └─ Operaciones: ~313 tickets

  6. NLP Preprocessing Pipeline (utils/preprocessing_data.py)

     Para CADA ticket:

     a) Tokenización
        └─ NLTK word_tokenize() → lista de tokens

     b) Lowercase
        └─ "Mi Computadora NO Funciona" → "mi computadora no funciona"

     c) Stopwords Removal
        ├─ NLTK stopwords español base (183 palabras)
        ├─ Custom stopwords adicionales del config.yaml:
        │  ["favor", "cordial", "saludo", "gracias", "atentamente", ...]
        └─ Filtrado: [t for t in tokens if t not in stopwords]

     d) Cleaning
        ├─ Eliminar puntuación: string.punctuation
        ├─ Eliminar números standalone
        ├─ Eliminar tokens < 2 caracteres
        └─ Strip whitespaces

     e) Stemming Snowball (español)
        ├─ SnowballStemmer('spanish')
        ├─ "computadora" → "comput"
        ├─ "problemas" → "problem"
        └─ Reduce dimensionalidad manteniendo semántica

     Ejemplo completo:
     Input:  "Por favor, mi computadora no funciona correctamente. Gracias"
     Output: "comput funcion correct"

  7. Feature Extraction: TF-IDF Vectorization

     ├─ TfidfVectorizer(
     │     max_features=5000,        # Top 5000 términos más importantes
     │     ngram_range=(1, 2),       # Unigrams + Bigrams
     │     min_df=2,                 # Mínimo 2 documentos
     │     max_df=0.8,               # Máximo 80% de documentos
     │     sublinear_tf=True         # Escala logarítmica de TF
     │  )
     │
     ├─ Fit en datos de entrenamiento
     ├─ Transform: texto → vector [5000 dimensiones]
     │
     └─ Resultado: Matriz sparse (1213, 5000)
        • Cada fila = 1 ticket
        • Cada columna = 1 término
        • Valores = TF-IDF score [0, 1]

  ---
  FASE 3: Train/Test Split 🔀

  8. Stratified Split

     ├─ train_test_split(
     │     X=tfidf_matrix,
     │     y=labels,
     │     test_size=0.2,           # 20% test
     │     stratify=y,              # Mantiene proporción de clases
     │     random_state=42          # Reproducibilidad
     │  )
     │
     ├─ X_train: 970 samples × 5000 features
     ├─ X_test:  243 samples × 5000 features
     ├─ y_train: 970 labels
     └─ y_test:  243 labels

  9. Reproducibilidad Seeds
     
     ├─ Python: random.seed(42)
     ├─ NumPy: np.random.seed(42)
     ├─ Env: PYTHONHASHSEED=42
     └─ Sklearn: random_state=42 en todos los modelos

  ---
  FASE 4: Entrenamiento de 7 Modelos 🤖

  10. Training Loop con Optuna Optimization

  Para CADA uno de los 7 modelos:

  ┌─────────────────────────────────────────────────────┐
  │ MODELO 1: Logistic Regression                       │
  ├─────────────────────────────────────────────────────┤
  │ Optuna Hyperparameter Search:                       │
  │   • Trials: 10 (en CI/CD) o 20 (local)             │
  │   • Sampler: TPE (Tree-structured Parzen Estimator) │
  │   • Objective: Maximizar F1-score (macro avg)       │
  │                                                      │
  │ Hyperparameters a optimizar:                        │
  │   • C: [0.01, 100] (log scale)                     │
  │   • penalty: ['l1', 'l2']                           │
  │   • solver: ['liblinear', 'saga']                   │
  │   • max_iter: [100, 500]                            │
  │                                                      │
  │ Cross Validation:                                    │
  │   • StratifiedKFold (2 folds en CI, 3 en local)    │
  │   • Métrica: f1_score(average='macro')              │
  │                                                      │
  │ Mejor configuración encontrada:                     │
  │   • C: 10.5                                         │
  │   • penalty: 'l2'                                   │
  │   • solver: 'liblinear'                             │
  │                                                      │
  │ Training final con mejores hiperparámetros          │
  │   • Fit en X_train completo                         │
  │   • Predict en X_test                               │
  │                                                      │
  │ Evaluación:                                         │
  │   • F1-score: 0.9712                                │
  │   • Accuracy: 0.9720                                │
  │   • Precision: 0.9715                               │
  │   • Recall: 0.9711                                  │
  │                                                      │
  │ MLflow Logging:                                      │
  │   ├─ log_params(C, penalty, solver)                │
  │   ├─ log_metrics(f1, accuracy, precision, recall)  │
  │   └─ log_model(sklearn_model)                      │
  └─────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────┐
  │ MODELO 2: Random Forest                             │
  ├─────────────────────────────────────────────────────┤
  │ Hyperparameters:                                     │
  │   • n_estimators: [100, 500]                        │
  │   • max_depth: [10, 50, None]                       │
  │   • min_samples_split: [2, 10]                      │
  │   • min_samples_leaf: [1, 4]                        │
  │   • max_features: ['sqrt', 'log2']                  │
  │                                                      │
  │ Mejor config:                                        │
  │   • n_estimators: 300                               │
  │   • max_depth: None                                 │
  │   • min_samples_split: 2                            │
  │                                                      │
  │ Evaluación:                                         │
  │   • F1-score: 0.9132                                │
  └─────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────┐
  │ MODELO 3: XGBoost                                   │
  ├─────────────────────────────────────────────────────┤
  │ Hyperparameters:                                     │
  │   • n_estimators: [100, 500]                        │
  │   • max_depth: [3, 10]                              │
  │   • learning_rate: [0.01, 0.3]                      │
  │   • subsample: [0.6, 1.0]                           │
  │   • colsample_bytree: [0.6, 1.0]                    │
  │   • gamma: [0, 5]                                   │
  │                                                      │
  │ Evaluación:                                         │
  │   • F1-score: 0.9627                                │
  └─────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────┐
  │ MODELO 4: SVM (Support Vector Machine)             │
  ├─────────────────────────────────────────────────────┤
  │ Hyperparameters:                                     │
  │   • C: [0.1, 100] (log scale)                       │
  │   • kernel: ['linear', 'rbf']                       │
  │   • gamma: ['scale', 'auto']                        │
  │                                                      │
  │ Evaluación:                                         │
  │   • F1-score: 0.9177                                │
  └─────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────┐
  │ MODELO 5: LightGBM                                  │
  ├─────────────────────────────────────────────────────┤
  │ Hyperparameters:                                     │
  │   • n_estimators: [100, 500]                        │
  │   • max_depth: [3, 10]                              │
  │   • learning_rate: [0.01, 0.3]                      │
  │   • num_leaves: [20, 100]                           │
  │   • min_child_samples: [10, 50]                     │
  │                                                      │
  │ Evaluación:                                         │
  │   • F1-score: 0.9670                                │
  └─────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────┐
  │ MODELO 6: Gradient Boosting ⭐ WINNER               │
  ├─────────────────────────────────────────────────────┤
  │ Hyperparameters:                                     │
  │   • n_estimators: [100, 500]                        │
  │   • max_depth: [3, 10]                              │
  │   • learning_rate: [0.01, 0.3]                      │
  │   • subsample: [0.6, 1.0]                           │
  │   • min_samples_split: [2, 10]                      │
  │                                                      │
  │ Mejor config encontrada:                            │
  │   • n_estimators: 400                               │
  │   • max_depth: 7                                    │
  │   • learning_rate: 0.1                              │
  │   • subsample: 0.9                                  │
  │                                                      │
  │ Evaluación: 🏆                                      │
  │   • F1-score: 0.9835 ← MEJOR                        │
  │   • Accuracy: 0.9835                                │
  │   • Precision: 0.9838                               │
  │   • Recall: 0.9833                                  │
  └─────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────┐
  │ MODELO 7: Extra Trees                              │
  ├─────────────────────────────────────────────────────┤
  │ Hyperparameters:                                     │
  │   • n_estimators: [100, 500]                        │
  │   • max_depth: [10, 50, None]                       │
  │   • min_samples_split: [2, 10]                      │
  │                                                      │
  │ Evaluación:                                         │
  │   • F1-score: 0.9134                                │
  └─────────────────────────────────────────────────────┘

  11. Comparación y Selección del Mejor Modelo

     Resultados Finales:
     ┌─────────────────────┬──────────┬──────────┐
     │ Modelo              │ F1-Score │ Accuracy │
     ├─────────────────────┼──────────┼──────────┤
     │ Gradient Boosting   │ 0.9835   │ 0.9835   │ ⭐ SELECCIONADO
     │ Logistic Regression │ 0.9712   │ 0.9720   │
     │ LightGBM           │ 0.9670   │ 0.9670   │
     │ XGBoost            │ 0.9627   │ 0.9630   │
     │ SVM                │ 0.9177   │ 0.9180   │
     │ Extra Trees        │ 0.9134   │ 0.9140   │
     │ Random Forest      │ 0.9132   │ 0.9135   │
     └─────────────────────┴──────────┴──────────┘

     Criterio de selección:
     ├─ Maximizar F1-score (macro average)
     ├─ En caso de empate: preferir menor complejidad
     └─ Winner: Gradient Boosting (F1: 0.9835)

  ---
  FASE 5: Guardado y Versionamiento 💾

  12. Serialización del Mejor Modelo

     ├─ Crear objeto de pipeline completo:
     │  {
     │    'vectorizer': TfidfVectorizer (fitted),
     │    'model': GradientBoostingClassifier (trained),
     │    'label_encoder': LabelEncoder (fitted),
     │    'preprocessing_config': {...}
     │  }
     │
     ├─ Guardar con pickle:
     │  └─ models/best_model.pkl (tamaño: ~50 MB)
     │
     └─ Crear backup con timestamp:
        └─ models/backups/best_model_20251213_154530.pkl

  13. Guardar Metadata JSON

     models/best_model_metadata.json:
     {
       "model_name": "Gradient_Boosting",
       "f1_score": 0.9835,
       "accuracy": 0.9835,
       "precision": 0.9838,
       "recall": 0.9833,
       "timestamp": "2025-12-13T15:45:30",
       "environment": "CI/CD",
       "training_samples": 970,
       "test_samples": 243,
       "features_count": 5000,
       "hyperparameters": {
         "n_estimators": 400,
         "max_depth": 7,
         "learning_rate": 0.1,
         "subsample": 0.9
       },
       "training_config": {
         "random_seed": 42,
         "cv_folds": 2,
         "optuna_trials": 10,
         "max_features": 5000
       },
       "all_results": {
         "Logistic_Regression": {"f1": 0.9712, ...},
         "Random_Forest": {"f1": 0.9132, ...},
         "XGBoost": {"f1": 0.9627, ...},
         "SVM": {"f1": 0.9177, ...},
         "LightGBM": {"f1": 0.9670, ...},
         "Gradient_Boosting": {"f1": 0.9835, ...},
         "Extra_Trees": {"f1": 0.9134, ...}
       },
       "confusion_matrix": [[...], [...], [...], [...]],
       "classification_report": {...}
     }

  14. DVC Versionamiento

     ├─ dvc add models/best_model.pkl
     │  ├─ Genera: models/best_model.pkl.dvc (puntero)
     │  ├─ Calcula: MD5 hash del modelo
     │  └─ Mueve archivo a: .dvc/cache/
     │
     ├─ dvc push
     │  ├─ Sube modelo a S3
     │  ├─ Path: s3://bucket/models/md5hash
     │  └─ Actualiza remote
     │
     └─ git add models/best_model.pkl.dvc
        └─ Commitea solo el puntero (lightweight)

  15. MLflow Registry

     ├─ mlflow.sklearn.log_model(
     │     sk_model=best_model,
     │     artifact_path="gradient_boosting_model",
     │     registered_model_name="TicketClassifier"
     │  )
     │
     ├─ Guarda en: mlruns/
     │  ├─ Experiment ID
     │  ├─ Run ID
     │  ├─ Artifacts/
     │  ├─ Metrics/
     │  └─ Params/
     │
     └─ Versionado automático: v1, v2, v3...

  ---
  FASE 6: Artifacts Upload (GitHub Actions) 📤

  16. Upload Artifacts to GitHub

     ├─ actions/upload-artifact@v3
     │
     ├─ Artifact 1: trained-model
     │  ├─ models/best_model.pkl
     │  └─ models/best_model_metadata.json
     │
     ├─ Artifact 2: mlflow-runs
     │  └─ mlruns/ (completo)
     │
     └─ Retención: 90 días

  ---
  FASE 7: Hot Reload de API 🔄

  17. Reload Model en API (sin downtime)

     ├─ Endpoint: POST /admin/reload-model
     │  └─ Headers: X-API-Key: $ADMIN_API_KEY
     │
     ├─ API descarga nuevo modelo:
     │  ├─ dvc pull models/best_model.pkl
     │  └─ Load desde S3
     │
     ├─ Recarga en memoria:
     │  ├─ global model_pipeline
     │  ├─ model_pipeline = pickle.load(...)
     │  └─ Log: "Model reloaded successfully"
     │
     └─ Zero downtime:
        • No reinicia uvicorn
        • Requests en proceso continúan con modelo anterior
        • Nuevos requests usan modelo nuevo

  ---
  FASE 8: Summary Report 📊

  18. GitHub Actions Summary

     Genera reporte markdown automático:

     ## 🏋️ Training Pipeline - Completed Successfully

     ### Best Model Selected
     - **Algorithm**: Gradient Boosting
     - **F1-Score**: 0.9835
     - **Accuracy**: 0.9835
     - **Training Time**: 58.3 minutes

     ### All Models Performance
     | Model | F1-Score | Accuracy | Training Time |
     |-------|----------|----------|---------------|
     | Gradient Boosting | 0.9835 | 0.9835 | 12.5 min |
     | Logistic Regression | 0.9712 | 0.9720 | 3.2 min |
     | LightGBM | 0.9670 | 0.9670 | 8.7 min |
     | XGBoost | 0.9627 | 0.9630 | 10.1 min |
     | SVM | 0.9177 | 0.9180 | 15.6 min |
     | Extra Trees | 0.9134 | 0.9140 | 6.8 min |
     | Random Forest | 0.9132 | 0.9135 | 7.4 min |

     ### Hyperparameters
     ```json
     {
       "n_estimators": 400,
       "max_depth": 7,
       "learning_rate": 0.1,
       "subsample": 0.9
     }

  Confusion Matrix

             TI  RRHH  Finanzas  Ops
  TI        59    0       1       0
  RRHH       0   60       0       1
  Finanzas   1    0      59       0
  Ops        0    1       0      61

  Next Steps

     ✅ Model pushed to S3
     ✅ API reloaded
     ✅ Ready for production
