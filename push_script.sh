#!/bin/bash
echo "Trying to push to GitHub..."
# Use GITHUB_TOKEN if available
if [ -n "$GITHUB_TOKEN" ]; then
    git remote set-url origin https://${GITHUB_TOKEN}@github.com/chin4d0ll/sugarglitch-realops.git
    git push origin main
else
    # Try with stored credentials
    git push origin main
fi
