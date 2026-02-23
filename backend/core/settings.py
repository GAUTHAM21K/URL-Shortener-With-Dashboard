import dj_database_url
import os

# Allow Vercel domains
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.vercel.app']

# Use Neon Database URL from environment variables
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# Update WSGI for Vercel
WSGI_APPLICATION = 'core.wsgi.application'