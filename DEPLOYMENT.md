# 🚀 Deployment Guide

Complete guide for deploying the Car Price Predictor to Azure with CI/CD.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Azure Setup](#azure-setup)
4. [GitHub Actions CI/CD](#github-actions-cicd)
5. [Manual Deployment](#manual-deployment)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## Prerequisites

### Required Tools

- **Azure CLI** ([Install](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
- **Docker** ([Install](https://docs.docker.com/get-docker/))
- **Docker Compose** (usually included with Docker)
- **Git**
- **Node.js 18+** (for frontend development)
- **Python 3.11+** (for backend development)

### Azure Requirements

- Active Azure subscription
- Appropriate permissions to create resources
- Azure Container Registry (will be created by setup script)

---

## 🏠 Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/Kanyira/Car-price-prediction-models.git
cd Car-price-prediction-models
```

### 2. Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

**Access the application:**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 3. Stop Services

```bash
docker-compose down
```

### 4. Development Mode (without Docker)

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

---

## ☁️ Azure Setup

### Step 1: Run the Setup Script

The automated setup script will create all required Azure resources:

```bash
cd azure
./setup-azure.sh
```

This script will:
- ✅ Create a resource group
- ✅ Create an Azure Container Registry (ACR)
- ✅ Enable admin access on ACR
- ✅ Create a service principal for GitHub Actions
- ✅ Output credentials for GitHub secrets

### Step 2: Configure GitHub Secrets

After running the setup script, add these secrets to your GitHub repository:

**Go to:** `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

Add the following secrets:

| Secret Name | Description | How to get |
|-------------|-------------|------------|
| `AZURE_CREDENTIALS` | Service principal JSON | Output from setup script |
| `AZURE_CONTAINER_REGISTRY` | ACR login server | Output from setup script |
| `ACR_USERNAME` | ACR username | Output from setup script |
| `ACR_PASSWORD` | ACR password | Output from setup script |

### Step 3: Update Configuration

Edit `azure/parameters.json` with your ACR name:

```json
{
  "containerRegistry": {
    "value": "YOUR_ACR_NAME.azurecr.io"
  },
  "backendImage": {
    "value": "YOUR_ACR_NAME.azurecr.io/car-price-backend:latest"
  },
  "frontendImage": {
    "value": "YOUR_ACR_NAME.azurecr.io/car-price-frontend:latest"
  }
}
```

---

## 🔄 GitHub Actions CI/CD

The CI/CD pipeline automatically runs on:
- Push to `main` or `master` branch
- Pull requests
- Manual trigger (workflow_dispatch)

### Pipeline Stages

#### 1. Build and Test (`build-and-test`)

- Checks out code
- Sets up Python and Node.js
- Installs dependencies
- Runs backend tests
- Builds frontend
- Uploads artifacts

#### 2. Build Docker Images (`build-docker-images`)

- Logs in to Azure Container Registry
- Builds backend Docker image
- Builds frontend Docker image
- Pushes images with `latest` and commit SHA tags
- Uses layer caching for faster builds

#### 3. Deploy to Azure (`deploy-to-azure`)

- Logs in to Azure
- Creates/updates resource group
- Deploys using Bicep template
- Creates Azure Container Apps for backend and frontend
- Outputs deployment URLs
- Posts comment on PR with URLs

### Manual Trigger

You can manually trigger deployment:

1. Go to `Actions` tab in GitHub
2. Select "Build and Deploy to Azure"
3. Click "Run workflow"
4. Select branch and run

### Monitoring Deployments

- Check the `Actions` tab for pipeline status
- View logs for each step
- See deployment summary with URLs

---

## 🛠️ Manual Deployment

If you prefer manual deployment or need to troubleshoot:

### Build and Push Docker Images

```bash
# Set variables
ACR_NAME="your-acr-name"
RESOURCE_GROUP="car-price-rg"

# Login to ACR
az acr login --name $ACR_NAME

# Build and push backend
docker build -t $ACR_NAME.azurecr.io/car-price-backend:latest .
docker push $ACR_NAME.azurecr.io/car-price-backend:latest

# Build and push frontend
docker build -t $ACR_NAME.azurecr.io/car-price-frontend:latest ./frontend
docker push $ACR_NAME.azurecr.io/car-price-frontend:latest
```

### Deploy to Azure

```bash
# Login to Azure
az login

# Deploy using Bicep
az deployment group create \
  --resource-group $RESOURCE_GROUP \
  --template-file azure/container-app.bicep \
  --parameters @azure/parameters.json
```

### Get Deployment URLs

```bash
# Get backend URL
az containerapp show \
  --name car-price-backend \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  -o tsv

# Get frontend URL
az containerapp show \
  --name car-price-frontend \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  -o tsv
```

---

## 📊 Monitoring and Maintenance

### View Logs

**Using Azure Portal:**
1. Go to Azure Portal
2. Navigate to your Container App
3. Select "Log stream" or "Logs"

**Using Azure CLI:**
```bash
# View backend logs
az containerapp logs show \
  --name car-price-backend \
  --resource-group car-price-rg \
  --follow

# View frontend logs
az containerapp logs show \
  --name car-price-frontend \
  --resource-group car-price-rg \
  --follow
```

### Health Checks

Both containers include health checks:

**Backend:**
- Liveness: `GET /` every 30s
- Readiness: `GET /` every 10s

**Frontend:**
- Liveness: HTTP check on port 80 every 30s

### Scaling

Container Apps auto-scale based on:
- Backend: Up to 5 replicas based on HTTP concurrency (50 requests)
- Frontend: Up to 3 replicas

**Manual scaling:**
```bash
az containerapp update \
  --name car-price-backend \
  --resource-group car-price-rg \
  --min-replicas 2 \
  --max-replicas 10
```

### Update Deployment

To update with new code:

1. **Automatic (Recommended):**
   - Push to main branch
   - GitHub Actions will automatically build and deploy

2. **Manual:**
   - Build and push new Docker images
   - Update container apps to use new images

### Rollback

To rollback to a previous version:

```bash
# List revisions
az containerapp revision list \
  --name car-price-backend \
  --resource-group car-price-rg \
  -o table

# Activate a specific revision
az containerapp revision activate \
  --revision <revision-name> \
  --resource-group car-price-rg
```

### Cost Management

**Current configuration:**
- Backend: 0.5 CPU, 1GB RAM
- Frontend: 0.25 CPU, 0.5GB RAM
- ACR: Basic tier
- Log Analytics: Pay-per-GB

**Estimated monthly cost:** ~$30-50 (varies by region and usage)

**To reduce costs:**
- Use spot instances if available
- Reduce minimum replicas to 0 (cold starts may occur)
- Use smaller resource allocations
- Delete when not in use

### Cleanup

To delete all resources:

```bash
# Delete entire resource group (CAUTION: This deletes everything)
az group delete --name car-price-rg --yes --no-wait

# Or delete specific resources
az containerapp delete --name car-price-backend --resource-group car-price-rg
az containerapp delete --name car-price-frontend --resource-group car-price-rg
az acr delete --name <acr-name> --resource-group car-price-rg
```

---

## 🔒 Security Best Practices

1. **Secrets Management:**
   - Never commit secrets to Git
   - Use GitHub Secrets for CI/CD
   - Use Azure Key Vault for production secrets

2. **Container Security:**
   - Images are scanned in ACR
   - Use specific image tags, not just `latest`
   - Regularly update base images

3. **Network Security:**
   - HTTPS is enforced on all ingress
   - Backend is only accessible via frontend proxy
   - Consider adding authentication

4. **Access Control:**
   - Use RBAC for Azure resources
   - Limit service principal permissions
   - Regularly rotate credentials

---

## 🐛 Troubleshooting

### Build Failures

**Issue:** Docker build fails
```bash
# Check build logs
docker-compose build --no-cache

# Test individual services
docker build -t test-backend .
docker build -t test-frontend ./frontend
```

### Deployment Failures

**Issue:** Azure deployment fails
```bash
# Check deployment logs
az deployment group show \
  --name container-app \
  --resource-group car-price-rg

# Validate Bicep template
az bicep build --file azure/container-app.bicep
```

### Container Not Starting

**Issue:** Container app not healthy
```bash
# Check logs
az containerapp logs show --name car-price-backend --resource-group car-price-rg

# Check revision status
az containerapp revision list --name car-price-backend --resource-group car-price-rg -o table
```

### Connection Issues

**Issue:** Frontend can't reach backend
- Check REACT_APP_API_URL environment variable
- Verify backend URL in Azure Portal
- Check CORS settings in backend

---

## 📚 Additional Resources

- [Azure Container Apps Documentation](https://docs.microsoft.com/en-us/azure/container-apps/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

---

## 🆘 Getting Help

- **Issues:** Open an issue on GitHub
- **Azure Support:** [Azure Support Portal](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade)
- **Documentation:** Check TROUBLESHOOTING.md

---

**Last Updated:** 2025-10-19
**Version:** 1.0.0
