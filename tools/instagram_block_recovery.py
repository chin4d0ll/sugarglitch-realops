# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Instagram Block Recovery Script
Detects and recovers from Instagram IP blocks using proxy rotation and session renewal
"""

import json
import os
import time
import requests
import logging
from typing import Dict, Optional, List, Any, Tuple
from datetime import datetime
import sys

# Import the ProxyRotator from ip_rotation_handler
try:
    from tools.ip_rotation_handler import ProxyRotator
except ImportError:
    try:
        from ip_rotation_handler import ProxyRotator
    except ImportError:
        print("❌ Could not import ProxyRotator from ip_rotation_handler.py")
        print("   Make sure ip_rotation_handler.py is in the same directory or tools/ directory")
        sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
class InstagramBlockRecovery:
    """
    Handles Instagram IP block detection and recovery using proxy rotation
    """

    def __init__(self, session_file: str = "tools/session_alx_trading.json"):
        """
        Initialize the recovery handler

        Args:
            session_file: Path to session JSON file
        """
        self.session_file = session_file
        self.proxy_rotator = ProxyRotator("config/proxies.json")
        self.session_data = None
        self.current_session = None

        # Configuration
        self.max_retry_attempts = 5
        self.retry_delay = 2  # seconds between retries
        self.test_url = "https://www.instagram.com/"
        self.inbox_url = "https://www.instagram.com/direct/inbox/"

        # Block detection patterns
        self.block_status_codes = [403, 429, 401]
        self.block_keywords = [
            "challenge_required",
            "checkpoint_required",
            "rate_limit",
            "blocked",
            "suspicious",
            "verify"
        ]

        self.load_session()

    def load_session(self) -> bool:
        """
        Load session data from JSON file

        Returns:
            bool: True if session loaded successfully
        """
        try:
            if not os.path.exists(self.session_file):
                logger.error(f"❌ Session file not found: {self.session_file}")
                return False

            with open(self.session_file, 'r', encoding='utf-8') as f:
                self.session_data = json.load(f)

            logger.info(f"✅ Loaded session from: {self.session_file}")
            return True

        except Exception as e:
            logger.error(f"❌ Error loading session: {e}")
            return False

    def create_session(self, proxy_url: Optional[str] = None) -> requests.Session:
        """
        Create a requests session with Instagram headers and proxy

        Args:
            proxy_url: Proxy URL to use (optional)

        Returns:
            requests.Session: Configured session
        """
        session = requests.Session()

        # Set proxy if provided
        if proxy_url:
            session.proxies = {
                'http': proxy_url,
                'https': proxy_url
            }

        # Default headers for Instagram
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }

        # Extract User-Agent from session data if available
        if self.session_data:
            # Handle different session data formats
            if isinstance(self.session_data, dict):
                if 'user_agent' in self.session_data:
                    headers['User-Agent'] = self.session_data['user_agent']
                elif 'headers' in self.session_data and 'User-Agent' in self.session_data['headers']:
                    headers['User-Agent'] = self.session_data['headers']['User-Agent']

            # Set cookies from session data
            if isinstance(self.session_data, list):
                # Cookie array format
                for cookie in self.session_data:
                    if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                        session.cookies.set(
                            cookie['name'],
                            cookie['value'],
                            domain=cookie.get('domain', '.instagram.com')
                        )
            elif isinstance(self.session_data, dict):
                # Various dict formats
                if 'cookies' in self.session_data:
                    cookies = self.session_data['cookies']
                    if isinstance(cookies, list):
                        for cookie in cookies:
                            if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                                session.cookies.set(
                                    cookie['name'],
                                    cookie['value'],
                                    domain=cookie.get('domain', '.instagram.com')
                                )
                    elif isinstance(cookies, dict):
                        for name, value in cookies.items():
                            session.cookies.set(name, value, domain='.instagram.com')

                # Direct cookie fields
                if 'sessionid' in self.session_data:
                    session.cookies.set('sessionid', self.session_data['sessionid'], domain='.instagram.com')

        session.headers.update(headers)
        return session

    def is_blocked(self, response: requests.Response) -> bool:
        """
        Check if the response indicates an IP block or challenge

        Args:
            response: HTTP response to check

        Returns:
            bool: True if blocked/challenged
        """
        # Check status codes
        if response.status_code in self.block_status_codes:
            logger.warning(f"🚫 Block detected: HTTP {response.status_code}")
            return True

        # Check response content for block indicators
        try:
            content = response.text.lower()
            for keyword in self.block_keywords:
                if keyword in content:
                    logger.warning(f"🚫 Block detected: Found keyword '{keyword}'")
                    return True
        except Exception:
            pass

        # Check for suspicious redirects
        if response.status_code in [302, 301] and 'challenge' in response.headers.get('Location', '').lower():
            logger.warning("🚫 Block detected: Challenge redirect")
            return True

        return False

    def test_connection(self, proxy_url: Optional[str] = None, timeout: int = 10) -> Tuple[bool, Optional[requests.Response]]:
        """
        Test connection to Instagram with optional proxy

        Args:
            proxy_url: Proxy URL to test (optional)
            timeout: Request timeout in seconds

        Returns:
            tuple: (success, response) - success is True if not blocked
        """
        try:
            session = self.create_session(proxy_url)

            logger.info(f"🧪 Testing connection to Instagram{' via proxy' if proxy_url else ''}...")

            response = session.get(self.test_url, timeout=timeout, allow_redirects=True)

            # Check if blocked
            if self.is_blocked(response):
                return False, response

            # Check if response is successful
            if response.status_code == 200:
                logger.info("✅ Connection test successful")
                return True, response
            else:
                logger.warning(f"⚠️ Unexpected status code: {response.status_code}")
                return False, response

        except requests.exceptions.Timeout:
            logger.warning(f"⏰ Connection timeout{' with proxy' if proxy_url else ''}")
            return False, None
        except requests.exceptions.ProxyError:
            logger.warning(f"🔗 Proxy connection error: {proxy_url}")
            return False, None
        except requests.exceptions.RequestException as e:
            logger.warning(f"❌ Connection error: {e}")
            return False, None
        except Exception as e:
            logger.error(f"💥 Unexpected error: {e}")
            return False, None

    def recover_from_block(self) -> Tuple[bool, Optional[str]]:
        """
        Attempt to recover from IP block using proxy rotation

        Returns:
            tuple: (success, working_proxy_url) - success is True if recovery successful
        """
        logger.info("🔄 Starting Instagram block recovery...")

        # First, test without proxy to confirm block
        success, response = self.test_connection()
        if success:
            logger.info("✅ No block detected - connection is working normally")
            return True, None

        logger.warning("🚫 Confirmed: Instagram access is blocked")

        if not self.proxy_rotator:
            logger.error("❌ No proxy rotator available for recovery")
            return False, None

        # Try recovery with proxy rotation
        for attempt in range(1, self.max_retry_attempts + 1):
            logger.info(f"🔄 Recovery attempt {attempt}/{self.max_retry_attempts}")

            # Get next proxy
            proxy_url = self.proxy_rotator.get_working_proxy()
            if not proxy_url:
                logger.error("❌ No working proxies available")
                break

            # Test connection with proxy
            success, response = self.test_connection(proxy_url)

            if success:
                logger.info(f"✅ Recovered with proxy: {self.proxy_rotator._mask_proxy_url(proxy_url)}")
                return True, proxy_url
            else:
                logger.warning(f"❌ Proxy failed: {self.proxy_rotator._mask_proxy_url(proxy_url)}")
                # ProxyRotator will automatically remove failed proxy

                if attempt < self.max_retry_attempts:
                    logger.info(f"⏳ Waiting {self.retry_delay}s before next attempt...")
                    time.sleep(self.retry_delay)

        logger.error("❌ Recovery failed - all proxies blocked or unavailable")
        return False, None

    def renew_session(self, session_file: str, new_proxy: str) -> bool:
        """
        Renew session cookies using a new proxy

        Args:
            session_file: Path to session file to update
            new_proxy: Proxy URL to use for renewal

        Returns:
            bool: True if session renewed successfully
        """
        logger.info(f"🔄 Attempting to renew session with new proxy...")

        try:
            # Create session with new proxy
            session = self.create_session(new_proxy)

            # Test access to Instagram Direct inbox
            response = session.get(self.inbox_url, timeout=15, allow_redirects=True)

            if response.status_code == 200 and not self.is_blocked(response):
                logger.info("✅ Session renewal successful - updating session file...")

                # Create backup of old session
                backup_file = f"{session_file}.backup.{int(time.time())}"
                if os.path.exists(session_file):
                    os.rename(session_file, backup_file)
                    logger.info(f"💾 Created backup: {backup_file}")

                # Extract updated cookies
                updated_cookies = []
                for cookie in session.cookies:
                    updated_cookies.append({
                        "name": cookie.name,
                        "value": cookie.value,
                        "domain": cookie.domain or ".instagram.com",
                        "path": cookie.path or "/",
                        "expires": -1,
                        "httpOnly": getattr(cookie, 'has_nonstandard_attr', lambda x: False)('HttpOnly'),
                        "secure": cookie.secure,
                        "sameSite": "Lax"
                    })

                # Add session metadata
                session_data = {
                    "cookies": updated_cookies,
                    "renewed_at": datetime.now().isoformat(),
                    "renewed_with_proxy": self.proxy_rotator._mask_proxy_url(new_proxy) if hasattr(self.proxy_rotator, '_mask_proxy_url') else "***masked***",
                    "user_agent": session.headers.get('User-Agent'),
                    "renewal_status": "success"
                }

                # Save updated session
                with open(session_file, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, indent=2, ensure_ascii=False)

                logger.info(f"✅ Session renewed and saved to: {session_file}")
                return True
            else:
                logger.warning(f"❌ Session renewal failed - Status: {response.status_code}")
                if self.is_blocked(response):
                    logger.warning("🚫 New proxy is also blocked")
                return False

        except Exception as e:
            logger.error(f"❌ Error during session renewal: {e}")
            return False

    def full_recovery_process(self) -> Dict[str, Any]:
        """
        Execute complete recovery process: block detection, proxy rotation, and session renewal

        Returns:
            dict: Recovery results and status
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "recovery_successful": False,
            "block_detected": False,
            "proxy_used": None,
            "session_renewed": False,
            "attempts": 0,
            "error": None
        }

        try:
            logger.info("🚀 Starting full Instagram block recovery process...")

            # Step 1: Detect block
            success, response = self.test_connection()
            if success:
                logger.info("✅ No block detected - no recovery needed")
                results["recovery_successful"] = True
                return results

            results["block_detected"] = True
            logger.warning("🚫 Block detected - starting recovery...")

            # Step 2: Recover with proxy rotation
            success, working_proxy = self.recover_from_block()
            results["attempts"] = self.max_retry_attempts

            if not success:
                results["error"] = "All proxies failed or blocked"
                return results

            results["proxy_used"] = working_proxy
            logger.info(f"✅ Recovery successful with proxy")

            # Step 3: Renew session if proxy worked
            if working_proxy:
                session_renewed = self.renew_session(self.session_file, working_proxy)
                results["session_renewed"] = session_renewed

                if session_renewed:
                    logger.info("✅ Session successfully renewed")
                    results["recovery_successful"] = True
                else:
                    logger.warning("⚠️ Proxy works but session renewal failed")
                    results["recovery_successful"] = True  # Proxy still works

            return results

        except Exception as e:
            logger.error(f"💥 Unexpected error in recovery process: {e}")
            results["error"] = str(e)
            return results
def renew_session(session_file: str, new_proxy: str) -> bool:
    """
    Standalone function to renew session cookies using a new proxy

    Args:
        session_file: Path to session file (sessionid + user_agent)
        new_proxy: Proxy URL to use for renewal

    Returns:
        bool: True if session renewed successfully
    """
    recovery = InstagramBlockRecovery(session_file)
    return recovery.renew_session(session_file, new_proxy)
def main():
    """Main function for testing and demo"""
    print("🛡️ Instagram Block Recovery Tool")
    print("=" * 50)

    # Setup logging for demo
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize recovery system
    recovery = InstagramBlockRecovery()

    if not recovery.proxy_rotator:
        print("❌ No proxy rotator available - please check proxy configuration")
        return 1

    print(f"📊 Loaded {len(recovery.proxy_rotator)} proxies")

    # Test 1: Simple connection test
    print("\n🧪 Test 1: Connection Test")
    print("-" * 30)
    success, response = recovery.test_connection()
    print(f"Result: {'✅ Success' if success else '❌ Blocked/Failed'}")

    # Test 2: Proxy rotation test
    print("\n🧪 Test 2: Proxy Rotation Test")
    print("-" * 30)
    if recovery.proxy_rotator:
        proxy = recovery.proxy_rotator.get_working_proxy()
        if proxy:
            success, response = recovery.test_connection(proxy)
            print(f"Proxy: {recovery.proxy_rotator._mask_proxy_url(proxy)}")
            print(f"Result: {'✅ Success' if success else '❌ Failed'}")
        else:
            print("❌ No working proxy available")

    # Test 3: Full recovery process
    print("\n🧪 Test 3: Full Recovery Process")
    print("-" * 30)
    results = recovery.full_recovery_process()

    print(f"Block detected: {'✅' if results['block_detected'] else '❌'}")
    print(f"Recovery successful: {'✅' if results['recovery_successful'] else '❌'}")
    print(f"Proxy used: {results.get('proxy_used', 'None')}")
    print(f"Session renewed: {'✅' if results['session_renewed'] else '❌'}")

    if results.get('error'):
        print(f"Error: {results['error']}")

    # Test 4: Standalone session renewal function
    print("\n🧪 Test 4: Standalone Session Renewal")
    print("-" * 30)

    if recovery.proxy_rotator:
        test_proxy = recovery.proxy_rotator.get_next_proxy()
        if test_proxy:
            success = renew_session("tools/session_alx_trading.json", test_proxy)
            print(f"Session renewal: {'✅ Success' if success else '❌ Failed'}")
        else:
            print("❌ No proxy available for session renewal test")

    return 0
if __name__ == "__main__":
    exit(main())
