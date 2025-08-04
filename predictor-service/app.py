from fastapi import FastAPI, Request, HTTPException
import joblib
import numpy as np
import os
import requests
import asyncio

app = FastAPI()

# GitHub release URL for model.pkl
MODEL_URL = "https://github.com/vibhupuri/credit-card-fraud-detection-mlops/releases/download/v1.0/model.pkl"
MODEL_LOCAL_PATH = "/tmp/model.pkl"

# Download model if not already present
if not os.path.exists(MODEL_LOCAL_PATH):
    try:
        print("📦 Downloading model from GitHub...")
        response = requests.get(MODEL_URL)
        response.raise_for_status()
        with open(MODEL_LOCAL_PATH, "wb") as f:
            f.write(response.content)
        print("✅ Model downloaded.")
    except Exception as e:
        print(f"❌ Failed to download model: {e}")
        raise RuntimeError("Model download failed.")

# Load model
try:
    model = joblib.load(MODEL_LOCAL_PATH)
    print("✅ Model loaded.")
except Exception as e:
    print(f"❌ Model loading failed: {e}")
    raise RuntimeError("Model loading failed.")

@app.post("/predict")
async def predict(request: Request):
    try:
        data = await request.json()
        features = np.array(data["features"]).reshape(1, -1)

        async def run_prediction():
            return model.predict(features)

        prediction = await asyncio.wait_for(run_prediction(), timeout=3.0)
        return {"prediction": int(prediction[0])}

    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Prediction timed out.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
