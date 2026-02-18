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
- **Documentation**: `DEPLOYMENT.md` — deployment, local development, troubleshooting

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

## 🚀 Deployment

**See [DEPLOYMENT.md](DEPLOYMENT.md)** for the full guide: local development, staging, production, GitHub Actions secrets, and troubleshooting.

| Environment | Branch | Trigger |
|-------------|--------|---------|
| **Staging** | `staging` | Push → build image → deploy |
| **Production** | `main` | Push → deploy |

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