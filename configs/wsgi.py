"""
WSGI config for configs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

ENV_NAME = os.environ.get('ENV_NAME', 'development')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'configs.settings.setting_{ENV_NAME}')

application = get_wsgi_application()
