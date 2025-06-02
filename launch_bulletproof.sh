#!/bin/bash
# 🥷 Quick launcher for Bulletproof DM Extractor

echo "🥷💖 LAUNCHING BULLETPROOF DM EXTRACTOR 💖🥷"
echo "=============================================="

# Activate virtual environment
if [[ -d "venv_bulletproof" ]]; then
    source venv_bulletproof/bin/activate
    echo "✅ Virtual environment activated"
fi

# Run the extractor
python3 advanced_dm_extractor_bulletproof_2025.py

echo "🎉 Bulletproof extraction completed!"
