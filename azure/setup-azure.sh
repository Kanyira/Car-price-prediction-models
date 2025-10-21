#!/bin/bash
# Azure setup script - Run this once to set up your Azure environment

set -e

echo "🚀 Setting up Azure environment for Car Price Predictor"
echo ""

# Variables - Update these with your values
RESOURCE_GROUP="car-price-rg"
LOCATION="eastus"
ACR_NAME="carpricecr$(date +%s)"  # Must be globally unique
SUBSCRIPTION_ID=""  # Get this from 'az account show'

echo "📋 Configuration:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  Container Registry: $ACR_NAME"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first:"
    echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Login to Azure
echo "🔐 Logging in to Azure..."
az login

# Set subscription if provided
if [ -n "$SUBSCRIPTION_ID" ]; then
    az account set --subscription "$SUBSCRIPTION_ID"
fi

# Create resource group
echo "📦 Creating resource group..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

# Create Azure Container Registry
echo "🐳 Creating Azure Container Registry..."
az acr create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$ACR_NAME" \
    --sku Basic \
    --admin-enabled true

# Get ACR credentials
echo "🔑 Getting ACR credentials..."
ACR_USERNAME=$(az acr credential show --name "$ACR_NAME" --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --query passwords[0].value -o tsv)
ACR_LOGIN_SERVER=$(az acr show --name "$ACR_NAME" --query loginServer -o tsv)

# Create service principal for GitHub Actions
echo "👤 Creating service principal for GitHub Actions..."
SP_NAME="car-price-sp-$(date +%s)"
SP_OUTPUT=$(az ad sp create-for-rbac \
    --name "$SP_NAME" \
    --role contributor \
    --scopes "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP" \
    --sdk-auth)

echo ""
echo "✅ Setup complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 GitHub Secrets - Add these to your repository:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "AZURE_CREDENTIALS:"
echo "$SP_OUTPUT"
echo ""
echo "AZURE_CONTAINER_REGISTRY:"
echo "$ACR_LOGIN_SERVER"
echo ""
echo "ACR_USERNAME:"
echo "$ACR_USERNAME"
echo ""
echo "ACR_PASSWORD:"
echo "$ACR_PASSWORD"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Next steps:"
echo "1. Go to your GitHub repository"
echo "2. Navigate to Settings → Secrets and variables → Actions"
echo "3. Add the secrets shown above"
echo "4. Update azure/parameters.json with your ACR name"
echo "5. Push to trigger the CI/CD pipeline"
echo ""
echo "🌐 Useful commands:"
echo "  View resources: az resource list -g $RESOURCE_GROUP -o table"
echo "  Delete everything: az group delete -n $RESOURCE_GROUP --yes"
echo ""
