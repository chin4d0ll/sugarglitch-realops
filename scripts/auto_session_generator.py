# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Instagram Session Generator - Automatic Fresh Session Creation
"""

import requests
import json
import time
import random
import uuid
from datetime import datetime
import hashlib

class InstagramSessionGenerator:
    def __init__(self):
        self.base_url = "https://i.instagram.com/api/v1"
        self.session = requests.Session()
        self.device_id = str(uuid.uuid4())
        self.advertising_id = str(uuid.uuid4())

    def generate_device_info(self):
        """Generate realistic device information"""
        devices = [
            {
                "model": "SM-G973F",
                "brand": "samsung",
                "device": "beyond1",
                "cpu": "exynos9820",
                "resolution": "1440x3040",
                "dpi": 550
            },
            {
                "model": "iPhone12,1",
                "brand": "iPhone",
                "device": "iPhone12,1",
                "cpu": "arm64",
                "resolution": "828x1792",
                "dpi": 326
            },
            {
                "model": "Pixel 5",
                "brand": "google",
                "device": "redfin",
                "cpu": "sm7250",
                "resolution": "1080x2340",
                "dpi": 432
            }
        ]

        device = random.choice(devices)

        return {
            "device_id": self.device_id,
            "advertising_id": self.advertising_id,
            "model": device["model"],
            "brand": device["brand"],
            "device": device["device"],
            "cpu": device["cpu"],
            "resolution": device["resolution"],
            "dpi": device["dpi"]
        }

    def setup_session_headers(self, device_info):
        """Setup session with Instagram mobile headers"""
        app_version = "264.0.0.22.109"
        version_code = "427570327"

        user_agent = f"Instagram {app_version} Android (30/11; {device_info['dpi']}dpi; {device_info['resolution']}; {device_info['brand']}; {device_info['model']}; {device_info['device']}; {device_info['cpu']}; en_US; {version_code})"

        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'X-IG-Capabilities': '3brTv10=',
            'X-IG-App-ID': '567067343352427',
            'X-IG-Device-ID': device_info['device_id'],
            'X-IG-Android-ID': device_info['advertising_id'],
            'Content-Type': 'application/x-www-form-urlencoded; charset = UTF-8',
            'Accept': '*/*',
            'Connection': 'Keep-Alive'
        })

    def generate_signed_request(self, data):
        """Generate signed request for Instagram API"""
        # Instagram's signature key (public knowledge)
        key = "c7b3324247ae4d3e922e6b65b2d4ce0b"

        json_data = json.dumps(data, separators=(',', ':'))
        signature = hashlib.hmac.new(
            key.encode('utf-8'),
            json_data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return f"ig_sig_key_version = 4&signed_body={signature}.{json_data}"

    def create_fresh_session_automated(self):
        """Create a fresh session using automated methods"""
        print("🤖 Creating fresh Instagram session automatically...")

        device_info = self.generate_device_info()
        self.setup_session_headers(device_info)

        # Method 1: Try session regeneration from existing data
        session_data = self.try_session_regeneration()
        if session_data:
            return session_data

        # Method 2: Try guest session creation
        session_data = self.try_guest_session()
        if session_data:
            return session_data

        # Method 3: Try session restoration
        session_data = self.try_session_restoration()
        if session_data:
            return session_data

        return None

    def try_session_regeneration(self):
        """Try to regenerate session from existing session data"""
        print("🔄 Method 1: Session Regeneration...")

        try:
            # Load existing session data
            session_files = [
                "hijacked_sessions/fresh_hijacked_session_1749169370.json",
                "tools/session_alx_trading.json"
            ]

            for file_path in session_files:
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)

                    # Extract useful data
                    old_sessionid = None
                    if isinstance(data, dict):
                        old_sessionid = data.get('sessionid')
                    elif isinstance(data, str):
                        old_sessionid = data

                    if old_sessionid and len(old_sessionid) > 20:
                        # Try to refresh the session
                        refreshed = self.refresh_session(old_sessionid)
                        if refreshed:
                            return refreshed

                except Exception:
                    continue

        except Exception as e:
            print(f"❌ Session regeneration failed: {e}")

        return None

    def refresh_session(self, old_sessionid):
        """Try to refresh an existing session"""
        try:
            self.session.cookies.set('sessionid', old_sessionid, domain='.instagram.com')

            # Try to refresh
            refresh_url = f"{self.base_url}/accounts/current_user/"
            response = self.session.get(refresh_url, timeout = 10)

            if response.status_code == 200:
                # Extract new session if available
                new_cookies = self.session.cookies
                for cookie in new_cookies:
                    if cookie.name == 'sessionid' and cookie.value != old_sessionid:
                        print("✅ Session refreshed successfully!")
                        return {
                            "sessionid": cookie.value,
                            "method": "refresh",
                            "timestamp": datetime.now().isoformat()
                        }

        except Exception as e:
            print(f"Session refresh failed: {e}")

        return None

    def try_guest_session(self):
        """Try to create a guest session"""
        print("🔄 Method 2: Guest Session Creation...")

        try:
            # Guest session endpoint
            guest_url = f"{self.base_url}/accounts/get_prefill_candidates/"

            response = self.session.get(guest_url, timeout = 10)

            if response.status_code == 200:
                # Extract session from response cookies
                for cookie in self.session.cookies:
                    if cookie.name == 'sessionid':
                        print("✅ Guest session created!")
                        return {
                            "sessionid": cookie.value,
                            "method": "guest",
                            "timestamp": datetime.now().isoformat()
                        }

        except Exception as e:
            print(f"Guest session creation failed: {e}")

        return None

    def try_session_restoration(self):
        """Try to restore session using cached data"""
        print("🔄 Method 3: Session Restoration...")

        try:
            # Look for cached session data in various locations
            cache_locations = [
                "data/",
                "sessions/",
                "hijacked_sessions/",
                "temp/"
            ]

            for location in cache_locations:
                cache_path = f"{location}instagram_cache.json"
                try:
                    with open(cache_path, 'r') as f:
                        cache_data = json.load(f)

                    if 'sessionid' in cache_data:
                        sessionid = cache_data['sessionid']

                        # Test if still valid
                        if self.test_session(sessionid):
                            print(f"✅ Restored session from cache: {cache_path}")
                            return {
                                "sessionid": sessionid,
                                "method": "restoration",
                                "timestamp": datetime.now().isoformat(),
                                "source": cache_path
                            }

                except Exception:
                    continue

        except Exception as e:
            print(f"Session restoration failed: {e}")

        return None

    def test_session(self, sessionid):
        """Test if a session is valid"""
        try:
            test_session = requests.Session()
            test_session.cookies.set('sessionid', sessionid, domain='.instagram.com')

            test_url = "https://www.instagram.com/api/v1/users/web_profile_info/?username = instagram"
            response = test_session.get(test_url, timeout = 5)

            return response.status_code == 200 and 'data' in response.text

        except Exception:
            return False

    def save_session(self, session_data):
        """Save the generated session"""
        if session_data:
            # Save to multiple locations for redundancy
            locations = [
                "fresh_auto_session.json",
                "data/fresh_session.json",
                "sessions/auto_generated_session.json"
            ]

            for location in locations:
                try:
                    # Create directory if needed
                    import os
                    os.makedirs(os.path.dirname(location), exist_ok = True)

                    with open(location, 'w') as f:
                        json.dump(session_data, f, indent = 2)

                    print(f"💾 Session saved to: {location}")
                except Exception:
                    continue

def main():
    print("🚀 AUTOMATIC Instagram Session Generator")
    print("=" * 50)

    generator = InstagramSessionGenerator()

    # Generate fresh session
    session_data = generator.create_fresh_session_automated()

    if session_data:
        print("\n✅ SUCCESS! Fresh session generated")
        print(f"📱 Session ID: {session_data['sessionid'][:20]}...")
        print(f"🔧 Method: {session_data['method']}")

        # Save session
        generator.save_session(session_data)

        # Test the new session
        print("\n🧪 Testing new session...")
        if generator.test_session(session_data['sessionid']):
            print("✅ New session is valid!")

            # Now run extraction with the fresh session
            print("\n🎯 Running extraction with fresh session...")
            from simple_automated_extractor import SimpleAutomatedExtractor

            extractor = SimpleAutomatedExtractor()
            success = extractor.extract_target_data(session_data['sessionid'])

            if success:
                print("🎉 COMPLETE SUCCESS! DM extraction completed with fresh session!")
            else:
                print("⚠️ Session valid but extraction had issues")

        else:
            print("❌ Generated session is not valid")
    else:
        print("\n❌ Failed to generate fresh session")
        print("💡 All automated methods failed")
        print("🔧 You may need to:")
        print("   1. Use a VPN to change IP address")
        print("   2. Wait for Instagram rate limits to reset")
        print("   3. Manually get session from browser")

if __name__ == "__main__":
    main()
