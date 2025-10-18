#!/usr/bin/env python3
"""
Test script to verify the API works correctly before testing in Postman.
This script tests the model loading and prediction logic.
"""

import json
import sys

def test_imports():
    """Test if all required packages are installed"""
    print("=" * 60)
    print("TEST 1: Checking imports...")
    print("=" * 60)
    
    try:
        import fastapi
        print("✓ fastapi installed")
    except ImportError as e:
        print(f"✗ fastapi not installed: {e}")
        return False
    
    try:
        import pydantic
        print("✓ pydantic installed")
    except ImportError as e:
        print(f"✗ pydantic not installed: {e}")
        return False
    
    try:
        import joblib
        print("✓ joblib installed")
    except ImportError as e:
        print(f"✗ joblib not installed: {e}")
        return False
    
    try:
        import pandas
        print("✓ pandas installed")
    except ImportError as e:
        print(f"✗ pandas not installed: {e}")
        return False
    
    try:
        import xgboost
        print("✓ xgboost installed")
    except ImportError as e:
        print(f"✗ xgboost not installed: {e}")
        return False
    
    try:
        import uvicorn
        print("✓ uvicorn installed")
    except ImportError as e:
        print(f"✗ uvicorn not installed: {e}")
        return False
    
    print("\n✓ All imports successful!\n")
    return True

def test_model_loading():
    """Test if the model file can be loaded"""
    print("=" * 60)
    print("TEST 2: Loading model...")
    print("=" * 60)
    
    try:
        import joblib
        import os
        
        model_path = "xgb_car_price_pipeline.pkl"
        
        if not os.path.exists(model_path):
            print(f"✗ Model file not found: {model_path}")
            return False, None
        
        print(f"✓ Model file exists: {model_path}")
        
        model = joblib.load(model_path)
        print("✓ Model loaded successfully!")
        print(f"  Model type: {type(model).__name__}\n")
        
        return True, model
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False, None

def test_prediction():
    """Test the prediction logic"""
    print("=" * 60)
    print("TEST 3: Testing prediction logic...")
    print("=" * 60)
    
    try:
        import pandas as pd
        import joblib
        
        # Load model
        model = joblib.load("xgb_car_price_pipeline.pkl")
        
        # Sample data (from the CSV)
        test_data = {
            'Levy': 1399,
            'Manufacturer': 'LEXUS',
            'Model': 'RX 450',
            'Prod. year': 2010,
            'Category': 'Jeep',
            'Leather interior': 1,  # Already converted (Yes = 1)
            'Fuel type': 'Hybrid',
            'Engine volume': 3.5,
            'Mileage': 186005,
            'Cylinders': 6.0,
            'Gear box type': 'Automatic',
            'Drive wheels': '4x4',
            'Wheel': 'Left wheel',
            'Color': 'Silver',
            'Airbags': 12,
            'Age': 15,
            'Mileage_per_year': 12400.0
        }
        
        print("Test input data:")
        for key, value in test_data.items():
            print(f"  {key}: {value}")
        print()
        
        # Create DataFrame
        df = pd.DataFrame([test_data])
        
        # Ensure correct column order
        expected_columns = [
            'Levy', 'Manufacturer', 'Model', 'Prod. year', 'Category', 'Leather interior',
            'Fuel type', 'Engine volume', 'Mileage', 'Cylinders', 'Gear box type',
            'Drive wheels', 'Wheel', 'Color', 'Airbags', 'Age', 'Mileage_per_year'
        ]
        df = df[expected_columns]
        
        # Cast data types
        df['Levy'] = df['Levy'].astype('int64')
        df['Mileage'] = df['Mileage'].astype('int64')
        df['Airbags'] = df['Airbags'].astype('int64')
        df['Leather interior'] = df['Leather interior'].astype('int64')
        df['Prod. year'] = df['Prod. year'].astype('int64')
        df['Age'] = df['Age'].astype('int64')
        df['Engine volume'] = df['Engine volume'].astype('float64')
        df['Cylinders'] = df['Cylinders'].astype('float64')
        df['Mileage_per_year'] = df['Mileage_per_year'].astype('float64')
        
        print("✓ DataFrame created and formatted")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {len(df.columns)}\n")
        
        # Make prediction
        prediction = model.predict(df)
        predicted_price = float(prediction[0])
        
        print(f"✓ Prediction successful!")
        print(f"  Predicted price: ${predicted_price:,.2f}\n")
        
        return True
    except Exception as e:
        print(f"✗ Error during prediction: {e}")
        import traceback
        print("\nFull error:")
        print(traceback.format_exc())
        return False

def test_api_schema():
    """Test the API request schema"""
    print("=" * 60)
    print("TEST 4: Validating API schema...")
    print("=" * 60)
    
    try:
        from pydantic import BaseModel
        from typing import Optional
        
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
        
        # Test data from sample_request.json
        sample_request = {
            "Levy": "1399",
            "Manufacturer": "LEXUS",
            "Model": "RX 450",
            "Prod_year": 2010,
            "Category": "Jeep",
            "Leather_interior": "Yes",
            "Fuel_type": "Hybrid",
            "Engine_volume": 3.5,
            "Mileage": 186005,
            "Cylinders": 6.0,
            "Gear_box_type": "Automatic",
            "Drive_wheels": "4x4",
            "Wheel": "Left wheel",
            "Color": "Silver",
            "Airbags": 12,
            "Age": 15,
            "Mileage_per_year": 12400
        }
        
        print("Testing sample request validation...")
        features = CarFeatures(**sample_request)
        print("✓ Sample request schema is valid!")
        print(f"  All {len(sample_request)} fields validated\n")
        
        return True
    except Exception as e:
        print(f"✗ Schema validation error: {e}")
        import traceback
        print("\nFull error:")
        print(traceback.format_exc())
        return False

def main():
    print("\n")
    print("🚗" * 30)
    print("CAR PRICE PREDICTION API - TEST SUITE")
    print("🚗" * 30)
    print("\n")
    
    all_passed = True
    
    # Run all tests
    if not test_imports():
        print("\n❌ FAILED: Install dependencies with: pip install -r requirements.txt")
        all_passed = False
    
    success, model = test_model_loading()
    if not success:
        print("\n❌ FAILED: Model loading failed")
        all_passed = False
    
    if not test_prediction():
        print("\n❌ FAILED: Prediction test failed")
        all_passed = False
    
    if not test_api_schema():
        print("\n❌ FAILED: API schema validation failed")
        all_passed = False
    
    # Final summary
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    if all_passed:
        print("\n✅ ALL TESTS PASSED!")
        print("\n📝 Next steps:")
        print("  1. Start the server: ./run_server.sh")
        print("     or: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        print("\n  2. Test in Postman:")
        print("     - GET  http://localhost:8000/")
        print("     - POST http://localhost:8000/predict")
        print("\n  3. Use the sample request from: sample_request.json")
        print("\n")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        print("\nPlease fix the issues above before running the API")
        print("\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
