#!/bin/bash
# purge-vps.sh - Clean up the mess from premature deploy (run on VPS as root)

echo "🧹 PEACOCK ENGINE - Purging VPS"
echo "================================"

# Stop and remove service
if systemctl is-active --quiet peacock-engine 2>/dev/null; then
    echo "⏹️  Stopping peacock-engine service..."
    systemctl stop peacock-engine
    systemctl disable peacock-engine 2>/dev/null || true
fi

# Remove service file
if [ -f /etc/systemd/system/peacock-engine.service ]; then
    echo "🗑️  Removing systemd service..."
    rm -f /etc/systemd/system/peacock-engine.service
    systemctl daemon-reload
fi

# Remove installation directory (including .venv)
if [ -d /opt/peacock-engine ]; then
    echo "🗑️  Removing /opt/peacock-engine (including .venv)..."
    rm -rf /opt/peacock-engine
fi

# Remove peacock user (optional - keep if you want)
# if id "peacock" &>/dev/null; then
#     echo "🗑️  Removing peacock user..."
#     userdel -r peacock 2>/dev/null || true
# fi

# Remove config
if [ -d /etc/peacock ]; then
    echo "🗑️  Removing /etc/peacock config..."
    rm -rf /etc/peacock
fi

# Remove Caddy config we added (keep Caddy itself)
if [ -f /etc/caddy/Caddyfile.peacock-backup ]; then
    echo "🔄 Restoring original Caddyfile..."
    mv /etc/caddy/Caddyfile.peacock-backup /etc/caddy/Caddyfile
    systemctl reload caddy 2>/dev/null || true
fi

echo ""
echo "✅ VPS cleaned up!"
echo ""
echo "Next: Pull the repo and run setup-openclaw.sh"
