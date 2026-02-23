import dj_database_url
import os

# Allow Vercel domains
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.vercel.app']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Add these three
    'rest_framework',
    'corsheaders',
    'shortener', 
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Keep this at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# Use Neon Database URL from environment variables
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        ssl_require=True if os.environ.get('DATABASE_URL') else False
    )
}

# Update WSGI for Vercel
WSGI_APPLICATION = 'core.wsgi.application'

# Allow all subdomains of vercel and localhost
ALLOWED_HOSTS = ['*'] 

# This is critical for POST requests (Shortening)
CSRF_TRUSTED_ORIGINS = [
    "https://url-shortener-with-dashboard.vercel.app",
    "https://*.vercel.app"
]

# Ensure CORS is wide open for your frontend
CORS_ALLOW_ALL_ORIGINS = True