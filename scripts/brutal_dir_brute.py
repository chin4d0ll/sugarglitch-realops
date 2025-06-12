# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💥 Directory Brute-forcer โหดๆ แบบ Async
เร็วกว่า dirb/gobuster หลายเท่า!
"""
import asyncio
import aiohttp
import time
from pathlib import Path

class BrutalDirBrute:
    def __init__(self, target_url, wordlist_path, threads=50):
        self.target_url = target_url.rstrip('/')
        self.wordlist_path = wordlist_path
        self.threads = threads
        self.found_dirs = []
        self.session = None

    async def check_directory(self, directory):
        """เช็คไดเรกทอรี่แบบ async - เร็วมากกก"""
        url = f"{self.target_url}/{directory}"

        try:
            async with self.session.get(url, timeout=5) as response:
                if response.status == 200:
                    size = len(await response.text())
                    self.found_dirs.append({
                        'url': url,
                        'status': response.status,
                        'size': size
                    })
                    print(f"✅ Found: {url} [Status: {response.status}] [Size: {size}]")

                elif response.status == 403:
                    # 403 = Forbidden แต่ไดเรกทอรี่มีอยู่จริง!
                    self.found_dirs.append({
                        'url': url,
                        'status': response.status,
                        'size': 0
                    })
                    print(f"🔒 Forbidden: {url} [Status: {response.status}]")

        except asyncio.TimeoutError:
            pass  # เงียบๆ เพื่อความเร็ว
        except Exception:
            pass

    async def run_bruteforce(self):
        """รันการ brute-force แบบ async"""
        print(f"🚀 Starting directory brute-force on {self.target_url}")

        # อ่าน wordlist
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                directories = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌ Wordlist not found: {self.wordlist_path}")
            return

        print(f"📋 Loaded {len(directories)} directories from wordlist")
        print(f"🔥 Using {self.threads} concurrent connections")

        # สร้าง session แบบประหยัดเมมโมรี่
        connector = aiohttp.TCPConnector(limit=self.threads)
        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        ) as session:
            self.session = session

            start_time = time.time()

            # สร้าง semaphore เพื่อจำกัดจำนวน concurrent requests
            semaphore = asyncio.Semaphore(self.threads)

            async def bounded_check(directory):
                async with semaphore:
                    await self.check_directory(directory)

            # รัน tasks ทั้งหมดพร้อมกัน
            tasks = [bounded_check(directory) for directory in directories]
            await asyncio.gather(*tasks, return_exceptions=True)

            end_time = time.time()

        print(f"\n🎉 Brute-force completed in {end_time - start_time:.2f} seconds")
        print(f"📁 Found {len(self.found_dirs)} directories:")

        # แสดงผลลัพธ์
        for result in sorted(self.found_dirs, key=lambda x: x['status']):
            status_emoji = "✅" if result['status'] == 200 else "🔒"
            print(f"   {status_emoji} {result['url']} [{result['status']}] [{result['size']} bytes]")

# 🔥 สร้าง wordlist เบสิค
def create_basic_wordlist():
    basic_dirs = [
        "admin", "administrator", "login", "portal", "dashboard",
        "wp-admin", "phpmyadmin", "cpanel", "webmail", "mail",
        "ftp", "ssh", "telnet", "backup", "backups", "old",
        "test", "testing", "dev", "development", "staging",
        "api", "v1", "v2", "uploads", "images", "files",
        "css", "js", "assets", "static", "media", "content",
        "private", "secret", "hidden", "temp", "tmp"
    ]

    with open("basic_wordlist.txt", "w", encoding='utf-8') as f:
        for dir_name in basic_dirs:
            f.write(f"{dir_name}\n")

    print("📝 Created basic_wordlist.txt with common directories")

# 🔥 วิธีใช้งาน
async def main():
    target = input("🎯 Enter target URL (e.g., http://example.com): ")

    # เช็คว่ามี wordlist หรือไม่
    wordlist_path = input("📋 Enter wordlist path (or press Enter for basic): ").strip()

    if not wordlist_path or not Path(wordlist_path).exists():
        print("📝 Creating basic wordlist...")
        create_basic_wordlist()
        wordlist_path = "basic_wordlist.txt"

    threads = int(input("🔥 Number of threads (default 50): ") or "50")

    bruter = BrutalDirBrute(target, wordlist_path, threads)
    await bruter.run_bruteforce()

if __name__ == "__main__":
    asyncio.run(main())
