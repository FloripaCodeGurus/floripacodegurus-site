# PostgreSQL RDS Deployment with GitHub Actions

This guide shows how to deploy and manage PostgreSQL RDS instances using GitHub Actions for your Django application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [RDS Instance Setup](#rds-instance-setup)
3. [GitHub Actions Configuration](#github-actions-configuration)
4. [Database Migration Strategy](#database-migration-strategy)
5. [Environment Configuration](#environment-configuration)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### AWS Resources Required
- AWS Account with appropriate permissions
- VPC with public and private subnets
- Security Groups configured
- IAM roles and policies

### Required AWS Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "rds:*",
                "ec2:DescribeVpcs",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeAvailabilityZones",
                "iam:PassRole"
            ],
            "Resource": "*"
        }
    ]
}
```

## RDS Instance Setup

### 1. Create RDS Subnet Group

```bash
# Create subnet group
aws rds create-db-subnet-group \
    --db-subnet-group-name floripacodegurus-subnet-group \
    --db-subnet-group-description "Subnet group for Floripa Code Gurus RDS" \
    --subnet-ids subnet-12345678 subnet-87654321
```

### 2. Create Security Group

```bash
# Create security group
aws ec2 create-security-group \
    --group-name floripacodegurus-rds-sg \
    --description "Security group for Floripa Code Gurus RDS" \
    --vpc-id vpc-12345678

# Add inbound rule for PostgreSQL
aws ec2 authorize-security-group-ingress \
    --group-id sg-12345678 \
    --protocol tcp \
    --port 5432 \
    --cidr 0.0.0.0/0
```

### 3. Create RDS Instance

```bash
# Create RDS instance
aws rds create-db-instance \
    --db-instance-identifier floripacodegurus-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.4 \
    --master-username floripacodegurus \
    --master-user-password YourSecurePassword123! \
    --allocated-storage 20 \
    --storage-type gp3 \
    --vpc-security-group-ids sg-12345678 \
    --db-subnet-group-name floripacodegurus-subnet-group \
    --backup-retention-period 7 \
    --multi-az \
    --storage-encrypted \
    --deletion-protection
```

## GitHub Actions Configuration

### 1. Create RDS Deployment Workflow

Create `.github/workflows/rds-deploy.yml`:

```yaml
name: Deploy PostgreSQL RDS

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        default: 'staging'
        type: choice
        options:
        - staging
        - production
      action:
        description: 'Action to perform'
        required: true
        default: 'create'
        type: choice
        options:
        - create
        - update
        - delete
        - backup
        - restore

jobs:
  rds-deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ secrets.AWS_REGION }}
    
    - name: Create RDS Instance
      if: github.event.inputs.action == 'create'
      run: |
        # Check if instance already exists
        if aws rds describe-db-instances --db-instance-identifier floripacodegurus-${{ github.event.inputs.environment }}-db 2>/dev/null; then
          echo "RDS instance already exists"
          exit 0
        fi
        
        # Create RDS instance
        aws rds create-db-instance \
          --db-instance-identifier floripacodegurus-${{ github.event.inputs.environment }}-db \
          --db-instance-class ${{ secrets.RDS_INSTANCE_CLASS }} \
          --engine postgres \
          --engine-version ${{ secrets.POSTGRES_VERSION }} \
          --master-username ${{ secrets.RDS_MASTER_USERNAME }} \
          --master-user-password ${{ secrets.RDS_MASTER_PASSWORD }} \
          --allocated-storage ${{ secrets.RDS_STORAGE_SIZE }} \
          --storage-type gp3 \
          --vpc-security-group-ids ${{ secrets.RDS_SECURITY_GROUP_ID }} \
          --db-subnet-group-name ${{ secrets.RDS_SUBNET_GROUP }} \
          --backup-retention-period ${{ secrets.RDS_BACKUP_RETENTION }} \
          --multi-az \
          --storage-encrypted \
          --deletion-protection \
          --tags Key=Environment,Value=${{ github.event.inputs.environment }} Key=Project,Value=FloripaCodeGurus
    
    - name: Wait for RDS Instance
      if: github.event.inputs.action == 'create'
      run: |
        echo "Waiting for RDS instance to be available..."
        aws rds wait db-instance-available --db-instance-identifier floripacodegurus-${{ github.event.inputs.environment }}-db
        echo "RDS instance is now available!"
    
    - name: Get RDS Endpoint
      id: get-endpoint
      run: |
        ENDPOINT=$(aws rds describe-db-instances \
          --db-instance-identifier floripacodegurus-${{ github.event.inputs.environment }}-db \
          --query 'DBInstances[0].Endpoint.Address' \
          --output text)
        echo "endpoint=$ENDPOINT" >> $GITHUB_OUTPUT
        echo "RDS Endpoint: $ENDPOINT"
    
    - name: Update Application Configuration
      if: github.event.inputs.action == 'create'
      run: |
        # Update environment variables in GitHub Secrets
        echo "RDS endpoint: ${{ steps.get-endpoint.outputs.endpoint }}"
        echo "Update your application's environment variables with:"
        echo "POSTGRES_HOST=${{ steps.get-endpoint.outputs.endpoint }}"
        echo "POSTGRES_DB=floripacodegurus_${{ github.event.inputs.environment }}"
        echo "POSTGRES_USER=${{ secrets.RDS_MASTER_USERNAME }}"
        echo "POSTGRES_PASSWORD=${{ secrets.RDS_MASTER_PASSWORD }}"
    
    - name: Create Database Backup
      if: github.event.inputs.action == 'backup'
      run: |
        # Create manual snapshot
        SNAPSHOT_ID="floripacodegurus-${{ github.event.inputs.environment }}-backup-$(date +%Y%m%d-%H%M%S)"
        aws rds create-db-snapshot \
          --db-instance-identifier floripacodegurus-${{ github.event.inputs.environment }}-db \
          --db-snapshot-identifier $SNAPSHOT_ID
        echo "Backup created: $SNAPSHOT_ID"
    
    - name: Delete RDS Instance
      if: github.event.inputs.action == 'delete'
      run: |
        # Remove deletion protection first
        aws rds modify-db-instance \
          --db-instance-identifier floripacodegurus-${{ github.event.inputs.environment }}-db \
          --no-deletion-protection \
          --apply-immediately
        
        # Delete the instance
        aws rds delete-db-instance \
          --db-instance-identifier floripacodegurus-${{ github.event.inputs.environment }}-db \
          --skip-final-snapshot
```

### 2. Create Database Migration Workflow

Create `.github/workflows/db-migrate.yml`:

```yaml
name: Database Migration

on:
  push:
    branches: [ main ]
    paths:
      - '**/migrations/**'
      - '**/models.py'
  workflow_dispatch:

jobs:
  migrate:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ secrets.AWS_REGION }}
    
    - name: Create database backup before migration
      run: |
        SNAPSHOT_ID="pre-migration-backup-$(date +%Y%m%d-%H%M%S)"
        aws rds create-db-snapshot \
          --db-instance-identifier floripacodegurus-production-db \
          --db-snapshot-identifier $SNAPSHOT_ID
        echo "Pre-migration backup created: $SNAPSHOT_ID"
    
    - name: Run database migrations
      run: |
        export DJANGO_SETTINGS_MODULE=configs.settings.production
        export POSTGRES_HOST=${{ secrets.POSTGRES_HOST }}
        export POSTGRES_DB=${{ secrets.POSTGRES_DB }}
        export POSTGRES_USER=${{ secrets.POSTGRES_USER }}
        export POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}
        export SECRET_KEY=${{ secrets.DJANGO_SECRET_KEY }}
        
        python manage.py migrate --noinput
        python manage.py collectstatic --noinput
    
    - name: Verify migration
      run: |
        export DJANGO_SETTINGS_MODULE=configs.settings.production
        export POSTGRES_HOST=${{ secrets.POSTGRES_HOST }}
        export POSTGRES_DB=${{ secrets.POSTGRES_DB }}
        export POSTGRES_USER=${{ secrets.POSTGRES_USER }}
        export POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}
        export SECRET_KEY=${{ secrets.DJANGO_SECRET_KEY }}
        
        python manage.py check --deploy
```

## Database Migration Strategy

### 1. Update Django Settings

Update `configs/settings/production.py`:

```python
from .base import *
from decouple import config
import dj_database_url

DEBUG = False
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# RDS Database Configuration
DATABASES = {
    'default': dj_database_url.parse(
        config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Alternative direct configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('POSTGRES_DB'),
#         'USER': config('POSTGRES_USER'),
#         'PASSWORD': config('POSTGRES_PASSWORD'),
#         'HOST': config('POSTGRES_HOST'),
#         'PORT': config('POSTGRES_PORT', '5432'),
#         'OPTIONS': {
#             'sslmode': 'require',
#         },
#     }
# }

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# HSTS settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Session security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 2. Update Docker Configuration

Update `docker-compose-production.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    restart: unless-stopped
    command: gunicorn configs.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
    ports:
      - "8000:8000"
    env_file:
      - .env.production
    environment:
      - DJANGO_SETTINGS_MODULE=configs.settings.production
      - ENV_NAME=production
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    networks:
      - app-network
    # Remove db dependency since we're using RDS
    # depends_on:
    #   - db

  # Remove local database service
  # db:
  #   image: postgres:15
  #   ...

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    networks:
      - app-network

volumes:
  static_volume:
  media_volume:

networks:
  app-network:
    driver: bridge
```

## Environment Configuration

### 1. GitHub Secrets for RDS

Add these secrets to your GitHub repository:

```
# AWS Configuration
AWS_ACCESS_KEY_ID: Your AWS Access Key
AWS_SECRET_ACCESS_KEY: Your AWS Secret Key
AWS_REGION: sa-east-1

# RDS Configuration
RDS_INSTANCE_CLASS: db.t3.micro
POSTGRES_VERSION: 15.4
RDS_MASTER_USERNAME: floripacodegurus
RDS_MASTER_PASSWORD: YourSecurePassword123!
RDS_STORAGE_SIZE: 20
RDS_SECURITY_GROUP_ID: sg-12345678
RDS_SUBNET_GROUP: floripacodegurus-subnet-group
RDS_BACKUP_RETENTION: 7

# Database Connection
DATABASE_URL: postgresql://username:password@host:port/database
POSTGRES_HOST: your-rds-endpoint.amazonaws.com
POSTGRES_DB: floripacodegurus_production
POSTGRES_USER: floripacodegurus
POSTGRES_PASSWORD: YourSecurePassword123!
POSTGRES_PORT: 5432

# Django Configuration
DJANGO_SECRET_KEY: your-secret-key
ALLOWED_HOSTS: yourdomain.com,www.yourdomain.com
```

### 2. Environment Variables Template

Create `.env.production.template`:

```bash
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration (RDS)
DATABASE_URL=postgresql://username:password@host:port/database
POSTGRES_HOST=your-rds-endpoint.amazonaws.com
POSTGRES_DB=floripacodegurus_production
POSTGRES_USER=floripacodegurus
POSTGRES_PASSWORD=your-secure-password
POSTGRES_PORT=5432

# Superuser Configuration
USER_NAME=JohnDoe
USER_EMAIL=administracao@floripacodegurus.com.br
USER_PASSWORD=JohnDoeSecurePassword#2025

# Environment
ENV_FILE=.env.production
DJANGO_SETTINGS_MODULE=configs.settings.production
```

## Monitoring and Maintenance

### 1. Create Monitoring Workflow

Create `.github/workflows/rds-monitor.yml`:

```yaml
name: RDS Monitoring

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  monitor:
    runs-on: ubuntu-latest
    
    steps:
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ secrets.AWS_REGION }}
    
    - name: Check RDS Status
      run: |
        aws rds describe-db-instances \
          --db-instance-identifier floripacodegurus-production-db \
          --query 'DBInstances[0].DBInstanceStatus' \
          --output text
    
    - name: Check Storage Usage
      run: |
        STORAGE=$(aws rds describe-db-instances \
          --db-instance-identifier floripacodegurus-production-db \
          --query 'DBInstances[0].AllocatedStorage' \
          --output text)
        echo "Allocated Storage: ${STORAGE}GB"
    
    - name: Check Backup Status
      run: |
        aws rds describe-db-snapshots \
          --db-instance-identifier floripacodegurus-production-db \
          --max-items 1 \
          --query 'DBSnapshots[0].Status' \
          --output text
```

### 2. Automated Backups

Create `.github/workflows/rds-backup.yml`:

```yaml
name: RDS Backup

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest
    
    steps:
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ secrets.AWS_REGION }}
    
    - name: Create Manual Snapshot
      run: |
        SNAPSHOT_ID="daily-backup-$(date +%Y%m%d-%H%M%S)"
        aws rds create-db-snapshot \
          --db-instance-identifier floripacodegurus-production-db \
          --db-snapshot-identifier $SNAPSHOT_ID
        echo "Backup created: $SNAPSHOT_ID"
    
    - name: Clean Old Snapshots
      run: |
        # Delete snapshots older than 30 days
        aws rds describe-db-snapshots \
          --db-instance-identifier floripacodegurus-production-db \
          --query 'DBSnapshots[?SnapshotCreateTime<`'$(date -d '30 days ago' -u +%Y-%m-%dT%H:%M:%S.000Z)'`].DBSnapshotIdentifier' \
          --output text | xargs -I {} aws rds delete-db-snapshot --db-snapshot-identifier {}
```

## Troubleshooting

### Common Issues

#### 1. RDS Instance Creation Failed
```bash
# Check VPC and subnet configuration
aws ec2 describe-vpcs
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-12345678"

# Check security group
aws ec2 describe-security-groups --group-ids sg-12345678
```

#### 2. Connection Timeout
```bash
# Check security group rules
aws ec2 describe-security-groups --group-ids sg-12345678

# Test connection from EC2
psql -h your-rds-endpoint.amazonaws.com -U floripacodegurus -d floripacodegurus_production
```

#### 3. Migration Failures
```bash
# Check database connectivity
python manage.py dbshell

# Check migration status
python manage.py showmigrations

# Rollback migration
python manage.py migrate app_name previous_migration_number
```

### Useful Commands

```bash
# List RDS instances
aws rds describe-db-instances

# Get RDS endpoint
aws rds describe-db-instances --db-instance-identifier floripacodegurus-production-db --query 'DBInstances[0].Endpoint.Address' --output text

# Check RDS status
aws rds describe-db-instances --db-instance-identifier floripacodegurus-production-db --query 'DBInstances[0].DBInstanceStatus' --output text

# List snapshots
aws rds describe-db-snapshots --db-instance-identifier floripacodegurus-production-db

# Modify RDS instance
aws rds modify-db-instance --db-instance-identifier floripacodegurus-production-db --db-instance-class db.t3.small --apply-immediately
```

## Security Best Practices

1. **Use IAM Database Authentication** when possible
2. **Enable encryption at rest** and in transit
3. **Use VPC security groups** to restrict access
4. **Regular security updates** and patches
5. **Monitor access logs** and unusual activity
6. **Use strong passwords** and rotate them regularly
7. **Enable automated backups** with appropriate retention
8. **Use Multi-AZ deployment** for high availability

---

**Last Updated:** January 2025
**Version:** 1.0
