
#!/usr/bin/env bash
set -o errexit

# Install system dependencies required for Pillow
apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev

# Install Python dependencies
pip install -r requirements.txt

# Django setup
python manage.py collectstatic --noinput
python manage.py migrate
