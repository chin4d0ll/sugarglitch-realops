from playwright.async_api import async_playwright
import json, asyncio, os
from datetime import datetime

def load_sessionid():
    """โหลด sessionid จากไฟล์ที่บันทึกไว้"""
    session_files = [
        "current_sessionid.txt",
        "extracted_session_config.json", 
        "sessionid_alx_trading.txt"
    ]
    
    for session_file in session_files:
        if os.path.exists(session_file):
            try:
                if session_file.endswith('.json'):
                    with open(session_file, 'r') as f:
                        data = json.load(f)
                        sessionid = data.get('sessionid', '')
                else:
                    with open(session_file, 'r') as f:
                        sessionid = f.read().strip()
                
                if sessionid:
                    print(f"✅ โหลด sessionid จาก {session_file}")
                    return sessionid
            except:
                continue
    
    return None

async def get_dms_from_alx_trading(sessionid: str):
    """ดึง DM จากบัญชี alx.trading โดยเฉพาะ"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        print("🔧 กำลังตั้งค่า session...")
        
        # ตั้งค่า cookie sessionid
        await context.add_cookies([{
            "name": "sessionid",
            "value": sessionid,
            "domain": ".instagram.com",
            "path": "/",
            "httpOnly": True,
            "secure": True
        }])

        try:
            print("🌐 เข้าสู่ Instagram...")
            await page.goto("https://www.instagram.com/direct/inbox/", timeout=60000)
            await page.wait_for_timeout(5000)

            print("🔍 ค้นหาแชทของ alx.trading...")
            
            # ค้นหาแชทของ alx.trading
            # วิธี 1: ค้นหาจากชื่อในรายการแชท
            chat_found = False
            alx_data = {
                "target_username": "alx.trading",
                "extraction_time": datetime.now().isoformat(),
                "messages": [],
                "chat_found": False
            }
            
            # ลองหาแชทที่มีชื่อ alx.trading
            await page.wait_for_timeout(3000)
            
            # ดูรายการแชททั้งหมด
            chats = await page.query_selector_all('[role="button"]')
            
            for chat in chats:
                try:
                    chat_text = await chat.inner_text()
                    if "alx.trading" in chat_text.lower() or "alx" in chat_text.lower():
                        print("✅ พบแชท alx.trading!")
                        await chat.click()
                        await page.wait_for_timeout(3000)
                        chat_found = True
                        break
                except:
                    continue
            
            if not chat_found:
                print("⚠️ ไม่พบแชทของ alx.trading ในรายการแชทล่าสุด")
                print("💡 ลองไปหาโดยตรงที่โปรไฟล์...")
                
                # วิธี 2: ไปหาโดยตรงที่โปรไฟล์
                await page.goto("https://www.instagram.com/alx.trading/", timeout=30000)
                await page.wait_for_timeout(3000)
                
                # หาปุ่ม Message
                message_button = await page.query_selector('text="Message"')
                if message_button:
                    await message_button.click()
                    await page.wait_for_timeout(3000)
                    chat_found = True
                    print("✅ เข้าแชทผ่านโปรไฟล์สำเร็จ!")
                else:
                    print("❌ ไม่สามารถเข้าแชทได้ - อาจไม่มีสิทธิ์หรือบัญชีไม่มีอยู่")
            
            if chat_found:
                alx_data["chat_found"] = True
                print("📝 กำลังดึงข้อความ...")
                
                # ดึงข้อความทั้งหมดในแชท
                await page.wait_for_timeout(2000)
                
                # scroll ขึ้นเพื่อโหลดข้อความเก่า
                for i in range(5):  # scroll 5 รอบ
                    await page.keyboard.press("PageUp")
                    await page.wait_for_timeout(1000)
                
                # ดึงข้อความทั้งหมด
                message_selectors = [
                    '[data-testid="message-text"]',
                    'div[dir="auto"]',
                    '.x1n2onr6',
                    'span'
                ]
                
                messages = []
                for selector in message_selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        for element in elements:
                            text = await element.inner_text()
                            if text and len(text.strip()) > 0 and text not in messages:
                                messages.append(text.strip())
                    except:
                        continue
                
                # กรองข้อความที่ดูเหมือนข้อความจริง
                filtered_messages = []
                for msg in messages:
                    if (len(msg) > 1 and 
                        not msg.isdigit() and 
                        msg not in ['•', '...', 'Message', 'Send'] and
                        len(msg) < 500):  # ไม่เอาข้อความยาวเกินไป
                        filtered_messages.append(msg)
                
                alx_data["messages"] = filtered_messages
                alx_data["message_count"] = len(filtered_messages)
                
                print(f"✅ ดึงข้อความได้ {len(filtered_messages)} ข้อความ")
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
        
        finally:
            await browser.close()
        
        # บันทึกข้อมูล
        filename = f"alx_trading_dm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(alx_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 บันทึกข้อมูลใน: {filename}")
        return alx_data

async def main():
    print("🎯 Instagram DM Extractor - alx.trading")
    print("=" * 40)
    
    # ลองโหลด sessionid จากไฟล์
    sessionid = load_sessionid()
    
    if not sessionid:
        print("❌ ไม่พบ sessionid ที่บันทึกไว้")
        print("💡 ลองรันคำสั่งนี้ก่อน: ./extract_session.sh")
        print("หรือใส่ sessionid ด้วยตนเอง:")
        sessionid = input("ใส่ sessionid ของคุณ: ").strip()
    else:
        print(f"✅ โหลด sessionid สำเร็จ: {sessionid[:15]}...")
    
    if not sessionid:
        print("❌ กรุณาใส่ sessionid")
        return
    
    print("🚀 เริ่มดึงข้อมูล...")
    result = await get_dms_from_alx_trading(sessionid)
    
    print("\n📊 สรุปผลลัพธ์:")
    print(f"🎯 เป้าหมาย: {result['target_username']}")
    print(f"✅ พบแชท: {'ใช่' if result['chat_found'] else 'ไม่'}")
    print(f"💬 จำนวนข้อความ: {result.get('message_count', 0)}")
    
    if result['chat_found'] and result.get('message_count', 0) > 0:
        print("\n📝 ตัวอย่างข้อความ (5 ข้อความแรก):")
        for i, msg in enumerate(result['messages'][:5]):
            print(f"  {i+1}. {msg}")
    
    print("\n🎉 เสร็จสิ้น!")

if __name__ == "__main__":
    asyncio.run(main())
