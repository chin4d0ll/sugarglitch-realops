# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Instagram Rate Limit Analyzer
วิเคราะห์และแก้ปัญหา rate limiting แบบ girly hacker 🌸
"""

import time
import json
import random
import asyncio
import aiohttp
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import logging
from datetime import datetime, timedelta

@dataclass
class RateLimitStrategy:
    """🛡️ Strategy สำหรับหลบ rate limit"""
    name: str
    min_delay: float
    max_delay: float
    backoff_multiplier: float
    max_retries: int
    success_rate: float
    description: str

class CuteRateLimitBypass:
    """
    🌸 Cute Rate Limit Bypass
    เทคนิค hacking เพื่อการศึกษา - หลบ Instagram rate limit แบบน่ารักๆ
    """

    def __init__(self, session_file: str = "session-alx.trading"):
        """Initialize CuteRateLimitBypass with default session file"""
        self.session_file = Path(session_file)
        self.logger = self._setup_logger()  # Initialize logger first

        # Check if session file exists
        if not self.session_file.exists():
            self.logger.warning(f"⚠️ Session file {session_file} not found, using fallback mode")
            self.session_data = {}
        else:
            self.session_data = self._load_session()

        # 🎯 Strategies สำหรับหลบ rate limit
        self.strategies = self._init_strategies()
        self.current_strategy = 0

        # 📊 Statistics
        self.request_count = 0
        self.success_count = 0
        self.rate_limit_count = 0
        self.last_request_time = 0

        # 🔄 Advanced rotation
        self.user_agents = self._get_user_agents()
        self.current_ua = 0

        # 🍪 Cookie management
        self.cookies = {}
        self.csrf_token = None

    def _setup_logger(self) -> logging.Logger:
        """📝 Setup cute logger"""
        logger = logging.getLogger("CuteBypass")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '🌸 %(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _load_session(self) -> Dict:
        """🔑 Load session data"""
        try:
            with open(self.session_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Session load error: {e}")
            return {}

    def _init_strategies(self) -> List[RateLimitStrategy]:
        """🎯 Initialize rate limit bypass strategies"""
        return [
            RateLimitStrategy(
                name="🐌 Ultra Slow",
                min_delay = 30.0,
                max_delay = 60.0,
                backoff_multiplier = 2.0,
                max_retries = 10,
                success_rate = 0.9,
                description="ช้าแต่แน่นอน - เหมาะกับการ bypass ที่ต้องการความปลอดภัย"
            ),
            RateLimitStrategy(
                name="🌊 Wave Pattern",
                min_delay = 15.0,
                max_delay = 45.0,
                backoff_multiplier = 1.5,
                max_retries = 8,
                success_rate = 0.7,
                description="รูปแบบคลื่น - เลียนแบบการใช้งานจริงของมนุษย์"
            ),
            RateLimitStrategy(
                name="⚡ Smart Burst",
                min_delay = 5.0,
                max_delay = 25.0,
                backoff_multiplier = 3.0,
                max_retries = 12,
                success_rate = 0.6,
                description="ระเบิดสั้น - เร็วแต่มีความเสี่ยง"
            ),
            RateLimitStrategy(
                name="🎭 Human Mimic",
                min_delay = 8.0,
                max_delay = 35.0,
                backoff_multiplier = 1.8,
                max_retries = 15,
                success_rate = 0.8,
                description="เลียนแบบมนุษย์ - รูปแบบการใช้งานที่เป็นธรรมชาติ"
            )
        ]

    def _get_user_agents(self) -> List[str]:
        """🕵️ User agents สำหรับ rotation"""
        return [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        ]

    def _get_current_strategy(self) -> RateLimitStrategy:
        """🎯 Get current bypass strategy"""
        return self.strategies[self.current_strategy]

    def _rotate_strategy(self):
        """🔄 Rotate to next strategy"""
        self.current_strategy = (self.current_strategy + 1) % len(self.strategies)
        strategy = self._get_current_strategy()
        self.logger.info(f"🔄 Switching to strategy: {strategy.name}")

    def _calculate_smart_delay(self, attempt: int = 1) -> float:
        """🧠 Calculate smart delay based on current situation"""
        strategy = self._get_current_strategy()

        # Base delay from strategy
        base_delay = random.uniform(strategy.min_delay, strategy.max_delay)

        # Adaptive delay based on recent rate limits
        if self.rate_limit_count > 5:
            base_delay *= 1.5

        # Exponential backoff for consecutive failures
        backoff_delay = base_delay * (strategy.backoff_multiplier ** (attempt - 1))

        # Add human-like randomness
        jitter = random.uniform(0.8, 1.3)
        final_delay = backoff_delay * jitter

        # Cap maximum delay
        return min(final_delay, 120.0)

    def _create_headers(self) -> Dict[str, str]:
        """🎭 Create headers with rotation"""
        # Rotate user agent
        self.current_ua = (self.current_ua + 1) % len(self.user_agents)

        headers = {
            'User-Agent': self.user_agents[self.current_ua],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,image/avif,image/webp,*/*;q = 0.8',
            'Accept-Language': 'en-US,en;q = 0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age = 0'
        }

        # Add session cookies
        if 'sessionid' in self.session_data.get('cookies', {}):
            sessionid = self.session_data['cookies']['sessionid']
            headers['Cookie'] = f'sessionid={sessionid}'

        # Add CSRF token if available
        if self.csrf_token:
            headers['X-CSRFToken'] = self.csrf_token

        return headers

    async def cute_request(self, session: aiohttp.ClientSession, url: str,
                          attempt: int = 1) -> Tuple[int, bytes, Dict]:
        """🌸 Make cute request with advanced bypass"""

        # Calculate smart delay
        delay = self._calculate_smart_delay(attempt)

        if attempt > 1:
            self.logger.info(f"😴 Cute sleep for {delay:.1f}s (attempt {attempt})...")
            await asyncio.sleep(delay)

        # Create headers with rotation
        headers = self._create_headers()

        # Add randomness to mimic human behavior
        if random.random() < 0.3:  # 30% chance to add extra delay
            extra_delay = random.uniform(1, 5)
            await asyncio.sleep(extra_delay)

        self.request_count += 1

        try:
            self.logger.info(f"🌟 Cute request #{attempt}: {url}")

            # Use timeout to prevent hanging
            timeout = aiohttp.ClientTimeout(total = 30)

            async with session.get(url, headers = headers, timeout = timeout) as response:
                content = await response.read()

                self.logger.info(f"📊 Response: HTTP {response.status} | {len(content):,} bytes")

                if response.status == 200:
                    self.success_count += 1

                    # Extract CSRF token if it's the homepage
                    if 'instagram.com' in url and not url.endswith('/direct/inbox/'):
                        content_text = content.decode('utf-8', errors='ignore')
                        csrf_match = content_text.find('"csrf_token":"')
                        if csrf_match != -1:
                            csrf_start = csrf_match + 14
                            csrf_end = content_text.find('"', csrf_start)
                            self.csrf_token = content_text[csrf_start:csrf_end]
                            self.logger.info(f"🔑 CSRF updated: {self.csrf_token[:15]}...")

                    return response.status, content, dict(response.headers)

                elif response.status == 429:
                    self.rate_limit_count += 1
                    self.logger.warning(f"🚫 Rate limited! (Total: {self.rate_limit_count})")

                    # Switch strategy if too many rate limits
                    if self.rate_limit_count % 3 == 0:
                        self._rotate_strategy()

                    return response.status, content, dict(response.headers)

                else:
                    self.logger.warning(f"⚠️ Unexpected status: {response.status}")
                    return response.status, content, dict(response.headers)

        except asyncio.TimeoutError:
            self.logger.error("⏰ Request timeout!")
            return 408, b'', {}
        except Exception as e:
            self.logger.error(f"💥 Request error: {e}")
            return 500, b'', {}

    async def bypass_rate_limit(self, url: str, max_attempts: int = 20) -> Tuple[int, bytes, Dict]:
        """🛡️ Main bypass function with multiple strategies"""

        connector = aiohttp.TCPConnector(limit = 1)  # Single connection to be nice
        timeout = aiohttp.ClientTimeout(total = 60)

        async with aiohttp.ClientSession(connector = connector, timeout = timeout) as session:

            for attempt in range(1, max_attempts + 1):
                status, content, headers = await self.cute_request(session, url, attempt)

                if status == 200:
                    success_rate = (self.success_count / self.request_count) * 100
                    self.logger.info(f"✅ Success! Rate: {success_rate:.1f}% ({self.success_count}/{self.request_count})")
                    return status, content, headers

                elif status == 429:
                    strategy = self._get_current_strategy()

                    if attempt >= strategy.max_retries:
                        self.logger.error(f"💀 Max retries reached for {strategy.name}")
                        self._rotate_strategy()
                        continue

                    # Exponential backoff with jitter
                    wait_time = self._calculate_smart_delay(attempt)
                    self.logger.info(f"🚫 Rate limited! Waiting {wait_time:.0f}s...")

                    # Show progress
                    for i in range(int(wait_time)):
                        if i % 5 == 0:
                            remaining = int(wait_time) - i
                            print(f"⏳ {remaining}s remaining...", end='\r')
                        await asyncio.sleep(1)

                    print()  # New line after countdown
                    continue

                else:
                    self.logger.error(f"💥 Failed with status {status}")
                    if attempt < max_attempts:
                        await asyncio.sleep(5)
                        continue
                    break

            self.logger.error("💀 All bypass attempts failed!")
            return 0, b'', {}

    def print_statistics(self):
        """📊 Print bypass statistics"""
        if self.request_count > 0:
            success_rate = (self.success_count / self.request_count) * 100
            rate_limit_rate = (self.rate_limit_count / self.request_count) * 100

            print(f"\n📊 Bypass Statistics:")
            print(f"  🎯 Total Requests: {self.request_count}")
            print(f"  ✅ Successful: {self.success_count} ({success_rate:.1f}%)")
            print(f"  🚫 Rate Limited: {self.rate_limit_count} ({rate_limit_rate:.1f}%)")
            print(f"  🎭 Current Strategy: {self._get_current_strategy().name}")

    def apply_cute_rate_limit(self):
        """🌸 Apply cute rate limiting for synchronous requests"""
        current_time = time.time()

        # Calculate time since last request
        if hasattr(self, 'last_request_time') and self.last_request_time > 0:
            time_since_last = current_time - self.last_request_time

            # Get current strategy
            strategy = self._get_current_strategy()
            min_delay = strategy.min_delay

            # If not enough time has passed, apply cute sleep
            if time_since_last < min_delay:
                sleep_time = min_delay - time_since_last
                sleep_time += random.uniform(0.5, 2.0)  # Add jitter

                self.logger.info(f"😴 Cute sleep for {sleep_time:.2f}s...")
                time.sleep(sleep_time)

        # Update last request time
        self.last_request_time = current_time
        self.request_count += 1

        # Apply adaptive delay if too many requests
        if self.request_count > 10 and self.request_count % 5 == 0:
            adaptive_delay = self._calculate_smart_delay()
            self.logger.info(f"🧠 Adaptive delay: {adaptive_delay:.2f}s")
            time.sleep(adaptive_delay)

    def emergency_cute_sleep(self):
        """🚨 Emergency cute sleep for severe rate limiting"""
        emergency_delay = random.uniform(60, 120)  # 1-2 minutes
        self.logger.warning(f"🚨 Emergency rate limit detected! Sleeping for {emergency_delay:.0f}s...")

        # Show countdown
        for i in range(int(emergency_delay)):
            if i % 10 == 0:
                remaining = int(emergency_delay) - i
                print(f"🚨 Emergency sleep: {remaining}s remaining...", end='\r')
            time.sleep(1)

        print()  # New line after countdown
        self.logger.info("✅ Emergency sleep complete, resuming...")

# 🚀 Main bypass script
async def main():
    """🌸 Main function สำหรับทดสอบ bypass"""
    print("🌸 Instagram Rate Limit Bypass - Educational Purpose")
    print("🛡️ Advanced Hacking Techniques for Learning")
    print("=" * 60)

    # Initialize bypass
    bypass = CuteRateLimitBypass("sessions/session-alx.trading")

    # Test URLs
    test_urls = [
        "https://www.instagram.com/",
        "https://www.instagram.com/direct/inbox/"
    ]

    for url in test_urls:
        print(f"\n🎯 Testing: {url}")
        print("-" * 40)

        status, content, headers = await bypass.bypass_rate_limit(url)

        if status == 200:
            print(f"✅ SUCCESS: {len(content):,} bytes received")
        else:
            print(f"❌ FAILED: Status {status}")

    # Show final statistics
    bypass.print_statistics()

if __name__ == "__main__":
    asyncio.run(main())
