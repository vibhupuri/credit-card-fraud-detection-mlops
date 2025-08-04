from fastapi import FastAPI, Request
import os
import joblib
import pandas as pd
import numpy as np
import requests

app = FastAPI()

# ─────────── GitHub Release URLs for All Artifacts ───────────
REPO_RELEASE_BASE = "https://github.com/vibhupuri/credit-card-fraud-detection-mlops/releases/download/v1.0/"
MODEL_URL = REPO_RELEASE_BASE + "model.pkl"
TRANSFORMER_URL = REPO_RELEASE_BASE + "transformer.pkl"
XTRAIN_COLS_URL = REPO_RELEASE_BASE + "xtrain_columns.pkl"

MODEL_PATH = "/tmp/model.pkl"
TRANSFORMER_PATH = "/tmp/transformer.pkl"
XTRAIN_COLS_PATH = "/tmp/xtrain_columns.pkl"

def download_if_missing(url, path):
    if not os.path.exists(path):
        print(f"📦 Downloading {os.path.basename(path)}...")
        response = requests.get(url)
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded {os.path.basename(path)}")

# ─────────── Download All Required Files ───────────
download_if_missing(MODEL_URL, MODEL_PATH)
download_if_missing(TRANSFORMER_URL, TRANSFORMER_PATH)
download_if_missing(XTRAIN_COLS_URL, XTRAIN_COLS_PATH)

# ─────────── Load the Artifacts ───────────
model = joblib.load(MODEL_PATH)
transformer = joblib.load(TRANSFORMER_PATH)
xtrain_columns = joblib.load(XTRAIN_COLS_PATH)

print("✅ All artifacts loaded successfully.")

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()

    # Wrap raw input into DataFrame
    input_df = pd.DataFrame([data])

    try:
        # Transform input
        transformed = transformer.transform(input_df)
        transformed_df = pd.DataFrame(transformed, columns=xtrain_columns)

        # Predict probability
        proba = model.predict_proba(transformed_df)[0][1]
        prediction = int(proba >= 0.99)

        return {
            "prediction": prediction,
            "fraud_probability": round(proba, 4)
        }

    except Exception as e:
        return {"error": str(e)}
