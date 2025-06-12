#!/bin/bash
# Create DM extractor on internet machine

echo "🏗️ CREATE DM EXTRACTOR ON INTERNET MACHINE"
echo "=========================================="

echo "1. Create directory:"
echo "mkdir -p instagram_dm_extractor/{sessions,data}"
echo "cd instagram_dm_extractor"

echo ""
echo "2. Create session file:"
echo 'cat > sessions/session-alx.trading << EOF'
echo '{"cookies": {"sessionid": "82d00883%3A1748264421%3A6f473b1c8d0b8d51"}}'
echo 'EOF'

echo ""
echo "3. Create requirements.txt:"
echo 'cat > requirements.txt << EOF'
echo 'requests>=2.28.0'
echo 'urllib3>=1.26.0'
echo 'aiohttp>=3.8.0'
echo 'EOF'

echo ""
echo "4. Download main script:"
echo "# Copy the content from final_real_dm_extractor.py and save as extractor.py"

echo ""
echo "5. Run:"
echo "pip3 install -r requirements.txt"
echo "python3 extractor.py"
