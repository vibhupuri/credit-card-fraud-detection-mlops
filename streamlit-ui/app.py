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
        # Send POST request
        payload = {"features": list(fields.values())}
        response = requests.post(PREDICT_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            if result["prediction"] == 1:
                st.error("⚠️ This transaction is likely FRAUDULENT.")
            else:
                st.success("✅ This transaction appears LEGITIMATE.")
        else:
            st.error(f"Server returned status code {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")
