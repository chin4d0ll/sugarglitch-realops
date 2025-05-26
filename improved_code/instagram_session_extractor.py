from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔐 INSTAGRAM SESSION ID EXTRACTOR 🔐
Target: whatilove1728
Mission: Extract valid Instagram sessionid for authentication
"""

import requests
import json
import time
import re
from datetime import datetime
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class InstagramSessionExtractor:
    def __init__(self):
        self.target_username = "whatilove1728"
        self.target_url = f"https://www.instagram.com/{self.target_username}/"
        
        # Proxy configuration
        self.proxy = {
            'http': 'http://brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95@brd.superproxy.io:22225',
            'https': 'http://brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95@brd.superproxy.io:22225'
        }
        
        # Real browser headers for stealth
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1'
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.proxies.update(self.proxy)
        self.session.verify = False
        
        self.extracted_data = {
            'target': self.target_username,
            'timestamp': datetime.now().isoformat(),
            'session_cookies': {},
            'csrf_tokens': {},
            'app_data': {},
            'user_data': {},
            'authentication_status': 'unknown'
        }

    def extract_instagram_home(self):
        """Extract session data from Instagram homepage"""
        print("🏠 EXTRACTING INSTAGRAM HOME SESSION DATA...")
        
        try:
            response = self.session.get('https://www.instagram.com/', timeout=30)
            
            # Extract cookies
            for cookie in response.cookies:
                self.extracted_data['session_cookies'][cookie.name] = cookie.value
                print(f"   🍪 Cookie: {cookie.name} = {cookie.value[:30]}...")
            
            # Extract CSRF token from HTML
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
            if csrf_match:
                self.extracted_data['csrf_tokens']['html_csrf'] = csrf_match.group(1)
                print(f"   🔑 HTML CSRF Token: {csrf_match.group(1)[:30]}...")
            
            # Extract app ID
            app_id_match = re.search(r'"app_id":"([^"]+)"', response.text)
            if app_id_match:
                self.extracted_data['app_data']['app_id'] = app_id_match.group(1)
                print(f"   📱 App ID: {app_id_match.group(1)}")
            
            # Extract rollout hash
            rollout_match = re.search(r'"rollout_hash":"([^"]+)"', response.text)
            if rollout_match:
                self.extracted_data['app_data']['rollout_hash'] = rollout_match.group(1)
                print(f"   🎲 Rollout Hash: {rollout_match.group(1)}")
            
            # Extract machine ID
            machine_match = re.search(r'"machine_id":"([^"]+)"', response.text)
            if machine_match:
                self.extracted_data['app_data']['machine_id'] = machine_match.group(1)
                print(f"   🤖 Machine ID: {machine_match.group(1)}")
            
            print("   ✅ Instagram home extraction complete")
            return True
            
        except Exception as e:
            print(f"   ❌ Instagram home extraction failed: {str(e)[:100]}...")
            return False

    def extract_target_profile(self):
        """Extract session data from target profile"""
        print(f"👤 EXTRACTING TARGET PROFILE SESSION DATA ({self.target_username})...")
        
        try:
            # Add existing cookies to headers if available
            if self.extracted_data['session_cookies']:
                cookie_string = '; '.join([f"{k}={v}" for k, v in self.extracted_data['session_cookies'].items()])
                self.session.headers['Cookie'] = cookie_string
                
                if 'csrftoken' in self.extracted_data['session_cookies']:
                    self.session.headers['X-CSRFToken'] = self.extracted_data['session_cookies']['csrftoken']
            
            response = self.session.get(self.target_url, timeout=30)
            
            # Extract user data from profile page
            user_id_match = re.search(r'"id":"(\d+)"', response.text)
            if user_id_match:
                self.extracted_data['user_data']['target_user_id'] = user_id_match.group(1)
                print(f"   👤 Target User ID: {user_id_match.group(1)}")
            
            # Extract profile data
            username_match = re.search(r'"username":"([^"]+)"', response.text)
            if username_match:
                self.extracted_data['user_data']['confirmed_username'] = username_match.group(1)
                print(f"   ✅ Confirmed Username: {username_match.group(1)}")
            
            # Check if profile is private
            private_match = re.search(r'"is_private":(true|false)', response.text)
            if private_match:
                self.extracted_data['user_data']['is_private'] = private_match.group(1) == 'true'
                print(f"   🔒 Profile Private: {private_match.group(1)}")
            
            # Extract follower count
            follower_match = re.search(r'"edge_followed_by":{"count":(\d+)}', response.text)
            if follower_match:
                self.extracted_data['user_data']['followers'] = int(follower_match.group(1))
                print(f"   👥 Followers: {follower_match.group(1)}")
            
            print("   ✅ Target profile extraction complete")
            return True
            
        except Exception as e:
            print(f"   ❌ Target profile extraction failed: {str(e)[:100]}...")
            return False

    def attempt_api_authentication(self):
        """Attempt to access authenticated API endpoints"""
        print("🔑 ATTEMPTING API AUTHENTICATION...")
        
        if not self.extracted_data['session_cookies']:
            print("   ❌ No session cookies available for authentication")
            return False
        
        try:
            # Prepare authenticated headers
            auth_headers = self.headers.copy()
            cookie_string = '; '.join([f"{k}={v}" for k, v in self.extracted_data['session_cookies'].items()])
            auth_headers['Cookie'] = cookie_string
            
            if 'csrftoken' in self.extracted_data['session_cookies']:
                auth_headers['X-CSRFToken'] = self.extracted_data['session_cookies']['csrftoken']
                auth_headers['X-Instagram-AJAX'] = '1'
                auth_headers['X-Requested-With'] = 'XMLHttpRequest'
            
            # Test authenticated endpoints
            auth_endpoints = [
                'https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/',
                'https://www.instagram.com/api/v1/users/self/',
                'https://www.instagram.com/accounts/edit/',
                'https://www.instagram.com/api/v1/direct_v2/inbox/'
            ]
            
            for endpoint in auth_endpoints:
                try:
                    response = self.session.get(endpoint, headers=auth_headers, timeout=15)
                    
                    if response.status_code == 200:
                        print(f"   ✅ Authenticated access to: {endpoint}")
                        self.extracted_data['authentication_status'] = 'authenticated'
                        
                        # Try to extract user ID from authenticated response
                        if 'user' in response.text and 'id' in response.text:
                            user_match = re.search(r'"id":"?(\d+)"?', response.text)
                            if user_match:
                                self.extracted_data['user_data']['authenticated_user_id'] = user_match.group(1)
                                print(f"   👤 Authenticated User ID: {user_match.group(1)}")
                        
                        return True
                        
                    elif response.status_code == 401:
                        print(f"   🔒 Unauthorized access to: {endpoint}")
                        
                    else:
                        print(f"   ⚠️  Status {response.status_code} for: {endpoint}")
                        
                except Exception as e:
                    print(f"   ❌ Auth endpoint failed {endpoint}: {str(e)[:50]}...")
            
            self.extracted_data['authentication_status'] = 'unauthenticated'
            print("   ❌ No authenticated access achieved")
            return False
            
        except Exception as e:
            print(f"   ❌ API authentication failed: {str(e)[:100]}...")
            return False

    def generate_session_summary(self):
        """Generate a summary of extracted session data"""
        print("📊 GENERATING SESSION SUMMARY...")
        
        summary = {
            'session_identifiers_found': [],
            'authentication_tokens_found': [],
            'access_level': 'none',
            'target_accessibility': 'unknown',
            'extraction_success': False
        }
        
        # Check for session identifiers
        session_cookies = ['sessionid', 'ds_user_id', 'shbid', 'shbts']
        for cookie in session_cookies:
            if cookie in self.extracted_data['session_cookies']:
                summary['session_identifiers_found'].append({
                    'type': 'cookie',
                    'name': cookie,
                    'value': self.extracted_data['session_cookies'][cookie],
                    'length': len(self.extracted_data['session_cookies'][cookie])
                })
        
        # Check for authentication tokens
        auth_tokens = ['csrf_token', 'csrftoken']
        for token in auth_tokens:
            if token in self.extracted_data['csrf_tokens']:
                summary['authentication_tokens_found'].append({
                    'type': 'csrf',
                    'name': token,
                    'value': self.extracted_data['csrf_tokens'][token],
                    'length': len(self.extracted_data['csrf_tokens'][token])
                })
            elif token in self.extracted_data['session_cookies']:
                summary['authentication_tokens_found'].append({
                    'type': 'cookie',
                    'name': token,
                    'value': self.extracted_data['session_cookies'][token],
                    'length': len(self.extracted_data['session_cookies'][token])
                })
        
        # Determine access level
        if self.extracted_data['authentication_status'] == 'authenticated':
            summary['access_level'] = 'authenticated'
        elif self.extracted_data['session_cookies']:
            summary['access_level'] = 'session_available'
        else:
            summary['access_level'] = 'none'
        
        # Determine target accessibility
        if self.extracted_data['user_data'].get('is_private'):
            summary['target_accessibility'] = 'private'
        elif 'target_user_id' in self.extracted_data['user_data']:
            summary['target_accessibility'] = 'public'
        
        # Overall success
        summary['extraction_success'] = bool(summary['session_identifiers_found'] or summary['authentication_tokens_found'])
        
        self.extracted_data['session_summary'] = summary
        
        # Print summary
        print(f"   📊 Session Identifiers Found: {len(summary['session_identifiers_found'])}")
        print(f"   🔑 Authentication Tokens Found: {len(summary['authentication_tokens_found'])}")
        print(f"   🎯 Access Level: {summary['access_level']}")
        print(f"   🔒 Target Accessibility: {summary['target_accessibility']}")
        print(f"   ✅ Extraction Success: {summary['extraction_success']}")
        
        # Print detailed findings
        for session_id in summary['session_identifiers_found']:
            print(f"   🆔 SESSION: {session_id['name']} = {session_id['value'][:50]}...")
        
        for auth_token in summary['authentication_tokens_found']:
            print(f"   🔐 TOKEN: {auth_token['name']} = {auth_token['value'][:50]}...")

    def extract_all_session_data(self):
        """Main extraction function"""
        print("=" * 80)
        print("🔐 INSTAGRAM SESSION ID EXTRACTOR")
        print(f"🎯 TARGET: {self.target_username}")
        print("🔐 EXTRACTING SESSION IDENTIFIERS")
        print("=" * 80)
        
        # Extract data step by step
        success_home = self.extract_instagram_home()
        time.sleep(2)
        
        success_profile = self.extract_target_profile()
        time.sleep(2)
        
        success_auth = self.attempt_api_authentication()
        time.sleep(1)
        
        self.generate_session_summary()
        
        # Save results
        timestamp = int(time.time())
        filename = f"INSTAGRAM_SESSION_EXTRACTION_{self.target_username}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.extracted_data, f, indent=2)
        
        print("=" * 80)
        print("🔐 SESSION EXTRACTION COMPLETE!")
        print(f"📊 Results saved: {filename}")
        print("🔐 SESSION DATA READY FOR ANALYSIS!")
        print("=" * 80)
        
        return self.extracted_data

@safe_execution
def main():
    extractor = InstagramSessionExtractor()
    return extractor.extract_all_session_data()

if __name__ == "__main__":
    main()
