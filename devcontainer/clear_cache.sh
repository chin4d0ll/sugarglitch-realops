#!/bin/bash
# 🧹 Cache Cleanup Script - เคลียแคชให้ลื่น
# สำหรับทำความสะอาดระบบให้ทำงานเร็วขึ้น

echo "🧹 เริ่มเคลียแคช..."

# ลบ Python cache
echo "🐍 ลบ Python cache..."
find /workspaces/sugarglitch-realops -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find /workspaces/sugarglitch-realops -name "*.pyc" -delete 2>/dev/null || true
find /workspaces/sugarglitch-realops -name "*.pyo" -delete 2>/dev/null || true

# ลบ log files ที่ใหญ่
echo "📋 ลบ log files ขนาดใหญ่..."
find /workspaces/sugarglitch-realops -name "*.log" -size +10M -delete 2>/dev/null || true

# ลบไฟล์ชั่วคราว
echo "🗑️ ลบไฟล์ชั่วคราว..."
find /workspaces/sugarglitch-realops -name "temp*" -type f -delete 2>/dev/null || true
find /workspaces/sugarglitch-realops -name "*.tmp" -delete 2>/dev/null || true
find /workspaces/sugarglitch-realops -name "*~" -delete 2>/dev/null || true

# ลบ system files
echo "💻 ลบ system files..."
find /workspaces/sugarglitch-realops -name ".DS_Store" -delete 2>/dev/null || true

# เคลียร์ temp directory
echo "📁 เคลียร์ temp directory..."
rm -rf /workspaces/sugarglitch-realops/temp/* 2>/dev/null || true

# ลบ broken virtual environment
echo "🔧 ลบ broken virtual environment..."
rm -rf /workspaces/sugarglitch-realops/.venv 2>/dev/null || true

# สถิติพื้นที่ที่ใช้
echo "📊 ตรวจสอบพื้นที่..."
du -sh /workspaces/sugarglitch-realops/ 2>/dev/null || true

echo "✅ เคลียแคชเสร็จแล้ว! ระบบควรทำงานลื่นขึ้น"
echo "🚀 พร้อมใช้งานแล้ว!"
