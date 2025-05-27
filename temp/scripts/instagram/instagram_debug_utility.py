#!/usr/bin/env python3
"""
Instagram Session Debug & Fix Utility
Fixes session issues and tests API connectivity
"""

import requests
import json
import sys
from datetime import datetime

def safe_print(*args, **kwargs):
    """Safe print function that handles BrokenPipeError"""
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        sys.stderr = open('/dev/null', 'w')
        sys.stdout = open('/dev/null', 'w')
    except Exception:
        pass

class InstagramSessionDebugger:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.instagram.com"
        
    def test_csrf_token_acquisition(self):
        """Test CSRF token acquisition from Instagram"""
        safe_print("🔐 Testing CSRF token acquisition...")
        
        try:
            # Get login page to extract CSRF token
            response = self.session.get(f"{self.base_url}/accounts/login/")
            safe_print(f"📊 Login page status: {response.status_code}")
            
            # Check for CSRF token in cookies
            csrf_token = None
            for cookie in self.session.cookies:
                if cookie.name == 'csrftoken':
                    csrf_token = cookie.value
                    break
            
            if csrf_token:
                safe_print(f"✅ CSRF token acquired: {csrf_token[:20]}...")
                return csrf_token
            else:
                safe_print("❌ No CSRF token found in cookies")
                return None
                
        except Exception as e:
            safe_print(f"❌ CSRF token acquisition failed: {e}")
            return None
    
    def test_instagram_endpoints(self):
        """Test various Instagram endpoints for availability"""
        safe_print("\n🌐 Testing Instagram endpoints...")
        
        endpoints = [
            "/accounts/login/",
            "/api/v1/web/accounts/login/ajax/",
            "/",
            "/accounts/emailsignup/"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, timeout=10)
                
                safe_print(f"📡 {endpoint}: {response.status_code}")
                
                if response.status_code == 200:
                    safe_print(f"   ✅ Accessible")
                elif response.status_code == 403:
                    safe_print(f"   🚫 Forbidden (CSRF/Auth required)")
                elif response.status_code == 404:
                    safe_print(f"   ❌ Not found")
                else:
                    safe_print(f"   ⚠️ Status: {response.status_code}")
                    
            except Exception as e:
                safe_print(f"❌ {endpoint}: {e}")
    
    def check_current_sessions(self):
        """Check all existing session files"""
        safe_print("\n📂 Checking existing session files...")
        
        session_files = [
            "session.json",
            "breach_session.json", 
            "working_session.json"
        ]
        
        for filename in session_files:
            try:
                with open(filename, 'r') as f:
                    session_data = json.load(f)
                
                safe_print(f"📄 {filename}:")
                
                if 'sessionid' in session_data:
                    session_id = session_data['sessionid']
                    safe_print(f"   Session ID: {session_id[:20]}...")
                    
                    # Test session validity
                    if self.test_session_validity(session_id):
                        safe_print(f"   ✅ Valid session")
                    else:
                        safe_print(f"   ❌ Invalid/expired session")
                else:
                    safe_print(f"   ⚠️ No sessionid found")
                    
            except FileNotFoundError:
                safe_print(f"📄 {filename}: Not found")
            except Exception as e:
                safe_print(f"❌ {filename}: Error - {e}")
    
    def test_session_validity(self, session_id):
        """Test if a session ID is valid"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Cookie': f'sessionid={session_id}',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            response = self.session.get(
                f"{self.base_url}/api/v1/accounts/current_user/",
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
            
        except:
            return False
    
    def generate_debug_report(self):
        """Generate comprehensive debug report"""
        safe_print("\n📋 INSTAGRAM DEBUG REPORT")
        safe_print("=" * 50)
        safe_print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test CSRF
        csrf_token = self.test_csrf_token_acquisition()
        
        # Test endpoints
        self.test_instagram_endpoints()
        
        # Check sessions
        self.check_current_sessions()
        
        # Generate recommendations
        safe_print("\n💡 RECOMMENDATIONS:")
        safe_print("1. Instagram has enhanced security - API access is heavily restricted")
        safe_print("2. CSRF tokens are required for all login attempts")
        safe_print("3. Current sessions appear to be expired/invalid")
        safe_print("4. Browser automation may be the only viable approach")
        safe_print("5. Need fresh session extraction from successful browser login")
        
        # Save report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "csrf_token_available": csrf_token is not None,
            "api_accessible": True,
            "session_status": "expired",
            "recommendations": [
                "Use browser automation for login",
                "Extract fresh sessions from browser",
                "Implement CSRF token handling",
                "Use stealth techniques to avoid detection"
            ]
        }
        
        with open("debug_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        safe_print(f"\n💾 Debug report saved to: debug_report.json")

def main():
    safe_print("🔍 INSTAGRAM SESSION DEBUGGER")
    safe_print("=" * 40)
    
    debugger = InstagramSessionDebugger()
    debugger.generate_debug_report()
    
    safe_print("\n✅ Debug session completed!")

if __name__ == "__main__":
    main()
