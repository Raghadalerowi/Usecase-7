import streamlit as st
import requests
import json

# FastAPI endpoint URL
API_URL = "https://usecase-7knn.onrender.com/predict"


# Function to make the POST request to the FastAPI model
def get_prediction(data):
    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Something went wrong"}


# Streamlit app UI
st.title("Football Player Prediction")

# Input fields for the prediction
age = st.number_input("Age", min_value=18, max_value=40, value=25)
appearance = st.number_input("Appearances", min_value=0, value=30)
minutes_played = st.number_input("Minutes Played", min_value=0, value=2700)
days_injured = st.number_input("Days Injured", min_value=0, value=15)
games_injured = st.number_input("Games Injured", min_value=0, value=3)
award = st.number_input("Award (Numeric)", min_value=0, value=1)
highest_value = st.number_input("Highest Value", min_value=0.0, value=15.5)
position = st.selectbox("Position", options=["Goalkeeper", "Midfield"])

# Prepare the data for the API call
data = {
    "age": age,
    "appearance": appearance,
    "minutes_played": minutes_played,
    "days_injured": days_injured,
    "games_injured": games_injured,
    "award": award,
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