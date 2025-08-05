import mlflow

mlflow.set_tracking_uri("http://mlflow:5000")

with mlflow.start_run():
    mlflow.log_param("model", "KNN")
    mlflow.log_param("features", 12)
    mlflow.log_param("threshold", 0.99)
    mlflow.log_metric("precision", 0.92)
    mlflow.log_metric("recall", 0.81)
