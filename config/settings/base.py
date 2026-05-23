from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    # Título de la ventana 
    "site_title": "Admin Kuyasqay",
    # Título de la pantalla de login
    "site_header": "Kuyasqay Pastelería",
    # Nombre de la marca (Arriba a la izquierda)
    "site_brand": "Kuyasqay",
    # Mensaje de bienvenida en el login
    "welcome_sign": "Bienvenida al panel de Kuyasqay",
    # Copyright en el footer
    "copyright": "Kuyasqay Pastelería",
    # Ocultar modelos específicos si es necesario (ej: Groups de auth)
    "hide_models": ["auth.Group"],
    # Iconos para el menú lateral (Usa iconos de FontAwesome)
    "icons": {
        "auth.user": "fas fa-user",
        "core.category": "fas fa-tags",
        "core.product": "fas fa-birthday-cake",
        "core.heroimage": "fas fa-images",
        "core.review": "fas fa-star",
    },
    # Orden del menú lateral
    "order_with_respect_to": ["core.product", "core.category", "core.heroimage", "core.review"],
    # Permite al administrador usar el "UI Builder"
    "show_ui_builder": True,
}