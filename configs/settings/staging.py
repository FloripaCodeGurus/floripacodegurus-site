from .base import *
from decouple import config

DEBUG = True  

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = ['floripacodegurus-staging.com',]

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
