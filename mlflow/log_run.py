# mlflow/log_run.py

import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("FraudDetection-Demo")

with mlflow.start_run():
    mlflow.log_param("model", "KNN")
    mlflow.log_param("threshold", 0.99)
    mlflow.log_metric("precision", 0.91)
    mlflow.log_metric("recall", 0.84)
    print("✅ Logged dummy MLflow run.")
