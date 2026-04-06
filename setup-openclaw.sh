#!/bin/bash
# setup-openclaw.sh - Setup PEACOCK ENGINE with existing OpenClaw (run on VPS)

PEACOCK_DIR="/opt/peacock-engine"
VENV_DIR="$PEACOCK_DIR/.venv"
SERVICE_NAME="peacock-engine"

echo "🦚 PEACOCK ENGINE - OpenClaw Setup"
echo "==================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Check if OpenClaw exists
if ! command -v openclaw &> /dev/null; then
    echo "⚠️  OpenClaw not found in PATH"
    echo "Make sure OpenClaw is installed before running this script"
    exit 1
fi

echo "✅ OpenClaw detected: $(which openclaw)"

# Create directory
echo ""
echo "📁 Creating directory..."
mkdir -p "$PEACOCK_DIR"
cd "$PEACOCK_DIR"

# Clone/pull repo
echo ""
echo "📥 Pulling from GitHub..."
if [ -d .git ]; then
    git pull origin main
else
    echo "❌ Not a git repo. Please clone first:"
    echo "  git clone <your-repo-url> $PEACOCK_DIR"
    exit 1
fi

# Create Python venv
echo ""
echo "🐍 Creating Python environment (.venv)..."
cd "$PEACOCK_DIR"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create systemd service (simple version, no Docker)
echo ""
echo "⚙️  Creating systemd service..."
cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=PEACOCK ENGINE - AI Orchestration Service
After=network.target

[Service]
Type=simple
WorkingDirectory=$PEACOCK_DIR
Environment=PATH=$VENV_DIR/bin
Environment=PYTHONPATH=$PEACOCK_DIR
EnvironmentFile=$PEACOCK_DIR/.env
ExecStart=$VENV_DIR/bin/python -m app.main
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create .env file if doesn't exist
if [ ! -f "$PEACOCK_DIR/.env" ]; then
    echo ""
    echo "🔐 Creating .env file..."
    cat > "$PEACOCK_DIR/.env" << 'EOF'
# PEACOCK ENGINE Environment
# Add your API keys here

GOOGLE_KEYS=your_key_here
GROQ_KEYS=your_key_here
DEEPSEEK_KEYS=your_key_here
MISTRAL_KEYS=your_key_here

PORT=3099
CHAT_UI_ENABLED=true
EOF
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo "   cd $PEACOCK_DIR && nano .env"
fi

# Setup OpenClaw integration
echo ""
echo "🔗 Setting up OpenClaw integration..."
# Add OpenClaw to PATH in service if needed
if ! grep -q "openclaw" /etc/systemd/system/$SERVICE_NAME.service; then
    sed -i "/Environment=PATH/a Environment=PATH=\/usr\/local\/bin:\/usr\/bin:\$PEACOCK_DIR\/.venv\/bin" /etc/systemd/system/$SERVICE_NAME.service
fi

# Reload and enable
echo ""
echo "🚀 Enabling service..."
systemctl daemon-reload
systemctl enable $SERVICE_NAME

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "   1. Edit API keys: sudo nano $PEACOCK_DIR/.env"
echo "   2. Start service: sudo systemctl start $SERVICE_NAME"
echo "   3. Check status: sudo systemctl status $SERVICE_NAME"
echo "   4. View logs: sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "🦚 PEACOCK ENGINE ready!"
