from fastapi import FastAPI, Request
import joblib
import numpy as np
import os
import requests

app = FastAPI()

# GitHub release URL for model.pkl
MODEL_URL = "https://github.com/vibhupuri/credit-card-fraud-detection-mlops/releases/download/v1.0/model.pkl"
MODEL_LOCAL_PATH = "/tmp/model.pkl"

# Download model if not already present
if not os.path.exists(MODEL_LOCAL_PATH):
    print("Downloading model...")
    response = requests.get(MODEL_URL)
    with open(MODEL_LOCAL_PATH, "wb") as f:
        f.write(response.content)

# Load model
model = joblib.load(MODEL_LOCAL_PATH)

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)
    return {"prediction": int(prediction[0])}
