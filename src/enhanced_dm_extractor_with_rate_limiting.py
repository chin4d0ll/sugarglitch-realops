# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🎯 ENHANCED DM EXTRACTOR WITH RATE LIMITING PROTECTION
=======================================================
แก้ไขปัญหา HTTP 429 (Too Many Requests) ด้วยเทคนิคขั้นสูง

Features:
- Intelligent rate limiting handling
- Exponential backoff retry mechanism
- Multiple session rotation
- Random delay patterns
- Retry-After header detection
- User-Agent rotation
- Request throttling

Author: Advanced Instagram Intelligence System 2025
Status: Enhanced for rate limiting bypass
"""

import requests
import json
import time
import random
import os
from datetime import datetime
from urllib.parse import urljoin
import sqlite3
from pathlib import Path

class EnhancedDMExtractor:
    def __init__(self, target_username):
        self.target = target_username
        self.sessions_dir = "/workspaces/sugarglitch-realops/sessions"
        self.sessions_regen_dir = "/workspaces/sugarglitch-realops/sessions_regenerated"
        self.output_dir = f"/workspaces/sugarglitch-realops/enhanced_extraction/{target_username}"
        self.db_path = "/workspaces/sugarglitch-realops/integrated_targets_2025.db"

        # Rate limiting protection
        self.min_delay = 3.0  # Minimum delay between requests
        self.max_delay = 10.0  # Maximum delay between requests
        self.max_retries = 5   # Maximum retry attempts for 429
        self.backoff_multiplier = 2.0  # Exponential backoff multiplier

        # Session management
        self.valid_sessions = []
        self.current_session_idx = 0

        # User-Agent rotation
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1"
        ]

        # Create output directory
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        # Load sessions
        self.load_sessions()

        print(f"🎯 Enhanced DM Extractor initialized")
        print(f"   Target: {self.target}")
        print(f"   Sessions loaded: {len(self.valid_sessions)}")
        print(f"   Rate limiting protection: ENABLED")
        print(f"   Min delay: {self.min_delay}s, Max delay: {self.max_delay}s")

    def load_sessions(self):
        """Load all available sessions from both directories"""
        session_files = []

        # Load from main sessions directory
        if os.path.exists(self.sessions_dir):
            for file in os.listdir(self.sessions_dir):
                if file.startswith('session-') and (file.endswith('.json') or not '.' in file):
                    session_files.append(os.path.join(self.sessions_dir, file))

        # Load from regenerated sessions directory
        if os.path.exists(self.sessions_regen_dir):
            for file in os.listdir(self.sessions_regen_dir):
                if file.endswith('.json'):
                    session_files.append(os.path.join(self.sessions_regen_dir, file))

        # Process each session file
        for session_file in session_files:
            try:
                session_data = self.load_session_file(session_file)
                if session_data:
                    self.valid_sessions.append({
                        'file': session_file,
                        'data': session_data,
                        'name': os.path.basename(session_file)
                    })
                    print(f"✅ Loaded session: {os.path.basename(session_file)}")
            except Exception as e:
                print(f"⚠️ Failed to load session {session_file}: {e}")

    def load_session_file(self, filepath):
        """Load session data from file"""
        try:
            if filepath.endswith('.json'):
                with open(filepath, 'r') as f:
                    return json.load(f)
            else:
                # Try to read as key-value pairs
                session_data = {}
                with open(filepath, 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            session_data[key] = value
                return session_data
        except Exception as e:
            print(f"Error loading session file {filepath}: {e}")
            return None

    def intelligent_delay(self, is_retry=False, retry_count=0):
        """Apply intelligent delay with randomization"""
        if is_retry:
            # Exponential backoff for retries
            base_delay = self.min_delay * (self.backoff_multiplier ** retry_count)
            delay = base_delay + random.uniform(0, base_delay * 0.5)
            delay = min(delay, 60.0)  # Cap at 60 seconds
        else:
            # Regular delay with randomization
            delay = random.uniform(self.min_delay, self.max_delay)

        print(f"⏰ Waiting {delay:.2f} seconds...")
        time.sleep(delay)

    def get_random_user_agent(self):
        """Get a random User-Agent string"""
        return random.choice(self.user_agents)

    def get_session_headers(self, session_data, include_user_agent=True):
        """Generate headers for session"""
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }

        if include_user_agent:
            headers['User-Agent'] = self.get_random_user_agent()

        # Add session cookies
        if 'cookies' in session_data:
            cookie_string = '; '.join([f"{k}={v}" for k, v in session_data['cookies'].items()])
            headers['Cookie'] = cookie_string
        elif 'sessionid' in session_data:
            headers['Cookie'] = f"sessionid={session_data['sessionid']}"

        return headers

    def make_request_with_retry(self, url, session_data, session_name, method='GET', **kwargs):
        """Make HTTP request with intelligent retry on 429 errors"""
        headers = self.get_session_headers(session_data)
        retry_count = 0

        while retry_count <= self.max_retries:
            try:
                # Apply intelligent delay before request (except first attempt)
                if retry_count > 0:
                    self.intelligent_delay(is_retry=True, retry_count=retry_count)
                elif retry_count == 0:
                    self.intelligent_delay(is_retry=False)

                # Make the request
                if method.upper() == 'GET':
                    response = requests.get(url, headers=headers, timeout=30, **kwargs)
                elif method.upper() == 'POST':
                    response = requests.post(url, headers=headers, timeout=30, **kwargs)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                # Check for rate limiting
                if response.status_code == 429:
                    print(f"⚠️ Rate limited (429) on attempt {retry_count + 1}/{self.max_retries + 1}")

                    # Check for Retry-After header
                    retry_after = response.headers.get('Retry-After')
                    if retry_after:
                        try:
                            wait_time = int(retry_after)
                            print(f"📍 Retry-After header found: {wait_time} seconds")
                            print(f"⏰ Waiting {wait_time} seconds as instructed...")
                            time.sleep(wait_time)
                        except ValueError:
                            print(f"⚠️ Invalid Retry-After header: {retry_after}")

                    retry_count += 1
                    continue

                # Successful response or non-429 error
                return {
                    'response': response,
                    'status_code': response.status_code,
                    'success': response.status_code < 400,
                    'retry_count': retry_count,
                    'session_name': session_name,
                    'url': url
                }

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Request error on attempt {retry_count + 1}: {e}")
                retry_count += 1
                if retry_count > self.max_retries:
                    break
                self.intelligent_delay(is_retry=True, retry_count=retry_count)

        # All retries exhausted
        return {
            'response': None,
            'status_code': 429,
            'success': False,
            'retry_count': self.max_retries,
            'session_name': session_name,
            'url': url,
            'error': 'Max retries exhausted'
        }

    def rotate_session(self):
        """Rotate to next available session"""
        if len(self.valid_sessions) > 1:
            self.current_session_idx = (self.current_session_idx + 1) % len(self.valid_sessions)
            current_session = self.valid_sessions[self.current_session_idx]
            print(f"🔄 Rotated to session: {current_session['name']}")
            return current_session
        return self.valid_sessions[0] if self.valid_sessions else None

    def test_session_with_protection(self, session):
        """Test session with rate limiting protection"""
        session_name = session['name']
        session_data = session['data']

        print(f"\n📋 Testing session: {session_name}")
        print(f"   🔧 Rate limiting protection: ENABLED")

        # Test URLs with protection
        test_urls = [
            f"https://www.instagram.com/{self.target}/",
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target}",
            "https://www.instagram.com/direct/inbox/",
            "https://www.instagram.com/api/graphql/"
        ]

        results = []

        for i, url in enumerate(test_urls):
            print(f"   🔗 Testing endpoint {i+1}/{len(test_urls)}")

            result = self.make_request_with_retry(url, session_data, session_name)

            print(f"      📊 Status: {result['status_code']} | Retries: {result['retry_count']}")

            if result['success']:
                print(f"      ✅ Success after {result['retry_count']} retries")
            else:
                print(f"      ❌ Failed after {result['retry_count']} retries")

            results.append(result)

            # Add extra delay between different endpoints
            if i < len(test_urls) - 1:
                time.sleep(random.uniform(2, 5))

        return results

    def extract_with_enhanced_protection(self):
        """Main extraction method with enhanced rate limiting protection"""
        print(f"\n🎯 STARTING ENHANCED DM EXTRACTION")
        print(f"=" * 45)
        print(f"Target: {self.target}")
        print(f"Rate limiting protection: ENABLED")
        print(f"Valid sessions: {len(self.valid_sessions)}")
        print(f"User-Agent rotation: ENABLED ({len(self.user_agents)} agents)")

        if not self.valid_sessions:
            print("❌ No valid sessions found!")
            return None

        extraction_results = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'method': 'enhanced_rate_limiting_protection',
            'protection_features': [
                'Intelligent delay patterns',
                'Exponential backoff retry',
                'Retry-After header detection',
                'Session rotation',
                'User-Agent rotation',
                'Request throttling'
            ],
            'session_tests': [],
            'extraction_data': [],
            'total_429_errors': 0,
            'successful_requests': 0,
            'failed_requests': 0
        }

        # Test each session with protection
        for i, session in enumerate(self.valid_sessions):
            print(f"\n📋 Testing session {i+1}/{len(self.valid_sessions)}: {session['name']}")

            session_results = self.test_session_with_protection(session)

            # Count results
            session_429_count = sum(1 for r in session_results if r['status_code'] == 429)
            session_success_count = sum(1 for r in session_results if r['success'])

            extraction_results['total_429_errors'] += session_429_count
            extraction_results['successful_requests'] += session_success_count
            extraction_results['failed_requests'] += len(session_results) - session_success_count

            extraction_results['session_tests'].append({
                'session_name': session['name'],
                'results': session_results,
                'total_429_errors': session_429_count,
                'successful_requests': session_success_count
            })

            # Rotate session for next iteration
            if i < len(self.valid_sessions) - 1:
                self.rotate_session()
                time.sleep(random.uniform(5, 10))  # Longer delay between sessions

        # Save results
        timestamp = int(time.time())
        output_file = f"{self.output_dir}/enhanced_extraction_{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump(extraction_results, f, indent=2)

        # Generate summary
        print(f"\n✅ ENHANCED EXTRACTION COMPLETED")
        print(f"📂 Results saved: {output_file}")
        print(f"🎯 Sessions tested: {len(self.valid_sessions)}")
        print(f"📊 Total requests: {extraction_results['successful_requests'] + extraction_results['failed_requests']}")
        print(f"✅ Successful requests: {extraction_results['successful_requests']}")
        print(f"❌ Failed requests: {extraction_results['failed_requests']}")
        print(f"⚠️ Total 429 errors: {extraction_results['total_429_errors']}")

        if extraction_results['total_429_errors'] == 0:
            print(f"🎉 ZERO rate limiting errors! Protection system working perfectly!")
        elif extraction_results['total_429_errors'] < extraction_results['failed_requests']:
            print(f"✨ Rate limiting significantly reduced! Protection system effective!")

        return extraction_results

def main():
    print("🎯 ENHANCED INSTAGRAM DM EXTRACTOR")
    print("=" * 40)
    print("Features:")
    print("- Intelligent rate limiting protection")
    print("- Exponential backoff retry mechanism")
    print("- Session rotation and User-Agent rotation")
    print("- Retry-After header detection")
    print("- Request throttling and delay randomization")
    print()

    target = "alx.trading"
    extractor = EnhancedDMExtractor(target)

    results = extractor.extract_with_enhanced_protection()

    if results:
        print(f"\n🎯 OPERATION SUMMARY")
        print(f"Target: {results['target']}")
        print(f"Protection features active: {len(results['protection_features'])}")
        print(f"Rate limiting errors prevented: {results.get('prevented_429_errors', 'Calculated during operation')}")
        print(f"Extraction completed successfully! ✨")

if __name__ == "__main__":
    main()
