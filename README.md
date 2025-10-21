# 🚗 Car Price Prediction Platform

A full-stack machine learning application for predicting car prices with a React frontend, FastAPI backend, Docker containerization, and Azure deployment.

## ✨ Features

- 🎨 **Modern React UI** - Beautiful, responsive interface for car price predictions
- 🚀 **FastAPI Backend** - High-performance REST API powered by XGBoost ML model
- 🐳 **Docker Ready** - Fully containerized with Docker Compose
- ☁️ **Azure Deployment** - Production-ready deployment to Azure Container Apps
- 🔄 **CI/CD Pipeline** - Automated testing and deployment with GitHub Actions
- 📊 **Real-time Predictions** - Instant price predictions based on 17+ car features

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

Run the entire stack with one command:

```bash
docker-compose up --build
```

**Access:**
- 🌐 Frontend: http://localhost
- 🔌 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

### Option 2: Development Mode

**Backend:**
```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

> 📖 **New to the project?** Check out [QUICKSTART.md](QUICKSTART.md) for a detailed guide!

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

### Backend
- **FastAPI** - Modern Python web framework
- **XGBoost** - Machine learning model (19,238 training samples)
- **Pandas** - Data processing
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI framework
- **Axios** - HTTP client
- **CSS3** - Modern styling with animations
- **Nginx** - Production web server

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Bitbucket Pipelines** - CI/CD automation
- **Azure Container Apps** - Cloud hosting
- **Azure Container Registry** - Docker image registry

## 📁 Project Structure

```
car-price-prediction-models/
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── App.js           # Main app component
│   │   └── index.js         # Entry point
│   ├── Dockerfile           # Frontend container config
│   └── nginx.conf           # Nginx configuration
├── azure/                    # Azure deployment configs
│   ├── container-app.bicep  # Infrastructure as Code
│   ├── parameters.json      # Deployment parameters
│   └── setup-azure.sh       # Setup script
├── bitbucket-pipelines.yml   # CI/CD pipeline configuration
├── azure/                    # Azure deployment configs
│   ├── setup-azure-bitbucket.sh  # Bitbucket setup script
├── main.py                   # FastAPI backend
├── xgb_car_price_pipeline.pkl  # Trained ML model
├── Dockerfile                # Backend container config
├── docker-compose.yml        # Local development setup
├── DEPLOYMENT.md             # Deployment guide
└── DOCKER.md                 # Docker guide
```

## 🚀 Deployment

### Deploy to Azure with Bitbucket Pipelines

1. **Setup Azure resources:**
   ```bash
   cd azure
   ./setup-azure-bitbucket.sh
   ```

2. **Configure Bitbucket Repository Variables:**
   - Go to Repository Settings → Pipelines → Repository variables
   - Add all 7 variables from setup script output
   - Mark sensitive values as "Secured"

3. **Enable Pipelines and Push:**
   ```bash
   git add bitbucket-pipelines.yml
   git commit -m "Add CI/CD pipeline"
   git push origin main
   ```

The pipeline will automatically build, test, and deploy to Azure!

For detailed setup, see [BITBUCKET_SETUP.md](BITBUCKET_SETUP.md) or [BITBUCKET_QUICKSTART.md](BITBUCKET_QUICKSTART.md)

### Local Docker Deployment

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

For detailed Docker instructions, see [DOCKER.md](DOCKER.md)

## 📖 Documentation

- **[BITBUCKET_QUICKSTART.md](BITBUCKET_QUICKSTART.md)** - ⚡ Quick 10-minute setup
- **[BITBUCKET_SETUP.md](BITBUCKET_SETUP.md)** - Complete Bitbucket Pipelines guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Detailed deployment guide for Azure
- **[DOCKER.md](DOCKER.md)** - Docker and containerization guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[POSTMAN_INSTRUCTIONS.md](POSTMAN_INSTRUCTIONS.md)** - API testing guide

## 🔄 CI/CD Pipeline

The project includes automated Bitbucket Pipelines:

### Main Pipeline (main/master branches)
- ✅ Build and test backend (parallel)
- ✅ Build and test frontend (parallel)
- ✅ Build Docker images (parallel)
- ✅ Push to Azure Container Registry
- ✅ Deploy to Azure Container Apps
- ✅ Output deployment URLs

### PR Validation (pull requests)
- ✅ Lint Python and JavaScript code
- ✅ Run automated tests
- ✅ Verify Docker builds
- ❌ No deployment (validation only)

### Custom Pipelines
- `deploy-production`: Manual deployment trigger
- `build-only`: Build without deploying

## 🌐 Live Demo

After pipeline deployment, check the logs for URLs:
- **Frontend URL**: `https://car-price-frontend-xxx.azurecontainerapps.io`
- **Backend API**: `https://car-price-backend-xxx.azurecontainerapps.io`
- **Swagger Docs**: `https://car-price-backend-xxx.azurecontainerapps.io/docs`
