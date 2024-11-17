import streamlit as st
import requests
import json

# FastAPI endpoint URL
API_URL = "https://usecase-7-vxqr.onrender.com/predict"

# Function to make the POST request to the FastAPI model
def get_prediction(data):
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Unexpected status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

# Streamlit app UI
st.title("Football Player Prediction")

# Input fields for the prediction
age = st.number_input("Age", min_value=18, max_value=40, value=25)
appearance = st.number_input("Appearances", min_value=0, value=30)
minutes_played = st.number_input("Minutes Played", min_value=0, value=2700)
highest_value = st.number_input("Highest Value", min_value=0.0, value=100.0, step=0.1)
position = st.selectbox("Position", options=["Goalkeeper", "Midfield","Attack","Defender"])

# Prepare the data for the API call
data = {
    "age": age,
    "appearance": appearance,
    "minutes_played": minutes_played, # Ensure the type matches API requirements
    "highest_value": highest_value,
    "position": position
}

# When the user clicks the "Predict" button
if st.button("Predict"):
    prediction = get_prediction(data)

    if "error" in prediction:
        st.error(prediction["error"])
    else:
        st.success(f"Prediction: {prediction['pred']}")
