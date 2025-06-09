# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Browser Session Hijacker
Captures fresh Instagram session from running browser process
"""

import os
import json
import sys
import time
import requests
import subprocess
import re
from datetime import datetime

class BrowserSessionHijacker:
    def __init__(self):
        self.session_file = "tools/session_alx_trading.json"
        self.backup_dir = "sessions_fresh"
        self.target = "alx.trading"

        # Ensure directories exist
        os.makedirs("tools", exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    def find_browser_processes(self):
        """Find running browser processes"""
        browsers = ['chrome', 'chromium', 'firefox', 'brave']
        running_browsers = []

        try:
            # Get all processes
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)

            for line in result.stdout.split('\n'):
                for browser in browsers:
                    if browser in line.lower() and '--user-data-dir' in line:
                        running_browsers.append(line)

            return running_browsers

        except Exception as e:
            print(f"❌ Error finding browsers: {e}")
            return []

    def extract_from_browser_cookies(self):
        """Extract cookies from browser cookie files"""
        print("🔍 Searching for browser cookie files...")

        # Common browser cookie locations
        cookie_paths = [
            "~/.config/google-chrome/Default/Cookies",
            "~/.config/chromium/Default/Cookies",
            "~/.mozilla/firefox/*/cookies.sqlite",
            "~/.config/BraveSoftware/Brave-Browser/Default/Cookies"
        ]

        for path in cookie_paths:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                print(f"📁 Found cookie file: {expanded_path}")
                # Note: Direct cookie extraction requires additional libraries
                # This is a placeholder for the concept

        print("ℹ️  Direct cookie extraction requires additional setup")
        return None

    def capture_network_traffic(self):
        """Capture network traffic for Instagram cookies"""
        print("🌐 Network traffic capture method...")
        print("ℹ️  This requires root access and additional tools")
        return None

    def manual_cookie_extraction(self):
        """Guide user through manual cookie extraction"""
        print("\n🍪 MANUAL COOKIE EXTRACTION GUIDE")
        print("="*50)
        print("1. Open Instagram in your browser and log in")
        print("2. Press F12 to open Developer Tools")
        print("3. Go to Application/Storage > Cookies > https://www.instagram.com")
        print("4. Right-click on the cookies table > 'Copy all as JSON'")
        print("5. Or manually copy these important cookies:")
        print("   - sessionid (REQUIRED)")
        print("   - csrftoken")
        print("   - ds_user_id")
        print("   - mid")
        print()

        method = input("Choose method:\n1. Paste JSON\n2. Enter manually\nChoice (1/2): ").strip()

        if method == "1":
            return self.parse_json_cookies()
        else:
            return self.manual_cookie_input()

    def parse_json_cookies(self):
        """Parse JSON cookies from browser"""
        print("\n📋 Paste the JSON cookies here (press Enter twice when done):")

        lines = []
        while True:
            line = input()
            if line == "" and lines:
                break
            lines.append(line)

        cookie_text = "\n".join(lines)

        try:
            # Try to parse as JSON array
            cookies_data = json.loads(cookie_text)

            session_data = {}
            for cookie in cookies_data:
                if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                    if cookie['name'] in ['sessionid', 'csrftoken', 'ds_user_id', 'mid', 'ig_did', 'shbid', 'rur']:
                        session_data[cookie['name']] = cookie['value']

            if session_data.get('sessionid'):
                print(f"✅ Parsed {len(session_data)} cookies from JSON")
                return session_data
            else:
                print("❌ No sessionid found in JSON")
                return None

        except json.JSONDecodeError:
            print("❌ Invalid JSON format")
            return None

    def manual_cookie_input(self):
        """Manual cookie input"""
        print("\n📝 Enter cookies manually:")

        sessionid = input("sessionid (REQUIRED): ").strip()
        if not sessionid:
            print("❌ sessionid is required!")
            return None

        session_data = {'sessionid': sessionid}

        # Optional cookies
        optional_cookies = ['csrftoken', 'ds_user_id', 'mid', 'ig_did', 'shbid', 'rur']
        for cookie_name in optional_cookies:
            value = input(f"{cookie_name} (optional): ").strip()
            if value:
                session_data[cookie_name] = value

        return session_data

    def validate_session(self, session_data):
        """Validate extracted session"""
        print("🔍 Validating session...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        # Build cookie string
        cookies = []
        for key, value in session_data.items():
            if value:
                cookies.append(f"{key}={value}")

        if cookies:
            headers['Cookie'] = "; ".join(cookies)

        try:
            response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)

            if response.status_code == 200:
                if 'login' not in response.url.lower() and '"is_logged_in":false' not in response.text:
                    print("✅ Session is valid!")
                    return True

            print("❌ Session validation failed")
            return False

        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False

    def save_session(self, session_data):
        """Save session to JSON files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        session_info = {
            'sessionid': session_data.get('sessionid', ''),
            'csrftoken': session_data.get('csrftoken', ''),
            'ds_user_id': session_data.get('ds_user_id', ''),
            'mid': session_data.get('mid', ''),
            'ig_did': session_data.get('ig_did', ''),
            'shbid': session_data.get('shbid', ''),
            'rur': session_data.get('rur', ''),
            'target': self.target,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'extraction_method': 'browser_hijack'
        }

        try:
            # Save main session
            with open(self.session_file, 'w') as f:
                json.dump(session_info, f, indent=2)
            print(f"✅ Session saved to {self.session_file}")

            # Save backup
            backup_file = f"{self.backup_dir}/session_{timestamp}.json"
            with open(backup_file, 'w') as f:
                json.dump(session_info, f, indent=2)
            print(f"✅ Backup saved to {backup_file}")

            return True

        except Exception as e:
            print(f"❌ Save failed: {e}")
            return False

    def run(self):
        """Main execution"""
        print("🕵️ BROWSER SESSION HIJACKER")
        print("="*40)
        print(f"Target: {self.target}")
        print()

        # Check for running browsers
        browsers = self.find_browser_processes()
        if browsers:
            print(f"🌐 Found {len(browsers)} browser processes")

        # Use manual extraction for now
        session_data = self.manual_cookie_extraction()

        if not session_data:
            print("❌ No session data extracted")
            return False

        # Validate session
        if not self.validate_session(session_data):
            print("❌ Session validation failed")
            return False

        # Save session
        if self.save_session(session_data):
            print("\n🎉 SESSION HIJACKING SUCCESSFUL!")
            print(f"✅ Fresh session saved to {self.session_file}")
            return True

        return False

def main():
    try:
        hijacker = BrowserSessionHijacker()
        return hijacker.run()
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
