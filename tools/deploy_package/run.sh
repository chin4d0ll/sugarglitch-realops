#!/bin/bash
# Instagram DM Extractor - Internet Environment Runner

echo "🚀 Instagram DM Extractor - Real Internet Environment"
echo "=================================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.7+"
    exit 1
fi

# Install requirements
echo "📦 Installing Python requirements..."
pip3 install -r requirements.txt

# Verify session file
if [ ! -f "sessions/session-alx.trading" ]; then
    echo "❌ Session file not found: sessions/session-alx.trading"
    exit 1
fi

echo "✅ Session file found"

# Create data directory
mkdir -p data

echo ""
echo "🎯 Starting REAL Instagram DM extraction..."
echo "📱 Target: alx.trading account"
echo "🛡️ Protection: Cute rate limiting enabled"
echo ""

# Run the extractor
python3 final_real_dm_extractor.py

# Check results
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Extraction completed!"
    echo "📂 Check data/ folder for results:"
    ls -la data/REAL_ALX_TRADING_DMS_*.json 2>/dev/null || echo "   (No output files found)"
else
    echo ""
    echo "❌ Extraction failed"
    echo "💡 Check network connectivity and session validity"
fi
