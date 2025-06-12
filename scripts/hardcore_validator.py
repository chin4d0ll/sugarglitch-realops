# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
HARDCORE SESSION & PROXY VALIDATOR
==================================
Validates Instagram sessions and proxy connections
"""

import aiohttp
import asyncio
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class HardcoreValidator:
    """Validates sessions and proxies for hardcore extraction"""

    def __init__(self):
        self.session_files = [
            "/workspaces/sugarglitch-realops/tools/session_alx_trading.json",
            "/workspaces/sugarglitch-realops/config/sessions.json"
        ]
        self.proxy_files = [
            "/workspaces/sugarglitch-realops/config/proxy_config.json",
            "/workspaces/sugarglitch-realops/config/real_proxy_config.json"
        ]

    async def validate_instagram_session(self, session_id: str, proxy: Optional[str] = None) -> Dict:
        """Validate Instagram session"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,image/webp,*/*;q = 0.8',
            'Accept-Language': 'en-US,en;q = 0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': f'sessionid={session_id}',
            'Referer': 'https://www.instagram.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        result = {
            "session_id": session_id[:10] + "...",
            "valid": False,
            "user_info": None,
            "error": None,
            "response_time": 0,
            "proxy_used": proxy
        }

        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test with Instagram homepage
                async with session.get(
                    "https://www.instagram.com/",
                    headers = headers,
                    proxy = proxy,
                    timeout = aiohttp.ClientTimeout(total = 30)
                ) as response:

                    result["response_time"] = time.time() - start_time

                    if response.status == 200:
                        text = await response.text()

                        # Check if logged in (not seeing login form)
                        if 'window._sharedData' in text and '"is_logged_in":true' in text:
                            result["valid"] = True

                            # Try to extract user info
                            try:
                                import re
                                user_match = re.search(r'"username":"([^"]+)"', text)
                                if user_match:
                                    result["user_info"] = {"username": user_match.group(1)}
                            except Exception:
                                pass

                        elif 'Login • Instagram' in text or 'login' in text.lower():
                            result["error"] = "Session expired - redirected to login"
                        else:
                            result["error"] = "Unknown response format"

                    elif response.status == 429:
                        result["error"] = f"Rate limited (HTTP {response.status})"
                    elif response.status >= 400:
                        result["error"] = f"HTTP {response.status}"
                    else:
                        result["error"] = f"Unexpected status: {response.status}"

        except asyncio.TimeoutError:
            result["error"] = "Request timeout"
        except Exception as e:
            result["error"] = str(e)

        return result

    async def test_proxy(self, proxy_url: str) -> Dict:
        """Test proxy connection"""
        result = {
            "proxy": proxy_url,
            "working": False,
            "ip_address": None,
            "country": None,
            "response_time": 0,
            "error": None
        }

        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test with httpbin
                async with session.get(
                    "https://httpbin.org/ip",
                    proxy = proxy_url,
                    timeout = aiohttp.ClientTimeout(total = 15)
                ) as response:

                    result["response_time"] = time.time() - start_time

                    if response.status == 200:
                        data = await response.json()
                        result["working"] = True
                        result["ip_address"] = data.get("origin")

                        # Try to get country info
                        try:
                            async with session.get(
                                f"https://httpbin.org/ip",
                                proxy = proxy_url,
                                timeout = aiohttp.ClientTimeout(total = 10)
                            ) as geo_response:
                                if geo_response.status == 200:
                                    geo_data = await geo_response.json()
                                    result["country"] = geo_data.get("country", "Unknown")
                        except Exception:
                            pass

                    else:
                        result["error"] = f"HTTP {response.status}"

        except asyncio.TimeoutError:
            result["error"] = "Connection timeout"
        except Exception as e:
            result["error"] = str(e)

        return result

    def load_sessions(self) -> List[Dict]:
        """Load all sessions from files"""
        sessions = []

        for file_path in self.session_files:
            try:
                if Path(file_path).exists():
                    with open(file_path, 'r') as f:
                        data = json.load(f)

                        if "sessionid" in data:
                            sessions.append({
                                "sessionid": data["sessionid"],
                                "username": data.get("username", "unknown"),
                                "source": file_path
                            })
                        elif "sessions" in data:
                            for session in data["sessions"]:
                                sessions.append({
                                    "sessionid": session["sessionid"],
                                    "username": session.get("username", "unknown"),
                                    "source": file_path
                                })
            except Exception as e:
                print(f"⚠️ Failed to load sessions from {file_path}: {e}")

        return sessions

    def load_proxies(self) -> List[str]:
        """Load all proxies from files"""
        proxies = []

        # Add Bright Data proxy examples
        brightdata_proxies = [
            "http://brd-customer-hl_12345678-zone-zone1:your_password@brd-customer-hl_12345678-zone-zone1.brd.superproxy.io:22225",
            "http://brd-customer-hl_12345678-zone-datacenter:your_password@brd-customer-hl_12345678-zone-datacenter.brd.superproxy.io:22225"
        ]
        proxies.extend(brightdata_proxies)

        # Load from config files
        for file_path in self.proxy_files:
            try:
                if Path(file_path).exists():
                    with open(file_path, 'r') as f:
                        data = json.load(f)

                        if "proxies" in data:
                            for proxy in data["proxies"]:
                                proxy_url = f"{proxy.get('protocol', 'http')}://"
                                if proxy.get('username') and proxy.get('password'):
                                    proxy_url += f"{proxy['username']}:{proxy['password']}@"
                                proxy_url += f"{proxy['host']}:{proxy['port']}"
                                proxies.append(proxy_url)

                        elif "brightdata" in data:
                            bd = data["brightdata"]
                            proxy_url = f"http://{bd['username']}:{bd['password']}@{bd['host']}:{bd['port']}"
                            proxies.append(proxy_url)

            except Exception as e:
                print(f"⚠️ Failed to load proxies from {file_path}: {e}")

        return proxies

    async def validate_all_sessions(self) -> List[Dict]:
        """Validate all loaded sessions"""
        sessions = self.load_sessions()

        if not sessions:
            print("❌ No sessions found to validate")
            return []

        print(f"🔍 Validating {len(sessions)} sessions...")

        results = []
        for i, session in enumerate(sessions):
            print(f"  [{i+1}/{len(sessions)}] Testing {session['username']}...")

            result = await self.validate_instagram_session(session["sessionid"])
            result["username"] = session["username"]
            result["source"] = session["source"]

            results.append(result)

            # Brief delay between requests
            await asyncio.sleep(1)

        return results

    async def test_all_proxies(self) -> List[Dict]:
        """Test all loaded proxies"""
        proxies = self.load_proxies()

        if not proxies:
            print("❌ No proxies found to test")
            return []

        print(f"🔍 Testing {len(proxies)} proxies...")

        results = []
        for i, proxy in enumerate(proxies):
            print(f"  [{i+1}/{len(proxies)}] Testing {proxy[:50]}...")

            result = await self.test_proxy(proxy)
            results.append(result)

            # Brief delay between requests
            await asyncio.sleep(0.5)

        return results

    def print_session_results(self, results: List[Dict]):
        """Print session validation results"""
        print("\n" + "="*70)
        print("📱 SESSION VALIDATION RESULTS")
        print("="*70)

        valid_count = 0
        for result in results:
            status = "✅ VALID" if result["valid"] else "❌ INVALID"
            username = result.get("username", "unknown")
            error = result.get("error", "")
            response_time = result.get("response_time", 0)

            print(f"{status} | {username:15} | {response_time:.2f}s | {error}")

            if result["valid"]:
                valid_count += 1
                if result.get("user_info"):
                    print(f"         User: {result['user_info']}")

        print(f"\n📊 Summary: {valid_count}/{len(results)} sessions valid ({valid_count/len(results)*100:.1f}%)")

    def print_proxy_results(self, results: List[Dict]):
        """Print proxy test results"""
        print("\n" + "="*70)
        print("🌐 PROXY TEST RESULTS")
        print("="*70)

        working_count = 0
        for result in results:
            status = "✅ WORKING" if result["working"] else "❌ FAILED"
            proxy = result["proxy"][:40] + "..." if len(result["proxy"]) > 40 else result["proxy"]
            response_time = result.get("response_time", 0)
            error = result.get("error", "")
            ip = result.get("ip_address", "")

            print(f"{status} | {proxy:35} | {response_time:.2f}s | {ip or '':15} | {error}")

            if result["working"]:
                working_count += 1

        print(f"\n📊 Summary: {working_count}/{len(results)} proxies working ({working_count/len(results)*100:.1f}%)")

    async def full_validation(self):
        """Run full validation of sessions and proxies"""
        print("🔥🔥🔥 HARDCORE VALIDATION SUITE 🔥🔥🔥")
        print("=" * 70)
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Validate sessions
        session_results = await self.validate_all_sessions()
        if session_results:
            self.print_session_results(session_results)

        # Test proxies
        proxy_results = await self.test_all_proxies()
        if proxy_results:
            self.print_proxy_results(proxy_results)

        # Save results
        report = {
            "timestamp": datetime.now().isoformat(),
            "session_results": session_results,
            "proxy_results": proxy_results,
            "summary": {
                "valid_sessions": len([r for r in session_results if r["valid"]]),
                "total_sessions": len(session_results),
                "working_proxies": len([r for r in proxy_results if r["working"]]),
                "total_proxies": len(proxy_results)
            }
        }

        report_file = f"/workspaces/sugarglitch-realops/data/validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent = 2)

        print(f"\n💾 Validation report saved: {report_file}")
        print("🎯 Ready for hardcore extraction!")

async def main():
    """Main validation function"""
    validator = HardcoreValidator()
    await validator.full_validation()

if __name__ == "__main__":
    asyncio.run(main())
