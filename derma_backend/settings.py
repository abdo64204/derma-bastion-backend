"""
Django settings for derma_backend project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if present
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-5xdo@by#-yblt#smz7$80ay!ko=m#lp*&%#1)xf35)&36^ta$t'
)

# Debug mode: default to True in local development, can be set to False in .env
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

# Host configuration (supports comma-separated hosts in DJANGO_ALLOWED_HOSTS)
allowed_hosts_raw = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
if allowed_hosts_raw:
    ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_raw.split(',') if h.strip()]
else:
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '.pythonanywhere.com',
        '*',
    ]

# Application definition
INSTALLED_APPS = [
    # Jazzmin must be before django.contrib.admin
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party packages
    'rest_framework',
    'corsheaders',

    # Local apps
    'products',
    'orders',
    'store_settings',
    'contact',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'derma_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'derma_backend.wsgi.application'

# Database configuration: defaults to SQLite; supports MySQL (e.g. PythonAnywhere MySQL)
if os.environ.get('DB_ENGINE') == 'mysql' or os.environ.get('USE_MYSQL', 'False').lower() in ('true', '1'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', ''),
            'USER': os.environ.get('DB_USER', ''),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', ''),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Ensure directories exist
STATIC_ROOT.mkdir(parents=True, exist_ok=True)
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# PythonAnywhere reverse proxy SSL detection
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CORS configuration for Angular frontend
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'True').lower() in ('true', '1', 'yes')
CORS_ALLOW_CREDENTIALS = True

default_cors_origins = [
    'http://localhost:4200',
    'http://127.0.0.1:4200',
    'http://localhost:3000',
]
cors_origins_raw = os.environ.get('CORS_ALLOWED_ORIGINS', '')
if cors_origins_raw:
    CORS_ALLOWED_ORIGINS = default_cors_origins + [
        origin.strip() for origin in cors_origins_raw.split(',') if origin.strip()
    ]
else:
    CORS_ALLOWED_ORIGINS = default_cors_origins

# CSRF Trusted Origins (Essential for Django 4.x on HTTPS domains / PythonAnywhere admin login)
default_csrf_origins = [
    'https://*.pythonanywhere.com',
    'http://localhost:4200',
    'http://127.0.0.1:4200',
]
csrf_origins_raw = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if csrf_origins_raw:
    CSRF_TRUSTED_ORIGINS = default_csrf_origins + [
        origin.strip() for origin in csrf_origins_raw.split(',') if origin.strip()
    ]
else:
    CSRF_TRUSTED_ORIGINS = default_csrf_origins

# Jazzmin Dashboard Theme Configuration
JAZZMIN_SETTINGS = {
    # Title & Branding
    "site_title": "Derma Bastion Admin",
    "site_header": "Derma Bastion",
    "site_brand": "Derma Bastion",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Welcome to Derma Bastion Control Center",
    "copyright": "Derma Bastion Official",

    # Search bar in top navbar
    "search_model": ["orders.Order", "products.Product"],

    # User avatar
    "user_avatar": None,

    # Top Menu Links
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Storefront", "url": "http://localhost:4200", "new_window": True},
        {"name": "Store Config API", "url": "/api/store-config/", "new_window": True},
        {"model": "orders.Order"},
        {"model": "products.Product"},
    ],

    # Navigation sidebar
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["orders", "products", "store_settings", "contact", "auth"],

    # Custom Icons for models (Font Awesome 5 Free)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user-shield",
        "auth.Group": "fas fa-users",
        "products": "fas fa-spa",
        "products.Product": "fas fa-pump-soap",
        "orders": "fas fa-shopping-bag",
        "orders.Order": "fas fa-receipt",
        "orders.OrderItem": "fas fa-boxes",
        "store_settings": "fas fa-sliders-h",
        "store_settings.StoreSettings": "fas fa-cogs",
        "contact": "fas fa-headset",
        "contact.ContactMessage": "fas fa-envelope-open-text",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # UI Options
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-teal",
    "navbar": "navbar-dark navbar-teal",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-teal",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

