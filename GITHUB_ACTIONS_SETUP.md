# GitHub Actions Setup Guide

This guide will help you set up automated deployment for your Django application using GitHub Actions.

## 🚀 Quick Setup

### 1. Repository Secrets Configuration

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add the following secrets:

#### Required Secrets:
```
EC2_HOST=ec2-54-94-54-29.sa-east-1.compute.amazonaws.com
EC2_SSH_KEY=-----BEGIN OPENSSH PRIVATE KEY-----
your-private-key-content-here
-----END OPENSSH PRIVATE KEY-----
```

#### Optional Secrets (for advanced features):
```
EC2_USER=ec2-user
EC2_PORT=22
DJANGO_SECRET_KEY=your-django-secret-key
POSTGRES_PASSWORD=your-database-password
```

### 2. SSH Key Setup

#### Generate SSH Key Pair (if you don't have one):
```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_key
```

#### Add Public Key to EC2 Instance:
```bash
# Copy the public key to your EC2 instance
ssh-copy-id -i ~/.ssh/github_actions_key.pub ec2-user@your-ec2-ip

# Or manually add to ~/.ssh/authorized_keys on EC2
cat ~/.ssh/github_actions_key.pub | ssh ec2-user@your-ec2-ip 'cat >> ~/.ssh/authorized_keys'
```

#### Add Private Key to GitHub Secrets:
```bash
# Copy the private key content
cat ~/.ssh/github_actions_key

# Add this content to EC2_SSH_KEY secret in GitHub
```

### 3. EC2 Instance Preparation

#### Initial Server Setup:
```bash
# Connect to your EC2 instance
ssh -i your-key.pem ec2-user@your-ec2-ip

# Run the setup script
curl -fsSL https://raw.githubusercontent.com/yourusername/floripacodegurus-site/main/setup-server-amazon-linux.sh | bash

# Create application directory
sudo mkdir -p /opt/floripacodegurus
sudo chown -R ec2-user:ec2-user /opt/floripacodegurus
```

#### Configure Environment:
```bash
cd /opt/floripacodegurus

# Create production environment file
cat > .env.production << 'EOF'
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,your-ec2-ip,localhost
POSTGRES_DB=floripacodegurus_prod
POSTGRES_USER=floripacodegurus_user
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
EOF
```

### 4. Security Group Configuration

In AWS Console → EC2 → Security Groups:

#### Add Inbound Rules:
- **Type**: Custom TCP, **Port**: 22, **Source**: Your IP (for SSH)
- **Type**: Custom TCP, **Port**: 8000, **Source**: 0.0.0.0/0 (for HTTP)
- **Type**: HTTP, **Port**: 80, **Source**: 0.0.0.0/0
- **Type**: HTTPS, **Port**: 443, **Source**: 0.0.0.0/0

## 🎯 Workflow Usage

### Automatic Deployment
- Push to `main` or `master` branch
- GitHub Actions will automatically:
  - Run tests
  - Build Docker containers
  - Deploy to EC2
  - Run health checks

### Manual Deployment
1. Go to **Actions** tab in your repository
2. Select **"Advanced Deploy Django App to AWS EC2"**
3. Click **"Run workflow"**
4. Choose environment (production/staging)
5. Click **"Run workflow"**

### SSL Certificate Setup
1. Go to **Actions** tab
2. Select **"SSL Certificate Setup"**
3. Click **"Run workflow"**
4. Enter your domain name and email
5. Click **"Run workflow"**

## 🔧 Workflow Features

### Deploy Workflow (`deploy.yml`)
- ✅ **Automated Testing**: Runs Django tests before deployment
- ✅ **Docker Build**: Builds and pushes containers
- ✅ **Health Checks**: Verifies application is running
- ✅ **Rollback**: Automatically rolls back on failure

### Advanced Deploy Workflow (`deploy-advanced.yml`)
- ✅ **Pre-deployment Backup**: Creates backup before deployment
- ✅ **Database Migration**: Runs Django migrations
- ✅ **Static Files**: Collects static files
- ✅ **Post-deployment Verification**: Comprehensive health checks
- ✅ **Environment Selection**: Choose production or staging

### SSL Setup Workflow (`ssl-setup.yml`)
- ✅ **Let's Encrypt**: Automatic SSL certificate generation
- ✅ **Nginx Configuration**: SSL-enabled nginx setup
- ✅ **Auto-renewal**: Configures certificate auto-renewal
- ✅ **HTTPS Redirect**: Redirects HTTP to HTTPS

## 🚨 Troubleshooting

### Common Issues

#### 1. SSH Connection Failed
```bash
# Check SSH key format
echo "$EC2_SSH_KEY" | head -1
# Should show: -----BEGIN OPENSSH PRIVATE KEY-----

# Test SSH connection manually
ssh -i ~/.ssh/github_actions_key ec2-user@your-ec2-ip
```

#### 2. Permission Denied
```bash
# Fix permissions on EC2
sudo chown -R ec2-user:ec2-user /opt/floripacodegurus
chmod 600 ~/.ssh/authorized_keys
```

#### 3. Docker Build Failed
```bash
# Check Docker installation
docker --version
docker-compose --version

# Check disk space
df -h
```

#### 4. Application Not Accessible
- Check security group rules
- Verify port 8000 is open
- Check application logs: `docker-compose logs web`

### Debug Commands

```bash
# Check workflow logs in GitHub Actions
# Go to Actions → Select workflow run → View logs

# Check EC2 instance
ssh ec2-user@your-ec2-ip
cd /opt/floripacodegurus
docker-compose ps
docker-compose logs web
```

## 📊 Monitoring

### GitHub Actions Status
- View workflow runs in **Actions** tab
- Check deployment status with badges in README
- Monitor deployment logs for issues

### Application Monitoring
```bash
# Check application status
curl -I http://your-ec2-ip:8000/

# Check container health
docker-compose ps
docker stats
```

## 🔄 Rollback Process

If deployment fails:

1. **Automatic Rollback**: Advanced workflow automatically rolls back
2. **Manual Rollback**: 
   ```bash
   ssh ec2-user@your-ec2-ip
   cd /opt/floripacodegurus
   docker-compose -f docker-compose-simple.yml down
   # Restore from backup if available
   ```

## 📝 Best Practices

1. **Always test locally** before pushing to main branch
2. **Use feature branches** for development
3. **Monitor deployment logs** for issues
4. **Keep secrets secure** and rotate regularly
5. **Backup database** before major deployments
6. **Use staging environment** for testing

## 🆘 Support

If you encounter issues:

1. Check the **Actions** tab for error logs
2. Verify all secrets are configured correctly
3. Test SSH connection manually
4. Check EC2 instance status and logs
5. Review security group configuration

For more help, check the troubleshooting section in the main README.md file.
