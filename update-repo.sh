#!/bin/bash
# update-repo.sh - Commit and push all changes to repo
# Run this on your local machine before deploying to VPS

set -e

echo "🦚 PEACOCK ENGINE - Repo Update Script"
echo "========================================"

# Check if we're in a git repo
if [ ! -d .git ]; then
    echo "❌ Not a git repository!"
    exit 1
fi

# Show what will be committed
echo ""
echo "📋 Changes to be committed:"
git status --short

# Add all changes
echo ""
echo "➕ Adding all changes..."
git add .

# Commit with timestamp
COMMIT_MSG="WebUI API + Token Counters + Deployment Ready - $(date '+%Y-%m-%d %H:%M')"
echo ""
echo "💾 Committing: $COMMIT_MSG"
git commit -m "$COMMIT_MSG" || echo "⚠️  Nothing to commit or commit failed"

# Push to remote
echo ""
echo "🚀 Pushing to remote..."
git push origin $(git branch --show-current) || echo "⚠️  Push failed - check remote config"

echo ""
echo "✅ Repo updated!"
echo ""
echo "Next steps on your VPS:"
echo "  1. git pull origin main"
echo "  2. chmod +x deploy.sh"
echo "  3. sudo ./deploy.sh"
