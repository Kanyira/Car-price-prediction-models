# ⚡ Bitbucket Pipelines Quick Start

Get your automated CI/CD pipeline running in under 10 minutes!

---

## 🎯 Quick Setup (3 Steps)

### Step 1: Setup Azure (5 minutes)

```bash
cd azure
./setup-azure-bitbucket.sh
```

**Save the output!** You'll need these 7 values:
- AZURE_CONTAINER_REGISTRY
- ACR_USERNAME
- ACR_PASSWORD
- AZURE_SUBSCRIPTION_ID
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET
- AZURE_TENANT_ID

---

### Step 2: Configure Bitbucket (3 minutes)

**A. Enable Pipelines:**
1. Go to your Bitbucket repository
2. **Repository Settings** → **Pipelines** → **Settings**
3. Toggle **Enable Pipelines** to ON

**B. Add Repository Variables:**
1. **Repository Settings** → **Pipelines** → **Repository variables**
2. Click **Add variable** for each:

| Variable | Value | Secured? |
|----------|-------|----------|
| AZURE_CONTAINER_REGISTRY | From step 1 | No |
| ACR_USERNAME | From step 1 | No |
| ACR_PASSWORD | From step 1 | **✅ Yes** |
| AZURE_SUBSCRIPTION_ID | From step 1 | No |
| AZURE_CLIENT_ID | From step 1 | No |
| AZURE_CLIENT_SECRET | From step 1 | **✅ Yes** |
| AZURE_TENANT_ID | From step 1 | No |

---

### Step 3: Deploy! (2 minutes)

```bash
# Commit the pipeline file
git add bitbucket-pipelines.yml
git commit -m "Add Bitbucket CI/CD pipeline"
git push origin main
```

**Watch it deploy!**
- Go to **Pipelines** tab in Bitbucket
- Watch the live progress
- Get your URLs from the deployment output

---

## 🎊 That's It!

Your pipeline will now:

✅ **Automatically build** on every push  
✅ **Run tests** before deployment  
✅ **Build Docker images** for frontend & backend  
✅ **Deploy to Azure** automatically  
✅ **Scale automatically** based on traffic  

---

## 📊 What Happens Next?

### On Every Push to Main/Master:
1. ✅ Build and test backend (Python)
2. ✅ Build and test frontend (React)
3. ✅ Build Docker images
4. ✅ Push to Azure Container Registry
5. ✅ Deploy to Azure Container Apps
6. ✅ Output deployment URLs

### On Pull Requests:
1. ✅ Validate and lint code
2. ✅ Run tests
3. ✅ Verify Docker builds
4. ❌ No deployment (validation only)

---

## 🌐 Access Your App

After deployment completes, check the pipeline output for URLs:

```
🚀 Deployment Successful!
Backend URL: https://car-price-backend.azurecontainerapps.io
Frontend URL: https://car-price-frontend.azurecontainerapps.io
```

---

## 🔍 Monitor Your Pipeline

### View Pipeline Status:
1. Go to **Pipelines** tab
2. See all runs with status
3. Click any run for detailed logs

### Pipeline Duration:
- ⏱️ First run: ~15-20 minutes (downloads images)
- ⏱️ Subsequent runs: ~10-12 minutes (cached)

---

## 🚀 Manual Deployment

Trigger deployment manually:

1. Go to **Pipelines** tab
2. Click **Run pipeline**
3. Select **deploy-production**
4. Click **Run**

---

## 🐛 Common Issues

### "Variables not found"
**Solution**: Double-check all 7 variables are added in Repository variables

### "Docker login failed"
**Solution**: Verify ACR_USERNAME and ACR_PASSWORD are correct

### "Azure login failed"
**Solution**: Re-run setup script and update service principal credentials

### Pipeline stuck?
**Solution**: Stop and re-run, check Bitbucket status page

---

## 📖 Need More Help?

- **Full Guide**: `BITBUCKET_SETUP.md`
- **Troubleshooting**: `TROUBLESHOOTING.md`
- **Docker Help**: `DOCKER.md`
- **Deployment**: `DEPLOYMENT.md`

---

## 💡 Pro Tips

1. **Test locally first**: `docker-compose up --build`
2. **Check logs**: Click on pipeline steps for details
3. **Secure secrets**: Always mark passwords as "Secured"
4. **Use PR validation**: Test before merging
5. **Monitor costs**: Check Azure cost analysis

---

## ✅ Verification Checklist

Before pushing:

- [ ] Azure setup completed
- [ ] All 7 Bitbucket variables added
- [ ] Pipelines enabled
- [ ] Variables marked as secured (2 of them)
- [ ] Local Docker test passed
- [ ] Committed bitbucket-pipelines.yml

---

## 🎯 What You Get

Your application is now:

✅ **Fully automated** - Push to deploy  
✅ **Production-ready** - Azure Container Apps  
✅ **Auto-scaling** - Handles traffic spikes  
✅ **Monitored** - Health checks enabled  
✅ **Tested** - Automated testing on every commit  
✅ **Secure** - Service principal authentication  

---

## 🎉 Success!

You now have a **fully automated CI/CD pipeline** that deploys to Azure on every push!

**Next**: Push your code and watch it deploy automatically! 🚀

---

**Questions?** Check `BITBUCKET_SETUP.md` for detailed documentation.
