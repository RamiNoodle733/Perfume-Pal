# Perfume Pal - Cloud Run Deployment Guide

## Prerequisites
1. Google Cloud CLI installed
2. Google Cloud account with billing enabled
3. Docker Desktop installed (optional, Cloud Build will handle it)

## Step 1: Install Google Cloud CLI
Download from: https://cloud.google.com/sdk/docs/install

## Step 2: Authenticate and Set Up Project
```bash
# Login to Google Cloud
gcloud auth login

# Set your project (replace with your project ID)
gcloud config set project perfume-pal-project

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

## Step 3: Create .gcloudignore File
Already included in the repo to exclude unnecessary files from deployment.

## Step 4: Deploy to Cloud Run
```bash
# Deploy with Cloud Build (automatically builds and deploys)
gcloud run deploy perfume-pal \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=AIzaSyB56m7EIiYtHIMH7x-X14Y9gBp1515UzlU,GOOGLE_CLOUD_PROJECT=perfume-pal-project \
  --port 8080 \
  --memory 512Mi \
  --timeout 300s
```

## Step 5: Get Your Public URL
After deployment completes, you'll see:
```
Service [perfume-pal] revision [perfume-pal-00001-xxx] has been deployed and is serving 100 percent of traffic.
Service URL: https://perfume-pal-xxxxx-uc.a.run.app
```

This URL is your public link that anyone can access!

## Step 6: Update Devpost Submission
Add the Cloud Run URL to:
- "Try it out" links
- "URL to the hosted Project for judging and testing"

## Step 7: Test Your Deployment
Visit your Cloud Run URL and test:
1. Intro screen loads
2. Click "ENTER SYSTEM"
3. Generate a perfume recipe
4. Check the About section

## Troubleshooting

### If you get authentication errors:
```bash
gcloud auth application-default login
```

### To view logs:
```bash
gcloud run services logs read perfume-pal --region us-central1 --limit 50
```

### To update environment variables:
```bash
gcloud run services update perfume-pal \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY=your-new-key
```

### To redeploy after code changes:
```bash
gcloud run deploy perfume-pal --source . --region us-central1
```

## Environment Variables
The deployment command sets:
- `GOOGLE_API_KEY`: Your Gemini API key
- `GOOGLE_CLOUD_PROJECT`: Your project ID
- `PORT`: Automatically set by Cloud Run to 8080

## Cost Estimate
Cloud Run free tier includes:
- 2 million requests per month
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds of compute time

Your app should stay within free tier for the hackathon!

## Security Notes
- The API key is set as an environment variable (not exposed in code)
- Service is set to `--allow-unauthenticated` for public access
- For production, consider using Secret Manager instead of environment variables
