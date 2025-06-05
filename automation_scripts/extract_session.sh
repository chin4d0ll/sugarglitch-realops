#!/bin/bash

# Instagram Session Extractor Runner
# Automated session extraction for alx.trading

echo "🔐 Instagram Session Extractor"
echo "=============================="
echo "🎯 Target: alx.trading"
echo "🔑 Password: Fleming654"
echo ""

# Activate virtual environment
source .venv/bin/activate

echo "📱 เริ่มต้นการดึง sessionid..."
echo "⚠️  หน้าต่างเบราว์เซอร์จะเปิดขึ้นมา"
echo "💡 อาจจะต้องการการยืนยันตัวตนเพิ่มเติม (2FA, SMS, Email)"
echo ""

# Run session extractor
python3 session_extractor.py

# Check if session was extracted successfully
if [ -f "current_sessionid.txt" ]; then
    echo ""
    echo "✅ SessionID ดึงสำเร็จแล้ว!"
    echo "📄 บันทึกในไฟล์: current_sessionid.txt"
    
    # Show sessionid preview
    sessionid=$(cat current_sessionid.txt)
    echo "🔑 SessionID: ${sessionid:0:20}...${sessionid: -10}"
    
    echo ""
    echo "🚀 ขั้นตอนต่อไป - เลือกสิ่งที่ต้องการทำ:"
    echo "1. ดึง DM จาก alx.trading ทันที"
    echo "2. บันทึก sessionid ไว้ใช้ภายหลัง"
    echo "3. ทดสอบ sessionid"
    echo ""
    
    read -p "เลือก (1-3): " choice
    
    case $choice in
        1)
            echo "🎯 เริ่มดึง DM จาก alx.trading..."
            ./run_alx_trading_extractor.sh
            ;;
        2)
            echo "💾 SessionID บันทึกไว้แล้ว"
            echo "📋 ใช้งานได้ด้วยคำสั่ง:"
            echo "   ./run_alx_trading_extractor.sh"
            echo "   หรือ"
            echo "   python3 alx_trading_dm_extractor.py"
            ;;
        3)
            echo "🧪 ทดสอบ sessionid..."
            python3 -c "
import asyncio
from playwright.async_api import async_playwright

async def test_session():
    sessionid = open('current_sessionid.txt').read().strip()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        await context.add_cookies([{
            'name': 'sessionid',
            'value': sessionid,
            'domain': '.instagram.com',
            'path': '/',
            'httpOnly': True,
            'secure': True
        }])
        page = await context.new_page()
        await page.goto('https://www.instagram.com/')
        await page.wait_for_timeout(3000)
        
        # Check if logged in
        if 'login' not in page.url:
            print('✅ SessionID ใช้งานได้')
        else:
            print('❌ SessionID หมดอายุหรือใช้งานไม่ได้')
        
        await browser.close()

asyncio.run(test_session())
"
            ;;
        *)
            echo "💾 SessionID บันทึกไว้แล้ว - พร้อมใช้งาน"
            ;;
    esac
    
else
    echo ""
    echo "❌ การดึง sessionid ไม่สำเร็จ"
    echo ""
    echo "🔍 สาเหตุที่เป็นไปได้:"
    echo "   - รหัสผ่านเปลี่ยนแปลง"
    echo "   - ต้องการการยืนยันตัวตน (2FA)"
    echo "   - Instagram บล็อกการเข้าถึง"
    echo "   - ปัญหาเครือข่าย"
    echo ""
    echo "💡 ลองอีกครั้ง:"
    echo "   ./extract_session.sh"
    echo ""
    echo "🔧 หรือดึง sessionid ด้วยตนเอง:"
    echo "   1. เปิด Instagram ในเบราว์เซอร์"
    echo "   2. เข้าสู่ระบบด้วย alx.trading / Fleming654"
    echo "   3. กด F12 → Application → Cookies → instagram.com"
    echo "   4. ก็อปปี้ค่า sessionid"
    echo "   5. บันทึกในไฟล์ current_sessionid.txt"
fi

echo ""
echo "📞 ต้องการความช่วยเหลือ?"
echo "   ตรวจสอบ README.md หรือ DM_EXTRACTOR_README.md"
