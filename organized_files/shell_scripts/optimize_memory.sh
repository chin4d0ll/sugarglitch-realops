#!/bin/bash

# SugarGlitch RealOps Memory Optimization Script
# This script optimizes memory usage to reduce RAM consumption

echo "🔧 Starting Memory Optimization..."

# Kill any hung VS Code extension processes
echo "📝 Cleaning up VS Code extension processes..."
pkill -f "extensionHost" 2>/dev/null || true
pkill -f "node.*vscode" 2>/dev/null || true

# Clear system caches
echo "🧹 Clearing system caches..."
sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || sudo sync && sudo echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true

# Clear Python cache
echo "🐍 Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Clear npm cache
echo "📦 Clearing npm cache..."
npm cache clean --force 2>/dev/null || true

# Optimize Node.js memory
echo "⚡ Setting Node.js memory limits..."
export NODE_OPTIONS="--max-old-space-size=1024"

# Force garbage collection in Python
echo "🗑️ Forcing garbage collection..."
python3 -c "import gc; gc.collect()" 2>/dev/null || true

# Clear temporary files
echo "🗂️ Clearing temporary files..."
rm -rf /tmp/npm-* 2>/dev/null || true
rm -rf /tmp/node-* 2>/dev/null || true
rm -rf ~/.cache/pip 2>/dev/null || true

# Show memory usage
echo "📊 Current memory usage:"
free -h || echo "Memory info not available"

echo "✅ Memory optimization complete!"
echo "💡 Tip: Run this script regularly to keep memory usage low"
