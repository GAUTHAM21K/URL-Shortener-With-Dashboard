#!/bin/bash
# Vercel build script for full-stack Django + React app

echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Copying frontend build to Django static folder..."
mkdir -p backend/staticfiles
cp -r frontend/dist/* backend/staticfiles/ || true

echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "Running Django migrations..."
cd backend
python manage.py migrate
python manage.py collectstatic --noinput
cd ..

echo "Build complete!"
