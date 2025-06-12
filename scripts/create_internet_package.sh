#!/bin/bash
# Complete setup script for internet environment

echo "📦 INSTAGRAM DM EXTRACTOR - INTERNET DEPLOYMENT"
echo "============================================="

# Create deployment archive
echo "🗜️ Creating deployment archive..."
cd /workspaces/sugarglitch-realops
tar -czf instagram_dm_extractor.tar.gz deploy_package/

echo ""
echo "✅ Deployment package created: instagram_dm_extractor.tar.gz"
echo ""
echo "🌐 TO RUN IN INTERNET ENVIRONMENT:"
echo "=================================="
echo ""
echo "1. Transfer instagram_dm_extractor.tar.gz to your internet machine"
echo ""
echo "2. Extract and run:"
echo "   tar -xzf instagram_dm_extractor.tar.gz"
echo "   cd deploy_package"
echo "   chmod +x run.sh"
echo "   ./run.sh"
echo ""
echo "3. Alternative manual run:"
echo "   cd deploy_package"
echo "   pip3 install -r requirements.txt"
echo "   python3 final_real_dm_extractor.py"
echo ""
echo "📊 Expected output:"
echo "   data/REAL_ALX_TRADING_DMS_*.json"
echo ""
echo "🎯 This will extract REAL Instagram DMs from alx.trading account"
echo "🛡️ With advanced rate limiting protection"
