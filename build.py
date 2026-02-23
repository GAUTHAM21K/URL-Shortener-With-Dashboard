#!/usr/bin/env python
"""
Vercel build script for full-stack Django + React app.
This script is called by vercel.json's buildCommand.
"""

import subprocess
import sys
import os
import shutil

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return success status."""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check)
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Starting Vercel Build Process")
    print("=" * 60)
    
    # Step 1: Install backend dependencies
    print("\n[1/6] Installing backend dependencies...")
    if not run_command("pip install -r backend/requirements.txt"):
        print("Failed to install backend dependencies")
        return 1
    
    # Step 2: Build frontend
    print("\n[2/6] Installing frontend dependencies...")
    if not run_command("npm install", cwd="frontend"):
        print("Failed to install frontend dependencies")
        return 1
    
    print("\n[3/6] Building frontend...")
    if not run_command("npm run build", cwd="frontend"):
        print("Failed to build frontend")
        return 1
    
    # Step 3: Copy frontend to Django static files
    print("\n[4/6] Copying frontend build to Django staticfiles...")
    frontend_dist = "frontend/dist"
    django_static = "backend/staticfiles"
    
    # Create directory
    os.makedirs(django_static, exist_ok=True)
    
    # Copy files
    if os.path.exists(frontend_dist):
        for item in os.listdir(frontend_dist):
            src = os.path.join(frontend_dist, item)
            dst = os.path.join(django_static, item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        print(f"✓ Copied {frontend_dist} to {django_static}")
    else:
        print(f"Warning: {frontend_dist} not found")
    
    # Step 4: Run Django migrations
    print("\n[5/6] Running Django migrations...")
    if not run_command("python manage.py migrate --noinput", cwd="backend"):
        print("Failed to run migrations")
        return 1
    
    # Step 5: Collect static files
    print("\n[6/6] Collecting Django static files...")
    if not run_command("python manage.py collectstatic --noinput", cwd="backend"):
        print("Failed to collect static files")
        return 1
    
    print("\n" + "=" * 60)
    print("✓ Build completed successfully!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
