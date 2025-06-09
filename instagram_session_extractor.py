#!/usr/bin/env python3
"""
Instagram Session Extractor - Production Ready
Clean, working version for extracting Instagram sessions and DMs
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InstagramExtractor:
    def __init__(self, output_dir="./results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session_file = self.output_dir / "session.json"
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        print("🔧 Setting up Chrome driver...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # For codespace environment
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome driver initialized")
            return True
        except Exception as e:
            print(f"❌ Failed to setup driver: {e}")
            return False
    
    def login_instagram(self, username, password):
        """Login to Instagram and capture session"""
        print(f"🔐 Logging in as {username}...")
        
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            # Wait for and fill username
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(username)
            
            # Fill password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            
            # Check if login was successful
            if "challenge" in self.driver.current_url or "login" in self.driver.current_url:
                print("⚠️ Login may require verification")
                return False
            
            print("✅ Login successful")
            self.save_session()
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def save_session(self):
        """Save session cookies and data"""
        print("💾 Saving session data...")
        
        try:
            cookies = self.driver.get_cookies()
            session_data = {
                "timestamp": datetime.now().isoformat(),
                "url": self.driver.current_url,
                "cookies": cookies,
                "user_agent": self.driver.execute_script("return navigator.userAgent;"),
                "session_id": None
            }
            
            # Extract session ID from cookies
            for cookie in cookies:
                if cookie['name'] == 'sessionid':
                    session_data['session_id'] = cookie['value']
                    break
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"✅ Session saved to {self.session_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save session: {e}")
            return False
    
    def extract_dm_data(self, target_username=None):
        """Extract DM data using session"""
        print("📨 Extracting DM data...")
        
        try:
            # Navigate to DMs
            self.driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(5)
            
            # Wait for DMs to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1n2onr6')]"))
            )
            
            dm_data = {
                "timestamp": datetime.now().isoformat(),
                "conversations": [],
                "metadata": {
                    "extraction_method": "selenium",
                    "target_username": target_username
                }
            }
            
            # Extract conversation list
            conversations = self.driver.find_elements(By.XPATH, "//div[contains(@role, 'button')]//div[contains(@class, 'x1lliihq')]")
            
            for i, conv in enumerate(conversations[:10]):  # Limit to first 10
                try:
                    conv_text = conv.text
                    if conv_text and len(conv_text) > 0:
                        dm_data["conversations"].append({
                            "index": i,
                            "preview": conv_text[:100],
                            "extracted_at": datetime.now().isoformat()
                        })
                except:
                    continue
            
            # Save DM data
            timestamp = int(datetime.now().timestamp())
            dm_file = self.output_dir / f"dm_extraction_{timestamp}.json"
            
            with open(dm_file, 'w') as f:
                json.dump(dm_data, f, indent=2)
            
            print(f"✅ DM data saved to {dm_file}")
            print(f"📊 Extracted {len(dm_data['conversations'])} conversations")
            
            return dm_file
            
        except Exception as e:
            print(f"❌ DM extraction failed: {e}")
            return None
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            print("🧹 Driver cleaned up")

def main():
    print("🚀 INSTAGRAM SESSION EXTRACTOR")
    print("="*50)
    
    extractor = InstagramExtractor()
    
    try:
        # Setup driver
        if not extractor.setup_driver():
            print("❌ Failed to setup driver")
            return
        
        # For demonstration - replace with actual credentials
        username = input("Enter Instagram username (or 'demo' for test): ")
        
        if username.lower() == 'demo':
            print("🎭 Running in demo mode...")
            # Create demo session file
            demo_session = {
                "timestamp": datetime.now().isoformat(),
                "mode": "demo",
                "status": "ready_for_real_credentials"
            }
            
            with open(extractor.session_file, 'w') as f:
                json.dump(demo_session, f, indent=2)
            
            print("✅ Demo session created")
            print("🔧 Replace with real credentials for actual extraction")
            
        else:
            password = input("Enter Instagram password: ")
            
            # Login and extract
            if extractor.login_instagram(username, password):
                dm_file = extractor.extract_dm_data()
                if dm_file:
                    print(f"🎯 Extraction complete! Check {dm_file}")
                else:
                    print("⚠️ DM extraction failed")
            else:
                print("❌ Login failed")
    
    except KeyboardInterrupt:
        print("\\n⏹️ Extraction stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        extractor.cleanup()

if __name__ == "__main__":
    main()
