# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🌸✨ Quick Demo Fixed - Cute Instagram Session Tester ✨🌸
Quick validation and demo for Instagram session functionality
"""

import requests
import json
import os
from pathlib import Path
from datetime import datetime

class CuteQuickDemo:
    """Adorable quick demo for session testing"""

    def __init__(self):
        self.session = requests.Session()
        self.setup_headers()
        print("🌸✨ Quick Demo Fixed initialized! ✨🌸")

    def setup_headers(self):
        """Setup mobile-friendly headers"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def find_session_files(self):
        """Find available session files"""
        print("🔍 Looking for session files...")

        session_paths = [
            "../sessions/session-alx.trading",
            "sessions/session-alx.trading",
            "../sessions_fresh/session-alx.trading",
            "sessions_fresh/session-alx.trading",
            "../hijacked_sessions/session-alx.trading",
            "hijacked_sessions/session-alx.trading"
        ]

        found_sessions = []
        for path in session_paths:
            if Path(path).exists():
                found_sessions.append(path)
                print(f"✅ Found: {path}")

        return found_sessions

    def load_session(self, session_file):
        """Load session from file"""
        try:
            print(f"📂 Loading session from: {session_file}")

            with open(session_file, 'r') as f:
                session_data = json.load(f)

            # Load cookies into session
            for cookie_name, cookie_value in session_data.items():
                self.session.cookies.set(cookie_name, cookie_value)

            print(f"💖 Loaded {len(session_data)} cookies")
            return True

        except Exception as e:
            print(f"💔 Error loading session: {e}")
            return False

    def test_instagram_access(self):
        """Test basic Instagram access"""
        print("🧪 Testing Instagram access...")

        try:
            # Test basic Instagram page
            response = self.session.get("https://www.instagram.com/")

            if response.status_code == 200:
                print("✅ Instagram homepage accessible")

                # Check if we're logged in
                if '"is_logged_in":true' in response.text:
                    print("🎉 Session is active and logged in!")
                    return "logged_in"
                else:
                    print("⚠️ Can access Instagram but not logged in")
                    return "not_logged_in"
            else:
                print(f"❌ Instagram access failed: {response.status_code}")
                return "failed"

        except Exception as e:
            print(f"💔 Instagram access error: {e}")
            return "error"

    def test_api_endpoint(self):
        """Test Instagram API endpoint"""
        print("🧪 Testing API endpoint...")

        try:
            # Test with a public user
            url = "https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram"
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    user_info = data['data']['user']
                    print(f"✅ API working! Got info for: {user_info.get('username')}")
                    print(f"   Followers: {user_info.get('edge_followed_by', {}).get('count', 'Unknown')}")
                    return True
                else:
                    print("⚠️ API responded but data format unexpected")
                    return False
            else:
                print(f"❌ API endpoint failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"💔 API test error: {e}")
            return False

    def test_specific_user(self, username="alx.trading"):
        """Test access to specific user"""
        print(f"🧪 Testing access to {username}...")

        try:
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    user_info = data['data']['user']
                    print(f"✅ Can access {username}!")
                    print(f"   User ID: {user_info.get('id')}")
                    print(f"   Full Name: {user_info.get('full_name')}")
                    print(f"   Is Private: {user_info.get('is_private')}")
                    print(f"   Followers: {user_info.get('edge_followed_by', {}).get('count', 'Unknown')}")

                    return {
                        'success': True,
                        'user_id': user_info.get('id'),
                        'is_private': user_info.get('is_private'),
                        'user_info': user_info
                    }
                else:
                    print(f"⚠️ Unexpected response format for {username}")
                    return {'success': False, 'reason': 'unexpected_format'}
            else:
                print(f"❌ Failed to access {username}: {response.status_code}")
                return {'success': False, 'reason': f'http_{response.status_code}'}

        except Exception as e:
            print(f"💔 Error testing {username}: {e}")
            return {'success': False, 'reason': str(e)}

    def run_quick_demo(self):
        """Run complete quick demo"""
        print("🌸✨ Starting Quick Demo! ✨🌸")

        results = {
            'timestamp': datetime.now().isoformat(),
            'session_files': [],
            'instagram_access': 'unknown',
            'api_test': False,
            'target_user_test': {},
            'recommendations': []
        }

        # Find session files
        session_files = self.find_session_files()
        results['session_files'] = session_files

        if not session_files:
            print("💔 No session files found!")
            results['recommendations'].append("Create session files in sessions/ directory")
            return results

        # Try each session file
        for session_file in session_files:
            print(f"\n🧪 Testing with session: {session_file}")

            if self.load_session(session_file):
                # Test Instagram access
                access_result = self.test_instagram_access()
                results['instagram_access'] = access_result

                if access_result in ['logged_in', 'not_logged_in']:
                    # Test API endpoint
                    api_result = self.test_api_endpoint()
                    results['api_test'] = api_result

                    if api_result:
                        # Test specific user
                        user_result = self.test_specific_user()
                        results['target_user_test'] = user_result

                        if user_result.get('success'):
                            print("🎉 All tests passed! Session is working!")
                            break
                        else:
                            print(f"⚠️ Target user test failed: {user_result.get('reason')}")
                    else:
                        print("⚠️ API test failed")
                else:
                    print("⚠️ Instagram access test failed")

            print("➡️ Trying next session file...\n")

        # Generate recommendations
        if results['instagram_access'] != 'logged_in':
            results['recommendations'].append("Session may be expired - try logging in again")

        if not results['api_test']:
            results['recommendations'].append("API access limited - check rate limits or session validity")

        if not results['target_user_test'].get('success'):
            results['recommendations'].append("Cannot access target user - check if account is private or blocked")

        # Save results
        timestamp = int(datetime.now().timestamp())
        results_file = f"quick_demo_results_{timestamp}.json"

        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n💾 Results saved to: {results_file}")

        return results

def main():
    """Main function"""
    demo = CuteQuickDemo()
    results = demo.run_quick_demo()

    print(f"\n🌸✨ Quick Demo Summary ✨🌸")
    print(f"Session Files Found: {len(results['session_files'])}")
    print(f"Instagram Access: {results['instagram_access']}")
    print(f"API Test: {'✅' if results['api_test'] else '❌'}")
    print(f"Target User Access: {'✅' if results['target_user_test'].get('success') else '❌'}")

    if results['recommendations']:
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"   {i}. {rec}")

if __name__ == "__main__":
    main()
