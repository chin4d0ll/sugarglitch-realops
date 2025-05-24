#!/bin/bash
# 🧪 ขั้นตอนการทดสอบ SugarGlitch อย่างมีจริยธรรม

echo "🔬 ชุดการทดสอบ SugarGlitch อย่างมีจริยธรรม"
echo "============================================="
echo "⚠️  เตือน: ทดสอบเฉพาะบัญชีของคุณเองเท่านั้น!"
echo ""

# ขั้นตอนที่ 1: ตรวจสอบ session
echo "📋 ขั้นตอนที่ 1: กำลังตรวจสอบ session..."
python validate_session.py
if [ $? -ne 0 ]; then
    echo "❌ การตรวจสอบ session ล้มเหลว กรุณาแก้ไข session.json ก่อน"
    exit 1
fi

echo ""
echo "📋 ขั้นตอนที่ 2: ทดสอบการเชื่อมต่อ Browser API..."
node browser_api.js

echo ""
echo "📋 ขั้นตอนที่ 3: ทดสอบการเชื่อมต่อ proxy..."
python test_proxy.py

echo ""
echo "📋 ขั้นตอนที่ 4: รันการวิเคราะห์หลัก..."
python main.py

echo ""
echo "✅ การทดสอบเสร็จสิ้น!"
echo "📄 ตรวจสอบโฟลเดอร์ export/ สำหรับผลลัพธ์"
echo "🔍 ตรวจทาน logs หากมีปัญหาใดๆ"
