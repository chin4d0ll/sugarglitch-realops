# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 GitHub Codespace Instagram Troubleshooter
แก้ปัญหาการรันใน Codespace + Instagram connection สำหรับ chin4d0ll
"""

import os
import sys
import subprocess
import json
import asyncio
import aiohttp
import requests
import socket
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
import time
import random

class CodespaceTroubleshooter:
    """
    🛠️ Troubleshooter สำหรับ GitHub Codespace
    แก้ปัญหาการเชื่อมต่อและการรัน Instagram extractor
    """

    def __init__(self):
        self.logger = self._setup_logger()
        self.environment_info = {}

    def _setup_logger(self) -> logging.Logger:
        """📝 Setup logger สำหรับ debugging"""
        logger = logging.getLogger("CodespaceFixer")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '🌸 %(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def check_codespace_environment(self) -> Dict[str, Any]:
        """🔍 ตรวจสอบ Codespace environment"""
        self.logger.info("🔍 Checking Codespace environment...")

        env_info = {
            'is_codespace': os.environ.get('CODESPACES', False),
            'codespace_name': os.environ.get('CODESPACE_NAME', 'Unknown'),
            'github_user': os.environ.get('GITHUB_USER', 'Unknown'),
            'python_version': sys.version,
            'working_directory': os.getcwd(),
            'available_memory': self._get_memory_info(),
            'network_access': self._test_network_access(),
            'installed_packages': self._get_installed_packages()
        }

        self.environment_info = env_info
        return env_info

    def _get_memory_info(self) -> str:
        """💾 ดูข้อมูล memory"""
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if 'MemTotal' in line:
                        mem_kb = int(line.split()[1])
                        mem_gb = mem_kb / 1024 / 1024
                        return f"{mem_gb:.1f} GB"
        except Exception:
            return "Unknown"
        return "Unknown"

    def _test_network_access(self) -> Dict[str, bool]:
        """🌐 ทดสอบการเชื่อมต่อ network"""
        network_tests = {
            'google': self._ping_host('google.com'),
            'instagram': self._ping_host('instagram.com'),
            'github': self._ping_host('github.com'),
            'dns_resolution': self._test_dns()
        }
        return network_tests

    def _ping_host(self, host: str) -> bool:
        """🏓 Ping host เพื่อทดสอบการเชื่อมต่อ"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '3', host],
                capture_output = True,
                text = True,
                timeout = 5
            )
            return result.returncode == 0
        except Exception:
            return False

    def _test_dns(self) -> bool:
        """🔍 ทดสอบ DNS resolution"""
        try:
            import socket
            socket.gethostbyname('google.com')
            return True
        except Exception:
            return False

    def _get_installed_packages(self) -> List[str]:
        """📦 ดูรายการ packages ที่ติดตั้งแล้ว"""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list'],
                capture_output = True,
                text = True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[2:]  # Skip headers
                packages = [line.split()[0] for line in lines if line.strip()]
                return packages
        except Exception:
            pass
        return []

    def install_required_packages(self) -> bool:
        """📋 ติดตั้ง packages ที่จำเป็น"""
        self.logger.info("📋 Installing required packages...")

        required_packages = [
            'aiohttp>=3.8.0',
            'aiofiles>=23.0.0',
            'requests>=2.28.0',
            'beautifulsoup4>=4.11.0',
            'lxml>=4.9.0'
        ]

        try:
            for package in required_packages:
                self.logger.info(f"📦 Installing {package}...")
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', package],
                    capture_output = True,
                    text = True
                )

                if result.returncode != 0:
                    self.logger.error(f"❌ Failed to install {package}")
                    self.logger.error(result.stderr)
                    return False

            self.logger.info("✅ All packages installed successfully!")
            return True

        except Exception as e:
            self.logger.error(f"💥 Installation error: {e}")
            return False

    def create_codespace_compatible_extractor(self) -> None:
        """🛠️ สร้าง extractor ที่ทำงานใน Codespace ได้"""

        extractor_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 Codespace-Compatible Instagram DM Extractor
สำหรับ chin4d0ll - ทำงานใน GitHub Codespace ได้แน่นอน
"""

import asyncio
import aiohttp
import json
import time
import random
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging

class CodespaceInstagramExtractor:
    """
    🌸 Instagram DM Extractor ที่ทำงานใน Codespace ได้
    เน้นความเสถียรและการจัดการ network ที่ดี
    """

    def __init__(self, session_file: str = "session-alx.trading"):
        self.session_file = Path(session_file)
        self.logger = self._setup_logger()
        self.session_data = {}
        self.request_count = 0
        self.success_count = 0

        # 🛡️ Conservative settings สำหรับ Codespace
        self.base_delay = 30.0  # 30 วินาที base delay
        self.max_delay = 120.0  # สูงสุด 2 นาที
        self.max_retries = 15
        self.timeout = 60  # 1 นาที timeout

        self._load_session()

    def _setup_logger(self) -> logging.Logger:
        """📝 Setup logger"""
        logger = logging.getLogger("CodespaceExtractor")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '🌸 %(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _load_session(self) -> None:
        """🔑 Load session data"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    self.session_data = json.load(f)
                    self.logger.info("✅ Session loaded successfully")

                    # Log session info (safely)
                    if 'cookies' in self.session_data:
                        sessionid = self.session_data['cookies'].get('sessionid', '')
                        if sessionid:
                            masked_id = sessionid[:10] + '...' + sessionid[-10:]
                            self.logger.info(f"🍪 Session ID: {masked_id}")
            else:
                self.logger.error(f"❌ Session file not found: {self.session_file}")

        except Exception as e:
            self.logger.error(f"💥 Session load error: {e}")

    def _create_headers(self) -> Dict[str, str]:
        """🎭 Create HTTP headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,image/avif,image/webp,*/*;q = 0.8',
            'Accept-Language': 'en-US,en;q = 0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        }

        # Add cookies if available
        if 'cookies' in self.session_data:
            cookies = []
            for name, value in self.session_data['cookies'].items():
                cookies.append(f"{name}={value}")
            if cookies:
                headers['Cookie'] = '; '.join(cookies)

        return headers

    async def _safe_request(self, session: aiohttp.ClientSession, url: str,
                           attempt: int = 1) -> Tuple[int, str]:
        """🛡️ Make safe HTTP request"""

        # Progressive delay
        if attempt > 1:
            delay = min(self.base_delay * (1.5 ** (attempt - 1)), self.max_delay)
            self.logger.info(f"😴 Waiting {delay:.1f}s before attempt {attempt}...")

            # Show countdown for long delays
            if delay > 20:
                for remaining in range(int(delay), 0, -5):
                    print(f"⏳ {remaining}s remaining...", end='\\r')
                    await asyncio.sleep(min(5, remaining))
                print()
            else:
                await asyncio.sleep(delay)

        # Add random jitter
        jitter = random.uniform(1, 5)
        await asyncio.sleep(jitter)

        headers = self._create_headers()
        self.request_count += 1

        try:
            self.logger.info(f"🌟 Request #{self.request_count} (attempt {attempt}): {url}")

            # Use conservative timeout
            timeout = aiohttp.ClientTimeout(total = self.timeout)

            async with session.get(url, headers = headers, timeout = timeout, ssl = False) as response:
                content = await response.text()

                self.logger.info(f"📊 Response: HTTP {response.status} | {len(content):,} chars")

                if response.status == 200:
                    self.success_count += 1
                    self.logger.info(f"✅ Success! ({self.success_count}/{self.request_count})")

                return response.status, content

        except asyncio.TimeoutError:
            self.logger.error("⏰ Request timeout!")
            return 408, ""
        except Exception as e:
            self.logger.error(f"💥 Request error: {e}")
            return 500, ""

    async def _persistent_request(self, session: aiohttp.ClientSession, url: str) -> Tuple[int, str]:
        """🔄 Persistent request with retry logic"""

        for attempt in range(1, self.max_retries + 1):
            status, content = await self._safe_request(session, url, attempt)

            if status == 200:
                return status, content
            elif status == 429:
                self.logger.warning(f"🚫 Rate limited on attempt {attempt}")
                continue
            elif status in [500, 502, 503, 504]:
                self.logger.warning(f"🔄 Server error {status}, retrying...")
                continue
            else:
                self.logger.warning(f"⚠️ Status {status} on attempt {attempt}")
                if attempt < self.max_retries:
                    await asyncio.sleep(10)
                    continue

        self.logger.error(f"💀 All {self.max_retries} attempts failed!")
        return 0, ""

    async def test_connectivity(self) -> bool:
        """🔍 Test basic connectivity"""
        self.logger.info("🔍 Testing connectivity...")

        # Conservative connector settings
        connector = aiohttp.TCPConnector(
            limit = 1,
            limit_per_host = 1,
            ttl_dns_cache = 300,
            use_dns_cache = True,
            keepalive_timeout = 30,
            enable_cleanup_closed = True
        )

        timeout = aiohttp.ClientTimeout(total = 60)

        async with aiohttp.ClientSession(connector = connector, timeout = timeout) as session:

            # Test basic connectivity
            test_urls = [
                "https://httpbin.org/get",
                "https://www.google.com",
                "https://www.instagram.com"
            ]

            for url in test_urls:
                self.logger.info(f"🌐 Testing {url}...")
                status, content = await self._safe_request(session, url)

                if status == 200:
                    self.logger.info(f"✅ {url} accessible")
                else:
                    self.logger.warning(f"❌ {url} failed (status: {status})")

            return True

    async def extract_instagram_data(self) -> Dict[str, Any]:
        """📱 Extract Instagram data"""
        self.logger.info("🌸 Starting Instagram data extraction...")

        if not self.session_data:
            self.logger.error("❌ No session data available")
            return {'error': 'No session data'}

        # Conservative connector for Codespace
        connector = aiohttp.TCPConnector(
            limit = 1,
            limit_per_host = 1,
            ttl_dns_cache = 600,
            use_dns_cache = True,
            keepalive_timeout = 60
        )

        timeout = aiohttp.ClientTimeout(total = 120)

        async with aiohttp.ClientSession(connector = connector, timeout = timeout) as session:

            # Step 1: Access Instagram homepage
            self.logger.info("🏠 Accessing Instagram homepage...")
            status, content = await self._persistent_request(session, "https://www.instagram.com/")

            if status != 200:
                return {'error': f'Homepage access failed: {status}'}

            self.logger.info("✅ Homepage accessible!")

            # Step 2: Try to access direct messages
            self.logger.info("📬 Trying to access DMs...")
            status, dm_content = await self._persistent_request(session, "https://www.instagram.com/direct/inbox/")

            result = {
                'timestamp': int(time.time()),
                'homepage_status': 200,
                'homepage_size': len(content),
                'dm_status': status,
                'dm_size': len(dm_content) if dm_content else 0,
                'total_requests': self.request_count,
                'successful_requests': self.success_count,
                'success_rate': (self.success_count / max(self.request_count, 1)) * 100
            }

            if status == 200:
                self.logger.info("✅ DM access successful!")
                result['dm_access'] = 'success'

                # Try to extract some basic info
                if 'direct' in dm_content:
                    result['contains_dm_data'] = True
                    result['dm_content_preview'] = dm_content[:500] + "..." if len(dm_content) > 500 else dm_content

            else:
                self.logger.warning(f"⚠️ DM access failed with status {status}")
                result['dm_access'] = 'failed'

            return result

    async def save_results(self, data: Dict[str, Any]) -> None:
        """💾 Save extraction results"""

        # Create data directory
        data_dir = Path("data")
        data_dir.mkdir(exist_ok = True)

        # Generate filename with timestamp
        timestamp = int(time.time())
        filename = f"codespace_extraction_{timestamp}.json"
        filepath = data_dir / filename

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii = False, indent = 2)

            self.logger.info(f"✅ Results saved to: {filepath}")

            # Also save a latest.json for easy access
            latest_filepath = data_dir / "latest.json"
            with open(latest_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii = False, indent = 2)

            self.logger.info(f"✅ Latest results: {latest_filepath}")

        except Exception as e:
            self.logger.error(f"💥 Save error: {e}")

async def main():
    """🚀 Main function สำหรับ Codespace"""
    print("🌸 Instagram DM Extractor for GitHub Codespace")
    print("🛡️ Optimized for Codespace Environment")
    print("💖 Made with love for chin4d0ll")
    print("=" * 60)

    try:
        # Create extractor
        extractor = CodespaceInstagramExtractor()

        # Test connectivity first
        await extractor.test_connectivity()

        # Extract data
        results = await extractor.extract_instagram_data()

        # Save results
        await extractor.save_results(results)

        # Print summary
        print("\\n🎉 Extraction Summary:")
        print(f"📊 Total Requests: {results.get('total_requests', 0)}")
        print(f"✅ Success Rate: {results.get('success_rate', 0):.1f}%")
        print(f"🏠 Homepage: {results.get('homepage_status', 'N/A')}")
        print(f"📬 DM Access: {results.get('dm_access', 'N/A')}")

        if results.get('dm_access') == 'success':
            print("🎯 DM data extraction successful!")
        else:
            print("⚠️ DM access limited, but homepage data extracted")

    except KeyboardInterrupt:
        print("\\n🛑 Extraction interrupted by user")
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ensure we have the right event loop policy for Codespace
    if sys.platform.startswith('linux'):
        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except ImportError:
            pass

    asyncio.run(main())
'''

        # Save the extractor
        filepath = Path("codespace_instagram_extractor.py")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(extractor_code)

        # Make it executable
        os.chmod(filepath, 0o755)

        self.logger.info(f"✅ Codespace-compatible extractor created: {filepath}")

    def print_diagnostics(self) -> None:
        """📊 Print diagnostic information"""
        env_info = self.check_codespace_environment()

        print("🌸 GitHub Codespace Diagnostics")
        print("=" * 50)

        print(f"🏠 Environment:")
        print(f"  Is Codespace: {env_info['is_codespace']}")
        print(f"  Codespace Name: {env_info['codespace_name']}")
        print(f"  GitHub User: {env_info['github_user']}")
        print(f"  Working Dir: {env_info['working_directory']}")
        print(f"  Memory: {env_info['available_memory']}")

        print(f"\n🐍 Python:")
        print(f"  Version: {env_info['python_version'].split()[0]}")
        print(f"  Packages: {len(env_info['installed_packages'])} installed")

        print(f"\n🌐 Network:")
        network = env_info['network_access']
        for service, status in network.items():
            icon = "✅" if status else "❌"
            print(f"  {service}: {icon}")

        # Check for required packages
        required = ['aiohttp', 'aiofiles', 'requests']
        installed = env_info['installed_packages']

        print(f"\n📦 Required Packages:")
        for package in required:
            if package in installed:
                print(f"  {package}: ✅")
            else:
                print(f"  {package}: ❌ (need to install)")

def main():
    """🚀 Main troubleshooter function"""
    print("🌸 GitHub Codespace Troubleshooter for chin4d0ll")
    print("🛠️ แก้ปัญหาการรันใน Codespace")
    print("=" * 60)

    troubleshooter = CodespaceTroubleshooter()

    # Run diagnostics
    troubleshooter.print_diagnostics()

    # Install packages if needed
    print("\n📋 Installing required packages...")
    if troubleshooter.install_required_packages():
        print("✅ Package installation completed!")
    else:
        print("❌ Package installation failed!")
        return

    # Create Codespace-compatible extractor
    print("\n🛠️ Creating Codespace-compatible extractor...")
    troubleshooter.create_codespace_compatible_extractor()

    print("\n🎉 Setup Complete!")
    print("🚀 Now you can run:")
    print("    python3 codespace_instagram_extractor.py")

if __name__ == "__main__":
    main()
