# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔑 Instagram Session Validator & Fixer
ตรวจสอบและแก้ไข session สำหรับ chin4d0ll
"""

import requests
import json
import re
import time
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

class InstagramSessionFixer:
    """🔧 แก้ไข Instagram session issues"""

    def __init__(self, session_file: str = "sessions/session-alx.trading"):
        self.session_file = Path(session_file)
        self.session_data = {}
        self.cookies = {}
        self._load_session()

        # 📱 Working headers (confirmed from previous test)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }

    def _load_session(self):
        """🔑 Load current session"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    self.session_data = json.load(f)
                    self.cookies = self.session_data.get('cookies', {})
                print(f"✅ Session loaded: {len(self.cookies)} cookies")

                # Show what we have
                cookie_names = list(self.cookies.keys())
                print(f"📝 Cookies: {cookie_names}")
            else:
                print(f"❌ Session file not found: {self.session_file}")
        except Exception as e:
            print(f"💥 Session load error: {e}")

    def validate_current_session(self) -> Tuple[bool, Dict[str, Any]]:
        """🔍 Validate if current session is still working"""
        print("🔍 Validating current session...")

        if not self.cookies:
            return False, {'error': 'No cookies found'}

        if 'sessionid' not in self.cookies:
            return False, {'error': 'No sessionid cookie'}

        # Test session by accessing Instagram
        headers = self.headers.copy()
        if self.cookies:
            cookie_string = '; '.join([f"{k}={v}" for k, v in self.cookies.items()])
            headers['Cookie'] = cookie_string

        try:
            response = requests.get(
                'https://www.instagram.com/',
                headers=headers,
                timeout=30,
                allow_redirects=True
            )

            result = {
                'status_code': response.status_code,
                'final_url': response.url,
                'redirected': response.url != 'https://www.instagram.com/',
                'content_length': len(response.text)
            }

            # Check if we're logged in
            content_lower = response.text.lower()

            # Look for login indicators
            login_indicators = ['login', 'log in', 'sign in', 'signin']
            logout_indicators = ['logout', 'log out', 'sign out']
            dm_indicators = ['direct', 'inbox', 'messages']
            profile_indicators = ['profile', 'settings', 'edit profile']

            result['has_login_form'] = any(indicator in content_lower for indicator in login_indicators)
            result['has_logout_option'] = any(indicator in content_lower for indicator in logout_indicators)
            result['has_dm_access'] = any(indicator in content_lower for indicator in dm_indicators)
            result['has_profile_access'] = any(indicator in content_lower for indicator in profile_indicators)

            # Determine login status
            if result['has_logout_option'] or result['has_dm_access'] or result['has_profile_access']:
                result['logged_in'] = True
                print("✅ Session is valid - user is logged in!")
            elif result['has_login_form'] or 'login' in result['final_url'].lower():
                result['logged_in'] = False
                print("❌ Session expired - redirected to login")
            else:
                result['logged_in'] = None
                print("⚠️ Login status unclear")

            # Extract additional session info from response
            result.update(self._extract_session_info_from_html(response.text))

            return result['logged_in'] == True, result

        except Exception as e:
            return False, {'error': str(e)}

    def _extract_session_info_from_html(self, html: str) -> Dict[str, Any]:
        """🔍 Extract session information from Instagram HTML"""
        info = {}

        try:
            # Look for Instagram's window._sharedData
            shared_data_pattern = r'window\._sharedData\s*=\s*({.*?});'
            match = re.search(shared_data_pattern, html)

            if match:
                try:
                    shared_data = json.loads(match.group(1))
                    info['has_shared_data'] = True

                    # Extract useful info
                    config = shared_data.get('config', {})
                    info['csrf_token'] = config.get('csrf_token')
                    info['viewer_id'] = config.get('viewer_id')
                    info['is_logged_in'] = config.get('is_logged_in', False)

                except json.JSONDecodeError:
                    info['has_shared_data'] = False

            # Look for rollout hash
            rollout_pattern = r'"rollout_hash":"([^"]+)"'
            match = re.search(rollout_pattern, html)
            if match:
                info['rollout_hash'] = match.group(1)

            # Look for app ID
            app_id_pattern = r'"app_id":"([^"]+)"'
            match = re.search(app_id_pattern, html)
            if match:
                info['app_id'] = match.group(1)

        except Exception as e:
            info['extraction_error'] = str(e)

        return info

    def extract_fresh_cookies_from_homepage(self) -> Dict[str, str]:
        """🆕 Extract fresh cookies from Instagram homepage"""
        print("🆕 Extracting fresh cookies from Instagram...")

        # Make a fresh request without any cookies
        headers = self.headers.copy()

        try:
            response = requests.get(
                'https://www.instagram.com/',
                headers=headers,
                timeout=30,
                allow_redirects=True
            )

            # Extract cookies from response
            fresh_cookies = {}

            # Get cookies from Set-Cookie headers
            for cookie in response.cookies:
                fresh_cookies[cookie.name] = cookie.value

            # Extract CSRF token from HTML
            csrf_token = None
            shared_data_pattern = r'window\._sharedData\s*=\s*({.*?});'
            match = re.search(shared_data_pattern, response.text)

            if match:
                try:
                    shared_data = json.loads(match.group(1))
                    csrf_token = shared_data.get('config', {}).get('csrf_token')
                    if csrf_token:
                        fresh_cookies['csrftoken'] = csrf_token
                except Exception:
                    pass

            # Extract from meta tags
            csrf_meta_pattern = r'<meta name="csrf-token" content="([^"]+)"'
            match = re.search(csrf_meta_pattern, response.text)
            if match:
                fresh_cookies['csrftoken'] = match.group(1)

            print(f"🆕 Extracted {len(fresh_cookies)} fresh cookies: {list(fresh_cookies.keys())}")

            return fresh_cookies

        except Exception as e:
            print(f"💥 Failed to extract fresh cookies: {e}")
            return {}

    def merge_session_cookies(self, fresh_cookies: Dict[str, str]) -> Dict[str, str]:
        """🔄 Merge fresh cookies with existing session"""
        print("🔄 Merging cookies...")

        # Start with existing cookies
        merged_cookies = self.cookies.copy()

        # Add fresh cookies (they will override existing ones)
        merged_cookies.update(fresh_cookies)

        # Ensure we keep the important sessionid if we have it
        if 'sessionid' in self.cookies and 'sessionid' not in fresh_cookies:
            merged_cookies['sessionid'] = self.cookies['sessionid']
            print("🔑 Kept existing sessionid")

        print(f"🔄 Merged cookies: {list(merged_cookies.keys())}")

        return merged_cookies

    def test_merged_session(self, merged_cookies: Dict[str, str]) -> Tuple[bool, Dict[str, Any]]:
        """🧪 Test merged session"""
        print("🧪 Testing merged session...")

        headers = self.headers.copy()
        cookie_string = '; '.join([f"{k}={v}" for k, v in merged_cookies.items()])
        headers['Cookie'] = cookie_string

        # Add CSRF token to headers if available
        if 'csrftoken' in merged_cookies:
            headers['X-CSRFToken'] = merged_cookies['csrftoken']

        try:
            # Test regular homepage
            response = requests.get(
                'https://www.instagram.com/',
                headers=headers,
                timeout=30,
                allow_redirects=True
            )

            result = {
                'homepage_status': response.status_code,
                'homepage_url': response.url,
                'homepage_redirected': response.url != 'https://www.instagram.com/'
            }

            # Check login status
            content_lower = response.text.lower()
            result['logged_in'] = 'logout' in content_lower or 'direct' in content_lower

            if result['logged_in']:
                print("✅ Merged session works - user appears logged in!")

                # Test direct messages access
                dm_response = requests.get(
                    'https://www.instagram.com/direct/inbox/',
                    headers=headers,
                    timeout=30,
                    allow_redirects=True
                )

                result['dm_status'] = dm_response.status_code
                result['dm_url'] = dm_response.url
                result['dm_accessible'] = dm_response.status_code == 200 and 'login' not in dm_response.url.lower()

                if result['dm_accessible']:
                    print("🎉 Direct messages accessible!")
                else:
                    print("⚠️ Direct messages not accessible")
            else:
                print("❌ Merged session still not logged in")

            return result['logged_in'], result

        except Exception as e:
            return False, {'error': str(e)}

    def save_fixed_session(self, fixed_cookies: Dict[str, str]) -> None:
        """💾 Save fixed session"""
        print("💾 Saving fixed session...")

        # Create backup of original session
        if self.session_file.exists():
            backup_file = self.session_file.with_suffix('.backup')
            import shutil
            shutil.copy2(self.session_file, backup_file)
            print(f"📋 Backup saved: {backup_file}")

        # Update session data
        updated_session = self.session_data.copy()
        updated_session['cookies'] = fixed_cookies
        updated_session['last_updated'] = int(time.time())
        updated_session['status'] = 'fixed'

        # Save updated session
        with open(self.session_file, 'w') as f:
            json.dump(updated_session, f, indent=2)

        print(f"✅ Fixed session saved: {self.session_file}")

    def run_session_fix(self) -> bool:
        """🚀 Run complete session fix process"""
        print("🌸 Instagram Session Fixer")
        print("💖 Fixing session for chin4d0ll")
        print("=" * 40)

        # Step 1: Validate current session
        is_valid, validation_result = self.validate_current_session()

        if is_valid:
            print("🎉 Current session is already working!")
            return True

        print(f"❌ Current session invalid: {validation_result.get('error', 'Session expired')}")

        # Step 2: Extract fresh cookies
        fresh_cookies = self.extract_fresh_cookies_from_homepage()

        if not fresh_cookies:
            print("💥 Failed to extract fresh cookies")
            return False

        # Step 3: Merge cookies
        merged_cookies = self.merge_session_cookies(fresh_cookies)

        # Step 4: Test merged session
        works, test_result = self.test_merged_session(merged_cookies)

        if works:
            print("🎉 Session fix successful!")

            # Step 5: Save fixed session
            self.save_fixed_session(merged_cookies)

            # Print summary
            print(f"\n📊 FIXED SESSION SUMMARY:")
            print(f"  Homepage: {'✅' if test_result.get('homepage_status') == 200 else '❌'}")
            print(f"  Logged in: {'✅' if test_result.get('logged_in') else '❌'}")
            print(f"  DM access: {'✅' if test_result.get('dm_accessible') else '❌'}")

            return True
        else:
            print("💥 Session fix failed")
            print("💡 You may need to manually get a fresh session from browser")
            return False

def main():
    """🚀 Main function"""
    print("🔑 Instagram Session Validator & Fixer")
    print("💖 Made with love for chin4d0ll")
    print("🎯 Educational purposes only")
    print()

    try:
        fixer = InstagramSessionFixer()
        success = fixer.run_session_fix()

        if success:
            print("\n🌟 Session fix complete!")
            print("✨ You can now run your DM extractor!")
        else:
            print("\n😢 Session fix failed")
            print("💡 Manual session refresh may be needed")

    except KeyboardInterrupt:
        print("\n🛑 Session fix interrupted")
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
