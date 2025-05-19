from fcgurus_site.settings.base import *

DEBUG = True

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = ['localhost','127.0.0.1:8000']

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

