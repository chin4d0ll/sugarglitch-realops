#!/usr/bin/env python3
"""
🔧 FIX HTTP 429 & CSRF TOKEN ERRORS
แก้ไขปัญหา Rate Limit และ CSRF Token Extraction Failed
"""

import time
import random
import requests
from fake_useragent import UserAgent


class FixHTTP429AndCSRF:
    """แก้ไขปัญหา HTTP 429 และ CSRF Token"""

    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.last_request_time = 0

    def get_fresh_session(self):
        """สร้าง session ใหม่ที่สะอาด"""
        self.session = requests.Session()

        # Headers ที่เหมือน browser จริงๆ
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }

        self.session.headers.update(headers)
        return self.session

    def smart_delay(self, attempt_number):
        """Intelligent delay ตาม attempt number"""
        # เพิ่ม delay ตาม attempt
        base_delay = 5  # 5 วินาที base

        if attempt_number <= 10:
            delay = base_delay + random.uniform(2, 5)
        elif attempt_number <= 50:
            delay = base_delay + random.uniform(5, 15)
        elif attempt_number <= 100:
            delay = base_delay + random.uniform(15, 30)
        else:
            delay = base_delay + random.uniform(30, 60)

        print(f"⏰ Smart delay: {delay:.1f} วินาที (attempt #{attempt_number})")
        time.sleep(delay)

    def get_csrf_token_safely(self, max_retries=5):
        """ดึง CSRF token แบบปลอดภัย"""
        for retry in range(max_retries):
            try:
                print(f"🔄 ดึง CSRF token (ครั้งที่ {retry + 1}/{max_retries})")

                # สร้าง session ใหม่
                session = self.get_fresh_session()

                # Delay ก่อน request
                if retry > 0:
                    delay = min(30 + (retry * 15), 120)  # Max 2 นาที
                    print(f"⏰ รอ {delay} วินาทีก่อน retry...")
                    time.sleep(delay)

                # Request หน้า login
                response = session.get(
                    'https://www.instagram.com/accounts/login/',
                    timeout=30,
                    allow_redirects=True
                )

                if response.status_code == 200:
                    # หา CSRF token
                    content = response.text

                    # Method 1: จาก meta tag
                    import re
                    csrf_match = re.search(r'"csrf_token":"([^"]+)"', content)
                    if csrf_match:
                        csrf_token = csrf_match.group(1)
                        print(
                            f"✅ CSRF token ดึงได้สำเร็จ: {csrf_token[:10]}...")
                        return csrf_token, session

                    # Method 2: จาก window._sharedData
                    shared_data_match = re.search(
                        r'window\._sharedData = ({.+?});', content)
                    if shared_data_match:
                        import json
                        try:
                            shared_data = json.loads(
                                shared_data_match.group(1))
                            csrf_token = shared_data.get(
                                'config', {}).get('csrf_token')
                            if csrf_token:
                                print(
                                    f"✅ CSRF token จาก _sharedData: {csrf_token[:10]}...")
                                return csrf_token, session
                        except:
                            pass

                elif response.status_code == 429:
                    print(f"🚨 HTTP 429 Rate Limited (retry {retry + 1})")
                    continue
                else:
                    print(f"❌ HTTP {response.status_code}: {response.reason}")

            except requests.exceptions.Timeout:
                print(f"⏰ Timeout (retry {retry + 1})")
            except requests.exceptions.ConnectionError:
                print(f"🌐 Connection error (retry {retry + 1})")
            except Exception as e:
                print(f"❌ Error: {e} (retry {retry + 1})")

        print("❌ ไม่สามารถดึง CSRF token ได้")
        return None, None

    def check_rate_limit_status(self):
        """ตรวจสอบสถานะ rate limit"""
        try:
            # Request ง่ายๆ เพื่อเช็ค
            response = requests.get(
                'https://www.instagram.com/',
                timeout=10,
                headers={'User-Agent': self.ua.random}
            )

            if response.status_code == 200:
                print("✅ ไม่มี rate limit - พร้อมใช้งาน")
                return True
            elif response.status_code == 429:
                print("🚨 ยังโดน rate limit อยู่")
                return False
            else:
                print(f"⚠️ HTTP {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ ไม่สามารถเช็คได้: {e}")
            return False

    def wait_for_rate_limit_reset(self):
        """รอให้ rate limit หาย"""
        print("🕐 รอให้ rate limit reset...")

        # 1m, 2m, 5m, 10m, 20m, 30m
        wait_times = [60, 120, 300, 600, 1200, 1800]

        for wait_time in wait_times:
            print(f"⏰ รอ {wait_time//60} นาที...")
            time.sleep(wait_time)

            if self.check_rate_limit_status():
                print("✅ Rate limit หายแล้ว!")
                return True

        print("❌ Rate limit ยังไม่หาย - ลองใหม่ภายหลัง")
        return False


def main():
    """ฟังก์ชันหลักสำหรับแก้ปัญหา"""
    print("🔧 HTTP 429 & CSRF TOKEN ERROR FIXER")
    print("=" * 50)

    fixer = FixHTTP429AndCSRF()

    # 1. เช็คสถานะปัจจุบัน
    print("\n📊 ตรวจสอบสถานะปัจจุบัน:")
    if not fixer.check_rate_limit_status():
        print("\n🚨 ตรวจพบ Rate Limit!")

        choice = input("รอให้ rate limit หายไหม? (y/N): ")
        if choice.lower() == 'y':
            if fixer.wait_for_rate_limit_reset():
                print("✅ พร้อมใช้งานแล้ว!")
            else:
                print("❌ ยังไม่พร้อม")
                return

    # 2. ทดสอบดึง CSRF token
    print("\n🔑 ทดสอบดึง CSRF token:")
    csrf_token, session = fixer.get_csrf_token_safely()

    if csrf_token:
        print(f"✅ สำเร็จ! CSRF Token: {csrf_token[:20]}...")

        # 3. แนะนำขั้นตอนต่อไป
        print("\n💡 ขั้นตอนต่อไป:")
        print("1. ใช้ CSRF token นี้สำหรับ login attempts")
        print("2. รอ 2-5 นาทีระหว่าง attempts")
        print("3. เปลี่ยน User-Agent ทุกครั้ง")
        print("4. ใช้ VPN หรือเปลี่ยน IP")

        # 4. แสดงรหัสผ่านที่ควรลองก่อน
        print("\n🎯 รหัสผ่านแนะนำสำหรับ alx.trading:")
        priority_passwords = [
            "4l3x.7r4dlng2025",    # ตัวที่ดึง CSRF ได้
            "4l3x7r4dlng2025",     # ไม่มีจุด
            "Alex.Trading2025",     # ปกติ
            "alex.trading2025",     # lowercase
            "AlxTrading2025",       # ไม่มีจุด
        ]

        for i, pwd in enumerate(priority_passwords, 1):
            print(f"   {i}. {pwd}")

        print("\n⚠️ วิธีแก้ปัญหา HTTP 429:")
        print("• รอ 30-60 นาทีระหว่าง attempts")
        print("• ใช้ VPN เปลี่ยน IP")
        print("• ลดจำนวน attempts ต่อชั่วโมง")
        print("• ใช้ proxy servers")
        print("• ลองผ่าน mobile app แทน")

    else:
        print("❌ ไม่สำเร็จ")
        print("\n💡 วิธีแก้:")
        print("1. รอ 1-2 ชั่วโมง")
        print("2. เปลี่ยน IP/VPN")
        print("3. ลองใหม่ในเวลาต่าง")
        print("4. ใช้ browser ปกติเข้า Instagram ก่อน")


if __name__ == "__main__":
    main()
