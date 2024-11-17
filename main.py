from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

# Load model and scaler
model = joblib.load('kmeans_model.joblib')
scaler = joblib.load('scaler.joblib')

@app.get("/")
def root():
    return "Welcome To Tuwaiq Academy"

class InputFeatures(BaseModel):
    age: float
    appearance: int
    minutes_played: float
    days_injured: int
    games_injured: int
    award: int
    highest_value: float
    position: str


def preprocessing(input_features: InputFeatures):
    dict_f = {
        'age': input_features.age,
        'appearance': input_features.appearance,
        'minutes played': input_features.minutes_played,
        'days_injured': input_features.days_injured,
        'games_injured': input_features.games_injured,
        'award': input_features.award,
        'highest_value': input_features.highest_value,
        'position_Goalkeeper': int(input_features.position == 'Goalkeeper'),
        'position_midfield': int(input_features.position == 'Midfield'),
    }
    print(f"dict_f: {dict_f}")  # Add debug log here
    features_list = [dict_f[key] for key in sorted(dict_f)]
    print(f"features_list: {features_list}")  # Add debug log here
    scaled_features = scaler.transform([features_list])
    return scaled_features


@app.post("/predict")
async def predict(input_features: InputFeatures):
    data = preprocessing(input_features)
    y_pred = model.predict(data)
    return {"pred": y_pred.tolist()[0]}