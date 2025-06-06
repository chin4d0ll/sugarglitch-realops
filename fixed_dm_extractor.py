#!/usr/bin/env python3
"""
Fixed Instagram DM Extractor - With Correct Username
"""

import json
import requests
import time
import sys
from pathlib import Path
from datetime import datetime

class FixedDMExtractor:
    def __init__(self):
        self.correct_username = "alxtrading"  # Fixed username without period
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'X-Requested-With': 'XMLHttpRequest',
        })
    
    def find_valid_session(self):
        """Find a valid session from available session files"""
        print("🔍 Searching for valid session files...")
        
        session_paths = [
            "/workspaces/sugarglitch-realops/tools/session_alx_trading.json",
            "/workspaces/sugarglitch-realops/hijacked_sessions",
            "/workspaces/sugarglitch-realops/sessions"
        ]
        
        for path in session_paths:
            path_obj = Path(path)
            if path_obj.is_file():
                try:
                    with open(path_obj, 'r') as f:
                        data = json.load(f)
                        sessionid = self.extract_sessionid(data)
                        if sessionid and self.test_session(sessionid):
                            print(f"✅ Found valid session in: {path}")
                            return sessionid
                except:
                    continue
            elif path_obj.is_dir():
                for session_file in path_obj.glob("*.json"):
                    try:
                        with open(session_file, 'r') as f:
                            data = json.load(f)
                            sessionid = self.extract_sessionid(data)
                            if sessionid and self.test_session(sessionid):
                                print(f"✅ Found valid session in: {session_file}")
                                return sessionid
                    except:
                        continue
        
        print("❌ No valid sessions found")
        return None
    
    def extract_sessionid(self, data):
        """Extract sessionid from various data formats"""
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            # Try different possible keys
            for key in ['sessionid', 'session_id', 'session', 'cookie', 'cookies']:
                if key in data:
                    value = data[key]
                    if isinstance(value, str):
                        return value
                    elif isinstance(value, dict) and 'sessionid' in value:
                        return value['sessionid']
        return None
    
    def test_session(self, sessionid):
        """Test if a session is valid"""
        try:
            self.session.cookies.set('sessionid', sessionid, domain='.instagram.com')
            
            # Test with profile API
            response = self.session.get(
                f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.correct_username}',
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return 'data' in data and 'user' in data['data']
            
        except Exception as e:
            print(f"Session test error: {e}")
        
        return False
    
    def extract_with_session(self, sessionid):
        """Attempt DM extraction with a valid session"""
        print(f"🎯 Attempting extraction for: {self.correct_username}")
        
        self.session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        
        # Get user ID first
        try:
            profile_response = self.session.get(
                f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.correct_username}',
                timeout=10
            )
            
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                user_id = profile_data['data']['user']['id']
                print(f"✅ Found user ID: {user_id}")
                
                # Try to access DMs
                dm_response = self.session.get(
                    f'https://www.instagram.com/api/v1/direct_v2/threads/',
                    timeout=10
                )
                
                if dm_response.status_code == 200:
                    dm_data = dm_response.json()
                    
                    # Save results
                    result = {
                        "timestamp": datetime.now().isoformat(),
                        "target": self.correct_username,
                        "user_id": user_id,
                        "profile_data": profile_data['data']['user'],
                        "dm_data": dm_data,
                        "status": "success"
                    }
                    
                    output_file = f"fixed_extraction_{int(time.time())}.json"
                    with open(output_file, 'w') as f:
                        json.dump(result, f, indent=2)
                    
                    print(f"✅ Extraction successful! Saved to: {output_file}")
                    return True
                else:
                    print(f"❌ DM access failed: {dm_response.status_code}")
            else:
                print(f"❌ Profile access failed: {profile_response.status_code}")
                
        except Exception as e:
            print(f"❌ Extraction error: {e}")
        
        return False
    
    def manual_session_prompt(self):
        """Prompt user to provide a manual session"""
        print("\n🔧 MANUAL SESSION REQUIRED")
        print("=" * 50)
        print("Since no valid sessions were found, you need to:")
        print("1. Open Instagram in your browser")
        print("2. Log into your account")
        print(f"3. Visit: https://www.instagram.com/{self.correct_username}/")
        print("4. Open Developer Tools (F12)")
        print("5. Go to Application → Cookies → instagram.com")
        print("6. Copy the 'sessionid' value")
        print("7. Create a file called 'manual_session.json' with:")
        print('   {"sessionid": "YOUR_SESSION_ID_HERE"}')
        print("8. Re-run this script")
        
        # Check if manual session exists
        manual_path = Path("manual_session.json")
        if manual_path.exists():
            try:
                with open(manual_path, 'r') as f:
                    data = json.load(f)
                    sessionid = data.get('sessionid')
                    if sessionid:
                        print("🔍 Found manual_session.json, testing...")
                        if self.test_session(sessionid):
                            print("✅ Manual session is valid!")
                            return sessionid
                        else:
                            print("❌ Manual session is invalid/expired")
            except Exception as e:
                print(f"❌ Error reading manual session: {e}")
        
        return None

def main():
    print("🚀 FIXED Instagram DM Extractor")
    print("=" * 50)
    
    extractor = FixedDMExtractor()
    
    # First try to find existing valid session
    sessionid = extractor.find_valid_session()
    
    # If no valid session found, prompt for manual
    if not sessionid:
        sessionid = extractor.manual_session_prompt()
    
    # If we have a valid session, attempt extraction
    if sessionid:
        success = extractor.extract_with_session(sessionid)
        if success:
            print("\n🎉 EXTRACTION COMPLETED SUCCESSFULLY!")
        else:
            print("\n❌ EXTRACTION FAILED - Check logs for details")
    else:
        print("\n⚠️  NO VALID SESSION AVAILABLE")
        print("   Please follow the manual steps above to get a fresh session")

if __name__ == "__main__":
    main()
