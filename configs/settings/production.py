from fcgurus_site.settings.base import *

DEBUG = False

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = ['fcgurus-production.herokuapp.com', '.herokuapp.com']

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

