#!/usr/bin/env python3
"""
🎯 ADVANCED ALX.TRADING DM EXTRACTOR
Advanced multi-method extractor for @alx.trading DMs
Uses browser automation, API calls, and session injection
"""

import json
import os
import requests
import sqlite3
import time
from datetime import datetime
from pathlib import Path

class AdvancedAlxExtractor:
    def __init__(self):
        self.target = "alx.trading"
        self.session_file = "/workspaces/sugarglitch-realops/sessions/session-alx.trading"
        self.output_dir = "/workspaces/sugarglitch-realops/data/alx_trading_advanced"
        self.db_path = f"{self.output_dir}/advanced_extraction.db"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load session
        self.session_data = self.load_session()
        self.cookies = self.extract_cookies()
        
        print(f"🎯 Advanced ALX.Trading DM Extractor")
        print(f"Target: {self.target}")
        print(f"Output: {self.output_dir}")
        
    def load_session(self):
        """Load and parse session file"""
        try:
            with open(self.session_file, 'r') as f:
                content = f.read().strip()
                
            # Try to parse as JSON first
            try:
                return json.loads(content)
            except:
                # If not JSON, assume it's raw sessionid
                return {"sessionid": content}
                
        except Exception as e:
            print(f"❌ Session load error: {e}")
            return None
    
    def extract_cookies(self):
        """Extract cookies from session data"""
        if not self.session_data:
            return {}
            
        cookies = {}
        
        if isinstance(self.session_data, dict):
            if 'cookies' in self.session_data:
                cookies = self.session_data['cookies']
            elif 'sessionid' in self.session_data:
                cookies['sessionid'] = self.session_data['sessionid']
        elif isinstance(self.session_data, str):
            cookies['sessionid'] = self.session_data
            
        print(f"✅ Cookies extracted: {list(cookies.keys())}")
        return cookies
    
    def setup_database(self):
        """Setup SQLite database for results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extraction_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                method TEXT,
                timestamp TEXT,
                success BOOLEAN,
                result_data TEXT,
                error_message TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dm_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT,
                message_id TEXT,
                sender TEXT,
                recipient TEXT,
                content TEXT,
                timestamp TEXT,
                message_type TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database setup complete")
    
    def method_1_direct_api(self):
        """Method 1: Direct Instagram API calls"""
        print("\n🔄 METHOD 1: Direct API Calls")
        print("=" * 40)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.instagram.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': '',
            'X-Instagram-AJAX': '1',
        }
        
        session = requests.Session()
        session.cookies.update(self.cookies)
        session.headers.update(headers)
        
        # Get CSRF token
        try:
            response = session.get('https://www.instagram.com/')
            if response.status_code == 200:
                # Extract CSRF token from response
                import re
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    session.headers['X-CSRFToken'] = csrf_token
                    print(f"✅ CSRF token: {csrf_token[:20]}...")
                else:
                    print("⚠️ No CSRF token found")
        except Exception as e:
            print(f"❌ CSRF error: {e}")
        
        # Try multiple endpoints
        endpoints = [
            'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'https://www.instagram.com/api/v1/direct_v2/threads/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'https://www.instagram.com/direct/inbox/',
        ]
        
        results = []
        for endpoint in endpoints:
            try:
                print(f"🔍 Testing: {endpoint}")
                response = session.get(endpoint, timeout=30)
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'inbox' in data or 'threads' in data:
                            results.append({
                                'endpoint': endpoint,
                                'data': data,
                                'success': True
                            })
                            print(f"   ✅ JSON data found")
                        else:
                            print(f"   ⚠️ No inbox/threads in response")
                    except:
                        print(f"   ⚠️ Non-JSON response")
                        # Save HTML for debugging
                        debug_file = f"{self.output_dir}/debug_{int(time.time())}.html"
                        with open(debug_file, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        print(f"   📁 Debug saved: {debug_file}")
                else:
                    print(f"   ❌ Status {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
        return results
    
    def method_2_profile_scraping(self):
        """Method 2: Profile page scraping for DM hints"""
        print("\n🔄 METHOD 2: Profile Scraping")
        print("=" * 40)
        
        session = requests.Session()
        session.cookies.update(self.cookies)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.instagram.com/',
        }
        session.headers.update(headers)
        
        urls_to_try = [
            f'https://www.instagram.com/{self.target}/',
            f'https://www.instagram.com/direct/t/',
            'https://www.instagram.com/direct/inbox/',
        ]
        
        results = []
        for url in urls_to_try:
            try:
                print(f"🔍 Accessing: {url}")
                response = session.get(url, timeout=30)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    # Look for data in the HTML
                    html = response.text
                    
                    # Search for JSON data in script tags
                    import re
                    
                    # Look for window._sharedData
                    shared_data_match = re.search(r'window\._sharedData\s*=\s*({.+?});', html)
                    if shared_data_match:
                        try:
                            shared_data = json.loads(shared_data_match.group(1))
                            results.append({
                                'url': url,
                                'shared_data': shared_data,
                                'type': 'shared_data'
                            })
                            print(f"   ✅ Shared data found")
                        except:
                            print(f"   ⚠️ Shared data parse error")
                    
                    # Look for user data
                    user_data_matches = re.findall(r'"username":"([^"]+)"', html)
                    if user_data_matches:
                        print(f"   👤 Users found: {len(set(user_data_matches))}")
                        results.append({
                            'url': url,
                            'users': list(set(user_data_matches)),
                            'type': 'user_mentions'
                        })
                    
                    # Save full HTML for analysis
                    html_file = f"{self.output_dir}/page_{url.replace('/', '_').replace(':', '')}.html"
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(html)
                    print(f"   📁 HTML saved: {html_file}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
        return results
    
    def method_3_graphql_queries(self):
        """Method 3: GraphQL queries"""
        print("\n🔄 METHOD 3: GraphQL Queries")
        print("=" * 40)
        
        session = requests.Session()
        session.cookies.update(self.cookies)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/',
        }
        session.headers.update(headers)
        
        # Common GraphQL queries for DMs
        queries = [
            {
                'name': 'DirectInbox',
                'query': '{"query":"query DirectInbox($cursor: String) { viewer { direct_messages(first: 20, after: $cursor) { edges { node { id thread_id created_at sender { username } message_text } } page_info { has_next_page end_cursor } } } }"}',
            },
            {
                'name': 'UserDMs',
                'query': f'{{"query":"query UserDMs {{ user(username: \\"{self.target}\\") {{ direct_messages {{ id thread_id message_text created_at }} }} }}"}}',
            }
        ]
        
        results = []
        graphql_url = 'https://www.instagram.com/api/graphql/'
        
        for query_info in queries:
            try:
                print(f"🔍 Testing GraphQL: {query_info['name']}")
                
                response = session.post(
                    graphql_url,
                    data=query_info['query'],
                    timeout=30
                )
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        results.append({
                            'query': query_info['name'],
                            'data': data,
                            'success': True
                        })
                        print(f"   ✅ GraphQL response received")
                    except:
                        print(f"   ⚠️ Non-JSON GraphQL response")
                        
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
        return results
    
    def save_results(self, all_results):
        """Save all results to files and database"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        json_file = f"{self.output_dir}/extraction_results_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        total_messages = 0
        for method, results in all_results.items():
            cursor.execute('''
                INSERT INTO extraction_attempts 
                (method, timestamp, success, result_data, error_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                method,
                timestamp,
                len(results) > 0,
                json.dumps(results),
                None
            ))
            
            # Count any messages found
            for result in results:
                if isinstance(result, dict) and 'data' in result:
                    # Try to count messages in the data
                    data_str = str(result['data'])
                    if 'message' in data_str.lower():
                        total_messages += 1
        
        conn.commit()
        conn.close()
        
        print(f"\n📊 EXTRACTION SUMMARY")
        print("=" * 40)
        print(f"📁 Results saved: {json_file}")
        print(f"🗄️ Database: {self.db_path}")
        print(f"📨 Potential messages: {total_messages}")
        
        return json_file
    
    def run_extraction(self):
        """Run all extraction methods"""
        print(f"🚀 Starting advanced extraction for {self.target}")
        
        if not self.cookies:
            print("❌ No valid session cookies found")
            return
            
        # Setup database
        self.setup_database()
        
        # Run all methods
        all_results = {}
        
        try:
            all_results['direct_api'] = self.method_1_direct_api()
        except Exception as e:
            print(f"❌ Method 1 failed: {e}")
            all_results['direct_api'] = []
        
        try:
            all_results['profile_scraping'] = self.method_2_profile_scraping()
        except Exception as e:
            print(f"❌ Method 2 failed: {e}")
            all_results['profile_scraping'] = []
        
        try:
            all_results['graphql_queries'] = self.method_3_graphql_queries()
        except Exception as e:
            print(f"❌ Method 3 failed: {e}")
            all_results['graphql_queries'] = []
        
        # Save all results
        result_file = self.save_results(all_results)
        
        print(f"\n✅ Advanced extraction completed")
        print(f"📁 Check results in: {self.output_dir}")
        
        return result_file

if __name__ == "__main__":
    extractor = AdvancedAlxExtractor()
    extractor.run_extraction()
