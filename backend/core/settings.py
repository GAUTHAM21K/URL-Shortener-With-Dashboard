# 1. Add your Vercel domain to allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'url-shortener-with-dashboard.vercel.app']

# 2. Configure CORS to allow your Vercel frontend
CORS_ALLOWED_ORIGINS = [
    "https://url-shortener-with-dashboard.vercel.app",
]

# Or, for the deployment phase to be safe:
CORS_ALLOW_ALL_ORIGINS = True 

# 3. Ensure CSRF is also handled for your domain
# 1. Add your Vercel URL to allowed hosts
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    'url-shortener-with-dashboard.vercel.app', # Your Vercel domain
    '.vercel.app' # Allow all vercel subdomains
]

# 2. Allow CORS from your frontend
CORS_ALLOWED_ORIGINS = [
    "https://url-shortener-with-dashboard.vercel.app",
]

# 3. Trust the domain for POST requests
CSRF_TRUSTED_ORIGINS = [
    "https://url-shortener-with-dashboard.vercel.app",
]