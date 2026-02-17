from .base import *

SECRET_KEY = 'django-insecure-lq5%@s8!h$(l9-tjl)7^sdsez8$5m1ztw5*ybo4an7i9@qsxa7'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'