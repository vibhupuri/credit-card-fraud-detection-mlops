import streamlit as st
import pandas as pd
import requests
import os

st.title("💳 Real-Time Credit Card Fraud Detection")

# Predictor service URL 
PREDICT_URL = PREDICT_URL = os.getenv("PREDICT_URL", "https://musical-yodel-g4jwgvv4554hwvv-8000.app.github.dev/predict")

fields = {
    "Transaction Amount": st.number_input("Transaction Amount (₹)", min_value=0.0),
    "Category": st.text_input("Category"),
    "City": st.text_input("City"),
    "State": st.text_input("State"),
    "Job": st.text_input("Job"),
    "Merchant": st.text_input("Merchant"),
    "Gender": st.selectbox("Gender", ['M', 'F']),
    "Zip Code": st.number_input("Zip Code", min_value=10000, max_value=99999),
    "City Population": st.number_input("City Population", min_value=0),
    "Latitude": st.number_input("Latitude"),
    "Longitude": st.number_input("Longitude"),
    "Merchant Latitude": st.number_input("Merchant Latitude"),
    "Merchant Longitude": st.number_input("Merchant Longitude"),
}

if st.button("🚨 Detect Fraud"):
    try:
        # Rename keys to match model input
        key_map = {
            "Transaction Amount": "amt",
            "Category": "category",
            "City": "city",
            "State": "state",
            "Job": "job",
            "Merchant": "merchant",
            "Gender": "gender",
            "Zip Code": "zip",
            "City Population": "city_pop",
            "Latitude": "lat",
            "Longitude": "long",
            "Merchant Latitude": "merch_lat",
            "Merchant Longitude": "merch_long"
        }
        model_input = {model_key: fields[user_key] for user_key, model_key in key_map.items()}

        # Send to predictor
        response = requests.post(PREDICT_URL, json=model_input)

        if response.status_code == 200:
            result = response.json()
            prediction = result.get("prediction")

            if prediction is None:
                st.error("❌ No 'prediction' key in response.")
                st.json(result)
            elif prediction == 1:
                st.error("⚠️ This transaction is likely FRAUDULENT.")
            else:
                st.success("✅ This transaction appears LEGITIMATE.")
        else:
            st.error(f"❌ Server returned {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.error(f"❌ Exception occurred: {e}")


