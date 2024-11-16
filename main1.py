#1st step
from fastapi import FastAPI , HTTPException
app = FastAPI()
 # GET request
@app.get("/")
def read_root():
    return {"message": "Welcome to Tuwaiq Academy"}
 # get request
@app.get("/items/")
def create_item(item: dict):
    return {"item": item}

#2nd step
from pydantic import BaseModel
# Define a Pydantic model for input data validation
class InputFeatures(BaseModel):
    position: str
    height: float
    age: float
    appearance: int
    minutes_played: int
    current_value: int
    highest_value: int
def preprocessing(input_features: InputFeatures): 
    dict_f = {
            'Position_Forward': input_features.position == 'Forward',
            'Position_Midfielder': input_features.position == 'Midfielder',
            'Position_Defender': input_features.position == 'Defender',
            'Position_Goalkeeper': input_features.position == 'Goalkeeper',
            'Height': input_features.height, 
            'Age': input_features.age, 
            'Appearance': input_features.appearance, 
            'Minutes_Played': input_features.minutes_played, 
            'Current_Value': input_features.current_value, 
            'Highest_Value': input_features.highest_value
        }
    return dict_f

@app.get("/predict")
def predict(input_features: InputFeatures):
    return preprocessing(input_features)

from sklearn.preprocessing import StandardScaler

# Assuming scaler is already fitted elsewhere in your code
scaler1 = StandardScaler()

class InputFeatures(BaseModel):
    position: str
    height: float
    age: float
    appearance: int
    minutes_played: int
    current_value: int
    highest_value: int

def preprocessing(input_features: InputFeatures): 
    # Dictionary for the input features
    dict_f = {
        # Categorical features (one-hot encoding for position)
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
    
    # Scale the input features
    scaled_features = scaler.transform([features_list])  # Reshape to 2D array for scaling
    
    return scaled_features

@app.post("/predict")
async def predict(input_features: InputFeatures):
    data = preprocessing(input_features)
    y_pred = model.predict(data)
    return {"pred": y_pred.tolist()[0]}