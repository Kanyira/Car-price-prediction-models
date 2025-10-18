# 🔧 Troubleshooting Guide

## The Error You Encountered

```
"columns are missing: {'Engine volume', 'Drive wheels', 'Gear box type', 'Leather interior', 'Prod. year', 'Fuel type'}"
```

This error means the DataFrame being sent to the model doesn't have the correct column names with spaces.

---

## ✅ **FIXED!** Here's What I Changed:

### 1. **Improved the mapping function** (lines 77-99 in main.py)
- Added better None value handling
- Improved Levy field parsing (handles "-" values)
- Made the logic more robust

### 2. **Added extensive debugging** (lines 101-168 in main.py)
- Prints received data
- Prints mapped data
- Prints DataFrame columns
- Checks for missing columns BEFORE calling the model
- Better error messages

### 3. **Better error handling**
- Now shows exactly which columns are missing
- Shows available columns for comparison

---

## 🧪 How to Verify It Works

### Option 1: Run the test script
```bash
python3 test_api.py
```

You should see:
```
✅ ALL TESTS PASSED!
```

### Option 2: Test in Postman

**Start the server:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**In Postman, use this exact JSON:**
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

**Expected Response:**
```json
{
    "predicted_price": 11118.31
}
```

---

## 🔍 Debugging Output

When you make a request, you'll see detailed output in the server terminal:

```
Received data: {'Levy': '1399', 'Manufacturer': 'LEXUS', ...}
Mapped data: {'Levy': 1399.0, 'Prod. year': 2010, ...}
DataFrame columns: ['Levy', 'Manufacturer', 'Model', 'Prod. year', ...]
DataFrame shape: (1, 17)
✓ All required columns present
Processed DataFrame columns: [...]
```

If something is wrong, you'll see:
```
ERROR: Missing columns: {'Engine volume', ...}
Available columns: ['Levy', 'Manufacturer', ...]
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: Wrong field names in JSON
**Symptom:** "Unprocessable Entity" (422) error

**Solution:** Make sure field names match EXACTLY:
- ✅ `Prod_year` (with underscore)
- ❌ `Prod year` (no underscore)
- ✅ `Leather_interior` 
- ❌ `Leather interior` (no underscore in JSON)

**Note:** Field names in JSON use underscores, but they get converted to spaces internally.

### Issue 2: Wrong data types
**Symptom:** Validation error or 422 error

**Solution:** Check data types:
- `Levy`: **string** (e.g., `"1399"` not `1399`)
- `Prod_year`: **integer** (e.g., `2010` not `"2010"`)
- `Engine_volume`: **float** (e.g., `3.5`)
- `Cylinders`: **float** (e.g., `6.0` or `6`)
- `Airbags`: **float** (e.g., `12` or `12.0`)
- `Leather_interior`: **string** (`"Yes"` or `"No"`)

### Issue 3: Missing required fields
**Symptom:** 422 Unprocessable Entity

**Solution:** All fields are required EXCEPT `Mileage_per_year` which is optional.

Make sure you include all these fields:
- Levy
- Manufacturer
- Model
- Prod_year
- Category
- Leather_interior
- Fuel_type
- Engine_volume
- Mileage
- Cylinders
- Gear_box_type
- Drive_wheels
- Wheel
- Color
- Airbags
- Age

### Issue 4: Server not starting
**Symptom:** "Connection refused" in Postman

**Solution:**
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or use the script:
./run_server.sh
```

---

## 📋 Field Reference - Quick Copy

### JSON Template (Copy this for testing):
```json
{
  "Levy": "STRING_HERE",
  "Manufacturer": "STRING_HERE",
  "Model": "STRING_HERE",
  "Prod_year": 2020,
  "Category": "STRING_HERE",
  "Leather_interior": "Yes",
  "Fuel_type": "STRING_HERE",
  "Engine_volume": 2.5,
  "Mileage": 100000,
  "Cylinders": 4.0,
  "Gear_box_type": "STRING_HERE",
  "Drive_wheels": "STRING_HERE",
  "Wheel": "Left wheel",
  "Color": "STRING_HERE",
  "Airbags": 8,
  "Age": 5
}
```

### Common Values:

**Manufacturers:** LEXUS, TOYOTA, MERCEDES-BENZ, BMW, HYUNDAI, KIA, HONDA, FORD, CHEVROLET, etc.

**Categories:** Sedan, Jeep, Hatchback, SUV, Coupe, Minivan, Pickup, etc.

**Fuel_type:** Petrol, Diesel, Hybrid, Electric, CNG, LPG

**Gear_box_type:** Automatic, Manual, Tiptronic, Variator

**Drive_wheels:** Front, Rear, 4x4

**Wheel:** "Left wheel" or "Right-hand drive"

**Leather_interior:** "Yes" or "No"

---

## 🔬 Advanced Debugging

If you still get errors, check the server logs:

1. Look at the terminal where `uvicorn` is running
2. You'll see detailed output showing:
   - What data was received
   - How it was mapped
   - What columns were created
   - Any errors that occurred

3. Copy the error and check:
   - Is the DataFrame being created with the right column names?
   - Are all 17 columns present?
   - Are the data types correct?

---

## 🆘 Still Having Issues?

1. Make sure you have the latest version from GitHub:
   ```bash
   git pull origin cursor/read-repository-files-cd38
   ```

2. Verify your `main.py` has the updated code (check the file date/time)

3. Run the test script:
   ```bash
   python3 test_api.py
   ```

4. If tests pass but Postman fails, check:
   - Are you using the correct URL? `http://localhost:8000/predict`
   - Is the Content-Type header set? `application/json`
   - Is your JSON valid? Use a JSON validator

---

## ✅ Expected Behavior

When everything works correctly:

1. **Server starts without errors**
2. **GET /** returns `{"message": "Car Price API running successfully"}`
3. **POST /predict** returns a prediction in ~100-500ms
4. **No "columns are missing" errors**
5. **Server logs show all debugging information**

---

**The fix is already in `main.py` - just pull the latest version and test!** 🎉
