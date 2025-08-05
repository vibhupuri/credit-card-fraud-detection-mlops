# mlflow/log_run.py

import mlflow
import os

# Use file-based local store instead of HTTP server
mlflow.set_tracking_uri("file:///tmp/mlruns")

mlflow.set_experiment("FraudDetection-Demo")

with mlflow.start_run():
    mlflow.log_param("model", "KNN")
    mlflow.log_param("threshold", 0.99)
    mlflow.log_metric("precision", 0.91)
    mlflow.log_metric("recall", 0.84)
    mlflow.log_metric("accuracy", 0.987)
    print("✅ Logged dummy MLflow run.")

