from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import joblib
import pandas as pd
import traceback
import warnings

# Suppress sklearn version warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Compatibility fix for sklearn version differences
import sklearn.compose._column_transformer as ct
if not hasattr(ct, '_RemainderColsList'):
    ct._RemainderColsList = list

# Initialize FastAPI
app = FastAPI(title="Car Price API")

# Add CORS middleware to allow requests from Postman and browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained pipeline
model = joblib.load("xgb_car_price_pipeline.pkl")

# Define what the input data should look like
class CarFeatures(BaseModel):
    Levy: str
    Manufacturer: str
    Model: str
    Prod_year: int
    Category: str
    Leather_interior: str
    Fuel_type: str
    Engine_volume: float
    Mileage: float
    Cylinders: float
    Gear_box_type: str
    Drive_wheels: str
    Wheel: str
    Color: str
    Airbags: float
    Age: int
    Mileage_per_year: Optional[float] = None

    class Config:
        populate_by_name = True

# Mapping from API schema fields to model/dataset fields
api_to_model_fields = {
    "Levy": "Levy",
    "Manufacturer": "Manufacturer",
    "Model": "Model",
    "Prod_year": "Prod. year",
    "Category": "Category",
    "Leather_interior": "Leather interior",
    "Fuel_type": "Fuel type",
    "Engine_volume": "Engine volume",
    "Mileage": "Mileage",
    "Cylinders": "Cylinders",
    "Gear_box_type": "Gear box type",
    "Drive_wheels": "Drive wheels",
    "Wheel": "Wheel",
    "Color": "Color",
    "Airbags": "Airbags",
    "Age": "Age",
    "Mileage_per_year": "Mileage_per_year"
}

def map_api_to_model(data: dict):
    model_data = {}
    for api_key, model_key in api_to_model_fields.items():
        if api_key in data:
            # Map Leather_interior to 1/0
            if api_key == "Leather_interior":
                model_data[model_key] = 1 if data[api_key] == "Yes" else 0
            # Convert Levy to float (will be cast to int64 later)
            elif api_key == "Levy":
                try:
                    model_data[model_key] = float(data[api_key])
                except ValueError:
                    model_data[model_key] = 0.0
            else:
                model_data[model_key] = data[api_key]
        else:
            model_data[model_key] = None
    return model_data

# Define root endpoint
@app.get("/")
def home():
    return {"message": "Car Price API running successfully"}

# Define prediction endpoint
@app.post("/predict")
async def predict_price(features: CarFeatures):
    try:
        data_dict = features.model_dump()
        model_data = map_api_to_model(data_dict)
        
        # Calculate Mileage_per_year if None
        if model_data["Mileage_per_year"] is None:
            model_data["Mileage_per_year"] = model_data["Mileage"] / max(model_data["Age"], 0.1)
        
        df = pd.DataFrame([model_data])
        print("Input DataFrame:", df.to_dict())
        print("Input dtypes:", df.dtypes.to_dict())
        
        # Enforce training data column order
        expected_columns = [
            'Levy', 'Manufacturer', 'Model', 'Prod. year', 'Category', 'Leather interior',
            'Fuel type', 'Engine volume', 'Mileage', 'Cylinders', 'Gear box type',
            'Drive wheels', 'Wheel', 'Color', 'Airbags', 'Age', 'Mileage_per_year'
        ]
        df = df[expected_columns]
        
        # Cast data types to match training data
        df['Levy'] = df['Levy'].astype('int64')
        df['Mileage'] = df['Mileage'].astype('int64')
        df['Airbags'] = df['Airbags'].astype('int64')
        df['Leather interior'] = df['Leather interior'].astype('int64')
        df['Prod. year'] = df['Prod. year'].astype('int64')
        df['Age'] = df['Age'].astype('int64')
        df['Engine volume'] = df['Engine volume'].astype('float64')
        df['Cylinders'] = df['Cylinders'].astype('float64')
        df['Mileage_per_year'] = df['Mileage_per_year'].astype('float64')
        
        print("Processed DataFrame:", df.to_dict())
        print("Processed dtypes:", df.dtypes.to_dict())
        
        prediction = model.predict(df)
        price = float(prediction[0])
        
        return {"predicted_price": round(price, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}\n{traceback.format_exc()}")
