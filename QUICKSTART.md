# ⚡ Quick Start Guide

Get up and running with the Car Price Predictor in under 5 minutes!

## 🎯 Choose Your Path

### 1️⃣ Just Want to Try It? (Docker - Easiest)

```bash
# Clone the repository
git clone https://github.com/Kanyira/Car-price-prediction-models.git
cd Car-price-prediction-models

# Start everything
docker-compose up --build
```

**That's it!** 🎉
- Frontend: http://localhost
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### 2️⃣ Want to Develop? (Development Mode)

**Terminal 1 - Backend:**
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

### 3️⃣ Want to Deploy to Azure? (Production)

**Step 1: Setup Azure**
```bash
cd azure
./setup-azure.sh
```

**Step 2: Add GitHub Secrets**

Go to GitHub → Settings → Secrets and add:
- `AZURE_CREDENTIALS` (from setup script)
- `AZURE_CONTAINER_REGISTRY` (from setup script)
- `ACR_USERNAME` (from setup script)
- `ACR_PASSWORD` (from setup script)

**Step 3: Deploy**
```bash
git push origin main
```

GitHub Actions will automatically deploy! 🚀

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 🧪 Test the API

### Using the Frontend

1. Open http://localhost (or your deployed URL)
2. Fill in the car details
3. Click "Predict Price"
4. Get instant prediction! 💰

### Using cURL

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### Using Postman

1. Import `sample_request.json`
2. POST to `http://localhost:8000/predict`
3. Send!

See [POSTMAN_INSTRUCTIONS.md](POSTMAN_INSTRUCTIONS.md) for details.

---

## 📦 What's Included?

### Frontend Features
- ✅ Beautiful, responsive UI
- ✅ Form validation
- ✅ Real-time predictions
- ✅ Error handling
- ✅ Loading states
- ✅ Mobile-friendly

### Backend Features
- ✅ FastAPI REST API
- ✅ XGBoost ML model
- ✅ Auto-documentation (Swagger)
- ✅ CORS enabled
- ✅ Health checks
- ✅ Detailed logging

### DevOps Features
- ✅ Docker containerization
- ✅ Docker Compose orchestration
- ✅ CI/CD with GitHub Actions
- ✅ Azure deployment configs
- ✅ Automated testing

---

## 🔧 Common Commands

### Docker

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up --build
```

### Development

```bash
# Backend
uvicorn main:app --reload

# Frontend
cd frontend && npm start

# Run tests
python test_api.py
```

### Deployment

```bash
# Deploy to Azure (automatic via push)
git push origin main

# Manual deployment
cd azure
az deployment group create --resource-group car-price-rg --template-file container-app.bicep
```

---

## 🆘 Having Issues?

### Docker won't start?
```bash
# Make sure Docker is running
docker ps

# Check if ports are available
lsof -i :80
lsof -i :8000
```

### Backend errors?
```bash
# Check Python version (needs 3.11+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check model file exists
ls -lh xgb_car_price_pipeline.pkl
```

### Frontend errors?
```bash
# Check Node version (needs 18+)
node --version

# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Still stuck?
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Check [DEPLOYMENT.md](DEPLOYMENT.md)
- Check [DOCKER.md](DOCKER.md)
- Open an issue on GitHub

---

## 📚 Next Steps

1. **Explore the API**: http://localhost:8000/docs
2. **Customize the frontend**: Edit `frontend/src/components/`
3. **Improve the model**: Check `Car price prediction.ipynb`
4. **Deploy to production**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)
5. **Set up monitoring**: Add Azure Application Insights

---

## 🎓 Learn More

- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **Docker**: https://docs.docker.com/
- **Azure Container Apps**: https://learn.microsoft.com/azure/container-apps/

---

## 🎉 You're Ready!

Choose your path above and start building! 

Need help? Check the docs or open an issue.

Happy coding! 🚀
