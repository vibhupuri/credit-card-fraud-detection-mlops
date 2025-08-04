from fastapi import FastAPI, Request
import joblib
import numpy as np
import os
import requests
import time

app = FastAPI()

# Model download config
MODEL_URL = "https://github.com/vibhupuri/credit-card-fraud-detection-mlops/releases/download/v1.0/model.pkl"
MODEL_LOCAL_PATH = "/tmp/model.pkl"

def download_model():
    retries = 3
    delay = 2  # seconds
    for i in range(retries):
        try:
            response = requests.get(MODEL_URL)
            response.raise_for_status()
            with open(MODEL_LOCAL_PATH, "wb") as f:
                f.write(response.content)
            print("✅ Model downloaded successfully.")
            return
        except Exception as e:
            print(f"⚠️ Attempt {i+1} failed: {e}")
            time.sleep(delay)
    raise RuntimeError("❌ Failed to download model after multiple attempts.")

# Ensure model is downloaded
if not os.path.exists(MODEL_LOCAL_PATH):
    print("📦 Downloading model...")
    download_model()

# Load model
model = joblib.load(MODEL_LOCAL_PATH)
print("✅ Model loaded.")

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)
    return {"prediction": int(prediction[0])}
