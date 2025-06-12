# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Simple Automated Instagram DM Extractor
Uses requests-only approach without Playwright dependencies
"""

import json
import requests
import time
import random
from pathlib import Path
from datetime import datetime
import base64

class SimpleAutomatedExtractor:
    def __init__(self):
        self.correct_username = "alxtrading"  # Fixed username
        self.session = requests.Session()
        self.proxies = self.load_working_proxies()

    def load_working_proxies(self):
        """Load working proxy list"""
        try:
            with open("config/working_proxies.json", 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'proxies' in data:
                    return data['proxies']
        except Exception:
            pass
        return []

    def setup_session(self):
        """Setup session with rotating proxy and headers"""
        # Use proxy if available
        if self.proxies:
            proxy = random.choice(self.proxies)
            if isinstance(proxy, dict):
                self.session.proxies.update(proxy)
                print(f"🌐 Using proxy: {list(proxy.values())[0]}")

        # Setup headers to mimic real browser
        user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]

        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest'
        })

    def find_best_session(self):
        """Find the best available session from all sources"""
        print("🔍 Searching for valid sessions...")

        session_sources = [
            # Direct session files
            {"path": "tools/session_alx_trading.json", "type": "direct"},
            {"path": "automated_session.json", "type": "direct"},
            {"path": "manual_session.json", "type": "direct"},

            # Hijacked sessions directory
            {"path": "hijacked_sessions", "type": "directory"},
            {"path": "sessions", "type": "directory"},
            {"path": "sessions_fresh", "type": "directory"},

            # Config files
            {"path": "config/master_config.json", "type": "config"},
            {"path": "config/config.json", "type": "config"},
        ]

        best_session = None
        best_score = 0

        for source in session_sources:
            sessions = self.extract_sessions_from_source(source)

            for session_data in sessions:
                score = self.score_session(session_data)
                if score > best_score:
                    best_session = session_data
                    best_score = score
                    print(f"✅ Better session found (score: {score}): {session_data.get('source', 'unknown')}")

        if best_session:
            print(f"🎯 Using best session (score: {best_score})")
            return best_session['sessionid']

        print("❌ No valid sessions found")
        return None

    def extract_sessions_from_source(self, source):
        """Extract sessions from a source"""
        sessions = []
        path = Path(source["path"])

        try:
            if source["type"] == "direct" and path.exists():
                with open(path, 'r') as f:
                    data = json.load(f)
                    sessionid = self.extract_sessionid_from_data(data)
                    if sessionid:
                        sessions.append({
                            "sessionid": sessionid,
                            "source": str(path),
                            "timestamp": path.stat().st_mtime
                        })

            elif source["type"] == "directory" and path.exists():
                for file_path in path.glob("*.json"):
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            sessionid = self.extract_sessionid_from_data(data)
                            if sessionid:
                                sessions.append({
                                    "sessionid": sessionid,
                                    "source": str(file_path),
                                    "timestamp": file_path.stat().st_mtime
                                })
                    except Exception:
                        continue

            elif source["type"] == "config" and path.exists():
                with open(path, 'r') as f:
                    data = json.load(f)
                    sessionid = self.extract_sessionid_from_config(data)
                    if sessionid:
                        sessions.append({
                            "sessionid": sessionid,
                            "source": str(path),
                            "timestamp": path.stat().st_mtime
                        })

        except Exception as e:
            pass

        return sessions

    def extract_sessionid_from_data(self, data):
        """Extract sessionid from various data formats"""
        if isinstance(data, str):
            return data if len(data) > 20 else None

        if isinstance(data, dict):
            # Direct sessionid
            if 'sessionid' in data:
                return data['sessionid']

            # Cookie format
            if 'cookies' in data:
                cookies = data['cookies']
                if isinstance(cookies, list):
                    for cookie in cookies:
                        if cookie.get('name') == 'sessionid':
                            return cookie.get('value')
                elif isinstance(cookies, dict):
                    return cookies.get('sessionid')

            # Session data
            if 'session' in data:
                return self.extract_sessionid_from_data(data['session'])

        return None

    def extract_sessionid_from_config(self, data):
        """Extract sessionid from config files"""
        # Check Instagram specific configs
        if 'instagram' in data:
            ig_data = data['instagram']
            return self.extract_sessionid_from_data(ig_data)

        # Check general session configs
        if 'sessions' in data:
            return self.extract_sessionid_from_data(data['sessions'])

        return None

    def score_session(self, session_data):
        """Score a session based on various factors"""
        score = 0
        sessionid = session_data['sessionid']

        # Length check (Instagram sessions are typically 32+ chars)
        if len(sessionid) >= 32:
            score += 10

        # Recency check (newer files get higher score)
        timestamp = session_data.get('timestamp', 0)
        hours_old = (time.time() - timestamp) / 3600
        if hours_old < 24:
            score += 5
        elif hours_old < 168:  # 1 week
            score += 3

        # Source reliability
        source = session_data.get('source', '')
        if 'fresh' in source or 'new' in source:
            score += 3
        if 'hijacked' in source:
            score += 2

        return score

    def test_session_validity(self, sessionid):
        """Test if session is valid by making a test request"""
        try:
            self.session.cookies.set('sessionid', sessionid, domain='.instagram.com')

            # Add required Instagram cookies
            self.session.cookies.set('csrftoken', 'missing', domain='.instagram.com')
            self.session.cookies.set('mid', f'Y{int(time.time())}-0', domain='.instagram.com')

            # Test with a simple API call
            test_url = 'https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram'
            headers = {
                'X-IG-App-ID': '936619743392459',
                'X-CSRFToken': 'missing',
                'X-Requested-With': 'XMLHttpRequest'
            }

            response = self.session.get(test_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    return True

        except Exception as e:
            print(f"Session test error: {e}")

        return False

    def extract_target_data(self, sessionid):
        """Extract data for the target username"""
        print(f"🎯 Extracting data for: {self.correct_username}")

        self.setup_session()
        self.session.cookies.set('sessionid', sessionid, domain='.instagram.com')

        # Add required cookies
        cookies = {
            'csrftoken': 'missing',
            'mid': f'Y{int(time.time())}-0',
            'ig_did': f'{random.randint(10**17, 10**18-1)}',
            'ig_nrcb': '1',
            'rur': 'VLL'
        }

        for name, value in cookies.items():
            self.session.cookies.set(name, value, domain='.instagram.com')

        result = {
            "timestamp": datetime.now().isoformat(),
            "target": self.correct_username,
            "method": "simple_automated",
            "extraction_attempts": []
        }

        # Method 1: Profile API
        try:
            print("📊 Method 1: Profile API...")
            profile_url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.correct_username}'
            headers = {
                'X-IG-App-ID': '936619743392459',
                'X-CSRFToken': 'missing',
                'X-Requested-With': 'XMLHttpRequest'
            }

            response = self.session.get(profile_url, headers=headers, timeout=15)

            attempt = {
                "method": "profile_api",
                "status_code": response.status_code,
                "timestamp": datetime.now().isoformat()
            }

            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    user_data = data['data']['user']
                    result["profile_data"] = user_data
                    result["user_id"] = user_data.get('id')
                    attempt["success"] = True
                    print(f"✅ Profile found: {user_data.get('full_name', 'N/A')}")
                else:
                    attempt["success"] = False
                    attempt["error"] = "Invalid response format"
            else:
                attempt["success"] = False
                attempt["error"] = f"HTTP {response.status_code}"
                attempt["response"] = response.text[:200]

            result["extraction_attempts"].append(attempt)

        except Exception as e:
            result["extraction_attempts"].append({
                "method": "profile_api",
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })

        # Method 2: Direct Messages API (if profile successful)
        if result.get("user_id"):
            try:
                print("💬 Method 2: DM API...")
                dm_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'

                response = self.session.get(dm_url, headers=headers, timeout=15)

                attempt = {
                    "method": "dm_api",
                    "status_code": response.status_code,
                    "timestamp": datetime.now().isoformat()
                }

                if response.status_code == 200:
                    dm_data = response.json()
                    result["dm_data"] = dm_data

                    # Look for target conversation
                    threads = dm_data.get('inbox', {}).get('threads', [])
                    target_thread = None

                    for thread in threads:
                        users = thread.get('users', [])
                        for user in users:
                            if user.get('username') == self.correct_username:
                                target_thread = thread
                                break
                        if target_thread:
                            break

                    if target_thread:
                        result["target_conversation"] = target_thread
                        result["message_count"] = len(target_thread.get('items', []))
                        print(f"🎯 Found conversation with {result['message_count']} messages")
                        attempt["success"] = True
                        attempt["message_count"] = result['message_count']
                    else:
                        print("⚠️ No conversation found with target")
                        attempt["success"] = True
                        attempt["message_count"] = 0

                else:
                    attempt["success"] = False
                    attempt["error"] = f"HTTP {response.status_code}"
                    attempt["response"] = response.text[:200]

                result["extraction_attempts"].append(attempt)

            except Exception as e:
                result["extraction_attempts"].append({
                    "method": "dm_api",
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })

        # Save results
        output_file = f"simple_automated_extraction_{int(time.time())}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)

        print(f"💾 Results saved to: {output_file}")

        # Determine success
        successful_attempts = [a for a in result["extraction_attempts"] if a.get("success")]
        return len(successful_attempts) > 0

def main():
    print("🚀 SIMPLE AUTOMATED Instagram DM Extractor")
    print("=" * 60)
    print("🎯 Target: alxtrading (corrected username)")
    print("🤖 Mode: Simple Automation (no Playwright)")
    print("=" * 60)

    extractor = SimpleAutomatedExtractor()

    # Find best session
    print("\n🔍 STEP 1: Finding Best Session")
    sessionid = extractor.find_best_session()

    if sessionid:
        print(f"✅ Session found: {sessionid[:20]}...")

        # Test session validity
        print("\n🧪 STEP 2: Testing Session Validity")
        if extractor.test_session_validity(sessionid):
            print("✅ Session is valid!")

            # Extract data
            print("\n📊 STEP 3: Data Extraction")
            success = extractor.extract_target_data(sessionid)

            if success:
                print("\n🎉 EXTRACTION COMPLETED SUCCESSFULLY!")
                print("📁 Check output file for detailed results")
            else:
                print("\n⚠️ EXTRACTION PARTIALLY SUCCESSFUL")
                print("📁 Check output file for details")
        else:
            print("❌ Session is invalid or expired")
            print("💡 Need fresh session from browser")
    else:
        print("❌ No sessions found")
        print("💡 Please add a valid sessionid to any of these locations:")
        print("   - manual_session.json")
        print("   - tools/session_alx_trading.json")
        print("   - hijacked_sessions/ directory")

if __name__ == "__main__":
    main()
