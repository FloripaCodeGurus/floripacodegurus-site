# Floripa Code Gurus — Deployment & Development Guide

Complete guide for local development, staging, and production deployment on **DigitalOcean Droplets** (or any Ubuntu VPS) with GitHub Actions and Docker.

---

## Table of Contents

1. [Overview](#overview)
2. [Local Development](#local-development)
3. [Staging Deployment](#staging-deployment)
4. [Production Deployment](#production-deployment)
5. [GitHub Actions Secrets](#github-actions-secrets)
6. [Post-Deployment & Maintenance](#post-deployment--maintenance)
7. [Troubleshooting](#troubleshooting)
8. [File Reference](#file-reference)

---

## Overview

| Environment   | Branch    | Workflow     | Directory                      | URL                      |
|--------------|-----------|--------------|--------------------------------|--------------------------|
| **Staging**  | `staging` | `staging.yml`| `/opt/floripacodegurus-staging`| `http://YOUR_DROPLET_IP` |
| **Production** | `main`  | `deploy.yml` | `/opt/floripacodegurus`        | `https://yourdomain.com` |

**Staging:** Builds Docker image → pushes to Docker Hub → deploys via SSH.  
**Production:** Deploys via SSH with local build on the server.

---

## Local Development

### Run with Docker Compose

```bash
# Local
docker compose -f docker-compose-local.yml --env-file .env.local up -d --build

# Development
docker compose -f docker-compose-development.yml --env-file .env.development up -d --build

# Stop and clean
docker compose -f docker-compose-local.yml down -v
docker compose -f docker-compose-development.yml --env-file .env.development down -v
```

### View logs

```bash
docker logs -f floripacodegurus-site-web-1
```

### Create superuser

Ensure `.env` contains:
```bash
USER_NAME="Your Name"
USER_EMAIL="your@email.com"
USER_PASSWORD="yourpassword"
```

```bash
chmod +x create_superuser.sh
./create_superuser.sh
```

### Migrations

```bash
export DJANGO_SETTINGS_MODULE=configs.settings.development && python3 manage.py makemigrations
export DJANGO_SETTINGS_MODULE=configs.settings.development && python3 manage.py migrate

# Reset SQLite (migration errors)
rm db.sqlite3
```

---

## Staging Deployment

### Prerequisites

- DigitalOcean droplet (Ubuntu 22.04+)
- GitHub repository
- Docker Hub account

### Step 1: Create Droplet

- **Image:** Ubuntu 22.04 LTS
- **Plan:** Basic (e.g. 1 vCPU / 512MB)
- **Authentication:** SSH key
- **Ports:** SSH (22), HTTP (80), HTTPS (443)

### Step 2: SSH Key

**Option A — Reuse existing key** (if you already SSH to the droplet)

**Option B — Deploy-only key**
```bash
ssh-keygen -t ed25519 -f ~/.ssh/deploy_staging -N "" -C "github-actions-staging"
ssh-copy-id -i ~/.ssh/deploy_staging.pub root@YOUR_DROPLET_IP
```

Copy the **private** key content (including `-----BEGIN` and `-----END`).

### Step 3: GitHub Secrets

**Settings → Secrets and variables → Actions → New repository secret**

| Secret                      | Description              | Example                      |
|----------------------------|--------------------------|------------------------------|
| `DEPLOY_HOST_STG`          | Staging droplet IP       | `134.209.73.13`              |
| `DEPLOY_SSH_KEY`           | Full private SSH key     | `-----BEGIN OPENSSH...`      |
| `DEPLOY_USER_STG`          | (Optional) SSH user      | `root`                       |
| `DOCKERHUB_USERNAME`       | Docker Hub login         | `fcgurus`                    |
| `DOCKERHUB_STAGING_DEPLOY_KEY` | Docker Hub token    | `dckr_pat_...`               |

**Docker Hub token:** Account Settings → Security → New Access Token (read/write).

### Step 4: Prepare Droplet

```bash
ssh root@YOUR_DROPLET_IP
```

**4.1 — Docker**
```bash
sudo apt-get update && sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
```

**4.2 — Docker Compose plugin**
```bash
sudo apt-get install -y docker-compose-plugin
docker compose version
```

**4.3 — Clone repo**
```bash
mkdir -p /opt/floripacodegurus-staging && cd /opt/floripacodegurus-staging
git clone https://github.com/FloripaCodeGurus/floripacodegurus-site.git .
git checkout staging
```

**4.4 — Environment**
```bash
cp env.staging.template .env.staging
nano .env.staging
```

Set: `SECRET_KEY`, `ALLOWED_HOSTS` (include droplet IP), `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

**4.5 — SSL directory**
```bash
mkdir -p /opt/floripacodegurus-staging/ssl
```

### Step 5: Deploy

**Manual first run:**
```bash
cd /opt/floripacodegurus-staging
docker compose -f docker-compose-staging.yml pull web
docker compose -f docker-compose-staging.yml up -d
docker compose -f docker-compose-staging.yml exec -T web python manage.py migrate --noinput
docker compose -f docker-compose-staging.yml exec -T web python manage.py collectstatic --noinput
```

**Automatic:** Push to `staging` branch.

**Access:** `http://YOUR_DROPLET_IP`

---

## Production Deployment

### Step 1: Create Droplet

Same as staging: Ubuntu 22.04+, SSH key, ports 22, 80, 443.

### Step 2: GitHub Secrets

| Secret          | Description        | Example                  |
|-----------------|--------------------|--------------------------|
| `DEPLOY_HOST`   | Production droplet IP | `134.209.73.13`       |
| `DEPLOY_SSH_KEY`| Private SSH key    | `-----BEGIN OPENSSH...`  |
| `DEPLOY_USER`   | (Optional) SSH user| `root`                   |

### Step 3: Prepare Droplet

**3.1 — Setup script**
```bash
ssh root@YOUR_DROPLET_IP
curl -fsSL https://raw.githubusercontent.com/FloripaCodeGurus/floripacodegurus-site/main/setup-server.sh | bash
exit && ssh root@YOUR_DROPLET_IP
```

**3.2 — Docker Compose plugin**
```bash
sudo apt-get install -y docker-compose-plugin
```

**3.3 — Clone repo**
```bash
mkdir -p /opt/floripacodegurus && cd /opt/floripacodegurus
git clone https://github.com/FloripaCodeGurus/floripacodegurus-site.git .
git checkout main
```

**3.4 — Environment**
```bash
cp env.production.template .env.production
nano .env.production
```

Set: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `POSTGRES_*`, `USER_NAME`, `USER_EMAIL`, `USER_PASSWORD`

**3.5 — SSL directory**
```bash
mkdir -p /opt/floripacodegurus/ssl
```

### Step 4: SSL (HTTPS)

```bash
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com --email your@email.com --agree-tos
```

Copy certs:
```bash
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/floripacodegurus/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/floripacodegurus/ssl/key.pem
sudo chown $USER:$USER /opt/floripacodegurus/ssl/*.pem
```

Uncomment SSL paths in `nginx.conf`:
```nginx
ssl_certificate /etc/nginx/ssl/cert.pem;
ssl_certificate_key /etc/nginx/ssl/key.pem;
ssl_protocols TLSv1.2 TLSv1.3;
```

### Step 5: Deploy

```bash
cd /opt/floripacodegurus
docker compose -f docker-compose-production.yml up -d --build
docker compose -f docker-compose-production.yml exec -T web python manage.py migrate --noinput
docker compose -f docker-compose-production.yml exec -T web python manage.py collectstatic --noinput
```

Or push to `main` for automatic deploy.

### Step 6: Firewall

```bash
sudo ufw allow 22 && sudo ufw allow 80 && sudo ufw allow 443
sudo ufw enable
```

---

## GitHub Actions Secrets

| Environment   | Secret                         | Required |
|---------------|--------------------------------|----------|
| **Staging**   | `DEPLOY_HOST_STG`             | Yes      |
| **Staging**   | `DEPLOY_SSH_KEY`              | Yes      |
| **Staging**   | `DOCKERHUB_USERNAME`          | Yes      |
| **Staging**   | `DOCKERHUB_STAGING_DEPLOY_KEY`| Yes      |
| **Staging**   | `DEPLOY_USER_STG`             | No (default: root) |
| **Production**| `DEPLOY_HOST`                 | Yes      |
| **Production**| `DEPLOY_SSH_KEY`              | Yes      |
| **Production**| `DEPLOY_USER`                 | No (default: root) |

---

## Post-Deployment & Maintenance

### Create superuser

```bash
# Staging
cd /opt/floripacodegurus-staging
docker compose -f docker-compose-staging.yml exec web python manage.py createsuperuser

# Production
cd /opt/floripacodegurus
docker compose -f docker-compose-production.yml exec web python manage.py createsuperuser
```

### Monitoring

```bash
docker compose -f docker-compose-staging.yml ps
docker compose -f docker-compose-staging.yml logs -f web
docker stats
```

### Database backup

```bash
cd /opt/floripacodegurus
docker compose -f docker-compose-production.yml exec db pg_dump -U floripacodegurus_user floripacodegurus_prod > backup_$(date +%Y%m%d).sql
```

### Update after code changes

- **Staging:** `git push origin staging`
- **Production:** `git push origin main` or manually:
  ```bash
  cd /opt/floripacodegurus
  git pull origin main
  docker compose -f docker-compose-production.yml up -d --build
  docker compose -f docker-compose-production.yml exec -T web python manage.py migrate --noinput
  docker compose -f docker-compose-production.yml exec -T web python manage.py collectstatic --noinput
  ```

### Cleanup

```bash
docker system prune -f
docker image prune -a -f
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ssh: no key found` / `missing server host` | Check `DEPLOY_SSH_KEY` (full key with `-----BEGIN`/`-----END`) and `DEPLOY_HOST_STG`/`DEPLOY_HOST` |
| `Directory missing` | Create directory, clone repo (see Step 4.3 / 3.3) |
| `docker compose` not found | `sudo apt-get install -y docker-compose-plugin` |
| 502 Bad Gateway | Ensure `entrypoint: []` on web service; check `docker compose logs web` |
| Postgres env warnings | Remove `environment` overrides in db service; use `env_file` only |
| PR_END_OF_FILE_ERROR (HTTPS) | For HTTP-only staging: `SECURE_SSL_REDIRECT = False` in `configs/settings/staging.py` |
| Can't connect from browser | `nc -zv YOUR_IP 80`; check UFW and DigitalOcean firewall for ports 80, 443 |
| Nginx SSL errors | Use `nginx-staging.conf` for HTTP-only; verify cert paths in `./ssl/` for HTTPS |

### Debugging commands

```bash
docker compose -f docker-compose-staging.yml logs -f web
docker compose -f docker-compose-staging.yml logs nginx
docker compose -f docker-compose-staging.yml exec web bash
```

---

## File Reference

| File | Purpose |
|------|---------|
| `docker-compose-staging.yml` | Staging: web, db, nginx (HTTP) |
| `docker-compose-production.yml` | Production: web, db, nginx (HTTP/HTTPS) |
| `nginx-staging.conf` | HTTP-only nginx for staging |
| `nginx.conf` | Production nginx (with SSL) |
| `env.staging.template` | Staging env template |
| `env.production.template` | Production env template |
| `setup-server.sh` | Initial server setup |
| `.github/workflows/staging.yml` | Staging CI/CD |
| `.github/workflows/deploy.yml` | Production CI/CD |

---

*Last updated: February 2026*
