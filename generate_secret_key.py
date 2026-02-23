#!/usr/bin/env python
"""Generate a SECRET_KEY for Django and print environment variable setup."""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from django.core.management.utils import get_random_secret_key
    secret_key = get_random_secret_key()
    print("\n" + "="*70)
    print("Django SECRET_KEY generated successfully!")
    print("="*70)
    print("\nCopy this value and add it to Vercel Environment Variables:\n")
    print(f"SECRET_KEY={secret_key}\n")
    print("="*70)
    print("\nAlso set these environment variables in Vercel Dashboard:\n")
    print("1. SECRET_KEY: <the key above>")
    print("2. DATABASE_URL: postgresql://user:password@host:port/database?sslmode=require")
    print("3. BASE_URL: https://your-app.vercel.app")
    print("4. DEBUG: False")
    print("="*70 + "\n")
except ImportError:
    print("Django is not installed. Please install it first:")
    print("pip install -r backend/requirements.txt")
    sys.exit(1)
