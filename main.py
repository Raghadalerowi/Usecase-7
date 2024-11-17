from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel
#import sklearn
model = joblib.load('knn_model.joblib')
scaler = joblib.load('scaler.joblib')
app = FastAPI()
# GET request
@app.get("/")
def read_root():
    return {"message": "Welcome to Tuwaiq Academy"}
# get request
@app.get("/items/")
def create_item(item: dict):
    return {"item": item}

# Define a Pydantic model for input data validation
class InputFeatures(BaseModel):
    highest_value: int
    appearance: int
    minutes_played: int
    award: int
    assists: float
    goals: float
    games_injured: int
def preprocessing(input_features: InputFeatures):
    dict_f = {
    'highest_value': input_features.highest_value,
    'appearance': input_features.appearance,
    'minutes played': input_features.minutes_played,
    'award': input_features.award,
    'assists': input_features.assists,
    'goals': input_features.goals,
    'games_injured': input_features.games_injured ,
    }
    # Convert dictionary values to a list in the correct order
    features_list = [dict_f[key] for key in sorted(dict_f)]
    # Scale the input features
    scaled_features = scaler.transform([list(dict_f.values())])
    return scaled_features
@app.get("/predict")
def predict(input_features: InputFeatures):
    return preprocessing(input_features)


@app.post("/predict")
async def predict(input_features: InputFeatures):
    data = preprocessing(input_features)
    y_pred = model.predict(data)
    return {"pred": y_pred.tolist()[0]}