# Floripa Code Gurus - Deployment Manual

This manual provides comprehensive instructions for deploying the Floripa Code Gurus Django application to AWS EC2 using Docker and GitHub Actions.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [AWS EC2 Setup](#aws-ec2-setup)
3. [GitHub Actions Configuration](#github-actions-configuration)
4. [Manual Deployment](#manual-deployment)
5. [Troubleshooting](#troubleshooting)
6. [Maintenance](#maintenance)

## Prerequisites

### Required Tools
- AWS CLI configured with appropriate permissions
- Docker and Docker Compose installed locally
- Git configured with SSH keys
- Access to GitHub repository

### AWS Resources Needed
- EC2 instance (Amazon Linux 2023)
- Security Group with appropriate ports
- Key Pair for SSH access

## AWS EC2 Setup

### 1. Launch EC2 Instance

1. **Instance Configuration:**
   - AMI: Amazon Linux 2023
   - Instance Type: t3.micro (minimum) or t3.small (recommended)
   - Storage: 20GB GP3 (minimum)

2. **Security Group Configuration:**
   ```
   Inbound Rules:
   - SSH (22): Your IP
   - HTTP (80): 0.0.0.0/0
   - HTTPS (443): 0.0.0.0/0
   - Custom (8000): 0.0.0.0/0 (for testing)
   ```

3. **Key Pair:**
   - Create or use existing key pair
   - Download the `.pem` file
   - Set proper permissions: `chmod 400 your-key.pem`

### 2. Connect to EC2 Instance

```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

### 3. Install Required Software

```bash
# Update system
sudo dnf update -y

# Install Docker
sudo dnf install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo dnf install -y git

# Install unzip
sudo dnf install -y unzip

# Logout and login again to apply group changes
exit
```

### 4. Create Application Directory

```bash
# Create application directory
sudo mkdir -p /opt/floripacodegurus
sudo chown -R ec2-user:ec2-user /opt/floripacodegurus
cd /opt/floripacodegurus
```

## GitHub Actions Configuration

### 1. Repository Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

#### Required Secrets:
```
AWS_ACCESS_KEY_ID: Your AWS Access Key ID
AWS_SECRET_ACCESS_KEY: Your AWS Secret Access Key
AWS_REGION: sa-east-1
EC2_HOST: ec2-54-94-54-29.sa-east-1.compute.amazonaws.com
EC2_USERNAME: ec2-user
EC2_SSH_KEY: Your private key content (see format below)
DJANGO_SECRET_KEY: Your Django secret key
USER_NAME: JohnDoe
USER_EMAIL: youremail@.com
USER_PASSWORD: YourSecurePassword#2025
```

#### SSH Key Format for EC2_SSH_KEY:
```
Add your private key content here. The key should be in OpenSSH format and include:
- -----BEGIN PRIVATE KEY-----
- Your private key content
- -----END PRIVATE KEY-----

Note: Keep your private key secure and never commit it to version control.
```

### 2. Workflow Configuration

The deployment workflow is already configured in `.github/workflows/deploy.yml`. It will:

1. Run tests on every push to `main` branch
2. Deploy automatically when tests pass
3. Create deployment package with all necessary files
4. Deploy to EC2 using SSH

## Manual Deployment

### 1. Prepare Deployment Package

```bash
# Clone repository
git clone https://github.com/your-username/floripacodegurus-site.git
cd floripacodegurus-site

# Create deployment directory
mkdir -p deployment

# Copy necessary files
cp -r escola tutoriais users newsletter configs manage.py requirements.txt Dockerfile docker-entrypoint.sh deployment/
cp docker-compose-production.yml deployment/
cp -r staticfiles deployment/ 2>/dev/null || echo "No staticfiles directory found"

# Create .env.production file
cat > deployment/.env.production << EOF
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database configuration
POSTGRES_DB=your_batabase_name
POSTGRES_USER=your_batabase_user_name
POSTGRES_PASSWORD=your-secure-password

# Superuser configuration
USER_NAME=JohnDoe
USER_EMAIL=youremail@.com
USER_PASSWORD=YourSecurePassword#2025

# Environment
ENV_FILE=.env.production
DJANGO_SETTINGS_MODULE=configs.settings.production
EOF

# Create deployment script
cat > deployment/deploy.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Starting deployment..."

# Stop existing containers
docker-compose -f docker-compose-production.yml down || true

# Remove old images
docker system prune -f || true

# Build and start new containers
docker-compose -f docker-compose-production.yml up -d --build

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 30

# Run migrations
echo "📊 Running database migrations..."
docker-compose -f docker-compose-production.yml exec -T web python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
docker-compose -f docker-compose-production.yml exec -T web python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
docker-compose -f docker-compose-production.yml exec -T web ./docker-entrypoint.sh || true

echo "✅ Deployment completed successfully!"
EOF

chmod +x deployment/deploy.sh

# Create zip file
cd deployment && zip -r ../deployment.zip . && cd ..
```

### 2. Upload to EC2

```bash
# Upload deployment package
scp -i your-key.pem deployment.zip ec2-user@your-ec2-public-ip:/opt/floripacodegurus/

# Connect to EC2
ssh -i your-key.pem ec2-user@your-ec2-public-ip

# Navigate to application directory
cd /opt/floripacodegurus

# Extract deployment package
unzip -o deployment.zip

# Run deployment
chmod +x deploy.sh
./deploy.sh
```

### 3. Verify Deployment

```bash
# Check running containers
docker-compose -f docker-compose-production.yml ps

# Check logs
docker-compose -f docker-compose-production.yml logs web

# Test application
curl http://localhost:8000/
```

## Troubleshooting

### Common Issues

#### 1. SSH Authentication Failed
```
Error: ssh: handshake failed: ssh: unable to authenticate
```

**Solution:**
- Verify `EC2_USERNAME` is set to `ec2-user`
- Check `EC2_SSH_KEY` format (must include `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----`)
- Ensure private key has correct permissions

#### 2. AWS Credentials Error
```
Error: The request signature we calculated does not match the signature you provided
```

**Solution:**
- Verify `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are correct
- Check `AWS_REGION` is set to `sa-east-1`

#### 3. Docker Build Failed
```
Error: failed to build Docker image
```

**Solution:**
- Check Dockerfile syntax
- Verify all files are copied correctly
- Check requirements.txt for dependency issues

#### 4. Database Connection Error
```
Error: could not connect to server
```

**Solution:**
- Verify database credentials in `.env.production`
- Check if PostgreSQL container is running
- Wait longer for database to initialize

#### 5. Static Files Not Found
```
Error: 404 for static files
```

**Solution:**
- Run `python manage.py collectstatic --noinput`
- Check static files volume mounting
- Verify nginx configuration

### Debugging Commands

```bash
# Check container logs
docker-compose -f docker-compose-production.yml logs -f web

# Check container status
docker-compose -f docker-compose-production.yml ps

# Access container shell
docker-compose -f docker-compose-production.yml exec web bash

# Check nginx logs
docker-compose -f docker-compose-production.yml logs nginx

# Check database logs
docker-compose -f docker-compose-production.yml logs db

# Restart specific service
docker-compose -f docker-compose-production.yml restart web

# Rebuild and restart
docker-compose -f docker-compose-production.yml up -d --build web
```

## Maintenance

### Regular Tasks

#### 1. Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose-production.yml up -d --build
```

#### 2. Database Backup
```bash
# Create backup
docker-compose -f docker-compose-production.yml exec db pg_dump -U floripacodegurus floripacodegurus > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
docker-compose -f docker-compose-production.yml exec -T db psql -U floripacodegurus floripacodegurus < backup_file.sql
```

#### 3. Log Rotation
```bash
# Check log sizes
docker system df

# Clean up old logs
docker system prune -f

# Clean up unused images
docker image prune -a -f
```

#### 4. Security Updates
```bash
# Update system packages
sudo dnf update -y

# Update Docker
sudo dnf update docker

# Restart services
sudo systemctl restart docker
```

### Monitoring

#### 1. Health Checks
```bash
# Application health
curl http://localhost:8000/health/

# Container health
docker-compose -f docker-compose-production.yml ps

# Resource usage
docker stats
```

#### 2. Log Monitoring
```bash
# Real-time logs
docker-compose -f docker-compose-production.yml logs -f

# Error logs only
docker-compose -f docker-compose-production.yml logs web | grep ERROR

# Access logs
docker-compose -f docker-compose-production.yml logs nginx | grep "GET\|POST"
```

### SSL Certificate Setup (Optional)

To enable HTTPS:

1. **Obtain SSL Certificate:**
   - Use Let's Encrypt with Certbot
   - Or upload your own certificate

2. **Update nginx.conf:**
   ```nginx
   # Uncomment and configure SSL settings
   ssl_certificate /etc/nginx/ssl/cert.pem;
   ssl_certificate_key /etc/nginx/ssl/key.pem;
   ```

3. **Mount SSL directory:**
   ```yaml
   volumes:
     - ./ssl:/etc/nginx/ssl
   ```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review GitHub Actions logs
3. Check EC2 instance logs
4. Contact the development team

---

**Last Updated:** January 2025
**Version:** 1.0
