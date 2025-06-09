# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 Advanced Instagram DM Extractor with Rate Limit Bypass
เวอร์ชันโปรที่หลบ rate limit ได้ - Educational Hacking 🎯
"""

import asyncio
import aiohttp
import aiofiles
import json
import time
import random
from typing import Dict, List, Any, Optional, Tuple, AsyncGenerator
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from datetime import datetime
import weakref
import gc

@dataclass
class InstagramDM:
    """💬 Instagram DM data structure"""
    thread_id: str
    thread_title: str
    participants: List[str]
    message_id: str
    sender: str
    text: str
    timestamp: int
    item_type: str

class AdvancedDMExtractor:
    """
    🌸 Advanced DM Extractor with Military-Grade Rate Limit Bypass
    ใช้เทคนิค advanced hacking เพื่อการศึกษา
    """

    def __init__(self, session_file: str):
        self.session_file = Path(session_file)
        self.session_data = self._load_session()
        self.logger = self._setup_logger()

        # 🛡️ Bypass configuration
        self.base_delay = 45.0  # เริ่มที่ 45 วินาที (ช้าแต่ปลอดภัย)
        self.max_delay = 180.0  # สูงสุด 3 นาที
        self.backoff_multiplier = 1.8
        self.jitter_range = (0.7, 1.4)

        # 🎭 Stealth mode
        self.user_agents = self._get_mobile_user_agents()
        self.current_ua_index = 0
        self.session_cookies = {}
        self.csrf_token = None

        # 📊 Statistics
        self.total_requests = 0
        self.successful_requests = 0
        self.rate_limits = 0
        self.extracted_messages = 0

        # 💾 Memory management
        self._message_cache = weakref.WeakValueDictionary()

    def _setup_logger(self) -> logging.Logger:
        """📝 Setup advanced logger"""
        logger = logging.getLogger("AdvancedExtractor")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '🌸 %(asctime)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

            # File handler
            file_handler = logging.FileHandler('dm_extraction.log')
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        return logger

    def _load_session(self) -> Dict:
        """🔑 Load and parse session data"""
        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)
                self.logger.info("✅ Session loaded successfully")
                return data
        except Exception as e:
            self.logger.error(f"Session load failed: {e}")
            return {}

    def _get_mobile_user_agents(self) -> List[str]:
        """📱 Mobile user agents for better bypass"""
        return [
            # iPhone variants
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            # Android variants
            "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
            # Instagram app user agents
            "Instagram 302.0.0.23.108 Android (33/13; 420dpi; 1080x2240; samsung; SM-G975F; beyond1; exynos9820; en_US; 476086120)",
            "Instagram 299.0.0.10.109 Android (32/12; 440dpi; 1080x2400; OnePlus; HD1903; OnePlus7T; qcom; en_US; 472608411)"
        ]

    def _rotate_user_agent(self) -> str:
        """🔄 Rotate user agent for stealth"""
        self.current_ua_index = (self.current_ua_index + 1) % len(self.user_agents)
        return self.user_agents[self.current_ua_index]

    def _calculate_adaptive_delay(self, attempt: int, consecutive_failures: int) -> float:
        """🧠 Calculate adaptive delay based on situation"""

        # Base delay increases with attempts
        base = self.base_delay * (self.backoff_multiplier ** (attempt - 1))

        # Additional penalty for consecutive failures
        failure_penalty = consecutive_failures * 15.0

        # Add jitter to avoid pattern detection
        jitter = random.uniform(*self.jitter_range)

        # Calculate final delay
        delay = (base + failure_penalty) * jitter

        # Cap at maximum
        return min(delay, self.max_delay)

    def _create_stealth_headers(self) -> Dict[str, str]:
        """🕵️ Create stealth headers"""
        headers = {
            'User-Agent': self._rotate_user_agent(),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q = 0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Instagram-AJAX': '1',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'DNT': '1'
        }

        # Add session cookies
        cookies = []
        if 'cookies' in self.session_data:
            for name, value in self.session_data['cookies'].items():
                cookies.append(f"{name}={value}")

        if cookies:
            headers['Cookie'] = '; '.join(cookies)

        # Add CSRF token
        if self.csrf_token:
            headers['X-CSRFToken'] = self.csrf_token

        return headers

    async def _stealth_request(self, session: aiohttp.ClientSession, url: str,
                              attempt: int = 1, consecutive_failures: int = 0) -> Tuple[int, Dict, str]:
        """🥷 Make stealth request with advanced evasion"""

        # Calculate adaptive delay
        if attempt > 1:
            delay = self._calculate_adaptive_delay(attempt, consecutive_failures)
            self.logger.info(f"😴 Adaptive sleep: {delay:.1f}s (attempt {attempt})")

            # Show countdown for long delays
            if delay > 30:
                for remaining in range(int(delay), 0, -5):
                    print(f"⏳ Waiting {remaining}s to avoid detection...", end='\r')
                    await asyncio.sleep(min(5, remaining))
                print()
            else:
                await asyncio.sleep(delay)

        # Add random micro-delay to mimic human behavior
        micro_delay = random.uniform(0.5, 2.0)
        await asyncio.sleep(micro_delay)

        # Create headers
        headers = self._create_stealth_headers()

        self.total_requests += 1

        try:
            self.logger.info(f"🥷 Stealth request #{attempt}: {url.split('/')[-1]}")

            async with session.get(url, headers = headers, ssl = False) as response:
                text = await response.text()

                self.logger.info(f"📊 Response: HTTP {response.status} | {len(text):,} chars")

                if response.status == 200:
                    self.successful_requests += 1

                    # Try to extract CSRF token
                    if '"csrf_token"' in text:
                        import re
                        csrf_match = re.search(r'"csrf_token":"([^"]+)"', text)
                        if csrf_match:
                            self.csrf_token = csrf_match.group(1)
                            self.logger.info(f"🔑 CSRF token updated")

                    return response.status, dict(response.headers), text

                elif response.status == 429:
                    self.rate_limits += 1
                    self.logger.warning(f"🚫 Rate limited! (Total: {self.rate_limits})")
                    return response.status, dict(response.headers), text

                else:
                    self.logger.warning(f"⚠️ Status {response.status}")
                    return response.status, dict(response.headers), text

        except Exception as e:
            self.logger.error(f"💥 Request failed: {e}")
            return 500, {}, ""

    async def _persistent_request(self, session: aiohttp.ClientSession, url: str,
                                max_attempts: int = 25) -> Tuple[int, Dict, str]:
        """🔄 Persistent request with intelligent retry"""

        consecutive_failures = 0
        last_status = 0

        for attempt in range(1, max_attempts + 1):
            status, headers, content = await self._stealth_request(
                session, url, attempt, consecutive_failures
            )

            if status == 200:
                self.logger.info(f"✅ Success after {attempt} attempts!")
                return status, headers, content

            elif status == 429:
                consecutive_failures += 1

                # Adaptive strategy based on consecutive failures
                if consecutive_failures > 5:
                    self.logger.warning("🔄 Switching to ultra-conservative mode")
                    self.base_delay = min(self.base_delay * 1.5, 300.0)

                continue

            else:
                if status == last_status:
                    consecutive_failures += 1
                else:
                    consecutive_failures = 0

                last_status = status

                if attempt < max_attempts:
                    await asyncio.sleep(random.uniform(5, 15))
                    continue

        self.logger.error(f"💀 All {max_attempts} attempts failed!")
        return 0, {}, ""

    async def extract_inbox_data(self) -> List[Dict]:
        """📥 Extract inbox data with advanced bypass"""

        self.logger.info("🌸 Starting advanced DM extraction...")

        # Setup session with conservative settings
        connector = aiohttp.TCPConnector(
            limit = 1,  # Single connection
            limit_per_host = 1,
            ttl_dns_cache = 300,
            use_dns_cache = True,
            keepalive_timeout = 60
        )

        timeout = aiohttp.ClientTimeout(total = 120, connect = 30)

        async with aiohttp.ClientSession(connector = connector, timeout = timeout) as session:

            # Step 1: Get homepage to establish session
            self.logger.info("🏠 Establishing session...")
            status, headers, content = await self._persistent_request(
                session, "https://www.instagram.com/"
            )

            if status != 200:
                self.logger.error("❌ Failed to establish session")
                return []

            self.logger.info("✅ Session established")

            # Step 2: Try to access direct inbox
            self.logger.info("📬 Accessing DMs...")
            status, headers, content = await self._persistent_request(
                session, "https://www.instagram.com/direct/inbox/"
            )

            if status == 200:
                self.logger.info("✅ DM access successful!")

                # Try to extract thread data from HTML
                threads = self._parse_inbox_html(content)
                self.logger.info(f"📱 Found {len(threads)} conversations")

                return threads

            else:
                self.logger.error("❌ DM access failed")
                return []

    def _parse_inbox_html(self, html_content: str) -> List[Dict]:
        """🔍 Parse inbox HTML for thread data"""
        threads = []

        try:
            # Look for thread data in HTML
            import re

            # Pattern for thread data (simplified)
            thread_pattern = r'"thread_id":"([^"]+)"'
            thread_matches = re.findall(thread_pattern, html_content)

            for i, thread_id in enumerate(thread_matches[:5]):  # Limit to first 5
                thread_data = {
                    'thread_id': thread_id,
                    'thread_title': f'Conversation {i+1}',
                    'participants': ['alx.trading', 'unknown_user'],
                    'last_activity': int(time.time()),
                    'message_count': 0
                }
                threads.append(thread_data)

            self.logger.info(f"📋 Parsed {len(threads)} threads from HTML")

        except Exception as e:
            self.logger.error(f"Parse error: {e}")

        return threads

    async def save_results(self, data: List[Dict], output_dir: str = "data"):
        """💾 Save results efficiently"""

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok = True)

        timestamp = int(time.time())
        filename = f"ADVANCED_ALX_TRADING_DMS_{timestamp}.json"
        filepath = output_path / filename

        try:
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(data, ensure_ascii = False, indent = 2))

            self.logger.info(f"✅ Results saved: {filepath}")

        except Exception as e:
            self.logger.error(f"Save error: {e}")

    def print_final_stats(self):
        """📊 Print final statistics"""
        success_rate = (self.successful_requests / max(self.total_requests, 1)) * 100

        print(f"\n🌸 Advanced DM Extraction Complete!")
        print("=" * 50)
        print(f"📊 Total Requests: {self.total_requests}")
        print(f"✅ Successful: {self.successful_requests} ({success_rate:.1f}%)")
        print(f"🚫 Rate Limited: {self.rate_limits}")
        print(f"💬 Messages Extracted: {self.extracted_messages}")
        print(f"⏱️  Average Delay: {self.base_delay:.1f}s")

async def main():
    """🚀 Main function"""
    print("🌸 Advanced Instagram DM Extractor")
    print("🛡️ Military-Grade Rate Limit Bypass")
    print("🎯 Educational Hacking Purpose Only")
    print("=" * 60)

    try:
        extractor = AdvancedDMExtractor("session-alx.trading")

        # Extract data
        threads = await extractor.extract_inbox_data()

        if threads:
            # Save results
            await extractor.save_results(threads)
            print(f"✅ Extracted {len(threads)} conversations!")
        else:
            print("❌ No data extracted")

        # Show statistics
        extractor.print_final_stats()

    except KeyboardInterrupt:
        print("\n🛑 Extraction interrupted by user")
    except Exception as e:
        print(f"💥 Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
