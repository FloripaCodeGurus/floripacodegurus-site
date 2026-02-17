# Floripa Code Gurus

[![Deploy Django App](https://github.com/yourusername/floripacodegurus-site/actions/workflows/deploy.yml/badge.svg)](https://github.com/yourusername/floripacodegurus-site/actions/workflows/deploy.yml)
[![Advanced Deploy](https://github.com/yourusername/floripacodegurus-site/actions/workflows/deploy-advanced.yml/badge.svg)](https://github.com/yourusername/floripacodegurus-site/actions/workflows/deploy-advanced.yml)

Welcome to **Floripa Code Gurus**!  
This is a web platform dedicated to teaching programming, developing websites, apps, systems, and much more. Our mission is to empower people with technology and foster a collaborative learning environment for all skill levels.

---

## 🚀 Features

- **Tutorials & Courses:**  
  Access a wide range of tutorials on Python, Django, Ruby, C#, PHP, Java, BioPython, and more.

- **Collaborative Learning:**  
  Join a community of learners and developers, share knowledge, and grow together.

- **Project Development:**  
  Build and showcase your own websites, apps, and systems with guidance from experienced mentors.

- **Admin Dashboard:**  
  Manage content and users with a secure Django admin interface.

---

## 🛠️ Tech Stack

- **Backend:** [Django 5.2](https://www.djangoproject.com/)
- **Database:** PostgreSQL 15
- **Deployment:** Docker, Docker Compose, Gunicorn, Nginx
- **Configuration:** Environment variables managed with `django-environ` and `python-decouple`
- **Infrastructure:** Digital Ocean Droplet (or any Ubuntu VPS)

---

## 📂 Project Structure

- **escola/**: Main app for courses and educational content  
- **tutoriais/**: Tutorials and learning resources  
- **users/**: User management and registration  
- **configs/**: Project configuration and settings
- **deployment/**: Docker and deployment configuration
  - `Dockerfile`: Container configuration
  - `docker-compose-production.yml`: Production setup with Nginx and PostgreSQL
  - `setup-server.sh`: Droplet/VPS server setup script (Ubuntu)
  - `env.production.template`: Production environment template
- **.github/workflows/**: GitHub Actions automation
  - `deploy.yml`: Basic automated deployment
  - `deploy-advanced.yml`: Advanced deployment with backups
  - `ssl-setup.yml`: SSL certificate automation
  - `troubleshoot.yml`: Deployment troubleshooting tools
  - `quick-fix.yml`: Quick deployment fixes
- **Documentation**:
  - `GITHUB_ACTIONS_SETUP.md`: Complete GitHub Actions setup guide

---

## 🌐 Live Demo

- **Production:** [https://www.floripacodegurus.com.br](https://www.floripacodegurus.com.br)
- **Production (Digital Ocean):** [http://134.209.73.13:8000](http://134.209.73.13:8000) (or your domain)

## 📊 Deployment Status

✅ **Deploy to Digital Ocean Droplet**
- **Droplet IP**: 134.209.73.13 (or your domain)
- **Services**: Django + PostgreSQL + Nginx (Docker Compose)
- **Workflows**: Push to main/master triggers deploy; manual workflows for SSL, troubleshoot, quick-fix

### Current Services
- **Web Application**: Django 5.2 (Gunicorn) on port 8000
- **Database**: PostgreSQL 15 with persistent storage
- **Reverse Proxy**: Nginx (ports 80, 443)
- **Infrastructure**: Digital Ocean Droplet (Ubuntu)

---

## 📝 Getting Started

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/floripacodegurus-site.git
    cd floripacodegurus-site
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Run migrations:**
    ```sh
    python manage.py migrate
    ```

4. **Start the development server:**
    ```sh
    python manage.py runserver
    ```

5. **Access the platform:**  
   Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🚀 Production Deployment (Digital Ocean Droplet)

### Prerequisites
- Digital Ocean droplet (Ubuntu 22.04+ recommended) or any Ubuntu VPS
- SSH access (root or a user with sudo)
- GitHub repository with secrets configured

### 🎯 Automated Deployment with GitHub Actions

#### 1. Configure GitHub Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**, and add:

| Secret | Description | Example |
|--------|-------------|---------|
| `DEPLOY_HOST` | Droplet IP or hostname | `134.209.73.13` |
| `DEPLOY_SSH_KEY` | Full private SSH key (PEM) | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `DEPLOY_USER` | (Optional) SSH user | `root` (default) |

#### 2. Deploy with GitHub Actions

**Automatic deployment:** Push to `main` or `master` — GitHub Actions will run tests and deploy.

**Manual deployment:**
- Go to **Actions** → **Advanced Deploy Django App to Server**
- Click **Run workflow**, choose environment (production/staging)

#### 3. SSL (HTTPS)

- **Actions** → **SSL Certificate Setup** → Run workflow with your domain and email.

### 🔧 Manual Deployment

1. **SSH into your droplet:**
   ```bash
   ssh root@134.209.73.13
   ```

2. **Run the setup script (first time):**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/floripacodegurus-site/main/setup-server.sh | bash
   # Log out and back in so the docker group applies
   ```

3. **Clone and deploy:**
   ```bash
   cd /opt/floripacodegurus
   git clone https://github.com/YOUR_USERNAME/floripacodegurus-site.git .
   cp env.production.template .env.production
   nano .env.production   # set SECRET_KEY, ALLOWED_HOSTS (include 134.209.73.13), POSTGRES_PASSWORD
   docker-compose -f docker-compose-production.yml up -d --build
   docker-compose -f docker-compose-production.yml exec web python manage.py migrate
   docker-compose -f docker-compose-production.yml exec web python manage.py collectstatic --noinput
   ```

4. **Firewall:** Ensure SSH (22), HTTP (80), HTTPS (443), and 8000 are allowed (Digital Ocean firewall or UFW).

### Environment Configuration

Copy `env.production.template` to `.env.production` and set at least:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=134.209.73.13,yourdomain.com,localhost
POSTGRES_DB=floripacodegurus_prod
POSTGRES_USER=floripacodegurus_user
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Management Commands

```bash
docker-compose -f docker-compose-production.yml ps
docker-compose -f docker-compose-production.yml logs -f
docker-compose -f docker-compose-production.yml exec web python manage.py createsuperuser
docker-compose -f docker-compose-production.yml exec web python manage.py migrate
docker-compose -f docker-compose-production.yml exec web python manage.py collectstatic --noinput
```

### GitHub Actions Workflows

- **Deploy Django App to Server** (`deploy.yml`) — Push to main/master: tests, deploy, health check.
- **Advanced Deploy** (`deploy-advanced.yml`) — Manual or push: backups, migrations, static files, verification.
- **SSL Certificate Setup** (`ssl-setup.yml`) — Manual: Let's Encrypt, Nginx SSL, HTTPS.
- **Troubleshoot** (`troubleshoot.yml`) — Manual: containers, logs, restart, connectivity, full diagnosis.
- **Quick Fix** (`quick-fix.yml`) — Manual: fix env, restart/rebuild containers, full fix.

### Docker Services

The deployment includes:
- **Web**: Django application (port 8000)
- **Database**: PostgreSQL 15
- **Nginx**: Reverse proxy (ports 80, 443)

### Monitoring

```bash
# System resources
htop

# Docker stats
docker stats

# Application logs
docker-compose -f docker-compose-production.yml logs -f web
```

---

## 🔧 Troubleshooting

### 🔧 GitHub Actions Troubleshooting

If deployment fails, use the troubleshooting workflows:

#### **Quick Fix (Recommended for current issue):**
1. **Go to Actions tab** in your GitHub repository
2. **Select "Fix Security Group for External Access"**
3. **Choose fix action**:
   - `check_security_group`: Check current security group rules
   - `add_port_8000`: Add port 8000 for Django access
   - `add_all_ports`: Add all required ports (22, 80, 443, 8000)
   - `full_setup`: Complete security group setup and test

#### **Alternative Quick Fix:**
1. **Go to Actions tab** in your GitHub repository
2. **Select "Quick Fix Deployment"**
3. **Choose fix action**:
   - `fix_env_file`: Fix environment file issues
   - `restart_containers`: Restart containers
   - `rebuild_containers`: Rebuild containers
   - `full_fix`: Complete deployment fix

#### **Advanced Troubleshooting:**
1. **Go to Actions tab** in your GitHub repository
2. **Select "Troubleshoot Deployment Issues"**
3. **Choose troubleshooting action**:
   - `check_containers`: Check container status
   - `check_logs`: Analyze container logs
   - `restart_services`: Restart all services
   - `check_connectivity`: Test network connectivity
   - `full_diagnosis`: Complete system analysis

### Common Issues

**1. Containers not starting:**
```bash
# Check logs
docker-compose -f docker-compose-production.yml logs

# Check system resources
df -h
free -h
```

**2. Database connection issues:**
```bash
# Check database container
docker-compose -f docker-compose-production.yml logs db

# Test database connection
docker-compose -f docker-compose-production.yml exec db pg_isready -U floripacodegurus_user
```

**3. Static files not loading:**
```bash
# Recollect static files
docker-compose -f docker-compose-production.yml exec web python manage.py collectstatic --noinput
```

**4. Permission issues:**
```bash
# Fix ownership
sudo chown -R $USER:$USER /opt/floripacodegurus
```

**5. Firewall / connectivity:**
- Ensure ports 22, 80, 443, 8000 are open (Digital Ocean firewall or UFW)
- Check that the droplet is running
- Verify SSH key and `authorized_keys` on the server

### Health Checks

```bash
# Application health
curl -I http://localhost:8000/

# Container status
docker-compose -f docker-compose-production.yml ps

# System resources
htop
```

### Log Locations

- **Application logs**: `docker-compose -f docker-compose-production.yml logs web`
- **Database logs**: `docker-compose -f docker-compose-production.yml logs db`
- **System logs**: `/var/log/syslog`

---

## 🤝 Contributing

We welcome contributions!  
Feel free to open issues, submit pull requests, or suggest new tutorials and features.

---

## 📄 License

This project is licensed under the MIT License.

---

## 📬 Contact

Questions, suggestions, or want to join the team?  
Email us at: [contato@floripacodegurus.com.br](mailto:contato@floripacodegurus.com.br)

---

Happy coding! 🚀