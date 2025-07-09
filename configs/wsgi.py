"""
WSGI config for configs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

ENV_NAME = env_name =  os.environ.get('ENV_NAME', 'development')

if env_name == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings.production')
elif env_name == 'staging':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings.staging')
elif env_name == 'development':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings.local')


application = get_wsgi_application()
