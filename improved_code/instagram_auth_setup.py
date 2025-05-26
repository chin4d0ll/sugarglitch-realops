from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔐 INSTAGRAM AUTHENTICATION SETUP
Secure login system for private profile access
"""

import asyncio
from playwright.async_api import async_playwright
import json
import os
from datetime import datetime

class InstagramAuth:
    def __init__(self):
        self.auth = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
        self.sbr_ws_cdp = f'wss://{self.auth}@brd.superproxy.io:9222'
        self.session_file = 'instagram_session.json'
        
    async def login_to_instagram(self, username, password):
        """
        🔐 Login to Instagram with your credentials
        """
        print("🚀 Starting Instagram Authentication...")
        
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(self.sbr_ws_cdp)
            
            try:
                page = await browser.new_page()
                
                # Go to Instagram login
                await page.goto('https://www.instagram.com/accounts/login/')
                await page.wait_for_load_state('networkidle')
                
                print("📱 Loading Instagram login page...")
                await page.screenshot(path='instagram_login.png')
                
                # Fill login form
                await page.fill('input[name="username"]', username)
                await page.fill('input[name="password"]', password)
                
                print("🔑 Filling login credentials...")
                
                # Click login button
                await page.click('button[type="submit"]')
                await page.wait_for_timeout(3000)
                
                # Check if login successful
                current_url = page.url
                if 'challenge' in current_url:
                    print("⚠️  2FA Challenge detected!")
                    await page.screenshot(path='instagram_2fa.png')
                    print("📧 Check your email/phone for verification code")
                    return False
                elif 'login' not in current_url:
                    print("✅ Login successful!")
                    
                    # Save session cookies
                    cookies = await page.context.cookies()
                    session_data = {
                        'cookies': cookies,
                        'login_time': datetime.now().isoformat(),
                        'username': username
                    }
                    
                    with open(self.session_file, 'w') as f:
                        json.dump(session_data, f, indent=2)
                    
                    await page.screenshot(path='instagram_logged_in.png')
                    return True
                else:
                    print("❌ Login failed!")
                    await page.screenshot(path='instagram_login_failed.png')
                    return False
                    
            finally:
                await browser.close()
    
    async def load_saved_session(self):
        """
        📂 Load previously saved Instagram session
        """
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                return json.load(f)
        return None
    
    async def test_session_valid(self):
        """
        🧪 Test if saved session is still valid
        """
        session_data = await self.load_saved_session()
        if not session_data:
            return False
            
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(self.sbr_ws_cdp)
            
            try:
                context = await browser.new_context()
                await context.add_cookies(session_data['cookies'])
                
                page = await context.new_page()
                await page.goto('https://www.instagram.com/')
                await page.wait_for_timeout(2000)
                
                # Check if still logged in
                if 'login' not in page.url:
                    print("✅ Session still valid!")
                    return True
                else:
                    print("❌ Session expired")
                    return False
                    
            finally:
                await browser.close()

async @safe_execution
def main():
    auth = InstagramAuth()
    
    print("🔐 INSTAGRAM AUTHENTICATION SETUP")
    print("=" * 50)
    
    # Check if we have a valid session
    if await auth.test_session_valid():
        print("✅ Using existing valid session")
        return
    
    # Need to login
    print("\n📝 Login Required:")
    print("1. Enter your Instagram username/email")
    print("2. Enter your Instagram password") 
    print("3. Complete 2FA if prompted")
    
    username = input("\n👤 Instagram Username/Email: ")
    password = input("🔑 Instagram Password: ")
    
    success = await auth.login_to_instagram(username, password)
    
    if success:
        print("🎉 Authentication complete! Ready for private profile access.")
    else:
        print("❌ Authentication failed. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
