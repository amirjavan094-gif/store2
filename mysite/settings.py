"""
Django settings for mysite project.
"""

from pathlib import Path
import os
import dj_database_url

# --- Base paths ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security ---
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-cx6m$rcfr2m9x6(fyd#3o=euia05$0e4oe70(1ml#jh*e^&eti"
)
DEBUG = os.environ.get("DEBUG", "True") == "True"

# ✅ لوکال و Render هر دو را مجاز کنیم
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "store2-1-v667.onrender.com"
]

# --- Installed Apps ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'django.contrib.humanize',
    'cart',
    'payment',
    'cloudinary',
    'cloudinary_storage',
    'rest_framework',
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

# --- Templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'mysite' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processor.cart',
                'cart.context_processor.categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# --- Database ---
if DEBUG:
    # ✅ حالت لوکال: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # ✅ حالت دیپلوی: PostgreSQL Render
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'store2db'),
            'USER': os.environ.get('DB_USER', 'store2db_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'VZIKIkzGBw3FEPKPvsrg9AixCzy5thwL'),
            'HOST': os.environ.get('DB_HOST', 'dpg-d3hohke3jp1c73fn8m20-a.oregon-postgres.render.com'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = []

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# --- Static & Media ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Cloudinary ---
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_URL = os.environ.get(
    'CLOUDINARY_URL',
    'cloudinary://API_KEY:API_SECRET@CLOUD_NAME'
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
