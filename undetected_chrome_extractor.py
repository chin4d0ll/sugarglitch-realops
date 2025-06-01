#!/usr/bin/env python3
"""
🥷 UNDETECTED CHROME STEALTH EXTRACTOR 🥷
หลบ bot detection ด้วย undetected-chromedriver + selenium-stealth
"""

import undetected_chromedriver as uc
from selenium_stealth import stealth
import json
import time
import random
from datetime import datetime
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class UndetectedChromeExtractor:
    def __init__(self):
        self.driver = None
        self.results = {
            'extraction_timestamp': datetime.now().isoformat(),
            'method': 'Undetected Chrome + Selenium Stealth',
            'accounts': {}
        }
        
        # Target accounts
        self.targets = ['alx.trading', 'whatilove1728']
        
        # Stealth user agents pool
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; SM-G996B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
        ]
    
    def setup_undetected_browser(self):
        """ตั้งค่า browser ที่หลบตัวได้"""
        print("🔧 Setting up undetected Chrome browser...")
        
        # Chrome options for maximum stealth
        options = uc.ChromeOptions()
        
        # Basic stealth options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        
        # Advanced anti-detection
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions-file-access-check')
        options.add_argument('--disable-extensions-http-throttling')
        options.add_argument('--disable-extensions-except-at-startup')
        
        # Mobile emulation for better stealth
        mobile_emulation = {
            "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
            "userAgent": random.choice(self.user_agents)
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # Create undetected Chrome instance
        self.driver = uc.Chrome(options=options, version_main=120)
        
        # Apply additional stealth with selenium-stealth
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="iPhone",
                webgl_vendor="Apple Inc.",
                renderer="Apple GPU",
                fix_hairline=True,
        )
        
        # Additional JavaScript injections for stealth
        self.inject_stealth_scripts()
        
        print("✅ Undetected browser ready!")
    
    def inject_stealth_scripts(self):
        """ฉีด JavaScript เพื่อหลบ detection"""
        print("💉 Injecting advanced stealth scripts...")
        
        stealth_scripts = [
            # Hide webdriver property
            """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            """,
            
            # Fake plugins
            """
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            """,
            
            # Fake languages
            """
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en', 'th'],
            });
            """,
            
            # Permission API override
            """
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            """,
            
            # Chrome runtime override
            """
            if (!window.chrome) {
                window.chrome = {};
            }
            if (!window.chrome.runtime) {
                window.chrome.runtime = {};
            }
            """,
        ]
        
        for script in stealth_scripts:
            try:
                self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                    'source': script
                })
            except:
                pass
        
        print("✅ Stealth scripts injected!")
    
    def load_session_cookies(self):
        """โหลด cookies จาก session file"""
        print("🍪 Loading session cookies...")
        
        session_file = "/workspaces/sugarglitch-realops/sessions/alx_trading_sessionid_1748519715.json"
        
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Navigate to Instagram first
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)
            
            # Add cookies
            if 'sessionid' in session_data:
                cookie = {
                    'name': 'sessionid',
                    'value': session_data['sessionid'],
                    'domain': '.instagram.com',
                    'path': '/',
                    'secure': True,
                    'httpOnly': True
                }
                self.driver.add_cookie(cookie)
                print("✅ Session cookie added")
                
                # Refresh to apply cookies
                self.driver.refresh()
                time.sleep(3)
                return True
                
        except Exception as e:
            print(f"❌ Cookie loading error: {e}")
        
        return False
    
    def extract_profile_data(self, username):
        """ดึงข้อมูล profile ด้วย undetected browser"""
        print(f"🎯 Extracting profile: {username}")
        
        try:
            # Navigate to profile
            profile_url = f"https://www.instagram.com/{username}/"
            self.driver.get(profile_url)
            
            # Random human-like delay
            time.sleep(random.uniform(3, 7))
            
            # Wait for page to load
            wait = WebDriverWait(self.driver, 15)
            
            profile_data = {}
            
            # Extract basic profile info
            try:
                # Username
                username_elem = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
                profile_data['username'] = username_elem.text
                
                # Full name
                try:
                    full_name = self.driver.find_element(By.XPATH, "//span[contains(@class, 'x1lliihq')]")
                    profile_data['full_name'] = full_name.text
                except:
                    profile_data['full_name'] = ""
                
                # Bio
                try:
                    bio_elem = self.driver.find_element(By.XPATH, "//h1/..//span")
                    profile_data['biography'] = bio_elem.text
                except:
                    profile_data['biography'] = ""
                
                # Follower/Following counts
                stats_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/followers/')]/..//span | //a[contains(@href, '/following/')]/..//span")
                
                stats = []
                for elem in stats_elements:
                    try:
                        text = elem.text.strip()
                        if text and any(c.isdigit() for c in text):
                            stats.append(text)
                    except:
                        continue
                
                if len(stats) >= 2:
                    profile_data['followers'] = stats[0]
                    profile_data['following'] = stats[1]
                
                # Posts count
                try:
                    posts_elem = self.driver.find_element(By.XPATH, "//div[contains(text(), 'posts') or contains(text(), 'โพสต์')]")
                    profile_data['posts'] = posts_elem.text
                except:
                    profile_data['posts'] = "0"
                
                # Check if private
                private_indicators = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'This account is private') or contains(text(), 'บัญชีนี้เป็นส่วนตัว')]")
                profile_data['is_private'] = len(private_indicators) > 0
                
                # Profile picture URL
                try:
                    img_elem = self.driver.find_element(By.XPATH, "//img[contains(@alt, 'profile picture')]")
                    profile_data['profile_pic_url'] = img_elem.get_attribute('src')
                except:
                    profile_data['profile_pic_url'] = ""
                
                print(f"✅ Profile data extracted for {username}")
                print(f"   👤 Full name: {profile_data.get('full_name', 'N/A')}")
                print(f"   👥 Followers: {profile_data.get('followers', 'N/A')}")
                print(f"   🔒 Private: {profile_data.get('is_private', False)}")
                
                return profile_data
                
            except TimeoutException:
                print(f"❌ Timeout loading profile: {username}")
                
        except Exception as e:
            print(f"❌ Profile extraction error for {username}: {e}")
        
        return None
    
    def run_stealth_extraction(self):
        """รันการดึงข้อมูลแบบ stealth"""
        print("🥷 UNDETECTED CHROME STEALTH EXTRACTOR")
        print("=" * 50)
        
        try:
            # Setup browser
            self.setup_undetected_browser()
            
            # Load session cookies
            session_loaded = self.load_session_cookies()
            
            if session_loaded:
                print("✅ Session cookies loaded")
            else:
                print("⚠️ No session - extracting public data only")
            
            # Extract data for each target
            for username in self.targets:
                print(f"\n🎯 Processing: {username}")
                
                # Human-like delay between requests
                delay = random.uniform(10, 20)
                print(f"⏰ Human-like delay: {delay:.1f}s")
                time.sleep(delay)
                
                # Extract profile
                profile_data = self.extract_profile_data(username)
                
                if profile_data:
                    self.results['accounts'][username] = profile_data
                    print(f"✅ Successfully extracted: {username}")
                else:
                    print(f"❌ Failed to extract: {username}")
            
            # Save results
            self.save_results()
            
            print("\n🎉 Stealth extraction completed!")
            
        finally:
            # Clean up
            if self.driver:
                self.driver.quit()
                print("🧹 Browser cleaned up")
        
        return self.results
    
    def save_results(self):
        """บันทึกผลลัพธ์"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/workspaces/sugarglitch-realops/results/undetected_chrome_results_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved: {filename}")

if __name__ == "__main__":
    extractor = UndetectedChromeExtractor()
    results = extractor.run_stealth_extraction()
    
    # Print summary
    print("\n📊 EXTRACTION SUMMARY")
    print("=" * 40)
    for username, data in results['accounts'].items():
        if data:
            print(f"👤 {username}:")
            print(f"   📱 Full name: {data.get('full_name', 'N/A')}")
            print(f"   👥 Followers: {data.get('followers', 'N/A')}")
            print(f"   📷 Posts: {data.get('posts', 'N/A')}")
            print(f"   🔒 Private: {data.get('is_private', False)}")
