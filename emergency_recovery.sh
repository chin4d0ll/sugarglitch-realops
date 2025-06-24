#!/bin/bash
# 🚨 Codespace Emergency Recovery Script
# ใช้เมื่อ Codespace crash หรือช้า

echo "🚨 Emergency Recovery Starting..."

# ฆ่า processes ที่กิน resources
pkill -f "node.*high-memory"
pkill -f "python.*memory-intensive"

# ล้าง cache
rm -rf ~/.cache/* 2>/dev/null
find /tmp -type f -mtime +0 -delete 2>/dev/null

# ปรับแต่ง Git
cd /workspaces/sugarglitch-realops 2>/dev/null && {
    git gc --aggressive --prune=now
    git repack -ad
} || echo "Not in git repo"

# รีสตาร์ท services สำคัญ
sudo systemctl restart docker 2>/dev/null || echo "Docker not available"

echo "✅ Emergency recovery completed!"
echo "💡 Consider restarting the Codespace if problems persist"
