#!/usr/bin/env python3
"""
🔥 FRESH SESSION EXTRACTOR - ALX.TRADING 🔥
============================================

Extract fresh Instagram session for alx.trading using confirmed Fleming654 pattern
Returns ready-to-use sessionid and ds_user_id

Author: SugarGlitch RealOps Team
Date: May 27, 2025
Target: alx.trading (CONFIRMED WORKING)
"""

import requests
import re
import json
import time
import random
from datetime import datetime

class FreshSessionExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.target_username = "alx.trading"
        self.confirmed_password = "Fleming654"  # ✅ CONFIRMED WORKING
        
        # Headers to mimic real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': '',
            'X-Instagram-AJAX': '1',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        
        print("🔥" * 20)
        print("🎯 FRESH SESSION EXTRACTOR")
        print("🔥" * 20)
        print(f"🎯 Target: {self.target_username}")
        print(f"🔑 Password: {self.confirmed_password}")
        print("🚀 Starting fresh session extraction...")
        print()

    def get_csrf_token(self):
        """Extract fresh CSRF token from Instagram login page"""
        try:
            print("📡 Getting fresh CSRF token...")
            response = self.session.get('https://www.instagram.com/accounts/login/', headers=self.headers)
            
            if response.status_code == 200:
                # Extract CSRF token from page
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    self.headers['X-CSRFToken'] = csrf_token
                    print(f"✅ CSRF Token obtained: {csrf_token[:20]}...")
                    return csrf_token
                    
                # Fallback: try from cookies
                csrf_token = None
                for cookie in self.session.cookies:
                    if cookie.name == 'csrftoken':
                        csrf_token = cookie.value
                        self.headers['X-CSRFToken'] = csrf_token
                        print(f"✅ CSRF Token from cookie: {csrf_token[:20]}...")
                        return csrf_token
                if not csrf_token:
                    print("❌ Failed to get CSRF token from cookies")
            print("❌ Failed to get CSRF token")
            return None
            
        except Exception as e:
            print(f"❌ CSRF extraction error: {str(e)}")
            return None

    def attempt_login(self):
        """Attempt login with confirmed credentials"""
        try:
            csrf_token = self.get_csrf_token()
            if not csrf_token:
                return None
                
            time.sleep(random.uniform(2, 4))
            
            login_data = {
                'username': self.target_username,
                'password': self.confirmed_password,
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}'
            }
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=self.headers,
                allow_redirects=False
            )
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code in [200, 302]:
                try:
                    response_data = response.json()
                    print(f"📄 Response: {json.dumps(response_data, indent=2)}")
                    
                    # Check for successful login
                    if response_data.get('authenticated') == True:
                        print("🎉 LOGIN SUCCESSFUL!")
                        return self.extract_session_data()
                        
                    elif response_data.get('status') == 'ok':
                        print("✅ Login OK - extracting session...")
                        return self.extract_session_data()
                        
                    elif response_data.get('checkpoint_url') or response_data.get('checkpoint_required'):
                        print("🔒 Checkpoint required - but credentials confirmed!")
                        print(f"🔗 Checkpoint URL: {response_data.get('checkpoint_url', 'N/A')}")
                        return self.extract_session_data()
                        
                    else:
                        print(f"⚠️ Unexpected response: {response_data}")
                        
                except Exception as ex:
                    print("📄 Non-JSON or error in response received")
                    print(f"Response content: {response.text[:500]}...")
                    print(f"Exception: {str(ex)}")
                    
            return None
                    
            return None
            
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return None

    def extract_session_data(self):
        """Extract session ID and user ID from cookies"""
        try:
            session_data = {}
            for cookie in self.session.cookies:
                try:
                    print(f"   {cookie.name}: {cookie.value[:50]}...")
                except Exception:
                    print(f"   {cookie.name}: <unprintable value>")
                
                if cookie.name == 'sessionid':
                    session_data['sessionid'] = cookie.value
                elif cookie.name == 'ds_user_id':
                    session_data['ds_user_id'] = cookie.value
                    
            if 'sessionid' in session_data:
                print("\n🎉 SESSION EXTRACTION SUCCESSFUL!")
                print("=" * 50)
                print(f"Target: {self.target_username}")
                print(f"Password: {self.confirmed_password}")
                print(f"SessionID: {session_data['sessionid']}")
                print(f"User ID: {session_data.get('ds_user_id', 'N/A')}")
                print("=" * 50)
                
                # Save to file
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"fresh_session_alx_trading_{timestamp}.json"
                
                try:
                    with open(filename, 'w') as f:
                        json.dump({
                            'target': self.target_username,
                            'password': self.confirmed_password,
                            'sessionid': session_data['sessionid'],
                            'ds_user_id': session_data.get('ds_user_id'),
                            'extracted_at': timestamp,
                            'status': 'FRESH_ACTIVE'
                        }, f, indent=2)
                    print(f"💾 Session saved to: {filename}")
                except Exception as file_ex:
                    print(f"❌ Failed to save session to file: {str(file_ex)}")
                
                # Test session validity
                self.test_session(session_data['sessionid'])
                
                return session_data
            else:
                print("❌ No sessionid found in cookies")
                return None
                
        except Exception as e:
            print(f"❌ Session extraction error: {str(e)}")
            return None

    def test_session(self, sessionid):
        """Test if extracted session is working"""
        try:
            print("\n🧪 Testing session validity...")
            
            test_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Cookie': f'sessionid={sessionid}'
            }
            
            response = requests.get('https://www.instagram.com/accounts/edit/', headers=test_headers)
            
            if 'accounts/login' not in response.url:
                print("✅ Session is ACTIVE and WORKING!")
                return True
            else:
                print("⚠️ Session may need verification")
                return False
                
        except Exception as e:
            print(f"❌ Session test error: {str(e)}")
            return False

    def run(self):
        """Main execution method"""
        try:
            result = self.attempt_login()
            
            if result:
                print("\n🔥 FRESH SESSION READY FOR USE! 🔥")
                print("\n📋 USAGE INSTRUCTIONS:")
                print("=" * 40)
                print("🌐 Browser Cookie:")
                print(f"sessionid={result['sessionid']}")
                print("\n🐍 Python (instagrapi):")
                print("from instagrapi import Client")
                print("cl = Client()")
                print(f"cl.login_by_sessionid('{result['sessionid']}')")
                print("user = cl.account_info()")
                print("print(user.username)  # Should show: alx.trading")
                print("=" * 40)
                
                return result
            else:
                print("\n❌ Session extraction failed")
                return None
                
        except Exception as e:
            print(f"❌ Execution error: {str(e)}")
            return None

if __name__ == "__main__":
    extractor = FreshSessionExtractor()
    extractor.run()
