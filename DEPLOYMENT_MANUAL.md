# Floripa Code Gurus - Deployment Manual

This manual provides instructions for deploying the Floripa Code Gurus Django application to a **Digital Ocean Droplet** (or any Ubuntu VPS) using Docker and GitHub Actions.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Digital Ocean Droplet Setup](#digital-ocean-droplet-setup)
3. [GitHub Actions Configuration](#github-actions-configuration)
4. [Manual Deployment](#manual-deployment)
5. [Troubleshooting](#troubleshooting)
6. [Maintenance](#maintenance)

## Prerequisites

### Required Tools
- Docker and Docker Compose installed locally (for local testing)
- Git configured with SSH keys
- Access to GitHub repository

### Server Requirements
- Digital Ocean Droplet (Ubuntu 22.04+ recommended) or any Ubuntu VPS
- SSH access (root or a user with sudo)
- Open ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 8000 (optional, for direct app access)

## Digital Ocean Droplet Setup

### 1. Create Droplet

1. **Droplet configuration:**
   - Image: Ubuntu 22.04 LTS (or later)
   - Plan: Basic (e.g. $6/mo) or higher
   - Region: Choose closest to your users
   - Authentication: SSH key (recommended) or password

2. **Firewall / Networking:**
   - Allow SSH (22), HTTP (80), HTTPS (443), and optionally 8000 (Django)

3. **SSH key:**
   - Add your public key in Digital Ocean or use password for first login.

### 2. Connect to Droplet

```bash
ssh root@134.209.73.13
# Or: ssh your-user@134.209.73.13
```

### 3. Run Setup Script (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/floripacodegurus-site/main/setup-server.sh | bash
# Log out and log back in so the docker group is applied
exit
ssh root@134.209.73.13
```

The script installs Docker, Docker Compose, Git, creates `/opt/floripacodegurus`, backup/health scripts, and UFW rules.

### 4. Or Install Manually

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker (see setup-server.sh for full steps)
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create app directory
sudo mkdir -p /opt/floripacodegurus
sudo chown -R $USER:$USER /opt/floripacodegurus
```

## GitHub Actions Configuration

### 1. Repository Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**.

Add:

#### Required secrets
| Secret | Description | Example |
|--------|-------------|---------|
| `DEPLOY_HOST` | Droplet IP or hostname | `134.209.73.13` |
| `DEPLOY_SSH_KEY` | Full private SSH key (PEM) | See below |

#### Optional
| Secret | Description | Default |
|--------|-------------|---------|
| `DEPLOY_USER` | SSH user on server | `root` |

#### SSH key format for DEPLOY_SSH_KEY
```
Paste the full private key, including:
-----BEGIN OPENSSH PRIVATE KEY-----
... key content ...
-----END OPENSSH PRIVATE KEY-----

Do not commit the private key to the repository.
```

### 2. Workflow Configuration

The deployment workflow is already configured in `.github/workflows/deploy.yml`. It will:

1. Run tests on every push to `main` branch
2. Deploy automatically when tests pass
3. Create deployment package with all necessary files
4. Deploy to server using SSH

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
scp deployment.tar.gz root@134.209.73.13:/opt/floripacodegurus/

# Connect to Droplet
ssh root@134.209.73.13

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
- Verify `DEPLOY_USER` is set if not using root (e.g. `root`)
- Check `DEPLOY_SSH_KEY` format (must include `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----`)
- Ensure private key has correct permissions

#### 2. AWS Credentials Error
```
Error: The request signature we calculated does not match the signature you provided
```

**Solution:**
- Verify `DEPLOY_HOST` is your droplet IP (e.g. `134.209.73.13`)
- Ensure `DEPLOY_SSH_KEY` is the full private key content
- Test SSH: `ssh root@134.209.73.13`

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
sudo apt-get update && sudo apt-get upgrade -y

# Update Docker
sudo apt-get update && sudo apt-get install --only-upgrade docker-ce

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
3. Check droplet/server logs
4. Contact the development team

---

**Last Updated:** January 2025
**Version:** 1.0
