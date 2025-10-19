# 🚀 Bitbucket Pipelines Setup Guide

Complete guide for setting up automated CI/CD with Bitbucket Pipelines and Azure deployment.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Azure Setup](#azure-setup)
3. [Bitbucket Configuration](#bitbucket-configuration)
4. [Pipeline Overview](#pipeline-overview)
5. [Testing and Deployment](#testing-and-deployment)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools (Local)

- **Azure CLI** ([Install](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
- **Docker** (for local testing)
- **Git**

### Bitbucket Requirements

- Bitbucket repository
- Bitbucket Pipelines enabled
- Appropriate permissions to add repository variables

### Azure Requirements

- Active Azure subscription
- Permissions to create resources
- Azure Container Registry (will be created by setup script)

---

## ☁️ Azure Setup

### Step 1: Run the Setup Script

The automated setup script will create all required Azure resources and generate the credentials for Bitbucket:

```bash
cd azure
./setup-azure-bitbucket.sh
```

This script will:
- ✅ Create a resource group (`car-price-rg`)
- ✅ Create an Azure Container Registry (ACR)
- ✅ Enable admin access on ACR
- ✅ Create a service principal for Bitbucket Pipelines
- ✅ Output all necessary credentials
- ✅ Save configuration to `azure-config.txt`

**⚠️ IMPORTANT**: Save the output! You'll need these values for Bitbucket configuration.

### Step 2: Note Your Credentials

After the script completes, you'll see output like this:

```
AZURE_CONTAINER_REGISTRY=carpricecr123456.azurecr.io
ACR_USERNAME=carpricecr123456
ACR_PASSWORD=xxxxxxxxxxxxx
AZURE_SUBSCRIPTION_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_SECRET=xxxxxxxxxxxxx
AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Keep these values handy for the next step!

---

## 🔧 Bitbucket Configuration

### Step 1: Enable Bitbucket Pipelines

1. Go to your Bitbucket repository
2. Click **Repository Settings** (gear icon)
3. Under **Pipelines**, click **Settings**
4. Toggle **Enable Pipelines** to ON

### Step 2: Add Repository Variables

Go to **Repository Settings** → **Pipelines** → **Repository variables**

Add the following variables:

| Variable Name | Value | Secured? | Description |
|---------------|-------|----------|-------------|
| `AZURE_CONTAINER_REGISTRY` | `yourregistry.azurecr.io` | ❌ No | ACR login server |
| `ACR_USERNAME` | `yourregistry` | ❌ No | ACR username |
| `ACR_PASSWORD` | `your-password` | ✅ **Yes** | ACR password |
| `AZURE_SUBSCRIPTION_ID` | `your-sub-id` | ❌ No | Azure subscription ID |
| `AZURE_CLIENT_ID` | `your-client-id` | ❌ No | Service principal app ID |
| `AZURE_CLIENT_SECRET` | `your-client-secret` | ✅ **Yes** | Service principal password |
| `AZURE_TENANT_ID` | `your-tenant-id` | ❌ No | Azure tenant ID |

**To add a variable:**
1. Click **Add variable**
2. Enter the **Name** (exactly as shown above)
3. Enter the **Value** (from setup script output)
4. Check **Secured** for sensitive values (passwords, secrets)
5. Click **Add**

### Step 3: Verify Configuration

Your repository variables should look like this:

```
✅ AZURE_CONTAINER_REGISTRY
✅ ACR_USERNAME
🔒 ACR_PASSWORD (Secured)
✅ AZURE_SUBSCRIPTION_ID
✅ AZURE_CLIENT_ID
🔒 AZURE_CLIENT_SECRET (Secured)
✅ AZURE_TENANT_ID
```

---

## 🔄 Pipeline Overview

### Pipeline File

The pipeline is defined in `bitbucket-pipelines.yml` at the root of your repository.

### Pipeline Triggers

1. **Main/Master Branch**
   - Automatic deployment on push
   - Runs: Build → Test → Docker Build → Deploy to Azure

2. **Pull Requests**
   - Validation and testing only
   - Runs: Lint → Test → Docker Build Verification

3. **Custom Pipelines**
   - `deploy-production`: Manual deployment trigger
   - `build-only`: Build Docker images without deploying

### Pipeline Stages

#### Stage 1: Build and Test (Parallel)
- **Backend**: Install dependencies, run tests
- **Frontend**: Install dependencies, build React app

#### Stage 2: Build Docker Images (Parallel)
- **Backend Image**: Build and push to ACR
- **Frontend Image**: Build and push to ACR
- Images tagged with commit SHA and `latest`

#### Stage 3: Deploy to Azure
- Login to Azure with service principal
- Create/update resource group
- Deploy using Bicep template
- Output deployment URLs

---

## 🚀 Testing and Deployment

### Initial Deployment

1. **Commit and push** `bitbucket-pipelines.yml`:
   ```bash
   git add bitbucket-pipelines.yml
   git commit -m "Add Bitbucket Pipelines CI/CD"
   git push origin main
   ```

2. **Watch the pipeline**:
   - Go to **Pipelines** in your Bitbucket repository
   - Click on the running pipeline to see live logs
   - Pipeline should complete in ~10-15 minutes

3. **Get your URLs**:
   - Check the deployment step output for URLs
   - Frontend: `https://car-price-frontend.azurecontainerapps.io`
   - Backend: `https://car-price-backend.azurecontainerapps.io`

### Manual Deployment

You can trigger deployment manually:

1. Go to **Pipelines** in Bitbucket
2. Click **Run pipeline**
3. Select branch (e.g., `main`)
4. Select pipeline: **deploy-production**
5. Click **Run**

### Pull Request Validation

When you create a PR:
- Pipeline automatically runs validation
- Checks: Backend tests, frontend build, Docker builds
- PR status shows pipeline results
- Merge only if pipeline passes

---

## 📊 Monitoring Pipelines

### View Pipeline Status

**In Bitbucket:**
1. Go to **Pipelines** tab
2. See all pipeline runs
3. Click any run to see detailed logs
4. Check step duration and status

**Pipeline Indicators:**
- ✅ Green: Success
- ❌ Red: Failed
- ⏸️ Yellow: In progress
- ⏹️ Gray: Stopped

### View Logs

1. Click on a pipeline run
2. Click on any step to expand logs
3. Use search to find specific errors
4. Download logs if needed

### Pipeline Duration

Expected times:
- **Build & Test**: ~2-3 minutes
- **Docker Build**: ~5-7 minutes
- **Azure Deployment**: ~3-5 minutes
- **Total**: ~10-15 minutes

---

## 🐛 Troubleshooting

### Pipeline Fails at Azure Login

**Error**: `Failed to login to Azure`

**Solution**:
```bash
# Verify service principal credentials
az login --service-principal \
  -u $AZURE_CLIENT_ID \
  -p $AZURE_CLIENT_SECRET \
  --tenant $AZURE_TENANT_ID

# If fails, recreate service principal
cd azure
./setup-azure-bitbucket.sh
# Update Bitbucket variables with new credentials
```

### Docker Build Fails

**Error**: `Error response from daemon`

**Solution**:
- Check Docker service is enabled in pipeline settings
- Verify Dockerfile syntax
- Test locally: `docker build -t test .`

### ACR Login Fails

**Error**: `unauthorized: authentication required`

**Solution**:
```bash
# Verify ACR credentials
az acr credential show --name your-acr-name

# Update Bitbucket variables:
# - ACR_USERNAME
# - ACR_PASSWORD
```

### Deployment Fails

**Error**: `Deployment failed`

**Solution**:
```bash
# Check Azure CLI version in pipeline
# Verify Bicep template
az bicep build --file azure/container-app.bicep

# Check resource group exists
az group show --name car-price-rg

# Manually deploy to test
az deployment group create \
  --resource-group car-price-rg \
  --template-file azure/container-app.bicep
```

### Variables Not Found

**Error**: `Variable AZURE_CONTAINER_REGISTRY not found`

**Solution**:
1. Go to Repository Settings → Pipelines → Repository variables
2. Verify all 7 variables are added
3. Check variable names match exactly (case-sensitive)
4. Re-run pipeline

### Pipeline Hangs

**Solution**:
1. Stop the pipeline
2. Check Bitbucket status: https://status.bitbucket.org/
3. Check Azure status: https://status.azure.com/
4. Re-run pipeline

---

## 🔒 Security Best Practices

### Securing Credentials

1. **Always mark sensitive values as "Secured"**:
   - ACR_PASSWORD
   - AZURE_CLIENT_SECRET

2. **Never commit credentials**:
   - Add `azure-config.txt` to `.gitignore`
   - Never hardcode passwords in code

3. **Rotate credentials regularly**:
   ```bash
   # Rotate ACR password
   az acr credential renew --name your-acr-name --password-name password

   # Rotate service principal
   az ad sp credential reset --id $AZURE_CLIENT_ID
   ```

### Access Control

1. Limit service principal permissions
2. Use separate principals for dev/prod
3. Enable Azure AD authentication
4. Use Azure Key Vault for secrets (advanced)

---

## 📈 Advanced Configuration

### Multi-Environment Setup

Create separate pipelines for different environments:

```yaml
pipelines:
  branches:
    develop:
      - step: *deploy-to-dev
    staging:
      - step: *deploy-to-staging
    main:
      - step: *deploy-to-production
```

### Conditional Deployments

Deploy only on specific conditions:

```yaml
- step:
    name: Deploy to Production
    deployment: production
    trigger: manual  # Require manual approval
    script:
      - echo "Deploying to production..."
```

### Slack Notifications

Add Slack notifications:

```yaml
- step:
    name: Notify Slack
    script:
      - pipe: atlassian/slack-notify:2.0.0
        variables:
          WEBHOOK_URL: $SLACK_WEBHOOK
          MESSAGE: "Deployment completed!"
```

### Caching Strategy

Optimize build times with caching:

```yaml
definitions:
  caches:
    pip: ~/.cache/pip
    npm: frontend/node_modules
    docker: /var/lib/docker
```

---

## 🎯 Pipeline Best Practices

1. **Keep pipelines fast**: Parallel steps, caching
2. **Fail fast**: Run tests before building Docker images
3. **Use artifacts**: Share files between steps
4. **Tag images properly**: Use commit SHA for traceability
5. **Monitor pipeline metrics**: Track duration and success rate
6. **Use manual triggers for production**: Avoid accidental deployments

---

## 📚 Additional Resources

- [Bitbucket Pipelines Documentation](https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/)
- [Azure Container Apps](https://docs.microsoft.com/en-us/azure/container-apps/)
- [Azure CLI Reference](https://docs.microsoft.com/en-us/cli/azure/)
- [Docker in Pipelines](https://support.atlassian.com/bitbucket-cloud/docs/use-docker-images-as-build-environments/)

---

## 🆘 Getting Help

- **Bitbucket Issues**: Check pipeline logs first
- **Azure Issues**: Check `TROUBLESHOOTING.md`
- **Docker Issues**: Check `DOCKER.md`
- **General Help**: Check `DEPLOYMENT.md`

---

## ✅ Deployment Checklist

Before deploying to production:

- [ ] Azure resources created (`./setup-azure-bitbucket.sh`)
- [ ] All 7 Bitbucket variables configured
- [ ] Pipelines enabled in repository settings
- [ ] `bitbucket-pipelines.yml` committed
- [ ] Docker service enabled in pipeline settings
- [ ] Local testing completed (`docker-compose up`)
- [ ] Bicep template validated
- [ ] Service principal has correct permissions
- [ ] ACR admin access enabled
- [ ] Resource group exists in Azure

---

## 🎉 Success!

Once configured, your pipeline will:

✅ Automatically build and test on every push  
✅ Deploy to Azure on main/master branch  
✅ Validate PRs before merging  
✅ Provide deployment URLs  
✅ Handle scaling automatically  

**You're ready for automated deployments!** 🚀

---

**Last Updated**: 2025-10-19  
**Version**: 1.0.0 (Bitbucket Pipelines)
