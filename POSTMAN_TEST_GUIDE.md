# 📬 Postman Testing Guide

## ✅ Status: **READY TO TEST**

All tests have passed! The API is ready to use in Postman.

---

## 🚀 Step 1: Start the Server

Open a terminal and run:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Or use the provided script:
```bash
./run_server.sh
```

You should see output like:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 📡 Step 2: Test GET Endpoint (Health Check)

**In Postman:**

1. Create a new request
2. Set method to: `GET`
3. Set URL to: `http://localhost:8000/`
4. Click **Send**

**Expected Response (200 OK):**
```json
{
    "message": "Car Price API running successfully"
}
```

---

## 📡 Step 3: Test POST Endpoint (Price Prediction)

**In Postman:**

1. Create a new request
2. Set method to: `POST`
3. Set URL to: `http://localhost:8000/predict`
4. Go to **Headers** tab and add:
   - Key: `Content-Type`
   - Value: `application/json`
5. Go to **Body** tab:
   - Select `raw`
   - Select `JSON` from the dropdown
6. Paste this JSON:

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

7. Click **Send**

**Expected Response (200 OK):**
```json
{
    "predicted_price": 11118.31
}
```

---

## 🧪 Additional Test Cases

### Test Case 2: Different Car (Toyota)
```json
{
  "Levy": "1053",
  "Manufacturer": "TOYOTA",
  "Model": "Camry",
  "Prod_year": 2014,
  "Category": "Sedan",
  "Leather_interior": "Yes",
  "Fuel_type": "Hybrid",
  "Engine_volume": 2.5,
  "Mileage": 398069,
  "Cylinders": 4.0,
  "Gear_box_type": "Automatic",
  "Drive_wheels": "Front",
  "Wheel": "Left wheel",
  "Color": "Black",
  "Airbags": 12,
  "Age": 11
}
```

### Test Case 3: Without Mileage_per_year (Auto-calculated)
```json
{
  "Levy": "810",
  "Manufacturer": "HYUNDAI",
  "Model": "Elantra",
  "Prod_year": 2016,
  "Category": "Sedan",
  "Leather_interior": "Yes",
  "Fuel_type": "Petrol",
  "Engine_volume": 1.8,
  "Mileage": 121840,
  "Cylinders": 4.0,
  "Gear_box_type": "Automatic",
  "Drive_wheels": "Front",
  "Wheel": "Left wheel",
  "Color": "Blue",
  "Airbags": 12,
  "Age": 9
}
```

---

## ❌ Common Issues & Solutions

### Issue 1: "Connection refused" or "Could not get response"
**Solution:** Make sure the server is running! Check the terminal where you started `uvicorn`.

### Issue 2: "Unprocessable Entity" (422 Error)
**Solution:** Check that:
- All required fields are present in your JSON
- Field names match exactly (case-sensitive!)
- Data types are correct:
  - `Levy`: string (e.g., "1399")
  - `Prod_year`: integer (e.g., 2010)
  - `Engine_volume`: float (e.g., 3.5)
  - `Airbags`: float (e.g., 12.0 or 12)
  - `Leather_interior`: "Yes" or "No" (string)

### Issue 3: "Internal Server Error" (500 Error)
**Solution:** Check the terminal where the server is running for detailed error messages.

### Issue 4: Request just keeps loading/spinning
**Solution:**
- Make sure you're using the correct URL: `http://localhost:8000` (not `https`)
- Try `http://127.0.0.1:8000` instead
- Check if another application is using port 8000

---

## 📊 Understanding the Response

The API returns a JSON object with the predicted car price:

```json
{
    "predicted_price": 11118.31
}
```

This means the model predicts the car's price to be **$11,118.31**.

---

## 🎯 Field Reference

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| Levy | string | "1399" or "-" | Tax levy amount |
| Manufacturer | string | "LEXUS" | Car manufacturer |
| Model | string | "RX 450" | Car model |
| Prod_year | integer | 2010 | Production year |
| Category | string | "Jeep" | Car category |
| Leather_interior | string | "Yes" or "No" | Has leather interior |
| Fuel_type | string | "Hybrid" | Type of fuel |
| Engine_volume | float | 3.5 | Engine size in liters |
| Mileage | float | 186005 | Total kilometers |
| Cylinders | float | 6.0 | Number of cylinders |
| Gear_box_type | string | "Automatic" | Transmission type |
| Drive_wheels | string | "4x4" | Drive system |
| Wheel | string | "Left wheel" | Steering position |
| Color | string | "Silver" | Car color |
| Airbags | float | 12 | Number of airbags |
| Age | integer | 15 | Car age in years |
| Mileage_per_year | float (optional) | 12400 | Avg km per year |

---

## 🌐 Alternative: Use Swagger UI

Instead of Postman, you can also test the API using the built-in Swagger UI:

1. Start the server
2. Open your browser and go to: `http://localhost:8000/docs`
3. Click on the endpoint you want to test
4. Click "Try it out"
5. Fill in the parameters or paste JSON
6. Click "Execute"

---

## ✅ What to Expect

✓ **GET /**: Should respond instantly (< 100ms)  
✓ **POST /predict**: Should respond in 100-500ms  
✓ **Status Code**: 200 OK for successful requests  
✓ **No hanging**: Requests should complete quickly  
✓ **No internal errors**: Model is properly loaded and tested  

---

**🎉 Your API is fully functional and ready to use!**
