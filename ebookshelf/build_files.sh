#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Move SQLite database to deployment folder
mkdir -p ./staticfiles/database
cp db.sqlite3 ./staticfiles/database/
