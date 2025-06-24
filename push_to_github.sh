#!/bin/bash

echo "🚀 ===== Push โปรเจกต์ขึ้น GitHub ====="

# ตั้งค่า environment variables
export GIT_COMMITTER_EMAIL="developer@example.com"
export GIT_COMMITTER_NAME="Developer"  
export GIT_AUTHOR_EMAIL="developer@example.com"
export GIT_AUTHOR_NAME="Developer"

# ตรวจสอบว่ามี remote repository
if git remote get-url origin > /dev/null 2>&1; then
    echo "📡 พบ remote repository: $(git remote get-url origin)"
else
    echo "❌ ไม่พบ remote repository"
    echo "ใช้คำสั่ง: git remote add origin <repository-url>"
    exit 1
fi

# ตรวจสอบสถานะ Git
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  มีไฟล์ที่ยังไม่ได้ commit"
    echo "กำลัง commit ก่อน push..."
    git add .
    git commit -m "Auto commit before push" --no-gpg-sign --no-verify
fi

# Push ขึ้น GitHub
echo "📤 กำลัง push ขึ้น GitHub..."
if git push origin main; then
    echo "✅ Push สำเร็จ!"
    echo "🌟 โปรเจกต์ได้ถูกอัพโหลดขึ้น GitHub แล้ว"
    echo "🔗 ดูที่: $(git remote get-url origin)"
else
    echo "❌ Push ล้มเหลว"
    echo "ลองใช้คำสั่ง: git push --set-upstream origin main"
fi

echo "===== เสร็จสิ้น ====="
