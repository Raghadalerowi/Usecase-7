import streamlit as st
import requests
import json 

# Define the FastAPI server URL (your remote URL)
API_URL = "https://usecase-7svm.onrender.com/predict"

def get_prediction(input_data):
    response = requests.post(API_URL, json=input_data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Something went wrong"}
    
# Streamlit app UI
st.title("Football Player Prediction SVM")

# User input fields with updated min/max values
position = st.selectbox("Position", ["Forward", "Midfielder", "Defender", "Goalkeeper"])
height = st.number_input("Height (cm)", min_value=140, max_value=200)
age = st.number_input("Age (years)", min_value=19, max_value=35)
appearance = st.number_input("Appearances", min_value=200, max_value=9000)
minutes_played = st.number_input("Minutes Played", min_value=120, max_value=100000)
current_value = st.number_input("Current Value (in USD)", min_value=10000, max_value=70000000)
highest_value = st.number_input("Highest Value (in USD)", min_value=10000, max_value=70000000)

# Prepare the input dictionary with the user inputs
input_data = {
    "position": position,
    "height": height,
    "age": age,
    "appearance": appearance,
    "minutes_played": minutes_played,
    "current_value": current_value,
    "highest_value": highest_value
}

# When the user clicks the "Predict" button, send the input to the FastAPI backend
if st.button("Predict"):
    prediction = get_prediction(input_data)

    if "error" in prediction:
        st.error(prediction["error"])
    else:
        st.success(f"Prediction: {prediction['pred']}")
