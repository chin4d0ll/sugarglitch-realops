#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Session ID Extractor
Automated session retrieval for alx.trading account
"""

from playwright.async_api import async_playwright
import json
import asyncio
from datetime import datetime
import os

class InstagramSessionExtractor:
    def __init__(self):
        self.username = "alx.trading"
        self.password = "Fleming654"
        self.session_data = {}
        
    async def extract_session(self):
        """Extract sessionid from Instagram login"""
        print("🎯 Instagram Session Extractor")
        print("=" * 40)
        print(f"Target: {self.username}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        async with async_playwright() as p:
            # Launch browser (headless for server environment)
            browser = await p.chromium.launch(
                headless=True,   # Must be True for server environment
                slow_mo=1000,    # Slow down for better success rate
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding'
                ]
            )
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            try:
                # Step 1: Navigate to Instagram
                print("📱 เข้าสู่ Instagram...")
                await page.goto("https://www.instagram.com/accounts/login/", timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Step 2: Handle cookie banner if present
                try:
                    cookie_button = page.locator('button:has-text("Accept"), button:has-text("Allow"), button:has-text("Only Allow Essential")')
                    if await cookie_button.count() > 0:
                        await cookie_button.first.click()
                        await page.wait_for_timeout(2000)
                except:
                    pass
                
                # Step 3: Fill login form
                print("🔑 ใส่ข้อมูลการเข้าสู่ระบบ...")
                
                # Wait for username field and fill
                username_selector = 'input[name="username"], input[aria-label="Phone number, username, or email"]'
                await page.wait_for_selector(username_selector, timeout=10000)
                await page.fill(username_selector, self.username)
                await page.wait_for_timeout(1000)
                
                # Fill password
                password_selector = 'input[name="password"], input[aria-label="Password"]'
                await page.fill(password_selector, self.password)
                await page.wait_for_timeout(1000)
                
                # Step 4: Submit login
                print("🚀 เข้าสู่ระบบ...")
                login_button = 'button[type="submit"], button:has-text("Log in"), button:has-text("Log In")'
                await page.click(login_button)
                
                # Step 5: Wait for login completion and handle potential 2FA/verification
                await page.wait_for_timeout(5000)
                
                # Check if we're redirected to home page or verification needed
                current_url = page.url
                print(f"📍 URL ปัจจุบัน: {current_url}")
                
                if "challenge" in current_url or "two_factor" in current_url:
                    print("⚠️  ต้องการการยืนยันตัวตน - รอ 30 วินาที...")
                    print("💡 ตรวจสอบอีเมลหรือ SMS สำหรับรหัสยืนยัน")
                    await page.wait_for_timeout(30000)  # Wait for manual verification
                
                # Try to navigate to home if not already there
                if "instagram.com" in current_url and not current_url.endswith("/"):
                    await page.goto("https://www.instagram.com/", timeout=15000)
                    await page.wait_for_timeout(3000)
                
                # Step 6: Extract cookies and session data
                print("🍪 ดึงข้อมูล session...")
                cookies = await context.cookies()
                
                session_id = None
                csrf_token = None
                
                for cookie in cookies:
                    if cookie['name'] == 'sessionid':
                        session_id = cookie['value']
                    elif cookie['name'] == 'csrftoken':
                        csrf_token = cookie['value']
                
                if session_id:
                    self.session_data = {
                        'username': self.username,
                        'sessionid': session_id,
                        'csrftoken': csrf_token,
                        'extracted_at': datetime.now().isoformat(),
                        'url': current_url,
                        'cookies': cookies
                    }
                    
                    print("✅ ดึง sessionid สำเร็จ!")
                    print(f"📋 SessionID: {session_id[:20]}...")
                    print(f"🔑 CSRF Token: {csrf_token[:20]}..." if csrf_token else "🔑 CSRF Token: ไม่พบ")
                    
                    # Save to file
                    await self.save_session_data()
                    
                else:
                    print("❌ ไม่พบ sessionid - อาจจะเข้าสู่ระบบไม่สำเร็จ")
                    
            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาด: {str(e)}")
                
            finally:
                await browser.close()
                
        return self.session_data
    
    async def save_session_data(self):
        """Save session data to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save full session data
        session_file = f"session_data_{timestamp}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2, ensure_ascii=False)
        
        # Save just sessionid for easy use
        sessionid_file = "current_sessionid.txt"
        with open(sessionid_file, 'w', encoding='utf-8') as f:
            f.write(self.session_data['sessionid'])
        
        # Save credentials for future use (encrypted would be better)
        config_file = "extracted_session_config.json"
        config_data = {
            'username': self.username,
            'sessionid': self.session_data['sessionid'],
            'last_extracted': self.session_data['extracted_at']
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        
        print(f"💾 บันทึกข้อมูลแล้ว:")
        print(f"   📄 {session_file}")
        print(f"   📄 {sessionid_file}")
        print(f"   📄 {config_file}")

async def main():
    extractor = InstagramSessionExtractor()
    session_data = await extractor.extract_session()
    
    if session_data and 'sessionid' in session_data:
        print("\n🎉 การดึง sessionid เสร็จสิ้น!")
        print("=" * 40)
        print("📋 ข้อมูลที่ได้:")
        print(f"   👤 Username: {session_data['username']}")
        print(f"   🔑 SessionID: {session_data['sessionid'][:20]}...{session_data['sessionid'][-10:]}")
        print(f"   ⏰ เวลา: {session_data['extracted_at']}")
        
        print("\n🚀 ขั้นตอนต่อไป:")
        print("1. รัน: ./run_alx_trading_extractor.sh")
        print("2. หรือ: python3 alx_trading_dm_extractor.py")
        print("3. sessionid จะถูกโหลดอัตโนมัติจากไฟล์ที่บันทึกไว้")
        
    else:
        print("\n❌ ไม่สามารถดึง sessionid ได้")
        print("💡 ตรวจสอบ:")
        print("   - ชื่อผู้ใช้และรหัสผ่านถูกต้อง")
        print("   - การเชื่อมต่ออินเทอร์เน็ต")
        print("   - Instagram ไม่ได้บล็อกการเข้าถึง")

if __name__ == "__main__":
    print("🔐 Instagram Session ID Extractor")
    print("🎯 Target: alx.trading")
    print("⚠️  ใช้เพื่อการศึกษาเท่านั้น")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  ยกเลิกการดำเนินการ")
    except Exception as e:
        print(f"\n❌ ข้อผิดพลาด: {e}")
