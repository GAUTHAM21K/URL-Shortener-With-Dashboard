#!/bin/bash
# Build script for Vercel - runs migrations
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
cd ..
