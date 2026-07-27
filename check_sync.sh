#!/bin/bash
# Checks that local -> GitHub -> Render are all running the same commit.
# Run from inside the project-phoenix-demo folder: ./check_sync.sh

set -e
cd "$(dirname "$0")"

RENDER_URL="https://project-phoenix-demo.onrender.com"

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git ls-remote origin main | awk '{print $1}')

echo "Local HEAD:   $LOCAL"
echo "GitHub main:  $REMOTE"

if [ "$LOCAL" = "$REMOTE" ]; then
  echo "✅ Local matches GitHub — nothing to push."
else
  echo "❌ Local and GitHub differ — run 'git push' (or 'git pull' if GitHub is ahead)."
fi

echo ""
echo "Checking Render deploy..."
RENDER_JSON=$(curl -s "$RENDER_URL/version" || echo "")
RENDER_COMMIT=$(echo "$RENDER_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('commit','unknown'))" 2>/dev/null || echo "unreachable")

echo "Render commit: $RENDER_COMMIT"

if [ "$RENDER_COMMIT" = "$REMOTE" ]; then
  echo "✅ Render is deployed on the same commit as GitHub main."
elif [ "$RENDER_COMMIT" = "unreachable" ] || [ -z "$RENDER_COMMIT" ]; then
  echo "⚠️  Couldn't reach $RENDER_URL/version — Render may still be deploying, or the /version route isn't live yet."
else
  echo "❌ Render is behind GitHub main — check the Render dashboard's Events tab for deploy status."
fi
