import os
import sys
from .base import *
from decouple import config

# Environment settings
ENVIRONMENT = os.environ.get('ENV_NAME', 'development') 
IS_DEVELOPMENT = ENVIRONMENT == 'development'
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)
SECRET_KEY = config("DJANGO_SECRET_KEY", default="dev-secret-key")
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='localhost').split(',')
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = None

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST', 'localhost'),
        'PORT': config('POSTGRES_PORT', '5434'),
    }
}

#  Logging Configuration
if IS_DEVELOPMENT:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'stream': sys.stdout,
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                'stream': sys.stdout,
            },
            'error_file': {
                'level': 'ERROR',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                'stream': sys.stderr,
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['error_file'],
                'level': 'ERROR',
                'propagate': False,
            },
            'app_files': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'users': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
else:
    # LOCAL logging configuration (using FileHandler)
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(LOGS_DIR, 'django.log'),
                'formatter': 'verbose',
            },
            'error_file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': os.path.join(LOGS_DIR, 'error.log'),
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['error_file'],
                'level': 'ERROR',
                'propagate': False,
            },
            'app_files': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'users': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
