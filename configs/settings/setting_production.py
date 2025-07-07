from .setting_base import *
from decouple import config

DEBUG = False

print("🚀 PRODUCTION SETTINGS LOADED - DEBUG should be False!")
print(f"🚀 DEBUG = {DEBUG}")

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = ['fcgurus-production.herokuapp.com', '.herokuapp.com']

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST', 'localhost'),
        'PORT': config('POSTGRES_PORT', '5432'),
    }
}

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

