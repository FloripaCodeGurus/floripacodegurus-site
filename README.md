# Floripa Code Gurus

[![Deploy Django App to AWS EC2](https://github.com/yourusername/floripacodegurus-site/actions/workflows/deploy.yml/badge.svg)](https://github.com/yourusername/floripacodegurus-site/actions/workflows/deploy.yml)
[![Advanced Deploy Django App to AWS EC2](https://github.com/yourusername/floripacodegurus-site/actions/workflows/deploy-advanced.yml/badge.svg)](https://github.com/yourusername/floripacodegurus-site/actions/workflows/deploy-advanced.yml)

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
- **Infrastructure:** AWS EC2, Amazon Linux 2023

---

## 📂 Project Structure

- **escola/**: Main app for courses and educational content  
- **tutoriais/**: Tutorials and learning resources  
- **users/**: User management and registration  
- **configs/**: Project configuration and settings
- **deployment/**: Docker and deployment configuration
  - `Dockerfile`: Container configuration
  - `docker-compose-simple.yml`: Simplified production setup
  - `docker-compose-production.yml`: Full production setup with Nginx
  - `setup-server-amazon-linux.sh`: EC2 server setup script
  - `env.production.template`: Production environment template
- **.github/workflows/**: GitHub Actions automation
  - `deploy.yml`: Basic automated deployment
  - `deploy-advanced.yml`: Advanced deployment with backups
  - `ssl-setup.yml`: SSL certificate automation
  - `troubleshoot.yml`: Deployment troubleshooting tools
  - `quick-fix.yml`: Quick deployment fixes
  - `fix-security-group.yml`: Security group configuration for external access
- **Documentation**:
  - `GITHUB_ACTIONS_SETUP.md`: Complete GitHub Actions setup guide

---

## 🌐 Live Demo

- **Production:** [https://www.floripacodegurus.com.br](https://www.floripacodegurus.com.br)
- **Development:** [http://ec2-54-94-54-29.sa-east-1.compute.amazonaws.com:8000](http://ec2-54-94-54-29.sa-east-1.compute.amazonaws.com:8000) (AWS EC2)

## 📊 Deployment Status

✅ **Successfully Deployed on AWS EC2**
- **Instance**: ec2-54-94-54-29.sa-east-1.compute.amazonaws.com
- **Status**: Running
- **Services**: Django + PostgreSQL + Docker
- **Last Updated**: September 26, 2025

### Current Services
- **Web Application**: Django 5.2 running on port 8000
- **Database**: PostgreSQL 15 with persistent storage
- **Container Management**: Docker Compose
- **Infrastructure**: AWS EC2 (Amazon Linux 2023)

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

## 🚀 Production Deployment (AWS EC2)

### Prerequisites
- AWS EC2 instance (Amazon Linux 2023 recommended)
- SSH access to your EC2 instance
- Domain name (optional but recommended)
- GitHub repository with secrets configured

### 🎯 Automated Deployment with GitHub Actions

#### 1. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions, and add:

```
EC2_HOST=your-ec2-public-ip-or-domain
EC2_SSH_KEY=your-private-ssh-key-content
```

#### 2. Deploy with GitHub Actions

**Automatic Deployment:**
- Push to `main` or `master` branch
- GitHub Actions will automatically deploy your application

**Manual Deployment:**
- Go to Actions tab in your GitHub repository
- Select "Advanced Deploy Django App to AWS EC2"
- Click "Run workflow"
- Choose environment (production/staging)

#### 3. SSL Certificate Setup

For HTTPS deployment:
- Go to Actions tab
- Select "SSL Certificate Setup"
- Click "Run workflow"
- Enter your domain name and email

### 🔧 Manual Deployment

1. **Connect to your EC2 instance:**
   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-ip
   ```

2. **Run the setup script:**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/yourusername/floripacodegurus-site/main/setup-server-amazon-linux.sh | bash
   ```

3. **Deploy your application:**
   ```bash
   cd /opt/floripacodegurus
   docker-compose -f docker-compose-simple.yml up -d
   ```

4. **Configure security group:**
   - Add inbound rule for port 8000 (HTTP)
   - Add inbound rule for port 80 (HTTP)
   - Add inbound rule for port 443 (HTTPS)

### Manual Deployment Steps

1. **Upload your application:**
   ```bash
   # From your local machine
   tar -czf deployment.tar.gz --exclude='venv' --exclude='__pycache__' --exclude='.git' .
   scp -i your-key.pem deployment.tar.gz ec2-user@your-ec2-ip:/opt/floripacodegurus/
   ```

2. **Extract and configure:**
   ```bash
   cd /opt/floripacodegurus
   tar -xzf deployment.tar.gz
   cp env.production.template .env.production
   # Edit .env.production with your values
   ```

3. **Start the application:**
   ```bash
   docker-compose -f docker-compose-simple.yml up -d --build
   ```

### Environment Configuration

Create `.env.production` with the following variables:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,your-ec2-ip,localhost
POSTGRES_DB=floripacodegurus_prod
POSTGRES_USER=floripacodegurus_user
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Management Commands

```bash
# Check container status
docker-compose -f docker-compose-simple.yml ps

# View logs
docker-compose -f docker-compose-simple.yml logs -f

# Restart containers
docker-compose -f docker-compose-simple.yml restart

# Create superuser
docker-compose -f docker-compose-simple.yml exec web python manage.py createsuperuser

# Run migrations
docker-compose -f docker-compose-simple.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose-simple.yml exec web python manage.py collectstatic --noinput
```

### GitHub Actions Workflows

The repository includes several automated workflows:

#### 🚀 **Deploy Django App to AWS EC2** (`deploy.yml`)
- **Trigger**: Push to main/master branch
- **Features**: 
  - Automated testing
  - Docker container deployment
  - Health checks
  - Rollback on failure

#### 🎯 **Advanced Deploy Django App to AWS EC2** (`deploy-advanced.yml`)
- **Trigger**: Manual or push to main/master
- **Features**:
  - Pre-deployment backups
  - Database migration
  - Static file collection
  - Post-deployment verification
  - Environment selection (production/staging)

#### 🔒 **SSL Certificate Setup** (`ssl-setup.yml`)
- **Trigger**: Manual workflow
- **Features**:
  - Let's Encrypt certificate generation
  - Nginx SSL configuration
  - Auto-renewal setup
  - HTTPS redirection

#### 🔧 **Troubleshoot Deployment Issues** (`troubleshoot.yml`)
- **Trigger**: Manual workflow
- **Features**:
  - Container status checking
  - Log analysis
  - Service restart
  - Connectivity testing
  - Full system diagnosis

#### ⚡ **Quick Fix Deployment** (`quick-fix.yml`)
- **Trigger**: Manual workflow
- **Features**:
  - Fix environment file issues
  - Restart containers
  - Rebuild containers
  - Complete deployment fix

#### 🔒 **Fix Security Group for External Access** (`fix-security-group.yml`)
- **Trigger**: Manual workflow
- **Features**:
  - Check current security group rules
  - Add port 8000 for Django access
  - Add all required ports (22, 80, 443, 8000)
  - Test external connectivity

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
docker-compose -f docker-compose-simple.yml logs -f web
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
docker-compose -f docker-compose-simple.yml logs

# Check system resources
df -h
free -h
```

**2. Database connection issues:**
```bash
# Check database container
docker-compose -f docker-compose-simple.yml logs db

# Test database connection
docker-compose -f docker-compose-simple.yml exec db pg_isready -U floripacodegurus_user
```

**3. Static files not loading:**
```bash
# Recollect static files
docker-compose -f docker-compose-simple.yml exec web python manage.py collectstatic --noinput
```

**4. Permission issues:**
```bash
# Fix ownership
sudo chown -R ec2-user:ec2-user /opt/floripacodegurus
```

**5. Security group issues:**
- Ensure port 8000 is open in AWS Security Group
- Check if the instance is running
- Verify SSH key permissions

### Health Checks

```bash
# Application health
curl -I http://localhost:8000/

# Container status
docker-compose -f docker-compose-simple.yml ps

# System resources
htop
```

### Log Locations

- **Application logs**: `docker-compose -f docker-compose-simple.yml logs web`
- **Database logs**: `docker-compose -f docker-compose-simple.yml logs db`
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