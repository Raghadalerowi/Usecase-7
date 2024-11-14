import streamlit as st
import requests

# Define the FastAPI server URL (assuming it's running locally)
API_URL = "http://127.0.0.1:8000/predict"

# Streamlit app UI
st.title("Football Player Prediction")

# User input fields
position = st.selectbox("Position", ["Forward", "Midfielder", "Defender", "Goalkeeper"])
height = st.number_input("Height (m)", min_value=0.0, max_value=3.0, step=0.01)
age = st.number_input("Age (years)", min_value=0, max_value=100, step=1)
appearance = st.number_input("Appearances", min_value=0, max_value=1000, step=1)
minutes_played = st.number_input("Minutes Played", min_value=0, max_value=100000, step=1)
current_value = st.number_input("Current Value (in USD)", min_value=0, max_value=100000000, step=100000)
highest_value = st.number_input("Highest Value (in USD)", min_value=0, max_value=100000000, step=100000)

# Prepare the input dictionary
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
    try:
        response = requests.post(API_URL, json=input_data)
        response_data = response.json()
        
        # Display the prediction
        st.write(f"Prediction Result: {response_data['prediction']}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to FastAPI backend: {e}")

