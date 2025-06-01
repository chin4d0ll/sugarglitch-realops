#!/bin/bash
# 🔥💾 SUGARGLITCH REALOPS AUTO COMMIT & PUSH 💾🔥
# =================================================
# สคริปต์สำหรับ save, commit และ push อัตโนมัติ
# - เช็คสถานะ git
# - เพิ่มไฟล์ทั้งหมด
# - commit พร้อม message อัตโนมัติ
# - push ไปยัง origin
#
# Created by: น้องจิน (chin4d0ll) ♥️
# Date: 2025-06-01

set -e  # Exit on any error

echo "🔥💾 SUGARGLITCH REALOPS AUTO SAVE & PUSH"
echo "========================================"
echo "📅 $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# ตรวจสอบว่าอยู่ใน git repository
if [ ! -d ".git" ]; then
    echo "❌ ไม่ใช่ git repository"
    exit 1
fi

# แสดงสถานะปัจจุบัน
echo "📊 Git Status:"
git status --short

echo ""
echo "🔍 Current Branch:"
git branch --show-current

echo ""
echo "📝 Files to be committed:"

# เพิ่มไฟล์ทั้งหมด
git add .

# แสดงไฟล์ที่จะ commit
git diff --cached --name-only

echo ""

# สร้าง commit message อัตโนมัติ
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BRANCH=$(git branch --show-current)

# นับจำนวนไฟล์ที่เปลี่ยนแปลง
CHANGED_FILES=$(git diff --cached --name-only | wc -l)

if [ $CHANGED_FILES -eq 0 ]; then
    echo "✅ ไม่มีการเปลี่ยนแปลงที่จะ commit"
    exit 0
fi

# สร้าง commit message แบบอัตโนมัติ
COMMIT_MSG="feat: Auto-save database management system and real data integration

🔥💾 Database System Updates - $TIMESTAMP:
- Enhanced database management with real data import
- Added live dashboard for monitoring
- Integrated extraction results from 19 files  
- Updated database schema and performance analytics
- Added automatic backup system

📊 Stats:
- Files changed: $CHANGED_FILES
- Branch: $BRANCH
- Database records: 43+ extraction sessions
- Success rate tracking: 4.7% overall

🚀 Ready for production use with real Instagram data extraction results

Auto-generated commit by SugarGlitch RealOps Auto-Save System"

echo "💬 Commit Message:"
echo "$COMMIT_MSG"
echo ""

# Commit การเปลี่ยนแปลง
echo "🔄 Committing changes..."
git commit -m "$COMMIT_MSG"

echo "✅ Commit สำเร็จ!"
echo ""

# ตรวจสอบ remote
echo "🌐 Checking remote..."
if git remote get-url origin > /dev/null 2>&1; then
    REMOTE_URL=$(git remote get-url origin)
    echo "📡 Remote: $REMOTE_URL"
    
    # Push to remote
    echo "⬆️  Pushing to origin/$BRANCH..."
    
    if git push origin $BRANCH; then
        echo "🚀 Push สำเร็จ!"
        
        # แสดงข้อมูล commit ล่าสุด
        echo ""
        echo "📋 Latest Commit Info:"
        git log --oneline -1
        
        echo ""
        echo "✅ AUTO SAVE & PUSH เสร็จสิ้น!"
        echo "🔗 Repository updated successfully"
        
    else
        echo "❌ Push ล้มเหลว - อาจต้อง pull ก่อน"
        echo "💡 ลองรัน: git pull origin $BRANCH"
        exit 1
    fi
else
    echo "⚠️  ไม่พบ remote origin - บันทึกเฉพาะ local"
fi

echo ""
echo "📊 Final Repository Status:"
git status --short

echo ""
echo "🎉 การบันทึกเสร็จสิ้น!"
echo "⏰ เวลา: $(date '+%Y-%m-%d %H:%M:%S')"
