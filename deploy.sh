#!/bin/bash

echo "🎯 ===== One-Click Deploy ====="
echo "ทำ commit และ push ขึ้น GitHub ในขั้นตอนเดียว"
echo ""

# รับข้อความ commit จากผู้ใช้
if [ -z "$1" ]; then
    echo "📝 กรุณาระบุข้อความ commit:"
    echo "ใช้งาน: ./deploy.sh \"ข้อความ commit\""
    exit 1
fi

COMMIT_MESSAGE="$1"

echo "1. 🧹 ทำความสะอาดโปรเจกต์..."
./clear_cache.sh > /dev/null 2>&1

echo "2. 📦 Commit การเปลี่ยนแปลง..."
./easy_commit.sh "$COMMIT_MESSAGE"

echo "3. 🚀 Push ขึ้น GitHub..."
./push_to_github.sh

echo ""
echo "✅ Deploy เสร็จสิ้น!"
echo "🔗 Repository: https://github.com/chin4d0ll/sugarglitch-realops"
echo "🌟 โปรเจกต์ของคุณอยู่บน GitHub แล้ว!"
