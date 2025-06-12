#!/bin/bash
# Quick VSCode Emergency Fix Script
# Run this when VSCode crashes or becomes unresponsive

echo "🚨 VSCode Emergency Fix - Quick Recovery"
echo "======================================="

# Check current memory usage
echo "💾 Current Memory Usage:"
free -h | grep -E "(Mem|Swap)"

# Find and kill problematic VSCode processes
echo ""
echo "🔍 Finding problematic VSCode processes..."
HEAVY_PROCESSES=$(ps aux --sort=-%mem | grep -E "(extensionHost|Pylance)" | awk '$4 > 5.0 {print $2}')

if [ -n "$HEAVY_PROCESSES" ]; then
    echo "🎯 Found heavy processes using >5% memory:"
    echo "$HEAVY_PROCESSES"
    echo ""
    echo "💀 Terminating heavy processes..."
    echo "$HEAVY_PROCESSES" | xargs -r kill -TERM
    sleep 2
    echo "✅ Heavy processes terminated"
else
    echo "✅ No heavy processes found"
fi

# Clear temp files quickly
echo ""
echo "🧹 Quick cleanup..."
find /workspaces/sugarglitch-realops -name "*.pyc" -delete 2>/dev/null
find /workspaces/sugarglitch-realops -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
echo "✅ Temp files cleaned"

# Check if we have enough memory now
echo ""
echo "📊 Memory after cleanup:"
free -h | grep Mem

echo ""
echo "🔄 Recovery complete! Try reloading VSCode now:"
echo "   Ctrl+Shift+P -> 'Developer: Reload Window'"
echo ""
echo "🆘 If still crashing:"
echo "   1. Save all work"
echo "   2. Restart the entire Codespace"
echo "   3. Consider upgrading Codespace size"
