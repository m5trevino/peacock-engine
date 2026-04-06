# PEACOCK ENGINE - Deployment Guide

## Quick Deploy (2 minutes)

### Step 1: Update Repo (Local Machine)
```bash
cd /home/flintx/ai-handler
chmod +x update-repo.sh
./update-repo.sh
```

### Step 2: On Your VPS
```bash
# SSH into your VPS
ssh user@your-vps-ip

# Clone/pull the repo
cd /opt
git clone <your-repo-url> peacock-engine
# OR if already exists:
cd peacock-engine && git pull origin main

# Run deployment
chmod +x deploy.sh
sudo ./deploy.sh
```

### Step 3: Configure & Start
```bash
# Add your API keys
sudo nano /etc/peacock/env

# Start the service
sudo systemctl start peacock-engine

# Check status
sudo systemctl status peacock-engine

# View logs
sudo journalctl -u peacock-engine -f
```

## Access Your Instance

- **Direct API**: `http://YOUR_VPS_IP:3099`
- **Via Caddy**: `http://YOUR_VPS_IP`
- **Health Check**: `http://YOUR_VPS_IP:3099/health`

## Files Created

| File | Purpose |
|------|---------|
| `/opt/peacock-engine/` | Installation directory |
| `/etc/peacock/env` | Environment variables (API keys) |
| `/etc/systemd/system/peacock-engine.service` | Systemd service |
| `/etc/caddy/Caddyfile` | Reverse proxy config |
| `/etc/fail2ban/jail.local` | Security config |

## Commands

```bash
# Start/Stop/Restart
sudo systemctl start peacock-engine
sudo systemctl stop peacock-engine
sudo systemctl restart peacock-engine

# View logs
sudo journalctl -u peacock-engine -f

# Update (after git pull)
sudo systemctl restart peacock-engine
```

## Security

- Firewall enabled (UFW)
- Fail2ban configured
- Caddy reverse proxy
- Service runs as non-root user
- API keys in secure location (`/etc/peacock/env`)

## Troubleshooting

**Service won't start?**
```bash
sudo journalctl -u peacock-engine -n 50
```

**Check API keys are set:**
```bash
sudo cat /etc/peacock/env
```

**Port already in use?**
```bash
sudo lsof -i :3099
sudo systemctl restart peacock-engine
```
