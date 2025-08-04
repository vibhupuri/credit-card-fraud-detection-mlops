from fastapi import FastAPI, Request
import joblib
import numpy as np
import os
import requests

app = FastAPI()

MODEL_URL = "https://github.com/vibhupuri/credit-card-fraud-detection-mlops/releases/download/v1.0/model.pkl"
MODEL_LOCAL_PATH = "/tmp/model.pkl"
model = None  # Global placeholder

@app.on_event("startup")
def load_model():
    global model
    if not os.path.exists(MODEL_LOCAL_PATH):
        print("📦 Downloading model from GitHub...")
        response = requests.get(MODEL_URL)
        with open(MODEL_LOCAL_PATH, "wb") as f:
            f.write(response.content)
        print("✅ Model downloaded.")
    model = joblib.load(MODEL_LOCAL_PATH)
    print("✅ Model loaded.")

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)
    return {"prediction": int(prediction[0])}
