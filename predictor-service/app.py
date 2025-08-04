from fastapi import FastAPI, Request
import joblib
import numpy as np
import os

app = FastAPI()
model_path = os.getenv("MODEL_PATH", "/shared/model.pkl")
model = joblib.load(model_path)

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)
    return {"prediction": int(prediction[0])}
