#!/bin/bash

# VS Code Extension Memory Fix Script
# This script fixes memory issues with VS Code extensions

echo "🔧 Fixing VS Code Extension Memory Issues..."

# Kill all extension host processes
echo "🔄 Stopping extension host processes..."
pkill -f "extensionHost" 2>/dev/null || echo "No extension host processes found"

# Clear extension cache
echo "🧹 Clearing extension cache..."
rm -rf ~/.vscode-server/extensions/.cache 2>/dev/null || true
rm -rf ~/.vscode/extensions/.cache 2>/dev/null || true

# Clear VS Code workspace cache
echo "🗂️ Clearing workspace cache..."
rm -rf ~/.vscode-server/data/User/workspaceStorage/* 2>/dev/null || true
rm -rf ~/.vscode/User/workspaceStorage/* 2>/dev/null || true

# Force garbage collection
echo "🗑️ Forcing memory cleanup..."
echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || sudo echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true

# Check memory usage
echo "📊 Memory status:"
free -h 2>/dev/null || echo "Memory info not available"

echo "✅ Extension fix complete!"
echo "🔄 Please restart VS Code to apply changes"
