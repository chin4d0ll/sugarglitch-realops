# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 ALX Trading Targeted DM Extractor
แก้ปัญหา HTTP 500 และดึง DM จาก alx.trading โดยตรง
💖 Optimized for chin4d0ll
"""

import asyncio
import aiohttp
import json
import time
import random
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import hashlib

class ALXTradingExtractor:
    """
    💖 Specialized extractor for alx.trading account
    """

    def __init__(self, session_file: str = "sessions/session-alx.trading"):
        self.session_file = Path(session_file)
        self.logger = self._setup_logger()
        self.session_data = {}
        self.target_username = "alx.trading"

        # 🎯 ALX Trading specific settings
        self.user_agents = [
            # Mobile first - Instagram loves mobile
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            # Instagram app user agents
            "Instagram 312.0.0.37.103 Android (34/14; 420dpi; 1080x2340; samsung; SM-G998B; o1s; exynos2100; en_US; 123456789)"
        ]

        # ⚡ Conservative settings to avoid 500 errors
        self.base_delay = 30.0
        self.max_retries = 10
        self.current_ua_index = 0

        # 📊 Statistics
        self.total_requests = 0
        self.successful_requests = 0
        self.error_500_count = 0

        self._load_session()

    def _setup_logger(self) -> logging.Logger:
        """💖 Setup girly logger"""
        logger = logging.getLogger("ALXExtractor")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('🌸 %(asctime)s - %(message)s 💖')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _load_session(self) -> None:
        """🔑 Load session for alx.trading"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    self.session_data = json.load(f)

                if self._validate_session():
                    self.logger.info("✅ ALX Trading session loaded successfully! 💕")
                else:
                    self.logger.warning("⚠️ Session validation failed for alx.trading")
            else:
                self.logger.error(f"❌ Session file not found: {self.session_file}")

        except Exception as e:
            self.logger.error(f"💥 Session load error: {e}")

    def _validate_session(self) -> bool:
        """🔍 Validate ALX Trading session"""
        if not isinstance(self.session_data, dict) or 'cookies' not in self.session_data:
            return False

        cookies = self.session_data['cookies']
        required_cookies = ['sessionid', 'csrftoken']

        for cookie in required_cookies:
            if cookie not in cookies or len(cookies[cookie]) < 10:
                self.logger.warning(f"Missing or invalid {cookie}")
                return False

        return True

    def _create_mobile_headers(self, url: str = "https://www.instagram.com/") -> Dict[str, str]:
        """📱 Create mobile-optimized headers to avoid 500 errors"""

        # Rotate user agent
        self.current_ua_index = (self.current_ua_index + 1) % len(self.user_agents)
        user_agent = self.user_agents[self.current_ua_index]

        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'DNT': '1'
        }

        # Add mobile-specific headers
        if 'iPhone' in user_agent:
            headers.update({
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"iOS"'
            })
        elif 'Android' in user_agent:
            headers.update({
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"'
            })

        # Add referer for non-homepage requests
        if url != "https://www.instagram.com/":
            headers['Referer'] = 'https://www.instagram.com/'

        # Add session cookies
        if 'cookies' in self.session_data:
            cookies = []
            for name, value in self.session_data['cookies'].items():
                cookies.append(f"{name}={value}")

            if cookies:
                headers['Cookie'] = '; '.join(cookies)

        return headers

    async def _safe_request(self, session: aiohttp.ClientSession, url: str,
                           attempt: int = 1) -> Tuple[int, str, Dict]:
        """🛡️ Safe request with 500 error handling"""

        self.total_requests += 1

        # Progressive delay
        if attempt > 1:
            delay = self.base_delay * (1.5 ** (attempt - 1))
            delay = min(delay, 180.0)  # Cap at 3 minutes

            self.logger.info(f"😴 Waiting {delay:.1f}s before attempt {attempt} 💤")
            await asyncio.sleep(delay)

        # Add micro-delay for human-like behavior
        await asyncio.sleep(random.uniform(2.0, 5.0))

        headers = self._create_mobile_headers(url)

        try:
            self.logger.info(f"🎯 Request #{self.total_requests} (attempt {attempt}): {url.split('/')[-1] or 'homepage'}")

            timeout = aiohttp.ClientTimeout(total=60)

            async with session.get(url, headers=headers, timeout=timeout, ssl=False) as response:
                content = await response.text()

                status_emoji = "✅" if response.status == 200 else "❌"
                self.logger.info(f"{status_emoji} HTTP {response.status} | {len(content):,} chars")

                if response.status == 200:
                    self.successful_requests += 1
                elif response.status == 500:
                    self.error_500_count += 1
                    self.logger.warning(f"🚫 Server Error 500! Total: {self.error_500_count}")

                return response.status, content, dict(response.headers)

        except asyncio.TimeoutError:
            self.logger.error("⏰ Request timeout")
            return 408, "", {}
        except Exception as e:
            self.logger.error(f"💥 Request error: {e}")
            return 500, "", {}

    async def _persistent_request(self, session: aiohttp.ClientSession, url: str) -> Tuple[int, str, Dict]:
        """🔄 Persistent request with retry logic"""

        for attempt in range(1, self.max_retries + 1):
            status, content, headers = await self._safe_request(session, url, attempt)

            if status == 200:
                success_rate = (self.successful_requests / self.total_requests) * 100
                self.logger.info(f"🎉 SUCCESS! Rate: {success_rate:.1f}% 💖")
                return status, content, headers

            elif status == 500:
                if attempt < self.max_retries:
                    self.logger.warning(f"🔄 Retrying after 500 error (attempt {attempt}/{self.max_retries})")
                    # Switch to more mobile user agent after 500 error
                    if attempt >= 3:
                        self.current_ua_index = 0  # Use iPhone UA
                    continue
                else:
                    self.logger.error("💀 Max retries reached for 500 errors")
                    break

            elif status in [429, 403]:
                self.logger.warning(f"🚫 Rate limited or forbidden: {status}")
                if attempt < self.max_retries:
                    # Long delay for rate limiting
                    await asyncio.sleep(120)
                    continue
                else:
                    break

            else:
                self.logger.warning(f"⚠️ Unexpected status: {status}")
                if attempt < self.max_retries:
                    await asyncio.sleep(30)
                    continue
                else:
                    break

        return status, content, headers

    async def test_alx_trading_access(self) -> Dict[str, Any]:
        """🎯 Test access to alx.trading Instagram profile"""

        self.logger.info("🌸 Starting ALX Trading access test 💖")

        if not self.session_data:
            return {'error': 'No session data for alx.trading'}

        # Ultra-simple connector to avoid issues
        connector = aiohttp.TCPConnector(
            limit=1,
            limit_per_host=1,
            keepalive_timeout=60,
            enable_cleanup_closed=True
        )

        timeout = aiohttp.ClientTimeout(total=90)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:

            test_results = {}

            # Test URLs specifically for alx.trading
            test_urls = [
                ("homepage", "https://www.instagram.com/"),
                ("alx_profile", f"https://www.instagram.com/{self.target_username}/"),
                ("direct_inbox", "https://www.instagram.com/direct/inbox/"),
                ("alx_messages", f"https://www.instagram.com/direct/t/")  # Base DM URL
            ]

            for test_name, url in test_urls:
                self.logger.info(f"🎯 Testing {test_name}: {url}")

                status, content, headers = await self._persistent_request(session, url)

                # Analyze content for ALX Trading specific elements
                analysis = self._analyze_response(content, test_name)

                test_results[test_name] = {
                    'url': url,
                    'status': status,
                    'success': status == 200,
                    'content_length': len(content),
                    'analysis': analysis,
                    'timestamp': datetime.now().isoformat()
                }

                # Rest between tests
                if test_name != test_urls[-1][0]:
                    rest_time = random.uniform(20, 40)
                    self.logger.info(f"😴 Resting {rest_time:.1f}s between tests 💤")
                    await asyncio.sleep(rest_time)

            # Compile results
            final_results = {
                'target': self.target_username,
                'timestamp': datetime.now().isoformat(),
                'session_valid': self._validate_session(),
                'total_requests': self.total_requests,
                'successful_requests': self.successful_requests,
                'error_500_count': self.error_500_count,
                'success_rate': (self.successful_requests / max(self.total_requests, 1)) * 100,
                'tests': test_results,
                'recommendations': self._generate_alx_recommendations()
            }

            return final_results

    def _analyze_response(self, content: str, test_type: str) -> Dict[str, Any]:
        """🔍 Analyze response content for ALX Trading specific info"""

        analysis = {
            'contains_alx_trading': False,
            'has_dm_interface': False,
            'login_required': False,
            'rate_limited': False,
            'content_type': 'unknown'
        }

        if not content:
            return analysis

        content_lower = content.lower()

        # Check for ALX Trading mentions
        if 'alx.trading' in content_lower or 'alxtrading' in content_lower:
            analysis['contains_alx_trading'] = True

        # Check for DM interface elements
        dm_indicators = ['direct', 'messages', 'conversation', 'inbox', 'thread']
        if any(indicator in content_lower for indicator in dm_indicators):
            analysis['has_dm_interface'] = True

        # Check for login requirement
        login_indicators = ['login', 'log in', 'sign in', 'authentication']
        if any(indicator in content_lower for indicator in login_indicators):
            analysis['login_required'] = True

        # Check for rate limiting
        if 'rate limit' in content_lower or 'too many requests' in content_lower:
            analysis['rate_limited'] = True

        # Determine content type
        if '<html' in content_lower:
            analysis['content_type'] = 'html'
        elif content.strip().startswith('{') or content.strip().startswith('['):
            analysis['content_type'] = 'json'
        elif 'error' in content_lower:
            analysis['content_type'] = 'error'

        return analysis

    def _generate_alx_recommendations(self) -> List[str]:
        """💡 Generate ALX Trading specific recommendations"""
        recommendations = []

        if self.error_500_count > 0:
            recommendations.extend([
                "🔧 Use mobile user agent exclusively (iPhone/Android)",
                "⏰ Increase delays between requests (30+ seconds)",
                "🔄 Try accessing during different times of day",
                "📱 Consider using Instagram mobile app headers"
            ])

        if self.successful_requests == 0:
            recommendations.extend([
                "🔑 Verify alx.trading session is still valid",
                "🌐 Check network connectivity to Instagram",
                "🛡️ Try using VPN or different IP address",
                "📞 Contact alx.trading for fresh session data"
            ])

        success_rate = (self.successful_requests / max(self.total_requests, 1)) * 100
        if success_rate < 50:
            recommendations.extend([
                "🐌 Reduce request frequency significantly",
                "🎭 Rotate between different user agents",
                "⏳ Implement exponential backoff delays",
                "🔐 Refresh session cookies if possible"
            ])

        return recommendations

    async def extract_alx_trading_dms(self) -> Dict[str, Any]:
        """💖 Extract DMs specifically from alx.trading account"""

        self.logger.info("🎯 Starting ALX Trading DM extraction 💕")

        # First test access
        access_test = await self.test_alx_trading_access()

        if access_test.get('success_rate', 0) < 50:
            self.logger.warning("⚠️ Low success rate, aborting DM extraction")
            return {
                'error': 'Access test failed',
                'access_test_results': access_test,
                'recommendation': 'Fix access issues first'
            }

        # If access test passes, proceed with DM extraction
        self.logger.info("✅ Access test passed, proceeding with DM extraction")

        connector = aiohttp.TCPConnector(limit=1, limit_per_host=1)
        timeout = aiohttp.ClientTimeout(total=120)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:

            # DM extraction endpoints
            dm_urls = [
                "https://www.instagram.com/direct/inbox/",
                "https://www.instagram.com/api/v1/direct_v2/inbox/",
                f"https://www.instagram.com/direct/t/"
            ]

            dm_results = {}

            for i, url in enumerate(dm_urls):
                self.logger.info(f"📨 Extracting DMs from endpoint {i+1}/{len(dm_urls)}")

                status, content, headers = await self._persistent_request(session, url)

                if status == 200 and content:
                    # Parse DM data
                    dm_data = self._parse_dm_content(content, url)
                    dm_results[f"endpoint_{i+1}"] = {
                        'url': url,
                        'status': status,
                        'dm_count': len(dm_data.get('messages', [])),
                        'conversations': dm_data.get('conversations', []),
                        'messages': dm_data.get('messages', [])
                    }
                else:
                    dm_results[f"endpoint_{i+1}"] = {
                        'url': url,
                        'status': status,
                        'error': 'Failed to retrieve DM data'
                    }

                # Long delay between DM requests
                if i < len(dm_urls) - 1:
                    await asyncio.sleep(random.uniform(45, 75))

            # Save results
            extraction_results = {
                'target': self.target_username,
                'timestamp': datetime.now().isoformat(),
                'access_test': access_test,
                'dm_extraction': dm_results,
                'total_requests': self.total_requests,
                'success_rate': (self.successful_requests / max(self.total_requests, 1)) * 100
            }

            await self._save_results(extraction_results)

            return extraction_results

    def _parse_dm_content(self, content: str, url: str) -> Dict[str, Any]:
        """📨 Parse DM content from Instagram response"""

        dm_data = {
            'messages': [],
            'conversations': [],
            'metadata': {}
        }

        try:
            # Try parsing as JSON first
            if content.strip().startswith('{'):
                json_data = json.loads(content)
                if 'inbox' in json_data:
                    dm_data['conversations'] = json_data['inbox'].get('threads', [])
                elif 'messages' in json_data:
                    dm_data['messages'] = json_data['messages']

            # Parse HTML for DM elements
            elif '<html' in content.lower():
                # Look for DM-related data in HTML
                import re

                # Extract JSON data from HTML
                json_matches = re.findall(r'window\._sharedData\s*=\s*({.*?});', content)
                for match in json_matches:
                    try:
                        shared_data = json.loads(match)
                        if 'entry_data' in shared_data:
                            dm_data['metadata'] = shared_data['entry_data']
                    except Exception:
                        pass

                # Look for message threads
                thread_matches = re.findall(r'thread_id["\s:]+([^"\\,}]+)', content)
                if thread_matches:
                    dm_data['conversations'] = [{'thread_id': tid} for tid in thread_matches[:10]]

        except Exception as e:
            self.logger.warning(f"⚠️ DM parsing error: {e}")

        return dm_data

    async def _save_results(self, results: Dict[str, Any]) -> None:
        """💾 Save ALX Trading extraction results"""

        # Create data directory
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        # Save detailed results
        timestamp = int(time.time())
        results_file = data_dir / f"alx_trading_extraction_{timestamp}.json"

        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        # Save summary
        summary_file = data_dir / f"alx_trading_summary_{timestamp}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("🌸 ALX Trading DM Extraction Results 🌸\n")
            f.write("=" * 50 + "\n\n")

            f.write(f"🎯 Target: {results['target']}\n")
            f.write(f"📅 Timestamp: {results['timestamp']}\n")
            f.write(f"📊 Total Requests: {results['total_requests']}\n")
            f.write(f"✅ Success Rate: {results['success_rate']:.1f}%\n\n")

            if 'dm_extraction' in results:
                f.write("📨 DM Extraction Results:\n")
                for endpoint, data in results['dm_extraction'].items():
                    status = "✅" if data.get('status') == 200 else "❌"
                    f.write(f"  {endpoint}: {status} (HTTP {data.get('status', 'N/A')})\n")
                    if 'dm_count' in data:
                        f.write(f"    Messages found: {data['dm_count']}\n")

        self.logger.info(f"✅ Results saved: {results_file} 💖")

async def main():
    """🚀 Main function for ALX Trading extraction"""
    print("🌸 ALX Trading Targeted DM Extractor")
    print("💖 Specialized for alx.trading account")
    print("🎯 Educational and troubleshooting purposes only")
    print("=" * 60)

    try:
        extractor = ALXTradingExtractor()

        # Run extraction
        results = await extractor.extract_alx_trading_dms()

        # Print summary
        print("\n🎉 Extraction Complete!")
        print("=" * 40)

        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            if 'recommendation' in results:
                print(f"💡 Recommendation: {results['recommendation']}")
        else:
            print(f"📊 Total Requests: {results['total_requests']}")
            print(f"✅ Success Rate: {results['success_rate']:.1f}%")

            if 'dm_extraction' in results:
                print("\n📨 DM Extraction Results:")
                for endpoint, data in results['dm_extraction'].items():
                    status = "✅" if data.get('status') == 200 else "❌"
                    print(f"  {endpoint}: {status}")
                    if 'dm_count' in data:
                        print(f"    Messages: {data['dm_count']}")

    except KeyboardInterrupt:
        print("\n🛑 Extraction interrupted by user")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")

if __name__ == "__main__":
    # Run with optimized event loop
    if sys.platform.startswith('linux'):
        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except ImportError:
            pass

    asyncio.run(main())
