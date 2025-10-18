# 🚗 Car Price Prediction API

A FastAPI-based REST API for predicting car prices using machine learning.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

**Option A: Using the shell script (Linux/Mac)**
```bash
chmod +x run_server.sh
./run_server.sh
```

**Option B: Using uvicorn directly**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Option C: Using Python**
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📡 API Endpoints

### GET `/`
Health check endpoint

**Response:**
```json
{
  "message": "Car Price API running successfully"
}
```

### POST `/predict`
Predict car price based on features

**Request Body Example:**
```json
{
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
```

**Response:**
```json
{
  "predicted_price": 13328.45
}
```

## 🧪 Testing with Postman

1. **Start the server** (see Quick Start above)
2. **Create a new request** in Postman
3. **Configure the request:**
   - Method: `POST`
   - URL: `http://localhost:8000/predict`
   - Headers: `Content-Type: application/json`
   - Body: Select `raw` and `JSON`, then paste the sample request from `sample_request.json`
4. **Click Send**

### Testing GET endpoint:
- Method: `GET`
- URL: `http://localhost:8000/`

## 🐛 Troubleshooting

### API not responding / hanging
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check if the server is actually running
- Make sure you're using the correct URL and port
- Check if another application is using port 8000

### Import errors
```bash
pip install --upgrade -r requirements.txt
```

### Model file not found
Make sure `xgb_car_price_pipeline.pkl` is in the same directory as `main.py`

## 📊 Features

**Input Parameters:**
- **Levy**: Tax levy amount (string, can be "-" for no levy)
- **Manufacturer**: Car manufacturer (e.g., LEXUS, TOYOTA, BMW)
- **Model**: Car model name
- **Prod_year**: Production year
- **Category**: Car category (Sedan, Jeep, Hatchback, etc.)
- **Leather_interior**: "Yes" or "No"
- **Fuel_type**: Petrol, Diesel, Hybrid, etc.
- **Engine_volume**: Engine size in liters
- **Mileage**: Total kilometers driven
- **Cylinders**: Number of cylinders
- **Gear_box_type**: Automatic, Manual, Tiptronic, etc.
- **Drive_wheels**: Front, Rear, 4x4
- **Wheel**: Left wheel or Right-hand drive
- **Color**: Car color
- **Airbags**: Number of airbags
- **Age**: Age of the car in years
- **Mileage_per_year**: Optional (auto-calculated if not provided)

## 🔧 Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **XGBoost**: Machine learning model for predictions
- **Pandas**: Data manipulation
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server
