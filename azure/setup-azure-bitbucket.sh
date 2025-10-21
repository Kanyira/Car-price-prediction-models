#!/bin/bash
# Azure setup script for Bitbucket Pipelines - Run this once to set up your Azure environment

set -e

echo "🚀 Setting up Azure environment for Car Price Predictor (Bitbucket)"
echo ""

# Variables - Update these with your values
RESOURCE_GROUP="car-price-rg"
LOCATION="eastus"
ACR_NAME="carpricecr$(date +%s)"  # Must be globally unique
SUBSCRIPTION_ID=""  # Get this from 'az account show'
SP_NAME="car-price-sp-$(date +%s)"

echo "📋 Configuration:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  Container Registry: $ACR_NAME"
echo "  Service Principal: $SP_NAME"
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
else
    SUBSCRIPTION_ID=$(az account show --query id -o tsv)
fi

echo "✅ Using subscription: $SUBSCRIPTION_ID"

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

# Create service principal for Bitbucket Pipelines
echo "👤 Creating service principal for Bitbucket Pipelines..."
SP_OUTPUT=$(az ad sp create-for-rbac \
    --name "$SP_NAME" \
    --role contributor \
    --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP")

# Extract service principal details
AZURE_CLIENT_ID=$(echo $SP_OUTPUT | jq -r '.appId')
AZURE_CLIENT_SECRET=$(echo $SP_OUTPUT | jq -r '.password')
AZURE_TENANT_ID=$(echo $SP_OUTPUT | jq -r '.tenant')

echo ""
echo "✅ Setup complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 Bitbucket Repository Variables - Add these to your repo:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Go to: Repository Settings → Pipelines → Repository variables"
echo ""
echo "Add these variables (mark sensitive ones as 'Secured'):"
echo ""
echo "Name: AZURE_CONTAINER_REGISTRY"
echo "Value: $ACR_LOGIN_SERVER"
echo "Secured: No"
echo ""
echo "Name: ACR_USERNAME"
echo "Value: $ACR_USERNAME"
echo "Secured: No"
echo ""
echo "Name: ACR_PASSWORD"
echo "Value: $ACR_PASSWORD"
echo "Secured: ✅ Yes"
echo ""
echo "Name: AZURE_SUBSCRIPTION_ID"
echo "Value: $SUBSCRIPTION_ID"
echo "Secured: No"
echo ""
echo "Name: AZURE_CLIENT_ID"
echo "Value: $AZURE_CLIENT_ID"
echo "Secured: No"
echo ""
echo "Name: AZURE_CLIENT_SECRET"
echo "Value: $AZURE_CLIENT_SECRET"
echo "Secured: ✅ Yes"
echo ""
echo "Name: AZURE_TENANT_ID"
echo "Value: $AZURE_TENANT_ID"
echo "Secured: No"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Next steps:"
echo "1. Go to your Bitbucket repository"
echo "2. Navigate to Repository Settings → Pipelines → Settings"
echo "3. Enable Pipelines"
echo "4. Go to Repository variables"
echo "5. Add all the variables shown above"
echo "6. Update azure/parameters.json with your ACR name"
echo "7. Push to trigger the pipeline"
echo ""
echo "🌐 Useful commands:"
echo "  View resources: az resource list -g $RESOURCE_GROUP -o table"
echo "  Delete everything: az group delete -n $RESOURCE_GROUP --yes"
echo ""
echo "💾 Save this information securely! You'll need it for Bitbucket configuration."
echo ""

# Save to file for reference
cat > azure-config.txt << EOF
Azure Configuration for Bitbucket Pipelines
==========================================

AZURE_CONTAINER_REGISTRY=$ACR_LOGIN_SERVER
ACR_USERNAME=$ACR_USERNAME
ACR_PASSWORD=$ACR_PASSWORD
AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID
AZURE_CLIENT_ID=$AZURE_CLIENT_ID
AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET
AZURE_TENANT_ID=$AZURE_TENANT_ID

Resource Group: $RESOURCE_GROUP
Location: $LOCATION
ACR Name: $ACR_NAME
Service Principal: $SP_NAME

⚠️  IMPORTANT: Keep this file secure and do not commit it to version control!
EOF

echo "💾 Configuration saved to: azure-config.txt"
echo "⚠️  IMPORTANT: Keep azure-config.txt secure and do not commit it to Git!"
echo ""
