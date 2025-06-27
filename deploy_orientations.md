
# Run docker-compose
    - docker-compose -f docker-compose-local.yml up -d --build (local)

# To clean memory
    - docker-compose -f docker-compose-local.yml down -v (local)

# Docker logs
    -  docker logs -f floripacodegurus-site-web-1   

# To create and test superuser creation

## Enabling file
    - chmod +x create_superuser.sh\

## Ensure your .env file contains
    - USER_NAME="Your Name"
    - USER_EMAIL="your@email.com"
    - USER_PASSWORD="yourpassword"

- Run the script:
./create_superuser.sh


# Applying mmigrations for users
    - python3 manage.py makemigrations users
    - python3 manage.py migrate users

# To reset database in case migration error
    - rm db.sqlite3