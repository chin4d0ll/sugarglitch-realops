#!/bin/bash

echo "🚨 Emergency Extension Host Memory Fix Script 🚨"
echo "Found multiple extensionHost processes consuming high memory"

# Kill old extensionHost processes (except newest one)
echo "Killing old extensionHost processes..."
ps aux | grep extensionHost | grep -v grep | sort -k9 | head -n -1 | awk '{print $2}' | xargs -r kill -9

# Clean up extension cache
echo "Cleaning extension cache..."
rm -rf ~/.vscode-remote/extensions/*/node_modules/.cache/* 2>/dev/null
rm -rf ~/.vscode-remote/extensionsCache/*/node_modules/.cache/* 2>/dev/null

# Force garbage collection on remaining processes
echo "Forcing garbage collection..."
ps aux | grep node | grep vscode | awk '{print $2}' | xargs -I {} kill -USR1 {} 2>/dev/null

# Clear temp files
echo "Clearing temp files..."
find /tmp -name "*vscode*" -type f -mmin +30 -delete 2>/dev/null

echo "✅ Extension cleanup completed!"
echo "💡 Restart VS Code if issues persist"

# Show current memory usage
echo ""
echo "Current memory usage:"
free -h
