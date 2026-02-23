# Production Issues Fixed for Vercel Deployment

## Problems Identified

### 1. **Hardcoded Localhost URLs in Backend**
- **Issue**: `views.py` was returning `http://localhost:8000/` for short URLs
- **Problem**: This doesn't work on Vercel where the domain is `*.vercel.app`
- **Fix**: Created `get_base_url()` function that:
  - Reads `BASE_URL` environment variable (best for production)
  - Falls back to request's domain (works for both local and production)
  - Properly determines HTTPS vs HTTP based on request

### 2. **Missing Environment Variables**
- **Issue**: `SECRET_KEY` defaulted to a dev key, `DEBUG` was set to `True`, database URL might not be set
- **Problem**: Django won't start properly in production without these
- **Fix**: Updated `settings.py` to:
  - Require `SECRET_KEY` from environment (generates error if not set)
  - Set `DEBUG = False` by default for production
  - Properly configure `ALLOWED_HOSTS` for *.vercel.app domains

### 3. **Poor Error Logging**
- **Issue**: 500 errors weren't showing what went wrong
- **Problem**: Hard to debug Vercel deployment issues
- **Fix**: Added comprehensive logging configuration that outputs to console (visible in Vercel logs)

### 4. **CORS/CSRF Misconfiguration for Production**
- **Issue**: CORS was set to allow all origins broadly
- **Problem**: Not optimal for production security
- **Fix**: 
  - Specific `CORS_ALLOWED_ORIGINS` list for development
  - `CORS_ALLOW_ALL_ORIGINS = True` only in production (when `DEBUG=False`)
  - Proper `CSRF_TRUSTED_ORIGINS` configuration

### 5. **Frontend Build Configuration**
- **Issue**: `vercel.json` was using `@vercel/static-build` for frontend
- **Problem**: Doesn't properly handle Vite build process
- **Fix**: Changed to `@vercel/node` builder which properly handles `package.json` scripts

### 6. **Missing Database Migrations in Build**
- **Issue**: `vercel.json` didn't specify how to run migrations on deploy
- **Problem**: Database tables don't get created when deploying to Vercel
- **Fix**: Added `buildCommand` to run migrations during build process

## Files Modified

### 1. `backend/shortener/views.py`
- Added `get_base_url(request)` function
- Updated `shorten_url()` to use dynamic base URL
- Updated `get_all_urls()` to use dynamic base URL
- Added error logging with `logger.error()`

### 2. `backend/core/settings.py`
- Proper SECRET_KEY handling with environment variable
- DEBUG mode based on environment
- Added comprehensive LOGGING configuration
- Fixed CORS and CSRF settings for production
- Proper ALLOWED_HOSTS configuration

### 3. `vercel.json`
- Updated to use `@vercel/node` for frontend
- Added `/admin/` routing for Django admin
- Added `buildCommand` for running migrations and builds
- Set environment variables at build time

## Files Created

### 1. `.env.example`
Template showing all required environment variables

### 2. `VERCEL_DEPLOYMENT.md`
Comprehensive deployment guide with step-by-step instructions

### 3. `generate_secret_key.py`
Helper script to generate and display SECRET_KEY

### 4. `backend/build.sh`
Build script for running migrations

## What You Need To Do

### 1. Generate SECRET_KEY
```bash
python generate_secret_key.py
```

### 2. Set Vercel Environment Variables
Go to Vercel Dashboard → Your Project → Settings → Environment Variables

Add:
- `SECRET_KEY`: Your generated key
- `DATABASE_URL`: Your PostgreSQL connection string (with `?sslmode=require`)
- `BASE_URL`: Your Vercel domain (e.g., `https://url-shortener-with-dashboard.vercel.app`)
- `DEBUG`: `False`

### 3. Push and Deploy
```bash
git add .
git commit -m "Fix: Vercel production deployment issues"
git push origin main
```

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| 500 errors on `/api/shorten/` | `SECRET_KEY` not set | Add `SECRET_KEY` to Vercel env vars |
| 500 errors on `/api/urls/` | `DATABASE_URL` not set or invalid | Verify `DATABASE_URL` in Vercel env vars |
| Wrong domain in short URLs | `BASE_URL` not set | Add `BASE_URL` to Vercel env vars |
| Build fails | Missing frontend build | Check `frontend/package.json` build script exists |
| Database migration issues | Migrations didn't run | Check Vercel build logs for errors |

## Local Testing

To test with environment variables locally:
```bash
cd backend
export SECRET_KEY="django-insecure-your-key-here"
export DATABASE_URL="postgresql://localhost/urlshorten"
export BASE_URL="http://localhost:8000"
export DEBUG="True"
python manage.py runserver
```

Test API:
```bash
curl -X POST http://localhost:8000/api/shorten/ \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://google.com"}'
```

Expected response:
```json
{
  "short_code": "abc123",
  "long_url": "https://google.com",
  "short_url": "http://localhost:8000/abc123"
}
```
