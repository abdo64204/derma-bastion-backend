#!/usr/bin/env bash
# ==============================================================================
# Derma Bastion Backend - PythonAnywhere Deployment & Update Script
# ==============================================================================
# Usage:
#   cd ~/derma-bastion-backend
#   bash deploy_pythonanywhere.sh
# ==============================================================================

set -e

echo "🚀 [1/6] Pulling latest changes from GitHub..."
git pull origin main

# Find and activate virtualenv if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f "$HOME/.virtualenvs/derma-bastion/bin/activate" ]; then
        echo "🐍 Activating virtualenv ~/.virtualenvs/derma-bastion..."
        source "$HOME/.virtualenvs/derma-bastion/bin/activate"
    elif [ -f "./.venv/bin/activate" ]; then
        echo "🐍 Activating virtualenv ./.venv..."
        source "./.venv/bin/activate"
    else
        echo "⚠️  No virtualenv active. Please activate your virtualenv or create one with:"
        echo "    mkvirtualenv --python=python3.10 derma-bastion"
    fi
fi

echo "📦 [2/6] Installing dependencies..."
pip install -r requirements.txt

echo "🔄 [3/6] Applying database migrations..."
python manage.py migrate

echo "🎨 [4/6] Collecting static files..."
python manage.py collectstatic --noinput

echo "👤 [5/6] Ensuring default admin superuser exists..."
python manage.py init_admin

echo "🌱 Checking if products should be seeded..."
python manage.py seed_products

echo "🔄 [6/6] Reloading PythonAnywhere Web App..."
# Find and touch the WSGI file to trigger automatic reload
WSGI_FILE=$(ls /var/www/*_wsgi.py 2>/dev/null | head -n 1 || true)
if [ -n "$WSGI_FILE" ]; then
    touch "$WSGI_FILE"
    echo "✅ Touched $WSGI_FILE to trigger automatic reload!"
else
    echo "ℹ️  Remember to click 'Reload' in the PythonAnywhere Web tab."
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo "👉 Check your Django Admin at: https://<your-username>.pythonanywhere.com/admin/"
echo "👉 Check your API at:          https://<your-username>.pythonanywhere.com/api/products/"
