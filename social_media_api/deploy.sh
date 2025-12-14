#!/bin/bash

# Deployment script for Social Media API

echo "🚀 Starting deployment process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if not exists (for development)
echo "👤 Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

echo "✅ Deployment preparation complete!"
echo "🔧 Start the server with: python manage.py runserver"
