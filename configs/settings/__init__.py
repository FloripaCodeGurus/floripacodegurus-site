import os

ENV_NAME = os.environ.get('ENV_NAME', 'development').lower()

if ENV_NAME == 'development':
    from .setting_development import *
elif ENV_NAME == 'homolog':
    from .setting_homolog import *
elif ENV_NAME == 'production':
    from .setting_production import *
else:
    raise ImportError(f'Unknown ENV_NAME: {ENV_NAME}')
