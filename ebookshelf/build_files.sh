#!/bin/bash

# Install dependencies (from requirements.txt)
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations (optional if you want to ensure DB schema is up-to-date)
echo "Running migrations..."
python manage.py migrate --noinput

# Ensure any environment variables are set for the build process (optional)
# If you're using .env file or other secret management methods, you can load them here
echo "Setting up environment variables..."
export $(cat .env | xargs)

# If you need to execute additional commands like database backup, you can add them here

echo "Build process completed successfully!"
