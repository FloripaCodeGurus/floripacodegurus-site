# GitHub Actions Setup Guide (Digital Ocean Droplet)

This guide helps you set up automated deployment for the Django application to a **Digital Ocean Droplet** (or any Ubuntu VPS) using GitHub Actions.

## 🚀 Quick Setup

### 1. Repository Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.

**Production (deploy.yml, branch `main`):**

| Secret | Description | Example |
|--------|-------------|---------|
| `DEPLOY_HOST` | Droplet IP or hostname | `134.209.73.13` |
| `DEPLOY_SSH_KEY` | Full private SSH key (PEM) | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `DEPLOY_USER` | (Optional) SSH user on server | `root` (default) |

**Staging (staging.yml, branch `staging`):**

| Secret | Description | Example |
|--------|-------------|---------|
| `DEPLOY_HOST_STG` | Staging droplet IP | `134.209.73.13` |
| `DEPLOY_SSH_KEY` | Same private SSH key (or a staging-specific key) | (same as above) |
| `DEPLOY_USER_STG` | (Optional) SSH user on staging server | `root` (default) |
| `DOCKERHUB_USERNAME` | Docker Hub login | `fcgurus` |
| `DOCKERHUB_STAGING_DEPLOY_KEY` | Docker Hub deploy token (or password) | `dckr_pat_...` |

### 2. SSH Key Setup

**Generate a key pair (if needed):**
```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_key
```

**Add the public key to your Droplet:**
```bash
ssh-copy-id -i ~/.ssh/github_actions_key.pub root@134.209.73.13
# Or manually: append the .pub content to ~/.ssh/authorized_keys on the server
```

**Add the private key to GitHub:**
- Copy the full content of `~/.ssh/github_actions_key` (including `-----BEGIN...` and `-----END...`).
- Create a secret named `DEPLOY_SSH_KEY` and paste that content.

### 3. Droplet Preparation

**First-time server setup:**
```bash
ssh root@134.209.73.13
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/floripacodegurus-site/main/setup-server.sh | bash
# Log out and log back in so the docker group is applied
```

**Production app directory (`/opt/floripacodegurus`):**
```bash
mkdir -p /opt/floripacodegurus && cd /opt/floripacodegurus
git clone https://github.com/FloripaCodeGurus/floripacodegurus-site.git .
cp env.production.template .env.production
nano .env.production   # set SECRET_KEY, ALLOWED_HOSTS (include droplet IP), POSTGRES_*
```

**Staging app directory (for staging workflow):**
```bash
mkdir -p /opt/floripacodegurus-staging && cd /opt/floripacodegurus-staging
git clone https://github.com/FloripaCodeGurus/floripacodegurus-site.git .
git checkout staging
cp env.staging.template .env.staging
nano .env.staging     # set SECRET_KEY, ALLOWED_HOSTS, POSTGRES_*
# Ensure docker-compose-staging.yml and nginx.conf are in this directory (they come from the repo)
```

### 4. Firewall

On the droplet (or in Digital Ocean Networking):

- Allow **SSH** (22)
- Allow **HTTP** (80) and **HTTPS** (443)
- Allow **8000** (Django/Gunicorn, optional if you use Nginx in front)

## 🎯 Workflow Usage

### Automatic deployment
- **Production:** Push to `main`. Workflow `deploy.yml` SSHs to the server, pulls code, and runs `docker-compose-production.yml`.
- **Staging:** Push to `staging`. Workflow `staging.yml` builds the Docker image, pushes to Docker Hub, SSHs to the staging server, and runs `docker-compose-staging.yml`.

### Manual deployment
1. Open the **Actions** tab.
2. Select **"Advanced Deploy Django App to Server (Digital Ocean / VPS)"**.
3. Click **Run workflow**, choose environment (e.g. production).
4. Click **Run workflow**.

### SSL (HTTPS)
1. **Actions** → **SSL Certificate Setup**.
2. Run workflow and enter domain and email.

## 🔧 Workflow Overview

- **Deploy Production** (`deploy.yml`): On push to `main`, SSH deploy with `docker-compose-production.yml`.
- **Deploy Staging** (`staging.yml`): On push to `staging`, build image, push to Docker Hub, SSH deploy with `docker-compose-staging.yml`.
- **SSL Certificate Setup** (if present): Let's Encrypt and Nginx SSL.

## 🚨 Troubleshooting

**SSH connection failed**
- Check `DEPLOY_HOST` (IP or hostname) and `DEPLOY_SSH_KEY` (full private key).
- Test manually: `ssh -i ~/.ssh/github_actions_key root@134.209.73.13`

**Permission denied**
- On server: `sudo chown -R $USER:$USER /opt/floripacodegurus`
- Ensure the public key is in `~/.ssh/authorized_keys` for the user used in `DEPLOY_USER`.

**Docker / deploy fails**
- On server: `docker-compose -f docker-compose-production.yml logs`
- Check disk: `df -h` and `free -h`

**App not reachable**
- Open ports 80, 443, and optionally 8000 in the droplet firewall or Digital Ocean networking.
- Ensure `ALLOWED_HOSTS` in `.env.production` includes your droplet IP (e.g. `134.209.73.13`) and domain.

## 📝 Notes

- No AWS credentials or EC2-specific configuration is required.
- Default SSH user is `root`; set `DEPLOY_USER` if you use another user.
- All deployment uses `docker-compose-production.yml` (Nginx + web + db).

For more detail, see **DEPLOYMENT.md**.
