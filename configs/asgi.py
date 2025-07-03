"""
ASGI config for configs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

ENV_NAME = os.environ.get('ENV_NAME', 'development')

os.environ.setdefault(f'DJANGO_SETTINGS_MODULE', 'configs.settings.{ENV_NAME}')

application = get_asgi_application()
