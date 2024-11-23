# build_files.sh
#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files into the correct directory for Vercel to serve
python manage.py collectstatic --noinput

# Run migrations if needed
python manage.py migrate --noinput
