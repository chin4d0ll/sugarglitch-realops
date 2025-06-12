#!/bin/bash
# Upload to cloud storage (example with curl)

echo "📤 CLOUD UPLOAD OPTIONS"
echo "======================"

echo "Option 1: Upload via file.io (temporary)"
echo "curl -F 'file=@instagram_dm_extractor.tar.gz' https://file.io"

echo ""
echo "Option 2: Upload to GitHub (if you have repo)"
echo "git add instagram_dm_extractor.tar.gz"
echo "git commit -m 'Add DM extractor package'"
echo "git push"

echo ""  
echo "Option 3: Upload to your cloud service"
echo "- Google Drive"
echo "- Dropbox"
echo "- OneDrive"

echo ""
echo "📁 Current package info:"
ls -lh /workspaces/sugarglitch-realops/instagram_dm_extractor.tar.gz 2>/dev/null || echo "Package not found"
