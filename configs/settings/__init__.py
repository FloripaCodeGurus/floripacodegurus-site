import os
from decouple import config

print("🔍 DEBUG: __init__.py está sendo carregado!")
print("🔍 DEBUG: Variáveis de ambiente relevantes:")
print(f"🔍 ENV_NAME = '{os.environ.get('ENV_NAME', 'NÃO ENCONTRADA')}'")
print(f"🔍 SECRET_KEY = '{os.environ.get('SECRET_KEY', 'NÃO ENCONTRADA')}'")
print(f"🔍 POSTGRES_DB = '{os.environ.get('POSTGRES_DB', 'NÃO ENCONTRADA')}'")

ENV_NAME = os.environ.get('ENV_NAME', 'development').lower()

print(f"🔍 DEBUG: ENV_NAME final = '{ENV_NAME}'")

if ENV_NAME == 'development':
    print("🔍 DEBUG: Carregando setting_development")
    from .setting_development import *
elif ENV_NAME == 'homolog':
    print("🔍 DEBUG: Carregando setting_homolog")
    from .setting_homolog import *
elif ENV_NAME == 'production':
    print("🔍 DEBUG: Carregando setting_production")
    from .setting_production import *
else:
    print(f"🔍 DEBUG: ENV_NAME desconhecido: '{ENV_NAME}'")
    raise ImportError(f'Unknown ENV_NAME: {ENV_NAME}')

print("🔍 DEBUG: __init__.py terminou de carregar")
