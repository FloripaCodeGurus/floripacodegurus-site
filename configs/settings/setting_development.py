from .setting_base import *
from decouple import config

DEBUG = True

SECRET_KEY = config("SECRET_KEY", default="dev-secret-key")

ALLOWED_HOSTS = ['localhost','127.0.0.1']

SECURE_SSL_REDIRECT = False

SECURE_PROXY_SSL_HEADER = None

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

