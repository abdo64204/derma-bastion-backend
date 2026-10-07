# 🚀 PythonAnywhere Deployment Guide - Derma Bastion Backend

This guide outlines the exact, step-by-step process for deploying the **Derma Bastion Django REST API** to **PythonAnywhere**.

---

## 📋 Overview of Setup

| Component | Value on PythonAnywhere |
| :--- | :--- |
| **Python Version** | Python 3.10 |
| **Project Directory** | `/home/<your-username>/derma-bastion-backend` |
| **Virtualenv Directory** | `/home/<your-username>/.virtualenvs/derma-bastion` |
| **Static URL / Path** | `/static/` → `/home/<your-username>/derma-bastion-backend/staticfiles` |
| **Media URL / Path** | `/media/` → `/home/<your-username>/derma-bastion-backend/media` |
| **WSGI File** | `/var/www/<your-username>_pythonanywhere_com_wsgi.py` |

*(Replace `<your-username>` with your actual PythonAnywhere username)*

---

## Step 1: Clone Repository on PythonAnywhere

1. Log in to your [PythonAnywhere Dashboard](https://www.pythonanywhere.com/).
2. Go to the **Consoles** tab and start a **Bash** console.
3. Clone your repository:
   ```bash
   git clone https://github.com/abdo64204/derma-bastion-backend.git
   cd derma-bastion-backend
   ```

---

## Step 2: Create Virtual Environment & Install Dependencies

In the same Bash console, run:

```bash
# Create a dedicated virtual environment with Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 derma-bastion

# Verify virtual environment is active (prompt should show (derma-bastion))
# Install all required packages
pip install -r requirements.txt
```

---

## Step 3: Create & Configure `.env` File

Create your production environment file from the template:

```bash
cp .env.example .env
nano .env
```

Edit the values in `.env`:
```ini
DJANGO_SECRET_KEY=replace-with-a-random-secure-secret-key-32chars
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<your-username>.pythonanywhere.com,localhost,127.0.0.1

# Enable CORS for your storefront frontend:
CORS_ALLOW_ALL_ORIGINS=True
CSRF_TRUSTED_ORIGINS=https://<your-username>.pythonanywhere.com,http://localhost:4200

# Default Admin Credentials
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=YourSecurePassword123!
DJANGO_SUPERUSER_EMAIL=admin@dermabastion.com
```

*Press `Ctrl + O` then `Enter` to save, and `Ctrl + X` to exit nano.*

---

## Step 4: Run Initial Migrations, Static Files & Data Seeding

You can run our automated deployment script:
```bash
bash deploy_pythonanywhere.sh
```

Or run the commands manually:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py init_admin
python manage.py seed_products
```

---

## Step 5: Configure the Web App in PythonAnywhere

1. Go to the **Web** tab in PythonAnywhere.
2. Click **Add a new web app**.
3. Choose **Manual configuration** (do **not** select the Django wizard; manual configuration gives you full control over your virtualenv and repository).
4. Select **Python 3.10**.

### 5.1 Set Paths
In the Web tab, scroll to the **Code** section and set:
- **Source code**: `/home/<your-username>/derma-bastion-backend`
- **Working directory**: `/home/<your-username>/derma-bastion-backend`

### 5.2 Set Virtualenv
In the **Virtualenv** section:
- Enter: `/home/<your-username>/.virtualenvs/derma-bastion`

### 5.3 Configure WSGI Configuration File
In the **Code** section, click on the WSGI configuration file link:
`/var/www/<your-username>_pythonanywhere_com_wsgi.py`

Delete all default code and replace it with:
```python
import os
import sys
from dotenv import load_dotenv

# REPLACE THIS WITH YOUR ACTUAL PYTHONANYWHERE USERNAME:
PA_USERNAME = '<your-username>'

# Project directory on PythonAnywhere
PROJECT_DIR = f'/home/{PA_USERNAME}/derma-bastion-backend'

# Add the project directory to Python's search path
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Load environment variables from .env
env_file = os.path.join(PROJECT_DIR, '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'derma_backend.settings'

# Initialize Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(Make sure to replace `<your-username>` on line 6 with your actual username)*
Click **Save** at the top right.

### 5.4 Configure Static and Media Files (Crucial for Admin Styles & Images)
Scroll down to the **Static files** table in the Web tab and add two rows:

| URL | Directory |
| :--- | :--- |
| `/static/` | `/home/<your-username>/derma-bastion-backend/staticfiles` |
| `/media/` | `/home/<your-username>/derma-bastion-backend/media` |

---

## Step 6: Reload & Verify

1. Go back to the top of the **Web** tab and click the big green **Reload <your-username>.pythonanywhere.com** button.
2. Test your endpoints in your browser:
   - **Health Check**: `https://<your-username>.pythonanywhere.com/` (returns API JSON status)
   - **Admin Portal**: `https://<your-username>.pythonanywhere.com/admin/`
   - **Products API**: `https://<your-username>.pythonanywhere.com/api/products/`
   - **Store Config API**: `https://<your-username>.pythonanywhere.com/api/store-config/`

---

## Step 7: Connect Angular Frontend to PythonAnywhere API

In your Angular frontend project (`derma-bastion-frontend`):

In `src/environments/environment.prod.ts` (or your API config):
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://<your-username>.pythonanywhere.com/api',
  mediaUrl: 'https://<your-username>.pythonanywhere.com'
};
```

---

## 🔄 Updating Your Backend in the Future

Whenever you push new code to GitHub, update PythonAnywhere in seconds:

1. Open a Bash console on PythonAnywhere.
2. Run:
   ```bash
   cd ~/derma-bastion-backend
   bash deploy_pythonanywhere.sh
   ```
*(The script pulls changes, installs dependencies, runs migrations, collects static files, and reloads your web app automatically).*

---

## 🛠 Troubleshooting & FAQs

### 1. `403 Forbidden: CSRF verification failed` on Admin Login
- Make sure `CSRF_TRUSTED_ORIGINS` in your `.env` contains:
  `CSRF_TRUSTED_ORIGINS=https://<your-username>.pythonanywhere.com`
- Reload the web app after updating `.env`.

### 2. Django Admin has no styling (plain unstyled HTML)
- Ensure you ran `python manage.py collectstatic --noinput`.
- Ensure the `/static/` row in the PythonAnywhere **Static files** table points to `/home/<your-username>/derma-bastion-backend/staticfiles`.

### 3. Uploaded Receipts or Images 404
- Ensure the `/media/` row in the PythonAnywhere **Static files** table points to `/home/<your-username>/derma-bastion-backend/media`.

### 4. 500 Internal Server Error
- In the PythonAnywhere Web tab, scroll down to the **Log files** section.
- Click on **Error log**: `/var/log/<your-username>.pythonanywhere.com.error.log` to inspect the exact traceback.
