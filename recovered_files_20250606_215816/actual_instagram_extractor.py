#!/usr/bin/env python3
"""
🎯 ACTUAL INSTAGRAM DM EXTRACTOR - NO MOCKUP
===========================================
ดึงข้อมูล DM จริงจาก Instagram โดยไม่ใช้ mockup
- ใช้ session cookies จริง
- เรียก Instagram endpoints จริง
- ตรวจสอบการเข้าถึงจริง
- รายงานผลจริง (ไม่ใช่ simulation)
"""

import json
import os
import time
import requests
import sqlite3
from datetime import datetime
from pathlib import Path
import urllib.parse
from target_database_manager import TargetDatabaseManager

class ActualInstagramExtractor:
    """🎯 Extract actual data from Instagram - NO MOCKUP"""
    
    def __init__(self):
        self.target = "alx.trading"
        self.project_root = "/workspaces/sugarglitch-realops"
        
        # Load real session
        self.session_cookies = self.load_actual_session()
        
        # Instagram endpoints
        self.base_url = "https://www.instagram.com"
        
        # Real headers from browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.instagram.com/',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        # Database
        self.db_manager = TargetDatabaseManager(f"{self.project_root}/integrated_targets_2025.db")
        
        # Output directory for REAL data only
        self.output_dir = f"{self.project_root}/actual_extraction/alx_trading"
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"🎯 ACTUAL Instagram Extractor - NO MOCKUP")
        print(f"   Target: {self.target}")
        print(f"   Real session loaded: {'✅' if self.session_cookies else '❌'}")
    
    def load_actual_session(self):
        """Load actual session cookies"""
        session_file = f"{self.project_root}/sessions/session-alx.trading"
        
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
                cookies = data.get('cookies', {})
                print(f"✅ Loaded session with cookies: {list(cookies.keys())}")
                return cookies
        except Exception as e:
            print(f"❌ Failed to load session: {e}")
            return None
    
    def create_authenticated_session(self):
        """Create session with real cookies"""
        session = requests.Session()
        
        if self.session_cookies:
            for name, value in self.session_cookies.items():
                session.cookies.set(name, value, domain='.instagram.com')
        
        session.headers.update(self.headers)
        return session
    
    def test_session_validity(self):
        """Test if session is actually valid"""
        print(f"\n🔍 TESTING SESSION VALIDITY")
        print(f"============================")
        
        session = self.create_authenticated_session()
        
        try:
            # Test basic Instagram access
            response = session.get(f"{self.base_url}/", timeout=10)
            print(f"📡 Instagram homepage: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                
                # Check if logged in
                if '"is_logged_in":true' in content or 'sessionid' in response.cookies:
                    print(f"✅ Session appears valid - logged in")
                    return True
                elif '"is_logged_in":false' in content:
                    print(f"❌ Session invalid - not logged in")
                    return False
                else:
                    print(f"⚠️ Cannot determine login status")
                    return False
            else:
                print(f"❌ Cannot access Instagram: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Session test error: {e}")
            return False
    
    def get_user_profile_real(self, username):
        """Get real user profile data"""
        print(f"🔍 Getting real profile data for {username}")
        
        session = self.create_authenticated_session()
        
        try:
            url = f"{self.base_url}/{username}/"
            response = session.get(url, timeout=10)
            
            print(f"📡 Profile page response: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                
                # Look for actual profile data
                profile_data = {
                    'username': username,
                    'accessible': True,
                    'profile_found': True,
                    'response_size': len(content),
                    'timestamp': datetime.now().isoformat()
                }
                
                # Check if profile exists
                if "Sorry, this page isn't available" in content:
                    profile_data['profile_found'] = False
                    print(f"❌ Profile not found")
                elif 'This account is private' in content:
                    profile_data['private'] = True
                    print(f"🔒 Profile is private")
                else:
                    profile_data['private'] = False
                    print(f"✅ Profile accessible")
                
                return profile_data
                
            elif response.status_code == 404:
                print(f"❌ Profile not found (404)")
                return {'username': username, 'profile_found': False, 'error': '404'}
            elif response.status_code == 429:
                print(f"⚠️ Rate limited (429)")
                return {'username': username, 'error': 'rate_limited'}
            else:
                print(f"❌ Error {response.status_code}")
                return {'username': username, 'error': f'http_{response.status_code}'}
                
        except Exception as e:
            print(f"❌ Profile extraction error: {e}")
            return {'username': username, 'error': str(e)}
    
    def attempt_dm_access_real(self):
        """Attempt to access real DM endpoints"""
        print(f"\n🔍 ATTEMPTING REAL DM ACCESS")
        print(f"==============================")
        
        session = self.create_authenticated_session()
        
        # Try different DM endpoints
        dm_endpoints = [
            '/direct/inbox/',
            '/api/v1/direct_v2/inbox/',
            '/direct/t/',
        ]
        
        results = []
        
        for endpoint in dm_endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                print(f"🔗 Trying: {endpoint}")
                
                response = session.get(url, timeout=10)
                
                result = {
                    'endpoint': endpoint,
                    'status_code': response.status_code,
                    'response_size': len(response.content),
                    'timestamp': datetime.now().isoformat()
                }
                
                if response.status_code == 200:
                    print(f"   ✅ Success: {response.status_code}")
                    
                    # Check for actual DM content
                    content = response.text
                    if 'direct' in content.lower() or 'message' in content.lower():
                        result['contains_dm_content'] = True
                        print(f"   📨 Contains DM-related content")
                    else:
                        result['contains_dm_content'] = False
                        print(f"   ⚠️ No DM content detected")
                        
                elif response.status_code == 302:
                    print(f"   🔄 Redirect: {response.status_code}")
                    result['redirect'] = True
                elif response.status_code == 403:
                    print(f"   🚫 Forbidden: {response.status_code}")
                    result['forbidden'] = True
                elif response.status_code == 429:
                    print(f"   ⚠️ Rate limited: {response.status_code}")
                    result['rate_limited'] = True
                else:
                    print(f"   ❌ Error: {response.status_code}")
                
                results.append(result)
                time.sleep(2)  # Delay between requests
                
            except Exception as e:
                print(f"   ❌ Exception: {e}")
                results.append({
                    'endpoint': endpoint,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        return results
    
    def perform_actual_extraction(self):
        """Perform actual extraction - NO MOCKUP"""
        print(f"\n🎯 STARTING ACTUAL EXTRACTION")
        print(f"==============================")
        print(f"Target: {self.target}")
        print(f"NO MOCKUP - REAL DATA ONLY")
        
        extraction_result = {
            'extraction_info': {
                'target': self.target,
                'timestamp': datetime.now().isoformat(),
                'method': 'actual_instagram_extraction',
                'no_mockup': True,
                'real_data_only': True
            },
            'session_test': None,
            'profile_data': None,
            'dm_access_attempts': [],
            'actual_data_found': False,
            'extraction_errors': []
        }
        
        try:
            # Test session validity
            extraction_result['session_test'] = {
                'valid': self.test_session_validity(),
                'timestamp': datetime.now().isoformat()
            }
            
            # Get real profile data
            if extraction_result['session_test']['valid']:
                extraction_result['profile_data'] = self.get_user_profile_real(self.target)
                
                # Attempt DM access
                extraction_result['dm_access_attempts'] = self.attempt_dm_access_real()
                
                # Check if any actual data was found
                if extraction_result['profile_data'].get('profile_found'):
                    extraction_result['actual_data_found'] = True
                
            else:
                extraction_result['extraction_errors'].append("Session invalid - cannot proceed")
            
        except Exception as e:
            error_msg = f"Extraction error: {str(e)}"
            extraction_result['extraction_errors'].append(error_msg)
            print(f"❌ {error_msg}")
        
        # Save REAL results only
        timestamp = int(time.time())
        output_file = f"{self.output_dir}/actual_extraction_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extraction_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ ACTUAL EXTRACTION COMPLETED")
        print(f"📂 Results saved: {output_file}")
        print(f"🎯 Actual data found: {extraction_result['actual_data_found']}")
        print(f"❌ Errors: {len(extraction_result['extraction_errors'])}")
        
        # Update database with REAL results
        try:
            operation_id = self.db_manager.log_operation(
                self.target,
                'actual_extraction_no_mockup',
                json.dumps({
                    'actual_data_found': extraction_result['actual_data_found'],
                    'session_valid': extraction_result['session_test']['valid'] if extraction_result['session_test'] else False,
                    'errors': extraction_result['extraction_errors']
                })
            )
            print(f"✅ Database updated - Operation ID: {operation_id}")
        except Exception as e:
            print(f"⚠️ Database update warning: {e}")
        
        return extraction_result
    
    def report_actual_findings(self, result):
        """Report only actual findings - NO MOCKUP"""
        print(f"\n📊 ACTUAL FINDINGS REPORT")
        print(f"==========================")
        print(f"Target: {self.target}")
        print(f"Method: Real extraction only")
        
        # Session status
        if result['session_test']:
            session_status = "✅ Valid" if result['session_test']['valid'] else "❌ Invalid"
            print(f"Session: {session_status}")
        
        # Profile data
        if result['profile_data']:
            profile = result['profile_data']
            if profile.get('profile_found'):
                privacy = "🔒 Private" if profile.get('private') else "🌐 Public"
                print(f"Profile: ✅ Found ({privacy})")
            else:
                print(f"Profile: ❌ Not found")
        
        # DM access
        print(f"DM Access Attempts: {len(result['dm_access_attempts'])}")
        for attempt in result['dm_access_attempts']:
            status = attempt.get('status_code', 'Error')
            endpoint = attempt.get('endpoint', 'Unknown')
            if status == 200:
                print(f"  ✅ {endpoint}: Success")
            elif status in [403, 429]:
                print(f"  🚫 {endpoint}: Blocked ({status})")
            else:
                print(f"  ❌ {endpoint}: Failed ({status})")
        
        # Errors
        if result['extraction_errors']:
            print(f"Errors:")
            for error in result['extraction_errors']:
                print(f"  ❌ {error}")
        
        print(f"\n🎯 ACTUAL DATA FOUND: {'YES' if result['actual_data_found'] else 'NO'}")

def main():
    """Main execution - REAL DATA ONLY"""
    print("🎯 ACTUAL INSTAGRAM DM EXTRACTOR - NO MOCKUP")
    print("============================================")
    print("This tool attempts to extract REAL data only")
    print("NO simulation, NO mockup, NO fake data")
    
    extractor = ActualInstagramExtractor()
    result = extractor.perform_actual_extraction()
    extractor.report_actual_findings(result)

if __name__ == "__main__":
    main()