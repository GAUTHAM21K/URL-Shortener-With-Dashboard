# Vercel Deployment Guide

## Quick Diagnosis

If you're seeing errors, check in this order:

1. **404 Error**: Frontend not serving
   - ✅ Go to: https://url-shortener-with-dashboard.vercel.app/
   - Should see React UI, not 404
   - If 404: Frontend build failed (check Vercel logs)

2. **500 Error on `/api/shorten/`**: Backend issue
   - ✅ Go to: https://url-shortener-with-dashboard.vercel.app/api/urls/
   - Should see JSON array, not 500
   - If 500: Check environment variables

## Environment Variables to Set in Vercel Dashboard

You MUST set these environment variables in your Vercel project settings:

### Required Variables (CRITICAL):

1. **SECRET_KEY**: A strong random key for Django
   - Generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - Example: `django-insecure-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

2. **DATABASE_URL**: Your PostgreSQL connection string
   - Format: `postgresql://user:password@host:port/dbname`
   - Must be SSL-enabled for Vercel (use `?sslmode=require`)

3. **BASE_URL**: Your Vercel deployment URL
   - Example: `https://url-shortener-with-dashboard.vercel.app`
   - Used to generate correct short links

### Optional Variables:

- **DEBUG**: Set to `False` (default, recommended for production)
- **PYTHONUNBUFFERED**: `1` (for better logging)

## Steps to Deploy:

### 1. Generate a Secret Key

```bash
cd backend
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and save it.

### 2. Set Up PostgreSQL Database

- Create a PostgreSQL database (e.g., on Neon DB or AWS RDS)
- Get your DATABASE_URL in the format: `postgresql://user:password@host:5432/database?sslmode=require`

### 3. Configure Vercel Environment Variables

1. Go to your Vercel project settings
2. Go to "Environment Variables"
3. Add these variables:
   - `SECRET_KEY`: (the key you generated)
   - `DATABASE_URL`: (your PostgreSQL URL)
   - `BASE_URL`: (your vercel domain, e.g., https://url-shortener-with-dashboard.vercel.app)
   - `DEBUG`: `False`

### 4. Push to GitHub and Deploy

```bash
git add .
git commit -m "Fix Vercel deployment"
git push origin main
```

Vercel will automatically deploy when you push. The deployment will:

- Install Python dependencies
- Run Django migrations
- Build the frontend
- Start the server

## If You Get 404 Errors:

Check the following:

1. **Frontend not built**: Ensure npm run build worked
   - Go to Vercel deployment logs
   - Look for errors in "Frontend" build output

2. **Missing environment variables**: Still critical
   - Even though 500 → 404, env vars matter for the backend to function
   - Set: `SECRET_KEY`, `DATABASE_URL`, `BASE_URL`, `DEBUG=False`

3. **Routes not matching**: Check vercel.json routing
   - `/api/*` should route to Python backend
   - Everything else should serve React frontend
   - React Router should handle client-side routing

4. **Static files missing**:
   - Verify `frontend/dist` folder exists after build
   - Check that Vite build completed successfully

### Debugging Steps:

1. **Check Vercel Build Logs**:
   - Go to Vercel Dashboard → Your Project
   - Click "Deployments" tab
   - Click latest deployment
   - Check both "Frontend" and "Backend" build logs

2. **Test Backend API Directly**:

   ```bash
   curl https://url-shortener-with-dashboard.vercel.app/api/urls/
   ```

   Should return JSON, not 404

3. **Test Frontend**:

   ```bash
   curl https://url-shortener-with-dashboard.vercel.app/ | head -20
   ```

   Should return HTML with `<!DOCTYPE html>`

4. **Check if migrations need to run**:
   - If backend returns 500, database tables might not exist
   - This requires DATABASE_URL to be set during build

## If You Still Get 500 Errors on /api/:

Migrations might not be running. Solution:

### Option A: Use Neon DB with automatic schema (Recommended)

1. Create database at https://neon.tech
2. Set DATABASE_URL from Neon dashboard
3. Manually run migrations locally, then sync to Neon
4. Or add migration script to vercel.json

### Option B: Add migration command to build

Update `vercel.json`'s Python build config to run migrations automatically

## Testing Locally:

To test before deploying:

```bash
# In backend directory, with environment variables
export DATABASE_URL="postgresql://user:password@localhost:5432/urlshorten"
export SECRET_KEY="your-secret-key"
export BASE_URL="http://localhost:8000"
export DEBUG="True"

python manage.py migrate
python manage.py runserver
```

Then test with:

```bash
curl -X POST http://localhost:8000/api/shorten/ \\
  -H "Content-Type: application/json" \\
  -d '{"long_url": "https://google.com"}'
```
