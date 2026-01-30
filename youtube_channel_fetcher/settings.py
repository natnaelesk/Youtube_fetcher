import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

allowed_hosts = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')
if 'youtube-fetcher.fly.dev' not in allowed_hosts:
    allowed_hosts.append('youtube-fetcher.fly.dev')
ALLOWED_HOSTS = allowed_hosts

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'videos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'youtube_channel_fetcher.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'youtube_channel_fetcher.wsgi.application'

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = 'static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'EXCEPTION_HANDLER': 'videos.views.custom_exception_handler',
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://youtube-fetcher.vercel.app",
]

vercel_url = os.getenv('VERCEL_URL')
if vercel_url:
    if not vercel_url.startswith('http'):
        vercel_url = f"https://{vercel_url}"
    if vercel_url not in CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append(vercel_url)

frontend_url = os.getenv('FRONTEND_URL')
if frontend_url:
    if not frontend_url.startswith('http'):
        frontend_url = f"https://{frontend_url}"
    if frontend_url not in CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append(frontend_url)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
YOUTUBE_API_BASE_URL = 'https://www.googleapis.com/youtube/v3'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'youtube-cache',
    }
}

CACHE_TIMEOUT = 600
