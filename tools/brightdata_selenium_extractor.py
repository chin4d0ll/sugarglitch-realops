#!/usr/bin/env python3
"""
Bright Data Selenium Session Extractor
Alternative selenium-based session extractor using Bright Data remote browser
"""

import os
import json
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests

class BrightDataSeleniumExtractor:
    def __init__(self):
        # Bright Data Selenium endpoint
        self.selenium_endpoint = "https://brd-customer-hl_63f0835e-zone-scraping_agent:o5wnk3ws1r04@brd.superproxy.io:9515"
        self.target_username = "alx.trading"
        self.session_file = "tools/session_alx_trading.json"
        self.logs_dir = "logs"
        
        # Ensure directories exist
        os.makedirs("tools", exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs("sessions", exist_ok=True)
        
    def log_message(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        # Also save to log file
        with open(f"{self.logs_dir}/selenium_extraction.log", "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
    
    def setup_driver(self):
        """Setup Selenium WebDriver with Bright Data"""
        self.log_message("🔧 Setting up Selenium WebDriver with Bright Data...")
        
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User agent
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Connect to Bright Data remote WebDriver
            driver = webdriver.Remote(
                command_executor=self.selenium_endpoint,
                options=chrome_options
            )
            
            # Execute script to hide automation
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.log_message("✅ WebDriver setup successful")
            return driver
            
        except Exception as e:
            self.log_message(f"❌ Failed to setup WebDriver: {e}")
            return None
    
    def extract_session_selenium(self):
        """Extract session using Selenium"""
        self.log_message("🚀 Starting Selenium session extraction...")
        
        driver = self.setup_driver()
        if not driver:
            return None
            
        try:
            self.log_message("📱 Navigating to Instagram...")
            driver.get("https://www.instagram.com/")
            
            # Wait for page to load
            time.sleep(3)
            
            self.log_message("🔍 Checking login status...")
            
            # Check if login form exists
            try:
                login_form = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "form"))
                )
                
                if login_form:
                    self.log_message("❌ Not logged in - login form detected")
                    self.log_message("⚠️  Manual login required!")
                    self.log_message("📋 Instructions:")
                    self.log_message("1. Browser should be open with Instagram")
                    self.log_message("2. Please login manually")
                    self.log_message("3. Wait for login completion...")
                    
                    # Wait for login completion (look for profile elements)
                    self.wait_for_login_completion(driver)
                    
            except:
                self.log_message("🔍 No login form found, checking existing session...")
            
            # Extract cookies after login
            session_data = self.extract_cookies_selenium(driver)
            
            if session_data and session_data.get('sessionid'):
                self.log_message("✅ Session extracted successfully!")
                
                # Test session validity
                if self.test_session_validity(session_data):
                    self.log_message("✅ Session is valid!")
                    self.save_session(session_data)
                    return session_data
                else:
                    self.log_message("❌ Extracted session is invalid")
                    return None
            else:
                self.log_message("❌ No valid session found")
                return None
                
        except Exception as e:
            self.log_message(f"❌ Error during extraction: {e}")
            return None
            
        finally:
            try:
                driver.quit()
                self.log_message("🔒 Browser closed")
            except:
                pass
    
    def wait_for_login_completion(self, driver):
        """Wait for manual login completion"""
        self.log_message("⏳ Waiting for manual login completion (max 5 minutes)...")
        
        max_wait = 300  # 5 minutes
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                # Check for logged-in indicators
                if self.check_login_indicators(driver):
                    self.log_message("✅ Login completion detected!")
                    return True
                    
                time.sleep(2)
                
            except Exception as e:
                self.log_message(f"Error checking login status: {e}")
                time.sleep(5)
        
        self.log_message("⏰ Login wait timeout reached")
        return False
    
    def check_login_indicators(self, driver):
        """Check for indicators that user is logged in"""
        try:
            # Look for common logged-in elements
            indicators = [
                'svg[aria-label="Home"]',
                'a[href="/direct/inbox/"]',
                'svg[aria-label="New post"]',
                'button[aria-label="New post"]'
            ]
            
            for indicator in indicators:
                try:
                    element = driver.find_element(By.CSS_SELECTOR, indicator)
                    if element:
                        return True
                except:
                    continue
                    
            # Check if current URL indicates logged in state
            current_url = driver.current_url.lower()
            if 'login' not in current_url and 'accounts' not in current_url:
                # Additional check: look for username in page source
                page_source = driver.page_source.lower()
                if 'is_logged_in":true' in page_source or '"viewer":{' in page_source:
                    return True
                    
            return False
            
        except Exception as e:
            self.log_message(f"Error checking login indicators: {e}")
            return False
    
    def extract_cookies_selenium(self, driver):
        """Extract cookies using Selenium"""
        self.log_message("🍪 Extracting cookies...")
        
        try:
            cookies = driver.get_cookies()
            session_data = {}
            
            for cookie in cookies:
                if cookie['name'] in ['sessionid', 'csrftoken', 'ds_user_id', 'mid', 'ig_did', 'shbid', 'rur']:
                    session_data[cookie['name']] = cookie['value']
                    self.log_message(f"✅ Found {cookie['name']}: {cookie['value'][:20]}...")
            
            return session_data
            
        except Exception as e:
            self.log_message(f"❌ Error extracting cookies: {e}")
            return {}
    
    def test_session_validity(self, session_data):
        """Test if extracted session is valid"""
        self.log_message("🔍 Testing extracted session validity...")
        
        if not session_data.get('sessionid'):
            self.log_message("❌ No sessionid found")
            return False
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        # Build cookie string
        cookies = []
        for key, value in session_data.items():
            if value:
                cookies.append(f"{key}={value}")
        
        if cookies:
            headers['Cookie'] = "; ".join(cookies)
        
        try:
            response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)
            
            if response.status_code == 200:
                if 'login' not in response.url.lower() and '"is_logged_in":false' not in response.text:
                    self.log_message("✅ Session validation successful!")
                    return True
                else:
                    self.log_message("❌ Session validation failed - not logged in")
                    return False
            else:
                self.log_message(f"❌ Session validation failed - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Error testing session: {e}")
            return False
    
    def save_session(self, session_data):
        """Save session data to JSON file"""
        self.log_message("💾 Saving session to file...")
        
        session_info = {
            'sessionid': session_data.get('sessionid', ''),
            'csrftoken': session_data.get('csrftoken', ''),
            'ds_user_id': session_data.get('ds_user_id', ''),
            'mid': session_data.get('mid', ''),
            'ig_did': session_data.get('ig_did', ''),
            'shbid': session_data.get('shbid', ''),
            'rur': session_data.get('rur', ''),
            'target': self.target_username,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'extraction_method': 'bright_data_selenium'
        }
        
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_info, f, indent=2)
            self.log_message(f"✅ Session saved to {self.session_file}")
            
            # Also save backup
            backup_file = f"sessions/session_selenium_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(backup_file, 'w') as f:
                json.dump(session_info, f, indent=2)
            self.log_message(f"✅ Backup saved to {backup_file}")
            
            return True
            
        except Exception as e:
            self.log_message(f"❌ Failed to save session: {e}")
            return False
    
    def run(self):
        """Main execution flow"""
        self.log_message("🚀 BRIGHT DATA SELENIUM SESSION EXTRACTOR")
        self.log_message("="*60)
        self.log_message(f"Target: {self.target_username}")
        self.log_message(f"Selenium Endpoint: {self.selenium_endpoint}")
        self.log_message(f"Session File: {self.session_file}")
        self.log_message("")
        
        try:
            session_data = self.extract_session_selenium()
            
            if session_data and session_data.get('sessionid'):
                self.log_message("🎉 SUCCESS! Fresh session extracted and saved!")
                self.log_message(f"📄 Session ID: {session_data['sessionid'][:20]}...")
                self.log_message(f"📁 Saved to: {self.session_file}")
                
                return True
            else:
                self.log_message("❌ Failed to extract valid session")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Critical error: {e}")
            return False

def main():
    """Main function"""
    try:
        extractor = BrightDataSeleniumExtractor()
        result = extractor.run()
        
        if result:
            print("\n🎉 Session extraction completed successfully!")
            print("Next steps:")
            print("1. Session is saved in tools/session_alx_trading.json")
            print("2. Run DM extraction with interceptor protection")
            print("3. Check logs/selenium_extraction.log for details")
        else:
            print("\n❌ Session extraction failed")
            print("Check logs/selenium_extraction.log for details")
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
