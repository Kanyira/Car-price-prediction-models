# 📬 Complete Postman Testing Instructions

## ✅ **API Status: FIXED AND TESTED**

The "missing columns" error has been **FIXED**. All tests pass! ✅

---

## 🚀 Quick Start (3 Steps)

### **Step 1: Start the Server**

Open a terminal in the project directory and run:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Wait for this message:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

---

### **Step 2: Test GET Endpoint (Health Check)**

**In Postman:**

1. Click **"New"** → **"HTTP Request"**
2. Set method to: **GET**
3. Set URL to: `http://localhost:8000/`
4. Click **"Send"**

**✅ Expected Response (200 OK):**
```json
{
    "message": "Car Price API running successfully"
}
```

---

### **Step 3: Test POST Endpoint (Predict Price)**

**In Postman:**

1. Create a **new request**
2. Set method to: **POST**
3. Set URL to: `http://localhost:8000/predict`
4. Go to **"Headers"** tab:
   - Click **"Add header"**
   - Key: `Content-Type`
   - Value: `application/json`
5. Go to **"Body"** tab:
   - Select **"raw"**
   - Select **"JSON"** from the dropdown (right side)
6. **Copy and paste this EXACT JSON:**

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

7. Click **"Send"**

**✅ Expected Response (200 OK):**
```json
{
    "predicted_price": 11118.31
}
```

**Response time:** Should be ~100-500ms

---

## 🧪 Additional Test Cases

### Test Case 2: Toyota Camry
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

### Test Case 4: Levy with "-" (No levy)
```json
{
  "Levy": "-",
  "Manufacturer": "FORD",
  "Model": "Focus",
  "Prod_year": 2015,
  "Category": "Sedan",
  "Leather_interior": "No",
  "Fuel_type": "Petrol",
  "Engine_volume": 1.6,
  "Mileage": 150000,
  "Cylinders": 4.0,
  "Gear_box_type": "Manual",
  "Drive_wheels": "Front",
  "Wheel": "Left wheel",
  "Color": "White",
  "Airbags": 4,
  "Age": 10
}
```

---

## 🎯 Important Field Requirements

### Data Types (CRITICAL!)

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| **Levy** | STRING | `"1399"` or `"-"` | Use quotes! |
| **Manufacturer** | STRING | `"LEXUS"` | |
| **Model** | STRING | `"RX 450"` | |
| **Prod_year** | INTEGER | `2010` | No quotes! |
| **Category** | STRING | `"Jeep"` | |
| **Leather_interior** | STRING | `"Yes"` or `"No"` | Exactly these values |
| **Fuel_type** | STRING | `"Hybrid"` | |
| **Engine_volume** | FLOAT | `3.5` | No quotes! |
| **Mileage** | FLOAT | `186005` | No quotes! |
| **Cylinders** | FLOAT | `6.0` or `6` | No quotes! |
| **Gear_box_type** | STRING | `"Automatic"` | |
| **Drive_wheels** | STRING | `"4x4"` | |
| **Wheel** | STRING | `"Left wheel"` | |
| **Color** | STRING | `"Silver"` | |
| **Airbags** | FLOAT | `12` or `12.0` | No quotes! |
| **Age** | INTEGER | `15` | No quotes! |
| **Mileage_per_year** | FLOAT (Optional) | `12400` | Auto-calculated if omitted |

### ⚠️ Common Mistakes

❌ **WRONG:**
```json
{
  "Levy": 1399,          // Should be string
  "Prod_year": "2010",   // Should be integer
  "leather_interior": "Yes", // Wrong case
  "Prod year": 2010      // Should use underscore
}
```

✅ **CORRECT:**
```json
{
  "Levy": "1399",        // String with quotes
  "Prod_year": 2010,     // Integer without quotes
  "Leather_interior": "Yes", // Correct case
  "Prod_year": 2010      // Underscore, not space
}
```

---

## 📊 What the Server Shows

When you make a request, the server terminal will show:

```
Received data: {'Levy': '1399', 'Manufacturer': 'LEXUS', ...}
Mapped data: {'Levy': 1399.0, 'Prod. year': 2010, 'Leather interior': 1, ...}
DataFrame columns: ['Levy', 'Manufacturer', 'Model', 'Prod. year', ...]
DataFrame shape: (1, 17)
Processed DataFrame columns: [...]
Processed DataFrame dtypes: {...}
```

This shows the data is being processed correctly!

---

## ❌ Error Reference

### Error 422: Unprocessable Entity
**Cause:** Invalid JSON structure or data types

**Fix:**
- Check all field names are spelled correctly
- Check data types match the requirements above
- Make sure JSON is valid (use a JSON validator)

### Error 500: Internal Server Error
**Cause:** Server-side processing error

**Fix:**
- Check the server terminal for detailed error messages
- Make sure all required fields are present
- Verify field names match exactly (case-sensitive!)

### Connection Refused / Cannot Connect
**Cause:** Server is not running

**Fix:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🌐 Alternative: Swagger UI

Instead of Postman, you can use the built-in Swagger UI:

1. Start the server
2. Open browser: `http://localhost:8000/docs`
3. Click on `/predict` endpoint
4. Click **"Try it out"**
5. Paste JSON in the request body
6. Click **"Execute"**

---

## ✅ Success Indicators

**Everything is working if:**
- ✅ Server starts without errors
- ✅ GET / returns success message
- ✅ POST /predict returns predicted_price
- ✅ Response time is 100-500ms
- ✅ No error messages in server logs
- ✅ Status code is 200 OK

---

## 🔧 Need Help?

See **TROUBLESHOOTING.md** for detailed debugging steps.

---

**Your API is fully functional and tested! 🎉**
