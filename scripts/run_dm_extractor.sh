#!/bin/bash
# 🎯 INSTAGRAM DM EXTRACTOR - AUTO RUN
# =====================================
# รันเลยทันที! สายแฮกระดับเทพ

echo "🎯 INSTAGRAM DM EXTRACTOR - สายแฮกระดับเทพ!"
echo "=================================================="
echo "🎯 Target: alx.trading (your account)"
echo "📱 Session: session-alx.trading"
echo "⚡ Mode: Quick & Safe"
echo ""

# ตรวจสอบ session
echo "🔍 Checking session..."
if [ -f "/workspaces/sugarglitch-realops/sessions/session-alx.trading" ]; then
    echo "✅ Session file found!"
    SESSION_INFO=$(cat /workspaces/sugarglitch-realops/sessions/session-alx.trading)
    echo "📊 Session: ${SESSION_INFO:0:50}..."
else
    echo "❌ Session file not found!"
    exit 1
fi

echo ""
echo "🚀 Starting DM extraction..."
echo "Choose your weapon:"
echo ""
echo "1) 🔥 Quick & Simple (Recommended)"
echo "2) 🛡️ Advanced Protected"  
echo "3) ⚡ Real-Time API"
echo "4) 📱 Session Tester"
echo ""

read -p "Enter choice (1-4): " choice

cd /workspaces/sugarglitch-realops

case $choice in
    1)
        echo "🔥 Running Quick DM Extractor..."
        python3 quick_dm_extractor.py
        ;;
    2)
        echo "🛡️ Running Advanced Protected Extractor..."
        python3 final_real_dm_extractor.py
        ;;
    3)
        echo "⚡ Running Real-Time API Extractor..."
        python3 src/instagram_tools/real_instagram_dm_extractor.py
        ;;
    4)
        echo "📱 Running Session Tester..."
        python3 instagram_session_tester.py
        ;;
    *)
        echo "❌ Invalid choice. Running default (Session Tester)..."
        python3 instagram_session_tester.py
        ;;
esac

echo ""
echo "🎉 Extraction completed!"
echo "📂 Check results in:"
ls -la *DM*.json 2>/dev/null || echo "   No DM files found"
ls -la *EXTRACTION*.json 2>/dev/null || echo "   No extraction files found"
echo ""
echo "🎯 Happy Hacking! 🔥"
