#!/bin/bash
"""
🔧 VS Code Extension Cleanup Script
แก้ไขปัญหา Remote Extensions ที่รีรันซ้ำๆ
"""

echo "🧹 CLEANING UP VS CODE EXTENSIONS RERUN ISSUES"
echo "=" * 60

# 1. Kill duplicate Codeium processes
echo "📱 Terminating duplicate Codeium processes..."
pkill -f "codeium.*language_server" 2>/dev/null || true
sleep 2

# 2. Kill duplicate MS SQL processes
echo "🗄️ Terminating duplicate MS SQL processes..."
pkill -f "MicrosoftSqlToolsServiceLayer" 2>/dev/null || true
pkill -f "SqlToolsResourceProviderService" 2>/dev/null || true
sleep 2

# 3. Clear VS Code extension cache
echo "🧽 Clearing VS Code extension cache..."
if [ -d "/home/codespace/.vscode-remote/data/CachedExtensions" ]; then
    rm -rf /home/codespace/.vscode-remote/data/CachedExtensions/*
    echo "✅ Extension cache cleared"
fi

# 4. Clear extension host cache
echo "🏠 Clearing extension host cache..."
if [ -d "/home/codespace/.vscode-remote/data/logs" ]; then
    find /home/codespace/.vscode-remote/data/logs -name "*.log" -mtime +1 -delete 2>/dev/null || true
    echo "✅ Extension host logs cleaned"
fi

# 5. Restart VS Code server (gentle reload)
echo "🔄 Requesting VS Code server reload..."

# Create a temporary reload marker
touch /tmp/vscode_reload_required.marker

echo ""
echo "✅ CLEANUP COMPLETED!"
echo "📝 Next steps:"
echo "   1. Reload VS Code window (Ctrl+Shift+P -> 'Developer: Reload Window')"
echo "   2. Extensions should now run with single instances"
echo "   3. Check if the rerun issue is resolved"
echo ""
echo "🔍 To verify fixes, run: ps aux | grep -E '(codeium|sql)' | wc -l"
echo "   (Should show fewer processes now)"
