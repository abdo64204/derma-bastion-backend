# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PythonAnywhere WSGI Configuration for Derma Bastion Backend
#
# INSTRUCTIONS:
# 1. In your PythonAnywhere Web tab, click on the WSGI configuration file link:
#    /var/www/<your-username>_pythonanywhere_com_wsgi.py
# 2. Delete the default boilerplate and paste the contents of this file.
# 3. Replace 'YOUR_USERNAME' with your actual PythonAnywhere username.
# 4. Save the file and click "Reload" on the Web tab!
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
import sys
from dotenv import load_dotenv

# PythonAnywhere username:
PA_USERNAME = 'abdelrahman64204'

# Project directory on PythonAnywhere
PROJECT_DIR = f'/home/{PA_USERNAME}/derma-bastion-backend'

# Add the project directory to Python's search path
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Load environment variables from /home/<username>/derma-bastion-backend/.env
env_file = os.path.join(PROJECT_DIR, '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)

# Point to Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'derma_backend.settings'

# Initialize Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
