#!/bin/bash
# push-to-github.sh - Push all changes to GitHub (run on LOCAL machine)

set -e

echo "🦚 PEACOCK ENGINE - Push to GitHub"
echo "==================================="

# Check git status
echo ""
echo "📋 Current status:"
git status --short

# Add everything
echo ""
echo "➕ Adding all files..."
git add -A

# Commit
echo ""
echo "💾 Committing..."
git commit -m "PEACOCK ENGINE v3.0 - WebUI APIs, Token Counters, Deployment Ready" || echo "⚠️  Nothing new to commit"

# Push
echo ""
echo "🚀 Pushing to GitHub..."
git push origin $(git branch --show-current)

echo ""
echo "✅ Pushed to GitHub!"
echo ""
echo "Now on your VPS, run:"
echo "  ./purge-and-setup.sh"
