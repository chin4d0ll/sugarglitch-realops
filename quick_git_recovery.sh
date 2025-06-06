#!/bin/bash
# 🌸 Quick Git Recovery Commands สำหรับ chin4d0ll
echo "🌸 Quick Git Recovery Commands"
echo "💖 Girly Hacker Edition"
echo "=" * 40

echo "📊 1. ตรวจสอบสถานะ Git:"
git status
echo ""

echo "📚 2. ดู commits ล่าสุด:"
git log --oneline -10
echo ""

echo "🔍 3. ดูไฟล์ที่เปลี่ยนแปลงใน commit ล่าสุด:"
git show --name-status HEAD
echo ""

echo "🗑️ 4. ดูไฟล์ที่ถูกลบ:"
git log --diff-filter=D --summary | grep delete
echo ""

echo "💾 5. กู้คืนไฟล์ที่ถูกลบ (ตัวอย่าง):"
echo "git checkout HEAD~1 -- filename.py"
echo ""

echo "🔄 6. ย้อนกลับไปยัง commit ก่อนหน้า:"
echo "git reset --hard HEAD~1"
echo ""

echo "🌸 7. ดูประวัติการเปลี่ยนแปลงของไฟล์:"
echo "git log --follow -- filename.py"