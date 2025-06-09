# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 Instagram 500 Error Fix Implementation
Comprehensive solution for chin4d0ll based on diagnosis results

This script provides:
1. Working configurations identified from testing
2. Retry logic with fallback strategies
3. Rate limit handling
4. Session management
"""

import requests
import json
import time
import random
from pathlib import Path
from typing import Dict, Any, Optional, List

class Instagram500Fixer:
    """💖 Complete Instagram 500 error solution"""

    def __init__(self, session_file: str = "sessions/session-alx.trading"):
        self.session_file = Path(session_file)
        self.session = requests.Session()
        self.cookies = {}
        self._load_session()

        # 🏆 Proven working configurations (from testing)
        self.working_configs = [
            {
                'name': 'Mobile iPhone (Primary)',
                'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
                'headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                }
            },
            {
                'name': 'Desktop Chrome (Fallback)',
                'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                }
            }
        ]

        self.current_config_index = 0
        self.retry_count = 0
        self.max_retries = 3

    def _load_session(self):
        """🔑 Load session cookies"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                    self.cookies = data.get('cookies', {})
                    print(f"✅ Loaded session with {len(self.cookies)} cookies")
            else:
                print(f"⚠️  No session file found: {self.session_file}")
        except Exception as e:
            print(f"💥 Session load error: {e}")

    def get_headers(self, config_index: int = 0) -> Dict[str, str]:
        """🛡️ Get headers for current configuration"""
        config = self.working_configs[config_index]
        headers = config['headers'].copy()
        headers['User-Agent'] = config['ua']

        # Add cookies if available
        if self.cookies:
            cookie_string = '; '.join([f"{k}={v}" for k, v in self.cookies.items()])
            headers['Cookie'] = cookie_string

        return headers

    def safe_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """🛡️ Make a safe request with automatic retry and fallback"""

        for attempt in range(self.max_retries):
            # Try current configuration
            for config_index in range(len(self.working_configs)):
                try:
                    headers = self.get_headers(config_index)
                    config_name = self.working_configs[config_index]['name']

                    print(f"🌟 Attempt {attempt + 1} with {config_name}")

                    # Add random delay to avoid rate limiting
                    if attempt > 0:
                        delay = random.uniform(2, 5)
                        print(f"⏰ Waiting {delay:.1f}s...")
                        time.sleep(delay)

                    response = self.session.request(
                        method=method,
                        url=url,
                        headers=headers,
                        timeout=30,
                        allow_redirects=True,
                        verify=False,
                        **kwargs
                    )

                    # Check response status
                    if response.status_code == 200:
                        print(f"✅ Success with {config_name}")
                        return response

                    elif response.status_code == 429:
                        print(f"⚠️  Rate limited (429) - waiting longer...")
                        time.sleep(random.uniform(10, 20))
                        continue

                    elif response.status_code == 500:
                        print(f"💥 Server error (500) with {config_name}")
                        continue

                    elif response.status_code in [302, 301]:
                        print(f"🔄 Redirect ({response.status_code}) - following...")
                        return response

                    else:
                        print(f"❌ HTTP {response.status_code} with {config_name}")
                        continue

                except requests.exceptions.Timeout:
                    print(f"⏰ Timeout with {config_name}")
                    continue

                except requests.exceptions.ConnectionError:
                    print(f"🔌 Connection error with {config_name}")
                    continue

                except Exception as e:
                    print(f"💥 Error with {config_name}: {e}")
                    continue

            # If all configs failed, wait before next attempt
            if attempt < self.max_retries - 1:
                wait_time = random.uniform(5, 15)
                print(f"😴 All configs failed, waiting {wait_time:.1f}s before retry...")
                time.sleep(wait_time)

        print(f"💔 All attempts failed for: {url}")
        return None

    def test_profile_access(self, username: str) -> Dict[str, Any]:
        """🧪 Test access to a specific profile"""
        url = f"https://www.instagram.com/{username}/"

        print(f"🎯 Testing profile access: {username}")
        response = self.safe_request(url)

        if response:
            return {
                'success': True,
                'status_code': response.status_code,
                'content_length': len(response.text),
                'url': url,
                'has_content': 'instagram' in response.text.lower()
            }
        else:
            return {
                'success': False,
                'url': url,
                'error': 'All retry attempts failed'
            }

    def extract_user_data(self, username: str) -> Optional[Dict[str, Any]]:
        """🎯 Extract user data with 500 error protection"""

        print(f"🌸 Extracting data for: {username}")

        # Test basic access first
        test_result = self.test_profile_access(username)
        if not test_result['success']:
            print(f"💔 Cannot access profile: {username}")
            return None

        print(f"✅ Profile accessible, extracting data...")

        # Your existing extraction logic goes here
        # This is just a framework - replace with actual extraction
        response = self.safe_request(f"https://www.instagram.com/{username}/")

        if response:
            # Parse response.text for actual data
            # This is where you'd add your existing parsing logic
            return {
                'username': username,
                'extracted_at': time.time(),
                'status': 'success',
                'data_size': len(response.text),
                'raw_content': response.text[:1000] + "..." if len(response.text) > 1000 else response.text
            }

        return None

def quick_test():
    """🚀 Quick test of the fixer"""
    fixer = Instagram500Fixer()

    # Test with chin4d0ll
    result = fixer.test_profile_access('chin4d0ll')
    print(f"\n🌟 Test Results:")
    print(json.dumps(result, indent=2))

    if result['success']:
        print(f"\n✅ SUCCESS: Instagram access is working!")
        print(f"✨ You can now use this fixer in your main extraction scripts")
    else:
        print(f"\n❌ FAILED: Still having issues")

if __name__ == "__main__":
    quick_test()
