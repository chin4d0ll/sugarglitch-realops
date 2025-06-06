#!/bin/bash
# Fleming Integrated Launcher
# Automated startup script for Fleming Integration

echo "🔥💎 FLEMING INTEGRATED LAUNCHER 2025 💎🔥"
echo "=========================================="
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Check for Python
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo "❌ Python not found. Please install Python 3."
    exit 1
fi

# Check for virtual environment
if [ -d ".venv/bin" ]; then
    echo "🔄 Activating virtual environment..."
    source .venv/bin/activate
fi

# Install required dependencies
echo "🔧 Checking requirements..."
$PYTHON -m pip install -q instagrapi fpdf2 Pillow

# Run Fleming integrated launcher
echo "🚀 Starting Fleming operations..."
$PYTHON fleming_integrated_launcher.py

echo ""
echo "✅ Fleming operations completed"