#!/usr/bin/env python3
"""
Real Session Validation with Instagram API
Tests if a session can actually access Instagram endpoints
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import os
import time
from datetime import datetime

class SessionValidator:
    def __init__(self):
        self.session_data = None
        
    def load_session(self, session_file):
        """Load session from file"""
        try:
            if not os.path.exists(session_file):
                print(f"❌ Session file not found: {session_file}")
                return False
                
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Extract sessionid from various possible locations
            sessionid = (data.get("sessionid") or 
                        data.get("session_id") or
                        data.get("cookies", {}).get("sessionid"))
            
            if not sessionid:
                print("❌ No sessionid found in session file")
                return False
            
            self.session_data = {
                "sessionid": sessionid,
                "csrf_token": (data.get("csrf_token") or 
                              data.get("csrftoken") or 
                              data.get("cookies", {}).get("csrftoken")),
                "user_agent": data.get("user_agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15")
            }
            
            print(f"✅ Session loaded: {sessionid[:20]}...")
            return True
            
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return False
    
    def validate_session(self):
        """Validate session by making actual Instagram API calls"""
        if not self.session_data:
            print("❌ No session data loaded")
            return False
        
        print("🔍 Validating session with real Instagram API calls...")
        
        # Test 1: Try to access Instagram main page with session
        print("\n1️⃣ Testing main page access with session...")
        if not self._test_main_page():
            return False
        
        # Test 2: Try to access user info endpoint
        print("\n2️⃣ Testing user info endpoint...")
        if not self._test_user_info():
            return False
            
        # Test 3: Try to access inbox/direct messages endpoint
        print("\n3️⃣ Testing direct messages endpoint...")
        return self._test_dm_endpoint()
    
    def _test_main_page(self):
        """Test access to Instagram main page"""
        try:
            headers = {
                'User-Agent': self.session_data['user_agent'],
                'Cookie': f'sessionid={self.session_data["sessionid"]}'
            }
            
            if self.session_data.get('csrf_token'):
                headers['X-CSRFToken'] = self.session_data['csrf_token']
            
            req = urllib.request.Request('https://www.instagram.com/', headers=headers)
            response = urllib.request.urlopen(req, timeout=15)
            content = response.read().decode('utf-8')
            
            if 'login' in content.lower() and 'password' in content.lower():
                print("❌ Session expired - redirected to login page")
                return False
            elif 'feed' in content.lower() or 'timeline' in content.lower():
                print("✅ Session valid - authenticated content loaded")
                return True
            else:
                print("🟡 Unclear response - session may be partially valid")
                return True
                
        except urllib.error.HTTPError as e:
            if e.code == 302:
                print("🟡 Redirect received - checking location...")
                location = e.headers.get('Location', '')
                if 'login' in location:
                    print("❌ Redirected to login - session expired")
                    return False
                else:
                    print("✅ Redirect but not to login - session may be valid")
                    return True
            else:
                print(f"❌ HTTP Error: {e.code} - {e.reason}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _test_user_info(self):
        """Test access to user info endpoint"""
        try:
            headers = {
                'User-Agent': self.session_data['user_agent'],
                'Cookie': f'sessionid={self.session_data["sessionid"]}',
                'Accept': 'application/json'
            }
            
            if self.session_data.get('csrf_token'):
                headers['X-CSRFToken'] = self.session_data['csrf_token']
            
            req = urllib.request.Request('https://www.instagram.com/accounts/edit/', headers=headers)
            response = urllib.request.urlopen(req, timeout=10)
            
            if response.getcode() == 200:
                print("✅ User info endpoint accessible")
                return True
            else:
                print(f"🟡 User info returned {response.getcode()}")
                return False
                
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print("❌ Forbidden - session lacks permissions")
                return False
            elif e.code == 302:
                print("🟡 Redirected - session may be valid but endpoint different")
                return True
            else:
                print(f"🟡 HTTP {e.code} - {e.reason}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _test_dm_endpoint(self):
        """Test access to direct messages endpoint"""
        try:
            headers = {
                'User-Agent': self.session_data['user_agent'],
                'Cookie': f'sessionid={self.session_data["sessionid"]}',
                'Accept': 'application/json'
            }
            
            if self.session_data.get('csrf_token'):
                headers['X-CSRFToken'] = self.session_data['csrf_token']
            
            # Try the direct messages API endpoint
            req = urllib.request.Request('https://i.instagram.com/api/v1/direct_v2/inbox/', headers=headers)
            response = urllib.request.urlopen(req, timeout=10)
            
            if response.getcode() == 200:
                print("✅ Direct messages endpoint accessible!")
                content = response.read().decode('utf-8')
                try:
                    data = json.loads(content)
                    if 'inbox' in data:
                        print("✅ Got inbox data - DM extraction should work!")
                        return True
                except:
                    pass
                print("✅ DM endpoint responded positively")
                return True
            else:
                print(f"🟡 DM endpoint returned {response.getcode()}")
                return False
                
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print("❌ DM endpoint forbidden - insufficient permissions")
                return False
            elif e.code == 401:
                print("❌ DM endpoint unauthorized - session invalid")
                return False
            else:
                print(f"🟡 DM endpoint HTTP {e.code} - {e.reason}")
                return False
        except Exception as e:
            print(f"❌ DM endpoint error: {e}")
            return False

def main():
    print("🔐 Instagram Session Validator")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now()}")
    
    validator = SessionValidator()
    
    # Test multiple session files
    session_files = [
        "alx_trading_session_fleming654.json",
        "fresh_sessions/working_session_1749202526.json",
        "session.json"
    ]
    
    for session_file in session_files:
        if os.path.exists(session_file):
            print(f"\n🔍 Testing session file: {session_file}")
            print("-" * 40)
            
            if validator.load_session(session_file):
                if validator.validate_session():
                    print(f"✅ Session {session_file} is VALID and ready for DM extraction!")
                    # Save result
                    result = {
                        "timestamp": datetime.now().isoformat(),
                        "session_file": session_file,
                        "status": "VALID",
                        "ready_for_extraction": True
                    }
                    with open(f"session_validation_{int(time.time())}.json", 'w') as f:
                        json.dump(result, f, indent=2)
                    return True
                else:
                    print(f"❌ Session {session_file} is INVALID")
            else:
                print(f"❌ Could not load session {session_file}")
        else:
            print(f"⚠️  Session file not found: {session_file}")
    
    print("\n❌ No valid sessions found")
    return False

if __name__ == "__main__":
    main()
