# Deployment Guide

This guide will walk you through deploying the YouTube Channel Fetcher application to production using Fly.io (backend) and Vercel (frontend).

## Prerequisites

- GitHub account
- Fly.io account (sign up at [fly.io](https://fly.io))
- Vercel account (sign up at [vercel.com](https://vercel.com))
- Fly CLI installed (see installation instructions below)
- YouTube Data API v3 key ([Get one here](https://console.cloud.google.com/apis/credentials))

## Part 1: Deploy Backend to Fly.io

### Step 1: Install Fly CLI

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**macOS/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Or download from:** [fly.io/docs/hands-on/install-flyctl/](https://fly.io/docs/hands-on/install-flyctl/)

### Step 2: Login to Fly.io

```bash
fly auth login
```

This will open your browser to authenticate.

### Step 3: Initialize Fly.io App

From your project root directory:

```bash
fly launch
```

When prompted:
- **App name**: Choose a unique name (e.g., `youtube-fetcher-backend`)
- **Region**: Choose the closest region (e.g., `iad` for US East, `lhr` for London)
- **PostgreSQL**: Select `n` (we'll use SQLite initially)
- **Redis**: Select `n`
- **Deploy now**: Select `n` (we'll set secrets first)

### Step 4: Update fly.toml

Edit `fly.toml` and replace `your-app-name` with your actual app name:

```toml
app = "your-actual-app-name"
```

### Step 5: Set Environment Variables (Secrets)

Set your secrets using Fly CLI:

```bash
# Generate a secure secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set secrets (replace values with your actual values)
fly secrets set SECRET_KEY="your-generated-secret-key-here"
fly secrets set DEBUG="False"
fly secrets set YOUTUBE_API_KEY="your-youtube-api-key-here"
fly secrets set ALLOWED_HOSTS="your-app-name.fly.dev"
```

### Step 6: Deploy

```bash
fly deploy
```

This will:
- Build the Docker image
- Push it to Fly.io
- Deploy your application

### Step 7: Get Your Backend URL

After deployment, your backend will be available at:
```
https://your-app-name.fly.dev
```

Verify it's working:
```bash
curl https://your-app-name.fly.dev/api/channel/videos/
```

You should get a 405 Method Not Allowed (expected for GET request to POST endpoint).

### Step 8: View Logs (Optional)

```bash
fly logs
```

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Push Code to GitHub

If you haven't already, push your code to GitHub:

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Connect Repository to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (or leave default)
   - **Output Directory**: `build`

### Step 3: Set Environment Variables

In Vercel project settings, add:

- **Name**: `REACT_APP_API_URL`
- **Value**: `https://your-app-name.fly.dev` (your Fly.io backend URL)

### Step 4: Deploy

Click **"Deploy"**. Vercel will:
- Install dependencies
- Build your React app
- Deploy to their CDN

Your frontend will be available at:
```
https://your-project-name.vercel.app
```

---

## Part 3: Update CORS Settings

After deploying the frontend, you need to update the backend CORS settings to allow your Vercel domain.

### Option 1: Using Environment Variable (Recommended)

Set the frontend URL as a secret in Fly.io:

```bash
fly secrets set FRONTEND_URL="https://your-project-name.vercel.app"
```

Then redeploy:

```bash
fly deploy
```

### Option 2: Manual Update

Alternatively, you can manually update `youtube_channel_fetcher/settings.py` to add your Vercel URL to `CORS_ALLOWED_ORIGINS`, then redeploy.

---

## Part 4: Verification

### Test Backend API

```bash
curl -X POST https://your-app-name.fly.dev/api/channel/videos/ \
  -H "Content-Type: application/json" \
  -d '{"channel_url": "https://www.youtube.com/@channelname"}'
```

### Test Frontend

1. Open your Vercel URL in a browser
2. Try fetching videos from a YouTube channel
3. Verify everything works end-to-end

---

## Troubleshooting

### Backend Issues

**Issue: App won't start**
- Check logs: `fly logs`
- Verify secrets are set: `fly secrets list`
- Ensure `ALLOWED_HOSTS` includes your Fly.io domain

**Issue: Static files not loading**
- Ensure `STATIC_ROOT` is set correctly
- Run `python manage.py collectstatic` locally to test
- Check WhiteNoise middleware is in `MIDDLEWARE`

**Issue: Database errors**
- SQLite should work out of the box
- For PostgreSQL, create a database: `fly postgres create`

### Frontend Issues

**Issue: CORS errors**
- Verify `REACT_APP_API_URL` is set correctly in Vercel
- Check backend `CORS_ALLOWED_ORIGINS` includes your Vercel domain
- Ensure backend is deployed and accessible

**Issue: Build fails**
- Check Vercel build logs
- Ensure all dependencies are in `package.json`
- Verify Node.js version compatibility

**Issue: API calls fail**
- Verify `REACT_APP_API_URL` environment variable is set
- Check backend is running and accessible
- Check browser console for detailed error messages

### General Issues

**Issue: Environment variables not working**
- In Fly.io: Use `fly secrets set KEY=value`
- In Vercel: Set in project settings → Environment Variables
- Restart/redeploy after setting variables

**Issue: Slow response times**
- First request may be slow (cold start)
- Subsequent requests should be faster
- Consider upgrading Fly.io plan if needed

---

## Updating Your Deployment

### Update Backend

1. Make changes to your code
2. Commit and push to GitHub
3. Redeploy: `fly deploy`

### Update Frontend

1. Make changes to your code
2. Commit and push to GitHub
3. Vercel will automatically deploy (if connected to GitHub)

---

## Cost

- **Fly.io**: Free tier includes 3 shared VMs (256MB each), always-on
- **Vercel**: Free tier includes unlimited deployments, always-on
- **Total**: $0/month for this setup

---

## Next Steps

- Set up custom domain (optional)
- Add PostgreSQL database (if needed)
- Set up monitoring and alerts
- Configure CI/CD for automatic deployments

---

## Support

- Fly.io Docs: [fly.io/docs](https://fly.io/docs)
- Vercel Docs: [vercel.com/docs](https://vercel.com/docs)
- Django Deployment: [docs.djangoproject.com/en/stable/howto/deployment/](https://docs.djangoproject.com/en/stable/howto/deployment/)

