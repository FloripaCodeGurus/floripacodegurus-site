#!/bin/bash

# Load environment variables from .env
set -a
source .env
set +a

# Check required variables
if [[ -z "$USER_EMAIL" || -z "$USER_PASSWORD" || -z "$USER_NAME" ]]; then
  echo "USER_EMAIL, USER_PASSWORD, and USER_NAME must be set in .env"
  exit 1
fi

# Split USER_NAME into first and last name (if possible)
FIRST_NAME=$(echo "$USER_NAME" | awk '{print $1}')
LAST_NAME=$(echo "$USER_NAME" | awk '{print $2}')
if [[ -z "$LAST_NAME" ]]; then
  LAST_NAME="Admin"
fi

# Run Django shell to create the superuser
python manage.py shell <<EOF
from users.models import CustomUser
if not CustomUser.objects.filter(email="$USER_EMAIL").exists():
    CustomUser.objects.create_superuser(
        email="$USER_EMAIL",
        password="$USER_PASSWORD",
        first_name="$FIRST_NAME",
        last_name="$LAST_NAME",
        phone_number="0000000000"
    )
    print("Superuser created.")
else:
    print("Superuser already exists.")
EOF