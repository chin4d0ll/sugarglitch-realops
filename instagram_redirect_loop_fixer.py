# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Instagram Redirect Loop Fixer
แก้ปัญหา redirect loop ใน Instagram สำหรับ chin4d0ll
"""

import requests
import json
import time
import random
from pathlib import Path
from urllib.parse import urllib.parse as urlparse, parse_qs
from typing import Dict, List, Any, Optional

class InstagramRedirectFixer:
    """🔄 Fixer สำหรับ Instagram redirect loops"""

    def __init__(self, session_file: str = "sessions/session-alx.trading"):
        self.session_file = Path(session_file)
        self.session_data = {}
        self.cookies = {}
        self._load_session()

        # ⚡ Optimized settings
        self.max_redirects = 5  # ลด redirects
        self.timeout = 45

        # 🛡️ Anti-detection headers
        self.headers = self._create_stealth_headers()

    def _load_session(self):
        """🔑 Load session with validation"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    self.session_data = json.load(f)
                    self.cookies = self.session_data.get('cookies', {})
                print(f"✅ Session loaded: {len(self.cookies)} cookies")

                # Validate important cookies
                important_cookies = ['sessionid', 'csrftoken', 'ds_user_id']
                missing = [c for c in important_cookies if c not in self.cookies]
                if missing:
                    print(f"⚠️ Missing cookies: {missing}")
                else:
                    print("🔑 All important cookies present")
            else:
                print(f"❌ Session file not found: {self.session_file}")
        except Exception as e:
            print(f"💥 Session load error: {e}")

    def _create_stealth_headers(self) -> Dict[str, str]:
        """🥷 Create stealth headers to avoid detection"""
        return {
            # Mobile user agent (works better than desktop)
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',

            # Proper accept headers
            'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,image/webp,image/apng,*/*;q = 0.8,application/signed-exchange;v = b3;q = 0.7',
            'Accept-Language': 'en-US,en;q = 0.9',
            'Accept-Encoding': 'gzip, deflate, br',

            # Security headers
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',

            # Connection settings
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age = 0',

            # Instagram-specific (to avoid redirects)
            'X-Requested-With': 'XMLHttpRequest',
            'X-Instagram-AJAX': '1',
            'X-IG-App-ID': '936619743392459',  # Instagram web app ID
        }

    def _add_session_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """🔐 Add session-specific headers"""
        enhanced_headers = headers.copy()

        # Add cookies as header string
        if self.cookies:
            cookie_string = '; '.join([f"{k}={v}" for k, v in self.cookies.items()])
            enhanced_headers['Cookie'] = cookie_string

        # Add CSRF token if available
        if 'csrftoken' in self.cookies:
            enhanced_headers['X-CSRFToken'] = self.cookies['csrftoken']

        return enhanced_headers

    def test_redirect_behavior(self, url: str, name: str) -> Dict[str, Any]:
        """🔍 Test redirect behavior for a specific URL"""
        print(f"\n🔍 Testing {name}: {url}")

        # Create session with custom settings
        session = requests.Session()
        session.max_redirects = self.max_redirects

        # Prepare headers
        headers = self._add_session_headers(self.headers)

        try:
            # Track redirects manually
            response = session.get(
                url,
                headers = headers,
                timeout = self.timeout,
                allow_redirects = True,  # Let it handle redirects
                stream = False  # Don't stream to avoid timeout
            )

            result = {
                'name': name,
                'url': url,
                'final_url': response.url,
                'status_code': response.status_code,
                'redirected': response.url != url,
                'redirect_count': len(response.history),
                'content_length': len(response.text),
                'success': response.status_code == 200,
                'headers': dict(response.headers),
            }

            # Analyze redirects
            if response.history:
                print(f"  🔄 Redirects: {len(response.history)}")
                for i, redirect in enumerate(response.history, 1):
                    print(f"    {i}. {redirect.status_code}: {redirect.url}")
                print(f"  🎯 Final URL: {response.url}")

            # Status
            if response.status_code == 200:
                print(f"  ✅ SUCCESS: HTTP {response.status_code} | {len(response.text):,} chars")

                # Check content type
                content_type = response.headers.get('content-type', '')
                if 'html' in content_type.lower():
                    print(f"  📄 Content: HTML page")

                    # Look for Instagram indicators
                    content_lower = response.text.lower()
                    if 'instagram' in content_lower:
                        print(f"  🎯 Instagram content detected")
                    if 'login' in content_lower:
                        print(f"  🔑 Login page detected")
                    if 'direct' in content_lower or 'inbox' in content_lower:
                        print(f"  📬 DM content detected")

            else:
                print(f"  ❌ FAILED: HTTP {response.status_code}")

            result['content_preview'] = response.text[:500] + "..." if len(response.text) > 500 else response.text

            return result

        except requests.exceptions.TooManyRedirects:
            print(f"  🔄 TOO MANY REDIRECTS (>{self.max_redirects})")
            return {
                'name': name,
                'url': url,
                'error': 'too_many_redirects',
                'success': False
            }
        except requests.exceptions.Timeout:
            print(f"  ⏰ TIMEOUT (>{self.timeout}s)")
            return {
                'name': name,
                'url': url,
                'error': 'timeout',
                'success': False
            }
        except Exception as e:
            print(f"  💥 ERROR: {e}")
            return {
                'name': name,
                'url': url,
                'error': str(e),
                'success': False
            }

    def try_alternative_endpoints(self) -> Dict[str, Any]:
        """🎯 Try alternative Instagram endpoints"""
        print("🎯 Testing alternative Instagram endpoints...")

        # Different endpoints to try
        endpoints = [
            ('homepage', 'https://www.instagram.com/'),
            ('homepage_no_slash', 'https://www.instagram.com'),
            ('explore', 'https://www.instagram.com/explore/'),
            ('accounts', 'https://www.instagram.com/accounts/'),
            ('accounts_login', 'https://www.instagram.com/accounts/login/'),
            ('direct_inbox', 'https://www.instagram.com/direct/inbox/'),
            ('direct', 'https://www.instagram.com/direct/'),

            # API endpoints
            ('api_v1', 'https://i.instagram.com/api/v1/'),
            ('graphql', 'https://www.instagram.com/graphql/query/'),

            # Mobile endpoints
            ('mobile', 'https://m.instagram.com/'),
            ('mobile_direct', 'https://m.instagram.com/direct/'),
        ]

        results = {}

        for name, url in endpoints:
            result = self.test_redirect_behavior(url, name)
            results[name] = result

            # Small delay between tests
            time.sleep(random.uniform(2, 4))

        return results

    def analyze_redirect_patterns(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """📊 Analyze redirect patterns"""
        print("\n📊 Analyzing redirect patterns...")

        analysis = {
            'total_tests': len(results),
            'successful': [],
            'failed': [],
            'redirect_loops': [],
            'timeouts': [],
            'common_redirect_targets': {},
            'working_endpoints': []
        }

        for name, result in results.items():
            if result.get('success', False):
                analysis['successful'].append(name)
                analysis['working_endpoints'].append({
                    'name': name,
                    'url': result['url'],
                    'final_url': result.get('final_url', result['url']),
                    'redirects': result.get('redirect_count', 0)
                })
            else:
                analysis['failed'].append(name)

                error = result.get('error', 'unknown')
                if 'redirect' in error:
                    analysis['redirect_loops'].append(name)
                elif 'timeout' in error:
                    analysis['timeouts'].append(name)

            # Track redirect targets
            final_url = result.get('final_url')
            if final_url:
                domain = urlparse(final_url).netloc
                analysis['common_redirect_targets'][domain] = analysis['common_redirect_targets'].get(domain, 0) + 1

        return analysis

    def generate_redirect_fix_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """💡 Generate recommendations to fix redirect issues"""
        recommendations = []

        success_rate = len(analysis['successful']) / analysis['total_tests'] * 100

        if success_rate > 50:
            recommendations.append("✅ Good news: Some endpoints work!")

            # Recommend working endpoints
            for endpoint in analysis['working_endpoints']:
                recommendations.append(f"🎯 Use: {endpoint['name']} ({endpoint['url']})")

        if analysis['redirect_loops']:
            recommendations.extend([
                "🔄 Redirect loop fixes:",
                "  📱 Try mobile endpoints (m.instagram.com)",
                "  🛡️ Add more anti-detection headers",
                "  🔐 Verify session cookies are valid",
                "  ⚡ Use shorter redirect limits",
                "  🌐 Try different IP/proxy"
            ])

        if analysis['timeouts']:
            recommendations.extend([
                "⏰ Timeout fixes:",
                "  🚀 Increase timeout duration",
                "  ⚡ Use faster network connection",
                "  🎯 Focus on working endpoints only"
            ])

        if not analysis['successful']:
            recommendations.extend([
                "🚫 All endpoints failed:",
                "  🔑 Session might be completely expired",
                "  🌐 Network/IP might be blocked",
                "  🛡️ Instagram might be detecting automation",
                "  💻 Try from different environment"
            ])

        return recommendations

    def save_results(self, results: Dict[str, Any], analysis: Dict[str, Any]) -> None:
        """💾 Save test results"""
        timestamp = int(time.time())

        # Create data directory
        data_dir = Path("data")
        data_dir.mkdir(exist_ok = True)

        # Save detailed results
        results_file = data_dir / f"redirect_test_results_{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': timestamp,
                'results': results,
                'analysis': analysis
            }, f, ensure_ascii = False, indent = 2)

        print(f"✅ Results saved to: {results_file}")

        # Save working endpoints list
        if analysis['working_endpoints']:
            working_file = data_dir / f"working_endpoints_{timestamp}.txt"
            with open(working_file, 'w') as f:
                f.write("🎯 Working Instagram Endpoints\n")
                f.write("=" * 40 + "\n\n")
                for endpoint in analysis['working_endpoints']:
                    f.write(f"{endpoint['name']}: {endpoint['url']}\n")
                    f.write(f"  Final URL: {endpoint['final_url']}\n")
                    f.write(f"  Redirects: {endpoint['redirects']}\n\n")

            print(f"✅ Working endpoints saved to: {working_file}")

    def run_redirect_diagnosis(self) -> None:
        """🚀 Run complete redirect diagnosis"""
        print("🌸 Instagram Redirect Loop Diagnosis")
        print("💖 Advanced troubleshooting for chin4d0ll")
        print("=" * 50)

        if not self.cookies:
            print("⚠️ No session cookies found - some tests may fail")

        # Test endpoints
        results = self.try_alternative_endpoints()

        # Analyze results
        analysis = self.analyze_redirect_patterns(results)

        # Print summary
        print(f"\n📊 SUMMARY:")
        print(f"  Total tests: {analysis['total_tests']}")
        print(f"  Successful: {len(analysis['successful'])} ✅")
        print(f"  Failed: {len(analysis['failed'])} ❌")
        print(f"  Redirect loops: {len(analysis['redirect_loops'])} 🔄")
        print(f"  Timeouts: {len(analysis['timeouts'])} ⏰")

        # Working endpoints
        if analysis['working_endpoints']:
            print(f"\n🎯 WORKING ENDPOINTS:")
            for endpoint in analysis['working_endpoints']:
                print(f"  ✅ {endpoint['name']}: {endpoint['url']}")

        # Generate recommendations
        recommendations = self.generate_redirect_fix_recommendations(analysis)

        print(f"\n💡 RECOMMENDATIONS:")
        for rec in recommendations:
            print(f"  {rec}")

        # Save results
        self.save_results(results, analysis)

        return analysis

def main():
    """🚀 Main function"""
    print("🔄 Instagram Redirect Loop Fixer")
    print("💖 Made with love for chin4d0ll")
    print("🎯 Educational purposes only")
    print()

    try:
        fixer = InstagramRedirectFixer()
        analysis = fixer.run_redirect_diagnosis()

        print("\n🌟 Diagnosis complete!")

        if analysis['working_endpoints']:
            print("🎉 Found working endpoints! You can use these for extraction")
        else:
            print("😢 No working endpoints found. Check recommendations above")

    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
