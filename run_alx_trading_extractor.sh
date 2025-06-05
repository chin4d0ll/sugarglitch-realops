#!/bin/bash

# alx.trading DM Extractor - Auto Run
# ดึง DM จาก alx.trading โดยเฉพาะ

clear
echo "📈 alx.trading DM Extractor"
echo "============================"
echo ""

# ตรวจสอบ Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 ไม่พบ กรุณาติดตั้ง Python3 ก่อน"
    exit 1
fi

echo "✅ พบ Python3"

# ตรวจสอบ playwright
if ! python3 -c "import playwright" 2>/dev/null; then
    echo "📦 ติดตั้ง Playwright..."
    pip3 install playwright
    playwright install chromium
else
    echo "✅ พบ Playwright"
fi

echo ""
echo "🎯 Target: alx.trading"
echo "📱 Platform: Instagram DM"
echo ""

# เลือกการทำงาน
echo "เลือกสิ่งที่ต้องการทำ:"
echo ""
echo "1. 🔍 ดึง DM จาก alx.trading (ต้องมี sessionid)"
echo "2. 📄 แปลงข้อมูลเป็น HTML Report"
echo "3. 🚀 ทำทั้งหมดตามลำดับ"
echo "4. 📊 ดูข้อมูลที่มีอยู่"
echo ""

read -p "เลือก (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🎯 เริ่มดึง DM จาก alx.trading..."
        echo "💡 Tips: sessionid หาได้จาก F12 > Application > Cookies > instagram.com"
        echo ""
        python3 alx_trading_dm_extractor.py
        ;;
    2)
        echo ""
        echo "📄 แปลงข้อมูลเป็น HTML Report..."
        python3 alx_trading_html_converter.py
        ;;
    3)
        echo ""
        echo "🚀 รันแบบครบชุด..."
        echo ""
        echo "Step 1: ดึง DM จาก alx.trading"
        python3 alx_trading_dm_extractor.py
        
        if ls alx_trading_dm_*.json 1> /dev/null 2>&1; then
            echo ""
            echo "Step 2: แปลงเป็น HTML Report"
            python3 alx_trading_html_converter.py
        else
            echo "❌ ไม่พบไฟล์ข้อมูล - การดึง DM อาจไม่สำเร็จ"
        fi
        ;;
    4)
        echo ""
        echo "📊 ไฟล์ข้อมูลที่มีอยู่:"
        echo "===================="
        
        json_files=$(ls alx_trading_dm_*.json 2>/dev/null | wc -l)
        html_files=$(ls alx_trading_report_*.html 2>/dev/null | wc -l)
        
        if [ $json_files -gt 0 ]; then
            echo "📄 ไฟล์ JSON: $json_files ไฟล์"
            ls -la alx_trading_dm_*.json | while read line; do
                echo "  📋 $line"
            done
        else
            echo "📄 ไฟล์ JSON: ไม่มี"
        fi
        
        echo ""
        
        if [ $html_files -gt 0 ]; then
            echo "🌐 ไฟล์ HTML: $html_files ไฟล์"
            ls -la alx_trading_report_*.html | while read line; do
                echo "  📊 $line"
            done
        else
            echo "🌐 ไฟล์ HTML: ไม่มี"
        fi
        ;;
    *)
        echo "❌ ตัวเลือกไม่ถูกต้อง"
        exit 1
        ;;
esac

echo ""
echo "🎉 เสร็จสิ้น!"

# แสดงไฟล์ผลลัพธ์
echo ""
echo "📁 ไฟล์ผลลัพธ์:"

if ls alx_trading_dm_*.json 1> /dev/null 2>&1; then
    latest_json=$(ls -t alx_trading_dm_*.json | head -n1)
    echo "✅ $latest_json - ข้อมูล DM ดิบ"
fi

if ls alx_trading_report_*.html 1> /dev/null 2>&1; then
    latest_html=$(ls -t alx_trading_report_*.html | head -n1)
    echo "✅ $latest_html - รายงาน HTML"
fi

echo ""
echo "💡 เคล็ดลับ:"
echo "  • เปิดไฟล์ .html ด้วยเบราว์เซอร์เพื่อดูรายงาน"
echo "  • ไฟล์ .json เก็บข้อมูลดิบสำหรับการประมวลผลต่อ"
echo "  • sessionid จะหมดอายุ ถ้าใช้ไม่ได้ให้เอาใหม่"
