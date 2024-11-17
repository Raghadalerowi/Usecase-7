from sklearn.preprocessing import StandardScaler
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import joblib

# Initialize the FastAPI app
app = FastAPI()

# Load the pre-trained model and scaler from disk
model = joblib.load('knn_model.joblib')
scaler = joblib.load('scaler.joblib')

# Define a Pydantic model for input data validation
class InputFeatures(BaseModel):
    position: str
    height: float
    age: float
    appearance: int
    minutes_played: int
    current_value: int
    highest_value: int

# Preprocessing function to convert input data into a format suitable for the model
def preprocessing(input_features: InputFeatures):
    # Dictionary for the input features
    dict_f = {
        'Position_Forward': input_features.position == 'Forward',
        'Position_Midfielder': input_features.position == 'Midfielder',
        'Position_Defender': input_features.position == 'Defender',
        'Position_Goalkeeper': input_features.position == 'Goalkeeper',
        
        # Numerical features
        'Height': input_features.height,
        'Age': input_features.age,
        'Appearance': input_features.appearance,
        'Minutes_Played': input_features.minutes_played,
        'Current_Value': input_features.current_value,
        'Highest_Value': input_features.highest_value
    }
    
    # Convert dictionary values to a list in the correct order
    features_list = [dict_f[key] for key in sorted(dict_f)]
    
    # Scale the input features using the loaded scaler (assuming the scaler was already fitted)
    scaled_features = scaler.transform([features_list])  # Reshape to 2D array for scaling
    
    return scaled_features

# Route to display a welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to Tuwaiq Academy"}

# Route for handling the "items" endpoint
@app.get("/items/")
def create_item(item: dict):
    return {"item": item}

# Route to handle the prediction process
@app.post("/predict")
async def predict(input_features: InputFeatures):
    # Preprocess the input features
    data = preprocessing(input_features)
    
    # Predict the result using the pre-trained model
    y_pred = model.predict(data)
    
    # Return the prediction as a JSON response
    return {"prediction": y_pred.tolist()[0]}  # Convert numpy array to list for JSON response
