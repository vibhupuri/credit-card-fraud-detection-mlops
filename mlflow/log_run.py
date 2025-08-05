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

html_report = f"""
<html>
<head><title>Prediction Log Summary</title></head>
<body>
    <h1>Prediction Run Summary</h1>
    <ul>
        <li><strong>Experiment:</strong> FraudDetection-Demo</li>
        <li><strong>Prediction:</strong> {int(y_pred[0])} (Probability: {y_proba[0]:.4f})</li>
        <li><strong>Logged to:</strong> {mlflow.get_tracking_uri()}</li>
    </ul>
</body>
</html>
"""

with open("report.html", "w") as f:
    f.write(html_report)


