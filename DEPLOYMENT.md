# Cloud Run Deployment Guide

This guide provides step-by-step instructions for deploying Perfume Pal to Google Cloud Run.

## Prerequisites

Before deploying, ensure you have:

1. ✅ Google Cloud account with billing enabled
2. ✅ Google Cloud SDK (`gcloud`) installed
3. ✅ Docker installed (optional, for local testing)
4. ✅ Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
5. ✅ Git repository with your code

## Step 1: Set Up Google Cloud Project

### 1.1 Create or Select a Project

```powershell
# List existing projects
gcloud projects list

# Create a new project (optional)
gcloud projects create perfume-pal-project --name="Perfume Pal"

# Set the active project
gcloud config set project perfume-pal-project
```

### 1.2 Enable Required APIs

```powershell
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Cloud Build API (for building containers)
gcloud services enable cloudbuild.googleapis.com

# Enable Artifact Registry API
gcloud services enable artifactregistry.googleapis.com

# Enable Generative AI API (optional, if using Vertex AI)
gcloud services enable aiplatform.googleapis.com
```

### 1.3 Set Default Region

```powershell
# Set your preferred region
gcloud config set run/region us-central1
```

## Step 2: Prepare Your Application

### 2.1 Test Locally First

```powershell
# Set environment variables
$env:GOOGLE_API_KEY="your-gemini-api-key"
$env:GOOGLE_CLOUD_PROJECT="perfume-pal-project"

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --host 0.0.0.0 --port 8080

# Test in browser: http://localhost:8080
```

### 2.2 Test with Docker Locally (Optional)

```powershell
# Build the Docker image
docker build -t perfume-pal .

# Run the container
docker run -p 8080:8080 `
  -e GOOGLE_API_KEY="your-api-key" `
  -e GOOGLE_CLOUD_PROJECT="perfume-pal-project" `
  perfume-pal

# Test in browser: http://localhost:8080
```

## Step 3: Deploy to Cloud Run

### Method 1: Deploy from Source (Recommended)

This method builds the container in the cloud automatically.

```powershell
gcloud run deploy perfume-pal `
  --source . `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars GOOGLE_API_KEY="your-gemini-api-key",GOOGLE_CLOUD_PROJECT="perfume-pal-project" `
  --min-instances 0 `
  --max-instances 10 `
  --memory 512Mi `
  --cpu 1 `
  --timeout 60
```

**Flags Explained:**
- `--source .`: Build from current directory
- `--region us-central1`: Deploy to US Central region
- `--allow-unauthenticated`: Allow public access
- `--set-env-vars`: Set environment variables
- `--min-instances 0`: Scale to zero when not in use (free tier friendly)
- `--max-instances 10`: Maximum concurrent instances
- `--memory 512Mi`: Allocate 512MB RAM
- `--cpu 1`: 1 vCPU
- `--timeout 60`: 60 second request timeout

### Method 2: Deploy from Container Registry

Build and push the image first, then deploy.

```powershell
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/perfume-pal-project/perfume-pal

# Deploy the image
gcloud run deploy perfume-pal `
  --image gcr.io/perfume-pal-project/perfume-pal `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars GOOGLE_API_KEY="your-gemini-api-key",GOOGLE_CLOUD_PROJECT="perfume-pal-project"
```

### Method 3: Deploy from Artifact Registry (Recommended for Production)

```powershell
# Create Artifact Registry repository
gcloud artifacts repositories create perfume-pal-repo `
  --repository-format=docker `
  --location=us-central1 `
  --description="Perfume Pal container images"

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build and tag the image
docker build -t us-central1-docker.pkg.dev/perfume-pal-project/perfume-pal-repo/perfume-pal:latest .

# Push to Artifact Registry
docker push us-central1-docker.pkg.dev/perfume-pal-project/perfume-pal-repo/perfume-pal:latest

# Deploy from Artifact Registry
gcloud run deploy perfume-pal `
  --image us-central1-docker.pkg.dev/perfume-pal-project/perfume-pal-repo/perfume-pal:latest `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars GOOGLE_API_KEY="your-gemini-api-key",GOOGLE_CLOUD_PROJECT="perfume-pal-project"
```

## Step 4: Verify Deployment

### 4.1 Get Service URL

```powershell
# Get the service URL
gcloud run services describe perfume-pal --region us-central1 --format="value(status.url)"
```

Example output: `https://perfume-pal-xxxxx-uc.a.run.app`

### 4.2 Test the Deployed Service

```powershell
# Test health endpoint
curl https://perfume-pal-xxxxx-uc.a.run.app/health

# Or open in browser
start https://perfume-pal-xxxxx-uc.a.run.app
```

### 4.3 Test API Endpoint

```powershell
# PowerShell example
$body = @{
    style = "dark oud"
    strength = "moderate"
    bottle_size_ml = 10
    vibe_words = @("smoky", "warm")
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://perfume-pal-xxxxx-uc.a.run.app/api/generate_blends" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

## Step 5: Configure Custom Domain (Optional)

### 5.1 Map a Custom Domain

```powershell
# Map your domain
gcloud run domain-mappings create `
  --service perfume-pal `
  --domain perfume-pal.yourdomain.com `
  --region us-central1

# Follow the instructions to add DNS records to your domain provider
```

### 5.2 Enable HTTPS

Cloud Run automatically provides HTTPS certificates for custom domains.

## Step 6: Update Environment Variables

If you need to update environment variables after deployment:

```powershell
gcloud run services update perfume-pal `
  --region us-central1 `
  --set-env-vars GOOGLE_API_KEY="new-api-key"

# Or update multiple variables
gcloud run services update perfume-pal `
  --region us-central1 `
  --set-env-vars GOOGLE_API_KEY="new-api-key",ENVIRONMENT="production"
```

## Step 7: View Logs and Monitor

### 7.1 View Logs

```powershell
# Stream logs
gcloud run services logs tail perfume-pal --region us-central1

# View logs in Cloud Console
gcloud run services logs read perfume-pal --region us-central1 --limit 50
```

### 7.2 Monitor in Cloud Console

1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click on your service
3. View metrics: requests, latency, errors, CPU, memory

## Step 8: Cost Optimization

### 8.1 Set Scaling Limits

```powershell
# Update to scale to zero when idle (free tier friendly)
gcloud run services update perfume-pal `
  --region us-central1 `
  --min-instances 0 `
  --max-instances 5
```

### 8.2 Monitor Costs

```powershell
# View billing in Cloud Console
gcloud billing accounts list

# Set up budget alerts in Cloud Console
# Go to: Billing > Budgets & alerts
```

### Free Tier Limits (as of 2025)
- 2 million requests per month
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds of compute time
- 1 GB network egress from North America per month

## Step 9: CI/CD with GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - id: 'auth'
      uses: 'google-github-actions/auth@v1'
      with:
        credentials_json: '${{ secrets.GCP_SA_KEY }}'
    
    - name: 'Deploy to Cloud Run'
      uses: 'google-github-actions/deploy-cloudrun@v1'
      with:
        service: 'perfume-pal'
        region: 'us-central1'
        source: '.'
        env_vars: |
          GOOGLE_API_KEY=${{ secrets.GOOGLE_API_KEY }}
          GOOGLE_CLOUD_PROJECT=${{ secrets.GCP_PROJECT_ID }}
```

## Troubleshooting

### Issue: Deployment Fails

```powershell
# Check build logs
gcloud builds list --limit 5

# View specific build
gcloud builds log BUILD_ID
```

### Issue: Service Returns 500 Errors

```powershell
# Check logs for errors
gcloud run services logs tail perfume-pal --region us-central1

# Common issues:
# - Missing environment variables
# - Invalid API key
# - Timeout issues (increase timeout)
```

### Issue: Cold Start Latency

```powershell
# Keep at least 1 instance warm
gcloud run services update perfume-pal `
  --region us-central1 `
  --min-instances 1
```

### Issue: Memory Issues

```powershell
# Increase memory allocation
gcloud run services update perfume-pal `
  --region us-central1 `
  --memory 1Gi
```

## Cleanup

To delete the service and stop incurring charges:

```powershell
# Delete Cloud Run service
gcloud run services delete perfume-pal --region us-central1

# Delete container images
gcloud container images delete gcr.io/perfume-pal-project/perfume-pal

# Delete the project (WARNING: deletes everything)
gcloud projects delete perfume-pal-project
```

## Security Best Practices

1. **Never commit secrets**: Use environment variables
2. **Least privilege**: Create a service account with minimal permissions
3. **Authentication**: For production, consider requiring authentication
4. **API keys**: Rotate API keys regularly
5. **Monitoring**: Set up alerts for unusual activity
6. **HTTPS only**: Cloud Run enforces this by default

## Production Checklist

- [ ] API key stored securely (Secret Manager recommended)
- [ ] Proper error handling implemented
- [ ] Logging configured
- [ ] Monitoring and alerts set up
- [ ] Budget alerts configured
- [ ] Scaling limits set appropriately
- [ ] Custom domain configured (optional)
- [ ] CI/CD pipeline set up (optional)
- [ ] Load testing performed
- [ ] Documentation updated

## Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Best Practices](https://cloud.google.com/run/docs/tips)
- [Troubleshooting](https://cloud.google.com/run/docs/troubleshooting)

---

**Need Help?**
- Cloud Run Documentation: https://cloud.google.com/run/docs
- Community Support: https://stackoverflow.com/questions/tagged/google-cloud-run
- Google Cloud Support: https://cloud.google.com/support
