# Vercel Deployment Guide

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

## If You Still Get 500 Errors:

Check Vercel's function logs:
1. Go to Vercel dashboard → your project
2. Go to the "Deployments" tab
3. Click on the latest deployment
4. Look for error messages in the logs

Common issues:
- **DATABASE_URL not set**: Check your environment variables
- **SECRET_KEY missing**: Add it to Vercel environment
- **Database not accessible**: Ensure PostgreSQL accepts connections from Vercel's IPs
- **Static files**: Make sure `collectstatic` runs during build

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
