# 🔧 FIX DEPLOYMENT - Step by Step

## What Happened?
You ran `deploy.sh` on the VPS before pushing from your local machine.

## How to Fix It?

### STEP 1: On Your LOCAL Machine (do this first!)
```bash
cd /home/flintx/ai-handler
./push-to-github.sh
```
This pushes all the PEACOCK ENGINE code to GitHub.

---

### STEP 2: On Your VPS (clean up the mess)
```bash
ssh your-vps-ip
sudo ./purge-vps.sh
```
This removes everything that was prematurely installed.

---

### STEP 3: On Your VPS (proper setup)
```bash
cd /opt/peacock-engine  # or wherever you want it
git clone <your-github-repo-url> .
sudo ./setup-openclaw.sh
```

---

### STEP 4: Configure & Start
```bash
# Add your API keys
sudo nano /opt/peacock-engine/.env

# Start it
sudo systemctl start peacock-engine

# Check it's running
sudo systemctl status peacock-engine
```

---

## Scripts Explained

| Script | Run On | Purpose |
|--------|--------|---------|
| `push-to-github.sh` | Local | Push code to GitHub |
| `purge-vps.sh` | VPS | Clean up premature deploy |
| `setup-openclaw.sh` | VPS | Proper setup with your OpenClaw |

---

## What About Docker?

**NO DOCKER!** The `setup-openclaw.sh` uses:
- Python `.venv` (local to project)
- systemd service
- Your existing OpenClaw installation

---

## Quick Reference

```bash
# LOCAL MACHINE
cd /home/flintx/ai-handler
./push-to-github.sh

# VPS
ssh your-vps
sudo ./purge-vps.sh
cd /opt/peacock-engine
git pull
sudo ./setup-openclaw.sh
sudo nano .env  # add keys
sudo systemctl start peacock-engine
```

🦚 Good luck!
