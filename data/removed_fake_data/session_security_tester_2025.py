# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔒 ADVANCED SESSION SECURITY TOOLKIT 2025
========================================
เครื่องมือทดสอบความปลอดภัยของ session สำหรับเจ้าของระบบ
- Session hijacking protection testing
- Session validation and monitoring
- Advanced authentication security

⚠️ สำหรับเจ้าของระบบเท่านั้น - Authorized Testing Only
"""

import json
import requests
import time
import hashlib
import urllib.parse
import re
import base64
from datetime import datetime, timedelta
import sqlite3
import threading
from pathlib import Path

class AdvancedSessionSecurityTester:
    """🔒 Advanced Session Security Testing Suite"""

    def __init__(self, target_domain=None):
        self.target_domain = target_domain or "localhost"
        self.project_root = "/workspaces/sugarglitch-realops"

        # Session storage
        self.sessions = {}
        self.intercepted_sessions = {}

        # Security test results
        self.security_results = {
            'session_vulnerabilities': [],
            'cookie_security': [],
            'auth_bypass': [],
            'session_fixation': [],
            'csrf_vulnerabilities': []
        }

        # Setup database for session tracking
        self.setup_security_database()

        print(f"🔒 Advanced Session Security Tester")
        print(f"   Target Domain: {self.target_domain}")
        print(f"   Testing Mode: Authorized Owner Testing")

    def setup_security_database(self):
        """Setup database for session security tracking"""
        db_path = f"{self.project_root}/data/session_security.db"
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS session_tests (
                id INTEGER PRIMARY KEY,
                test_type TEXT,
                target_url TEXT,
                session_id TEXT,
                test_payload TEXT,
                result TEXT,
                vulnerability_found BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS intercepted_sessions (
                id INTEGER PRIMARY KEY,
                session_id TEXT,
                cookies TEXT,
                headers TEXT,
                source_ip TEXT,
                user_agent TEXT,
                captured_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def capture_session_cookies(self, url, method='GET', data=None):
        """🕵️ Capture and analyze session cookies"""
        print(f"\n🕵️ CAPTURING SESSION COOKIES")
        print(f"================================")

        session = requests.Session()

        try:
            if method.upper() == 'GET':
                response = session.get(url, timeout=10)
            else:
                response = session.post(url, data=data, timeout=10)

            print(f"📡 Response Status: {response.status_code}")

            # Analyze cookies
            cookies_info = []
            for cookie in response.cookies:
                cookie_analysis = self.analyze_cookie_security(cookie)
                cookies_info.append(cookie_analysis)

                print(f"🍪 Cookie: {cookie.name}")
                print(f"   Value: {cookie.value[:20]}...")
                print(f"   Domain: {cookie.domain}")
                print(f"   Secure: {cookie.secure}")
                print(f"   HttpOnly: {getattr(cookie, 'httponly', False)}")
                print(f"   SameSite: {getattr(cookie, 'samesite', 'None')}")

            # Store session for testing
            session_id = self.generate_session_id(response.cookies)
            self.sessions[session_id] = {
                'cookies': dict(response.cookies),
                'headers': dict(response.headers),
                'url': url,
                'captured_time': datetime.now().isoformat(),
                'security_analysis': cookies_info
            }

            print(f"✅ Session captured: {session_id}")
            return session_id, cookies_info

        except Exception as e:
            print(f"❌ Session capture failed: {e}")
            return None, []

    def analyze_cookie_security(self, cookie):
        """🔍 Analyze cookie security properties"""
        analysis = {
            'name': cookie.name,
            'value_length': len(cookie.value),
            'secure': cookie.secure,
            'httponly': getattr(cookie, 'httponly', False),
            'samesite': getattr(cookie, 'samesite', None),
            'domain': cookie.domain,
            'path': cookie.path,
            'vulnerabilities': []
        }

        # Check for security vulnerabilities
        if not cookie.secure:
            analysis['vulnerabilities'].append('Missing Secure flag')

        if not getattr(cookie, 'httponly', False):
            analysis['vulnerabilities'].append('Missing HttpOnly flag')

        if not getattr(cookie, 'samesite', None):
            analysis['vulnerabilities'].append('Missing SameSite attribute')

        # Check for weak session IDs
        if self.is_weak_session_id(cookie.value):
            analysis['vulnerabilities'].append('Weak session ID detected')

        return analysis

    def is_weak_session_id(self, session_value):
        """Check if session ID is weak or predictable"""
        # Check length
        if len(session_value) < 16:
            return True

        # Check for sequential patterns
        if re.search(r'(123|abc|000|111)', session_value, re.IGNORECASE):
            return True

        # Check entropy (simplified)
        unique_chars = len(set(session_value))
        if unique_chars < len(session_value) * 0.5:
            return True

        return False

    def test_session_fixation(self, target_url, login_endpoint=None):
        """🎯 Test for session fixation vulnerabilities"""
        print(f"\n🎯 TESTING SESSION FIXATION")
        print(f"============================")

        results = []

        try:
            # Step 1: Get initial session
            print("📋 Step 1: Obtaining initial session...")
            session1 = requests.Session()
            response1 = session1.get(target_url)
            initial_cookies = dict(response1.cookies)

            if not initial_cookies:
                print("❌ No session cookies found")
                return results

            print(f"✅ Initial session: {list(initial_cookies.keys())}")

            # Step 2: Perform login (if endpoint provided)
            if login_endpoint:
                print("🔐 Step 2: Attempting authentication...")
                login_data = {
                    'username': 'test_user',
                    'password': 'test_password'
                }

                response2 = session1.post(login_endpoint, data=login_data)
                after_login_cookies = dict(session1.cookies)

                # Check if session ID changed after login
                session_changed = False
                for cookie_name in initial_cookies:
                    if cookie_name in after_login_cookies:
                        if initial_cookies[cookie_name] != after_login_cookies[cookie_name]:
                            session_changed = True
                            break

                result = {
                    'test_type': 'session_fixation',
                    'target_url': target_url,
                    'session_changed_after_login': session_changed,
                    'vulnerability': not session_changed,
                    'initial_cookies': initial_cookies,
                    'after_login_cookies': after_login_cookies
                }

                if not session_changed:
                    print("⚠️ VULNERABILITY: Session ID not changed after login")
                    self.security_results['session_fixation'].append(result)
                else:
                    print("✅ Session ID properly regenerated after login")

                results.append(result)

        except Exception as e:
            print(f"❌ Session fixation test failed: {e}")

        return results

    def test_session_hijacking_protection(self, session_id):
        """🛡️ Test session hijacking protection mechanisms"""
        print(f"\n🛡️ TESTING SESSION HIJACKING PROTECTION")
        print(f"========================================")

        if session_id not in self.sessions:
            print("❌ Session not found")
            return []

        session_data = self.sessions[session_id]
        results = []

        # Test 1: IP Address Binding
        print("🔍 Test 1: IP Address Binding Check...")
        ip_binding_result = self.test_ip_binding(session_data)
        results.append(ip_binding_result)

        # Test 2: User Agent Binding
        print("🔍 Test 2: User Agent Binding Check...")
        ua_binding_result = self.test_user_agent_binding(session_data)
        results.append(ua_binding_result)

        # Test 3: Session Timeout
        print("🔍 Test 3: Session Timeout Check...")
        timeout_result = self.test_session_timeout(session_data)
        results.append(timeout_result)

        # Test 4: Concurrent Session Limits
        print("🔍 Test 4: Concurrent Session Limits...")
        concurrent_result = self.test_concurrent_sessions(session_data)
        results.append(concurrent_result)

        return results

    def test_ip_binding(self, session_data):
        """Test if session is bound to IP address"""
        try:
            # Simulate request from different IP using proxy headers
            session = requests.Session()

            # Set original cookies
            for name, value in session_data['cookies'].items():
                session.cookies.set(name, value)

            # Add spoofed IP headers
            spoofed_headers = {
                'X-Forwarded-For': '192.168.1.100',
                'X-Real-IP': '192.168.1.100',
                'X-Originating-IP': '192.168.1.100'
            }

            response = session.get(session_data['url'], headers=spoofed_headers)

            result = {
                'test_type': 'ip_binding',
                'spoofed_ip_accepted': response.status_code == 200,
                'vulnerability': response.status_code == 200,
                'response_code': response.status_code
            }

            if result['vulnerability']:
                print("⚠️ VULNERABILITY: Session not bound to IP address")
            else:
                print("✅ Session appears to be IP-bound")

            return result

        except Exception as e:
            print(f"❌ IP binding test failed: {e}")
            return {'test_type': 'ip_binding', 'error': str(e)}

    def test_user_agent_binding(self, session_data):
        """Test if session is bound to User-Agent"""
        try:
            session = requests.Session()

            # Set original cookies
            for name, value in session_data['cookies'].items():
                session.cookies.set(name, value)

            # Use different User-Agent
            spoofed_headers = {
                'User-Agent': 'Mozilla/5.0 (Totally Different Browser)'
            }

            response = session.get(session_data['url'], headers=spoofed_headers)

            result = {
                'test_type': 'user_agent_binding',
                'different_ua_accepted': response.status_code == 200,
                'vulnerability': response.status_code == 200,
                'response_code': response.status_code
            }

            if result['vulnerability']:
                print("⚠️ VULNERABILITY: Session not bound to User-Agent")
            else:
                print("✅ Session appears to be User-Agent bound")

            return result

        except Exception as e:
            print(f"❌ User-Agent binding test failed: {e}")
            return {'test_type': 'user_agent_binding', 'error': str(e)}

    def test_session_timeout(self, session_data):
        """Test session timeout mechanisms"""
        try:
            # Check if session has timeout indicators
            timeout_indicators = []

            # Check cookie expiration
            for name, value in session_data['cookies'].items():
                if 'expires' in str(value).lower():
                    timeout_indicators.append(f"Cookie {name} has expiration")

            # Test with old session (simulate time passage)
            session = requests.Session()
            for name, value in session_data['cookies'].items():
                session.cookies.set(name, value)

            # Add headers to simulate time passage
            old_time_headers = {
                'If-Modified-Since': (datetime.now() - timedelta(hours=24)).strftime('%a, %d %b %Y %H:%M:%S GMT')
            }

            response = session.get(session_data['url'], headers=old_time_headers)

            result = {
                'test_type': 'session_timeout',
                'timeout_indicators': timeout_indicators,
                'old_session_accepted': response.status_code == 200,
                'vulnerability': len(timeout_indicators) == 0,
                'response_code': response.status_code
            }

            if result['vulnerability']:
                print("⚠️ VULNERABILITY: No session timeout mechanisms detected")
            else:
                print("✅ Session timeout mechanisms present")

            return result

        except Exception as e:
            print(f"❌ Session timeout test failed: {e}")
            return {'test_type': 'session_timeout', 'error': str(e)}

    def test_concurrent_sessions(self, session_data):
        """Test concurrent session limitations"""
        try:
            # Create multiple sessions with same credentials
            sessions = []

            for i in range(3):
                session = requests.Session()
                for name, value in session_data['cookies'].items():
                    session.cookies.set(name, value)
                sessions.append(session)

            # Test concurrent access
            responses = []
            for i, session in enumerate(sessions):
                try:
                    response = session.get(session_data['url'])
                    responses.append({
                        'session': i + 1,
                        'status_code': response.status_code,
                        'success': response.status_code == 200
                    })
                except Exception as e:
                    responses.append({
                        'session': i + 1,
                        'error': str(e),
                        'success': False
                    })

            successful_concurrent = sum(1 for r in responses if r.get('success', False))

            result = {
                'test_type': 'concurrent_sessions',
                'concurrent_sessions_allowed': successful_concurrent,
                'vulnerability': successful_concurrent > 1,
                'responses': responses
            }

            if result['vulnerability']:
                print(f"⚠️ VULNERABILITY: {successful_concurrent} concurrent sessions allowed")
            else:
                print("✅ Concurrent session limitations in place")

            return result

        except Exception as e:
            print(f"❌ Concurrent session test failed: {e}")
            return {'test_type': 'concurrent_sessions', 'error': str(e)}

    def test_csrf_protection(self, target_url, form_endpoints=None):
        """🛡️ Test CSRF protection mechanisms"""
        print(f"\n🛡️ TESTING CSRF PROTECTION")
        print(f"==========================")

        results = []

        try:
            # Test basic CSRF
            session = requests.Session()
            response = session.get(target_url)

            # Look for CSRF tokens in response
            csrf_tokens_found = []
            if 'csrf' in response.text.lower():
                csrf_patterns = [
                    r'name=["\']csrf[_-]?token["\'][^>]*value=["\']([^"\']+)',
                    r'<meta[^>]*name=["\']csrf[_-]?token["\'][^>]*content=["\']([^"\']+)',
                    r'_token["\']?\s*:\s*["\']([^"\']+)'
                ]

                for pattern in csrf_patterns:
                    matches = re.findall(pattern, response.text, re.IGNORECASE)
                    csrf_tokens_found.extend(matches)

            # Test form endpoints if provided
            if form_endpoints:
                for endpoint in form_endpoints:
                    csrf_result = self.test_csrf_on_endpoint(session, endpoint)
                    results.append(csrf_result)

            general_result = {
                'test_type': 'csrf_protection',
                'csrf_tokens_found': len(csrf_tokens_found),
                'tokens': csrf_tokens_found[:5],  # Show first 5 tokens
                'vulnerability': len(csrf_tokens_found) == 0
            }

            if general_result['vulnerability']:
                print("⚠️ VULNERABILITY: No CSRF tokens detected")
            else:
                print(f"✅ CSRF tokens found: {len(csrf_tokens_found)}")

            results.append(general_result)

        except Exception as e:
            print(f"❌ CSRF protection test failed: {e}")

        return results

    def test_csrf_on_endpoint(self, session, endpoint):
        """Test CSRF protection on specific endpoint"""
        try:
            # Attempt POST without CSRF token
            test_data = {'test': 'value'}
            response = session.post(endpoint, data=test_data)

            result = {
                'test_type': 'csrf_endpoint',
                'endpoint': endpoint,
                'post_without_token_allowed': response.status_code in [200, 201, 302],
                'vulnerability': response.status_code in [200, 201, 302],
                'response_code': response.status_code
            }

            if result['vulnerability']:
                print(f"⚠️ VULNERABILITY: {endpoint} accepts POST without CSRF token")
            else:
                print(f"✅ {endpoint} requires CSRF token")

            return result

        except Exception as e:
            return {'test_type': 'csrf_endpoint', 'endpoint': endpoint, 'error': str(e)}

    def generate_session_id(self, cookies):
        """Generate unique session ID for tracking"""
        cookie_string = str(sorted(cookies.items()))
        return hashlib.md5(cookie_string.encode()).hexdigest()[:16]

    def comprehensive_session_security_test(self, target_url, login_endpoint=None, form_endpoints=None):
        """🎯 Comprehensive session security assessment"""
        print(f"\n🎯 COMPREHENSIVE SESSION SECURITY TEST")
        print(f"======================================")
        print(f"Target: {target_url}")
        print(f"Login Endpoint: {login_endpoint}")
        print(f"Form Endpoints: {form_endpoints}")

        all_results = {
            'target_url': target_url,
            'test_timestamp': datetime.now().isoformat(),
            'tests_performed': []
        }

        # Test 1: Capture and analyze session
        session_id, cookie_analysis = self.capture_session_cookies(target_url)
        if session_id:
            all_results['session_id'] = session_id
            all_results['cookie_analysis'] = cookie_analysis

        # Test 2: Session fixation
        fixation_results = self.test_session_fixation(target_url, login_endpoint)
        all_results['tests_performed'].extend(fixation_results)

        # Test 3: Session hijacking protection
        if session_id:
            hijacking_results = self.test_session_hijacking_protection(session_id)
            all_results['tests_performed'].extend(hijacking_results)

        # Test 4: CSRF protection
        csrf_results = self.test_csrf_protection(target_url, form_endpoints)
        all_results['tests_performed'].extend(csrf_results)

        # Generate report
        report = self.generate_security_report(all_results)

        # Save results
        timestamp = int(time.time())
        output_file = f"{self.project_root}/reports/session_security_test_{timestamp}.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)

        print(f"\n✅ COMPREHENSIVE TEST COMPLETED!")
        print(f"📂 Results saved: {output_file}")

        return all_results

    def generate_security_report(self, results):
        """Generate comprehensive security report"""
        vulnerabilities = [test for test in results.get('tests_performed', [])
                         if test.get('vulnerability', False)]

        print(f"\n📋 SECURITY ASSESSMENT SUMMARY")
        print(f"==============================")
        print(f"Target: {results['target_url']}")
        print(f"Test Time: {results['test_timestamp']}")
        print(f"Tests Performed: {len(results.get('tests_performed', []))}")
        print(f"Vulnerabilities Found: {len(vulnerabilities)}")

        if vulnerabilities:
            print(f"\n⚠️ VULNERABILITIES DETECTED:")
            for i, vuln in enumerate(vulnerabilities, 1):
                print(f"   {i}. {vuln.get('test_type', 'Unknown')} - {vuln.get('vulnerability', 'Unknown')}")
        else:
            print(f"\n✅ NO CRITICAL VULNERABILITIES DETECTED")

        # Cookie security summary
        cookie_analysis = results.get('cookie_analysis', [])
        if cookie_analysis:
            print(f"\n🍪 COOKIE SECURITY SUMMARY:")
            for cookie in cookie_analysis:
                if cookie.get('vulnerabilities'):
                    print(f"   Cookie '{cookie['name']}': {', '.join(cookie['vulnerabilities'])}")

        return results

def main():
    """Main testing function"""
    print("🔒 ADVANCED SESSION SECURITY TOOLKIT 2025")
    print("==========================================")
    print("⚠️ FOR AUTHORIZED SYSTEM TESTING ONLY ⚠️")
    print("==========================================")

    # Example usage for testing your own system
    tester = AdvancedSessionSecurityTester("your-domain.com")

    # Comprehensive test
    results = tester.comprehensive_session_security_test(
        target_url="https://your-domain.com/",
        login_endpoint="https://your-domain.com/login",
        form_endpoints=[
            "https://your-domain.com/contact",
            "https://your-domain.com/profile/update"
        ]
    )

    print("\n🎯 Testing complete!")
    print("📊 Check the generated report for detailed findings")

if __name__ == "__main__":
    main()
