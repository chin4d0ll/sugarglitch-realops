# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔥 INSTAGRAM SESSION SECURITY ANALYZER 2025
===========================================
เครื่องมือวิเคราะห์และทดสอบความปลอดภัยของ Instagram session
- Session validation และ security analysis
- Cookie security assessment
- Authentication bypass testing
- Session hijacking protection evaluation

⚠️ สำหรับเจ้าของระบบและการทดสอบที่ได้รับอนุญาตเท่านั้น
"""

import json
import requests
import time
import hashlib
import base64
import re
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlparse
import sqlite3
from pathlib import Path

class InstagramSessionAnalyzer:
    """🔍 Instagram Session Security Analyzer"""

    def __init__(self):
        self.project_root = "/workspaces/sugarglitch-realops"
        self.instagram_endpoints = {
            'login': 'https://www.instagram.com/accounts/login/',
            'api_base': 'https://www.instagram.com/api/v1/',
            'direct': 'https://www.instagram.com/direct/',
            'graphql': 'https://www.instagram.com/graphql/query/'
        }

        # Session analysis results
        self.analysis_results = {
            'session_strength': {},
            'security_features': {},
            'vulnerabilities': [],
            'recommendations': []
        }

        print("🔥 Instagram Session Security Analyzer 2025")
        print("=" * 50)

    def load_instagram_session(self, session_file=None):
        """📂 Load Instagram session from file"""
        if not session_file:
            session_file = f"{self.project_root}/sessions/session-alx.trading"

        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)

            cookies = session_data.get('cookies', {})
            print(f"✅ Loaded session: {list(cookies.keys())}")

            return cookies

        except Exception as e:
            print(f"❌ Failed to load session: {e}")
            return None

    def analyze_instagram_cookies(self, cookies):
        """🍪 Analyze Instagram cookie security"""
        print(f"\n🍪 ANALYZING INSTAGRAM COOKIES")
        print(f"==============================")

        cookie_analysis = {}
        security_score = 0
        max_score = 0

        for cookie_name, cookie_value in cookies.items():
            max_score += 10
            analysis = {
                'name': cookie_name,
                'value_length': len(str(cookie_value)),
                'security_features': [],
                'vulnerabilities': [],
                'strength_score': 0
            }

            # Analyze session ID (sessionid cookie)
            if cookie_name == 'sessionid':
                analysis['type'] = 'primary_session'

                # Check session ID strength
                if len(str(cookie_value)) >= 32:
                    analysis['security_features'].append('Strong length (32+ chars)')
                    analysis['strength_score'] += 3
                    security_score += 3
                else:
                    analysis['vulnerabilities'].append('Weak session ID length')

                # Check for entropy
                if self.check_entropy(str(cookie_value)):
                    analysis['security_features'].append('Good entropy')
                    analysis['strength_score'] += 2
                    security_score += 2
                else:
                    analysis['vulnerabilities'].append('Low entropy detected')

                # Check for patterns
                if not self.has_predictable_patterns(str(cookie_value)):
                    analysis['security_features'].append('No predictable patterns')
                    analysis['strength_score'] += 2
                    security_score += 2
                else:
                    analysis['vulnerabilities'].append('Predictable patterns found')

            # Analyze CSRF token
            elif cookie_name == 'csrftoken':
                analysis['type'] = 'csrf_protection'

                if len(str(cookie_value)) >= 32:
                    analysis['security_features'].append('Strong CSRF token length')
                    analysis['strength_score'] += 2
                    security_score += 2
                else:
                    analysis['vulnerabilities'].append('Weak CSRF token')

            # Analyze other security cookies
            else:
                analysis['type'] = 'auxiliary'
                analysis['strength_score'] += 1
                security_score += 1

            cookie_analysis[cookie_name] = analysis

            print(f"🔍 Cookie: {cookie_name}")
            print(f"   Type: {analysis.get('type', 'unknown')}")
            print(f"   Length: {analysis['value_length']} chars")
            print(f"   Score: {analysis['strength_score']}/10")

            if analysis['security_features']:
                print(f"   ✅ Features: {', '.join(analysis['security_features'])}")

            if analysis['vulnerabilities']:
                print(f"   ⚠️ Issues: {', '.join(analysis['vulnerabilities'])}")

        overall_score = (security_score / max_score) * 100 if max_score > 0 else 0
        print(f"\n📊 Overall Cookie Security Score: {overall_score:.1f}%")

        self.analysis_results['session_strength'] = {
            'overall_score': overall_score,
            'cookie_analysis': cookie_analysis
        }

        return cookie_analysis

    def check_entropy(self, value):
        """Check entropy of a value"""
        if len(value) < 8:
            return False

        # Simple entropy check - count unique characters
        unique_chars = len(set(value))
        entropy_ratio = unique_chars / len(value)

        return entropy_ratio > 0.5

    def has_predictable_patterns(self, value):
        """Check for predictable patterns in session ID"""
        patterns = [
            r'123456',
            r'abcdef',
            r'000000',
            r'111111',
            r'(.)\1{3,}',  # Repeated characters
            r'(012|123|234|345|456|567|678|789)',  # Sequential numbers
        ]

        for pattern in patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return True

        return False

    def test_session_validity(self, cookies):
        """🔐 Test Instagram session validity"""
        print(f"\n🔐 TESTING SESSION VALIDITY")
        print(f"===========================")

        session = requests.Session()

        # Add cookies to session
        for name, value in cookies.items():
            session.cookies.set(name, value, domain='.instagram.com')

        # Standard headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.instagram.com/',
        }

        session.headers.update(headers)

        validity_tests = []

        # Test 1: Homepage access
        try:
            print("📋 Test 1: Homepage access...")
            response = session.get("https://www.instagram.com/", timeout=10)

            homepage_test = {
                'test': 'homepage_access',
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'logged_in': '"is_logged_in":true' in response.text,
                'content_length': len(response.text)
            }

            if homepage_test['logged_in']:
                print("   ✅ Session valid - logged in")
            elif homepage_test['success']:
                print("   ⚠️ Session accessible but login status unclear")
            else:
                print("   ❌ Session invalid or blocked")

            validity_tests.append(homepage_test)

        except Exception as e:
            print(f"   ❌ Homepage test failed: {e}")
            validity_tests.append({'test': 'homepage_access', 'error': str(e)})

        # Test 2: Direct messages access
        try:
            print("📋 Test 2: Direct messages access...")
            response = session.get("https://www.instagram.com/direct/inbox/", timeout=10)

            dm_test = {
                'test': 'direct_messages',
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'has_dm_content': 'direct' in response.text.lower(),
                'redirect_to_login': '/accounts/login' in response.url
            }

            if dm_test['success'] and not dm_test['redirect_to_login']:
                print("   ✅ Direct messages accessible")
            else:
                print("   ❌ Direct messages not accessible")

            validity_tests.append(dm_test)

        except Exception as e:
            print(f"   ❌ DM test failed: {e}")
            validity_tests.append({'test': 'direct_messages', 'error': str(e)})

        # Test 3: API access
        try:
            print("📋 Test 3: API access...")

            # Get CSRF token first
            csrf_token = cookies.get('csrftoken', '')
            api_headers = headers.copy()
            api_headers.update({
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest'
            })

            response = session.get(
                "https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram",
                headers=api_headers,
                timeout=10
            )

            api_test = {
                'test': 'api_access',
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'has_json_response': False
            }

            try:
                json_data = response.json()
                api_test['has_json_response'] = True
                api_test['response_data'] = 'Valid JSON response'
            except Exception:
                api_test['response_data'] = 'Non-JSON response'

            if api_test['success']:
                print("   ✅ API access working")
            else:
                print("   ❌ API access blocked")

            validity_tests.append(api_test)

        except Exception as e:
            print(f"   ❌ API test failed: {e}")
            validity_tests.append({'test': 'api_access', 'error': str(e)})

        # Calculate overall validity score
        successful_tests = sum(1 for test in validity_tests if test.get('success', False))
        validity_score = (successful_tests / len(validity_tests)) * 100

        print(f"\n📊 Session Validity Score: {validity_score:.1f}%")
        print(f"📋 Successful Tests: {successful_tests}/{len(validity_tests)}")

        self.analysis_results['security_features']['session_validity'] = {
            'score': validity_score,
            'tests': validity_tests
        }

        return validity_tests

    def analyze_session_security_features(self, cookies):
        """🛡️ Analyze Instagram session security features"""
        print(f"\n🛡️ ANALYZING SECURITY FEATURES")
        print(f"===============================")

        security_features = {
            'csrf_protection': False,
            'secure_cookies': False,
            'httponly_cookies': False,
            'samesite_protection': False,
            'session_rotation': False
        }

        # Check CSRF protection
        if 'csrftoken' in cookies:
            security_features['csrf_protection'] = True
            print("✅ CSRF token present")
        else:
            print("❌ No CSRF token found")
            self.analysis_results['vulnerabilities'].append({
                'type': 'missing_csrf',
                'severity': 'HIGH',
                'description': 'No CSRF token found in session'
            })

        # Note: We can't directly check Secure, HttpOnly, SameSite from just cookie values
        # These would need to be checked during actual HTTP responses
        print("⚠️ Note: Secure, HttpOnly, SameSite flags require HTTP response analysis")

        # Check for session rotation indicators
        sessionid = cookies.get('sessionid', '')
        if sessionid and self.appears_recently_generated(sessionid):
            security_features['session_rotation'] = True
            print("✅ Session appears recently generated")
        else:
            print("⚠️ Session age cannot be determined")

        self.analysis_results['security_features'].update(security_features)
        return security_features

    def appears_recently_generated(self, session_value):
        """Check if session appears recently generated (heuristic)"""
        # This is a heuristic - Instagram sessionid format includes timestamp
        try:
            # Instagram sessionid often has format like: user_id%3Atimestamp%3Ahash
            if '%3A' in session_value:  # URL encoded colon
                parts = session_value.split('%3A')
                if len(parts) >= 2:
                    # Try to extract timestamp
                    timestamp_part = parts[1]
                    try:
                        timestamp = int(timestamp_part)
                        session_time = datetime.fromtimestamp(timestamp)
                        age = datetime.now() - session_time

                        # Consider "recent" if less than 30 days old
                        return age.days < 30
                    except Exception:
                        pass
        except Exception:
            pass

        return False

    def test_session_hijacking_resistance(self, cookies):
        """🥷 Test resistance to session hijacking"""
        print(f"\n🥷 TESTING HIJACKING RESISTANCE")
        print(f"===============================")

        resistance_tests = []

        # Test 1: Different User-Agent
        print("📋 Test 1: Different User-Agent resistance...")
        ua_test = self.test_user_agent_change(cookies)
        resistance_tests.append(ua_test)

        # Test 2: Different IP simulation
        print("📋 Test 2: IP change simulation...")
        ip_test = self.test_ip_change_simulation(cookies)
        resistance_tests.append(ip_test)

        # Test 3: Missing referrer
        print("📋 Test 3: Missing referrer test...")
        referrer_test = self.test_missing_referrer(cookies)
        resistance_tests.append(referrer_test)

        # Calculate resistance score
        resistant_tests = sum(1 for test in resistance_tests if not test.get('vulnerable', True))
        resistance_score = (resistant_tests / len(resistance_tests)) * 100

        print(f"\n📊 Hijacking Resistance Score: {resistance_score:.1f}%")

        self.analysis_results['security_features']['hijacking_resistance'] = {
            'score': resistance_score,
            'tests': resistance_tests
        }

        return resistance_tests

    def test_user_agent_change(self, cookies):
        """Test session with different User-Agent"""
        try:
            session = requests.Session()

            # Add cookies
            for name, value in cookies.items():
                session.cookies.set(name, value, domain='.instagram.com')

            # Use suspicious User-Agent
            session.headers.update({
                'User-Agent': 'SuspiciousBot/1.0 (Hacking Tool)',
                'Accept': '*/*'
            })

            response = session.get("https://www.instagram.com/", timeout=10)

            result = {
                'test': 'user_agent_change',
                'different_ua_accepted': response.status_code == 200,
                'vulnerable': response.status_code == 200,
                'status_code': response.status_code
            }

            if result['vulnerable']:
                print("   ⚠️ Session works with suspicious User-Agent")
                self.analysis_results['vulnerabilities'].append({
                    'type': 'weak_ua_validation',
                    'severity': 'MEDIUM',
                    'description': 'Session accepts requests from suspicious User-Agents'
                })
            else:
                print("   ✅ Session rejects suspicious User-Agents")

            return result

        except Exception as e:
            print(f"   ❌ User-Agent test failed: {e}")
            return {'test': 'user_agent_change', 'error': str(e)}

    def test_ip_change_simulation(self, cookies):
        """Test session with simulated IP change"""
        try:
            session = requests.Session()

            # Add cookies
            for name, value in cookies.items():
                session.cookies.set(name, value, domain='.instagram.com')

            # Add headers to simulate different IP
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'X-Forwarded-For': '1.2.3.4',
                'X-Real-IP': '1.2.3.4',
                'X-Originating-IP': '1.2.3.4'
            })

            response = session.get("https://www.instagram.com/", timeout=10)

            result = {
                'test': 'ip_change_simulation',
                'different_ip_accepted': response.status_code == 200,
                'vulnerable': response.status_code == 200,
                'status_code': response.status_code
            }

            if result['vulnerable']:
                print("   ⚠️ Session works with different IP headers")
            else:
                print("   ✅ Session validates IP consistency")

            return result

        except Exception as e:
            print(f"   ❌ IP change test failed: {e}")
            return {'test': 'ip_change_simulation', 'error': str(e)}

    def test_missing_referrer(self, cookies):
        """Test session without proper referrer"""
        try:
            session = requests.Session()

            # Add cookies
            for name, value in cookies.items():
                session.cookies.set(name, value, domain='.instagram.com')

            # Remove referrer or use suspicious one
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://malicious-site.com/'
            })

            response = session.get("https://www.instagram.com/direct/", timeout=10)

            result = {
                'test': 'missing_referrer',
                'malicious_referrer_accepted': response.status_code == 200,
                'vulnerable': response.status_code == 200,
                'status_code': response.status_code
            }

            if result['vulnerable']:
                print("   ⚠️ Session accepts requests from malicious referrers")
            else:
                print("   ✅ Session validates referrer")

            return result

        except Exception as e:
            print(f"   ❌ Referrer test failed: {e}")
            return {'test': 'missing_referrer', 'error': str(e)}

    def generate_security_recommendations(self):
        """📋 Generate security recommendations"""
        print(f"\n📋 SECURITY RECOMMENDATIONS")
        print(f"============================")

        recommendations = []

        # Based on vulnerabilities found
        for vuln in self.analysis_results['vulnerabilities']:
            if vuln['type'] == 'missing_csrf':
                recommendations.append("🔒 Implement CSRF token validation")
            elif vuln['type'] == 'weak_ua_validation':
                recommendations.append("🕵️ Strengthen User-Agent validation")

        # General recommendations
        recommendations.extend([
            "🔄 Implement regular session rotation",
            "🌐 Use secure cookie flags (Secure, HttpOnly, SameSite)",
            "📍 Consider IP binding for sensitive operations",
            "⏰ Implement proper session timeout",
            "📊 Monitor for suspicious session activity",
            "🔐 Use strong session ID generation",
            "🚫 Implement concurrent session limits"
        ])

        self.analysis_results['recommendations'] = recommendations

        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")

        return recommendations

    def comprehensive_session_analysis(self, session_file=None):
        """🎯 Comprehensive Instagram session security analysis"""
        print(f"\n🎯 COMPREHENSIVE SESSION ANALYSIS")
        print(f"==================================")

        # Load session
        cookies = self.load_instagram_session(session_file)
        if not cookies:
            return None

        # Run all analyses
        cookie_analysis = self.analyze_instagram_cookies(cookies)
        validity_tests = self.test_session_validity(cookies)
        security_features = self.analyze_session_security_features(cookies)
        resistance_tests = self.test_session_hijacking_resistance(cookies)
        recommendations = self.generate_security_recommendations()

        # Compile final report
        final_report = {
            'analysis_timestamp': datetime.now().isoformat(),
            'session_file': session_file,
            'cookie_count': len(cookies),
            'analysis_results': self.analysis_results
        }

        # Save report
        timestamp = int(time.time())
        output_file = f"{self.project_root}/reports/instagram_session_analysis_{timestamp}.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)

        # Print summary
        self.print_analysis_summary()

        print(f"\n✅ ANALYSIS COMPLETED!")
        print(f"📂 Report saved: {output_file}")

        return final_report

    def print_analysis_summary(self):
        """Print analysis summary"""
        print(f"\n📊 ANALYSIS SUMMARY")
        print(f"===================")

        # Session strength
        strength = self.analysis_results.get('session_strength', {})
        if 'overall_score' in strength:
            print(f"🍪 Cookie Security Score: {strength['overall_score']:.1f}%")

        # Session validity
        validity = self.analysis_results.get('security_features', {}).get('session_validity', {})
        if 'score' in validity:
            print(f"🔐 Session Validity Score: {validity['score']:.1f}%")

        # Hijacking resistance
        resistance = self.analysis_results.get('security_features', {}).get('hijacking_resistance', {})
        if 'score' in resistance:
            print(f"🥷 Hijacking Resistance Score: {resistance['score']:.1f}%")

        # Vulnerabilities
        vulns = self.analysis_results.get('vulnerabilities', [])
        print(f"⚠️ Vulnerabilities Found: {len(vulns)}")

        for vuln in vulns:
            print(f"   • {vuln['type']} ({vuln['severity']}): {vuln['description']}")

        # Recommendations
        recs = self.analysis_results.get('recommendations', [])
        print(f"💡 Recommendations: {len(recs)}")

def main():
    """Main analysis function"""
    print("🔥 INSTAGRAM SESSION SECURITY ANALYZER 2025")
    print("=" * 60)
    print("⚠️ FOR AUTHORIZED TESTING OF YOUR OWN SESSIONS ONLY ⚠️")
    print("=" * 60)

    analyzer = InstagramSessionAnalyzer()

    # Run comprehensive analysis
    report = analyzer.comprehensive_session_analysis()

    if report:
        print("\n🎯 Analysis complete!")
        print("📊 Check the generated report for detailed findings")
    else:
        print("\n❌ Analysis failed - check session file")

if __name__ == "__main__":
    main()
