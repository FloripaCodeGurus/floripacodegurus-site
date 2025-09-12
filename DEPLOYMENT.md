# Django App Deployment Guide - AWS EC2 with GitHub Actions

This guide will walk you through deploying your Django application to AWS EC2 using GitHub Actions for continuous deployment.

## 📋 Prerequisites

- AWS account with EC2 access
- GitHub repository with your Django app
- Domain name (optional but recommended)
- SSL certificate (for HTTPS)

## 🚀 Quick Start

### 1. Set up AWS EC2 Instance

1. Launch an EC2 instance (Ubuntu 20.04 or later recommended)
2. Configure security groups to allow:
   - SSH (port 22)
   - HTTP (port 80)
   - HTTPS (port 443)
3. Connect to your instance and run the setup script:

```bash
# Download and run the setup script
curl -fsSL https://raw.githubusercontent.com/yourusername/yourrepo/main/setup-server.sh | bash

# Or if you have the file locally
chmod +x setup-server.sh
./setup-server.sh
```

### 2. Configure GitHub Repository Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions, and add these secrets:

#### Required Secrets:
```
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1

EC2_HOST=your-ec2-public-ip-or-domain
EC2_USERNAME=ubuntu
EC2_SSH_KEY=your-private-ssh-key-content
EC2_PORT=22

DJANGO_SECRET_KEY=your-django-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-ec2-ip

POSTGRES_DB=floripacodegurus_prod
POSTGRES_USER=floripacodegurus_user
POSTGRES_PASSWORD=your-secure-database-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

USER_NAME=Admin User
USER_EMAIL=admin@yourdomain.com
USER_PASSWORD=your-admin-password
```

### 3. Deploy

Push your code to the main/master branch to trigger automatic deployment:

```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

## 📁 File Structure

The deployment setup includes these key files:

```
├── .github/workflows/deploy.yml          # GitHub Actions workflow
├── docker-compose-production.yml         # Production Docker setup
├── nginx.conf                            # Nginx configuration
├── setup-server.sh                      # EC2 server setup script
├── env.production.template              # Environment variables template
└── DEPLOYMENT.md                        # This documentation
```

## 🔧 Manual Deployment Steps

If you prefer manual deployment or need to troubleshoot:

### 1. Prepare Your Server

```bash
# Run the setup script
./setup-server.sh

# Log out and back in to apply docker group changes
exit
# SSH back into your server
```

### 2. Deploy Your Application

```bash
# Navigate to the application directory
cd /opt/floripacodegurus

# Copy your environment file
cp env.production.template .env.production
# Edit .env.production with your actual values
nano .env.production

# Deploy using Docker Compose
docker-compose -f docker-compose-production.yml up -d --build

# Run migrations
docker-compose -f docker-compose-production.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose-production.yml exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose -f docker-compose-production.yml exec web python manage.py createsuperuser
```

## 🛠️ Management Commands

### Monitoring
```bash
# Check application status
/opt/floripacodegurus/monitor.sh

# View logs
docker-compose -f docker-compose-production.yml logs -f

# Health check
/opt/floripacodegurus/health-check.sh
```

### Backups
```bash
# Create backup
/opt/floripacodegurus/backup.sh

# Restore from backup (manual process)
cd /opt/floripacodegurus/backups
tar -xzf backup-YYYYMMDD-HHMMSS.tar.gz
```

### Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose-production.yml down
docker-compose -f docker-compose-production.yml up -d --build

# Run migrations if needed
docker-compose -f docker-compose-production.yml exec web python manage.py migrate
```

## 🔒 SSL Configuration

### Using Let's Encrypt (Recommended)

1. Install Certbot:
```bash
sudo apt-get install certbot python3-certbot-nginx
```

2. Obtain SSL certificate:
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. Update nginx.conf to use the certificates:
```nginx
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
```

### Using Custom Certificates

1. Upload your certificates to `/opt/floripacodegurus/ssl/`
2. Update nginx.conf with your certificate paths
3. Restart nginx: `docker-compose -f docker-compose-production.yml restart nginx`

## 🚨 Troubleshooting

### Common Issues

1. **Containers not starting**
   ```bash
   # Check logs
   docker-compose -f docker-compose-production.yml logs
   
   # Check system resources
   df -h
   free -h
   ```

2. **Database connection issues**
   ```bash
   # Check database container
   docker-compose -f docker-compose-production.yml logs db
   
   # Test database connection
   docker-compose -f docker-compose-production.yml exec db pg_isready -U $POSTGRES_USER
   ```

3. **Static files not loading**
   ```bash
   # Recollect static files
   docker-compose -f docker-compose-production.yml exec web python manage.py collectstatic --noinput
   ```

4. **Permission issues**
   ```bash
   # Fix ownership
   sudo chown -R $USER:$USER /opt/floripacodegurus
   ```

### Log Locations

- Application logs: `/var/log/floripacodegurus/django.log`
- Nginx logs: `docker-compose -f docker-compose-production.yml logs nginx`
- System logs: `/var/log/syslog`

## 📊 Monitoring and Maintenance

### Automated Tasks

The setup includes these automated cron jobs:
- Daily backups at 2 AM
- Health checks every 5 minutes

### Performance Monitoring

```bash
# System resources
htop

# Docker stats
docker stats

# Application metrics
docker-compose -f docker-compose-production.yml exec web python manage.py shell
```

### Security Updates

```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade

# Update Docker images
docker-compose -f docker-compose-production.yml pull
docker-compose -f docker-compose-production.yml up -d
```

## 🔄 Rollback Process

If you need to rollback to a previous version:

1. **Using backups:**
   ```bash
   cd /opt/floripacodegurus/backups
   # Find the backup you want to restore
   ls -la
   # Extract and restore
   tar -xzf backup-YYYYMMDD-HHMMSS.tar.gz
   ```

2. **Using Git:**
   ```bash
   cd /opt/floripacodegurus
   git log --oneline
   git checkout <previous-commit-hash>
   docker-compose -f docker-compose-production.yml up -d --build
   ```

## 📞 Support

If you encounter issues:

1. Check the logs first
2. Run the health check script
3. Review this documentation
4. Check GitHub Actions workflow runs for deployment errors

## 🔐 Security Best Practices

1. **Keep your system updated:**
   ```bash
   sudo apt-get update && sudo apt-get upgrade
   ```

2. **Use strong passwords** for all accounts and services

3. **Regular backups** - the system creates daily backups automatically

4. **Monitor logs** for suspicious activity

5. **Use HTTPS** - configure SSL certificates

6. **Restrict SSH access** - consider using key-based authentication only

7. **Firewall configuration** - only open necessary ports

---

## 📝 Additional Notes

- The deployment uses Docker containers for consistency
- Nginx serves as a reverse proxy and handles SSL termination
- PostgreSQL is used as the production database
- Static files are served by WhiteNoise with compression
- The system includes automated health checks and backups
- All logs are properly configured and rotated

For questions or issues, please refer to the troubleshooting section or create an issue in the repository.
