#!/bin/bash

# Instagram DM Extractor - Auto Run Script
# ติดตั้งและรันโปรแกรมดึง DM อัตโนมัติ

echo "🔧 Instagram DM Extractor - Auto Setup & Run"
echo "=============================================="

# ตรวจสอบ Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 ไม่พบ กรุณาติดตั้ง Python3 ก่อน"
    exit 1
fi

echo "✅ พบ Python3"

# ติดตั้ง pip packages
echo "📦 ติดตั้ง Python packages..."
pip3 install playwright asyncio

# ติดตั้ง chromium
echo "🌐 ติดตั้ง Chromium browser..."
playwright install chromium

echo ""
echo "🚀 พร้อมใช้งาน! เลือกสิ่งที่ต้องการทำ:"
echo ""
echo "1. ดึง DM จาก Instagram (ต้องมี sessionid)"
echo "2. แปลง JSON เป็น HTML"
echo "3. แปลง HTML เป็น PDF"
echo "4. รันทั้งหมดตามลำดับ"
echo ""

read -p "เลือก (1-4): " choice

case $choice in
    1)
        echo "🎯 เริ่มดึง DM..."
        python3 dm_extractor.py
        ;;
    2)
        echo "🔄 แปลง JSON เป็น HTML..."
        python3 json_to_html_converter.py
        ;;
    3)
        echo "📄 แปลง HTML เป็น PDF..."
        python3 html_to_pdf_converter.py
        ;;
    4)
        echo "🎯 ขั้นตอนที่ 1: ดึง DM..."
        python3 dm_extractor.py
        
        if [ -f "dm_output.json" ]; then
            echo "🔄 ขั้นตอนที่ 2: แปลง JSON เป็น HTML..."
            python3 json_to_html_converter.py
            
            if [ -f "dm_output.html" ]; then
                echo "📄 ขั้นตอนที่ 3: แปลง HTML เป็น PDF..."
                python3 html_to_pdf_converter.py
            fi
        fi
        ;;
    *)
        echo "❌ ตัวเลือกไม่ถูกต้อง"
        exit 1
        ;;
esac

echo ""
echo "🎉 เสร็จสิ้น! ตรวจสอบไฟล์ผลลัพธ์:"
echo ""

if [ -f "dm_output.json" ]; then
    echo "✅ dm_output.json - ข้อมูล DM ดิบ"
fi

if [ -f "dm_output.html" ]; then
    echo "✅ dm_output.html - รายงาน HTML"
fi

if [ -f "dm_output.pdf" ]; then
    echo "✅ dm_output.pdf - รายงาน PDF"
fi

echo ""
echo "💡 เคล็ดลับ: sessionid หาได้จาก F12 > Application > Cookies > instagram.com"
