#!/bin/bash
# 🚨 Emergency cleanup script

echo "🚨 EMERGENCY CLEANUP INITIATED 🚨"

# Kill any running Python processes related to Instagram
pkill -f "instagrapi"
pkill -f "instagram"
pkill -f "dm_extractor"

# Clear temporary files
rm -f session_*.json
rm -f *.tmp
rm -f *.log

# Clear memory cache
sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || echo "⚠️ Cache clear requires sudo"

echo "✅ Emergency cleanup completed!"
