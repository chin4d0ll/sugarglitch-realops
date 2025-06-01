#!/usr/bin/env python3
"""
Quick Cookie Fix - Automated cookie extraction and validation
"""

import os
import json
import time
import requests
import warnings
import urllib3
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from fake_useragent import UserAgent

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')

class QuickCookieFix:
    def __init__(self):
        self.ua = UserAgent()
        self.proxy = None  # ตั้งค่า proxy ที่นี่ถ้าต้องการ เช่น "http://proxy:port"
        self.sessions_dir = "/workspaces/sugarglitch-realops/sessions"
        self.instaloader_session_dir = os.path.expanduser("~/.instaloader")
        os.makedirs(self.sessions_dir, exist_ok=True)
        os.makedirs(self.instaloader_session_dir, exist_ok=True)
    
    def load_existing_session(self, username):
        """โหลด session จากไฟล์ ~/.instaloader/session-<username> ถ้ามี"""
        session_file = f"{self.instaloader_session_dir}/session-{username}"
        
        if os.path.exists(session_file):
            try:
                print(f"🔍 Found existing Instaloader session: {session_file}")
                # อ่านไฟล์ session (Instaloader session เป็น pickle format)
                with open(session_file, 'rb') as f:
                    session_data = f.read()
                
                if len(session_data) > 0:
                    print("✅ Existing session loaded successfully")
                    return session_file
                else:
                    print("⚠️ Session file is empty")
                    return None
                    
            except Exception as e:
                print(f"❌ Failed to load existing session: {e}")
                return None
        else:
            print(f"📂 No existing session found at: {session_file}")
            return None
    
    def create_stealth_session(self):
        """สร้าง requests session พร้อม stealth headers"""
        session = requests.Session()
        
        # ตั้งค่า stealth headers
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        session.headers.update(headers)
        
        # ตั้งค่า proxy ถ้ามี
        if self.proxy:
            session.proxies = {
                'http': self.proxy,
                'https': self.proxy
            }
            print(f"🌐 Using proxy: {self.proxy}")
        
        # ปิด SSL verification
        session.verify = False
        
        return session

    def quick_cookie_extraction(self):
        """Quick automated cookie extraction"""
        print("🚀 QUICK COOKIE EXTRACTION STARTING...")
        
        try:
            # Setup Chrome options for stealth
            options = uc.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-web-security")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            # Initialize driver
            driver = uc.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("🌐 Opening Instagram...")
            driver.get("https://www.instagram.com/accounts/login/")

            time.sleep(5)

            # Login automatically
            username = "alx.trading"
            password = "Fleming654"
            
            print(f"🔑 Logging in as {username}...")
            
            # Find and fill login form
            wait = WebDriverWait(driver, 20)
            
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            password_field = driver.find_element(By.NAME, "password")
            
            # Type credentials with human-like delays
            for char in username:
                username_field.send_keys(char)
                time.sleep(0.1)
            
            time.sleep(1)
            
            for char in password:
                password_field.send_keys(char)
                time.sleep(0.1)
            
            # Click login
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            print("⏳ Waiting for login...")
            time.sleep(8)
            
            # Check for 2FA
            current_url = driver.current_url
            if "challenge" in current_url or "two_factor" in current_url:
                print("🔐 2FA DETECTED!")
                print("Please complete 2FA in the browser window...")
                input("Press Enter when login is complete...")
            
            # Wait for main page
            time.sleep(5)
            
            # Extract cookies
            print("🍪 Extracting cookies...")
            cookies = driver.get_cookies()
            
            cookie_dict = {}
            for cookie in cookies:
                cookie_dict[cookie['name']] = cookie['value']
            
            # Check for essential cookies
            essential_cookies = ['sessionid', 'csrftoken', 'ds_user_id']
            missing_cookies = [c for c in essential_cookies if c not in cookie_dict]
            
            if missing_cookies:
                print(f"⚠️ Missing essential cookies: {missing_cookies}")
            else:
                print("✅ All essential cookies found!")
            
            # Save cookies
            timestamp = int(time.time())
            cookie_file = f"/workspaces/sugarglitch-realops/fresh_cookies_{timestamp}.json"
            
            cookie_dict['extracted_at'] = timestamp
            cookie_dict['extraction_method'] = 'automated'
            
            with open(cookie_file, 'w') as f:
                json.dump(cookie_dict, f, indent=2)
            
            print(f"💾 Cookies saved to: {cookie_file}")
            
            driver.quit()
            
            # Test cookies immediately
            print("\n🧪 Testing extracted cookies...")
            if test_cookies(cookie_dict):
                print("🎉 SUCCESS! Cookies are working!")
                return cookie_file
            else:
                print("❌ Cookies test failed")
                return None
            
        except Exception as e:
            print(f"❌ Cookie extraction failed: {e}")
            if 'driver' in locals():
                driver.quit()
            return None

def test_cookies(cookies):
    """Quick test of extracted cookies"""
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        })
        
        # Add cookies
        for name, value in cookies.items():
            if isinstance(value, str):
                session.cookies.set(name, value, domain='.instagram.com')
        
        # Test request
        response = session.get("https://www.instagram.com/alx.trading/", timeout=10)
        
        # Check if logged in
        is_logged_in = '"viewer":' in response.text and response.status_code == 200
        
        print(f"Test result: Status {response.status_code}, Logged in: {is_logged_in}")
        return is_logged_in
        
    except Exception as e:
        print(f"Cookie test error: {e}")
        return False

def create_sessionid_only_file():
    """Create session file with just sessionid for quick testing"""
    print("\n📝 ALTERNATIVE: Manual sessionid input")
    print("If automated extraction fails, you can manually input sessionid:")
    print()
    
    sessionid = input("Paste your sessionid from browser (or press Enter to skip): ").strip()
    
    if sessionid:
        cookies = {
            'sessionid': sessionid,
            'extracted_at': int(time.time()),
            'extraction_method': 'manual_sessionid'
        }
        
        cookie_file = "/workspaces/sugarglitch-realops/manual_sessionid.json"
        with open(cookie_file, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print(f"💾 Manual sessionid saved to: {cookie_file}")
        
        if test_cookies(cookies):
            print("✅ Manual sessionid works!")
            return cookie_file
        else:
            print("❌ Manual sessionid failed")
    
    return None

def main():
    """Main execution"""
    print("🔥 INSTAGRAM COOKIE QUICK FIX 🔥")
    print("="*40)
    
    # Try automated extraction first
    cookie_file = quick_cookie_extraction()
    
    if not cookie_file:
        # Fallback to manual sessionid
        cookie_file = create_sessionid_only_file()
    
    if cookie_file:
        print(f"\n🎯 READY TO EXTRACT!")
        print(f"Cookie file: {cookie_file}")
        print("\nRun main extraction:")
        print("python instagram_anti_bot_bypass.py")
    else:
        print("\n❌ Cookie extraction failed completely")
        print("💡 Try manual cookie extraction using browser DevTools")
        print("📖 Read: COOKIE_EXTRACTION_GUIDE.md")

if __name__ == "__main__":
    main()
