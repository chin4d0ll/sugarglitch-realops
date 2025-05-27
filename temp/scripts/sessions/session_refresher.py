#!/usr/bin/env python3
"""
🔄 SESSION REFRESHER & BROWSER AUTOMATION 🔄
ระบบรีเฟรช session โดยใช้ browser automation
"""

import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from advanced_session_manager import AdvancedSessionManager


class SessionRefresher:
    def __init__(self, username: str = "whatilove1728"):
        self.username = username
        self.session_manager = AdvancedSessionManager(username)
        self.driver = None
        self.ua = UserAgent()
        
        print(f"🔄 Session Refresher initialized for: {username}")
    
    def setup_browser(self, headless: bool = False) -> bool:
        """ตั้งค่า browser สำหรับ automation"""
        try:
            print("🌐 Setting up browser...")
            
            # Chrome options
            options = Options()
            
            if headless:
                options.add_argument('--headless')
            
            # Anti-detection options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User agent
            user_agent = self.ua.random
            options.add_argument(f'--user-agent={user_agent}')
            
            # Window size
            options.add_argument('--window-size=1920,1080')
            
            # Disable images for faster loading (optional)
            prefs = {
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values": {
                    "notifications": 2
                }
            }
            options.add_experimental_option("prefs", prefs)
            
            # Try undetected chrome first
            try:
                self.driver = uc.Chrome(options=options)
                print("✅ Using undetected-chromedriver")
            except:
                # Fallback to regular webdriver
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                print("✅ Using regular ChromeDriver")
            
            # Execute script to remove automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def manual_login_session_capture(self) -> bool:
        """เปิด browser ให้ user login แล้วจับ session"""
        if not self.setup_browser(headless=False):
            return False
        
        try:
            print("🔐 MANUAL LOGIN SESSION CAPTURE")
            print("=" * 40)
            print("📋 Instructions:")
            print("1. Browser will open to Instagram login page")
            print("2. Login manually with your credentials")
            print("3. Navigate to your profile or target profile")
            print("4. Press ENTER in this terminal when ready")
            print("5. Session will be captured automatically")
            print()
            
            # เปิด Instagram login page
            self.driver.get("https://www.instagram.com/accounts/login/")
            
            # รอให้หน้าโหลด
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("🌐 Instagram login page opened")
            print("👤 Please login manually...")
            
            # รอให้ user login
            input("Press ENTER after you have logged in and navigated to the target profile...")
            
            # จับ cookies และ session data
            print("\n📊 Capturing session data...")
            
            cookies = self.driver.get_cookies()
            current_url = self.driver.current_url
            page_source_length = len(self.driver.page_source)
            
            print(f"🍪 Captured {len(cookies)} cookies")
            print(f"🔗 Current URL: {current_url}")
            print(f"📄 Page source length: {page_source_length}")
            
            # สร้าง session data
            session_data = {
                'cookies': cookies,
                'current_url': current_url,
                'capture_method': 'manual_browser_login',
                'user_agent': self.driver.execute_script("return navigator.userAgent;")
            }
            
            # เพิ่ม metadata
            metadata = {
                'capture_method': 'manual_browser_login',
                'capture_url': current_url,
                'browser_user_agent': session_data['user_agent'],
                'cookies_count': len(cookies)
            }
            
            # บันทึก session
            if self.session_manager.save_session(session_data, metadata):
                print("✅ Session captured and saved successfully!")
                
                # ทดสอบ session ทันที
                print("\n🧪 Testing captured session...")
                if self.session_manager.test_session_validity():
                    print("🎉 SUCCESS: Session is working!")
                    return True
                else:
                    print("⚠️ Session test failed, but data was saved")
                    return True
            else:
                print("❌ Failed to save session")
                return False
                
        except Exception as e:
            print(f"❌ Session capture failed: {e}")
            return False
        
        finally:
            if self.driver:
                print("🔚 Closing browser...")
                self.driver.quit()
    
    def automated_refresh_attempt(self, login_username: str = None, login_password: str = None) -> bool:
        """พยายาม refresh session แบบอัตโนมัติ (ต้องมี credentials)"""
        print("🤖 AUTOMATED SESSION REFRESH")
        print("⚠️ This requires Instagram credentials")
        
        if not login_username or not login_password:
            print("❌ Username and password required for automated refresh")
            print("💡 Use manual_login_session_capture() instead")
            return False
        
        if not self.setup_browser(headless=True):
            return False
        
        try:
            print("🔐 Attempting automated login...")
            
            # เปิด Instagram login
            self.driver.get("https://www.instagram.com/accounts/login/")
            
            # รอให้หน้าโหลด
            time.sleep(3)
            
            # หา username field
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
            )
            
            # หา password field  
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            
            # ใส่ข้อมูล
            username_field.clear()
            username_field.send_keys(login_username)
            
            time.sleep(1)
            
            password_field.clear()
            password_field.send_keys(login_password)
            
            time.sleep(1)
            
            # คลิกปุ่ม login
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # รอ login
            time.sleep(5)
            
            # ตรวจสอบว่า login สำเร็จหรือไม่
            current_url = self.driver.current_url
            
            if "challenge" in current_url or "two_factor" in current_url:
                print("⚠️ Two-factor authentication or challenge detected")
                print("💡 Please use manual login method")
                return False
            elif "accounts/login" in current_url:
                print("❌ Login failed - still on login page")
                return False
            else:
                print("✅ Login appears successful")
                
                # จับ session
                cookies = self.driver.get_cookies()
                session_data = {
                    'cookies': cookies,
                    'current_url': current_url,
                    'capture_method': 'automated_login'
                }
                
                metadata = {
                    'capture_method': 'automated_login',
                    'login_username': login_username
                }
                
                return self.session_manager.save_session(session_data, metadata)
                
        except Exception as e:
            print(f"❌ Automated refresh failed: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def restore_session_to_browser(self) -> bool:
        """กู้คืน session กลับไปยัง browser"""
        session_data = self.session_manager.current_session
        
        if not session_data:
            print("❌ No session data to restore")
            return False
        
        if not self.setup_browser(headless=False):
            return False
        
        try:
            print("🔄 Restoring session to browser...")
            
            # เปิด Instagram
            self.driver.get("https://www.instagram.com/")
            time.sleep(2)
            
            # เพิ่ม cookies
            if 'cookies' in session_data:
                for cookie in session_data['cookies']:
                    try:
                        # ปรับ cookie format สำหรับ Selenium
                        cookie_dict = {
                            'name': cookie['name'],
                            'value': cookie['value'],
                            'domain': cookie.get('domain', '.instagram.com'),
                            'path': cookie.get('path', '/'),
                            'secure': cookie.get('secure', True)
                        }
                        
                        self.driver.add_cookie(cookie_dict)
                    except Exception as e:
                        print(f"⚠️ Failed to add cookie {cookie.get('name', 'unknown')}: {e}")
                
                print(f"🍪 Restored {len(session_data['cookies'])} cookies")
            
            # รีเฟรชหน้า
            self.driver.refresh()
            time.sleep(3)
            
            current_url = self.driver.current_url
            print(f"🔗 Current URL after restore: {current_url}")
            
            # ลองเข้าถึง profile
            profile_url = f"https://www.instagram.com/{self.username}/"
            self.driver.get(profile_url)
            time.sleep(3)
            
            final_url = self.driver.current_url
            print(f"🎯 Final URL: {final_url}")
            
            if "login" in final_url:
                print("❌ Session restore failed - redirected to login")
                return False
            else:
                print("✅ Session restored successfully!")
                print("🌐 Browser is ready for manual inspection")
                input("Press ENTER to close browser...")
                return True
                
        except Exception as e:
            print(f"❌ Session restore failed: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()


def main():
    print("🔄💀 SESSION REFRESHER & BROWSER AUTOMATION 💀🔄")
    print("=" * 60)
    
    refresher = SessionRefresher("whatilove1728")
    
    print("\n📋 AVAILABLE OPTIONS:")
    print("1. 🔐 Manual Login & Session Capture")
    print("2. 🔄 Restore Existing Session to Browser") 
    print("3. 🧪 Test Current Session")
    print("4. 📊 Show Session Status")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        print("\n🔐 Starting manual login session capture...")
        refresher.manual_login_session_capture()
    
    elif choice == "2":
        print("\n🔄 Restoring session to browser...")
        # โหลด session ก่อน
        refresher.session_manager.load_session()
        refresher.restore_session_to_browser()
    
    elif choice == "3":
        print("\n🧪 Testing current session...")
        refresher.session_manager.load_session()
        refresher.session_manager.test_session_validity()
    
    elif choice == "4":
        print("\n📊 Session status...")
        refresher.session_manager.load_session()
        refresher.session_manager.list_available_sessions()
    
    else:
        print("❌ Invalid option")


if __name__ == "__main__":
    main()
