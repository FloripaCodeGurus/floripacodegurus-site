#!/bin/bash

# EC2 Server Setup Script for Django App Deployment (Amazon Linux)
# Run this script on your EC2 instance to prepare it for deployment

set -e

echo "🚀 Setting up Amazon Linux EC2 server for Django app deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo yum update -y

# Install Docker
echo "🐳 Installing Docker..."
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
echo "🔧 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add current user to docker group
echo "👤 Adding user to docker group..."
sudo usermod -aG docker $USER

# Install additional packages
echo "📚 Installing additional packages..."
sudo yum install -y git htop unzip curl wget

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /opt/floripacodegurus
sudo chown -R $USER:$USER /opt/floripacodegurus

# Create backup directory
echo "💾 Creating backup directory..."
mkdir -p /opt/floripacodegurus/backups

# Configure firewall (Amazon Linux uses iptables)
echo "🔥 Configuring firewall..."
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables-save > /etc/iptables/rules.v4 2>/dev/null || echo "iptables rules saved"

# Create log directory
echo "📝 Creating log directory..."
sudo mkdir -p /var/log/floripacodegurus
sudo chown -R $USER:$USER /var/log/floripacodegurus

# Create systemd service for auto-start (optional)
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/floripacodegurus.service > /dev/null << EOF
[Unit]
Description=FloripaCodeGurus Django App
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/floripacodegurus
ExecStart=/usr/local/bin/docker-compose -f docker-compose-production.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose-production.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Create monitoring script
echo "📊 Creating monitoring script..."
cat > /opt/floripacodegurus/monitor.sh << 'EOF'
#!/bin/bash

# Simple monitoring script for the Django app
echo "=== FloripaCodeGurus App Status ==="
echo "Date: $(date)"
echo ""

echo "Docker containers:"
docker-compose -f docker-compose-production.yml ps

echo ""
echo "System resources:"
echo "Memory usage:"
free -h

echo ""
echo "Disk usage:"
df -h

echo ""
echo "Application logs (last 10 lines):"
docker-compose -f docker-compose-production.yml logs --tail=10 web

echo ""
echo "Database logs (last 5 lines):"
docker-compose -f docker-compose-production.yml logs --tail=5 db
EOF

chmod +x /opt/floripacodegurus/monitor.sh

# Create backup script
echo "💾 Creating backup script..."
cat > /opt/floripacodegurus/backup.sh << 'EOF'
#!/bin/bash

# Backup script for the Django app
BACKUP_DIR="/opt/floripacodegurus/backups"
DATE=$(date +%Y%m%d-%H%M%S)

echo "Creating backup at $DATE..."

# Create backup directory
mkdir -p "$BACKUP_DIR/$DATE"

# Backup database
echo "Backing up database..."
docker-compose -f docker-compose-production.yml exec -T db pg_dump -U $POSTGRES_USER $POSTGRES_DB > "$BACKUP_DIR/$DATE/database.sql"

# Backup media files
echo "Backing up media files..."
cp -r media "$BACKUP_DIR/$DATE/"

# Backup environment file
echo "Backing up environment file..."
cp .env.production "$BACKUP_DIR/$DATE/" 2>/dev/null || echo "No .env.production found"

# Create archive
echo "Creating backup archive..."
cd "$BACKUP_DIR"
tar -czf "backup-$DATE.tar.gz" "$DATE"
rm -rf "$DATE"

echo "Backup completed: backup-$DATE.tar.gz"

# Clean old backups (keep last 7 days)
find "$BACKUP_DIR" -name "backup-*.tar.gz" -mtime +7 -delete

echo "Old backups cleaned up."
EOF

chmod +x /opt/floripacodegurus/backup.sh

# Create SSL directory
echo "🔒 Creating SSL directory..."
mkdir -p /opt/floripacodegurus/ssl

# Create health check script
echo "🏥 Creating health check script..."
cat > /opt/floripacodegurus/health-check.sh << 'EOF'
#!/bin/bash

# Health check script for the Django app
echo "Performing health check..."

# Check if containers are running
if ! docker-compose -f docker-compose-production.yml ps | grep -q "Up"; then
    echo "❌ Containers are not running"
    exit 1
fi

# Check if web service is responding
if ! curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "❌ Web service is not responding"
    exit 1
fi

# Check database connection
if ! docker-compose -f docker-compose-production.yml exec -T db pg_isready -U $POSTGRES_USER > /dev/null 2>&1; then
    echo "❌ Database is not ready"
    exit 1
fi

echo "✅ All health checks passed"
exit 0
EOF

chmod +x /opt/floripacodegurus/health-check.sh

# Set up cron jobs
echo "⏰ Setting up cron jobs..."
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/floripacodegurus/backup.sh") | crontab -
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/floripacodegurus/health-check.sh") | crontab -

echo ""
echo "✅ Server setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Log out and log back in to apply docker group changes"
echo "2. Clone your repository to /opt/floripacodegurus"
echo "3. Configure your environment variables"
echo "4. Deploy using Docker Compose"
echo ""
echo "Useful commands:"
echo "- Monitor app: /opt/floripacodegurus/monitor.sh"
echo "- Check health: /opt/floripacodegurus/health-check.sh"
echo "- Create backup: /opt/floripacodegurus/backup.sh"
echo "- View logs: docker-compose -f docker-compose-production.yml logs -f"
echo ""
echo "⚠️  Don't forget to:"
echo "- Add your SSL certificates to /opt/floripacodegurus/ssl/"
echo "- Configure your domain in production settings"
echo "- Set up your environment variables"
