#!/bin/bash
# deploy.sh - One-shot deployment script for VPS
# Run this on your VPS after pulling the repo

set -e

PEACOCK_DIR="/opt/peacock-engine"
SERVICE_NAME="peacock-engine"
USER="peacock"

echo "🦚 PEACOCK ENGINE - VPS Deployment Script"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Update system
echo ""
echo "🔄 Updating system packages..."
apt-get update
apt-get upgrade -y

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
apt-get install -y \
    python3-pip \
    python3-venv \
    git \
    curl \
    ufw \
    fail2ban

# Check if Caddy is installed, if not install it
if ! command -v caddy &> /dev/null; then
echo ""
echo "🌐 Installing Caddy..."
    apt-get install -y debian-keyring debian-archive-keyring apt-transport-https
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
    apt-get update
    apt-get install -y caddy
fi

# Create user if doesn't exist
if ! id "$USER" &>/dev/null; then
    echo ""
    echo "👤 Creating peacock user..."
    useradd -r -s /bin/false -d "$PEACOCK_DIR" "$USER"
fi

# Create directory structure
echo ""
echo "📁 Creating directory structure..."
mkdir -p "$PEACOCK_DIR"
mkdir -p "$PEACOCK_DIR/logs"
mkdir -p "$PEACOCK_DIR/uploads"
mkdir -p /etc/peacock

# Copy current directory to installation location
echo ""
echo "📂 Installing PEACOCK ENGINE..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rsync -av --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' "$SCRIPT_DIR/" "$PEACOCK_DIR/"

# Set ownership
chown -R "$USER:$USER" "$PEACOCK_DIR"

# Create virtual environment
echo ""
echo "🐍 Setting up Python environment..."
sudo -u "$USER" bash -c "
    cd $PEACOCK_DIR
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
"

# Create systemd service
echo ""
echo "⚙️  Creating systemd service..."
cat > /etc/systemd/system/$SERVICE_NAME.service << 'EOF'
[Unit]
Description=PEACOCK ENGINE - AI Orchestration Service
After=network.target

[Service]
Type=simple
User=peacock
Group=peacock
WorkingDirectory=/opt/peacock-engine
Environment=PATH=/opt/peacock-engine/.venv/bin
Environment=PYTHONPATH=/opt/peacock-engine
EnvironmentFile=/etc/peacock/env
ExecStart=/opt/peacock-engine/.venv/bin/python -m app.main
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=peacock-engine

[Install]
WantedBy=multi-user.target
EOF

# Create environment file template
echo ""
echo "🔐 Creating environment file..."
if [ ! -f /etc/peacock/env ]; then
    cat > /etc/peacock/env << 'EOF'
# PEACOCK ENGINE Environment Variables
# Add your API keys here

# Google/Gemini API Keys (comma-separated with labels)
GOOGLE_KEYS=LABEL1:key1,LABEL2:key2

# Groq API Keys
GROQ_KEYS=LABEL1:key1,LABEL2:key2

# DeepSeek API Key
DEEPSEEK_KEYS=key1

# Mistral API Key
MISTRAL_KEYS=key1

# Server Configuration
PORT=3099
CHAT_UI_ENABLED=true
PEACOCK_DEBUG=false

# Optional: Proxy/Tunnel
PROXY_ENABLED=false
PROXY_URL=
PEACOCK_TUNNEL=false
EOF
    chmod 600 /etc/peacock/env
    echo "⚠️  IMPORTANT: Edit /etc/peacock/env and add your API keys!"
fi

# Create Caddy config
echo ""
echo "🌐 Configuring Caddy..."
cat > /etc/caddy/Caddyfile << EOF
{
    auto_https off
}

:80 {
    reverse_proxy localhost:3099
    
    # Security headers
    header {
        X-Content-Type-Options nosniff
        X-Frame-Options DENY
        X-XSS-Protection "1; mode=block"
        Referrer-Policy strict-origin-when-cross-origin
    }
    
    # Rate limiting (requires caddy-rate-limit module)
    # rate_limit {
    #     zone static_example {
    #         key static
    #         events 100
    #         window 1m
    #     }
    # }
}

# For HTTPS (when you have a domain)
# yourdomain.com {
#     reverse_proxy localhost:3099
#     tls your@email.com
# }
EOF

# Configure firewall
echo ""
echo "🛡️  Configuring firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 3099/tcp  # PEACOCK ENGINE (direct access)
ufw --force enable

# Configure fail2ban
echo ""
echo "🔒 Configuring fail2ban..."
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[peacock-engine]
enabled = true
port = http,https,3099
filter = peacock-engine
logpath = /var/log/syslog
maxretry = 10
EOF

# Create fail2ban filter for PEACOCK
cat > /etc/fail2ban/filter.d/peacock-engine.conf << EOF
[Definition]
failregex = ^.*PEACOCK.*Failed authentication.*from <HOST>.*$
            ^.*PEACOCK.*Rate limit exceeded.*from <HOST>.*$
ignoreregex =
EOF

# Enable and start services
echo ""
echo "🚀 Starting services..."
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl restart caddy
systemctl restart fail2ban

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "📋 Next Steps:"
echo "   1. Edit API keys: sudo nano /etc/peacock/env"
echo "   2. Start PEACOCK: sudo systemctl start $SERVICE_NAME"
echo "   3. Check status: sudo systemctl status $SERVICE_NAME"
echo "   4. View logs: sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "🌐 Access your instance:"
echo "   - Direct: http://YOUR_VPS_IP:3099"
echo "   - Via Caddy: http://YOUR_VPS_IP"
echo ""
echo "🦚 PEACOCK ENGINE is ready to fly!"
