"""
ASGI config for configs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

ENV_NAME = os.environ.get('ENV_NAME', 'development')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'configs.settings.setting_{ENV_NAME}')

application = get_asgi_application()
