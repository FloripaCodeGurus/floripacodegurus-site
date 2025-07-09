#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Default to the base settings module
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agilfileconfig.settings')

    # Load the environment variable for the settings module
    env_name = os.environ.get('ENV_NAME', 'development').lower()

    if env_name == 'production':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'configs.settings.production'
    elif env_name == 'staging':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'configs.settings.staging'
    elif env_name == 'development':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'configs.settings.development'
    elif env_name == 'local':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'configs.settings.local'
    else:
        print(f"Unknown ENV_NAME: {env_name}. Defaulting to dev settings.")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
