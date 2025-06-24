#!/bin/bash

echo "🚀 ===== การบำรุงรักษาโปรเจกต์ ====="

# เคลียร์แคชทั้งหมด
echo "1. 🧹 เคลียร์แคช..."
./clear_cache.sh > /dev/null 2>&1

# ตรวจสอบขนาดโปรเจกต์
echo "2. 📊 ตรวจสอบขนาดโปรเจกต์..."
CURRENT_SIZE=$(du -sh . 2>/dev/null | cut -f1)
echo "   ขนาดปัจจุบัน: $CURRENT_SIZE"

# ตรวจสอบจำนวนไฟล์
echo "3. 📁 จำนวนไฟล์:"
echo "   - Python files: $(find . -name "*.py" | wc -l)"
echo "   - Text files: $(find . -name "*.txt" | wc -l)"
echo "   - JSON files: $(find . -name "*.json" | wc -l)"
echo "   - Shell scripts: $(find . -name "*.sh" | wc -l)"

# Git status
echo "4. 📋 Git status:"
if git rev-parse --git-dir > /dev/null 2>&1; then
    UNCOMMITTED=$(git status --porcelain | wc -l)
    if [ $UNCOMMITTED -eq 0 ]; then
        echo "   ✅ ไม่มีไฟล์ที่ยังไม่ได้ commit"
    else
        echo "   ⚠️  มีไฟล์ $UNCOMMITTED ไฟล์ที่ยังไม่ได้ commit"
    fi
else
    echo "   ❌ ไม่ใช่ Git repository"
fi

# แนะนำการปรับปรุง
echo "5. 💡 คำแนะนำ:"
if [ $(find . -name "*.pyc" | wc -l) -gt 0 ]; then
    echo "   - พบไฟล์ .pyc ที่ควรลบ"
fi

if [ ! -f .gitignore ]; then
    echo "   - ควรสร้างไฟล์ .gitignore"
fi

echo ""
echo "✅ การบำรุงรักษาเสร็จสิ้น!"
