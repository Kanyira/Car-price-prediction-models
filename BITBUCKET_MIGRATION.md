# 🔄 Migrating to Bitbucket Pipelines

This guide helps you migrate from GitHub Actions to Bitbucket Pipelines.

## ✅ What Changed

### Files Added
- ✅ `bitbucket-pipelines.yml` - CI/CD pipeline configuration
- ✅ `azure/setup-azure-bitbucket.sh` - Bitbucket-specific setup script
- ✅ `BITBUCKET_SETUP.md` - Complete setup guide
- ✅ `BITBUCKET_QUICKSTART.md` - Quick start guide
- ✅ `.gitignore` - Updated to exclude azure-config.txt

### Files Kept (Still Useful)
- ✅ `Dockerfile` - Backend container (unchanged)
- ✅ `frontend/Dockerfile` - Frontend container (unchanged)
- ✅ `docker-compose.yml` - Local testing (unchanged)
- ✅ `azure/container-app.bicep` - Azure infrastructure (unchanged)
- ✅ All application code (unchanged)

### Files Not Needed Anymore
- ❌ `.github/workflows/` - GitHub Actions (can be deleted)
- ❌ `azure/setup-azure.sh` - GitHub version (use Bitbucket version)

---

## 🚀 Migration Steps

### Step 1: Remove GitHub Actions (Optional)

```bash
# Remove GitHub Actions workflows (if you won't use GitHub anymore)
rm -rf .github/

# Or keep them if you want to maintain both platforms
```

### Step 2: Setup Azure for Bitbucket

```bash
cd azure
./setup-azure-bitbucket.sh
```

**Important Differences:**
- Outputs different credentials format
- Creates service principal credentials (not JSON)
- Saves configuration to `azure-config.txt`

### Step 3: Configure Bitbucket

1. **Enable Pipelines**:
   - Repository Settings → Pipelines → Settings
   - Enable Pipelines

2. **Add Repository Variables** (7 total):
   - AZURE_CONTAINER_REGISTRY
   - ACR_USERNAME
   - ACR_PASSWORD (secured)
   - AZURE_SUBSCRIPTION_ID
   - AZURE_CLIENT_ID
   - AZURE_CLIENT_SECRET (secured)
   - AZURE_TENANT_ID

### Step 4: Update and Push

```bash
# Add the pipeline file
git add bitbucket-pipelines.yml

# Optional: Remove GitHub Actions
git rm -rf .github/

# Commit and push
git commit -m "Migrate to Bitbucket Pipelines"
git push origin main
```

---

## 🔍 Key Differences

### GitHub Actions vs Bitbucket Pipelines

| Feature | GitHub Actions | Bitbucket Pipelines |
|---------|---------------|-------------------|
| **Config File** | `.github/workflows/*.yml` | `bitbucket-pipelines.yml` |
| **Secrets** | Repository Secrets | Repository Variables |
| **Parallel Jobs** | `jobs:` with `needs:` | `parallel:` steps |
| **Manual Trigger** | `workflow_dispatch` | `custom:` pipelines |
| **Artifacts** | `actions/upload-artifact` | `artifacts:` in step |
| **Caching** | `actions/cache` | `caches:` definition |
| **Docker** | Built-in | Requires `docker` service |

### Authentication Differences

**GitHub Actions** (JSON format):
```json
{
  "clientId": "xxx",
  "clientSecret": "xxx",
  "subscriptionId": "xxx",
  "tenantId": "xxx"
}
```

**Bitbucket Pipelines** (Individual variables):
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET
- AZURE_SUBSCRIPTION_ID
- AZURE_TENANT_ID

### Pipeline Syntax Comparison

**GitHub Actions:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: docker build .
```

**Bitbucket Pipelines:**
```yaml
pipelines:
  default:
    - step:
        name: Build
        script:
          - docker build .
```

---

## 📊 Feature Parity

Both platforms support:

✅ **Automated triggers** (push, PR, manual)  
✅ **Parallel execution** (faster builds)  
✅ **Docker support** (build and push images)  
✅ **Secrets management** (secure variables)  
✅ **Artifact sharing** (between steps)  
✅ **Caching** (dependencies, Docker layers)  
✅ **Branch-specific pipelines**  
✅ **Manual approvals** (custom pipelines)  

---

## 🎯 Why Bitbucket Pipelines?

Advantages:
- ✅ Integrated with Bitbucket
- ✅ Simple configuration
- ✅ Good free tier (50 minutes/month)
- ✅ Native Docker support
- ✅ Easy parallel execution
- ✅ Built-in deployment tracking

Considerations:
- ⚠️ Minute-based billing
- ⚠️ Fewer pre-built actions
- ⚠️ Community smaller than GitHub

---

## 📝 Updated Documentation

After migration, use these docs:

| For This | Read This |
|----------|-----------|
| Quick setup | BITBUCKET_QUICKSTART.md |
| Full guide | BITBUCKET_SETUP.md |
| Docker help | DOCKER.md (unchanged) |
| Troubleshooting | TROUBLESHOOTING.md (unchanged) |
| Deployment | DEPLOYMENT.md (updated) |

---

## 🔧 Testing Your Pipeline

### 1. Local Test First

```bash
docker-compose up --build
```

Verify everything works locally.

### 2. Test Pipeline

Push to a feature branch first:

```bash
git checkout -b test-pipeline
git push origin test-pipeline
```

Check Pipelines tab for results.

### 3. Deploy to Production

Once verified, merge to main:

```bash
git checkout main
git merge test-pipeline
git push origin main
```

---

## 🐛 Common Migration Issues

### Issue: Variables Not Working

**Symptom**: Pipeline fails with "Variable not found"

**Solution**:
- Check variable names are EXACT (case-sensitive)
- Verify all 7 variables are added
- Check for typos in variable names

### Issue: Azure Login Fails

**Symptom**: "Failed to login to Azure"

**Solution**:
- Use Bitbucket setup script (not GitHub one)
- Verify service principal credentials
- Check AZURE_CLIENT_SECRET is marked as secured

### Issue: Docker Build Fails

**Symptom**: "Cannot connect to Docker daemon"

**Solution**:
- Add `docker` to `services:` in step
- Increase memory: `docker: memory: 3072`

### Issue: Deployment Timeout

**Symptom**: Pipeline hangs at deployment

**Solution**:
- Check Azure CLI version
- Verify resource group exists
- Test deployment manually first

---

## 📊 Cost Comparison

### GitHub Actions
- Free: 2,000 minutes/month (public repos)
- Free: 2,000 minutes/month (private repos)
- Paid: $0.008/minute (after free tier)

### Bitbucket Pipelines
- Free: 50 minutes/month
- Paid: $10/month for 2,500 minutes
- Additional: $10/1,000 minutes

**Your Usage** (~15 min/deployment):
- 3 deployments/day = ~1,350 minutes/month
- Bitbucket cost: ~$10-20/month
- GitHub cost: $0 (if public) or $0 (within free tier)

---

## ✅ Migration Checklist

- [ ] Azure setup completed (Bitbucket version)
- [ ] 7 Bitbucket variables configured
- [ ] Pipelines enabled in repository
- [ ] `bitbucket-pipelines.yml` added
- [ ] Local Docker test passed
- [ ] Test pipeline on feature branch
- [ ] Production deployment successful
- [ ] Old GitHub Actions removed (optional)
- [ ] Documentation updated
- [ ] Team notified of change

---

## 🎉 Migration Complete!

You're now using Bitbucket Pipelines for CI/CD!

**Next steps**:
1. Monitor first few deployments
2. Optimize pipeline (caching, parallel steps)
3. Set up deployment notifications
4. Configure branch-specific pipelines

---

## 🆘 Need Help?

- **Bitbucket Help**: [BITBUCKET_SETUP.md](BITBUCKET_SETUP.md)
- **General Issues**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Docker Issues**: [DOCKER.md](DOCKER.md)
- **Bitbucket Docs**: https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/

---

**Migration Date**: 2025-10-19  
**Status**: ✅ Complete
