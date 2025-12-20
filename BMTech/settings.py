import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")

# En développement local, DEBUG doit être True pour que runserver serve les fichiers statiques
DEBUG = True

ALLOWED_HOSTS = [
    '197a30db-7379-43fc-b739-5b80edc59cb3-00-3bzgg87jtxu2u.riker.replit.dev',
    '.replit.dev',  # Autorise tous les sous-domaines Replit
    'localhost',
    '127.0.0.1',
    '192.168.1.136'
]

CSRF_TRUSTED_ORIGINS = [
    'https://197a30db-7379-43fc-b739-5b80edc59cb3-00-3bzgg87jtxu2u.riker.replit.dev',
    'https://*.replit.dev',  # Important pour Replit
]
CSRF_TRUSTED_ORIGINS = ['https://197a30db-7379-43fc-b739-5b80edc59cb3-00-3bzgg87jtxu2u.riker.replit.dev']



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Gestion_panel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Gestion_panel.middleware.AuthMiddleware',
]

ROOT_URLCONF = 'BMTech.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Gestion_panel.context_processors.current_user',
            ],
        },
    },
]

WSGI_APPLICATION = 'BMTech.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
