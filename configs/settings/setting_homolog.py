from .setting_base import *
from decouple import config

DEBUG = True  

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = [
    'fcgurus-homolog.herokuapp.com', # Aqui depende do domínio que tá hospedado
    '.herokuapp.com',
]

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
