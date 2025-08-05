# mlflow/log_run.py

import mlflow
import os
import random
import string 
from datetime import datetime
from pathlib import Path

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


# 🕒 Timestamp
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
def generate_run_id(length=32):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
run_id = generate_run_id()


# 🌐 Save static report
with open("docs/report.html", "w") as f:
    f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>📊 Fraud Detection Run Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            padding: 40px;
        }}
        .report {{
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
        }}
        .metric {{
            font-size: 1.1em;
            margin: 8px 0;
        }}
        .meta {{
            color: #555;
            font-size: 0.9em;
            margin-top: 20px;
        }}
        code {{
            background-color: #eee;
            padding: 2px 5px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="report">
        <h1>📋 MLflow Run Summary</h1>

        <div class="metric"><strong>Model:</strong> K-Nearest Neighbors (KNN)</div>
        <div class="metric"><strong>Threshold:</strong> 0.99</div>

        <hr>

        <div class="metric"><strong>Accuracy:</strong> 98.7%</div>
        <div class="metric"><strong>Precision:</strong> 91%</div>
        <div class="metric"><strong>Recall:</strong> 84%</div>

        <hr>

        <div class="meta">📆 Run Time: {timestamp}</div>
        <div class="meta">🆔 Run ID: <code>{run_id}</code></div>
        <div class="meta">📁 Experiment: <code>FraudDetection-Demo</code></div>
    </div>
</body>
</html>
""")



