# Django App Deployment Guide - Digital Ocean Droplet with GitHub Actions

This guide walks you through deploying your Django application to a **Digital Ocean Droplet** (or any Ubuntu VPS) using GitHub Actions for continuous deployment.

## 📋 Prerequisites

- Digital Ocean droplet (or any Ubuntu VPS) with SSH access
- GitHub repository with your Django app
- Domain name (optional but recommended)
- SSL certificate (for HTTPS)

## 🚀 Quick Start

### 1. Set up your Digital Ocean Droplet

1. Create a droplet (Ubuntu 22.04 or later recommended).
2. Add your SSH key in Digital Ocean or use password auth initially.
3. Ensure these ports are open (Digital Ocean firewall or UFW):
   - SSH (22)
   - HTTP (80)
   - HTTPS (443)
   - Application (8000) — for direct app access before Nginx
4. SSH into your droplet and run the setup script:

```bash
# Download and run the setup script
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/floripacodegurus-site/main/setup-server.sh | bash

# Or if you have the file locally
chmod +x setup-server.sh
./setup-server.sh
```

5. Log out and back in so the `docker` group is applied, then clone your repo (or let GitHub Actions deploy):

```bash
cd /opt/floripacodegurus
# If you prefer manual first deploy:
git clone https://github.com/YOUR_USERNAME/floripacodegurus-site.git .
# Then create .env.production (see env.production.template) and run:
# docker-compose -f docker-compose-production.yml up -d --build
```

### 2. Configure GitHub Repository Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.

Add these secrets:

#### Required Secrets

| Secret           | Description                          | Example                    |
|------------------|--------------------------------------|----------------------------|
| `DEPLOY_HOST`    | Droplet IP or hostname               | `134.209.73.13`            |
| `DEPLOY_SSH_KEY` | Private SSH key content (full PEM)   | `-----BEGIN OPENSSH PRIVATE KEY-----...` |

#### Optional

| Secret        | Description              | Default |
|---------------|--------------------------|---------|
| `DEPLOY_USER` | SSH user on the server   | `root`  |

#### Django / app (optional; can be set on server in `.env.production`)

- `DJANGO_SECRET_KEY`
- `POSTGRES_PASSWORD`
- etc. (see `env.production.template`)

You do **not** need any AWS keys or EC2-specific secrets.

### 3. Deploy

Push to `main` or `master` to trigger automatic deployment:

```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

## 📁 File Structure

Key files for deployment:

```
├── .github/workflows/deploy.yml          # GitHub Actions workflow
├── .github/workflows/deploy-advanced.yml  # Advanced deploy with backups
├── docker-compose-production.yml         # Production Docker setup
├── nginx.conf                            # Nginx configuration
├── setup-server.sh                       # Droplet/VPS setup script
├── env.production.template               # Environment variables template
└── DEPLOYMENT.md                         # This file
```

## 🔧 Manual Deployment Steps

If you want to deploy or troubleshoot manually:

### 1. Prepare the server

```bash
./setup-server.sh
# Log out and back in
```

### 2. Deploy the application

```bash
cd /opt/floripacodegurus

# Copy and edit environment file
cp env.production.template .env.production
nano .env.production   # set SECRET_KEY, ALLOWED_HOSTS (include 134.209.73.13), DB password, etc.

# Deploy with Docker Compose
docker-compose -f docker-compose-production.yml up -d --build

# Migrations and static files
docker-compose -f docker-compose-production.yml exec web python manage.py migrate
docker-compose -f docker-compose-production.yml exec web python manage.py collectstatic --noinput

# Create superuser (optional)
docker-compose -f docker-compose-production.yml exec web python manage.py createsuperuser
```

## 🛠️ Management Commands

### Monitoring

```bash
/opt/floripacodegurus/monitor.sh
docker-compose -f docker-compose-production.yml logs -f
/opt/floripacodegurus/health-check.sh
```

### Backups

```bash
/opt/floripacodegurus/backup.sh
```

### Updates (after code changes)

```bash
cd /opt/floripacodegurus
git pull origin main
docker-compose -f docker-compose-production.yml down
docker-compose -f docker-compose-production.yml up -d --build
docker-compose -f docker-compose-production.yml exec web python manage.py migrate
```

## 🔒 SSL Configuration (Let's Encrypt)

1. Install Certbot on the droplet (Ubuntu):

```bash
sudo apt-get install certbot
```

2. Use the **SSL Certificate Setup** workflow in GitHub Actions (Actions → SSL Certificate Setup), or on the server:

```bash
sudo certbot certonly --standalone -d yourdomain.com --email your@email.com --agree-tos
# Copy certs to /opt/floripacodegurus/ssl/ and point nginx to them (see nginx.conf)
```

## 🚨 Troubleshooting

- **Containers not starting:**  
  `docker-compose -f docker-compose-production.yml logs`  
  Check disk: `df -h` and `free -h`.

- **Database connection errors:**  
  `docker-compose -f docker-compose-production.yml logs db`  
  Ensure `.env.production` has correct `POSTGRES_*` and that the `db` service is up.

- **Static files not loading:**  
  `docker-compose -f docker-compose-production.yml exec web python manage.py collectstatic --noinput`

- **Permission issues:**  
  `sudo chown -R $USER:$USER /opt/floripacodegurus`

## 🔐 Security Notes

1. Keep the system updated: `sudo apt-get update && sudo apt-get upgrade`
2. Use strong passwords and a strong `SECRET_KEY`
3. Prefer SSH key auth; disable password login if possible
4. Restrict SSH and open only needed ports in the firewall

---

- Deployment uses **Docker** and **docker-compose-production.yml**.
- **Nginx** acts as reverse proxy and can serve SSL.
- **PostgreSQL** is the production database.
- Static files are served by WhiteNoise with compression.
- No AWS resources or configurations are required.
